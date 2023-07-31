from dotenv import load_dotenv
import os
import dotenv
from dotenv import dotenv_values
from aiogram import Bot, Dispatcher, executor, types, filters
from parse import term_reader
from dbmanager import Database

load_dotenv()
vars = ["", "", "", False]

bot = Bot(os.getenv("API_TOKEN"), proxy=os.environ.get("PROXY_URL"))
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=("start"))
async def registration(message: types.Message):
    with Database() as db_cursor:
        if not db_cursor.execute("""select * from users where ID = {}""".format(message.from_user.id)).fetchall():
            vars[3] = True
            await message.answer("Введите логин")
        else:
            await message.answer("Уже есть в бд")


@dispatcher.message_handler(commands=("term_mean"))
async def cmd_last_mean(message: types.Message):
    with Database() as db_cursor:
        print(db_cursor.execute("""select * from users where ID = {}""".format(message.from_user.id)).fetchall())
        if db_cursor.execute("""select * from users where ID = {}""".format(message.from_user.id)).fetchall():
            keyboard = types.InlineKeyboardMarkup(row_width=15)
            keyboard.add(types.InlineKeyboardButton(text="1", callback_data="1"))
            keyboard.add(types.InlineKeyboardButton(text="2", callback_data="2"))
            keyboard.add(types.InlineKeyboardButton(text="3", callback_data="3"))
            await message.answer("Выберите триместр", reply_markup=keyboard)
        else:
            await message.answer("Введите данные, (start)")


@dispatcher.message_handler()
async def reg2(mes: types.Message):

    if vars[3]:
        info = await bot.get_me()
        vars[0] = info.username
        print(mes.text, info.username, mes.from_user.full_name)
        change = 0
        if not vars[1]:
            print(mes.text, 1)
            vars[1] = mes.text
            change = 1
            await mes.answer("Введите пароль")


        if not vars[2] and not change:
            print(mes.text, 2, change, vars[2])
            vars[2] = mes.text
            # dotenv.set_key(dotenv_file, "password",  mes.text)
            print(vars)
            #password = vars[2].encode('utf-8')
            values = (mes.from_user.id, vars[1], vars[2])
    
            #with sqlite3.connect("parsebot.db") as conn:
            # conn = sqlite3.connect("parsebot.db")
            # cursor = conn.cursor()
            with Database() as db_cursor:
                db_cursor.execute("""
                        INSERT INTO users(ID, username, password) VALUES
                        (?, ?, ?)
                        """, values)
            await mes.answer("Вы зарегистрированы")


@dispatcher.callback_query_handler()
async def cmd_term_mean(call: types.CallbackQuery):
    with Database() as db_cursor:
        lst = db_cursor.execute("""select * from users where ID = {}""".format(call.from_user.id)).fetchall()
    h = term_reader(int(call.data)-1, lst[0][1], lst[0][2])
    await call.message.answer(h, reply_markup=types.ReplyKeyboardRemove())

print(__name__)
if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True)