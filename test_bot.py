from random import *
import logging
from telegram import Update
from telegram.ext import CommandHandler, Application, ContextTypes, MessageHandler, filters
TestBotAPI_Token = "7861786407:AAHxk0wOV7Tt9JCO3MdFbpxFJNBlw8vGVPM"
changer = 0
changer_log = []
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', #Просто чтоб понять, что и где сломалось
    level=logging.INFO
)

#ФУНКЦИЯ СТАРТ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):  
    await context.bot.send_message(chat_id=update.effective_chat.id, text="OMG, AMMALIVE")

#ФУНКЦИЯ ЭХО
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

#ФУНКЦИЯ КАПС
async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

#ФУНКЦИЯ ПЛЮС
async def plus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global changer
    global changer_log
    inputed = context.args
    try:
        num = sum(list(map(int, context.args)))
        changer += num
        changer_log.append(f"Успешно добавили к числу {changer}, число {num}")
        await context.bot.send_message(update.effective_chat.id, text=f"Изначально было число: {changer-num}\nНо теперь оно: {changer}")
    except:
        print(f"Не удалось к числу: {changer} добавить: {inputed}")
        changer_log.append(f"Не удалось добавить к числу {changer}, число {inputed}")
        await context.bot.send_message(update.effective_chat.id, text=f"Произошла ошибка!!!\nНе удалось добавить {inputed}")
#ФУКНЦИЯ ДЛЯ ПОЛУЧЕНИЯ ЛОГОВ ФУНКЦИИ ПЛЮС
async def changerlog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global changer_log
    output = ""
    if len(changer_log) > 0:
        i = 1
        for x in changer_log:
            output += f"{i}. {x}\n"
            i+=1
        await context.bot.send_message(update.effective_chat.id, text=output)
    else:
        await context.bot.send_message(update.effective_chat.id, text="Логи пусты. Действий с функцией 'plus' не было") 


if __name__ == '__main__':
    application = Application.builder().token(TestBotAPI_Token).build() #Создаем бота

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo) #фильтрует, что сообщение это только текст и не команда
    start_handler = CommandHandler('start', start)
    caps_handler = CommandHandler('caps', caps)
    plus_handler = CommandHandler('plus', plus)
    changerLogs_handler = CommandHandler('Changerlog', changerlog)


    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(plus_handler)
    application.add_handler(changerLogs_handler)


    application.run_polling()