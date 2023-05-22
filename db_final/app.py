from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql
from datetime import datetime

app = Flask(__name__)
app.secret_key = "nccucs"


# 跳轉到登入頁面
@app.route("/")
def login():
    return render_template("login.html")


# 跳轉到註冊頁面
@app.route("/sign_up", methods=["GET"])
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


# 貼文顯示處理
@app.route("/postArea", methods=["GET"])
def postArea():
    # 建立與資料庫的連線
    con = sql.connect("funCrew_db.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    # 從資料庫中獲取所有貼文內容，按照最新的放在最上面
    cur.execute("SELECT * FROM Post ORDER BY postTime DESC")
    posts = cur.fetchall()

    # 取得使用者暱稱的函式
    def get_nickname(userID):
        try:
            # 根據 userID 查詢使用者的暱稱
            cur.execute("SELECT nickname FROM User WHERE userID=?", (userID,))
            nickname = cur.fetchone()[0]
            return nickname
        except Exception as e:
            print(f"Error occurred while retrieving nickname: {str(e)}")
            return ""

    # 檢查有沒有存在nickname
    if "nickname" in session:
        nickname = session["nickname"]
    else:
        nickname = ""

    # 關閉資料庫連線
    con.close()

    # 傳遞貼文內容和使用者暱稱的函式到 postArea.html 進行顯示
    return render_template("postArea.html", posts=posts, get_nickname=get_nickname)


# 登出處理
@app.route("/logout")
def logout():
    # 清除使用者的登入資訊
    session.pop("nickname", None)
    # 導向登入頁面
    return render_template("login.html")


# 登入處理
@app.route("/sign_in", methods=["GET", "POST"])
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
            "SELECT nickname FROM User WHERE email=? and password=?",
            (
                email,
                password,
            ),
        )
        nickname = cur.fetchone()[0]
        session["nickname"] = nickname

    # 點選登入btn後會切回home首頁
    return redirect("/home")


# 註冊處理
# 使用者提交表單的時候會執行sign_up_post
@app.route("/sign_up_post", methods=["POST"])
def sign_up_post():
    try:
        # 取得表單資料
        email = request.form["email"]
        password = request.form["password"]
        check_password = request.form["check_password"]
        cellphone = request.form["cellphone"]
        nickname = request.form["nickname"]
        gender = request.form["gender"]
        birth = request.form["birth"]

        if password != check_password:
            msg = "二次確認密碼與設定的密碼不相同，請重新確認"
            return render_template("register.html", msg=msg)

        with sql.connect("funCrew_db.db") as con:
            cur = con.cursor()

            # 檢查信箱是否重複（排除目前正在註冊的使用者）
            cur.execute("SELECT * FROM User WHERE email=? AND email<>?", (email, email))
            existing_user = cur.fetchone()

            if existing_user is not None:
                msg = "該信箱已被註冊，請使用其他信箱"
                return render_template("register.html", msg=msg)

            # 執行註冊動作
            cur.execute(
                "INSERT INTO User (email, password, cellphone, nickname, gender, birth) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    email,
                    password,
                    cellphone,
                    nickname,
                    gender,
                    birth,
                ),
            )
            con.commit()

        # 點選註冊，成功後，轉到註冊成功的頁面
        return redirect("/registration_success")

    except Exception as e:
        con.rollback()
        msg = f"註冊失敗！請確認你的資料。錯誤訊息：{str(e)}"
        return render_template("register.html", msg=msg)

    finally:
        con.close()


# 貼文發布處理
@app.route("/submitPost", methods=["POST"])
def submitPost():
    content = request.form.get("content")

    if content:
        # 建立與資料庫的連線
        con = sql.connect("funCrew_db.db")
        cur = con.cursor()

        # 取得當前使用者的userID
        nickname = session.get("nickname")
        cur.execute("SELECT userID FROM User WHERE nickname=?", (nickname,))
        userID = cur.fetchone()[0]

        # 取得當前時間
        postTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 將貼文存入資料庫
        cur.execute(
            "INSERT INTO Post (postContent, postUserID, postTime) VALUES (?, ?, ?)",
            (content, userID, postTime),
        )
        con.commit()

        # 關閉資料庫連線
        con.close()

    # 重新導向到貼文區域
    return redirect("/postArea")


if __name__ == "__main__":
    app.secret_key = "super secret key"
    app.run(debug=True, port=1222)
