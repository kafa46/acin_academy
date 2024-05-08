# Whisper `finetuned_archive` 폴더

## 파인튜닝 완료된 모델은 아래 링크에서 받을 수 있습니다.
    - whisper-small (+ AI-hub 한국어 음성 파인튜닝)
    - whisper-medium (+ AI-hub 한국어 음성 파인튜닝)

## 다운로드 링크
    - 다운로드 링크
        - Finetuned whisper-small: [click me](https://drive.google.com/drive/folders/1Yy5VVGjLt6PgueA7sTU8mVqWL0yE9TpJ?usp=sharing)
        - Finetuned whisper-medium: [click me](https://drive.google.com/drive/folders/1SICxOhh79hnmIXPhRN7oJLrcF5QX6DVN?usp=sharing)

## 참고사항
    - 모델을 다운로드 받아서 `model_archive` 또는 `model_fintuned` 디렉토리에 복사하시면 됩니다.
    - 추론 단계에서 `--base-model` 옵션을 이용해 파인튜팅 된 모델과 base-model을 맞춰줘야 합니다.
    - (예시)
        - 파인 튜닝된 `whisper-small` 모델 적용 시 `--base-model openai/whisper-small` 적용
        - 파인 튜닝된 `whisper-medium` 모델 적용 시 `--base-model openai/whisper-medium` 적용