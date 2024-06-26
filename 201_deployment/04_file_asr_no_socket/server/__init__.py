import config
from flask import Flask
from ai_asr.inferece import WhisperInference

# Create whisper objectr
whisper = WhisperInference()

def create_app() -> Flask:
    '''서비스용 앱 생성'''
    app = Flask(__name__)
    app.config.from_object(config)
    
    # Blueprint 등록
    from .views import main_views
    from .views import asr_file_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(asr_file_views.bp)
    
    return app
