import requests
import time
import sys
import io
import urllib3

# Блок для исправления ошибки кодировки 'latin-1'
try:
    import http.client
    http.client._MAXHEADERS = 1000
except:
    pass

# Отключаем SSL-предупреждения
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Настройка кодировки для консоли
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ==========================================
# НАСТРОЙКИ БОТА
# ==========================================
BOT_TOKEN = "f9LHodD0cOJDvMkvHcYvQ_WXz46iuVcrUsoYaH7QLRQ799cTzdNwqAxxCj7qgX8D4a42anK0_SA86LkhmoAC"  # Вставьте свой токен

BASE_URL = "https://platform-api2.max.ru"
last_update_id = 0

# ==========================================
# ФУНКЦИЯ ОТПРАВКИ
# ==========================================
def send_message(chat_id, text):
    url = f"{BASE_URL}/messages/sendText"
    headers = {
        "Authorization": BOT_TOKEN,
        "Content-Type": "application/json; charset=utf-8"
    }
    data = {
        "chatId": chat_id,
        "text": text
    }
    try:
        # ВАЖНО: timeout=4 - если сервер не отвечает 4 секунды, бот не зависнет
        response = requests.post(url, headers=headers, json=data, verify=False, timeout=4)
        if response.status_code != 200:
            print(f"❌ Ошибка отправки. Код: {response.status_code}")
    except Exception as e:
        pass # Молча пропускаем ошибки отправки, чтобы не спамить консоль

# ==========================================
# ФУНКЦИЯ ПОЛУЧЕНИЯ
# ==========================================
def get_updates():
    global last_update_id
    url = f"{BASE_URL}/updates"
    headers = {
        "Authorization": BOT_TOKEN
    }
    params = {
        "marker": last_update_id
    }
    try:
        print("📡 Проверяю...", end="\r")
        
        # ВАЖНО: timeout=4 - если сервер молчит 4 секунды, бот продолжит работу
        response = requests.get(url, headers=headers, params=params, verify=False, timeout=4)
        
        print(" " * 20, end="\r") # Очищаем строку проверки
        
        if response.status_code == 429:
            return []
        if response.status_code == 401:
            print("⛔ ОШИБКА 401: Неверный токен!")
            return []
        if response.status_code != 200:
            print(f"⚠️ Ошибка {response.status_code}")
            return []

        data = response.json()
        return data.get("updates", [])
        
    except requests.exceptions.Timeout:
        # Если прошло 4 секунды, а ответа нет - просто выходим и ждем дальше
        print(" " * 20, end="\r") 
        return []
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return []

# ==========================================
# ЗАПУСК
# ==========================================
print("🤖 Макс Бот запущен и ждет сообщений...")

while True:
    updates = get_updates()
    
    if updates:
        for update in updates:
            last_update_id = update.get("marker", last_update_id)
            chat_id = update.get("chatId")
            text = update.get("text")
            
            if chat_id and text:
                print(f"✅ {text}")
                send_message(chat_id, f"Привет! Я получил: '{text}'")
                break 
                
    time.sleep(2)