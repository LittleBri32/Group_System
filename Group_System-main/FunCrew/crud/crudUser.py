from flask import Blueprint, request, render_template, session, redirect
import sqlite3 as sql


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


# 註冊處理
# 使用者在 register.html 提交表單的時候會執行
@user_bp.route("/signupPost", methods=["POST"])
def signupPost():
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