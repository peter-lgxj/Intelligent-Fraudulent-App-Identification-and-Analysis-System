from flask import Flask, render_template,request, abort, send_file
from flask_socketio import SocketIO, emit
import eventlet
from src.Domain import Domain
import json
# from flask_restx import Api, Resource

app = Flask(__name__)

socketio = SocketIO(app)

class allineed:
    flag=False
    ends=True
    d=Domain()

a=allineed()

@app.route('/start')
def startss():
    a.flag=True
    print(a.flag)
    return "start"

def background_main_thread():
    while a.ends:
        eventlet.sleep(2)
        print("=======================waiting========================")
        if a.flag:
            print("begin")
            
            socketio.emit('my_event', {'msg': 'starting get src'}, namespace='/test')
            a.d.get_src()
            print("\033[92msuccessfully get src\033[92m")
            print("\033[97m \033[97m")
            socketio.emit('my_event', {'msg': 'successfully get src'}, namespace='/test')
            # eventlet.sleep(2)
            
            socketio.emit('my_event', {'msg': 'starting get basic info'}, namespace='/test')
            f=a.d.get_basic_info()
            print("\033[92msuccessfully get basic info\033[92m")
            print("\033[97m \033[97m")
            socketio.emit('my_event', {'msg': 'successfully get basic info', 'data':f}, namespace='/test')
            # eventlet.sleep(2)
            
            socketio.emit('my_event', {'msg': 'starting get judge res, type:roy(red/orange/yellow)'}, namespace='/test')
            t=a.d.get_judge_res('roy')
            print("\033[92msuccessfully get judge res roy\033[92m")
            print("\033[97m \033[97m")
            socketio.emit('my_event', {'msg': 'successfully get type:roy', 'data':t}, namespace='/test')
            # eventlet.sleep(2)
            
            socketio.emit('my_event', {'msg': 'starting get judge res, type:scg(sex/scam/gamble)'}, namespace='/test')
            t=a.d.get_judge_res('scg')
            print("\033[92msuccessfully get judge res scg\033[92m")
            print("\033[97m \033[97m")
            socketio.emit('my_event', {'msg': 'successfully get type:scg', 'data':t}, namespace='/test')
            # eventlet.sleep(2)
            
            socketio.emit('my_event', {'msg': 'starting get url,ip,domain'}, namespace='/test')
            a.d.get_uid(a.d.result_path)
            print("\033[92msuccessfully get uid\033[92m")
            print("\033[97m \033[97m")
            socketio.emit('my_event', {'msg': 'successfully get uid', 'data':a.d.uid}, namespace='/test')
            # eventlet.sleep(2)
            
            socketio.emit('my_event', {'msg': 'starting fetch packet fake'}, namespace='/test')
            a.d.fetch_pack_fake()
            print("\033[92msuccessfully fetch pack fake\033[92m")
            print("\033[97m \033[97m")
            socketio.emit('my_event', {'msg': 'successfully fetch pack fake','data':a.d.backstage}, namespace='/test')
            # eventlet.sleep(2)
            
            socketio.emit('my_event', {'msg': 'starting produce out file'}, namespace='/test')
            a.d.produce_out_file()
            print("\033[92msuccessfully produce out file\033[92m")
            print("\033[97m \033[97m")
            with open("./templates/output.html", 'w', encoding='utf-8') as file:
                file.write(a.d.html_obj)
            socketio.emit('my_event', {'msg': 'successfully produce out file, please press display button'}, namespace='/test')
            
            # eventlet.sleep(2)
            a.ends=False
            a.flag=False
            # break


@socketio.on('connect',namespace='/test')
def test_connect():
    print("====================客户端已连接=======================")
    a.ends=True
    eventlet.spawn_n(background_main_thread)  
    emit('my定时事件', {'data': '客户端已连接'})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print("====================客户端已断开=======================")
    a.ends=False
    a.flag=False
    print(False)
    # 在这里可以添加你希望在客户端断开连接时执行的逻辑

@app.route('/test')
def index():
    return render_template('index.html')

@app.route('/upload_apk', methods=['POST'])
def upload_apk():
    if request.method == 'POST':
        print("request received:upload_apk")
        print("uploadloading apk")
        print(request.files['file'])
        print(request.files['file'].filename)
        try:
            file = request.files['file']#[0]
            file_path = f'./apks/{file.filename}'
            a.d.apkname=file.filename
            file.save(file_path)
            print("upload completed")
            # a.ends=True
            return "success"
        except Exception as e:
            return "error"


@app.route('/display')
def download_file():
    # 指定文件所在的目录
    try:
        print("displaying")
        # 使用 send_file 函数发送文件
        return render_template('output.html')
    except FileNotFoundError:
        # 如果文件不存在，返回 404 错误
        abort(404)
        
if __name__ == '__main__':
    socketio.run(app,host='127.0.0.1',port=5000, debug=False)
