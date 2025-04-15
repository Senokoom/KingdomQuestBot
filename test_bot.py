from random import *
import logging
from telegram import Update
from telegram.ext import CommandHandler, Application, ContextTypes, MessageHandler, filters
import classes
import thegame

TestBotAPI_Token = "7861786407:AAHxk0wOV7Tt9JCO3MdFbpxFJNBlw8vGVPM"
# user_data = []


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', #Просто чтоб понять, что и где сломалось
    level=logging.INFO
)


# def UserFinder(user_id):
#     print(f"Поиск: {user_id}")
#     for user in user_data:
#         if(user_id == user.id):
#             print("Нашёл")
#             return user
#     print("Такого нет")
#     return False


# def CheckUserInSystem(user_id): #сюда на вход поступает id пользователя
#     print(f"Существует ли: {user_id}")
#     for user in user_data:
#         if(user_id == user.id):
#             print("уже у нас, сворачиваемся")
#             return True #user already in userdata, no need to worry
#     try:
#         user_data.append(classes.user(user_id))
#         print("Добавили")
#         return True
#     except:
#         print("ошибочка получилась")
#         return False



#ФУНКЦИЯ СТАРТ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _user = manager.get_or_create_user(update.effective_user.id)
    if _user != None:
        print(_user)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Started the bot.\nWelcome, {update.effective_user.first_name}!")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="произошла ошибка, сорян")

#ФУНКЦИЯ ЭХО
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

#ФУНКЦИЯ КАПС
async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)



#ФУНКЦИЯ ПЛЮС
async def plus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _user = manager.find_user_by_tgid(update.effective_user.id)
    inputed = context.args
    try:
        num = sum(list(map(int, context.args)))
        manager.update_user_count(_user['tgid'], _user['count'] + num)
        # _user.changer_log.append(f"Успешно добавили к числу {_user.changer-num}, число {num}")
        await context.bot.send_message(update.effective_chat.id, text=f"Изначально было число: {_user['count']}\nНо теперь оно: {_user['count']+num}")
    except:
        print(f"Не удалось к числу: {_user['count']} добавить: {inputed}")
        # _user.changer_log.append(f"Не удалось добавить к числу {_user.changer}, число {inputed}")
        await context.bot.send_message(update.effective_chat.id, text=f"Произошла ошибка!!!\nНе удалось добавить {inputed}")




#ФУКНЦИЯ ДЛЯ ПОЛУЧЕНИЯ ЛОГОВ ФУНКЦИИ ПЛЮС
# async def changerlog(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     _user = manager.find_user_by_tgid(update.effective_user.id)
#     output = ""
#     if len(_user.changer_log) > 0:
#         i = 1
#         for x in _user.changer_log:
#             output += f"{i}. {x}\n"
#             i+=1
#         await context.bot.send_message(update.effective_chat.id, text=output)
#     else:
#         await context.bot.send_message(update.effective_chat.id, text="Логи пусты. Действий с функцией 'plus' не было")




def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = manager.get_or_create_user(update.effective_user.id)
    game = thegame.game(
        user, 
        update,
        context
    )
    game.play()





# ЭТО ЗАПУСКАЕТСЯ, КОГДА ЗАПУСКАЮ КОД
if __name__ == '__main__':

    config = {
        'host': '185.9.147.4',
        'port' : '3312',
        'database': 'kingdom',
        'user': 'leva',
        'password': 'jV8kF0mC0q'
    }
    manager = classes.MySQLDataBase(**config)


    application = Application.builder().token(TestBotAPI_Token).build() #построили бота

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo) #фильтрует, что сообщение это только текст и не команда
    start_handler = CommandHandler('start', start)
    caps_handler = CommandHandler('caps', caps)
    plus_handler = CommandHandler('plus', plus)
    play_handler = CommandHandler('play', play)
    # changerLogs_handler = CommandHandler('Changerlog', changerlog)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(plus_handler)
    application.add_handler(play_handler)
    # application.add_handler(changerLogs_handler)



    application.run_polling()

