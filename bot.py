import telebot
bot = telebot.TeleBot("6322819748:AAFNIuSrtSz9ZAlnTkl0DK4xRwKuKW5Y7Do")
bot.remove_webhook()
bot.set_webhook("https://d5d3041c13om056df5pq.apigw.yandexcloud.net")