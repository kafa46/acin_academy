# OpenAI whisper 모델 Finetunning

여기는 ACIN Academy에서 제공하는 Open Courses 중에서 `ACIN-202. Fine-tuning using Transfer Learning (전이학습을 이용한 파인 튜닝)` 과정에 대한 내용을 정리한 페이지 입니다.

## Useful Links
- ACIN Academy 전체과정 보기: 바로가기 ([click me](https://github.com/kafa46/acin_academy/))
- 개인 홈페이지: [click me](https://prof.acin.kr)
- YouTube Channel: [Jump to Youtube](https://www.youtube.com/@kafa46)
- Email (primary): <a href="mailto:kafa46@cju.ac.kr">kafa46@cju.ac.kr</a>
- Email (alternative): <a href="mailto:kafa46@gmail.com">kafa46@gmail.com</a>

## OpenAI Whisper 모델 파인 튜닝

- 참고: 전체 소스코드는 시리즈가 완료되면 추가 예정입니다.

|분야|주제|Youtube|Slides|Codes|
|---|---|---|---|---|
|OT|01. Orientation|[click](https://youtu.be/Q7SqTAH0pHk)|[link](https://github.com/kafa46/acin_academy/blob/master/202_fine_tunning/whisper/slides/01_orientation.pdf)|없음|
|전처리|02. Dataset Acquisition (데이터 확보)|[click](https://youtu.be/tqqJbk_JK8k)|[link](https://github.com/kafa46/acin_academy/blob/master/202_fine_tunning/whisper/slides/02_dataset_processing.pdf)|[codes](https://github.com/kafa46/acin_academy/blob/master/202_fine_tunning/whisper)|
|전처리|03. 음성 파일 변환(`.pcm` &rarr; `.wav`)|[click](https://youtu.be/pstczQsOVSU)|없음|[codes](https://github.com/kafa46/acin_academy/blob/master/202_fine_tunning/whisper)|
|전처리|04. Argparse를 이용한 audio 처리를 위한 하부 명령어 (sub-command) 등록 및 터미널 arguments 등록|[click](https://youtu.be/reE3YscH34c)|없음|[codes](https://github.com/kafa46/acin_academy/blob/master/202_fine_tunning/whisper)|
|전처리|05. 데이터셋 텍스트 파일 인코딩을 utf-8로 통일|[click](https://youtu.be/ruLlrIzZG6Q)|없음|[codes](https://github.com/kafa46/acin_academy/blob/master/202_fine_tunning/whisper)|
|전처리|06. 큰 학습 데이터셋을 작은 그룹으로 나누기|[click](https://youtu.be/uumj5-A5LTI)|없음|[codes](https://github.com/kafa46/acin_academy/blob/master/202_fine_tunning/whisper)|
|전처리|07. 데이터셋을 .csv 또는 pickle 파일로 저장하기|[click](https://youtu.be/8hpeplbENK8)|없음|[codes](https://github.com/kafa46/acin_academy/blob/master/202_fine_tunning/whisper)|
|전처리|08. csv 또는 pickle 저장 기능을 argparse에 등록하기|[click](https://youtu.be/oiUKGI8Z28k)|없음|[codes](https://github.com/kafa46/acin_academy/blob/master/202_fine_tunning/whisper)|
|전처리|09. 학습데이터를 Train/Test set으로 분할하는 기능 구현|[click](https://youtu.be/RDdxueGw1rY)|없음|[codes](https://github.com/kafa46/acin_academy/blob/master/202_fine_tunning/whisper)|
|전처리|10. 폴더 내부 모든 특정 파일 삭제 기능 구현, 모든 기능을 argpase에 등록하기|[click](https://youtu.be/1jtU6p4BSnE)|없음|[codes](https://github.com/kafa46/acin_academy/blob/master/202_fine_tunning/whisper)|
|Finetune|11. (Finetune) Plan of Attack against Whisper fine-tune(모델 파인 튜팅을 위한 공격/구현 계획)|[click](https://youtu.be/_bTNp6PaeXI)|[link](https://github.com/kafa46/acin_academy/blob/master/202_fine_tunning/whisper/slides/11_finetune_strategy_attack_plan.pdf)|없음|
|Finetune|12. (Finetune) 파인튜닝에 필요한 폴더/파일 생성, 필요한 패키지 설치|[click](https://youtu.be/lHActMFrWa4)|없음|없음|
|Finetune|13. (Finetune) 긴급 수정 ㅠㅠ - ".csv" 데이터 파일 header(제목줄) 추가|[click](https://youtu.be/Gby9Hfjt1DU)|없음|없음|
|Finetune|14. (Finetune) Trainer 클래스의 load_dataset 메서드 구현 및 argparse 등록|[click](https://youtu.be/P9dw_xLxpZw)|없음|없음|
|Finetune|15. (Finetune) whisper 모델 종류 및 디렉토리 구조를 __init__ 함수에 초기화 해주기|[click](https://youtu.be/iOaU--mAmf0)|없음|없음|
|Finetune|16. (Finetune) whisper tokenizer, feature extractor, processor 등록(로딩), .cache 폴더 확인 하기|[click](https://youtu.be/0ST_zq5cUWQ)|없음|없음|
|Finetune|17. (Finetune) whisper prepare_dataset 및 process_dataset 구현|[준비중]()|없음|없음|
|Finetune|계속 추가 예정 ^^|-|-|-|
