import requests
import time
import sys
import io
import urllib3
import threading

# Отключаем SSL-предупреждения
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Настройка кодировки для логов
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ==========================================
# НАСТРОЙКИ БОТА
# ==========================================
BOT_TOKEN = "f9LHodD0cOJElwJ-QgWwz2vzlo55Lloe6efbhBRlN6wb7R02rGbP0EfAmNWqmVq6q-ljq2_Et3O4NSQG6UZX",

BASE_URL = "https://platform-api2.max.ru"
last_update_id = 0

# ==========================================
# ФУНКЦИЯ ОТПРАВКИ
# ==========================================
def send_message(chat_id, text):
    url = f"{BASE_URL}/messages/sendText"
    headers = {
        "Authorization": BOT_TOKEN,
        "Content-Type": "application/json; charset=utf-8"
    }
    data = {
        "chatId": chat_id,
        "text": text
    }
    try:
        response = requests.post(url, headers=headers, json=data, verify=False, timeout=4)
        if response.status_code != 200:
            print(f"❌ Ошибка отправки. Код: {response.status_code}")
    except:
        pass

# ==========================================
# ФУНКЦИЯ ПОЛУЧЕНИЯ
# ==========================================
def get_updates():
    global last_update_id
    url = f"{BASE_URL}/updates"
    headers = {
        "Authorization": BOT_TOKEN
    }
    params = {
        "marker": last_update_id
    }
    try:
        response = requests.get(url, headers=headers, params=params, verify=False, timeout=4)
        
        if response.status_code == 429:
            return []
        if response.status_code == 401:
            return []
        if response.status_code != 200:
            return []

        data = response.json()
        return data.get("updates", [])
    except:
        return []

# ==========================================
# ЗАПУСК БОТА В ФОНОВОМ РЕЖИМЕ (Thread)
# ==========================================
def run_bot():
    print("🤖 Макс Бот запущен в облаке и ждет сообщений...")
    while True:
        updates = get_updates()
        if updates:
            for update in updates:
                last_update_id = update.get("marker", last_update_id)
                chat_id = update.get("chatId")
                text = update.get("text")
                if chat_id and text:
                    print(f"✅ Получено: {text}")
                    send_message(chat_id, f"Привет! Я получил: '{text}'")
                    break 
        time.sleep(2)

# Запускаем бота в отдельном потоке (это спасет от ошибки Streamlit)
thread = threading.Thread(target=run_bot)
thread.daemon = True
thread.start()

# Держим приложение открытым (это нужно для Streamlit)
import streamlit as st
st.title("🤖 Мой Макс Бот")
st.write("Бот работает в фоновом режиме. Откройте приложение MAX и напишите ему!")

