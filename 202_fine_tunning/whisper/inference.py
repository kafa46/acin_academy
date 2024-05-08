'''
Implementation of openai/whisper-large-v3
    Source: https://huggingface.co/openai/whisper-large-v3
Fine tuning:
    Source: https://huggingface.co/blog/fine-tune-whisper
'''

import torch
import argparse
from transformers import (
    AutoModelForSpeechSeq2Seq, 
    AutoProcessor, 
    pipeline,
)

def get_parser() -> argparse.Namespace:
    '''argument parser'''
    parser = argparse.ArgumentParser(prog='Whisper inference')
    parser.add_argument(
        '--base-model', '-b',
        required=True,
        help='Pretrained model from huggingface'
    )
    parser.add_argument(
        '--pretrained-model', '-p',
        required=True,
        help='Finetuned model directory'
    )
    parser.add_argument(
        '--audio-file', '-a',
        required=True,
        help='Audio (source) file for ASR processing'
    )
    parser.add_argument(
        '--lang',
        default='korean',
        help='Target language after processing, default: korean'
    )
    parser.add_argument(
        '--task',
        default='transcribe',
        help='ASR task: translate or transcribe, default: transcribe'
    )
    parser.add_argument(
        '--sample-rate',
        type=int,
        default=16000,
        help='Sampling rate for voice file, default: 16,000'
    )
    config = parser.parse_args()
    return config


class Inference:
    def __init__(self, config) -> None:
        self.config = config
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.torch_type = torch.float16 if torch.cuda.is_available() else torch.float32
        # Applying flash attention 
        # - Huggingface flash-attn 소개
        #   - flash-atten: https://huggingface.co/docs/transformers/main/en/perf_infer_gpu_one?install=NVIDIA
        # - How to apply flash-attn in huggingface
        #   - https://huggingface.co/openai/whisper-large-v3/discussions/63
        # - PyPI (Python Package Index) page -> You need to check the requirements & how to install using pip
        #   - https://pypi.org/project/flash-attn/
        # - github flash-attn -> You can get rich info on flash-attn 
        #   - https://github.com/Dao-AILab/flash-attention        
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            pretrained_model_name_or_path=self.config.pretrained_model, 
            torch_dtype=self.torch_type,
            low_cpu_mem_usage=True, 
            use_safetensors=True,
            device_map=self.device,
            attn_implementation='flash_attention_2'
        )
        # self.model.to(self.device)
        self.processor = AutoProcessor.from_pretrained(self.config.base_model)
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            torch_dtype=self.torch_type,
            # We can omit some optional args by applying default settings
            # max_new_tokens=128,
            chunk_length_s=30,
            # batch_size=16,
            # return_timestamps=True,
            # device=self.device,
        )
    
    def run(self) -> None:
        '''Perform inference'''
        options = {
            'language': self.config.lang,
            'task': self.config.task
        }
        result = self.pipe(self.config.audio_file, generate_kwargs=options, return_timestamps=True)
        if isinstance(result, dict):
            text = result['text']
        elif isinstance(result, list):
            text = ''
            for x in result:
                chunk_list = x['chunk']
                for chunk in chunk_list:
                    text += chunk['text']
        else:
            print('Type error.. ㅠㅠ')
        print(text)
                    
        

if __name__=='__main__':
    config = get_parser()
    inference = Inference(config)
    inference.run()