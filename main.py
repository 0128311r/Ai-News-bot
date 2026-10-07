import os
import json
import urllib.request
import urllib.error

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
GROQ_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    clean_text = text[:4000] if len(text) > 4000 else text
    
    payload = json.dumps({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": clean_text,
        "disable_web_page_preview": True
    }).encode('utf-8')
    
    req = urllib.request.Request(
        url, 
        data=payload, 
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            print("Сообщение успешно отправлено в Telegram!")
    except Exception as e:
        print(f"Ошибка Telegram: {e}")

def main():
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {GROQ_API_KEY}'
    }

    data = json.dumps({
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": "Сделай краткую сводку из 3 главных новостей ИИ за сегодня на русском языке. Пиши простым текстом без звездочек и решеток."}
        ]
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            if "choices" in result and len(result["choices"]) > 0:
                text = result["choices"][0]["message"]["content"]
                send_telegram(text)
            else:
                send_telegram(f"Ответ от API: {result}")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        send_telegram(f"Ошибка Groq API ({e.code}): {error_body}")
    except Exception as e:
        send_telegram(f"Ошибка при обращении к API: {e}")

if __name__ == "__main__":
    main()
