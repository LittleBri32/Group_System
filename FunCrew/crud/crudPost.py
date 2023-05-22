from extensions import db
from database import *
from flask import Blueprint, request


post_bp = Blueprint('post', __name__)

# 顯示所有貼文
@post_bp.route("/post",methods = ['POST'])
def showThePost(jsonDict):
    pass

# 貼文


# 刪除貼文

# 留言

# 刪除留言