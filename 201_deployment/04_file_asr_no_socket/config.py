'''Config for flask app (server)'''

import os
from secret import csrf_token_secret

BASE_DIR = os.path.dirname(__file__)

# secret key for CSRF token
SECRET_KEY = csrf_token_secret

# file transfer config
UPLOAD_FILE_DIR = os.path.join(BASE_DIR, 'server/static/files/upload/')
TEMP_FILE_DIR = os.path.join(BASE_DIR, 'server/static/files/temp')

# ASR model upload directory (especially for Whisper model)
ASR_MODEL_DIR = os.path.join(BASE_DIR, 'ai_asr/models')

# ASR file (ex: .mp3) uploaded from client
CLIENT_AUDIO_UPLOAD_DIR = os.path.join(BASE_DIR, 'server/static/files/asr')

# TODO