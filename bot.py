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
from weather_data import get_weather_data, format_weather_data

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
    try:
        api_key = context.bot_data['api_key']
        amount = float(context.args[0])
        from_currency = context.args[1].upper()
        to_currency = context.args[2].upper()

        rates = get_currency_rates(api_key)  # Предполагается, что эта функция возвращает актуальные курсы валют
        converted_amount = convert_currency(amount, from_currency, to_currency, rates['rates'])

        await update.message.reply_text(f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")
    except (IndexError, ValueError):
        await update.message.reply_text("Используйте формат: /convert <сумма> <исходная_валюта> <целевая_валюта>")


async def check_rate_change(update: Update, context: CallbackContext, current_rate: float, threshold: float) -> None:
    if current_rate > threshold:
        await update.message.reply_text(f"Внимание! Курс превысил пороговое значение: {current_rate:.2f}")
    else:
        await update.message.reply_text(f"Курс ниже порогового значения: {current_rate:.2f}")


async def set_threshold(update: Update, context: CallbackContext) -> None:
    try:
        threshold = float(context.args[0])
        context.user_data['threshold'] = threshold
        await update.message.reply_text(f"Пороговое значение установлено: {threshold:.2f}")
    except (IndexError, ValueError):
        await update.message.reply_text("Пожалуйста, введите пороговое значение в формате: /set_threshold <значение>")


def check_currency_change(context: CallbackContext) -> None:
    api_key = context.bot_data['api_key']

    # Получение текущего курса валют
    current_rates = get_currency_rates(api_key)
    usd_to_rub = current_rates['rates']['RUB']
    print("check_currency_change вызвана")

    for chat_id in context.bot_data['subscribers']:
        context.bot.send_message(chat_id=chat_id, text=f"Курс USD/RUB: {usd_to_rub:.2f}")
    # Проверка изменения курса и отправка уведомления
    # if abs(usd_to_rub - context.bot_data['last_rate']) > context.bot_data['threshold']:
    #     for chat_id in context.bot_data['subscribers']:
    #         context.bot.send_message(chat_id=chat_id, text=f"Курс USD/RUB изменился: {usd_to_rub:.2f}")
    #         context.bot_data['last_rate'] = usd_to_rub


async def weather(update: Update, context: CallbackContext) -> None:
    try:
        city = context.args[0]
        api_weather_key = context.bot_data['api_weather_key']
        weather_data = get_weather_data(api_weather_key, city)
        formatted_data = format_weather_data(weather_data)
        await update.message.reply_text(formatted_data)
    except IndexError:
        await update.message.reply_text("Пожалуйста, укажите город в формате: /weather <город>")
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {e}")


def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("Переменная окружения BOT_TOKEN не установлена!")
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("Переменная окружения API_KEY не установлена!")
    api_weather_key = os.getenv("API_WEATHER_KEY")
    if not api_weather_key:
        raise ValueError("Переменная окружения API_WEATHER_KEY не установлена!")

    # Создаем экземпляр Application
    application = Application.builder().token(token).build()

    application.bot_data['api_key'] = api_key
    application.bot_data['api_weather_key'] = api_weather_key

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("convert", convert))
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(CommandHandler("set_threshold", set_threshold))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    job_queue = application.job_queue
    job_queue.run_repeating(check_currency_change, interval=100, first=0)

    # Запускаем бота
    application.run_polling()


if __name__ == '__main__':
    main()
