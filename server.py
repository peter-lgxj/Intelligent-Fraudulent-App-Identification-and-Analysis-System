from flask import Flask, render_template,request, abort
from flask_socketio import SocketIO, emit
import eventlet
from src.Domain import Domain
import json
# from flask_restx import Api, Resource

app = Flask(__name__)

socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")

class allineed:
    flag=False
    ends=True
    only_one=True
    d=Domain()

a=allineed()

@app.route('/start')
def startss():
    a.flag=True
    print(a.flag)
    return "start"

def background_main_thread():
    while a.ends:
        eventlet.sleep(5)
        print("=======================waiting========================")
        # socketio.emit('my_event', {'msg': 'waiting'}, namespace='/test')
        
        if a.flag:
            eventlet.sleep(3)
            socketio.emit('my_event', {'msg': 'starting get src'}, namespace='/test')
            eventlet.sleep(3)
            print("begin")
            
            a.d.get_src()
            print("\033[92msuccessfully get src\033[92m")
            print("\033[97m \033[97m")
            socketio.emit('my_event', {'msg': 'successfully get src'}, namespace='/test')
            eventlet.sleep(3)
            
            socketio.emit('my_event', {'msg': 'starting get basic info'}, namespace='/test')
            eventlet.sleep(3)
            f=a.d.get_basic_info()
            a.d.permission_analysis()
            print("\033[92msuccessfully get basic info\033[92m")
            print("\033[97m \033[97m")
            socketio.emit('my_event', {'msg': 'successfully get basic info', 'data':f}, namespace='/test')
            eventlet.sleep(3)
            socketio.emit('my_event', {'msg': 'successfully done permission analyze', 'data':a.d.permission_infos}, namespace='/test')
            eventlet.sleep(3)
            
            socketio.emit('my_event', {'msg': 'starting get judge res, type:(black/grey/white)'}, namespace='/test')
            eventlet.sleep(3)
            t=a.d.get_judge_res('roy')
            roy=t
            print(roy)
            print(type(roy))
            print("\033[92msuccessfully get judge res roy\033[92m")
            print("\033[97m \033[97m")
            socketio.emit('my_event', {'msg': 'successfully get type:roy', 'data':t}, namespace='/test')
            eventlet.sleep(3)
            
            if roy != "white":
                socketio.emit('my_event', {'msg': 'starting get judge res, type:scg(sex/scam/gamble)'}, namespace='/test')
                eventlet.sleep(3)
                t=a.d.get_judge_res('scg')
                
                print("\033[92msuccessfully get judge res scg\033[92m")
                print("\033[97m \033[97m")
                socketio.emit('my_event', {'msg': 'successfully get type:scg', 'data':t}, namespace='/test')
                eventlet.sleep(3)
            else:
                a.d.type="normal"
            
            socketio.emit('my_event', {'msg': 'starting get url,ip,domain'}, namespace='/test')
            eventlet.sleep(3)
            a.d.get_uid(a.d.result_path)
            print("\033[92msuccessfully get uid\033[92m")
            print("\033[97m \033[97m")
            socketio.emit('my_event', {'msg': 'successfully get uid', 'data':a.d.uid}, namespace='/test')
            eventlet.sleep(3)
            
            
            socketio.emit('my_event', {'msg': 'starting fetch packet fake'}, namespace='/test')
            eventlet.sleep(3)
            a.d.fetch_pack_fake()
            print("\033[92msuccessfully fetch pack fake\033[92m")
            print("\033[97m \033[97m")
            socketio.emit('my_event', {'msg': 'successfully fetch pack fake','data':a.d.backstage}, namespace='/test')
            eventlet.sleep(3)
            
            socketio.emit('my_event', {'msg': 'starting produce out file'}, namespace='/test')
            eventlet.sleep(3)
            a.d.produce_out_file()
            print("\033[92msuccessfully produce out file\033[92m")
            print("\033[97m \033[97m")
            with open("./templates/output.html", 'w', encoding='utf-8') as file:
                file.write(a.d.html_obj)
            socketio.emit('my_event', {'msg': 'successfully produce out file, please press display button'}, namespace='/test')
            eventlet.sleep(3)
            # eventlet.sleep(2)
            a.ends=False
            a.flag=False
            break


@socketio.on('connect',namespace='/test')
def test_connect():
    print("====================客户端已连接=======================")
    a.ends=True
    if a.only_one:
        eventlet.spawn_n(background_main_thread)
        a.only_one=False 
    emit('my_event', {'data': '客户端已连接'},namespace='/test')


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print("====================客户端已断开=======================")
    emit('my_event', {'data': '客户端已断开'},namespace='/test')
    a.ends=False
    a.flag=False
    a.only_one=True
    print(False)


@app.route('/tests')
def index():
    return render_template('index4.html')

@app.route('/upload_apk', methods=['POST'])
async def upload_apk():
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
            # emit('upload_apk', {'msg': 'successfully upload apk file, please press start button'}, namespace='/test')
            # eventlet.sleep(3)
            # a.ends=True
            return "success"
        except Exception as e:
            return "error"


@app.route('/display')
async def download_file():
    # 指定文件所在的目录
    try:
        print("displaying")
        # 使用 send_file 函数发送文件
        return render_template('output.html')
    except FileNotFoundError:
        # 如果文件不存在，返回 404 错误
        abort(404)
        
if __name__ == '__main__':
    socketio.run(app,host='127.0.0.1',port=5000, debug=False, allow_unsafe_werkzeug=True)
