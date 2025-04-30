from random import *
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, Application, CommandHandler, CallbackQueryHandler
import classes


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class state:
    def __init__(self, state_id, text, outcome, buttons, outtext,  pic=None):
        self.state_id = state_id
        self.text = text
        self.outcome = outcome
        self.buttons = buttons
        self.outtext = outtext


class StateMachine:
    def __init__(self, states, manager: classes.MySQLDataBase): #update: Update, manager: classes.MySQLDataBase, context: ContextTypes.DEFAULT_TYPE Их нужно передавать в функции
        self.manager = manager
        self.states = states
        self.current_state = None
    #async def out(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # await update.message.reply_text(self.text, reply_markup=InlineKeyboardMarkup(keyboard))
    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        query.answer()
        user = self.manager.find_user_by_tgid(update.effective_user.id)
        # await update.effective_message.delete()
        # self.manager.update_user_count(update.effective_user.id, int(user['count']) + self.outcome[int(query.data)])  #тут outcome
        # await context.bot.send_message(update.effective_chat.id, text = f"{self.outtext[int(query.data)]} {int(user['count']) + self.outcome[int(query.data)]}") #и тут по сути outtext
    async def get_random_state(self):
        self.current_state = choice(self.states)
        keyboard = []
        for x in range(len(self.current_state.buttons)):
            keyboard.append([InlineKeyboardButton(self.current_state.buttons[x], callback_data=f'{x}')])
        '''
        И так, прикол в том, что он бесконечно отправляет одно сообщение, потому что у меня все было в цикле while. Поэтому надо переделать все с помощью deepseek и рекурсии. 
        Еще, как идея на будущее, сделать так, чтобы state подтягивались из другого файла, где их будет удобно создавать. А так всё ок :)
        '''


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
        stateMachine = StateMachine(states, manager)
        current_state = states[0]

            
