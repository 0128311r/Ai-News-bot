import os
import json
import urllib.request

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": text}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req)
        print("Сообщение успешно отправлено в Telegram!")
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")

def main():
    if GEMINI_API_KEY.startswith("AIzaSy"):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        headers = {'Content-Type': 'application/json'}
    else:
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {GEMINI_API_KEY}'
        }

    data = json.dumps({
        "contents": [{"parts": [{"text": "Сделай краткую сводку из 3 главных новостей ИИ за сегодня на русском языке."}]}]
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            if "candidates" in result:
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                send_telegram(text)
            else:
                send_telegram(f"Ответ от Gemini: {result}")
    except Exception as e:
        send_telegram(f"Ошибка при обращении к Gemini API: {e}")

if __name__ == "__main__":
    main()
