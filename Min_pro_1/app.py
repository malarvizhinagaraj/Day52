from flask import Flask, request
from flask_restful import Resource, Api
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
api = Api(app)

# In-memory store
posts = []
next_id = 1

# Post List Resource (GET all, POST new)
class PostListResource(Resource):
    def get(self):
        return posts

    def post(self):
        global next_id
        data = request.get_json()

        if not data.get('title') or not data.get('content'):
            raise BadRequest('Both title and content are required.')

        post = {
            'id': next_id,
            'title': data['title'],
            'content': data['content'],
            'author': data.get('author', 'Anonymous')
        }
        posts.append(post)
        next_id += 1
        return post, 201

# Single Post Resource (GET, PUT, DELETE)
class PostResource(Resource):
    def get(self, post_id):
        for post in posts:
            if post['id'] == post_id:
                return post
        return {'error': 'Post not found'}, 404

    def put(self, post_id):
        data = request.get_json()
        for post in posts:
            if post['id'] == post_id:
                if 'title' in data:
                    post['title'] = data['title']
                if 'content' in data:
                    post['content'] = data['content']
                if 'author' in data:
                    post['author'] = data['author']
                return post
        return {'error': 'Post not found'}, 404

    def delete(self, post_id):
        for post in posts:
            if post['id'] == post_id:
                posts.remove(post)
                return {'message': f'Post {post_id} deleted'}
        return {'error': 'Post not found'}, 404

# Route setup
api.add_resource(PostListResource, '/posts')
api.add_resource(PostResource, '/posts/<int:post_id>')

if __name__ == '__main__':
    app.run(debug=True)
