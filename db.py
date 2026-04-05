from flask_pymongo import PyMongo

mongo = PyMongo()

def init_db(app):
    app.config.from_object('config.Config')
    mongo.init_app(app)
    return mongo