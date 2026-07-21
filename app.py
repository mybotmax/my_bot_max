import requests
import json
import os
from flask import Flask, request, jsonify

# ВСТАВЬТЕ СВОЙ ТОКЕН СЮДА
BOT_TOKEN = "ВАШ_ТОКЕН_СЮДА"
BASE_URL = "https://platform-api2.max.ru"

app = Flask(__name__)

# Функция отправки сообщения
def send_message(chat_id, text):
    url = f"{BASE_URL}/messages/sendText"
    headers = {
        "Authorization": BOT_TOKEN,
        "Content-Type": "application/json"
    }
    data = {
        "chatId": chat_id,
        "text": text
    }
    try:
        requests.post(url, headers=headers, json=data, timeout=5)
    except:
        pass

# Это место, куда MAX будет стучаться
@app.route('/', methods=['POST'])
def webhook():
    try:
        # Получаем данные от MAX
        data = request.json
        print(f"📩 Получено: {data}")
        
        # Ищем chatId и текст
        chat_id = data.get("chatId")
        text = data.get("text")
        
        if chat_id and text:
            send_message(chat_id, f"Привет! Я получил: '{text}'")
            print(f"✅ Ответ отправлен на {text}")
            
        # Обязательно отвечаем серверу MAX статусом 200
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print(f"Ошибка: {e}")
        return jsonify({"status": "error"}), 500

# Запускаем приложение (Streamlit это поддерживает)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
