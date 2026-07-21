import requests
import streamlit as st

BOT_TOKEN = "ВАШ_ТОКЕН_СЮДА"
# ВАЖНО: Адрес для отправки сообщений (эндпоинт) изменился
SEND_URL = "https://platform-api2.max.ru/messages/sendText"

def send_message(chat_id, text):
    headers = {"Authorization": BOT_TOKEN, "Content-Type": "application/json"}
    data = {"chatId": chat_id, "text": text}
    try:
        # Отправляем запрос прямо на SEND_URL
        response = requests.post(SEND_URL, headers=headers, json=data, timeout=5, verify=False)
        if response.status_code != 200:
            st.error(f"Ошибка отправки. Код: {response.status_code}")
    except Exception as e:
        st.error(f"Ошибка сети при отправке: {e}")

st.title("🤖 Мой Макс Бот")
st.info("🟢 Сервер запущен. Бот работает.")

chat_id = st.query_params.get("chatId")
text = st.query_params.get("text")

if chat_id:
    st.success(f"✅ Получено сообщение: {text}")
    send_message(chat_id, f"Привет! Я получил: '{text}'")
    st.success("✅ Ответ отправлен!")
else:
    st.write("Ожидание первого сообщения...")
