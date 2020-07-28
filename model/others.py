from flask import request
from flask_restful import Resource, reqparse
from config import *


class Notice(Resource):
    def get(self):
        with SQLManager() as db:
            sql = (
                "SELECT article.id as id,article.title as title,article.introduce as introduce,"
                "article.addTime as addTime,type.typeName as typeName,user.username as username "
                "FROM article LEFT JOIN type ON article.typeId=type.id LEFT JOIN user ON "
                "article.userId=user.id WHERE article.id=4"
            )
            result = db.get_one(sql)
            return {"code": 0, "data": result}


class YysTv(Resource):
    def get(self):
        with SQLManager() as db:
            sql = "SELECT id,title,href,bg from yysTV"
            result = db.get_list(sql)
            return {"code": 0, "data": result}


class File(Resource):
    def post(self):
        f = request.files["file"]
        path = "http://212.64.78.155/images/" + f.filename
        f.save("/usr/share/nginx/images/" + f.filename)
        return {"code": 0, "path": path}


class Login(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        # 参数列表
        arg_list = [
            {"arg": "username", "type": str},
            {"arg": "password", "type": str},
            {"arg": "newPassword", "type": str},
        ]
        for item in arg_list:
            self.parser.add_argument(item["arg"], type=item["type"])

    # 用户登陆
    def post(self):
        with SQLManager() as db:
            data = self.parser.parse_args()
            username = data.get("username")
            password = data.get("password")
            sql = "SELECT id,username,avatar FROM user WHERE username=%s AND password=MD5(%s)"
            result = db.get_one(sql, (username, password))
            if result:
                return {"code": 0, "msg": "登陆成功", "data": result}
            else:
                return {"code": 1, "msg": "登陆失败"}

    # 修改密码
    def put(self, user_id=None):
        with SQLManager() as db:
            data = self.parser.parse_args()
            password = data.get("password")
            new_password = data.get("newPassword")
            sql = "SELECT id,username,avatar FROM user WHERE id=%s AND password=MD5(%s)"
            result = db.get_one(sql, (user_id, password))
            if result:
                db.modify(
                    "UPDATE user SET password=MD5(%s) WHERE id=%s",
                    (new_password, user_id),
                )
                return {"code": 0}
            else:
                return {"code": 1}
