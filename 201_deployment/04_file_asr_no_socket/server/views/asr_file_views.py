from flask import (
    Blueprint,
    render_template,
)

bp = Blueprint('asr_file', __name__, url_prefix='/asr_file')

@bp.route('/')
def index():
    '''메인 페이지'''
    return render_template('asr_file.html')