from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lectures_13.api_tg_bot import api_bot

api = api_bot
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard = True)
button1 = KeyboardButton(text = "Информация")
button2 = KeyboardButton(text = "Упрощенный вариант")
button3 = KeyboardButton(text = "Доработанный вариант")
kb.add(button1)
kb.row(button2, button3)

class UserState(StatesGroup, option = None):
    age = State()
    growth = State()
    weight = State()
    gender = State()
    option = State()

@dp.message_handler(commands = ["start"])
async def start(message):
    await message.answer("Приветствую", reply_markup = kb)

@dp.message_handler(text = "Информация")
async def inform(message):
    await message.answer("Информация о боте:\n"
                         "Вычисление суточного потребления каллорий по формуле Миффлина-Сан Жеора\n"
                         "Упрощенный вариант и\n"
                         "Доработанный вариант:\n"
                         "учитывает степень физической активности человека")

@dp.message_handler(text = "Доработанный вариант")
async def set_option(message):
    await message.answer("Оцените вашу активность (введите соответствующее значение):\n"
                         "Минимальная активность - 1.2\n"
                         "Слабая активность - 1,375\n"
                         "Средняя активность - 1.55\n"
                         "Высокая активность - 1,725\n"
                         "Экстра-активность - 1,9")
    await UserState.option.set()

@dp.message_handler(state = UserState.option)
@dp.message_handler(text = "Упрощенный вариант")
async def set_age(message, state):
    await state.update_data(option = message.text)
    await message.answer("Введите свой возраст:", )
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer("Введите свой рост (в см.):")
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer("Введите свой вес (в кг.):")
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def set_gender(message, state):
    await state.update_data(weight = message.text)
    await message.answer("Введите свой пол (М , Ж):")
    await UserState.gender.set()

@dp.message_handler(state = UserState.gender)
async def send_calories(message, state):
    await state.update_data(gender = message.text)
    data = await state.get_data()
    print(data)
    try:
        if data['gender'] == 'М':
            calor = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5
        elif data['gender'] == 'Ж':
            calor = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) - 161
    except (ValueError, UnboundLocalError):
        await message.answer("Введены не корректные данные")
    try:
        if data["option"] == "Упрощенный вариант":
            await message.answer(f'Ваша норма калорий в сутки: {calor}')
        else:
            await message.answer(f'Ваша норма калорий в сутки: {calor * float(data["option"])}')
    except (ValueError, UnboundLocalError):
        await message.answer("Введены не корректные данные")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

"""
 1. Упрощенный вариант формулы Миффлина-Сан Жеора:

для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;
для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.
2. Доработанный вариант формулы Миффлина-Сан Жеора, в отличие от упрощенного дает более точную информацию
    и учитывает степень физической активности человека:

для мужчин: (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) + 5) x A;
для женщин: (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) – 161) x A.

A – это уровень активности человека, его различают обычно по пяти степеням физических нагрузок в сутки:

Минимальная активность: A = 1,2.
Слабая активность: A = 1,375.
Средняя активность: A = 1,55.
Высокая активность: A = 1,725.
Экстра-активность: A = 1,9 (под эту категорию обычно подпадают люди, занимающиеся, например, тяжелой атлетикой,
или другими силовыми видами спорта с ежедневными тренировками, а также те, кто выполняет тяжелую физическую работу).
"""