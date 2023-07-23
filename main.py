from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from speechkit import ShortAudioRecognition
from speechkit import Session, SpeechSynthesis
import pathlib as p

from dotenv import load_dotenv, find_dotenv
import os

env_path = find_dotenv()
if env_path == "":
    raise Exception("Окружение не найдено")
else:
    load_dotenv(env_path)
    print('Окружение найдено')
    API_TOKEN = os.getenv('API_TOKEN_TEST')
    oauth_token = os.getenv('oauth_token')
    catalog_id = os.getenv('catalog_id')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

#подключение speechkit
session = Session.from_yandex_passport_oauth_token(oauth_token, catalog_id)

#работа с голосовыми сообщениями
@dp.message_handler(content_types='voice')
async def voice_message_handler(message: types.Message):
    if message.content_type == types.ContentType.VOICE:
        file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_on_disk = p.Path("", f"{file_id}.mp3")
    await bot.download_file(file_path, destination=file_on_disk)
    with open(file_on_disk, 'rb') as f:
        data = f.read()
    os.remove(file_on_disk)
    recognizeShortAudio = ShortAudioRecognition(session)
    text = recognizeShortAudio.recognize(data)
    if text.lower() == "Посмотреть фотографии Элизы".lower():
        await message.answer("Чтобы посмотреть фотографии, проговори в голосовом сообщении одну из команд:\n- Молодая Элиза\n- Старая Элиза")
    elif text.lower() == "Послушать истории".lower():
        await message.answer("Чтобы послушать истории, проговори в голосовом сообщении одну из команд:\n- История любви\n- Об алгоритме обработки естественного языка\n- О базах данных")
    elif text.lower() == "Узнать об увлечениях".lower():
        await message.answer("Чтобы узнать об увлечениях, проговори в голосовом сообщении одну из команд:\n- Коротко об Элизе\n- Главное увлечение")
    elif text.lower() == "Молодая Элиза".lower():
        await message.answer_photo(photo=open("school.png", 'rb'), caption="В школе Элиза организовывала разные мероприятия и любила котиков. Иногда она надевала фиолетовые очки, чтобы ботать матан было не так грустно.")
    elif text.lower() == "Старая элиза".lower():
        await message.answer_photo(photo=open("old.png", 'rb'), caption="Элиза любит ходить в походы, фото в понамке приехало из пещерных городов Крыма. Еще она любит собирать квадрокоптеры и занимается чирлидингом - строит пирамиды из людей!")
    elif text.lower() == "История любви".lower():
        await message.answer_audio(audio=open("История первой любви.m4a", 'rb'))
    elif text.lower() == "Об алгоритме обработки естественного языка".lower():
        await message.answer_audio(audio=open("GPT и AI.m4a", 'rb'))
    elif text.lower() == "О базах данных".lower():
        await message.answer_audio(audio=open("Об SQL и NoSQL.m4a", 'rb'))
    elif text.lower() == "Немного об Элизе".lower():
        await message.answer(
            "Буду краток. Элиза data scientist, она вышла замуж за Python, но еще шикарно делает презентации и часто общается с Figma. Иногда она моделирует машинные двигатели в SolidWorks и делает квадрокоптеры, но иногда ей хочется стать русалкой.")
    elif text.lower() == "Главное увлечение".lower():
        await message.answer("Находить что-то новое. Вечер удался если квантовые вычисления ускорили перемножение матриц, приложение по колонизации Марса придумано и новая поза йоги выучена. По этой причине Элиза за свои 20 лет попробовала примерно *** (очень много). Она обучала роботов компьютерному зрению, чтобы те играли в футбол, сделала свой интернет-магазин арахисовой пасты в 9 классе, прошла 1000 и 1 курс по машинному обучению, чтобы убедиться, что под капотом не магия, а линал, поступила в МФТИ, занялась моделированием пончиков в Blender, нейробиологией и еще много-много чем. На сегодняшний день она работала на позициях проджект менеджера, тестировщика, Python-разработчика и сейчас - инженером данных. ")
    else:
        await message.answer("О-о..Прости:( О таком Элиза еще мне не рассказала. Если ты уверен, что такая команда все же есть, пожалуйста, произнеси еще раз как можно четче.")

#кнопки для выбора режима общения с ботом
howkb = InlineKeyboardMarkup(row_width=1)
howButton = InlineKeyboardButton(text='Буду использовать кнопки', callback_data='button1_how')
howButton2 = InlineKeyboardButton(text='Буду отправлять голосовые', callback_data='button2_how')
howkb.add(howButton, howButton2)


# создание кнопок для первичного выбора действий
urlkb = InlineKeyboardMarkup(row_width=1)
urlButton = InlineKeyboardButton(text='Посмотреть фотографии', callback_data='button1')
urlButton2 = InlineKeyboardButton(text='Послушать истории', callback_data='button2')
urlButton3 = InlineKeyboardButton(text='Узнать об увлечениях', callback_data='button3')
urlkb.add(urlButton, urlButton2, urlButton3)


# сообщение юзеру после запуска бота
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет, друг! Я Лесной Эльф, личный помощник Элизы. \nТы можешь использовать для общения со мной кнопки или голосовые сообщения. Как ты хочешь со мной общаться?",
                         reply_markup=howkb)

