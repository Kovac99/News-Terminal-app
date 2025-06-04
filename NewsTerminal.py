from rich.text import Text
import requests
import time
from rich.console import Console
from rich.table import Table
from datetime import datetime

API_KEY = '2360c15698b24498a591772e95ec5811'
URL = 'https://newsapi.org/v2/top-headlines?language=en&apiKey=' + API_KEY

keywords = [
    'bitcoin', 'oil', 'stocks', 'breaking', 'gold', 'Trump', 'Ukraine', 'China', 'Putin', 'Russia',
    'Stock', 'Economy', 'economy', 'rate', 'Rate', 'money', 'crypto', 'usd', 'dollar',
    'Dollar', 'euro', 'Euro', 'Japan', 'Frank', 'Israel', 'war'
]

console = Console()

def fetch_news():
    response = requests.get(URL)
    return response.json()['articles']

def highlight_keywords(text, keywords):
    text_obj = Text(text)
    for kw in keywords:
        start = 0
        while True:
            index = text.lower().find(kw.lower(), start)
            if index == -1:
                break
            text_obj.stylize("bold red", index, index + len(kw))
            start = index + len(kw)
    return text_obj

def display_news(articles):
    table = Table(title="Real Time News Terminal", show_lines=True)
    table.add_column("Source", style="cyan", justify="center")
    table.add_column("Title", style="magenta", no_wrap=False, justify="left", overflow="fold")
    table.add_column("Published At", style="green", no_wrap=False, justify="center")

    for article in articles:
        published_str = article['publishedAt']
        published_dt = datetime.fromisoformat(published_str.replace('Z', '+00:00'))
        published_time = published_dt.strftime('%H:%M:%S')

        highlighted_title = highlight_keywords(article['title'], keywords)

        table.add_row(
            article['source']['name'],
            highlighted_title,
            published_time
        )

    console.clear()
    console.print(table)

if __name__ == '__main__':
    while True:
        news = fetch_news()
        display_news(news)
        time.sleep(60)