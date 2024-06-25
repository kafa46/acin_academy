import os

from datetime import datetime
from flask import (
    Blueprint,
    render_template,
    request,
)
from werkzeug.utils import secure_filename
from config import UPLOAD_FILE_DIR
from server.forms import FileUploadForm

bp = Blueprint('asr_file', __name__, url_prefix='/asr_file')

@bp.route('/')
def index():
    '''메인 페이지'''
    form = FileUploadForm()
    return render_template(
        'asr_file.html',
        form=form,
    )
    
@bp.route('/upload/<user_id>', methods=['POST'])
def upload(user_id):
    # 파일 저장
    print(f'user_id: {user_id}')
    print('upodad func working')
    
    # 서버에 파일을 저장하는 코드를 작성해야 함
    user_upload_dir = os.path.join(UPLOAD_FILE_DIR, user_id)
    if not os.path.exists(user_upload_dir):
        os.mkdir(user_upload_dir)
    files = request.files.getlist('file')
    for file in files:
        print(f'file.name: {file.name}')
        prefix_name = f"{datetime.now().strftime('%y%m%d_%H_%M_%S.%f')}_."
        # "20280623_00_12_34.327_."
        safe_filename = prefix_name + secure_filename(file.filename)
        print(f'safe_filename: {safe_filename}')
        file.save(
            os.path.join(user_upload_dir, safe_filename)
        )
    return {
        'status': 'upload success',
    }

@bp.route('/process', methods=['POST'])
def process():
    # ASR 인공지능 수행
    return '결과 텍스트'