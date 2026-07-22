import requests
import streamlit as st

BOT_TOKEN = "f9LHodD0cOJDvMkvHcYvQ_WXz46iuVcrUsoYaH7QLRQ799cTzdNwqAxxCj7qgX8D4a42anK0_SA86LkhmoAC"
# Поменяли URL: api2 заменили на api
SEND_URL = "https://api.max.ru/messages/sendText"

def send_message(chat_id, text):
    headers = {"Authorization": BOT_TOKEN, "Content-Type": "application/json"}
    data = {"chatId": chat_id, "text": text}
    try:
        response = requests.post(SEND_URL, headers=headers, json=data, timeout=5, verify=False)
        if response.status_code != 200:
            st.error(f"Ошибка отправки. Код: {response.status_code}")
    except Exception as e:
        st.error(f"Ошибка сети: {e}")

st.title("🤖 Мой Макс Бот")
st.info("Сервер запущен. Ожидаю сообщение...")

params = st.query_params
if "chatId" in params and "text" in params:
    chat_id = params["chatId"]
    text = params["text"]
    st.success(f"✅ Получено: {text}")
    send_message(chat_id, f"Привет! Я получил: '{text}'")
else:
    st.write("Ожидание первого сообщения...")
