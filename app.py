import requests
import streamlit as st
import time

# ==========================================
# НАСТРОЙКИ БОТА
# ==========================================
BOT_TOKEN = "ВАШ_ТОКЕН_СЮДА"
BASE_URL = "https://platform-api2.max.ru"

# ==========================================
# ФУНКЦИЯ ОТПРАВКИ
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
            st.error(f"Ошибка отправки: {response.status_code}")
    except Exception as e:
        st.error(f"Ошибка сети: {e}")

# ==========================================
# ИНТЕРФЕЙС STREAMLIT
# ==========================================
st.set_page_config(page_title="Мой Макс Бот", layout="centered")
st.title("🤖 Мой Макс Бот")
st.info("🟢 Сервер запущен. Бот работает.")

# Блок обработки параметров от Макса
params = st.query_params
chat_id = params.get("chatId")
text = params.get("text")

if chat_id:
    if text:
        st.success(f"✅ Получено сообщение: {text}")
        send_message(chat_id, f"Привет! Ты написал: '{text}'")
        st.success("✅ Ответ отправлен!")
    elif "start" in params or not text:
        st.success("✅ Получена команда Старт")
        send_message(chat_id, "Привет! Я твой бот. Напиши мне что-нибудь.")
        st.success("✅ Ответ отправлен!")
else:
    st.write("Ожидание первого сообщения...")
