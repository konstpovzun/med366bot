from aiogram.fsm.state import State, StatesGroup

class MedForm(StatesGroup):
    choose_action = State()
    consent = State()
    age = State()
    gender = State()
    weight = State()
    symptoms = State()
    symptoms_clarify = State()
    link = State()
    fact = State()
    photo = State()
    video = State() # <--- НОВОЕ СОСТОЯНИЕ

class Feedback(StatesGroup):
    waiting = State()