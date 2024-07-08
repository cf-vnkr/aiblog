import os
import requests
from slugify import slugify
from datetime import datetime
import random
from tasks import build
import subprocess
import time

ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
AUTH_TOKEN = os.environ.get("CLOUDFLARE_AUTH_TOKEN")

today = datetime.today().strftime('%Y-%m-%d %H:%M')
today_date = datetime.today().strftime('%Y-%m-%d')


def return_answer (response):
    dictionary = response.json()
    string = dictionary['result']['response']
    answer = string.split("\n\n")[1]
    return answer

def write_article (title, title_slug, story, news_theme, image, today, today_date):
    file_name = f"content/{today_date}-{title_slug}.md"
    try:
        f = open(file_name, "a")
        f.write(f"Title: {title}\n")
        f.write(f"Date: {today}\n")
        f.write(f"Category: {news_theme}\n")
        f.write("\n")
        f.write("> This article is AI generated!\n")
        f.write("\n")
        f.write(f"![Alt Text](images/{image})\n")
        f.write("\n")
        f.write(story)
        f.close()
    except Exception as e:
       # By this way we can know about the type of error occurring
        print("Couldn't write article to file: ",e)

news_types: list[str] = [
    "technology",
    "biotech",
    "cyber security",
    "smart home",
    "IoT",
    "gaming",
    "green energy",
    "autosports",
    "space exploration",
    "mobile devices",
    "daily joke"
]

while True:
    news_theme = random.choice(news_types)

    prompt = f"Give me one name for a {news_theme} related news article"
    response = requests.post(
    f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/meta/llama-3-8b-instruct",
        headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
        json={
        "messages": [
            {"role": "system", "content": "You are a professional assistant"},
            {"role": "user", "content": prompt}
        ]
        }
    )

    try:
        response.status_code
        title = return_answer(response)
        print(title)
    except Exception as e:
       # By this way we can know about the type of error occurring
        print("Couldn't generate title: ",e)
        continue

    title_slug = slugify(title)

    prompt = f"Create an article with 3 paragraphs named {title}."
    response = requests.post(
    f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/meta/llama-3-8b-instruct",
        headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
        json={
        "messages": [
            {"role": "system", "content": "You are a professional assistant"},
            {"role": "user", "content": prompt}
        ]
        }
    )

    try:
        response.status_code
        article = return_answer(response)
        print(article)
    except Exception as e:
       # By this way we can know about the type of error occurring
        print("Couldn't generate article body: ",e)
        continue

    prompt = f"{title}"
    image_name = f"{today_date}-{title_slug}.png"
    response = requests.post(
    f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/stabilityai/stable-diffusion-xl-base-1.0",
        headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
        json={"prompt": prompt}
    )
    try:
        with open(f"content/images/{image_name}", "wb") as f:
            f.write(response.content)
    except Exception as e:
       # By this way we can know about the type of error occurring
        print("Couldn't generate image: ",e)
        continue

    try:
        write_article(title, title_slug, article, news_theme, image_name, today, today_date)
    except Exception as e:
       # By this way we can know about the type of error occurring
        print("Couldn't invoke write_article: ",e)
        continue

    try:
        subprocess.run(['pelican', 'content'])
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', today])
        subprocess.run(['git','push'])
    except Exception as e:
       # By this way we can know about the type of error occurring
        print("Couldn't build or commit: ",e)
        continue

    hour = 3600
    time.sleep(random.randint(6, 36) * hour)