@dp.message_handler(commands=['gogit'])
async def start(message: types.Message):
    await message.answer("Лови ссылку на репозиторий бота: https://github.com/elfeliza/bot_test/tree/master")

@dp.callback_query_handler(lambda c: c.data == 'button1_how')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Ты выбрал кнопки для общения со мной. Жмякай, чтобы узнать об Элизе!",
                           reply_markup=urlkb)

@dp.callback_query_handler(lambda c: c.data == 'button2_how')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Ты выбрал голосовые сообщения для общения со мной. Пожалуйста, проговаривай команды четко, не съедай окончания:)\nЧтобы узнать об Элизе, проговори в голосовом сообщении одну из команд:\n- Посмотреть фотографии Элизы\n- Послушать истории\n- Узнать об увлечениях")


# кнопки для показа фотографий
photokb = InlineKeyboardMarkup(row_width=1)
photoButton1 = InlineKeyboardButton(text='Молодая Элиза', callback_data='button_photo_1')
photoButton2 = InlineKeyboardButton(text='Старая Элиза', callback_data='button_photo_2')
photokb.add(photoButton1, photoButton2)


# выбор фотографии
@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Готовь свои нервы. Какую фотографию тебе показать?",
                           reply_markup=photokb)


# показ школьного фото
@dp.callback_query_handler(lambda c: c.data == 'button_photo_1')
async def process_callback_button_photo_1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_photo(callback_query.from_user.id, photo=open("school.png", 'rb'),
                         caption="В школе Элиза организовывала разные мероприятия и любила котиков. Иногда она надевала фиолетовые очки, чтобы ботать матан было не так грустно.")


# показ фото старой Элизы
@dp.callback_query_handler(lambda c: c.data == 'button_photo_2')
async def process_callback_button_photo_2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_photo(callback_query.from_user.id, photo=open("old.png", 'rb'),
                         caption="Элиза любит ходить в походы, фото в понамке приехало из пещерных городов Крыма. Еще она любит собирать квадрокоптеры и занимается чирлидингом - строит пирамиды из людей!")


# кнопки для рассказа об увлечениях
storykb = InlineKeyboardMarkup(row_width=1)
storyButton1 = InlineKeyboardButton(text='Коротко об Элизе', callback_data='button_story_1')
storyButton2 = InlineKeyboardButton(text='Главное увлечение', callback_data='button_story_2')
storykb.add(storyButton1, storyButton2)


# выбор рассказа про увлечения
@dp.callback_query_handler(lambda c: c.data == 'button3')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Темные моменты биографии я опущу. О чем хочешь узнать?",
                           reply_markup=storykb)


# об Элизе
@dp.callback_query_handler(lambda c: c.data == 'button_story_1')
async def process_callback_button_story_1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           'Буду краток. Элиза data scientist, она вышла замуж за Python, но еще шикарно делает презентации и часто общается с Figma. Иногда она моделирует машинные двигатели в SolidWorks и делает квадрокоптеры, но иногда ей хочется стать русалкой.')

# о главном увлечении
@dp.callback_query_handler(lambda c: c.data == 'button_story_2')
async def process_callback_button_story_2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,"Находить что-то новое. Вечер удался если квантовые вычисления ускорили перемножение матриц, приложение по колонизации Марса придумано, новая поза йоги выучена, а ее брат тихонько грустит над интерпретируемостью Python. Именно по этой причине Элиза за свои 20 лет попробовала примерно *** (очень много). Она обучала роботов компьютерному зрению, чтобы те играли в футбол, сделала свой интернет-магазин арахисовой пасты в 9 классе, прошла 1000 и 1 курс по машинному обучению, чтобы убедиться, что под капотом не магия, а линал, поступила в МФТИ (тоже,видимо, убедиться в чем-то), занялась моделированием пончиков в Blender и нейробиологией и еще много-много всего. На сегодняшний день она работала на позиции Project Manager, тестировщик, Python-разработчик и сейчас Data Science.")

# кнопки для рассказа историй
voicekb = InlineKeyboardMarkup(row_width=1)
voiceButton1 = InlineKeyboardButton(text='Чем отличается SQL от NoSQL', callback_data='button_voice_1')
voiceButton2 = InlineKeyboardButton(text='Что такое GPT?', callback_data='button_voice_2')
voiceButton3 = InlineKeyboardButton(text="История первой любви", callback_data='button_voice_3')

voicekb.add(voiceButton1, voiceButton2, voiceButton3)


# выбор истории
@dp.callback_query_handler(lambda c: c.data == 'button2')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Приготовься, будет интересно. Что бы ты хотел послушать?",
                           reply_markup=voicekb)


# показ школьного фото
@dp.callback_query_handler(lambda c: c.data == 'button_voice_1')
async def process_callback_button_photo_1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_audio(callback_query.from_user.id, audio=open("Об SQL и NoSQL.m4a", 'rb'))

# показ школьного фото
@dp.callback_query_handler(lambda c: c.data == 'button_voice_2')
async def process_callback_button_photo_2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_audio(callback_query.from_user.id, audio=open("GPT и AI.m4a", 'rb'))

# показ школьного фото
@dp.callback_query_handler(lambda c: c.data == 'button_voice_3')
async def process_callback_button_photo_3(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_audio(callback_query.from_user.id, audio=open("История первой любви.m4a", 'rb'))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
