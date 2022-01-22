import os

from dotenv import load_dotenv

load_dotenv()

# Заберем токен нашего бота (прописать в файле ".env")
BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

# Заберем данные для подключения к базе данных (юзер, пароль, название бд) - тоже прописать в файле ".env"
PGUSER = str(os.getenv("PGUSER"))
PGPASSWORD = str(os.getenv("PGPASSWORD"))
DATABASE = str(os.getenv("DATABASE"))

admins = [
    os.getenv("ADMIN_ID"),
]

# Ссылка подключения к базе данных
DATABASE_URL = os.getenv("DATABASE_URL")
aiogram_redis = {
    'host': DATABASE_URL,
}

redis = {
    'address': (DATABASE_URL, 6379),
    'encoding': 'utf8'
}
