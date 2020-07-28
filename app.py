from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from model.article import Article
from model.user import User
from model.type import Type
from model.others import Notice, YysTv, File, Login

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)
api = Api(app)

api.add_resource(Article, "/api/v4/article", "/api/v4/article/<string:article_id>")
api.add_resource(Notice, "/api/v4/notice")
api.add_resource(YysTv, "/api/v4/yysTV")
api.add_resource(File, "/api/v4/file")
api.add_resource(Login, "/api/v4/login", "/api/v4/login/<string:user_id>")
api.add_resource(User, "/api/v4/user", "/api/v4/user/<string:user_id>")
api.add_resource(Type, "/api/v4/type", "/api/v4/type/<string:type_id>")
