import logging
import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info(f"Пользователь {update.effective_user.id} отправил команду /start")
    await update.message.reply_text('Привет! Я ваш бот для мониторинга курсов валют. Как я могу помочь?')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)


def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("Переменная окружения BOT_TOKEN не установлена!")

    # Создаем экземпляр Application
    application = Application.builder().token(token).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запускаем бота
    application.run_polling()


if __name__ == '__main__':
    main()
