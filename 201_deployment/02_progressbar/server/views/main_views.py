'''Main views'''

from asyncio import sleep
from datetime import datetime
from flask import (
    Blueprint,
    jsonify,
    render_template,
    request,
)
from werkzeug.utils import secure_filename
from server.forms import FileUploadForm
from config import UPLOAD_FILE_DIR

# Socket.io 글로벌 객체 import
from server import socketio

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    '''메인 페이지'''
    form = FileUploadForm()
    return render_template(
        'main.html',
        form = form,
    )
    # return 'hello ACINemy'

# # 이전 버전
# @bp.route('/process/', methods=['POST'])
# def process():
#     '''딥러닝 요청에 대한 처리'''
#     if request.method=='POST':
#         files = request.files.getlist('file')
#         for file in files:
#             print(f'file.name: {file.filename}')
#             prefix_name = f"{datetime.utcnow().strftime('%y%m%d_%H_%M_%S.%f')}_."
#             safe_filename = prefix_name + secure_filename(file.filename)
#             print(f'safe_filename: {safe_filename}')
#             file.save(UPLOAD_FILE_DIR + safe_filename)
#         # 딥러닝 알고리즘 실행
#         # 결과를 클라이언트에게 전달
#         return jsonify(
#             {'content': '딥러닝 처리 성공~~\n축하드려요^^.'}
#         )
#     return jsonify(
#             {'content': 'fail'}
#     )


# 비동기처리: async, await 적용해야 함
@bp.route('/process/<socket_id>', methods=['POST'])
async def process(socket_id):
    '''딥러닝 요청에 대한 처리'''
    if request.method=='POST':
        files = request.files.getlist('file')
        for file in files:
            print(f'file.name: {file.filename}')
            prefix_name = f"{datetime.now().strftime('%y%m%d_%H_%M_%S.%f')}_."
            safe_filename = prefix_name + secure_filename(file.filename)
            print(f'safe_filename: {safe_filename}')
            file.save(UPLOAD_FILE_DIR + safe_filename)

        # 딥러닝 알고리즘 실행
        # 딥러닝 학습 -> epoch 10회 수행한다고 가정
        NUM_EPOCH = 10
        for x in range(10):
            # Socket.io 통신
            percent = (x+1)/NUM_EPOCH * 100
            print(f'percent: {percent}%')
            socketio.emit('process_status', percent, to=socket_id)
            await sleep(2)

        # 결과를 클라이언트에게 전달
        return jsonify(
            {'content': '딥러닝 처리 성공~~\n축하드려요^^.'}
        )

    return jsonify(
            {'content': 'fail'}
    )

