from flask import (
    Blueprint,
    render_template,
)
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
    return 'message'

@bp.route('/process', methods=['POST'])
def process():
    # ASR 인공지능 수행
    return '결과 텍스트'