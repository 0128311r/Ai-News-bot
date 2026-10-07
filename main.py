import os
import requests

TAVILY_API_KEY = os.environ["TAVILY_API_KEY"]
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

query = """
Find the most important AI news from the last 24 hours.
Focus on OpenAI, Google, Anthropic, Meta, xAI, NVIDIA, regulation, new AI models, AI products, chips, and major AI launches.
Return concise results with source links.
"""

response = requests.post(
    "https://api.tavily.com/search",
    json={
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "advanced",
        "max_results": 8,
        "include_answer": True,
        "include_raw_content": False,
    },
    timeout=30,
)

response.raise_for_status()
data = response.json()

message = "AI-дайджест за сегодня\n\n"

if data.get("answer"):
    message += data["answer"].strip() + "\n\n"

results = data.get("results", [])

if not results:
    message += "Сегодня не удалось найти свежие новости по AI."

for index, item in enumerate(results, start=1):
    title = item.get("title", "Без заголовка")
    url = item.get("url", "")
    content = item.get("content", "")

    message += f"{index}. {title}\n"

    if content:
        message += f"{content[:300].strip()}...\n"

    if url:
        message += f"{url}\n"

    message += "\n"

telegram_response = requests.post(
    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
    data={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message[:4000],
        "disable_web_page_preview": True,
    },
    timeout=30,
)

telegram_response.raise_for_status()

print("Digest sent to Telegram")
