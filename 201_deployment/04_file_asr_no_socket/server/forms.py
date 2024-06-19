'''사용자 데이터(.mp3) 수신을 위한 Form 정의'''

from flask_wtf import FlaskForm
from wtforms import MultipleFileField
from wtforms.validators import DataRequired

class FileUploadForm(FlaskForm):
    '''사용자로부터 파일을 전송받을 폼'''
    files = MultipleFileField(
        '첨부파일',
        validators=[DataRequired()]
    )