from flask import Flask, request, render_template, jsonify
from flask_migrate import Migrate
import json
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
    
    # User
    # ----------------------------------------------------------------
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
    
    # Activity
    # ----------------------------------------------------------------
    # 顯示所有活動
    @app.route("/activity/all",methods = ['POST'])
    def showAllActivities():
        if request.method == "POST":
            jsonDict = request.get_json()
            activityType = jsonDict.get('type', None)
            result, statusCode = showAllActivity(activityType)
            return jsonify(result)
        return jsonify({'error': 'The resource was not found'}), 404
    
    # 顯示使用者參加的活動
    @app.route("/activity/my",methods = ['POST'])
    def showMyActivities():
        if request.method == "POST":
            jsonDict = request.get_json()
            result, statusCode = showMyActivity(jsonDict)
            return jsonify(result)
        return jsonify({'error': 'The resource was not found'}), 404
    
    # 發起活動
    @app.route("/activity/create",methods = ['POST'])
    def hostActivities():
        if request.method == "POST":
            jsonDict = request.get_json()
            result, statusCode = createActivity(jsonDict)
            return jsonify(result)
        return jsonify({'error': 'The resource was not found'}), 404
    
    # 刪除活動
    @app.route("/activity/delete",methods = ['POST'])
    def callOffActivities():
        if request.method == "POST":
            jsonDict = request.get_json()
            result, statusCode = deleteActivity(jsonDict)
            return jsonify(result)
        return jsonify({'error': 'The resource was not found'}), 404
    
    # 更新活動
    @app.route("/activity/update",methods = ['POST'])
    def updateActivities():
        if request.method == "POST":
            jsonDict = request.get_json()
            result, statusCode = modifyActivity(jsonDict)
            return jsonify(result)
        return jsonify({'error': 'The resource was not found'}), 404
    
    # 加入活動
    @app.route("/activity/join",methods = ['POST'])
    def ParticipateActivities():
        if request.method == "POST":
            jsonDict = request.get_json()
            result, statusCode = joinActivity(jsonDict)
            return jsonify(result)
        return jsonify({'error': 'The resource was not found'}), 404

    # 退出活動
    @app.route("/activity/leave",methods = ['POST'])
    def withdrawActivities():
        if request.method == "POST":
            jsonDict = request.get_json()
            result, statusCode = leaveActivity(jsonDict)
            return jsonify(result)
        return jsonify({'error': 'The resource was not found'}), 404
    
    # 評分
    @app.route("/activity/rate",methods = ['POST'])
    def feedbackActivities():
        if request.method == "POST":
            jsonDict = request.get_json()
            result, statusCode = rateActivity(jsonDict)
            return jsonify(result)
        return jsonify({'error': 'The resource was not found'}), 404

    # 留言討論
    @app.route("/activity/discussion",methods = ['POST'])
    def discussActivities():
        if request.method == "POST":
            jsonDict = request.get_json()
            result, statusCode = engageActivity(jsonDict)
            return jsonify(result)
        return jsonify({'error': 'The resource was not found'}), 404


    with app.app_context():
        db.create_all()
    return app

app = create_app()

migrate = Migrate(app, db, render_as_batch = True)

