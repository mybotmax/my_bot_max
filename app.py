import requests
import streamlit as st

BOT_TOKEN = "ВАШ_ТОКЕН_СЮДА"
# Для теста используем этот адрес. Если он неверный - мы увидим это в ответе сервера
TEST_URL = "https://api.max.ru/messages/sendText"

st.title("🔍 Диагностика Макса")

params = st.query_params
chat_id = params.get("chatId")
text = params.get("text")

if chat_id:
    st.write(f"✅ Получено сообщение: {text}")
    
    headers = {"Authorization": BOT_TOKEN, "Content-Type": "application/json"}
    data = {"chatId": chat_id, "text": f"Ответ: '{text}'"}
    
    try:
        # Стучимся в Макс
        response = requests.post(TEST_URL, headers=headers, json=data, timeout=5, verify=False)
        
        # ВАЖНО: Выводим полный ответ сервера!
        st.error(f"Код ответа: {response.status_code}")
        
        # Это и есть та самая строчка с кодом, которую просил тот ИИ!
        st.code(response.text)
        
        if response.status_code == 200:
            st.success("Этот адрес работает!")
        else:
            st.warning("Смотрим на текст ошибки выше. Он подскажет правильный адрес.")

    except Exception as e:
        st.error(f"Ошибка подключения: {e}")
else:
    st.info("Допишите в конец ссылки браузера: `/?chatId=123&text=Привет` и нажмите Enter, чтобы запустить диагностику.")
