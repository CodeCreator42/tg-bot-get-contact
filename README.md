   # Telegram Chat Bot

   Этот проект представляет собой чат-бота для Telegram, написанного на Python с использованием библиотеки `python-telegram-bot` и базы данных SQLite.

   ## Функционал

   - Сбор данных пользователя при нажатии кнопки "Старт".
   - Отправка данных администратору.
   - Возможность отправки сообщений пользователю от имени бота.
   - Пересылка сообщений от пользователя администратору.

   ## Установка

   1. Клонируйте репозиторий:
      ```bash
      git clone https://github.com/CodeCreator42/tg-bot-get-contact.git
      cd telegram-chat-bot
      ```

   2. Установите зависимости:
      ```bash
      pip install -r requirements.txt
      ```

   3. Настройте файл `config.py`:
      - Вставьте ваш токен бота и ID администратора.

   ## Запуск
BASH
python3 main.py
