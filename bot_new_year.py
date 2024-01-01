#imports 

import random
import re
from pymongo import MongoClient
from aiogram import Dispatcher, Bot, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import API_TOKEN

#api_token

token = API_TOKEN
bot = Bot(token)
dp = Dispatcher(bot, storage=MemoryStorage())

#database

cluster = MongoClient('mongodb+srv://matveidev:antipova1977@cluster0.sfhubs3.mongodb.net/')

db = cluster['DB_NY']
collection_wishes = db['collection_wishes']

#states

class ClientStates(StatesGroup):

	wish = State()

#check_in

check_in = {'🎅 Новорічне передбачення від ШІ', '🎄 Побажати щось', '👌 Так'}

#keyboards

keyboard_main=ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("🎅 Новорічне передбачення від ШІ")
            ],
			[
                KeyboardButton("🎄 Побажати щось")
            ],
			[
				KeyboardButton("📖 Подивитися на дошку побажань")
            ]
        ],

        resize_keyboard=True,
    )

#functions

def ai_list():
	list = ['Енергія нового року запропонує багато позитивних змін.',
        'Глобальні ініціативи для боротьби з кліматичними змінами отримають новий поштовх.',
        'Екологічно чисті технології стануть більш доступними для широкого загалу.',
        'Розвиток інновацій у галузі медицини зробить лікування більш ефективним.',
        'Велика кількість принципових відкриттів у галузі науки.',
        'Збільшення інтересу до космосу, нові місії та відкриття у космічному дослідженні.',
        'Розвиток синтетичної їжі та біоінженерії.',
        'Зменшення використання одноразових матеріалів та пакування.',
        'Пришвидшений розвиток електромобільності та альтернативних джерел енергії.',
        'Збільшення популярності сонячної енергії та вітроенергетики.',
        'Подальший розвиток віртуальної та розширеної реальності.',
        'Закінчення війни.',
        'Збільшення кількості технологій для роботи з віддаленими командами.',
        'Нові методи лікування та підтримки психічного здоров`я.',
        'Зростання популярності підприємництва серед молоді.',
        'Посилення уваги до важливості емоційного інтелекту.',
        'Збільшення кількості глобальних заходів для боротьби з нерівністю.',
        'Підвищення уваги до проблем гендерної рівності.',
        'Сприяння розвитку технологій для очищення води та повітря.',
        'Зростання популярності веганської та рослинної дієти.',
        'Розширення можливостей для гнучкої роботи та віддалених команд.',
        'Впровадження нових методів відновлення ґрунтів та лісів.',
        'Зростання інтересу до збереження біорізноманіття.',
        'Посилення кіберзахисту та кібербезпеки.',
        'Великі кроки у розвитку штучного інтелекту.',
        'Збільшення кількості ініціатив для заохочення чистого відновлюваного виробництва.',
        'Розвиток альтернативних методів очищення океанів від пластику.',
        'Збільшення інвестицій у відновлювані джерела енергії.',
        'Розвиток гідропоніки та вертикального землеробства.',
        'Посилення заходів для захисту прав тварин.',
        'Розвиток технологій для переробки та використання вторинних ресурсів.',
        'Зростання популярності масового спорту та здорового способу життя.',
        'Впровадження нових форм відновлення та переробки відходів.',
        'Розвиток технологій для збереження води та управління водними ресурсами.',
        'Збільшення уваги до проблеми голоду в світі та розвиток методів боротьби з нею.',
        'Вдосконалення технологій виробництва електроніки та її вторинного використання.',
        'Зростання інтересу до місцевого виробництва та споживання.',
        'Посилення ініціатив для вивчення та захисту океанів.',
        'Великі кроки у напрямку розвитку космічного туризму.',
        'Збільшення інвестицій у проекти відновлення лісів та створення',
        'Великі кроки у напрямку розвитку космічного туризму.']
	
	result = random.choice(list)
	return result

def user_insertation(user_id, wish):
	
    wishes_list = {
		'id': user_id,
		'prompt': wish
    }
    result_func = 'Ваше побажання записане !'
	
    collection_wishes.insert_one(wishes_list)
	
    return result_func

#start message

@dp.message_handler(commands=['start'])
async def start_buttons(message: types.Message):

    keyboard_main=ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("🎅 Новорічне передбачення від ШІ")
            ],
			[
                KeyboardButton("🎄 Побажати щось")
            ],
			[
				KeyboardButton("📖 Подивитися на дошку побажань")
            ]
        ],

        resize_keyboard=True,
    )

    await message.answer(

        f'Привет, *{message.from_user.first_name}*!\n\nВот список функий:',

        reply_markup=keyboard_main,

        parse_mode='Markdown',

    )

#handlers

@dp.message_handler(lambda message: message.text == '🎅 Новорічне передбачення від ШІ', state=None)
async def prediction(message: types.Message):

	await message.answer(f'Передбачення від ШІ на прийдешній рік для нашої країни : "{ai_list()}"')

@dp.message_handler(lambda message: message.text == '🎄 Побажати щось', state=None)
async def wish_keyboard(message: types.Message):
	
	keyboard_wish=ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("👌 Так")
            ],
			[
                KeyboardButton("🔙 На головну")
            ]
        ],

        resize_keyboard=True,
    )
	await message.answer('Ви хочете зробити своє побажання?', reply_markup=keyboard_wish)

@dp.message_handler(lambda message: message.text == '🔙 На головну', state=None)
async def back(message: types.Message):

    await message.reply('Виконано !', reply_markup=keyboard_main)

@dp.message_handler(lambda message: message.text == '👌 Так', state=None)
async def create_wish(message: types.Message):

	await ClientStates.wish.set()
	await message.answer('Введіть побажання :')
	
@dp.message_handler(state=ClientStates.wish)
async def load_wish(message: types.Message, state: FSMContext):
	async with state.proxy() as data:

		data['wish'] = message.text
		user_id = message.from_user.username
		users_records = collection_wishes.find_one({'id': user_id})
		user_text = message.text

		if user_text == '🔙 На головну':

			await message.reply('Виконано!', reply_markup=keyboard_main)
			await state.finish()
			
		elif user_text in check_in:

			await state.finish()
			await message.answer('Антиспам', reply_markup=keyboard_main)
		
		elif users_records == None:
			
			await message.reply(f"{user_insertation(user_id, data['wish'])}")
		else:
			
			await message.reply('Ви вже відправляли побажання або у вас не встановлений унікальний ID у налаштуваннях')
			await message.answer('Негайно встановіть унікальний ID у телеграм для коректної роботи із застосунком')
			await state.finish()

@dp.message_handler(lambda message: message.text == '📖 Подивитися на дошку побажань', state=None)
async def prediction(message: types.Message):
	
    array = collection_wishes.find({}, {'id': 1, 'prompt': 1})

    response = "Список побажань:\n"
    for user in array:
        response += f"\n@{user['id']} - {user['prompt']}\n"
        substring_to_remove = f"\n@{user['id']} - {user['prompt']}\n"
        if user['prompt'] == 'null':
            response = re.sub(substring_to_remove, "", response)
	

    if len(response) <= 4096:
        await message.reply(response)
    else:
        while response:
            chunk, response = response[:4096], response[4096:]
            await message.reply(chunk)

#bot pooling

if __name__ == '__main__':

	executor.start_polling(dp, skip_updates=True)