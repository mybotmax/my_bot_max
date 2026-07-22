import requests
import streamlit as st

BOT_TOKEN = "f9LHodD0cOJDvMkvHcYvQ_WXz46iuVcrUsoYaH7QLRQ799cTzdNwqAxxCj7qgX8D4a42anK0_SA86LkhmoAC"

# ========================
# ВЫБЕРИТЕ ВАРИАНТ (1, 2 или 3):
VARIANT = 1
# ========================

# В зависимости от варианта выбираем URL и метод отправки
if VARIANT == 1:
    SEND_URL = "https://platform-api2.max.ru/messages/sendText" # Post JSON
elif VARIANT == 2:
    SEND_URL = "https://platform-api2.max.ru/sendText"          # Post JSON (без messages)
elif VARIANT == 3:
    SEND_URL = "https://platform-api2.max.ru/messages/sendText" # Get параметры

def send_message(chat_id, text):
    headers = {"Authorization": BOT_TOKEN}
    try:
        if VARIANT == 3:
            # Вариант 3: GET запрос (данные в ссылке)
            response = requests.get(f"{SEND_URL}?chatId={chat_id}&text={text}", headers=headers, timeout=5, verify=False)
        else:
            # Варианты 1 и 2: POST запрос (данные в JSON)
            headers["Content-Type"] = "application/json"
            data = {"chatId": chat_id, "text": text}
            response = requests.post(SEND_URL, headers=headers, json=data, timeout=5, verify=False)

        if response.status_code != 200:
            st.error(f"Ошибка отправки. Код: {response.status_code}")
        else:
            st.success("✅ Ответ отправлен!") # Это сообщение появится только при успехе
    except Exception as e:
        st.error(f"Ошибка сети при отправке: {e}")

st.title("🤖 Мой Макс Бот")
st.info("🟢 Сервер запущен. Бот работает.")

chat_id = st.query_params.get("chatId")
text = st.query_params.get("text")

if chat_id:
    st.success(f"✅ Получено сообщение: {text}")
    send_message(chat_id, f"Привет! Я получил: '{text}'")
else:
    st.write("Ожидание первого сообщения...")
