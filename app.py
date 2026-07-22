import requests
import streamlit as st
import json

BOT_TOKEN = "f9LHodD0cOJDvMkvHcYvQ_WXz46iuVcrUsoYaH7QLRQ799cTzdNwqAxxCj7qgX8D4a42anK0_SA86LkhmoAC"
TEST_URL = "https://api.max.ru/msg/sendText"

st.title("🔍 Диагностика Макса (исправленная)")

params = st.query_params
chat_id = params.get("chatId")
text = params.get("text")

if chat_id:
    st.success(f"✅ Получено сообщение: {text}")
    
    headers = {"Authorization": BOT_TOKEN, "Content-Type": "application/json"}
    data = {"chatId": chat_id, "text": f"Ответ: '{text}'"}
    
    try:
        # ВАЖНО: ensure_ascii=False спасает от ошибки 'latin-1'
        json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        
        response = requests.post(TEST_URL, headers=headers, data=json_data, timeout=5, verify=False)
        
        st.error(f"Код ответа: {response.status_code}")
        st.code(response.text)
        
        if response.status_code == 200:
            st.success("🎉 Ура! Адрес работает, а кириллица прошла!")
        else:
            st.warning("Смотрим на текст ошибки выше.")

    except Exception as e:
        st.error(f"Ошибка подключения: {e}")
else:
    st.info("Допишите в конец ссылки: `/?chatId=123&text=Привет` и нажмите Enter.")
