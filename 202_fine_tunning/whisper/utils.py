'''Utilities for fine-tunning
'''

import pickle
from random import shuffle
import pandas as pd
import numpy as np
import librosa as lr
import soundfile as sf
import os
from tqdm import tqdm

class PrepareDataset:
    def __init__(self, audio_dir: str = './data/audio') -> None:
        self.VOICE_DIR = audio_dir
   

    def pcm2audio(
        self,
        audio_path: str,
        ext: str = 'wav',
        save_file: bool = True,
        remove: bool = False, # Keep original audio file
    ) -> object:
        '''참고 블로그: https://noggame.tistory.com/15'''
        buf = None
        with open(audio_path, 'rb') as tf:
            buf = tf.read()
            # zero (0) padding
            # 경우에 따라서 PCM 파일의 길이가 8bit(1byte)로
            # 나누어 떨어지지 않는 경우가 있어 0으로 패딩을 더해준다.
            # 패딩하지 않으면 numpy나 librosa 사용 시 오류가 날 수 있다.
            buf = buf+b'0' if len(buf)%2 else buf
        pcm_data = np.frombuffer(buf, dtype='int16')
        wav_data = lr.util.buf_to_float(x=pcm_data, n_bytes=2)
        
        # 음성 파일을 변환하여 저장: .pcm -> .wav
        if save_file:
            save_file_name = audio_path.replace('.pcm', f'.{ext}')
            sf.write(
                file=save_file_name,
                data=wav_data,
                samplerate=16000,
                format='WAV',
                endian='LITTLE',
                subtype='PCM_16'
            )
        
        # 파일 삭제 옵션일 경우에는 .pcm 파일 삭제
        if remove:
            if os.path.isfile(audio_path):
                os.remove(audio_path)
        
        return wav_data
    
    
    def process_audio(
        self,
        source_dir: str,
        remove_original_audio: bool = True
    ) -> None:
        '''.pcm 파일을 .wav 파일로 변환한 후 현재 디렉토리에 저장'''
        print(f'source_dir: {source_dir}')
        sub_directories = sorted(os.listdir(source_dir))
        print(f'Processing audios: {len(sub_directories)} directories')
        for directory in tqdm(sub_directories, desc=f'Processing directory: {source_dir}'):
            if os.path.isdir(directory):
                files = os.listdir(os.path.join(source_dir, directory))
                for file_name in files:
                    if file_name.endswith('.pcm'):
                        self.pcm2audio(
                            audio_path=os.path.join(source_dir, directory, file_name),
                            ext='wav',
                            remove=remove_original_audio,
                        )
            else:
                file_name = directory
                if file_name.endswith('.pcm'):
                    self.pcm2audio(
                        audio_path=os.path.join(source_dir, file_name),
                        ext='wav',
                        remove=remove_original_audio,
                    )

            
    def convert_text_utf(self, file_path: str) -> None:
        '''파일 인코딩 변경: cp494 -> utf-8로 변환하여 저장'''
        try:
            with open(file_path, 'rt', encoding='cp949') as f:
                lines = f.readlines()
        except:
            with open(file_path, 'rt', encoding='utf-8') as f:
                lines = f.readlines()
        with open(file_path, 'wt', encoding='utf-8') as f:
            for line in lines:
                f.write(line)


    def convert_all_files_to_utf8(self, target_dir: str) -> None:
        '''디렉토리 내부의 모든 텍스트 파일을 utf-8 인코딩으로 변경'''
        print(f'Target directory: {target_dir}')
        sub_directories = sorted(os.listdir(target_dir))
        num_files = 0
        for directory in tqdm(sub_directories, desc='converting cp949 -> utf8'):
            files = sorted(os.listdir(os.path.join(target_dir, directory)))
            for file_name in files:
                if file_name.endswith('.txt'):
                    self.convert_text_utf(
                        os.path.join(target_dir, directory, file_name)
                    )
                    num_files += 1
        print(f'{num_files} txt files are converted.')
        print('Done!')


    def split_whole_data(self, target_file:str) -> None:
        '''전체 데이터 파일 (train.trn)을 그룹별로 구분
        For example, in train.trn file
            KsponSpeech_01/KsponSpeech_0001/KsponSpeech_000001.pcm :: 'some text'
                -> this file will be stored in train_KsponSpeech_01.trn
            KsponSpeech_02/KsponSpeech_0001/KsponSpeech_000002.pcm :: 'some text'
                -> this file will be stored in train_KsponSpeech_02.trn
        '''
        with open(target_file, 'rt') as f:
            lines = f.readlines()
            data_group = set()
            for line in lines:
                data_group.add(line.split('/')[0])
        data_group = sorted(list(data_group))
        data_dic = { group: [] for group in data_group} # dict comprehension
        for line in lines:
            data_dic[line.split('/')[0]].append(line)
        # Save file seperately
        # target_file: data/info/train.trn -> ['data', 'info', 'train.trn']
        save_dir = target_file.split('/')[:-1]
        save_dir = '/'.join(save_dir)
        for group, line_list in data_dic.items():
            file_path = os.path.join(save_dir, f'train_{group}.trn')
            with open(file_path, 'wt', encoding='utf-8') as f:
                for text in line_list:
                    f.write(text)
                print(f'File created -> {file_path}')
        print('Done!')


    def get_dataset_dict(self, file_name: str, ext: str = 'wav') -> dict:
        '''path_dir에 있는 파일을 dict 형태로 가공하여 리턴
            return data_dic = {
                        'audio': ['file_path1', 'file_path2', ...],
                        'text': ['text1', 'text2', ...]
            }'''
        data_dic = {'path': [], 'sentence': []}
        print(f'file_name: {file_name}')
        with open(file_name, 'rt', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                audio, text = line.split('::')
                audio = audio.strip()
                audio = os.path.join(
                    os.getcwd(), # '/home/kafa46/finetune-tutorial'
                    self.VOICE_DIR.replace('./', ''), # './data/audio' -> 'data/audio'
                    audio
                )
                if audio.endswith('.pcm'):
                    audio = audio.replace('.pcm', f'.{ext}')
                text = text.strip()
                data_dic['path'].append(audio)
                data_dic['sentence'].append(text)
        return data_dic
        

    def save_trn_to_pkl(self, file_name: str) -> None:
        '''.trn 파일을 dict로 만든 후 .pkl 바이너리로 그냥 저장(dump)'''
        data_dict = self.get_dataset_dict(file_name)
        # pickle file dump
        file_name_pickle = file_name + '.dic.pkl'
        with open(file_name_pickle, 'wb') as f:
            pickle.dump(data_dict, f)
        print(f'Dataset is saved via dictionary pickle')
        print(f'Dataset path: {file_name_pickle}')


    def save_trn_to_csv(self, file_name: str) -> None:
        '''.trn 파일을 .csv로 저장'''
        data_dic = self.get_dataset_dict(file_name)
        file_name_csv = file_name.split('.')[:-1]
        file_name_csv = ''.join(file_name_csv) + '.csv'
        if file_name.startswith('.'):
            file_name_csv = '.' + file_name_csv
        data_df = pd.DataFrame(data_dic)
        data_df.to_csv(file_name_csv, index=False, header=False)
        print(f'Dataset is saved via csv')
        print(f'Dataset path: {file_name_csv}')        


    def split_train_test(self, 
        target_file: str, 
        train_size: float = 0.8
    ) -> None:
        '''입력 파일(.trn)을 train/test 분류하여 저장
            if train_size is 0.8,
                train:test = 80%:20%
        '''
        with open(target_file, 'rt') as f:
            data = f.readlines()
            train_num = int(len(data) * train_size)
        # If you set header (header=True) in csv file, you need following codes
        # header = None
        # if target_file.endswith('.csv'):
        #     header = data[0]
        #     data = data[1:]
        #     train_num = int(len(data)*train_size)
        shuffle(data)
        data_train = sorted(data[0:train_num])
        data_test = sorted(data[train_num:])
        
        # train_set 파일 저장
        train_file = target_file.split('.')[:-1]
        train_file = ''.join(train_file) + '_train.csv' 
        if target_file.startswith('.'):
            train_file = '.' + train_file
        with open(train_file, 'wt', encoding='utf-8') as f:
            for line in data_train:
                f.write(line)
        print(f'Train_dataset saved -> {train_file} ({train_size*100:.1f}%)')
        
        # test_set 파일 저장
        test_file = target_file.split('.')[:-1]
        test_file = ''.join(test_file) + '_test.csv' 
        if target_file.startswith('.'):
            test_file = '.' + test_file
        with open(test_file, 'wt', encoding='utf-8') as f:
            for line in data_test:
                f.write(line)
        print(f'Test_dataset saved -> {test_file} ({(1.0-train_size)*100:.1f}%)')


    def remove_all_text_files(self, target_dir: str, ext: str = 'txt') -> None:
        '''디렉토리 내부의 모든 특정 형태의 파일(in our case, txt)을 삭제'''
        print(f'Target directory: {target_dir}')
        sub_directories = sorted(os.listdir(target_dir))
        num_files = 0
        for directory in tqdm(sub_directories, desc=f'Delete all {ext} files'):
            files = os.listdir(os.path.join(target_dir, directory))
            for file_name in files:
                if file_name.endswith(f'.{ext}'):
                    os.remove(
                        os.path.join(target_dir, directory, file_name)
                    )
                    num_files += 1
        print(f'Removed {num_files} txt files')
        print('Done!')
    
    
if __name__=='__main__':
    # audio = 'data/audio/KsponSpeech_01/KsponSpeech_0001/KsponSpeech_000001.pcm'
    # prepareds = PrepareDataset()
    # prepareds.pcm2audio(audio_path=audio, remove=True)
    # source_dir = 'data/audio/KsponSpeech_01'
    # prepareds = PrepareDataset()
    # prepareds.process_audio(source_dir=source_dir)
    # text_file = 'data/audio/KsponSpeech_01/KsponSpeech_0001/KsponSpeech_000004.txt'
    # target_dir = 'data/audio/KsponSpeech_01'
    # target_file = './data/info/train_KsponSpeech_0.csv'
    # prepareds = PrepareDataset()
    # data_dict = prepareds.get_dataset_dict(target_file)
    # print(data_dict)
    # prepareds.save_trn_to_csv(target_file)
    # target_dir = 'data/audio/KsponSpeech_01'
    # prepareds.remove_all_text_files(target_dir)
    pass
    