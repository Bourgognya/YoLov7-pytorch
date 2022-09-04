from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)  # 实例化，可视为固定格式
app.debug = True  # Flask内置了调试模式，可以自动重载代码并显示调试信息
app.config['JSON_AS_ASCII'] = False  # 解决flask接口中文数据编码问题

#设置可跨域范围
CORS(app, supports_credentials=True)

# 展示Flask如何读取服务器本地图片, 并返回图片流给前端显示的例子
def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    import base64
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream

# 跳转到html页面显示图片   app.route()为跳转路由，类似springboot
@app.route('/')
def hello_world():
  img_path = 'static/5.jpg'
  img_stream = return_img_stream(img_path)
  # render_template()函数是flask函数，它从模版文件夹templates中呈现给定的模板上下文。
  return render_template('index.html',img_stream=img_stream)

@app.route('/index')
def img():
  img_path = 'static/0.jpg'
  img_stream = return_img_stream(img_path)
  # render_template()函数是flask函数，它从模版文件夹templates中呈现给定的模板上下文。
  return render_template('index.html',img_stream=img_stream)


#   // 主函数
if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # 默认值：host="127.0.0.1", port=5000, debug=False
    app.run(host="127.0.0.1", port=5010)