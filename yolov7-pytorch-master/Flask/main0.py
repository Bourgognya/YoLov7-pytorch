from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


# MySql datebase
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:gary131464035@127.0.0.1:3306/oyster"

oyster = SQLAlchemy(app)

class Product(oyster.Model):
    __tablename__ = 'Product'
    pid = oyster.Column(oyster.Integer, primary_key=True)
    name = oyster.Column(oyster.String(30), unique=True, nullable=False)
    weight = oyster.Column(oyster.String(10), nullable=False)
    meat_weight = oyster.Column(oyster.Float, nullable=False)
    size= oyster.Column(oyster.Float, nullable=True)
    insert_time = oyster.Column(oyster.DateTime, default=datetime.now)
    update_time = oyster.Column(oyster.DateTime, onupdate=datetime.now, default=datetime.now)


    def __init__(self, name, weight, meat_weight, size):
        self.name = name
        self.weight = weight
        self.meat_weight = meat_weight
        self.size= size
#讀取txt
path = 'output.txt'
f = open(path, 'r')
i,num=0,0
for line in f.readlines():
    num+=int(line)*(10**(2-i))
    i+=1
f.close()
print(num)
 
# 模型( model )定義
# class Product(db.Model):
#     __tablename__ = 'product'
#     pid = db.Column(db.Integer, primary_key=True)
#     name = db.Column(
#         db.String(30), unique=True, nullable=False)
#     price = db.Column(db.Integer, nullable=False)
#     img = db.Column(
#         db.String(100), unique=True, nullable=False)
#     description = db.Column(
#         db.String(255), nullable=True)
#     state = db.Column(
#         db.String(10), nullable=True)
#     insert_time = db.Column(db.DateTime, default=datetime.now)
#     update_time = db.Column(
#         db.DateTime, onupdate=datetime.now, default=datetime.now)


#     def __init__(self, name, price, img, description, state):
#         self.name = name
#         self.price = price
#         self.img = img
#         self.description = description
#         self.state = state

# # # Add data
product_max = Product('Oyster2',num,0.0,10.0)
oyster.session.add(product_max)
oyster.session.commit()

# Read data
# query = Product.query.filter_by(name='Tom123').first()
# print(query.name)
# print(query.price)
# print(query.img)


# 可以用動態參數傳入
# filters = {'name': 'Tom123', 'price': 5555}
# query = Product.query.filter_by(**filters).first()

# #補充排序
# Product.query.filter_by(name='MTom123').order_by("value desc")

#刪除資料
# query = Product.query.filter_by(name='jen').first()
# db.session.delete(query)
# db.session.commit()

# Updata data
# query = Product.query.filter_by(name='Max').first()
# # 將 price 修改成 10 塊
# query.price = 10
# db.session.commit()

@app.route('/')
def index():
    # Create data
    oyster.create_all()
    return 'ok'


if __name__ == "__main__":
    app.run(debug=True)