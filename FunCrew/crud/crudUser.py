from extensions import db
from database import *
from flask import Blueprint, request
# from werkzeug.security import check_password_hash

user_bp = Blueprint('user', __name__)


# 登入
@user_bp.route('/login', methods=['POST'])
def login(jsonData):
    # 從 JSON 中提取使用者資料
    email = jsonData.get('email')
    password = jsonData.get('password')

    # 檢查必要欄位是否存在
    if not (email and password):
        return {'error': '缺少必要欄位'}, 400
    # 在資料庫中查詢使用者
    user = User.query.filter_by(email= email).first()
    # 檢查使用者是否存在並且密碼是否正確
    if user and check_password_hash(user.password, password):
        # 如果登入成功，回傳成功訊 息
        return {'message': '登入成功'}, 200
    else:
        # 如果登入失敗，回傳錯誤訊息
        return {'error': '無效的憑證'}, 401




# 建立使用者
@user_bp.route('/signup', methods=['POST'])
def register():
    if request.method == "POST":
        jsonData = request.get_json()
    # 讀取使用者資訊
    password = jsonData.get('password')
    nickname = jsonData.get('nickname')
    gender = jsonData.get('gender')
    age = jsonData.get('age')
    reputation_score = jsonData.get('reputationScore')
    cellphone = jsonData.get('cellphone')
    email = jsonData.get('email')
    # 檢查必要欄位是否存在
    if not (password and nickname and gender):
        return {'error': 'Missing required fields'}, 400
    # 檢查性別選項是否合法
    gender_options = [option[0] for option in User.genderOption]
    if gender not in gender_options:
        return {'error': 'Invalid gender'}, 400
    # 檢查使用者名稱是否已存在
    existingUser = User.query.filter_by(nickname = nickname).first()
    if existingUser:
        return {'error': 'User with this nickname already exists'}, 400
    # 如果 reputationScore 不存在，將其設置為預設值 100
    if reputation_score is None or reputation_score == '':
        reputation_score = 100
    # 建立新使用者
    user = User(
        password = password,
        nickname = nickname,
        gender = gender,
        age = age,
        reputationScore = reputation_score,
        cellphone = cellphone,
        email = email
    )

    try:
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201
    except Exception as e:
        return {'error': str(e)}, 500


# 使用者更新資料
@user_bp.route("/update",methods = ['POST'])
def updateUser(jsonData):
    if request.method == "POST":
        jsonData = request.get_json()
    # 讀取使用者資訊
    nickname = jsonData.get('nickname')
    password = jsonData.get('password')
    gender = jsonData.get('gender')
    age = jsonData.get('age')
    reputation_score = jsonData.get('reputationScore')
    cellphone = jsonData.get('cellphone')
    email = jsonData.get('email')
    # 首先找到要更新的用戶
    user = User.query.filter_by(nickname=nickname).first()
    # 如果找不到用戶，則返回一個錯誤
    if user is None:
        return {'error': 'User not found'}, 404
    # 更新用戶資訊
    if password is not None:
        user.password = password
    if gender is not None:
        user.gender = gender
    if age is not None:
        user.age = age
    if reputation_score is not None:
        user.reputationScore = reputation_score
    if cellphone is not None:
        user.cellphone = cellphone
    if email is not None:
        user.email = email
    # 儲存更新
    try:
        db.session.commit()
        return {'message': 'User updated successfully'}, 200
    except Exception as e:
        return {'error': str(e)}, 500



# 使用者更新密碼




# 刪除使用者
@user_bp.route("/delete",methods = ['POST'])
def deleteUser(jsonData):
    if request.method == "POST":
        jsonData = request.get_json()
    # 讀取使用者資訊
    nickname = jsonData.get('nickname')
    # 檢查必要欄位是否存在
    if not nickname:
        return {'error': 'Missing required field'}, 400
    # 查詢使用者
    user = User.query.filter_by(nickname=nickname).first()
    if not user:
        return {'error': 'User not found'}, 404

    try:
        # 刪除使用者並提交更改
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}, 200
    except Exception as e:
        return {'error': str(e)}, 500

# 忘記密碼
@user_bp.route("/forgetPassword",methods = ['POST'])
def forgetePassword(jsonDict):
    pass


# 聯繫客服
@user_bp.route("/help",methods = ['POST'])
def help(jsonDict):
    pass



# 個人資訊
@user_bp.route("/info",methods = ['POST'])
def myInfo(jsonDict):
    pass


# 他人資訊
@user_bp.route("/otherInfo",methods = ['POST'])
def otherInfo(jsonDict):
    pass
