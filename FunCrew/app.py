from crud import crudActivity, crudPost, crudUser
from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_mail import Mail, Message
import os
import sqlite3 as sql
from crud.crudUser import get_nickname, get_avatar_path
from datetime import datetime


app = Flask(__name__)
app.secret_key = "nccucs"

# Mail
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")  # 改成自己信箱
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")  # 改成自己信箱
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False

mail = Mail(app)

# 把三個模組註冊到 app 中
app.register_blueprint(crudUser.user_bp, url_prefix="/user")
app.register_blueprint(crudActivity.activity_bp, url_prefix="/activity")
app.register_blueprint(crudPost.post_bp, url_prefix="/post")

UPLOAD_FOLDER = os.path.join(os.getcwd(), "static")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# 跳轉到登入頁面
@app.route("/")
def login():
    return render_template("login.html")


# 跳轉到註冊頁面
@app.route("/signup", methods=["GET"])
def sign_up():
    return render_template("register.html")


# 跳轉到註冊成功畫面
@app.route("/registration_success")
def registration_success():
    return render_template("registration_success.html")


# 跳轉到首頁畫面
@app.route("/home")
def home():
    if "userID" in session:
        # 建立與資料庫的連線
        con = sql.connect("funCrew_db.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        nickname = get_nickname(session["userID"])
        filename = get_avatar_path(session["userID"])

        # 從資料庫中獲取最新的三篇貼文
        cur.execute(
            "SELECT * FROM Post, User WHERE postUserID = userID ORDER BY postTime DESC LIMIT 3"
        )
        posts = cur.fetchall()
        # 從資料庫中獲取最新的三個聚會
        cur.execute(
            "SELECT * FROM Activity, User WHERE organizerUserID = userID ORDER BY createTime DESC LIMIT 3"
        )
        activities = cur.fetchall()
        # 關閉資料庫連線
        con.close()
        return render_template(
            "home.html",
            nickname=nickname,
            posts=posts,
            avatar=filename,
            activities=activities,
        )
    else:
        return render_template("login.html")


# 跳轉到忘記密碼頁面
@app.route("/forget")
def forget():
    return render_template("forgetPassword.html")


# mail 處理
# @app.route('/forgetPassword', methods=['GET','POST'])
# 忘記密碼表單送出
@app.route("/forgetPassword", methods=["GET", "POST"])
def forget_password():
    if request.method == "POST":
        phone = request.form.get("phone")
        email = request.form.get("email")
        # Check if phone and email exist in database
        with sql.connect("funCrew_db.db") as con:
            cur = con.cursor()
            cur.execute(
                "SELECT * FROM User WHERE cellphone=? AND email=?", (phone, email)
            )
            user = cur.fetchone()
        if user:
            msg = Message(
                "[FunCrew] 密碼找回",
                sender="111753135@g.nccu.edu.tw",  # 改成自己信箱
                recipients=[user["email"]],
                body="Your password is: " + user["password"],
            )
            try:
                mail.send(msg)
            except Exception as e:
                print(e)
            flash("請至您的信箱查收信件", "success")
            return redirect(url_for("login"))
        else:
            session["error"] = "No user with this phone number and email."
            return redirect(url_for("forget_password"))
    else:
        return render_template("forgetPassword.html")


# 跳轉到忘記密碼畫面: 填電子信箱
@app.route("/forgotPassword")
def forgot_password():
    return render_template("forgot_password.html")


# 跳轉到密碼已成功傳到電子信箱介面
@app.route("/forgot_password_success")
def forgot_password_success():
    return render_template("forgot_password_success.html")


if __name__ == "__main__":
    app.secret_key = "super secret key"
    app.run(debug=True, port=8115)
