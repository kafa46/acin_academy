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
    
    
    