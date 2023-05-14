from extensions import db
from database import *

# 建立使用者
def createUser(jsonData):
    # 擷取 JSON 數據中的使用者資訊
    password = jsonData.get('password')
    role = jsonData.get('role')
    nickname = jsonData.get('nickname')
    gender = jsonData.get('gender')
    age = jsonData.get('age')
    reputation_score = jsonData.get('reputationScore')
    cellphone = jsonData.get('cellphone')
    email = jsonData.get('email')
    # 檢查必要欄位是否存在
    if not (password and role and nickname and gender):
        return {'error': 'Missing required fields'}, 400
    # 檢查性別選項是否合法
    gender_options = [option[0] for option in User.genderOption]
    if gender not in gender_options:
        return {'error': 'Invalid gender'}, 400
    # 檢查使用者名稱是否已存在
    existingUser = User.query.filter_by(nickname=nickname).first()
    if existingUser:
        return {'error': 'User with this nickname already exists'}, 400
    # 如果 reputationScore 不存在，將其設置為預設值 100
    if reputation_score is None or reputation_score == '':
        reputation_score = 100
    # 建立新使用者
    user = User(
        password=password,
        role=role,
        nickname=nickname,
        gender=gender,
        age=age,
        reputationScore=reputation_score,
        cellphone=cellphone,
        email=email
    )

    try:
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201
    except Exception as e:
        return {'error': str(e)}, 500


# 使用者登入驗證

# 使用者更新資料

# 使用者更新密碼

# 刪除使用者
def deleteUser(jsonData):
    # 擷取 JSON 數據中的使用者名稱
    nickname = jsonData.get('nickname')
    # 檢查必要欄位是否存在
    if not nickname:
        return {'error': 'Missing required field'}, 400
    # 查詢使用者
    user = User.query.filter_by(nickname=nickname).first()
    # 如果找不到該使用者
    if not user:
        return {'error': 'User not found'}, 404

    try:
        # 刪除使用者並提交更改
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}, 200
    except Exception as e:
        return {'error': str(e)}, 500

