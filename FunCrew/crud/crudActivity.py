from flask import Blueprint, request, render_template, session, redirect
import sqlite3 as sql
import uuid
from datetime import datetime
from .crudUser import get_nickname

activity_bp = Blueprint('activity', __name__)

#顯示創建活動的頁面
@activity_bp.route("/hostActivity/<string:id>", methods=["GET"])
def hostActivity(id):
    cityList = ['臺北市','新北市','桃園市','臺中市','臺南市','高雄市','新竹縣',
    '苗栗縣','彰化縣','南投縣','雲林縣','嘉義縣','屏東縣','宜蘭縣','花蓮縣',
    '臺東縣','澎湖縣','金門縣','連江縣','基隆市','新竹市','嘉義市','其他']
    categoryList = ['影音展演','商業投資','遊戲卡牌','體驗學習','旅行出遊','其他']
    if id != 'home' :
        fun = 'update'
    else:
        fun = 'create'    
    return render_template("hostActivity.html", cityList = cityList, categoryList = categoryList,
        fun = fun, nickname=get_nickname(session["userID"]), id = id)

#成功報名頁面
@activity_bp.route("/signUpSuccess/<string:id>", methods=["GET","POST"])
def signUpSuccess(id):
    try:
        with sql.connect("funCrew_db.db") as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO Participant \
                    (participantUserID, participantActivityID)\
                    VALUES (?, ?)",
                (
                    session['userID'],id
                ),
            )
            con.commit()
    except Exception as e:
        print(e)
        con.rollback()
        msg = f"活動讀取失敗！請確認你的資料。錯誤訊息：{str(e)}"
    return render_template("signUpSuccess.html")

#創建活動後顯示活動頁面
def showActivity(Id, actID):
    try:
        con = sql.connect("funCrew_db.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM Activity, User WHERE activityID = '%s' and userID ='%d' \
                and organizerUserID = userID " %(actID, Id)
        )
        info = cur.fetchall()
        return render_template(
            "personalActivity.html", info=info, userID = session["userID"],\
                nickname=get_nickname(session["userID"]),  member = joinList(id)
        )
    except Exception as e:
        print(e)
        con.rollback()
        msg = f"活動讀取失敗！請確認你的資料。錯誤訊息：{str(e)}"
        return render_template("home.html", msg=msg)

def joinList(id):
    con = sql.connect("funCrew_db.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute(
        "SELECT participantUserID FROM Participant \
        WHERE participantActivityID = '%s'"\
        %(id)
    )
    info = cur.fetchall()
    member = []
    for i in info:
        member.append(i[0]) #userID
    return member
@activity_bp.route("/showAct/<string:id>", methods=["POST","GET"])
def showAct(id):
    con = sql.connect("funCrew_db.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM Activity WHERE activityID = '%s' " %(id)
    )
    info = cur.fetchall()
    print(info[0]['area'])
    return render_template(
        "personalActivity.html", info = info, userID = session["userID"],\
            nickname=get_nickname(session["userID"]), member = joinList(id)
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
        peopleLimited = request.form["peopleLimited"]
        fee = request.form["fee"]
        area = request.form["area"]
        category = request.form["category"]
        signUp = 0
        status = 'N'
        # 取得當前使用者的userID
        userID = session.get("userID")
        with sql.connect("funCrew_db.db") as con:
            cur = con.cursor()
            if id == 'create':
                id = str(uuid.uuid4())
                tn = datetime.now() 
                ts = int(tn.timestamp())
                cur.execute(
                    "INSERT INTO Activity \
                        (activityID, title, Intro, time, area, location, category, \
                        peopleLimited, expireDate, fee, status, organizerUserID, signUp, createTime) \
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        id, title, Intro, time, area, location, category,
                        peopleLimited, expireDate, fee, status, userID, signUp, ts
                    ),
                )
            else:
                cur.execute(
                    "Update Activity \
                        SET activityID = id , title = title, Intro = Intro,\
                             time = time, area = area, location = location, category = category, \
                        peopleLimited = peopleLimited, expireDate expireDate, fee \
                        WHERE activityID = '%s'" %(id) \
                        
                )
            con.commit()
        # 跳轉到 personalActivity 頁面
        return showActivity(userID, id)
        # return render_template("personalActivity.html", activityID = id, userID = userID)
    except Exception as e:
        print(e.message)
        con.rollback()
        msg = f"活動創建失敗！請確認你的資料。錯誤訊息：{str(e)}"
        return render_template("home.html", msg=msg)
    finally:
        con.close()

#刪除活動
@activity_bp.route("/delAct/<string:activityID>", methods=["GET","POST"])
def delAct(activityID):
    try:
        with sql.connect("funCrew_db.db") as con:
            cur = con.cursor()
            cur.execute(
                "DELETE FROM Activity \
                WHERE activityID = '%s'" %(activityID)      
            )
            con.commit()
        # 跳轉到主頁面
        return redirect("/home")
    except Exception as e:
        print(e)
        con.rollback()
        msg = f"刪除活動失敗！請確認你的資料。錯誤訊息：{str(e)}"
        return render_template("signUpSuccess.html", msg=msg)
    finally:
        con.close()

# 評分
@activity_bp.route("/rating/<string:id>", methods=["GET","POST"])        
def rating(id):
    try:
        rating = request.form["rating"]
        print(rating,id,session["userID"])
        with sql.connect("funCrew_db.db") as con:
            cur = con.cursor()
            cur.execute(
                "Update Participant \
                    SET score = '%d' \
                    WHERE participantActivityID = '%s' and participantUserID = '%s'" %(int(rating),id,session["userID"])
            )
            con.commit()
        # 不跳轉畫面
        return ('', 204)
    except Exception as e:
        print(e)
        con.rollback()
        msg = f"刪除活動失敗！請確認你的資料。錯誤訊息：{str(e)}"
        return render_template("signUpSuccess.html", msg=msg)
    finally:
        con.close()