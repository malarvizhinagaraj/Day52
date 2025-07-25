from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

users = []
next_id = 1

class UserResource(Resource):
    def get(self, user_id):
        user = next((u for u in users if u['id'] == user_id), None)
        if not user:
            return {"error": "User not found"}, 404
        return user

    def put(self, user_id):
        data = request.get_json()
        user = next((u for u in users if u['id'] == user_id), None)
        if not user:
            return {"error": "User not found"}, 404
        user.update(data)
        return user

    def delete(self, user_id):
        global users
        users = [u for u in users if u['id'] != user_id]
        return {"message": "Deleted"}, 200

class UserListResource(Resource):
    def get(self):
        return users

    def post(self):
        global next_id
        data = request.get_json()
        data['id'] = next_id
        next_id += 1
        users.append(data)
        return data, 201

api.add_resource(UserListResource, '/api/users')
api.add_resource(UserResource, '/api/users/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
