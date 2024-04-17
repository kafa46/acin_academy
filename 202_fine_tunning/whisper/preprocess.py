'''
한국어 음성대화 데이터셋 전처리
subcommand
    - audio
    - file
'''

import argparse
from utils import PrepareDataset


def audio_process(config) -> None:
    print('Start audio processing')
    preprocessor = PrepareDataset()
    preprocessor.process_audio(
        source_dir=config.target_dir,
        remove_original_audio=config.remove_original_audio,
    )


def file_process(config) -> None:
    print('Start file processing')
    preprocessor = PrepareDataset()
    if config.target_file:
        if not (
            config.csv or
            config.pkl or
            config.split_whole_data or
            config.split_train_test
        ):
            print(f'If --target-file (-t) is feed, \
one of --csv, --pkl, --split-train-test (-s) or \
--split-whole-data (-w) must be set.')
            return
        if config.csv:
            preprocessor.save_trn_to_csv(config.target_file)
        if config.pkl:
            preprocessor.save_trn_to_pkl(config.target_file)
        if config.split_whole_data:
            preprocessor.split_whole_data(config.target_file)
        if config.split_train_test:
            preprocessor.split_train_test(
                target_file=config.target_file,
                train_size=config.ratio
            )
    if config.convert_all_to_utf:
        if not config.target_dir:
            print('If --convert-all-to-utf8 (-c) flagged, you must feed --target-dir')
        preprocessor.convert_all_files_to_utf8(config.target_dir)
    if config.remove_all_text_files:
        if not config.target_dir:
            print(f'If --remove-all-text-files (-R) flagged,\
                    you must feed --target-dir')
            return
        preprocessor.remove_all_text_files(
            target_dir=config.target_dir,
            ext=config.remove_file_type
        )
    
    
def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='Korean speech dataset pre-processor',
        description='Process Korean speech dataset'
    )
    sub_parser = parser.add_subparsers(title='sub-command')
    
    ### Parser for sub-command 'audio' ###
    parser_audio = sub_parser.add_parser(
        'audio',
        help='sub-command for audio processing'
    )
    parser_audio.add_argument(
        '--target-dir', '-t',
        required=True,
        help='directory of audio files'
    )
    parser_audio.add_argument(
        '--remove-original-audio', '-r',
        action='store_true',
        help='Remove original audio files'
    )
    parser_audio.set_defaults(func=audio_process)
    
    ### Parser for sub-command 'file' ###
    parser_file = sub_parser.add_parser(
        'file',
        help='handling txt encoding, generate pkl/csv file,\
            or split file (train/test)'
    )
    parser_file.add_argument(
        '--target-file', '-t',
        # required=True,
        help='Target file name for processing'
    )
    parser_file.add_argument(
        '--convert-all-to-utf', '-c',
        action='store_true',
        help='Convert all text files to utf-8 under target_dir'
    )
    parser_file.add_argument(
        '--target-dir', '-d',
        # required=True,
        help='Target directory for converting file encoding to utf-8\
            Use by combining --convert-all-to-utf (-c) flag'
    )
    parser_file.add_argument(
        '--split-whole-data', '-w',
        action='store_true',
        help='Split whole data file int group'
    )
    parser_file.add_argument(
        '--csv',
        action='store_true',
        help='Generate csv file'
    )
    parser_file.add_argument(
        '--pkl',
        action='store_true',
        help='Generate pickle file'
    )
    parser_file.add_argument(
        '--split-train-test', '-s',
        action='store_true',
        help='Flag split train/test set, \
              default: 0.8 (train:test -> 80:20)'
    )
    parser_file.add_argument(
        '--ratio',
        type=float,
        default=0.8,
        help='Split file into .train & .test files'
    )
    parser_file.add_argument(
        '--remove-all-text-files', '-R',
        action='store_true',
        help='Remove all specific type files under target dir'
    )
    parser_file.add_argument(
        '--remove-file-type',
        default='txt',
        help='Set remove file type'
    )
    
    parser_file.set_defaults(func=file_process)
    config = parser.parse_args()
    return config


if __name__=='__main__':
    config = get_parser()
    config.func(config)
    