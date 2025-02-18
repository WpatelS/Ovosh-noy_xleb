from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram import Router, F, types
from aiogram.enums import ChatAction
import asyncio
from app.keyboards import main_kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class Reg(StatesGroup):
    name = State()
    agr = State()
    pw = State()
    num = State()

class Log_in(StatesGroup):
    name = State()
    pw = State()

data = dict()

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer('Здравствуйте, напишите желаемое имя пользователя')

@user_router.message(Reg.name)
async def cmd_name_registration(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.agr)
    await message.answer('Желаете ли вы зарегистрироваться?', reply_markup=main_kb)

@user_router.message(Reg.agr)
async def cmd_agreement(message: Message, state: FSMContext):
    if message.text == 'Да':
        await state.set_state(Reg.pw)
        await message.answer('Напишите желаемый пароль', reply_markup=types.ReplyKeyboardRemove())
    elif message.text == 'Нет':
        await state.clear()
        await message.answer('АХАХХАХАХАХХАХАХАА', reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer('А?')

@user_router.message(Reg.pw)
async def cmd_password_registration(message: Message, state: FSMContext):
    await state.update_data(pw=message.text)
    await state.set_state(Reg.num)
    await message.answer('Введите свой номер телефона')

@user_router.message(Reg.num)
async def cmd_phone_number_registration(message: Message, state: FSMContext):
    await state.update_data(num=message.text)
    global data
    print(data)
    data = await state.get_data()
    print(data)
    await state.clear()
    print(data)
    await message.answer('Регистрация успешно завершена')

@user_router.message(Command('pull'))
async def cmd_pull(message: Message, state: FSMContext):
    print(data)
    if len(data) == 0:
        await message.answer('Пройдите в начале регистрацию')
    else:
        await state.set_state(Log_in.name)
        await message.answer('Напишите имя пользователя')

@user_router.message(Log_in.name)
async def cmd_name_Log_in(message: Message, state: FSMContext):
        if message.text == data['name']:
            await state.set_state(Log_in.pw)
            await message.answer('Напишите пароль')
        else:
            await message.answer('Неверное имя пользователя')

@user_router.message(Log_in.pw)
async def cmd_name_Log_in(message: Message, state: FSMContext):
        if message.text == data['pw']:
            await state.clear()
            await message.answer_sticker(r'CAACAgIAAxkBAAEMsNVntMI6MzErJCqPn-d-oJ4HSLkHZQACDAIAArm7RxnSXrEl8ZdrWjYE')
        else:
            await message.answer('Неверный пароль')    

@user_router.message()
async def cmd_start(message: Message):
    await message.answer('Шо тебе?')