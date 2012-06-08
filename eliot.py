import flask
from flask.ext.pymongo import PyMongo

app = flask.Flask(__name__)
app.config['MONGO_DBNAME'] = 'test'
mongo = PyMongo(app, config_prefix='MONGO')


@app.route('/')
def home_page():
    topics = [topic for topic in mongo.db.topics.find()]
    return flask.render_template("index.html", topics=topics)


@app.route('/vote/<string:topic>/', methods=['GET'])
def vote(topic):
    try:
        mongo.db.topics.update({'name': topic}, {"$inc": {"votes": 1}})
    finally:
        return flask.redirect('/')


@app.route('/add_topic/', methods=['POST'])
def add_topic():
    try:
        if flask.request.form.get('topic'):
            mongo.db.topics.insert({'name': flask.request.form.get('topic'), 'votes': 0}, {"unique": "true"})
    finally:
        return flask.redirect('/')

app.run()
