from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = "nccucs"


# 首頁路由
@app.route("/")
def home():
    return render_template("home.html")


# 註冊
@app.route("/new_user")
def new_user():
    return render_template("new_user.html")


# 登入
@app.route("/sign_in_view")
def sign_in_view():
    return render_template("sign_in_view.html")


# 註冊
# 指定一個路由，讓使用者提交註冊表單的時候，會執行sign_up
@app.route("/sign_up", methods=["POST"])
def sign_up():
    try:
        # userID = request.form["userID"]
        password = request.form["password"]
        nickname = request.form["nickname"]
        gender = request.form["gender"]
        age = request.form["age"]
        cellphone = request.form["cellphone"]
        email = request.form["email"]

        with sql.connect("database_final_project.db") as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO User (password, nickname, gender, age, cellphone, email) VALUES (?, ?, ?, ?, ?, ?)",
                (password, nickname, gender, age, cellphone, email),
            )
            con.commit()
            msg = "帳號已成功建立！"
    except:
        con.rollback()
        print(con.rollback())
        msg = "註冊失敗！"
    finally:
        con.close()
        return render_template("result.html", msg=msg)


# 登入
@app.route("/sign_in", methods=["POST"])
def sign_in():
    con = sql.connect("database_final_project.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    userID = request.form["userID"]
    password = request.form["password"]
    cur.execute("SELECT * FROM User WHERE userID=? and password=?", (userID, password))
    con.commit()
    msg = "帳號或密碼錯誤！"
    people = cur.fetchall()
    if len(people) == 0:
        return render_template("result.html", msg=msg)

    cur.execute(
        "SELECT nickname FROM User WHERE userID=? and password=?",
        (
            userID,
            password,
        ),
    )
    nickname = cur.fetchone()[0]
    session["nickname"] = nickname
    session["userID"] = userID
    return redirect("/sign_in_activities")


@app.route("/sign_in_activities")
def sign_in_activities():
    if "nickname" in session:
        return render_template("sign_in_activities.html", nickname=session["nickname"])
    else:
        return render_template("/")


if __name__ == "__main__":
    app.secret_key = "super secret key"
    app.run(debug=True, port=8080)
