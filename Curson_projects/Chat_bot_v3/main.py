from dotenv import load_dotenv
import os

# Загрузка переменных окружения из .env файла
load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))

# Остальной код остается без изменений
