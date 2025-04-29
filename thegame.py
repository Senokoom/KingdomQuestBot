from random import *
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Application, ContextTypes, MessageHandler, filters
from transitions import Machine
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

# states = []
# state_addcount = state(
#     0,
#     "Число 10 к счетчику?",
#     [["прибавить"], ["убавить"]],
#     ["Вы прибавили 10", "Вы убавили 10"]
# )
# states.append(state_addcount)


class game:
    def __init__(self, database: classes.MySQLDataBase, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.manager = database
        self.context = context
        self.update = update
    
    async def play(self):
        context = self.context 
        update = self.update
        manager = self.manager
        user = manager.get_or_create_user(update.effective_user.id)
        counter = user['count']