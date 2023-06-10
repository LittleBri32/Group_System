from flask import Blueprint, request, render_template, session, redirect
import sqlite3 as sql
import os
from werkzeug.utils import secure_filename
import uuid


# @app.template_global()
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
        print(f"Error occurred while retrieving nickname: {str(e)}")
        return ""


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
    # 點選登入btn後會切回home首頁
    return redirect("/home")


# 登出處理
@user_bp.route("/logout")
def logout():
    # 清除使用者的登入資訊
    session.pop("nickname", None)
    # 導向登入頁面
    return render_template("login.html")


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
