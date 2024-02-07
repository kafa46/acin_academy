from server import create_app, socketio

app = create_app()

if __name__=='__main__':
    socketio.run(
        app=app,
        host='0.0.0.0',
        port='5678',
        debug=True,
    )