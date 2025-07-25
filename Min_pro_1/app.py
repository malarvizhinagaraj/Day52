from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)
api = Api(app)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Malar@localhost/userdb'

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:Malar@localhost/userdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)
 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
 
    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'email': self.email}
 

with app.app_context():
    db.create_all()
 

class UserList(Resource):
    def get(self):
        users = User.query.all()
        return {'users': [user.to_dict() for user in users]}, 200
 
    def post(self):
        data = request.get_json()
        if not data or 'name' not in data or 'email' not in data:
            return {'message': 'Name and email are required.'}, 400
 
        if User.query.filter_by(email=data['email']).first():
            return {'message': 'Email already exists.'}, 409
 
        new_user = User(name=data['name'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict(), 201
 

class UserResource(Resource):
    def get(self, id):
        user = User.query.get(id)
        if not user:
            return {'message': 'User not found.'}, 404
        return user.to_dict(), 200
 
    def put(self, id):
        user = User.query.get(id)
        if not user:
            return {'message': 'User not found.'}, 404
 
        data = request.get_json()
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        db.session.commit()
        return user.to_dict(), 200
 
    def delete(self, id):
        user = User.query.get(id)
        if not user:
            return {'message': 'User not found.'}, 404
 
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted'}, 200
 

api.add_resource(UserList, '/users')
api.add_resource(UserResource, '/users/<int:id>')
 
if __name__ == '__main__':
    app.run(debug=True)
