from flask import Flask, render_template, request, session, Response, redirect
from database import connector
from model import entities
import json
import time

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        js = json.dumps(user, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { 'status': 404, 'message': 'Not Found'}
    return Response(message, status=404, mimetype='application/json')

@app.route('/users', methods = ['POST'])
def create_user():
    c =  json.loads(request.form['values'])
    user = entities.User(
        username=c['username'],
        name=c['name'],
        password=c['password']
    )
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    return 'Created User'

@app.route('/users', methods = ['GET'])
def get_users():
    session = db.getSession(engine)
    dbResponse = session.query(entities.User)
    data = []
    for user in dbResponse:
        data.append(user)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/users', methods = ['PUT'])
def update_user():
    session = db.getSession(engine)
    id = request.form['key']
    user = session.query(entities.User).filter(entities.User.id == id).first()
    c =  json.loads(request.form['values'])
    for key in c.keys():
        setattr(user, key, c[key])
    session.add(user)
    session.commit()
    return 'Updated User'

@app.route('/users', methods = ['DELETE'])
def delete_users():
    id = request.form['key']
    session = db.getSession(engine)
    messages = session.query(entities.User).filter(entities.User.id == id).one()
    session.delete(messages)
    session.commit()
    return "Deleted User"

@app.route('/authenticate', methods=['POST'])
def authenticate():
    message=json.loads(request.data)
    username=message['username']
    password=message['password']
    db_session = db.getSession(engine)
    try:
        user = db_session.query(entities.User
            ).filter(entities.User.username==username
            ).filter(entities.User.password==password
            ).one()
        session['logged_user']=user.id
        message = {'message':'Authorized'}
        return Response(message, status=200, mimetype='application/json')
    except Exception:
        message = {'message':'Unauthorized'}
        return Response(message, status=401, mimetype='application/json')

@app.route('/CrearUsuarios', methods = ["POST"])
def CrearUsuarios():
    message = json.loads(request.data)
    user = entities.User(
    name=message['name'],
    username=message['username'],
    password= message['password']
    )
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    message = {'message': 'User Created'}
    return Response(message, status=200, mimetype='application/json')


if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=5000, threaded=True, host=('127.0.0.1'))
