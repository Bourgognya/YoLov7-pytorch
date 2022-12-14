import os

from flask import Flask, render_template, Response, make_response
from camera import VideoCamera


app = Flask(__name__)

#相機推流
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#相機串流(攝影機)
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/video_feed2')
# def video_feed2():
#     return Response(gen(VideoCamera()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

#當前實時相機畫面
@app.route('/cur_camera')
def cur_camera():
    return render_template('cur_camer.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)