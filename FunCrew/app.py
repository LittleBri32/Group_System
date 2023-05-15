from flask import Flask, request, render_template, jsonify
import json
from flask_migrate import Migrate
from extensions import db
from crud.crudUser import *
from crud.crudActivity import *
from crud.crudPost import *


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/DBS/Final/Group_System/FunCrew/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    # 啟用調試模式，debug
    app.debug = True
    db.init_app(app)

    # 初始化 Flask-Migrat
    migrate = Migrate(app, db)  

    # Home
    @app.route("/",methods = ['GET'])
    def home():
        return render_template("home.html")
    
    # # 登入
    # @app.route("/user/signin",methods = ['POST'])
    # def login():
    #     if request.method == "POST":
    #         jsonDict = request.get_json()
    #         result, statusCode = loginUser(jsonDict)
    #         return jsonify(result)
    #     return jsonify({'error': 'The resource was not found'}), 404
    

    # 註冊
    @app.route("/user/signup",methods = ['POST'])
    def register():
        if request.method == "POST":
            jsonDict = request.get_json()
            result, statusCode = createUser(jsonDict)
            return jsonify(result)
        return jsonify({'error': 'The resource was not found'}), 404
    
    # 使用者更新資料
    @app.route("/user/update",methods = ['POST'])
    def modifyUser():
        if request.method == "POST":
            jsonDict = request.get_json()
            result, statusCode = updateUser(jsonDict)
            return jsonify(result)
        return jsonify({'error': 'The resource was not found'}), 404

    # 使用者更新密碼

    # 刪除使用者
    @app.route("/user/delete",methods = ['POST'])
    def removeUser():
        if request.method == "POST":
            jsonDict = request.get_json()
            result, statusCode = deleteUser(jsonDict)
            return jsonify(result)
        return jsonify({'error': 'The resource was not found'}), 404
    


    with app.app_context():
        db.create_all()
    return app

app = create_app()

