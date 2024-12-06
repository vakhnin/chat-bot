import logging
import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters, CallbackContext
)

from currency_rates import get_currency_rates

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def convert_currency(amount: float, from_currency: str, to_currency: str, rates: dict) -> float:
    if from_currency == "USD":
        base_amount = amount
    else:
        base_amount = amount / rates[from_currency]

    if to_currency == "USD":
        return base_amount
    else:
        return base_amount * rates[to_currency]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info(f"Пользователь {update.effective_user.id} отправил команду /start")
    await update.message.reply_text('Привет! Я ваш бот для мониторинга курсов валют. Как я могу помочь?')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)


async def convert(update: Update, context: CallbackContext) -> None:
    print(111)
    try:
        api_key = os.getenv("API_KEY")
        if not api_key:
            raise ValueError("Переменная окружения API_KEY не установлена!")
        amount = float(context.args[0])
        from_currency = context.args[1].upper()
        to_currency = context.args[2].upper()

        rates = get_currency_rates(api_key)  # Предполагается, что эта функция возвращает актуальные курсы валют
        converted_amount = convert_currency(amount, from_currency, to_currency, rates['rates'])

        await update.message.reply_text(f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")
    except (IndexError, ValueError):
        await update.message.reply_text("Используйте формат: /convert <сумма> <исходная_валюта> <целевая_валюта>")


def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("Переменная окружения BOT_TOKEN не установлена!")

    # Создаем экземпляр Application
    application = Application.builder().token(token).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("convert", convert))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запускаем бота
    application.run_polling()


if __name__ == '__main__':
    main()
