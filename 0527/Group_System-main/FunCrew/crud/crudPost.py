from flask import Blueprint, request, render_template, session, redirect, url_for
from .crudUser import get_nickname
import sqlite3 as sql
from datetime import datetime

post_bp = Blueprint("post", __name__)

# 取得留言的的函式
def get_comment(postID):
    con = sql.connect("funCrew_db.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    # 根據 userID 查詢使用者的暱稱
    cur.execute("SELECT nickname FROM User WHERE conmmentPostid=?", (postID,))
    comments = cur.fetchall()

    # 關閉資料庫連線
    con.close()

    return comments

# 貼文顯示處理
@post_bp.route("/posts", methods=["GET"])
def posts():
    # 建立與資料庫的連線
    con = sql.connect("funCrew_db.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    # 從資料庫中獲取所有貼文內容，按照最新的放在最上面
    cur.execute(
        "SELECT * FROM Post, User WHERE postUserID = userID ORDER BY postTime DESC"
    )
    posts = cur.fetchall()

    # 關閉資料庫連線
    con.close()

    # 傳遞貼文內容和使用者暱稱的函式到 posts.html 進行顯示
    return render_template(
        "posts.html", nickname=get_nickname(session["userID"]), posts=posts
    )


# 貼文發布處理
@post_bp.route("/create_post", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        # 建立與資料庫的連線
        con = sql.connect("funCrew_db.db")
        cur = con.cursor()

        # 取得當前使用者的userID
        userID = session.get("userID")

        # 取得當前時間
        postTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 將貼文存入資料庫
        cur.execute(
            "INSERT INTO Post (postUserID, postTitle, postContent, postTime) VALUES (?, ?, ?, ?)",
            (userID, title, content, postTime),
        )
        con.commit()

        # 關閉資料庫連線
        con.close()
        return redirect("/post/posts")
    # 
    return render_template("create_post.html")

@post_bp.route('/posts/<int:postID>')
def post_detail(postID):
    # 建立與資料庫的連線
    con = sql.connect("funCrew_db.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    # 從資料庫中獲取所有貼文內容，按照最新的放在最上面
    cur.execute(
        "SELECT * FROM Post WHERE postID = ?", (postID,)
    )
    post = cur.fetchone()

    # 關閉資料庫連線
    con.close()
    return render_template('post_detail.html', post=post)


