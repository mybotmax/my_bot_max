import requests
import streamlit as st

BOT_TOKEN = "f9LHodD0cOJDvMkvHcYvQ_WXz46iuVcrUsoYaH7QLRQ799cTzdNwqAxxCj7qgX8D4a42anK0_SA86LkhmoAC"
BASE_URL = "https://platform-api2.max.ru"

def send_message(chat_id, text):
    url = f"{BASE_URL}/messages/sendText"
    headers = {"Authorization": BOT_TOKEN, "Content-Type": "application/json"}
    data = {"chatId": chat_id, "text": text}
    try:
        # ЗДЕСЬ МЫ ДОБАВИЛИ verify=False, чтобы победить SSL-ошибку
        response = requests.post(url, headers=headers, json=data, timeout=5, verify=False)
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
