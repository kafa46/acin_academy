import os

from datetime import datetime
from flask import (
    Blueprint,
    jsonify,
    render_template,
    request,
)
from werkzeug.utils import secure_filename
from config import UPLOAD_FILE_DIR
from server.forms import FileUploadForm
# from ai_asr.inferece import WhisperInference
from server import whisper

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
    # user_id 추출
    user_id = request.json['user_id']
    print(f'user_id in process: {user_id}')
    if not user_id:
        return jsonify({
                'status': 'fail',
                'contents': '사용자 식별에 실패했습니다.\n다시 시도해 주세요 ㅠ'
            })
    
    # 업로드 된 음성 파일 가져오기
    target_dir = os.path.join(UPLOAD_FILE_DIR, user_id)
    audio_files = os.listdir(target_dir)
    if len(audio_files) == 0:
        return jsonify({
                'status': 'fail',
                'contents': '서버에 처리할 파일이 없네요ㅠㅠ.\n다시 시도해 주세요 ㅠ'
            })
    # ASR 인공지능 수행
    result_dic = {}
    result_dic['length'] = len(audio_files)
    for idx, audio in enumerate(audio_files):
        # ASR Processing
        # transcript = 'OpenAI whisper에서 꼰대 교수님 최고~~~'
        target_file = os.path.join(target_dir, audio)
        transcript = whisper.inference(target_file)
        transcript = transcript.replace('/', '')
        transcript = transcript.replace('. ', '.\n\n')
        result_dic[f'{idx}'] = transcript
    
    print(f'result_dic: {result_dic}')
    
    return jsonify(result_dic)