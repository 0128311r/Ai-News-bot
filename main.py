import os
import requests
import feedparser
from google import genai

# Получение токенов и ключей из настроек окружения
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# 1. Сбор новостей ИИ из RSS-лент
rss_urls = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://habr.com/ru/rss/hub/artificial_intelligence/all/?fl=ru"
]

news_items = []
for url in rss_urls:
    feed = feedparser.parse(url)
    for entry in feed.entries[:5]:  # Берём 5 свежих новостей
        news_items.append(f"- {entry.title}: {entry.link}")

raw_text = "\n".join(news_items)

# 2. Обработка и выжимка через Gemini API
client = genai.Client(api_key=GEMINI_API_KEY)
prompt = f"Сделай краткую структурированную выжимку главных новостей ИИ за сегодня на русском языке:\n\n{raw_text}"

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

summary = response.text

# 3. Отправка итогового отчёта в Telegram
telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": TELEGRAM_CHAT_ID,
    "text": f"🤖 **Ежедневный дайджест новостей ИИ**\n\n{summary}",
    "parse_mode": "Markdown"
}
requests.post(telegram_url, json=payload)
