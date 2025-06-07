from flask import Flask, render_template_string
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = '2360c15698b24498a591772e95ec5811'
URL = f'https://newsapi.org/v2/top-headlines?language=en&apiKey={API_KEY}'

keywords = ['bitcoin', 'oil', 'stocks', 'breaking', 'gold', 'Trump', 'Ukraine', 'China', 'Putin', 'Russia']
def highlight_keywords(text):
    for kw in keywords:
        text = text.replace(kw, f'<span style="color:red", font-weight:"bold">{kw}</span>')
    return text

@app.route('/news')
def news():
    response = requests.get(URL)
    data = response.json()
    articles = data.get('articles', [])
    for article in articles:
        article['title'] = highlight_keywords(article['title'])
        dt = datetime.fromisoformat(article['publishedAt'].replace('Z', '+00:00'))
        article['publishedAt'] = dt.strftime('%Y-%m-%d %H:%M:%S')

    html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <title>News Terminal</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { width: 100%; border-collapse: collapse; }
                th, td { border: 1px solid #ccc; padding: 8px; }
                th { background-color: #333; color: white; }
                tr:nth-child(even) { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h1>News Terminal</h1>
            <table>
                <thead>
                    <tr>
                        <th>Source</th>
                        <th>Title</th>
                        <th>Published At</th>
                    </tr>
                </thead>
                <tbody>
                    {% for article in articles %}
                    <tr>
                        <td>{{ article.source.name }}</td>
                        <td>{{ article.title|safe }}</td>
                        <td>{{ article.publishedAt }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </body>
        </html>
        """
    return render_template_string(html, articles=articles)
@app.route('/')
def home():
    return '<h1>Welcome to the Trading Website</h1><p>Visit <a href="/news">News Terminal</a></p>'

if __name__ == '__main__':
    app.run(debug=True)