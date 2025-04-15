from random import *
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Application, ContextTypes, MessageHandler, filters
import test_bot
import classes


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class state:
    def __init__(self,  state_id, text, buttons, aftermath, pic=None):
        self.state_id = state_id
        self.text = text
        self.buttons = buttons
        self.aftermath = aftermath
        self.pic = pic

# нифига пока не работает
# Надо сделать обработчик ответов(желательно универсальныим)
# И надо еще решить ошибку, с тем, что вообще этот код не запускается

states = []
state_addcount = state(
    0,
    "Число 10 к счетчику?",
    [["прибавить"], ["убавить"]],
    ["Вы прибавили 10", "Вы убавили 10"]
)
states.append(state_addcount)


class game:
    def __init__(self, user, database, application, update, context):
        self.user = user
        self.application = application
        self.manager = database
        self.context = context
        self.update = update
    
    def play(self):
        user = self.user
        context = self.context 
        update = self.update
        manager = self.manager
        counter = user['count']
        while counter != 110:
            context.bot.send_message(update.effective_chat.id, text = f"Прибавили к {counter}: 10.\nПолучилось {counter+10} ")
            manager.update_user_count(user['tgid'], counter+10)
            counter+=10
            
