import flask
from flask.ext.pymongo import PyMongo
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from bson import json_util
import json
import gevent

app = flask.Flask(__name__)
app.config['MONGO_DBNAME'] = 'test'
mongo = PyMongo(app, config_prefix='MONGO')


@app.route('/poll')
def poll():
    ws = flask.request.environ.get('wsgi.websocket')
    topics = [topic for topic in mongo.db.topics.find()]
    while True:
        try:
            ws.send(json.dumps(topics, default=json_util.default))
        except Exception, e:
            print e
        gevent.sleep(1)


@app.route('/')
def home_page():
    topics = [topic for topic in mongo.db.topics.find()]
    return flask.render_template("index.html", topics=topics)


@app.route('/vote/<string:topic>/', methods=['GET'])
def vote(topic):
    try:
        mongo.db.topics.update({'name': topic}, {"$inc": {"votes": 1}})
    finally:
        return "worked"


@app.route('/add_topic/', methods=['POST'])
def add_topic():
    try:
        if flask.request.form.get('topic'):
            mongo.db.topics.insert({'name': flask.request.form.get('topic'), 'votes': 0}, {"unique": "true"})
    finally:
        return "worked"

if __name__ == '__main__':
    server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
