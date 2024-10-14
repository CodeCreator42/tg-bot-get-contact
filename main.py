import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import TOKEN, ADMIN_ID
from database import Database

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация базы данных
db = Database('users.db')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    keyboard = [[KeyboardButton(text="Поделиться контактами", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        f"Привет, {user.first_name}! Пожалуйста, поделитесь контактами. Это нужно для организации личного VPN доступа для вас.",
        reply_markup=reply_markup
    )

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    contact = update.message.contact
    
    logger.info(f"Получены контактные данные от пользователя {user.id}")
    
    # Сохранение данных пользователя в базе данных
    db.add_user(user.id, user.username, user.first_name, user.last_name, contact.phone_number)
    
    # Отправка информации администратору
    admin_message = (f"Новая заявка:\n"
                     f"ID: {user.id}\n"
                     f"Username: {user.username}\n"
                     f"Имя: {user.first_name} {user.last_name}\n"
                     f"Телефон: {contact.phone_number}")
    await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message)
    
    logger.info(f"Сообщение администратору отправлено: {admin_message}")
    
    # Отправка сообщения пользователю с выбором периода VPN
    keyboard = [
        [KeyboardButton(text="На месяц")],
        [KeyboardButton(text="На полгода")],
        [KeyboardButton(text="На год")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "Спасибо! На какой период времени вам нужен VPN?",
        reply_markup=reply_markup
    )

async def handle_vpn_period(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    period = update.message.text
    
    # Обновление информации о пользователе в базе данных
    db.add_user(user.id, user.username, user.first_name, user.last_name, None, period)
    
    # Отправка информации администратору
    admin_message = (f"Новая заявка от пользователя:\n"
                     f"ID: {user.id}\n"
                     f"Username: {user.username}\n"
                     f"Период использования: {period}")
    await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message)
    
    await update.message.reply_text("Ваша заявка отправлена администратору.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    message = update.message.text
    
    if user.id == ADMIN_ID:
        # Обработка сообщений от администратора
        try:
            user_id, text = message.split(' ', 1)
            user_id = int(user_id)
            await context.bot.send_message(chat_id=user_id, text=text)
        except ValueError:
            await update.message.reply_text("Неправильный формат. Используйте: ID_пользователя сообщение")
    else:
        # Пересылка сообщений пользователя администратору
        admin_message = f"От пользователя:\nID: {user.id}\nUsername: {user.username}\nСообщение: {message}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message)
        await update.message.reply_text("Ваше сообщение отправлено администратору.")

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    application.add_handler(MessageHandler(filters.Regex("^(На месяц|На полгода|На год)$"), handle_vpn_period))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
