from flask_restful import Resource, reqparse
from config import *


class Type(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("typeName", type=str)

    # 查找类型
    def get(self):
        with SQLManager() as db:
            result = db.get_list("SELECT id,typeName from type")
            return {"code": 0, "data": result}

    # 增加类型
    def post(self):
        with SQLManager() as db:
            data = self.parser.parse_args()
            type_name = data.get("typeName")
            insert_id = db.create("INSERT INTO type(typeName) VALUES(%s)", type_name)
            return {"code": 0, "insertId": insert_id}

    # 修改类型
    def put(self, type_id=None):
        with SQLManager() as db:
            data = self.parser.parse_args()
            type_name = data.get("typeName")
            db.modify("UPDATE type SET typeName=%s WHERE id=%s", (type_name, type_id))
            return {"code": 0}

    # 删除类型
    def delete(self, type_id=None):
        with SQLManager() as db:
            db.modify("DELETE FROM type WHERE id=%s", type_id)
            return {"code": 0}
