from flask import Flask
from flask import render_template
from flask import request
#在路由裡的method建立以GET為傳遞方式,
app = Flask(__name__)
@app.route("/getname", methods=['GET'])
def getname():
    name = request.args.get('name')
    return render_template('get.html',**locals())

if __name__ == "__main__":
    app.run(debug=True)