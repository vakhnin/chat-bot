import os

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я ваш бот для мониторинга курсов валют.')

def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("Переменная окружения BOT_TOKEN не установлена!")
    # Create an Application instance
    application = Application.builder().token(token).build()

    # Add the command handler
    application.add_handler(CommandHandler("start", start))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
