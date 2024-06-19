from flask import (
    Blueprint,
    render_template,
)

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    '''메인 페이지'''
    return render_template('main.html')