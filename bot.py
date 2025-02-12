import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Хранение данных пользователей
user_data = {}

# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Профиль", callback_data='profile')],
        [InlineKeyboardButton("Создать игру", callback_data='create_game')],
        [InlineKeyboardButton("Найти игру", callback_data='find_game')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Добро пожаловать! Выберите действие:', reply_markup=reply_markup)

# Обработка нажатий на кнопки
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'profile':
        balance = user_data.get(query.from_user.id, {}).get('balance', 0)
        keyboard = [
            [InlineKeyboardButton("Пополнить баланс", callback_data='top_up')],
            [InlineKeyboardButton("Вывести баланс", callback_data='withdraw')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text=f"Ваш баланс: {balance} Bytecoin", reply_markup=reply_markup)

    elif query.data == 'create_game':
        query.edit_message_text(text="Напишите ставку:")
        return 'WAITING_FOR_BET'  # Состояние ожидания ставки

    elif query.data == 'find_game':
        # Здесь можно добавить логику для поиска игр
        query.edit_message_text(text="Поиск игр... (функция не реализована)")

# Обработка текста (ставка)
def handle_message(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('state') == 'WAITING_FOR_BET':
        bet = update.message.text
        try:
            bet = int(bet)
            if bet <= 0:
                raise ValueError("Ставка должна быть положительным числом.")
            user_data[update.message.from_user.id] = user_data.get(update.message.from_user.id, {})
            user_data[update.message.from_user.id]['bet'] = bet
            context.user_data['state'] = 'WAITING_FOR_CHOICE'
            update.message.reply_text("Ставка создана! Выберите: камень, ножницы или бумага.")
        except ValueError as e:
            update.message.reply_text(f"Ошибка: {e}. Пожалуйста, введите корректную ставку.")

    elif context.user_data.get('state') == 'WAITING_FOR_CHOICE':
        choice = update.message.text.lower()
        if choice in ['камень', 'ножницы', 'бумага']:
            # Логика игры здесь (например, против бота или другого игрока)
            update.message.reply_text(f"Вы выбрали: {choice}. Ожидайте соперника...")
            # Здесь можно добавить логику для ожидания другого игрока
            context.user_data['state'] = None  # Сброс состояния
        else:
            update.message.reply_text("Пожалуйста, выберите: камень, ножницы или бумага.")

def main() -> None:
    updater = Updater("7022821881:AAFdYnfKGPcAgTNgoUOXpDlSxLxJwUogxgY")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
