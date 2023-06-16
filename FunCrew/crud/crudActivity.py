from flask import Blueprint, request, render_template, session, redirect
import sqlite3 as sql
import uuid
import time
from datetime import datetime
from .crudUser import get_nickname, get_avatar_path
from werkzeug.utils import secure_filename

activity_bp = Blueprint("activity", __name__)


# 顯示活動頁面
@activity_bp.route("/activities/<string:show_methed>", methods=["GET", "POST"])
def show_activities_method(show_methed):
    userID = session["userID"]
    if show_methed == "signingUp" or show_methed == "None":
        con = sql.connect("funCrew_db.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        # 從資料庫中獲取所有報名中活動內容
        cur.execute(
            "SELECT * FROM Activity, User WHERE status = ? AND organizerUserID = userID ORDER BY createTime DESC",
            (show_methed,),
        )
        activities = cur.fetchall()
        # 關閉資料庫連線
        con.commit()
        con.close()
    elif show_methed == "preparing":
        con = sql.connect("funCrew_db.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        # 從資料庫中獲取所有籌備中活動內容
        cur.execute(
            "SELECT * FROM Activity, User WHERE status = ? AND organizerUserID = userID ORDER BY createTime DESC",
            (show_methed,),
        )
        activities = cur.fetchall()
        # 關閉資料庫連線
        con.commit()
        con.close()
    elif show_methed == "end":
        con = sql.connect("funCrew_db.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        # 從資料庫中獲取所有已結束活動內容
        cur.execute(
            "SELECT * FROM Activity, User WHERE status = ? AND organizerUserID = userID ORDER BY createTime DESC",
            (show_methed,),
        )
        activities = cur.fetchall()
        # 關閉資料庫連線
        con.commit()
        con.close()
    elif show_methed == "my_activities":
        con = sql.connect("funCrew_db.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        # 從資料庫中獲取所有我辦過的活動
        cur.execute(
            "SELECT * FROM Activity WHERE organizerUserID=? ORDER BY createTime DESC",
            (userID,),
        )
        activities = cur.fetchall()
        # 關閉資料庫連線
        con.commit()
        con.close()
    return render_template(
        "activities.html",
        nickname=get_nickname(userID),
        avatar=get_avatar_path(userID),
        userID=userID,
        activities=activities,
        show_methed=show_methed,
    )


# 個別活動頁面
@activity_bp.route(
    "/activities/activity_detail/<string:activityID>", methods=["GET", "POST"]
)
def activity_detail(activityID):
    show_methed = request.args.get("show_methed")
    # 取得當前使用者的userID
    origin_user = session["userID"]

    con = sql.connect("funCrew_db.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    # 當前登入用戶的頭貼/名字
    cur.execute("SELECT nickname FROM User WHERE userID=?", (origin_user,))
    origin_username = cur.fetchone()[0]
    cur.execute("SELECT image FROM User WHERE userID=?", (origin_user,))
    origin_user_image = cur.fetchone()[0]

    cur.execute(
        "SELECT * FROM Participant WHERE participantUserID=? AND participantActivityID=?",
        (origin_user, activityID),
    )
    joint = cur.fetchone()

    # 從資料庫中獲取單獨活動內容
    cur.execute(
        "SELECT * FROM Activity, User WHERE organizerUserID=userID AND activityID=?",
        (activityID,),
    )
    activity = cur.fetchone()

    # 抓評論同時抓這個評論用戶的頭貼
    cur.execute(
        """
        SELECT Discussion.*, User.image, User.nickname 
        FROM Discussion 
        INNER JOIN User ON Discussion.discussionUserID = User.userID 
        WHERE discussionActivityID = ? 
        ORDER BY discussionTime DESC
        """,
        (activityID,),
    )
    discussions = cur.fetchall()

    # 抓這篇活動創建人的頭像
    cur.execute(
        "SELECT image FROM User WHERE userID=? ", (activity["organizerUserID"],)
    )
    user_image = cur.fetchone()

    # 抓活動下面的留言
    if request.method == "POST":
        content = request.form.get("content")

        # 建立與資料庫的連線
        # con = sql.connect("funCrew_db.db")
        # cur = con.cursor()

        # 取得當前時間
        postTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 將討論存入資料庫
        con = sql.connect("funCrew_db.db")
        cur = con.cursor()
        cur.execute(
            "INSERT INTO Discussion (discussionActivityID, discussionUserID, discussionContent, discussionTime) VALUES (?, ?, ?, ?)",
            (
                activityID,
                origin_user,
                content,
                postTime,
            ),
        )

        # 關閉資料庫連線
        con.commit()
        con.close()
        return redirect(request.referrer)

    return render_template(
        "activity_detail.html",
        activity=activity,
        discussions=discussions,
        activityID=activityID,
        userID=origin_user,
        show_methed=show_methed,
        user_image=user_image,
        origin_username=origin_username,
        origin_user_image=origin_user_image,
        joint=joint,
    )


# 我的活動
@activity_bp.route("/my_activities", methods=["GET"])
def my_activities():
    userID = session["userID"]

    # 建立與資料庫的連線
    con = sql.connect("funCrew_db.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    # 從資料庫中獲取所有舉辦過的活動內容，按照最新的放在最上面
    cur.execute(
        "SELECT * FROM Activity WHERE organizerUserID = ? ORDER BY createTime DESC",
        (userID,),
    )
    my_activities = cur.fetchall()

    # 關閉資料庫連線
    con.commit()
    con.close()

    # 傳遞貼文內容和使用者暱稱的函式到 posts.html 進行顯示
    return render_template(
        "activities.html",
        nickname=get_nickname(userID),
        my_activities=my_activities,
        avatar=get_avatar_path(userID),
    )


# 顯示創建活動的頁面
@activity_bp.route("/hostActivity/<string:id>", methods=["GET"])
def hostActivity(id):
    nickname = get_nickname(session["userID"])
    cityList = [
        "臺北市",
        "新北市",
        "桃園市",
        "臺中市",
        "臺南市",
        "高雄市",
        "新竹縣",
        "苗栗縣",
        "彰化縣",
        "南投縣",
        "雲林縣",
        "嘉義縣",
        "屏東縣",
        "宜蘭縣",
        "花蓮縣",
        "臺東縣",
        "澎湖縣",
        "金門縣",
        "連江縣",
        "基隆市",
        "新竹市",
        "嘉義市",
        "其他",
    ]
    categoryList = ["影音展演", "商業投資", "遊戲卡牌", "體驗學習", "旅行出遊", "其他"]

    if id != "home":
        fun = "update"
        con = sql.connect("funCrew_db.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM Activity WHERE activityID = '%s' " % (id))
        info = cur.fetchall()
        return render_template(
            "hostActivity.html",
            cityList=cityList,
            categoryList=categoryList,
            fun=fun,
            nickname=nickname,
            id=id,
            info=info,
        )
    else:
        fun = "create"
        return render_template(
            "hostActivity.html",
            cityList=cityList,
            categoryList=categoryList,
            fun=fun,
            nickname=nickname,
            id=id,
        )


# 成功報名頁面
@activity_bp.route("/signUpSuccess/<string:id>", methods=["GET", "POST"])
def signUpSuccess(id):
    try:
        with sql.connect("funCrew_db.db") as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO Participant (participantUserID, participantActivityID)\
                VALUES (?, ?)",
                (session["userID"], id),
            )
            con.commit()
    except Exception as e:
        # print(e)
        con.rollback()
        msg = f"報名失敗！請確認你的資料。錯誤訊息：{str(e)}"
    return render_template("signUpSuccess.html")


# 參加名單(id:活動id)
def joinList(id):
    con = sql.connect("funCrew_db.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute(
        "SELECT participantUserID FROM Participant \
        WHERE participantActivityID = '%s'"
        % (id)
    )
    info = cur.fetchall()
    member = []
    for i in info:
        member.append(i[0])  # userID
    return member


# show personalActivity.html
@activity_bp.route("/show/<string:id>", methods=["POST", "GET"])
def show(id):
    try:
        sign = True
        info = {}
        info["nickname"] = get_nickname(session["userID"])
        info["userID"] = session["userID"]
        info["signUp"] = len(joinList(id))
        con = sql.connect("funCrew_db.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM Activity WHERE activityID = '%s' " % (id))
        data = cur.fetchall()
        info["createDate"] = str(datetime.fromtimestamp(int(data[0]["createTime"])))
        info["expireDate"] = data[0]["expireDate"]
        info["time"] = data[0]["time"]
        info["title"] = data[0]["title"]
        info["area"] = data[0]["area"]
        info["location"] = data[0]["location"]
        info["Intro"] = data[0]["Intro"]
        info["organizerUserID"] = data[0]["organizerUserID"]
        info["hostName"] = get_nickname(info["organizerUserID"])
        info["activityID"] = data[0]["activityID"]
        info["fee"] = data[0]["fee"]
        info["peopleLimited"] = data[0]["peopleLimited"]

        value = str(datetime.fromtimestamp(datetime.now().timestamp()).date())
        # value  = "2023-06-30"
        if value > info["expireDate"]:
            sign = False

        cur.execute(
            "SELECT * FROM Discussion WHERE discussionActivityID = '%s' \
                ORDER BY discussionTime DESC"
            % (id)
        )
        comment = cur.fetchall()
        nickname = {}
        time = {}
        for i in comment:
            nickname[i["discussionUserID"]] = get_nickname(i["discussionUserID"])
            time[i["discussionUserID"]] = str(
                datetime.fromtimestamp(int(i["discussionTime"]))
            )

    except Exception as e:
        # print(e)
        con.rollback()
        msg = f"刪除活動失敗！請確認你的資料。錯誤訊息：{str(e)}"
        return render_template("home.html", msg=msg)
    return render_template(
        "personalActivity.html",
        info=info,
        member=joinList(id),
        time=time,
        nickname=nickname,
        comment=comment,
        sign=sign,
    )


# 創立、更新
# 使用者在 hostActivity.html 提交表單的時候會執行
@activity_bp.route("/submitActivity/<string:id>", methods=["POST"])
def submitActivity(id):
    try:
        title = request.form["title"]
        Intro = request.form["Intro"]
        location = request.form["location"]
        time = request.form["time"]
        expireDate = request.form["expireDate"]
        if time < expireDate:
            msg = f"錯誤！請確認你的資料。錯誤訊息：{str(e)}"
            return render_template("hostActivity.html", msg=msg)
        peopleLimited = request.form["peopleLimited"]
        fee = request.form["fee"]
        area = request.form["area"]
        category = request.form["category"]
        signUp = 0
        status = "signingUp"
        # 取得當前使用者的userID
        userID = session.get("userID")
        with sql.connect("funCrew_db.db") as con:
            cur = con.cursor()
            if id == "create":
                id = str(uuid.uuid4())
                tn = datetime.now()
                ts = int(tn.timestamp())
                cur.execute(
                    "INSERT INTO Activity \
                        (activityID, title, Intro, time, area, location, category, \
                        peopleLimited, expireDate, fee, status, organizerUserID, signUp, createTime) \
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        id,
                        title,
                        Intro,
                        time,
                        area,
                        location,
                        category,
                        peopleLimited,
                        expireDate,
                        fee,
                        status,
                        userID,
                        signUp,
                        ts,
                    ),
                )
            else:
                cur.execute(
                    "Update Activity \
                        SET  title = title, Intro = Intro,\
                             time = time, area = area, location = location, category = category, \
                        peopleLimited = peopleLimited, expireDate = expireDate, fee = fee\
                        WHERE activityID = '%s'"
                    % (id)
                )
            con.commit()
        # 跳轉到 personalActivity 頁面
        return show(id)
    except Exception as e:
        # print(e)
        msg = f"活動創建失敗！請確認你的資料。"
        return render_template("hostActivity.html", msg=msg)


# 刪除活動
@activity_bp.route("/delAct/<string:activityID>", methods=["GET", "POST"])
def delAct(activityID):
    try:
        with sql.connect("funCrew_db.db") as con:
            cur = con.cursor()
            cur.execute(
                "DELETE FROM Activity \
                WHERE activityID = '%s'"
                % (activityID)
            )
            con.commit()
        # 跳轉到主頁面
        return redirect("/home")
    except Exception as e:
        # print(e)
        msg = f"刪除活動失敗！請確認你的資料。錯誤訊息：{str(e)}"
        return render_template("signUpSuccess.html", msg=msg)
    finally:
        con.close()


# 評分
@activity_bp.route("/rating/<string:id>", methods=["GET", "POST"])
def rating(id):
    try:
        rating = request.form["rating"]
        # print(rating, id, session["userID"])
        with sql.connect("funCrew_db.db") as con:
            cur = con.cursor()
            cur.execute(
                "Update Participant \
                    SET score = '%d' \
                    WHERE participantActivityID = '%s' and participantUserID = '%s'"
                % (int(rating), id, session["userID"])
            )
            con.commit()
        # 不跳轉畫面
        return ("", 204)
    except Exception as e:
        # print(e)
        con.rollback()
        msg = f"刪除活動失敗！請確認你的資料。錯誤訊息：{str(e)}"
        return render_template("signUpSuccess.html", msg=msg)
    finally:
        con.close()


# 留言區
@activity_bp.route("/comment/<string:id>", methods=["POST", "GET"])
def comment(id):
    try:
        comment = request.form["comment"]
        with sql.connect("funCrew_db.db") as con:
            cur = con.cursor()
        if len(comment) > 0:
            tn = datetime.now()
            ts = str(round(tn.timestamp()))
            cur.execute(
                "INSERT INTO Discussion \
                    (discussionUserID, discussionActivityID, discussionTime, discussionContent) \
                    VALUES(?, ?, ?, ?)",
                (session["userID"], id, ts, comment),
            )
            con.commit()
        # 跳轉到 personalActivity 頁面
        return show(id)
    except Exception as e:
        # print(e)
        con.rollback()
        msg = f"活動創建失敗！請確認你的資料。錯誤訊息：{str(e)}"
        return render_template("home.html", msg=msg)
    finally:
        con.close()


@activity_bp.route("/show/<int:id>", methods=["POST", "GET"])
def updateComment(id):
    with sql.connect("funCrew_db.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Discussion WHERE discussionID = '%d'" % (id))
        comment = cur.fetchall()
        content = comment[0][4]
        # print(content)
        id = comment[0][0]
        time = str(datetime.fromtimestamp(int(comment[0][3])))
    return render_template(
        "updateComment.html",
        content=content,
        time=time,
        nickname=get_nickname(comment[0][1]),
        id=id,
    )


@activity_bp.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    try:
        comment = request.form["comment"]
        # print(comment)
        with sql.connect("funCrew_db.db") as con:
            cur = con.cursor()
            tn = datetime.now()
            ts = str(round(tn.timestamp()))
            cur.execute(
                "SELECT discussionActivityID FROM Discussion WHERE discussionID = '%d'"
                % (id)
            )
            actID = cur.fetchall()
            cur.execute(
                "UPDATE  Discussion SET discussionContent = '%s' \
                WHERE discussionID = '%d'"
                % (comment, id)
            )
            con.commit()
        # 跳轉到 personalActivity 頁面
        return show(actID[0][0])
    except Exception as e:
        # print(e)
        con.rollback()
        msg = f"活動創建失敗！請確認你的資料。錯誤訊息：{str(e)}"
        return render_template("home.html", msg=msg)
    finally:
        con.close()


@activity_bp.route("/delete/<int:id>", methods=["POST", "GET"])
def delete(id):
    try:
        with sql.connect("funCrew_db.db") as con:
            cur = con.cursor()
            cur.execute(
                "SELECT discussionActivityID FROM Discussion WHERE discussionID = '%d'"
                % (id)
            )
            actID = cur.fetchall()
            cur.execute("DELETE FROM Discussion WHERE discussionID = '%d'" % (id))
            con.commit()
        # 跳轉到 personalActivity 頁面
        return show(actID[0][0])
    except Exception as e:
        # print(e)
        con.rollback()
        msg = f"活動創建失敗！請確認你的資料。錯誤訊息：{str(e)}"
        return render_template("home.html", msg=msg)
    finally:
        con.close()
