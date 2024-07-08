import os
import requests
from slugify import slugify
from datetime import datetime
import random
from tasks import build
import subprocess

ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
AUTH_TOKEN = os.environ.get("CLOUDFLARE_AUTH_TOKEN")

today = datetime.today().strftime('%Y-%m-%d %H:%M')
today_date = datetime.today().strftime('%Y-%m-%d')


def return_answer (response):
    dictionary = response.json()
    string = dictionary['result']['response']
    answer = string.split("\n\n")[1]
    return answer

def write_article (title, title_slug, story, image, today, today_date):
    file_name = f"content/{today_date}-{title_slug}.md"
    print(file_name)
    f = open(file_name, "a")
    f.write(f"Title: {title}\n")
    f.write(f"Date: {today}\n")
    f.write("\n")
    f.write("> This article is AI generated!\n")
    f.write("\n")
    f.write(f"![Alt Text](images/{image})\n")
    f.write("\n")
    f.write(story)
    f.close()

news_types: list[str] = [
    "technology",
    "biotech",
    "cyber security",
    "smart home",
    "IoT",
    "gaming"
]

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

title = return_answer(response) # TODO: wrap in try except to break the loop

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

article = return_answer(response)


prompt = f"{title}"
image_name = f"{today_date}-{title_slug}.png"
response = requests.post(
  f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/stabilityai/stable-diffusion-xl-base-1.0",
    headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
    json={"prompt": prompt}
)
with open(f"content/images/{image_name}", "wb") as f:
    f.write(response.content)


write_article(title, title_slug, article, image_name, today, today_date)

subprocess.run(['pelican', 'content'])
subprocess.run(['git', 'add', '.'])
subprocess.run(['git', 'commit', '-m', today])
subprocess.run(['git','push'])