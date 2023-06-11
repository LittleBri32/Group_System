from flask import Blueprint, request, render_template, session, redirect,url_for,flash,current_app
import sqlite3 as sql
import os
from werkzeug.utils import secure_filename





# 建立使用者
def createUser(jsonData):
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
def updateUser(jsonData):
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
        # 建立與資料庫的連線
        con = sql.connect("funCrew_db.db")
        cur = con.cursor()

        # 根據 userID 查詢使用者的暱稱
        cur.execute("SELECT nickname FROM User WHERE userID=?", (userID,))
        nickname = cur.fetchone()[0]

        # 關閉資料庫連線
        con.close()

        return nickname
    except Exception as e:
        return {'error': str(e)}, 500

import os
from werkzeug.utils import secure_filename


# 模組套件
user_bp = Blueprint("user", __name__)

# 此處為 user_bp 模組，所以路徑為 @user_bp.route("<>",)
# 在 html 引用時，需設路徑為 "/user/sign_in" 樣子


# 登入處理
@user_bp.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    # 建立與資料庫的連線
    con = sql.connect("funCrew_db.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        cur.execute(
            "SELECT * FROM User WHERE email=? and password=?", (email, password)
        )
        # 提交資料庫交易，確保將查詢結果寫入資料庫。
        con.commit()
        # 設定錯誤訊息
        msg = "帳號或密碼錯誤！"
        # 檢索所有符合查詢條件的資料，並將結果存儲在people變數中
        people = cur.fetchall()
        # 如果不符合查詢條件則在login登入介面顯示錯誤訊息
        if len(people) == 0:
            return render_template("login.html", msg=msg)
        cur.execute(
            "SELECT userID FROM User WHERE email=? and password=?",
            (
                email,
                password,
            ),
        )
        userID = cur.fetchone()[0]
        session["userID"] = userID
        ############################################# Gary
        try:
            cur.execute("DROP TABLE temp{}ViewCount".format(userID))
        except sql.OperationalError:
            pass
        cur.execute("CREATE TABLE temp{}ViewCount (postID INTEGER PRIMARY KEY)".format(userID))
        con.commit()
        con.close()
        #################################################################################
    # 點選登入btn後會切回home首頁
    return redirect("/home")


# 登出處理
@user_bp.route("/logout")
def logout():
    ##################################################################### Gary
    con = sql.connect("funCrew_db.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("DROP TABLE temp{}ViewCount".format(session["userID"]))
    ############################################################
    # 清除使用者的登入資訊
    session.pop("nickname", None)
    # 導向登入頁面
    return render_template("login.html")


    try:
        # 刪除使用者並提交更改
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}, 200
    except Exception as e:
        return {'error': str(e)}, 500

# 忘記密碼
def forgetedPassword(jsonDict):
    pass


# 聯繫客服
def helpMe(jsonDict):
    pass


# 取得使用者暱稱的函式
# @app.template_global()
def get_nickname(userID):
    # 建立與資料庫的連線
    con = sql.connect("funCrew_db.db")
    cur = con.cursor()

        # 根據 userID 查詢使用者的暱稱
        cur.execute("SELECT nickname FROM User WHERE userID=?", (userID,))
        nickname = cur.fetchone()[0]

        # 關閉資料庫連線
        con.close()

    return nickname

##############侑萱#########################
@user_bp.route('/personalInfo')
def personal_info():
    userID = session["userID"]
    con = sql.connect("funCrew_db.db")
    cur = con.cursor()

    cur.execute("SELECT image FROM User WHERE userID=?", (userID,))
    user_image = cur.fetchone()

    cur.execute("SELECT * FROM User WHERE userID=?", (userID,))
    person = cur.fetchall()[0]

    cur.execute("SELECT Avg(Participant.score) FROM Participant, Activity WHERE organizerUserID=? AND participantActivityID=activityID", (userID,))
    score = cur.fetchone()[0]

    cur.execute("SELECT postID, postTitle FROM Post WHERE postUserID=?", (userID,))
    posts = cur.fetchall()

    cur.execute("SELECT title FROM Activity WHERE organizerUserID=?", (userID,))
    activitys = cur.fetchall()

    return render_template('personalInfo.html', nickname=get_nickname(userID), user_image=user_image, user_id = str(userID), person=person, score=score, posts=posts, activitys=activitys)



@user_bp.route('/personalInfo', methods=['POST'])
def upload_photo():
    userID = session['userID']
    file = request.files['photo']
    file_path =os.path.join(current_app.config['UPLOAD_FOLDER'], str(userID)+".png")
    file.save(file_path)
    # 將圖片路徑保存到資料庫
    userID = session["userID"]
    con = sql.connect("funCrew_db.db")
    cur = con.cursor()
    cur.execute("UPDATE User SET image = ? WHERE userID = ?", (file_path, userID))
    con.commit()
    con.close()
    return redirect(url_for('user.personal_info'))

@user_bp.route('/update_personalInfo', methods=['GET', 'POST'])
def update_personalInfo():

    userID = session['userID']
    con = sql.connect("funCrew_db.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM User WHERE userID=?", (userID,))
    person = cur.fetchall()[0]
    
    if "save" in request.form:
        nickname = request.form.get('nickname')
        birth = request.form.get('birth')
        gender = request.form.get('gender')
        cellphone = request.form.get('cellphone')
        
        con = sql.connect("funCrew_db.db")
        cur = con.cursor()
        cur.execute("UPDATE User SET nickname = ?, birth = ?, gender = ?, cellphone = ? WHERE userID = ?", (nickname, birth, gender, cellphone, userID))
        con.commit()
        con.close()
        return redirect(url_for('user.personal_info'))
    return render_template("update_personalInfo.html", person=person)

@user_bp.route('/info/<int:userID>')
def info(userID):
    con = sql.connect("funCrew_db.db")
    cur = con.cursor()

    cur.execute("SELECT cellphone,gender FROM User WHERE userID=?", (userID,))
    cellphone, gender = cur.fetchone()
    #################
    cur.execute("SELECT Avg(Participant.score) FROM Participant, Activity WHERE organizerUserID=? AND participantActivityID=activityID", (userID,))
    score = cur.fetchone()[0]
    ################
    cur.execute("SELECT image FROM User WHERE userID=?", (userID,))
    user_image = cur.fetchone()

    cur.execute("SELECT postID, postTitle FROM Post WHERE postUserID=? ORDER BY postTime DESC LIMIT 3", (userID,))
    posts = cur.fetchall()

    cur.execute("SELECT title FROM Activity WHERE organizerUserID=?", (userID,))
    activitys = cur.fetchall()

    return render_template('Info.html', nickname=get_nickname(userID),score=score,gender=gender,cellphone=cellphone, posts=posts,activitys=activitys,user_image=user_image,user_id = str(userID))











##############侑萱#########################


