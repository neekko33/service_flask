from flask_restful import Resource, reqparse
from config import *


class User(Resource):

    # 获取用户信息
    def get(self, user_id=None):
        with SQLManager() as db:
            if user_id:
                sql = (
                    "SELECT id,avatar,username,nickname,tags,address,introduce "
                    "FROM user NATURAL JOIN userInfo WHERE id=%s"
                )
                result = db.get_one(sql, user_id)
                return {"code": 0, "data": result}
            else:
                sql = "SELECT id,username,nickname,tags,address,introduce FROM user NATURAL JOIN userInfo"
                result = db.get_list(sql)
                return {"code": 0, "data": result}

    # TODO: 新增用户
    def post(self):
        pass

    # TODO: 编辑用户信息
    def put(self, user_id=None):
        pass

    # TODO: 删除用户
    def delete(self, user_id=None):
        pass
