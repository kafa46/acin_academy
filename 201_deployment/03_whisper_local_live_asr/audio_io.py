'''whisper streamming
    References
        - https://digging-on-bytes.com/whisper%EC%99%80-python%EC%9C%BC%EB%A1%9C-%EC%8B%A4%EC%8B%9C%EA%B0%84-%EB%B2%88%EC%97%AD%EA%B8%B0-%EB%A7%8C%EB%93%A4%EA%B8%B0-part1/
'''

import soundcard as sc


def select_mic() -> int:
    mics = sc.all_microphones(include_loopback=True)
    print('\n--------------------------------------------')
    print('사용 가능한 음성 입출력 장치 목록입니다.')
    print('--------------------------------------------')
    for idx, mic in enumerate(mics):
        try:
            print(f'\n{idx}: {mic.name}')
        except Exception as e:
            print(e)
    mic_idx = int(input('\n사용할 마이크를 입력해 주세요: '))
    print('\n')
    return mic_idx
    

if __name__=='__main__':
    select_mic()