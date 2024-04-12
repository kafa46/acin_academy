
'''ACIN Academy 딥러닝 서비스 배포용 웹'''

from flask import Flask
import config

def create_app() -> Flask:
    '''서비스 용 앱 생성'''
    app = Flask(__name__)
    app.config.from_object(config)

    # Blueprint 등록
    from .views import main_views
    app.register_blueprint(
        main_views.bp,
    )
    
    return app
