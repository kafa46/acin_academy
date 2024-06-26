'''Implementation of openai/whisper-large-v3
    Source: https://huggingface.co/openai/whisper-large-v3
Fine tuning:
    Source: https://huggingface.co/blog/fine-tune-whisper
'''

import torch
import os

from config import ASR_MODEL_DIR
from transformers import (
    AutoModelForSpeechSeq2Seq,
    AutoProcessor,
    pipeline,
)

class WhisperInference:
    def __init__(self) -> None:
        self.device: str = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.base_model: str = 'openai/whisper-medium'
        self.pretrained_model: str = os.path.join(ASR_MODEL_DIR, 'whisper-medium')
        self.torch_type: float = torch.float16 if torch.cuda.is_available() else torch.float32
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            pretrained_model_name_or_path=self.pretrained_model,
            torch_dtype=self.torch_type,
            use_safetensors=True,
            low_cpu_mem_usage=True,
            device_map=self.device,
            # Applying flash attention
            #   - https://huggingface.co/openai/whisper-large-v3/discussions/63
            attn_implementation="flash_attention_2",
        )
        self.processor = AutoProcessor.from_pretrained(self.base_model)
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            torch_dtype=self.torch_type
        )
    
    def inference(
        self,
        audio_file: str,
        lang: str = 'korean',
        task: str = 'transcribe'
    ) -> str:
        '''음성파일 -> 텍스트 추론 수행'''
        options = {
            "language": lang, 
            "task": task,
        }
        result = self.pipe(audio_file, generate_kwargs=options)
        
        if isinstance(result, dict):
            text = result['text']
        elif isinstance(result, list):
            text = ''
            for x in result:
                chunk_list = x['chunks']
                for chunk in chunk_list:
                    text += chunk['text']
        return text