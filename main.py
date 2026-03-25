import time
import json
import random

from api import get_updates, send_message
from Player import Player
from settings import DB_CONFIG
from event import Event
from database import MySQLDataBase


db = MySQLDataBase(DB_CONFIG)
db.connect()

players = {}        # tgid -> Player
user_events = {}    # tgid -> Event


with open("events.json", "r", encoding="utf-8") as f:
    events_data = json.load(f)

events = [Event.from_dict(e) for e in events_data]


