import requests
import streamlit as st
import urllib3

# Отключаем SSL-предупреждения
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==========================================
# НАСТРОЙКИ БОТА
# ==========================================
BOT_TOKEN = "f9LHodD0cOKLhxOlQDEgM5JmnKyKGs0915KLSUKglWdLvWbX3X2Nab4KyEqSPA5YOrIz6SSy21_xEEs9JicY"
# ЗАМЕНИЛИ api2 НА api
SEND_URL = "https://api.max.ru/messages/sendText"

# ==========================================
# ФУНКЦИЯ ОТПРАВКИ
# ==========================================
def send_message(chat_id, text):
    headers = {"Authorization": BOT_TOKEN, "Content-Type": "application/json"}
    data = {"chatId": chat_id, "text": text}
    try:
        # Отправляем запрос на НОВЫЙ URL
        response = requests.post(SEND_URL, headers=headers, json=data, timeout=5, verify=False)
        if response.status_code != 200:
            st.error(f"Ошибка отправки. Код: {response.status_code}")
    except Exception as e:
        st.error(f"Ошибка сети при отправке: {e}")

# ==========================================
# ИНТЕРФЕЙС STREAMLIT
# ==========================================
st.set_page_config(page_title="Мой Макс Бот", layout="centered")
st.title("🤖 Мой Макс Бот")
st.info("🟢 Сервер запущен. Бот работает.")

chat_id = st.query_params.get("chatId")
text = st.query_params.get("text")

if chat_id:
    if text:
        st.success(f"✅ Получено сообщение: {text}")
        send_message(chat_id, f"Привет! Я получил: '{text}'")
        st.success("✅ Ответ отправлен!")
    else:
        st.success("✅ Получен запрос без текста")
        send_message(chat_id, "Привет! Напиши мне что-нибудь!")
        st.success("✅ Ответ отправлен!")
else:
    st.write("Ожидание первого сообщения...")
