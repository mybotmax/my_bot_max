# bot.py - ОБЫЧНЫЙ PYTHON (НЕ STREAMLIT)
import requests
import json
import time

BOT_TOKEN = "f9LHodD0cOLNe5TAyASUtuyV1Dl4KEGrYkDpQyaZmTfbiZP3C7PmL46-VL8-Z7Gr808kj6ajFQWpTEoTvLzD"
BASE_URL = "https://platform-api2.max.ru"
last_update_id = 0

def send_message(chat_id, text):
    url = f"{BASE_URL}/messages"
    headers = {"Authorization": BOT_TOKEN, "Content-Type": "application/json"}
    data = {"chatId": chat_id, "text": text}
    try:
        json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        response = requests.post(url, headers=headers, data=json_data, timeout=5, verify=False)
        return response.status_code == 200
    except:
        return False

def get_updates():
    global last_update_id
    url = f"{BASE_URL}/updates"
    headers = {"Authorization": BOT_TOKEN}
    params = {"marker": last_update_id}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5, verify=False)
        if response.status_code == 200:
            data = response.json()
            updates = data.get("updates", [])
            if updates:
                last_update_id = updates[-1].get("marker", last_update_id)
            return updates
    except:
        pass
    return []

print("🟢 Бот запущен в режиме Long Polling. Жду сообщений...")

while True:
    updates = get_updates()
    if updates:
        for update in updates:
            chat_id = update.get("chatId")
            text = update.get("text")
            if chat_id and text:
                print(f"✅ Получено: {text}")
                if send_message(chat_id, f"Привет! Я получил: '{text}'"):
                    print("✅ Ответ отправлен!")
                else:
                    print("❌ Ошибка отправки ответа.")
    time.sleep(2)
