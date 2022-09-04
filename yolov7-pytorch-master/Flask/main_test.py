from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# MySql datebase
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:gary131464035@127.0.0.1:3306/db"

db = SQLAlchemy(app)
# 模型( model )定義
class Product(db.Model):
    __tablename__ = 'product'
    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(10), nullable=False)
    insert_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)

    def __init__(self, name, price, img, description, state):
        self.name = name
        self.price = price
        self.img = img
        self.description = description
        self.state = state

@app.route('/add',methods=['GET'])
def add():
    name = request.args.get('name')
    price = int(request.args.get('price'))
    img = request.args.get('img')
    des = request.args.get('des')
    state = request.args.get('state')
    product = Product(name,price,img,des,state)
    db.session.add(product)
    db.session.commit()
    return 'ok'
    
@app.route('/')
def index():
    return 'home page'
    
# Create data
@app.route('/create')
def create():
    db.create_all()
    return 'ok'

if __name__ == "__main__":
    app.run(debug=True)