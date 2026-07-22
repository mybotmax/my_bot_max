import requests
import streamlit as st
import json

BOT_TOKEN = "f9LHodD0cOJDvMkvHcYvQ_WXz46iuVcrUsoYaH7QLRQ799cTzdNwqAxxCj7qgX8D4a42anK0_SA86LkhmoAC"

# ВАЖНО: Это правильный адрес из документации!
SEND_URL = "https://platform-api2.max.ru/messages"

st.title("🤖 Мой Макс Бот")
st.info("🟢 Сервер запущен. Жду сообщений...")

params = st.query_params
chat_id = params.get("chatId")
text = params.get("text")

if chat_id:
    st.success(f"✅ Получено: {text}")
    
    headers = {"Authorization": BOT_TOKEN, "Content-Type": "application/json"}
    data = {"chatId": chat_id, "text": f"Привет! Я получил: '{text}'"}
    
    try:
        # Отправляем запрос на правильный адрес
        json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        response = requests.post(SEND_URL, headers=headers, data=json_data, timeout=5, verify=False)
        
        if response.status_code == 200:
            st.success("✅ Ответ успешно отправлен в MAX!")
        else:
            st.error(f"⚠️ Ошибка отправки. Код: {response.status_code}")
            st.code(response.text)
            
    except Exception as e:
        st.error(f"Ошибка подключения: {e}")
else:
    st.write("Ожидание первого сообщения...")
