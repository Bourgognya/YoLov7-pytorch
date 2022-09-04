from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/getname", methods=['GET'])
def getname():
    name = request.args.get('name')
    return render_template('get.html',**locals())
    
if __name__ == '__main__':
    app.run()
