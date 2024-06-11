'''음성 검출하기(VAD: Voice Activity Detection)
    - VAD: 오디오 데이터에서 사람의 음성이 존재하는지를 검출
    - 입력 오디오 데이터에 음성이 있을 경우에만 whisper에 넘겨주어 
        transcription을 할 수 있도록 하기 위해 사용한다.
    - packages
        py-webrtcvad: https://github.com/wiseman/py-webrtcvad
        pypi: https://pypi.org/project/webrtcvad/
    - References
        https://github.com/snakers4/silero-vad/tree/master/examples/microphone_and_webRTC_integration
        
        Errors in "pip install webrtcvad"
            Failed to build webrtcvad
            ERROR: Could not build wheels for webrtcvad, which is required to install pyproject.toml-based projects
        Try:
            https://stackoverflow.com/questions/75003495/error-could-not-build-wheels-for-prophet-which-is-required-to-install-pyprojec
        Final solution:    
            pip install webrtcvad-wheels
'''

import collections, queue
import pyaudio
import webrtcvad


RATE_PROCESS = 16000

class Audio(object):
    """Streams raw audio from microphone.
    Data is received in a separate thread, 
    and stored in a buffer, to be read from.
    """
    def __init__(
        self, 
        callback=None, 
        device=None, 
        channels: int = 1,
        input_rate=RATE_PROCESS,
        blocks_per_second: int = 50,
    ):
        self.format = pyaudio.paInt16
        self.buffer_queue = queue.Queue()
        self.channels = channels
        self.device = device
        self.input_rate = input_rate
        self.rate_process = RATE_PROCESS
        self.sample_rate = RATE_PROCESS
        self.blocks_per_second = blocks_per_second
        self.block_size = int(self.rate_process / self.blocks_per_second)
        self.block_size_input = int(self.input_rate / self.blocks_per_second)
        self.pa = pyaudio.PyAudio()

        def proxy_callback(in_data, frame_count, time_info, status):
            callback(in_data)
            return (None, pyaudio.paContinue)
        
        if callback is None: 
            def callback(in_data):
                return self.buffer_queue.put(in_data)
        
        kwargs = {
            'format': self.format,
            'channels': self.channels,
            'rate': self.input_rate,
            'input': True,
            'frames_per_buffer': self.block_size_input,
            'stream_callback': proxy_callback,
        }
        
        # self.chunk = None
        
        if not self.device:
            kwargs['input_device_index'] = self.device
        self.stream = self.pa.open(**kwargs)
        self.stream.start_stream()

    def read(self):
        """Return a block of audio data, blocking if necessary."""
        return self.buffer_queue.get()

    def destroy(self):
        '''Stop streamming & terminate pyaudio object'''
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()

    frame_duration_ms = property(
        lambda self: 1000 * self.block_size // self.sample_rate
    )


class VADAudio(Audio):
    """Filter & segment audio 
    with voice activity detection.
    """

    def __init__(
        self, 
        aggressiveness: int = 3, 
        device:int = None, 
        input_rate: int = None
    ):
        super().__init__(device=device, input_rate=input_rate)
        self.vad = webrtcvad.Vad(aggressiveness)

    def frame_generator(self):
        """Generator that yields all audio frames from microphone."""
        if self.input_rate == self.rate_process:
            while True:
                yield self.read()
        else:
            raise Exception("Resampling required")

    def vad_collector(self, padding_ms=300, ratio=0.75, frames=None):
        """Generator that yields series of consecutive audio frames 
        comprising each utterence, separated by yielding a single None.
        Determines voice activity by ratio of frames in padding_ms. 
        Uses a buffer to include padding_ms prior to being triggered.
        Example: (frame, ..., frame, None, frame, ..., frame, None, ...)
                 |---utterence---|        |---utterence---|
        """
        if frames is None: 
            frames = self.frame_generator()
        num_padding_frames = padding_ms // self.frame_duration_ms
        ring_buffer = collections.deque(maxlen=num_padding_frames)
        
        triggered = False

        for frame in frames:
            if len(frame) < 640:
                return

            is_speech = self.vad.is_speech(frame, self.sample_rate)

            if not triggered:
                ring_buffer.append((frame, is_speech))
                num_voiced = len([f for f, speech in ring_buffer if speech])
                if num_voiced > ratio * ring_buffer.maxlen:
                    triggered = True
                    for f, s in ring_buffer:
                        yield f
                    ring_buffer.clear()

            else:
                yield frame
                ring_buffer.append((frame, is_speech))
                num_unvoiced = len([f for f, speech in ring_buffer if not speech])
                if num_unvoiced > ratio * ring_buffer.maxlen:
                    triggered = False
                    yield None
                    ring_buffer.clear()