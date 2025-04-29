from random import *
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, Application, CommandHandler, CallbackQueryHandler
from functools import partial
import classes


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class state:
    def __init__(self,  state_id, text, outcome, buttons, outtext, manager: classes.MySQLDataBase,  pic=None): #update: Update, manager: classes.MySQLDataBase, context: ContextTypes.DEFAULT_TYPE Их нужно передавать в функции
        self.state_id = state_id
        self.text = text
        self.outcome = outcome
        self.buttons = buttons
        self.outtext = outtext
        self.manager = manager
    async def out(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = []
        for x in range(len(self.buttons)):
            keyboard.append([InlineKeyboardButton(self.buttons[x], callback_data=f'{x}')])
        await update.message.reply_text(self.text, reply_markup=InlineKeyboardMarkup(keyboard))
    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        query.answer()
        user = self.manager.find_user_by_tgid(update.effective_user.id)
        self.manager.update_user_count(update.effective_user.id, int(user['count']) + self.outcome[int(query.data)])  #тут outcome
        await context.bot.send_message(update.effective_chat.id, text = f"{self.outtext[int(query.data)]} {int(user['count']) + self.outcome[int(query.data)]}") #и тут по сути outtext
states = []

def createStates(manager):
        counter_state = state(
            0,
            "Число 10 к счетчику?",
            [+10, -10],
            ["Прибавить", "Убавить"],
            ["Вы прибавили 10 к числу: ", "Вы убавили на 10 число: "],
            manager
        )
        states.append(counter_state)


class game:
    def __init__(self, application: Application, database: classes.MySQLDataBase, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.application = application
        self.manager = database
        self.context = context
        self.update = update
    
    async def play(self):
        context = self.context 
        update = self.update
        manager = self.manager
        application = self.application
        createStates(manager)
        current_state = states[0]
        application.add_handler(CallbackQueryHandler(current_state.button))
        await current_state.out(update, context)