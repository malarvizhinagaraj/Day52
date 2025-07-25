from flask import Flask, request, jsonify

app = Flask(__name__)

articles = []
article_id_counter = 1

@app.route('/articles', methods=['GET'])
def get_articles():
    category = request.args.get('category')
    date = request.args.get('published_date')

    filtered = articles
    if category:
        filtered = [a for a in filtered if a['category'] == category]
    if date:
        filtered = [a for a in filtered if a['published_date'] == date]

    return jsonify({'articles': filtered}), 200

@app.route('/articles', methods=['POST'])
def create_article():
    global article_id_counter
    data = request.get_json()
    headline = data.get('headline')
    category = data.get('category')
    published_date = data.get('published_date')

    if not all([headline, category, published_date]):
        return jsonify({'error': 'All fields are required.'}), 400

    article = {
        'id': article_id_counter,
        'headline': headline,
        'category': category,
        'published_date': published_date
    }
    articles.append(article)
    article_id_counter += 1

    return jsonify({'message': 'Article added.', 'article': article}), 201

@app.route('/articles/<int:article_id>', methods=['PUT'])
def update_article(article_id):
    data = request.get_json()
    for article in articles:
        if article['id'] == article_id:
            article['headline'] = data.get('headline', article['headline'])
            article['category'] = data.get('category', article['category'])
            article['published_date'] = data.get('published_date', article['published_date'])
            return jsonify({'message': 'Article updated.', 'article': article}), 200

    return jsonify({'error': 'Article not found.'}), 404

@app.route('/articles/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    for article in articles:
        if article['id'] == article_id:
            articles.remove(article)
            return jsonify({'message': 'Article deleted.'}), 200

    return jsonify({'error': 'Article not found.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
