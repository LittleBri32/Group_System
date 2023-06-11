from flask import Blueprint, request, render_template, session, redirect, url_for
from .crudUser import get_nickname
import sqlite3 as sql
from datetime import datetime

post_bp = Blueprint("post", __name__)


# 貼文顯示處理
@post_bp.route("/posts/<string:sortmethod>", methods=["GET", "POST"])
def posts_method(sortmethod):
    userID = session["userID"]
    searching_value=""
    if sortmethod == 'newest':
        con = sql.connect("funCrew_db.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        # 從資料庫中獲取所有貼文內容，按照最新的放在最上面
        cur.execute("SELECT * FROM Post, User WHERE postUserID = userID ORDER BY postTime DESC")
        posts = cur.fetchall()
        # 關閉資料庫連線
        con.close()
    elif sortmethod == 'mostView':
        con = sql.connect("funCrew_db.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        # 從資料庫中獲取所有貼文內容，按照最新的放在最上面
        cur.execute("SELECT * FROM Post, User WHERE postUserID = userID ORDER BY postView DESC")
        posts = cur.fetchall()
        # 關閉資料庫連線
        con.close()
    elif sortmethod == 'hotest': 
        con = sql.connect("funCrew_db.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        # 從資料庫中獲取所有貼文內容，按照最新的放在最上面
        cur.execute("SELECT * FROM Post, User LEFT JOIN Comment ON postID=commentPostID WHERE postUserID=userID GROUP BY postID ORDER BY count(commentPostID) DESC")
        posts = cur.fetchall()
        # 關閉資料庫連線
        con.close()
    elif sortmethod == 'searching':
        if request.form.get("searching_value"):
            searching_value = request.form.get("searching_value")
        elif request.args.get("searching_value"):
            searching_value = request.args.get("searching_value")
        searching_exp = "%"+searching_value+"%"
        con = sql.connect("funCrew_db.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM Post, User WHERE postUserID = userID AND (postTitle LIKE ? OR nickName LIKE ?)", (searching_exp, searching_exp,))
        posts = cur.fetchall()
        con.close()
    elif sortmethod == 'my_posts': 
        con = sql.connect("funCrew_db.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        # 從資料庫中獲取所有貼文內容，按照最新的放在最上面
        cur.execute("SELECT * FROM Post WHERE postUserID = ? ORDER BY postTime DESC", (userID,))
        posts = cur.fetchall()
        # 關閉資料庫連線
        con.close()
    return render_template("posts.html", nickname=get_nickname(userID), posts=posts, userID=userID, sortmethod=sortmethod, searching_value=searching_value)


# 貼文發布處理
@post_bp.route("/create_post", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        previous_url = request.form.get("previous_url")
        title = request.form.get("title")
        content = request.form.get("content")

        # 建立與資料庫的連線
        con = sql.connect("funCrew_db.db")
        cur = con.cursor()

        # 取得當前使用者的userID
        userID = session["userID"]

        # 取得當前時間
        postTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 將貼文存入資料庫
        cur.execute(
            "INSERT INTO Post (postUserID, postTitle, postContent, postTime, postView) VALUES (?, ?, ?, ?, 0)",
            (userID, title, content, postTime),
        )
        con.commit()

        # 關閉資料庫連線
        con.close()
        return redirect(previous_url)
    # 
    return render_template("create_post.html", previous_url=request.referrer)

# 個別帖文頁面
@post_bp.route('/posts/<int:postID>', methods=["GET", "POST"])
def post_detail(postID):
    sortmethod = request.args.get("sortmethod")
    searching_value = request.args.get("searching_value")
    # 取得當前使用者的userID
    userID = session["userID"]

    con = sql.connect("funCrew_db.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    # 從資料庫中獲取單獨貼文內容
    cur.execute("SELECT * FROM Post, User WHERE postUserID=userID AND postID=?", (postID,))
    post = cur.fetchone()

    cur.execute("SELECT * FROM Comment, User WHERE commentPostID = ? AND userID = commentUserID ORDER BY commentTime DESC", (postID,))
    comments = cur.fetchall()

    # View的記錄與防止刷view
    cur.execute("SELECT postView FROM Post WHERE postID = ?", (postID,))
    view = cur.fetchone()[0]
    # try: 可以插入記錄到view count，代表這次登入沒看過
    try:
        cur.execute("INSERT INTO temp{}ViewCount (postID) VALUES (?)".format(userID), (postID,))
        view = view+1
        cur.execute("UPDATE Post SET postView=? WHERE postID = ?", (view, postID,))
        con.commit()
        con.close()
    # except: 不可以插入記錄到view count，代表這次登入看過
    except sql.IntegrityError:
        pass
    
    # 抓留言
    if request.method == "POST":
        content = request.form.get("content")

        # 建立與資料庫的連線
        con = sql.connect("funCrew_db.db")
        cur = con.cursor()

        # 取得當前時間
        postTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 將貼文存入資料庫
        cur.execute(
            "INSERT INTO Comment (commentPostID, commentUserID, commentContent, commentTime) VALUES (?, ?, ?, ?)",
            (postID, userID, content, postTime),
        )
        con.commit()

        # 關閉資料庫連線
        con.close()
        return redirect(request.referrer)

    return render_template('post_detail.html', post=post, comments=comments, postID=postID, userID=userID, views=view, sortmethod=sortmethod, searching_value=searching_value)
# , comments=comments

# 我的貼文
@post_bp.route("/my_posts", methods=["GET"])
def my_posts():
    userID = session["userID"]
    
    # 建立與資料庫的連線
    con = sql.connect("funCrew_db.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    # 從資料庫中獲取所有貼文內容，按照最新的放在最上面
    cur.execute("SELECT * FROM Post WHERE postUserID = ? ORDER BY postTime DESC", (userID,))
    my_posts = cur.fetchall()

    # 關閉資料庫連線
    con.close()

    # 傳遞貼文內容和使用者暱稱的函式到 posts.html 進行顯示
    return render_template(
        "my_posts.html", nickname=get_nickname(userID), posts=my_posts
    )

# 更改帖文頁面
@post_bp.route('/posts/update_post/<int:postID>', methods=["GET", "POST"])
def update_post(postID):
    # 建立與資料庫的連線
    con = sql.connect("funCrew_db.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    # 從資料庫中獲取所有貼文內容，按照最新的放在最上面
    cur.execute("SELECT * FROM Post WHERE postID = ?", (postID,))
    post = cur.fetchone()

    # 關閉資料庫連線
    con.close()

    # 抓更改
    if request.method == "POST":
        previous_url = request.form.get("previous_url")
        title = request.form.get("title")
        content = request.form.get("content")

        # 建立與資料庫的連線
        con = sql.connect("funCrew_db.db")
        cur = con.cursor()

        # 更改資料庫
        cur.execute(
            "UPDATE Post SET postTitle = ?, postContent = ? WHERE postID = ?;",
            (title, content, postID)
        )
        con.commit()

        # 關閉資料庫連線
        con.close()
        return redirect(previous_url)

    return render_template('update_post.html', post=post, previous_url=request.referrer)

# 刪除帖文頁面
@post_bp.route('/posts/delete_post/<int:postID>', methods=["GET", "POST"])
def delete_post(postID):
    # 刪除確認
    if request.method == "POST":
        previous_url = request.form.get("previous_url")
        # 建立與資料庫的連線
        con = sql.connect("funCrew_db.db") 
        cur = con.cursor()

        cur.execute("PRAGMA foreign_keys = ON;")
        cur.execute("DELETE FROM Post WHERE postID = ?;", (postID,))
        con.commit()

        # 關閉資料庫連線
        con.close()
        return redirect(previous_url)

    return render_template('delete_post.html', postID=postID, previous_url=request.referrer)

# 我的留言
@post_bp.route("/my_comments", methods=["GET"])
def my_domments():
    userID = session["userID"]
    
    # 建立與資料庫的連線
    con = sql.connect("funCrew_db.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    # 從資料庫中獲取所有貼文內容，按照最新的放在最上面
    cur.execute(
        "SELECT commentID, commentPostID, commentTime, commentContent, postTitle FROM Comment, Post WHERE commentPostID=postID AND commentUserID=? order by postTime DESC, commentTime DESC, commentPostID ASC;", (userID,)
    )
    my_comments = cur.fetchall()

    # 關閉資料庫連線
    con.close()

    # 傳遞貼文內容和使用者暱稱的函式到 posts.html 進行顯示
    return render_template(
        "my_comments.html", nickname=get_nickname(userID), comments=my_comments
    )

# 更改留言頁面
@post_bp.route('/posts/update_comment/<int:commentID>', methods=["GET", "POST"])
def update_comment(commentID):
    # 建立與資料庫的連線
    con = sql.connect("funCrew_db.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    # 從資料庫中獲取留言內容
    cur.execute("SELECT * FROM Comment WHERE commentID = ?", (commentID,))
    comment = cur.fetchone()

    # 關閉資料庫連線
    con.close()

    # 抓更改
    if request.method == "POST":
        previous_url = request.form.get("previous_url")
        content = request.form.get("content")

        # 建立與資料庫的連線
        con = sql.connect("funCrew_db.db")
        cur = con.cursor()

        # 更改資料庫
        cur.execute(
            "UPDATE Comment SET commentContent = ? WHERE commentID = ?;",
            (content, commentID)
        )
        con.commit()

        # 關閉資料庫連線
        con.close()
        return redirect(previous_url)

    return render_template('update_comment.html', comment=comment, previous_url=request.referrer)

# 刪除留言確認頁面
@post_bp.route('/posts/delete_comment/<int:commentID>', methods=["GET", "POST"])
def delete_comment(commentID):
    # 刪除確認
    if request.method == "POST":
        previous_url = request.form.get("previous_url")

        # 建立與資料庫的連線
        con = sql.connect("funCrew_db.db")
        cur = con.cursor()

        
        # 更改資料庫
        cur.execute("DELETE FROM Comment WHERE commentID = ?;", (commentID,))
        con.commit()

        # 關閉資料庫連線
        con.close()
        return redirect(previous_url)

    return render_template('delete_comment.html', commentID=commentID, previous_url=request.referrer)