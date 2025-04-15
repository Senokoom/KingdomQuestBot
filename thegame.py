from random import *
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Application, ContextTypes, MessageHandler, filters


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
    def __init__(self, user, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.user = user
        self.context = context
        self.update = update
    
    def play(self):
        reply_markup = ReplyKeyboardMarkup(states[self.user['state']].buttons, resize_keyboard=True)
        self.update.message.reply_text(states[self.user['state']].text, reply_markup=reply_markup)