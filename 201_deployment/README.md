# ACIN Academy에 방문하신 것을 환영합니다. <a id='top'></a>

여기는 ACIN Academy에서 제공하는 Open Courses 중에서 `ACIN-201. Service Deployment (서비스 배포)` 과정에 대한 내용을 정리한 페이지 입니다.

## Useful Links
- ACIN Academy 전체과정 보기: 바로가기 [(click me)](https://github.com/kafa46/acin_academy)
- 꼰대 교수님 유튜브: 바로가기 [(click me)](https://www.youtube.com/@kafa46)
- 꼰대 교수님 개인 홈페이지: 바로가기 [(click me)](https://prof.acin.kr/)

## ACIN-201. Service Deployment (서비스 배포) 구성
- [Chapter 1. 딥러닝 배포 서버 구축](#server)
- [Chapter 2. 서버 모니터링(백엔드 처리 상태)](#monitoring)
- [Chapter 3. OpenAI Whisper - Local Live ASR](#local_live_asr)
- [Chapter 4. OpenAI Whisper - Client-server-based File ASR Service](#cs-file-asr)
<hr>

### Chapter 1. 딥러닝 배포 서버 구축 <a id='server'></a>
|분야|주제|Youtube|Slides|Codes|
|---|---|---|---|---|
|웹 서버|01. 오리엔테이션 및 가상 환경 구축|[click](https://youtu.be/VQChvFGhxrE)|[link](https://github.com/kafa46/acin_academy/blob/master/01_deployment/01_web_server/01_web_server.pdf)|[codes](https://github.com/kafa46/acin_academy/tree/master/01_deployment/01_web_server)|
|웹 서버|02. 폴더 구조 생성, 설정파일 작성, Main Controller (main_view), 블루프린트 등록|[click](https://youtu.be/gBR3FvEIang)|[link](https://github.com/kafa46/acin_academy/blob/master/01_deployment/01_web_server/01_web_server.pdf)|[codes](https://github.com/kafa46/acin_academy/tree/master/01_deployment/01_web_server)|
|웹 서버|03. 프런트 템플릿 작성(base.htm, main.html)|[click](https://youtu.be/tv5swAHtqhk)|[link](https://github.com/kafa46/acin_academy/blob/master/01_deployment/01_web_server/01_web_server.pdf)|[codes](https://github.com/kafa46/acin_academy/tree/master/01_deployment/01_web_server)|
|웹 서버|04. 파일첨부 기능 지원을 위한 JavaScript 코딩 (파일 추가, 파일 검증)|[click](https://youtu.be/nM7DrE3okHA)|[link](https://github.com/kafa46/acin_academy/blob/master/01_deployment/01_web_server/01_web_server.pdf)|[codes](https://github.com/kafa46/acin_academy/tree/master/01_deployment/01_web_server)|
|웹 서버|05. 파일처리 부가기능, 비동기 Ajax 통신 구현, 백엔드 파일처리|[click](https://youtu.be/Ly31-ow14rc)|[link](https://github.com/kafa46/acin_academy/blob/master/01_deployment/01_web_server/01_web_server.pdf)|[codes](https://github.com/kafa46/acin_academy/tree/master/01_deployment/01_web_server)|

[맨위로 이동](#top)
<hr>

### Chapter 2. 서버 모니터링(백엔드 처리 상태) <a id='monitoring'></a>
|분야|주제|Youtube|Slides|Codes|
|---|---|---|---|---|
|서버 모니터링|01. 딥러닝 배포 서버 모니터링 필요성, 접근방법, 목표 시스템|[click](https://youtu.be/qP_Vt4tXWX0)|[link](https://github.com/kafa46/acin_academy/blob/master/201_deployment/03_whisper_local_live_asr/slides/01_whisper_local_live_asr_attack_plan.pdf)|[codes](https://github.com/kafa46/acin_academy/tree/master/01_deployment/02_progressbar)|
|서버 모니터링|02. 의존성 설치, progress-bar 코딩, 프런트 websocket 코딩|[click](https://youtu.be/jDD9191v_GA)|[link](https://github.com/kafa46/acin_academy/blob/master/01_deployment/02_progressbar/01_progress_bar.pdf)|[codes](https://github.com/kafa46/acin_academy/tree/master/01_deployment/02_progressbar)|
|서버 모니터링|03. 백엔드 코딩(run_server.py, run.sh, \__init__.py 수정), 서버 작동 확인|[click](https://youtu.be/4FoSOLBUxfk)|[link](https://github.com/kafa46/acin_academy/blob/master/01_deployment/02_progressbar/01_progress_bar.pdf)|[codes](https://github.com/kafa46/acin_academy/tree/master/01_deployment/02_progressbar)|
|서버 모니터링|04. Progress-bar 및 결과창 동적 처리|[click](https://youtu.be/1R5Q8gA2NMg)|[link](https://github.com/kafa46/acin_academy/blob/master/01_deployment/02_progressbar/01_progress_bar.pdf)|[codes](https://github.com/kafa46/acin_academy/tree/master/01_deployment/02_progressbar)|
|서버 모니터링|05. 다중 접속, 다중 사용자 처리|[click](https://youtu.be/qM_pdELVXhA)|[link](https://github.com/kafa46/acin_academy/blob/master/01_deployment/02_progressbar/01_progress_bar.pdf)|[codes](https://github.com/kafa46/acin_academy/tree/master/01_deployment/02_progressbar)|

[맨위로 이동](#top)
<hr>

### Chapter 3. OpenAI Whisper - Local Live ASR <a id='local_live_asr'></a>
|분야|주제|Youtube|Slides|Codes|
|---|---|---|---|---|
|ASR|01. Local Live ASR 구현을 위한 오리엔테이션 (Attack Plan)|[click](https://youtu.be/M2feOKAoXTc)|[link](https://github.com/kafa46/acin_academy/blob/master/201_deployment/03_whisper_local_live_asr/slides/01_whisper_local_live_asr_attack_plan.pdf)|없음|
|ASR|02. 프로젝트 폴더구조 생성, finetuned model 복사, audio_io 구현|[click](https://youtu.be/WcDYe3rswI4)|없음|[codes](https://github.com/kafa46/acin_academy/tree/master/201_deployment/03_whisper_local_live_asr)|
|ASR|03. VAD 코드 분석 및 vad.py 작성|[click](https://youtu.be/DQW0cqXYa6Q)|없음|[codes](https://github.com/kafa46/acin_academy/tree/master/201_deployment/03_whisper_local_live_asr)|
|ASR|04. Entry point main.py 코딩 (argparser 포함)|[click](https://youtu.be/4NqRilfuTpA)|없음|[codes](https://github.com/kafa46/acin_academy/tree/master/201_deployment/03_whisper_local_live_asr)|
|ASR|05. 전이학습 모델 로딩을 위한 models/whisper.py 코딩|[click](https://youtu.be/KXcZLEuxMA4)|없음|[codes](https://github.com/kafa46/acin_academy/tree/master/201_deployment/03_whisper_local_live_asr)|
|ASR|06. VAD 및 Whisper 모델 연동, 미니 프로젝트 #2 마무리 인사|[click](https://youtu.be/cWp4vaPGeww)|없음|[codes](https://github.com/kafa46/acin_academy/tree/master/201_deployment/03_whisper_local_live_asr)|


[맨위로 이동](#top)
<hr>

### Chapter 4. OpenAI Whisper - Client-server-based File ASR Service <a id='cs-file-asr'></a>
|분야|주제|Youtube|Slides|Codes|
|---|---|---|---|---|
|ASR-CS|01. 클라이언트-서버 기반 File ASR 서비스 구현 오리엔테이션 (Attack Plan)|[click](https://youtu.be/0tXTsIUNMOI)|[link](https://github.com/kafa46/acin_academy/blob/master/201_deployment/04_file_asr_no_socket/references/01_client-server_file_asr_no_socket.pdf)|없음|
|ASR-CS|02. 프로젝트 구조(폴더) 잡기, 기본 설정파일 코딩|[click](https://youtu.be/mSwujzcZ__A)|[link](https://github.com/kafa46/acin_academy/blob/master/201_deployment/04_file_asr_no_socket/references/01_client-server_file_asr_no_socket.pdf)|[codes](https://github.com/kafa46/acin_academy/tree/master/201_deployment/04_file_asr_no_socket)|
|ASR-CS|03. 프런트 구현 - base.html 및 main.html 코딩|[click](https://youtu.be/G4SVV7bppyg)|[link](https://github.com/kafa46/acin_academy/blob/master/201_deployment/04_file_asr_no_socket/references/01_client-server_file_asr_no_socket.pdf)|[codes](https://github.com/kafa46/acin_academy/tree/master/201_deployment/04_file_asr_no_socket)|
|ASR-CS|04. 서버 - 일부 views 구현, 서버 구동, base.html 업데이트|[click](https://youtu.be/wAw7TcEFpGw)|[link](https://github.com/kafa46/acin_academy/blob/master/201_deployment/04_file_asr_no_socket/references/01_client-server_file_asr_no_socket.pdf)|[codes](https://github.com/kafa46/acin_academy/tree/master/201_deployment/04_file_asr_no_socket)|

### Chapter XX(TBD). REST API
- 준비 중 (오픈되면 Update 예정)