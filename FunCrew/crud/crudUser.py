from flask import (
    Blueprint,
    request,
    render_template,
    session,
    redirect,
    url_for,
    flash,
    current_app,
)
import sqlite3 as sql
import os
from werkzeug.utils import secure_filename
import uuid


# 模組套件
user_bp = Blueprint("user", __name__)
# 此處為 user_bp 模組，所以路徑為 @user_bp.route("<>",)
# 在 html 引用時，需設路徑為 "/user/signin" 樣子


# 登入處理
@user_bp.route("/signin", methods=["GET", "POST"])
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
            cur.execute("DROP TABLE temp{}ViewCount;".format(userID))
        except:
            pass
        cur.execute(
            "CREATE TABLE temp{}ViewCount (postID INTEGER PRIMARY KEY)".format(userID)
        )
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
    try:
        cur.execute("DROP TABLE temp{}ViewCount".format(session["userID"]))
    except:
        pass
    con.commit()
    con.close()
    ############################################################
    # 清除使用者的登入資訊
    session.pop("nickname", None)
    # 導向登入頁面
    return render_template("login.html")
    # try:
    #     # 刪除使用者並提交更改
    #     db.session.delete(user)
    #     db.session.commit()
    #     return {'message': 'User deleted successfully'}, 200
    # except Exception as e:
    #     return {'error': str(e)}, 500


# 忘記密碼處理
@user_bp.route("/forgotPasswordPost", methods=["POST"])
def forgotPasswordPost():
    con = None
    try:
        con = sql.connect("funCrew_db.db")
        con.row_factory = sql.Row
        cur = con.cursor()

        if request.method == "POST":
            email = request.form["email"]
            cur.execute("SELECT * FROM User WHERE email=?", (email,))
            con.commit()

            people = cur.fetchall()
            if len(people) == 0:
                msg = "沒有這個電子信箱的用戶，請重新輸入！"
                return render_template("forgot_password.html", msg=msg)

            return redirect("/forgot_password_success")

    except Exception as e:
        msg = "發生錯誤：" + str(e)
        return render_template("forgot_password.html", msg=msg)
    finally:
        if con:
            con.close()


# 註冊處理
# 使用者在 register.html 提交表單的時候會執行
@user_bp.route("/signupPost", methods=["POST"])
def signupPost():
    con = None  # 初始化資料庫連線變數
    try:
        # 取得表單資料
        email = request.form["email"]
        password = request.form["password"]
        check_password = request.form["check_password"]
        cellphone = request.form["cellphone"]
        nickname = request.form["nickname"]
        gender = request.form["gender"]
        birth = request.form["birth"]
        avatar = request.files["image"]  # 取得上傳的檔案
        if password != check_password:
            msg = "二次確認密碼與設定的密碼不相同，請重新確認"
            return render_template("register.html", msg=msg)
        with sql.connect("funCrew_db.db") as con:
            # 建立與資料庫的連線
            cur = con.cursor()
            # 檢查信箱是否重複（排除目前正在註冊的使用者）
            cur.execute("SELECT * FROM User WHERE email=? AND email<>?", (email, email))
            existing_user = cur.fetchone()
            if existing_user is not None:
                msg = "該信箱已被註冊，請使用其他信箱"
                return render_template("register.html", msg=msg)
            # 儲存上傳的大頭貼圖片
            if avatar:
                # 獲取原始檔案名稱和副檔名
                filename = secure_filename(avatar.filename)
                extension = filename.rsplit(".", 1)[1]
                # 生成唯一的檔案名稱
                unique_filename = str(uuid.uuid4()) + "." + extension
                avatar.save(os.path.join("static/images/avatars/" + unique_filename))
            else:
                unique_filename = "default_avatar.png"  # 預設大頭貼檔名
            # 執行註冊動作
            cur.execute(
                "INSERT INTO User (email, password, cellphone, nickname, gender, birth, image) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    email,
                    password,
                    cellphone,
                    nickname,
                    gender,
                    birth,
                    unique_filename,  # 使用儲存的檔名
                ),
            )
            con.commit()

        # 點選註冊，成功後，轉到註冊成功的頁面
        return redirect("/registration_success")
    except Exception as e:
        msg = "註冊過程發生錯誤：" + str(e)
        if con:
            con.rollback()  # 發生異常時回滾資料庫操作
        return render_template("register.html", msg=msg)
    finally:
        if con:
            con.close()  # 關閉資料庫連線


