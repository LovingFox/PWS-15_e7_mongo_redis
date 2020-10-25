import os
from flask import Flask, app
from flask_restful import Api
from flask_mongoengine import MongoEngine

from api import cache, AdvertsApi, AdvertApi, AdvTagsApi, AdvCommentApi, AdvStatApi

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')

app = Flask(__name__)

app.config['MONGODB_HOST'] = MONGO_HOST
app.config['MONGODB_DB'] = 'board'
app.config["CACHE_TYPE"] = 'redis'
app.config["CACHE_REDIS_HOST"] = REDIS_HOST


api = Api(app)
db = MongoEngine(app)
cache.init_app(app)

api.add_resource(AdvertsApi,      '/advs')
api.add_resource(AdvertApi,       '/adv/<adv_id>')
api.add_resource(AdvTagsApi,      '/tags/<adv_id>')
api.add_resource(AdvCommentApi,   '/comment/<adv_id>')
api.add_resource(AdvStatApi,      '/stat/<adv_id>')

app.run(debug=True)

