import requests
import json
import streamlit as st
import time

# ==========================================
# НАСТРОЙКИ БОТА
# ==========================================
# ВСТАВЬТЕ СВОЙ ТОКЕН СЮДА (в кавычках)
BOT_TOKEN = "ВАШ_ТОКЕН_СЮДА"
BASE_URL = "https://platform-api2.max.ru"

# ==========================================
# ФУНКЦИЯ ОТПРАВКИ СООБЩЕНИЯ
# ==========================================
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
        response = requests.post(url, headers=headers, json=data, timeout=5)
        if response.status_code != 200:
            print(f"❌ Ошибка отправки: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка соединения: {e}")

# ==========================================
# ЗАПУСК ИНТЕРФЕЙСА STREAMLIT
# ==========================================
st.set_page_config(page_title="Мой Макс Бот", layout="centered")
st.title("🤖 Мой Макс Бот")
st.write("✅ Бот успешно запущен и готов принимать сообщения!")

# Этот блок нужен, чтобы Streamlit не "засыпал"
# Он создает пустое место для логов
log_area = st.empty()

# Функция, которая будет слушать Макс через Webhook (если он настроен)
# В Streamlit мы используем специальный обработчик запросов
if st.query_params:
    try:
        # Получаем данные от Макса
        data = st.query_params.to_dict()
        print(f"📩 Получено: {data}")
        
        chat_id = data.get("chatId")
        text = data.get("text")
        
        if chat_id and text:
            send_message(chat_id, f"Привет! Я получил: '{text}'")
            log_area.success(f"✅ Ответ отправлен на: {text}")
    except Exception as e:
        log_area.error(f"❌ Ошибка обработки: {e}")

# Держим приложение активным
st.info("🟢 Сервер работает. Отправьте сообщение боту в MAX.")
