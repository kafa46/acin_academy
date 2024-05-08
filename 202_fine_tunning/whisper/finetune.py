'''Fine-tuning whisper (possible: tiny, small, medium, etc.)
References:
    - Master reference -> https://huggingface.co/blog/fine-tune-whisper
    - Korean blog -> https://velog.io/@mino0121/NLP-OpenAI-Whisper-Fine-tuning-for-Korean-ASR-with-HuggingFace-Transformers
Written by: Prof. Giseop Noh
License: MIT license
'''

import argparse
import os
from pprint import pprint
import evaluate
import torch
import numpy as np
from datasets import load_dataset, DatasetDict
from trainer.collator import DataCollatorSpeechSeq2SeqWithPadding
from utils import get_unique_directory
from transformers import (
    WhisperFeatureExtractor,
    WhisperTokenizer,
    WhisperProcessor,
    WhisperForConditionalGeneration,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
)
from scipy.io.wavfile import read



def get_config():
    '''Whisper finetuning args parsing function'''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--base-model', '-b',
        required=True,
        help='Base model for tokenizer, processor, feature extractor. \
            Ex. "openai/whisper-tiny", "openai/whisper-small", etc. from huggingface'
    )
    parser.add_argument(
        '--pretrained-model', '-p',
        default='',
        help='Pre-treained model from huggingface or local computer. \
            If not given, we will set the modes same to --base-model (-b).'
    )
    parser.add_argument(
        '--output-dir', '-o',
        default='./model_output',
        help='Directory for saving whisper finetune outputs, default: "./model_output"'
    )
    parser.add_argument(
        '--finetuned-model-dir', '-ft',
        required=True,
        help='Directory for saving fine-tuned model (best model after train)'
    )
    ############
    parser.add_argument(
        '--train-set', '-t',
        required=True,
        help='Train dataset name (file name or file paht)'
    )
    parser.add_argument(
        '--valid-set', '-v',
        required=True,
        help='Validation dataset name (file name or file paht)'
    )
    parser.add_argument(
        '--test-set', '-e',
        required=True,
        help='Test dataset name (file name or file paht)'
    )
    parser.add_argument(
        '--lang',
        default='Korean',
        help='Language for fine-tuning, default: Korean'
    )
    parser.add_argument(
        '--task',
        default='transcribe',
        help='transcribe or translate, default: transcribe'
    )
    parser.add_argument(
        '--sample-rate',
        type=int,
        default=16000,
        help='sampling rate for voice(audio) file, default: 16,000'
    )
    parser.add_argument(
        '--metric',
        default='cer',
        help='evaluation metric (wer, cer, accuracy, ...), default: cer'
    )
    config = parser.parse_args()
    return config


