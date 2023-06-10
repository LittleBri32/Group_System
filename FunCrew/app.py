from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql
from crud import crudActivity, crudPost, crudUser
from crud.crudUser import get_nickname
from crud.crudUser import get_avatar_path

app = Flask(__name__)
app.secret_key = "nccucs"


# 把三個模組註冊到 app 中
app.register_blueprint(crudUser.user_bp, url_prefix="/user")
app.register_blueprint(crudActivity.activity_bp, url_prefix="/activity")
app.register_blueprint(crudPost.post_bp, url_prefix="/post")


# 跳轉到登入頁面
@app.route("/")
def login():
    return render_template("login.html")


# 跳轉到忘記密碼畫面: 填電子信箱
@app.route("/forgotPassword")
def forgot_password():
    return render_template("forgot_password.html")


# 跳轉到密碼已成功傳到電子信箱介面
@app.route("/forgot_password_success")
def forgot_password_success():
    return render_template("forgot_password_success.html")


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

        # 關閉資料庫連線
        con.close()
        return render_template(
            "home.html",
            nickname=nickname,
            posts=posts,
            avatar=filename,
        )
    else:
        return render_template("login.html")


if __name__ == "__main__":
    app.secret_key = "super secret key"
    app.run(debug=True, port=1478)
