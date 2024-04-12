'''Config for flask app (server)'''

import os
from secret import csrf_token_secrete

BASE_DIR = os.path.dirname(__file__)

# Seret key for CSRF token
SECRET_KEY = csrf_token_secrete

# File transfer config
UPLOAD_FILE_DIR = 'server/static/files/upload/'
TEMP_FILE_DIR = 'server/static/files/temp/'

# TODO
# Database config