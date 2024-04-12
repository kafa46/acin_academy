from server import create_app, socketio

app = create_app()

if __name__=='__main__':
    # socketio.run(app=app, host='0.0.0.0', port='80', debug=True)
    socketio.run(app=app, host='127.0.0.1', port='5001', debug=True)
    # socketio.run(app=app, debug=True)
