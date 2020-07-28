from config import *
from flask_restful import Resource, reqparse


class Article(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        # 参数列表
        arg_list = [
            {"arg": "pageSize", "type": int},
            {"arg": "pageNum", "type": int},
            {"arg": "typeId", "type": int},
            {"arg": "title", "type": str},
            {"arg": "content", "type": str},
            {"arg": "introduce", "type": str},
            {"arg": "addTime", "type": str},
            {"arg": "userId", "type": int},
        ]
        for item in arg_list:
            self.parser.add_argument(item["arg"], type=item["type"])

    # 获取文章
    def get(self, article_id=None):
        with SQLManager() as db:
            if article_id:
                sql = (
                    "SELECT article.id as id,article.title as title,article.introduce as introduce,"
                    "article.content as content,article.typeId as typeId,article.userId as userId,"
                    "article.addTime as addTime,type.typeName as typeName,user.username as username "
                    "FROM article LEFT JOIN type ON article.typeId=type.id LEFT JOIN user ON "
                    "article.userId=user.id WHERE article.id=%s"
                )
                try:
                    result = db.get_one(sql, article_id)
                    return {
                        "code": 0,
                        "data": result,
                    }
                except Exception as e:
                    return {
                        "code": 1,
                        "data": e,
                    }
            else:
                data = self.parser.parse_args()
                type_id = data.get("typeId")
                page_size = data.get("pageSize")
                page_num = data.get("pageNum")
                if type_id:
                    sql = (
                        "SELECT article.id as id,article.title as title,article.introduce as introduce,"
                        "article.addTime as addTime,type.typeName as typeName,user.username as username "
                        "FROM article LEFT JOIN type ON article.typeId=type.id LEFT JOIN user ON "
                        "article.userId=user.id WHERE article.typeId=%s ORDER BY article.id DESC LIMIT %s,%s "
                    )
                    result = db.get_list(
                        sql, (type_id, page_size * (page_num - 1), page_size)
                    )
                else:
                    sql = (
                        "SELECT article.id as id,article.title as title,article.introduce as introduce,"
                        "article.addTime as addTime,type.typeName as typeName,user.username as username "
                        "FROM article LEFT JOIN type ON article.typeId=type.id LEFT JOIN user ON "
                        "article.userId=user.id ORDER BY article.id DESC LIMIT %s,%s ;"
                    )
                    result = db.get_list(sql, (page_size * (page_num - 1), page_size))
                count = db.get_one("SELECT COUNT(id) FROM article")
                return {
                    "code": 0,
                    "data": result,
                    "total": count["COUNT(id)"],
                }

    # 新增文章
    def post(self):
        with SQLManager() as db:
            data = self.parser.parse_args()
            sql = "INSERT INTO article(title,content,introduce,addTime,typeId,userId) VALUES (%s,%s,%s,%s,%s,%s)"
            try:
                insert_id = db.create(
                    sql,
                    (
                        data.get("title"),
                        data.get("content"),
                        data.get("introduce"),
                        data.get("addTime"),
                        data.get("typeId"),
                        data.get("userId"),
                    ),
                )
                return {"code": 0, "insertId": insert_id}
            except Exception as e:
                return {"code": 1, "data": e}

    # 删除文章
    def delete(self, article_id=None):
        if article_id:
            with SQLManager() as db:
                sql = "DELETE FROM article WHERE id=%s"
                try:
                    db.modify(sql, article_id)
                    return {"code": 0}
                except Exception as e:
                    return {"code": 1, "data": e}
