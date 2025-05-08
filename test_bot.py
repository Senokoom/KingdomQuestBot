from random import *
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Application, ContextTypes, MessageHandler, filters, CallbackQueryHandler
import classes

TestBotAPI_Token = "7861786407:AAHxk0wOV7Tt9JCO3MdFbpxFJNBlw8vGVPM"
# user_data = []


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', #Просто чтоб понять, что и где сломалось
    level=logging.INFO
)




class state:
    def __init__(self, state_id, text, outcome, buttons, outtext, pic=None):
        self.state_id = state_id
        self.text = text
        self.outcome = outcome
        self.buttons = buttons
        self.outtext = outtext


#ЭТО БЫЛО РЕШЕНИЕ С ИСПОЛЬЗОВАНИЕМ INLINE КНОПОК. НЕ СРАБОТАЛО ИЗ-ЗА ПРОБЛЕМ С ПОЛУЧЕНИЕМ update (как я понял)

# async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     query.answer()
#     user = manager.find_user_by_tgid(update.effective_user.id)
#     current_state = states[int(user['state'])]  #ТУТ из БД достается текущий state. Нужно добавить обновление
#     manager.update_user_count(update.effective_user.id, int(user['count']) + current_state.outcome[int(query.data)])  #тут outcome
#     await update.callback_query.edit_message_text(text = f"{current_state.outtext[int(query.data)]} {int(user['count']) + current_state.outcome[int(query.data)]}") #и тут по сути outtext
#     await get_random_state(update)


# async def get_random_state(update: Update):
#     current_state = choice(states)
#     manager.update_user_state(update.effective_user.id, states.index(current_state)) #тут закидывает в бдшку новый индекс state
#     keyboard = []
#     for x in range(len(current_state.buttons)):
#         keyboard.append([InlineKeyboardButton(current_state.buttons[x], callback_data=f'{x}')])
    
#     await update.message.reply_text(
#         current_state.text,
#         reply_markup=InlineKeyboardMarkup(keyboard)
#         )


async def MessAns(update: Update, context: ContextTypes.DEFAULT_TYPE): #это handler reply. Вызывается, когда польз пишет что-то
    
    user = manager.find_user_by_tgid(update.effective_user.id)
    current_state : state = states[int(user['state'])]  #ТУТ из БД достается текущий state
    flag = False
    try:
        uwu = current_state.buttons.index(update.message.text)
        outcome = current_state.outcome[uwu] #тут вложенный массив, т.к. потом будет проще изменять больше, чем 1 параметр
        counter = outcome[0]
        manager.update_user_count(update.effective_user.id, int(user['count']) + counter)  #тут outcome заносится в бд
        flag = True
    except:
        await context.bot.send_message(update.effective_chat.id, text = "Incorrect input")
    if(flag):
        await context.bot.send_message(update.effective_chat.id, text = f"Ты молодец, {current_state.outtext[uwu]} {int(user['count']) + current_state.outcome[uwu][0]}")
        await get_random_state(update)




async def get_random_state(update: Update):
    current_state = choice(states)
    manager.update_user_state(update.effective_user.id, states.index(current_state)) #тут закидывает в бдшку новый индекс state
    keyboard = [[x] for x in current_state.buttons]
    keyboard.append(["/showcount"])
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        current_state.text,
        reply_markup=reply_markup
    )



states = []

def createStates():
        counter_state = state(
            0,
            "Число 10 к счетчику?",
            [[10], [-10]],
            ["Прибавить", "Убавить"],
            ["Вы прибавили 10 к числу: ", "Вы убавили на 10 число: "]
        )
        states.append(counter_state)



#ФУНКЦИЯ СТАРТ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _user = manager.get_or_create_user(update.effective_user.id)
    if _user != None:
        print(_user)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Started the bot.\nWelcome, {update.effective_user.first_name}!")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="произошла ошибка, сорян")

#ВЫВОДИТ ТЕКУЩИЙ count ЮЗЕРА
async def showcount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _user = manager.get_or_create_user(update.effective_user.id)
    if _user != None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=(f" Ваш текущий счетчик это: {_user['count']}!"))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="произошла ошибка, сорян")

#ФУНКЦИЯ ЭХО
#async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

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
        await context.bot.send_message(update.effective_chat.id, text=f"Изначально было число: {_user['count']}\nНо теперь оно: {_user['count']+num}")
    except:
        print(f"Не удалось к числу: {_user['count']} добавить: {inputed}")
        await context.bot.send_message(update.effective_chat.id, text=f"Произошла ошибка!!!\nНе удалось добавить {inputed}")



async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    createStates()
    await get_random_state(update)


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

    #echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo) #фильтрует, что сообщение это только текст и не команда
    start_handler = CommandHandler('start', start)
    caps_handler = CommandHandler('caps', caps)
    plus_handler = CommandHandler('plus', plus)
    play_handler = CommandHandler('play', play)
    answer_uwu_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, MessAns)
    showcount_handler = CommandHandler('showcount', showcount)
    

    # changerLogs_handler = CommandHandler('Changerlog', changerlog)
    application.add_handler(start_handler)
    #application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(plus_handler)
    application.add_handler(play_handler)
    application.add_handler(showcount_handler)
    application.add_handler(answer_uwu_handler)
    # application.add_handler(changerLogs_handler)

    application.run_polling()





