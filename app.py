import requests
import streamlit as st
import json

BOT_TOKEN = "f9LHodD0cOLNe5TAyASUtuyV1Dl4KEGrYkDpQyaZmTfbiZP3C7PmL46-VL8-Z7Gr808kj6ajFQWpTEoTvLzD"
SEND_URL = "https://platform-api2.max.ru/messages"

st.title("🤖 Мой Макс Бот")
st.info("🟢 Сервер запущен. Жду сообщений...")

params = st.query_params
chat_id = params.get("chatId")
text = params.get("text")

if chat_id:
    st.success(f"✅ Получено: {text}")
    
    # ⚠️ ВОТ ЗДЕСЬ ВАЖНОЕ ИЗМЕНЕНИЕ: ДОБАВИЛИ Bearer
    headers = {"Authorization": f"Bearer{BOT_TOKEN}", "Content-Type": "application/json"}
    
    data = {"chatId": chat_id, "text": f"Привет! Я получил: '{text}'"}
    
    try:
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