# 定義取得使用者大頭貼路徑的函式
def get_avatar_path(userID):
    try:
        # 建立與資料庫的連線
        con = sql.connect("funCrew_db.db")
        cur = con.cursor()

        # 根據 userID 查詢使用者的頭貼
        cur.execute("SELECT image FROM User WHERE userID=?", (userID,))
        filename = cur.fetchone()[0]

        # 關閉資料庫連線
        con.close()

        return "static/images/avatars/" + filename
    except Exception as e:
        print(f"Error occurred while retrieving filename: {str(e)}")
        return ""


# 取得使用者暱稱的函式
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
@user_bp.route("/personalInfo")
def personal_info():
    userID = session["userID"]
    con = sql.connect("funCrew_db.db")
    cur = con.cursor()

    cur.execute("SELECT image FROM User WHERE userID=?", (userID,))
    user_image = cur.fetchone()

    cur.execute("SELECT * FROM User WHERE userID=?", (userID,))
    person = cur.fetchall()[0]

    cur.execute(
        "SELECT Avg(Participant.score) FROM Participant, Activity WHERE organizerUserID=? AND participantActivityID=activityID",
        (userID,),
    )
    score = cur.fetchone()[0]

    cur.execute("SELECT postID, postTitle FROM Post WHERE postUserID=?", (userID,))
    posts = cur.fetchall()

    cur.execute("SELECT title FROM Activity WHERE organizerUserID=?", (userID,))
    activitys = cur.fetchall()

    return render_template(
        "personalInfo.html",
        nickname=get_nickname(userID),
        user_image=user_image,
        user_id=str(userID),
        person=person,
        score=score,
        posts=posts,
        activitys=activitys,
    )


@user_bp.route("/personalInfo", methods=["POST"])
# 使用者上傳大頭貼
def upload_photo():
    userID = session["userID"]
    file = request.files["photo"]
    # 獲取原始檔案名稱和副檔名
    filename = secure_filename(file.filename)
    extension = filename.rsplit(".", 1)[1]
    unique_filename = str(uuid.uuid4()) + "." + extension
    file_path = os.path.join("static/images/avatars/" + unique_filename)
    file.save(file_path)

    # 將圖片路徑保存到資料庫
    userID = session["userID"]
    con = sql.connect("funCrew_db.db")
    cur = con.cursor()
    cur.execute("UPDATE User SET image = ? WHERE userID = ?", (unique_filename, userID))
    con.commit()
    con.close()
    return redirect(url_for("user.personal_info"))


@user_bp.route("/update_personalInfo", methods=["GET", "POST"])
def update_personalInfo():
    userID = session["userID"]
    con = sql.connect("funCrew_db.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM User WHERE userID=?", (userID,))
    person = cur.fetchall()[0]

    if "save" in request.form:
        nickname = request.form.get("nickname")
        birth = request.form.get("birth")
        gender = request.form.get("gender")
        cellphone = request.form.get("cellphone")

        con = sql.connect("funCrew_db.db")
        cur = con.cursor()
        cur.execute(
            "UPDATE User SET nickname = ?, birth = ?, gender = ?, cellphone = ? WHERE userID = ?",
            (nickname, birth, gender, cellphone, userID),
        )
        con.commit()
        con.close()
        return redirect(url_for("user.personal_info"))
    return render_template("update_personalInfo.html", person=person)


@user_bp.route("/info/<int:userID>")
def info(userID):
    origin_user = session["userID"]
    con = sql.connect("funCrew_db.db")
    cur = con.cursor()

    cur.execute("SELECT nickname FROM User WHERE userID=?", (origin_user,))
    origin_username = cur.fetchone()[0]

    cur.execute("SELECT cellphone,gender, birth FROM User WHERE userID=?", (userID,))
    cellphone, gender, birth = cur.fetchone()
    #################
    cur.execute(
        "SELECT Avg(Participant.score) FROM Participant, Activity WHERE organizerUserID=? AND participantActivityID=activityID",
        (userID,),
    )
    score = cur.fetchone()[0]
    ################
    cur.execute("SELECT image FROM User WHERE userID=?", (userID,))
    user_image = cur.fetchone()

    cur.execute("SELECT image FROM User WHERE userID=?", (origin_user,))
    origin_user_image = cur.fetchone()

    cur.execute(
        "SELECT postID, postContent FROM Post WHERE postUserID=? ORDER BY postTime DESC LIMIT 3",
        (userID,),
    )
    posts = cur.fetchall()

    cur.execute("SELECT title FROM Activity WHERE organizerUserID=?", (userID,))
    activitys = cur.fetchall()

    return render_template(
        "Info.html",
        nickname=get_nickname(userID),
        score=score,
        gender=gender,
        birth=birth,
        cellphone=cellphone,
        posts=posts,
        activitys=activitys,
        user_image=user_image,
        user_id=str(userID),
        origin_username=origin_username,
        origin_user_image=origin_user_image,
    )


##############侑萱#########################
