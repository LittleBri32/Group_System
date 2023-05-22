from extensions import db
from database import *
from dateutil.parser import parse
from flask import Blueprint, request


activity_bp = Blueprint('Activity', __name__)


# 顯示所有活動
@activity_bp.route("/activity/all",methods = ['POST'])
def showAllActivity(activityType):
    if activityType and activityType != "ALL":
        activities = Activity.query.filter(Activity.status.in_(['F', 'A']), Activity.type==activityType).all()
    else:
        activities = Activity.query.filter(Activity.status.in_(['F', 'A'])).all()

    activities_list = []

    for activity in activities:
        activities_list.append({
            'activityID': activity.activityID,
            'title': activity.title,
            'intro': activity.intro,
            'time': activity.time,
            'area': activity.area,
            'location': activity.location,
            'category': activity.category,
            'peopleLimited': activity.peopleLimited,
            'signUp': activity.signUp,
            'fee': activity.fee,
            'expireDate': activity.expireDate,
            'status': activity.status,
            'hostID': activity.hostID,
        })

    result = {'activities': activities_list}
    return result, 200





# 顯示使用者參加的活動
@activity_bp.route("/my",methods = ['POST'])
def showMyActivity(jsonData):
    pass



# 發起活動
@activity_bp.route("/create",methods = ['POST'])
def createActivity(jsonData):
    # 讀取活動資訊
    intro = jsonData.get('intro')
    time = parse(jsonData.get('time')) if jsonData.get('time') else None
    area = jsonData.get('area')
    location = jsonData.get('location')
    peopleLimited = jsonData.get('peopleLimited')
    signUp = jsonData.get('signUp')
    fee = jsonData.get('fee')
    title = jsonData.get('title')

    category = jsonData.get('category')
    expireDate = parse(jsonData.get('expireDate')).date() if jsonData.get('expireDate') else None
    status = jsonData.get('status')
    hostID = jsonData.get('hostID')

    # 檢查必要欄位是否存在
    if not (hostID and time and area and location and peopleLimited and signUp and fee and expireDate and status and type):
        return {'error': 'Missing required fields'}, 400

    # 檢查地區選項是否合法
    area_options = [option[0] for option in Activity.area_option]
    if area not in area_options:
        return {'error': 'Invalid area'}, 400

    # 檢查狀態選項是否合法
    status_options = [option[0] for option in Activity.status_option]
    if status not in status_options:
        return {'error': 'Invalid status'}, 400

    # 建立新活動
    activity = Activity(
        hostID = hostID,
        title = title,
        intro = intro,
        status = status,
        time = time,
        area = area,
        location = location,
        peopleLimited = peopleLimited,
        signUp = signUp,
        fee = fee,
        expireDate = expireDate,
        category = category
    )
    try:
        db.session.add(activity)
        db.session.commit()
        return {'message': 'Activity created successfully'}, 201
    except Exception as e:
        return {'error': str(e)}, 500





# 刪除活動
@activity_bp.route("/activity/delete",methods = ['POST'])

def deleteActivity(jsonData):
    # 讀取活動 ID
    activityID = jsonData.get('activityID')
    if activityID is None:
        return {'error': 'Missing activity ID'}, 400
    # 在資料庫中查找活動
    activity = Activity.query.get(activityID)
    if activity is None:
        return {'error': 'Activity not found'}, 404
    # 檢查當前用戶是否為活動主辦者
    # if current_user.userID != activity.hostID:  # 新增
    #     return {'error': 'Only the host can delete the activity'}, 403  # 新增
    # 刪除活動
    try:
        db.session.delete(activity)
        db.session.commit()
        return {'message': 'Activity deleted successfully'}, 200
    except Exception as e:
        return {'error': str(e)}, 500



# 修改活動
@activity_bp.route("/update",methods = ['POST'])
def modifyActivity(jsonData):
    pass


# 加入活動
@activity_bp.route("/join",methods = ['POST'])
def joinActivity(jsonData):
    pass

# 退出活動
@activity_bp.route("/leave",methods = ['POST'])
def leaveActivity(jsonData):
    pass

# 評分
@activity_bp.route("/rate",methods = ['POST'])
def rateActivity(jsonData):
    pass

# 留言討論
@activity_bp.route("/discussion",methods = ['POST'])
def engageActivity(jsonData):
    pass