class Trainer:
    '''Whisper finetune trainer'''

    def __init__(self, config) -> None:
        '''Init all required args for whisper finetune'''
        self.config = config

        # 사전 학습 모델 - 2개
        #   Base model -> tokenizer, feature_extractor, processor
        #   pre-trained model -> model for fine-tuning

        if config.pretrained_model:
            self.pretrained_model = config.pretrained_model
        else:
            print('\nPre-trained model is not given...')
            print(f'We will set pre-trained model same to --base-model (-b): {config.base_model}\n')
            self.pretrained_model = config.base_model

        self.output_dir = get_unique_directory(
            dir_name=config.output_dir,
            model_name=self.pretrained_model
        )
        self.finetuned_model_dir = get_unique_directory(
            dir_name=config.finetuned_model_dir,
            model_name=self.pretrained_model
        )
        print(f'\nTraining outputs will be saved -> {self.output_dir}')
        print(f'Fine-tuned model will be saved -> {self.finetuned_model_dir}\n')

        # Feature Extractor 등록
        self.feature_extractor = WhisperFeatureExtractor.from_pretrained(
            config.base_model
        )
        # Tokenizer 등록
        self.tokenizer = WhisperTokenizer.from_pretrained(
            pretrained_model_name_or_path=config.base_model,
            language=config.lang,
            task=config.task
        )
        # Processor 등록
        self.processor = WhisperProcessor.from_pretrained(
            pretrained_model_name_or_path=config.base_model,
            language=config.lang,
            task=config.task
        )
        # Model 생성/등록
        self.model = WhisperForConditionalGeneration.from_pretrained(self.pretrained_model)
        # Label Collator 등록
        self.data_collator = DataCollatorSpeechSeq2SeqWithPadding(
            processor=self.processor,
            decoder_start_token_id=self.model.config.decoder_start_token_id,
        )
        # Training args 등록
        self.training_args = Seq2SeqTrainingArguments(
            output_dir=self.output_dir,     # change to a repo name of your choice
            per_device_train_batch_size=16, # if you want, you can modify 16 -> 32 if GPU performance available
            gradient_accumulation_steps=1,  # increase by 2x for every 2x decrease in batch size
            learning_rate=1e-5,
            warmup_steps=500,               # Step concept 64 samples/epoch -> 32 samples/mini-batch, step 64/32 -> 2 steps
            # max_steps=5000,
            gradient_checkpointing=True,
            # https://jaeyung1001.tistory.com/entry/bf16-fp16-fp32%EC%9D%98-%EC%B0%A8%EC%9D%B4%EC%A0%90
            fp16=True,                      # 부동소수점 자리수 defalut: fp32 -> fp16 speed-up training
            evaluation_strategy="steps",
            per_device_eval_batch_size=8,   # if you want, you can modify 8 -> 16 -> 32 if GPU performance available
            predict_with_generate=True,
            generation_max_length=225,
            # 개인별 컴퓨팅 환경에 따라 적절하게 숫자 조정 가능
            save_steps=1000, # modify 1000 -> 2000
            eval_steps=1000, # modify 1000 -> 2000
            logging_steps=100, # modify 25 -> 100
            # report_to=["tensorboard"],
            load_best_model_at_end=True,
            metric_for_best_model=config.metric,
            greater_is_better=False,
            push_to_hub=False,
        )


    def load_dataset(self,) -> DatasetDict:
        '''Build dataset containing train/valid/test sets'''
        dataset = DatasetDict()
        dataset['train'] = load_dataset(
            path='csv',
            name='aihub-ko',
            split='train',
            data_files=self.config.train_set
        )
        dataset['valid'] = load_dataset(
            path='csv',
            name='aihub-ko',
            split='train',
            data_files=self.config.valid_set
        )
        dataset['test'] = load_dataset(
            path='csv',
            name='aihub-ko',
            split='train',
            data_files=self.config.test_set
        )
        return dataset


    def compute_metrics(self, pred) -> dict:
        '''Prepare evaluation metric (wer, cer, etc.)'''
        metric = evaluate.load(self.config.metric)
        # 음성인식(ASR) 모델 error 측정
        #   - wer: word error rate - school
        #   - cer: char error rate - 조사(접두어, 접미얼), 학교는, 학교에, 학교를....
        pred_ids = pred.predictions
        label_ids = pred.label_ids
        label_ids[label_ids == -100] = self.tokenizer.pad_token_id
        pred_str = self.tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
        label_str = self.tokenizer.batch_decode(label_ids, skip_special_tokens=True)
        error_rate = 100 * metric.compute(predictions=pred_str, references=label_str)
        return {f'{self.config.metric}': error_rate}


    def prepare_dataset(self, batch) -> object:
        '''Get input features with numpy array & sentence labels'''
        audio = batch["path"]
        _, data = read(audio)
        audio_array = np.array(data, dtype=np.float32)

        # compute log-Mel input features from input audio array
        batch["input_features"] = self.feature_extractor(
            audio_array,
            sampling_rate=config.sample_rate
        ).input_features[0]

        # encode target text to label ids
        batch["labels"] = self.tokenizer(batch["sentence"]).input_ids
        return batch


    def process_dataset(self, dataset: DatasetDict) -> tuple:
        '''Process loaded dataset applying prepare_dataset()'''
        print('\nStart train dataset mapping')
        print(dataset['train'])
        train = dataset['train'].map(
            function=self.prepare_dataset,
            remove_columns=dataset.column_names['train'],
            num_proc=8,
        )
        print('\nStart valid dataset mapping')
        print(dataset['valid'])
        valid = dataset['valid'].map(
            function=self.prepare_dataset,
            remove_columns=dataset.column_names['valid'],
            num_proc=8,
        )
        print('\nStart test dataset mapping')
        print(dataset['test'])
        test = dataset['test'].map(
            function=self.prepare_dataset,
            remove_columns=dataset.column_names['test'],
            num_proc=8,
        )
        return (train, valid, test)


    def enforce_fine_tune_lang(self) -> None:
        '''Enforce fine-tune language'''
        self.model.config.suppress_tokes = []
        self.model.generation_config.suppress_tokens = []
        # model config issue -> https://github.com/huggingface/transformers/issues/21994
        self.model.config.forced_decoder_ids = self.processor.tokenizer.get_decoder_prompt_ids(
            language=config.lang,
            task=config.task,
        )
        # generations_config issue -> https://github.com/huggingface/transformers/issues/21937
        self.model.generation_config.forced_decoder_ids = self.processor.tokenizer.get_decoder_prompt_ids(
            language=config.lang,
            task=config.task,
        )


    def create_trainer(self, train, valid) -> Seq2SeqTrainer:
        '''Create seq2seq trainer'''
        return Seq2SeqTrainer(
            args=self.training_args,
            model=self.model,
            train_dataset=train,
            eval_dataset=valid,
            data_collator=self.data_collator,
            compute_metrics=self.compute_metrics,
            tokenizer=self.processor.feature_extractor,
        )


    def run(self) -> None:
        '''Run trainer'''
        self.enforce_fine_tune_lang()
        dataset = self.load_dataset()
        train, valid, test = self.process_dataset(dataset=dataset)
        trainer = self.create_trainer(train, valid)
        print('\nStart training...\n')
        trainer.train()
        trainer.save_model(self.finetuned_model_dir)
        print('\nStart testing performance using test_dataset...\n')
        result_dic = trainer.evaluate(eval_dataset=test)
        pprint(result_dic)
        print('\nClearing GPU cache')
        torch.cuda.empty_cache()
        print('\nTraining completed!!!')


if __name__=='__main__':
    config = get_config()
    # trainer = Trainer(config)
    # dataset = trainer.load_dataset()
    # print(dataset)
    # print(dataset['train'][0])
    # print(dataset['train'][0]['sentence'])
    # input_str = dataset['train'][0]['sentence']
    # labels = trainer.tokenizer(input_str).input_ids
    # print(f'\ninput_str:\t {input_str}')
    # print(f'\nlabels:\t {labels}')
    # decoded_str_with_special_tokens = trainer.tokenizer.decode(labels, skip_special_tokens=False)
    # decoded_str_without_special_tokens = trainer.tokenizer.decode(labels, skip_special_tokens=True)
    # print(f'\ndecoded w/ special:\t {decoded_str_with_special_tokens}')
    # print(f'decoded w/o special:\t {decoded_str_without_special_tokens}\n')
    # print(f'\nIs equal:\t {input_str == decoded_str_without_special_tokens}')
    # print(dataset)
    # train, valid, test = trainer.process_dataset(dataset)
    # print(train)

    trainer = Trainer(config=config)
    trainer.run()

