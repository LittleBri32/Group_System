from extensions import db

# 建立 User table
class User(db.Model):
    __tablename__ = 'User'
    userID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String(255))
    nickname = db.Column(db.String(64), unique=True)
    gender = db.Column(db.String(1), nullable=False)
    age = db.Column(db.Integer)
    reputationScore = db.Column(db.Integer)
    cellphone = db.Column(db.String(10))
    email = db.Column(db.String(50))
    genderOption = [
        ("F", "Female"),
        ("M", "Male"),
        ("N", "Non-binary"),
    ]


# 建立 Activity table
class Activity(db.Model):
    __tablename__ = 'Activity'
    activityID = db.Column(db.Integer, primary_key = True , autoincrement = True)
    title = db.Column(db.String(30))
    intro = db.Column(db.Text)
    time = db.Column(db.DateTime)
    area = db.Column(db.String(1))
    location = db.Column(db.String(30))
    category = db.Column(db.String(1))
    peopleLimited = db.Column(db.Integer)
    signUp = db.Column(db.Integer)
    fee = db.Column(db.Integer)
    expireDate = db.Column(db.Date)
    status = db.Column(db.String(1))
    hostID = db.Column(db.Integer, db.ForeignKey('User.userID')) #發起人ID

    host = db.relationship('User',) 
    area_option = [
        ("N", "北部"),
        ("W", "西部"),
        ("S", "南部"),
        ("E", "東部"),
        ("I", "離島"),
    ]
    status_option = [
        ("F", "已額滿"),
        ("A", "可加入"),
        ("E", "已結束"),
    ]
    category_option = [
        ("1", "其他"),
        ("2", "運動"),
        ("3", "團購"),
        ("4", "搭車"),
        ("5", "唱歌"),
        ("6", "美食"),
        ("7", "逛街")
    ]
    


# 建立 Discussion table
class Discussion(db.Model):
    __tablename__ = 'Discussion'
    discussionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    discussionUserID = db.Column(db.Integer, db.ForeignKey('User.userID'))
    discussionActivityID = db.Column(db.Integer, db.ForeignKey('Activity.activityID'))
    discussionTime = db.Column(db.DateTime)
    discussionContent = db.Column(db.String(255))

    user = db.relationship('User')
    activity = db.relationship('Activity')




# 建立 Participant table
class Participant(db.Model):
    __tablename__ = 'Participant'
    participantUserID = db.Column(db.Integer, db.ForeignKey('User.userID'), primary_key=True)
    participantActivityID = db.Column(db.Integer, db.ForeignKey('Activity.activityID'), primary_key=True)
    score = db.Column(db.Integer)

    user = db.relationship('User')
    activity = db.relationship('Activity')



# 建立 Post table
class Post(db.Model):
    __tablename__ = 'Post'
    postID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    postUserID = db.Column(db.Integer, db.ForeignKey('User.userID'))
    postTime = db.Column(db.DateTime)
    postContent = db.Column(db.Text)

    user = db.relationship('User')


# # 建立 Hashtag table
# class Hashtag(db.Model):
#     __tablename__ = 'Hashtag'
#     postID = db.Column(db.Integer, db.ForeignKey('Post.postID'), primary_key = True)
#     hashtag = db.Column(db.String(50), primary_key = True)

#     post = db.relationship('Post')


# 建立 Comment table
class Comment(db.Model):
    __tablename__ = 'Comment'
    commentID = db.Column(db.Integer, primary_key=True, autoincrement = True)
    commentPostID = db.Column(db.Integer, db.ForeignKey('Post.postID'))
    commentUserID = db.Column(db.Integer, db.ForeignKey('User.userID'))
    commentTime = db.Column(db.DateTime)
    commentContent = db.Column(db.Text)

    post = db.relationship('Post')
    user = db.relationship('User')




