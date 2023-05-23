from flask import Blueprint, request, render_template, session, redirect
from .crudUser import get_nickname
import sqlite3 as sql


post_bp = Blueprint('post', __name__)



    

# 貼文顯示處理
@post_bp.route("/area", methods=["GET"])
def postArea():
    # 建立與資料庫的連線
    con = sql.connect("funCrew_db.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    # 從資料庫中獲取所有貼文內容，按照最新的放在最上面
    cur.execute("SELECT * FROM Post ORDER BY postTime DESC")
    posts = cur.fetchall()

    # 檢查有沒有存在nickname
    if "nickname" in session:
        nickname = session["nickname"]
    else:
        nickname = ""

    # 關閉資料庫連線
    con.close()

    # 傳遞貼文內容和使用者暱稱的函式到 postArea.html 進行顯示
    return render_template(
        "postArea.html", posts=posts, get_nickname=get_nickname, nickname=nickname
    )

        



# 貼文發布處理
@post_bp.route("/submitPost", methods=["POST"])
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