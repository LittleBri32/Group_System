from flask import Flask, render_template, request, redirect, session
from datetime import datetime
from crud import crudActivity, crudPost, crudUser


app = Flask(__name__)
app.secret_key = "nccucs"


# 把三個模組註冊到 app 中
app.register_blueprint(crudUser.user_bp, url_prefix = '/user')
app.register_blueprint(crudActivity.activity_bp, url_prefix = '/activity')
app.register_blueprint(crudPost.post_bp, url_prefix = '/post')



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
    if "nickname" in session:
        return render_template("home.html", nickname=session["nickname"])
    else:
        return render_template("/")
    # 檢查有沒有存在nickname
    if "nickname" in session:
        nickname = session["nickname"]
    else:
        nickname = ""
    # 關閉資料庫連線
    con.close()
    # 傳遞貼文內容和使用者暱稱的函式到 postArea.html 進行顯示
    return render_template("postArea.html", posts=posts, get_nickname=get_nickname)


    

    

if __name__ == "__main__":
    app.secret_key = "super secret key"
    app.run(debug=True, port = 5000)
