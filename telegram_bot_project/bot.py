import telebot
from telebot import formatting
from icalendar import Calendar
from datetime import datetime
from datetime import date
from datetime import timedelta

# Создаем экземпляр календаря
#calendar = Calendar()
calendar = {}
# Создаем экземпляр бота
bot = telebot.TeleBot('5878418008:AAE3g9LSPismvIqqzYgFfmICT6qYfY3jWec')

bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("help", "Помощь."),
        telebot.types.BotCommand("next", "Какая моя следующая пара?"),
        telebot.types.BotCommand("room", "В какую аудиторию мне нужно идти сейчас?"),
        telebot.types.BotCommand("tom", "Какие у меня пары завтра?"),
        telebot.types.BotCommand("sem", "Ближайший семенар."),
        telebot.types.BotCommand("lec", "Ближайшая лекция."),
    ],
)
# check command
cmd = bot.get_my_commands(scope=None, language_code=None)

# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Привет! Я бот-помощник по учебе. '
            'Скинь мне ical-файл c РУЗ (https://ruz.hse.ru/ruz/main) '
            'и я помогу тебе сориентироваться в расписании.'
            'Мои команды:\n'
            '"/help", "Помощь."\n'
            '"/next", "Какая моя следующая пара?"\n'
            '"/tom", "Какие у меня пары завтра?"\n'
            '"/room", "В какую аудиторию мне нужно идти сейчас?"\n'
            '"/sem", "Ближайший семенар."\n'
            '"/lec", "Ближайшая лекция."'
            )
# Помощь
@bot.message_handler(commands=["help"])
def help(m, res=False):
    bot.send_message(m.chat.id, 'Привет! Я бот-помощник по учебе. '
            'Скинь мне ical-файл c РУЗ (https://ruz.hse.ru/ruz/main) '
            'и я помогу тебе сориентироваться в расписании.'
            'Мои команды:\n'
            '"/help", "Помощь."\n'
            '"/next", "Какая моя следующая пара?"\n'
            '"/tom", "Какие у меня пары завтра?"\n'
            '"/room", "В какую аудиторию мне нужно идти сейчас?"\n'
            '"/sem", "Ближайший семенар."\n'
            '"/lec", "Ближайшая лекция."'
            )

def get_next_event(clnd, date, ev_type=None):
    current_event = None
    for component in clnd.walk():
        if component.name == "VEVENT":
            if ev_type == "sem":
                if current_event is None and "Семинар" in component['description']:
                    current_event = component
                else:
                    continue
                if date < component['dtstart'].dt and component['dtstart'].dt < current_event['dtstart'].dt and "Семинар" in component['description']:
                    current_event = component
            elif ev_type == "lec":
                if current_event is None and "Лекция" in component['description']:
                    current_event = component
                else:
                    continue
                if date < component['dtstart'].dt and component['dtstart'].dt < current_event['dtstart'].dt and "Лекция" in component['description']:
                    current_event = component
            else:
                if current_event is None:
                    current_event = component
                if date < component['dtstart'].dt and component['dtstart'].dt < current_event['dtstart'].dt:
                    current_event = component
    return current_event

@bot.message_handler(commands=["next"])
def next(m, res=False):
    global calendar
    now = datetime.now()
    if m.chat.id in calendar:
        current_event = get_next_event(calendar[m.chat.id], now)

        if current_event is not None and now < current_event['dtstart'].dt:
            reply = "Следующая пара: {}\nНачало: {}\nОкончание: {}".format(
                    current_event['summary'], current_event['dtstart'].dt, current_event['dtend'].dt)
            bot.send_message(m.chat.id, reply)
        else:
            bot.send_message(m.chat.id, "Следующих занятий не найдено.")
    else:
        bot.send_message(m.chat.id, "Следующих занятий не найдено. Загрузи ical-файл с расписанием.")


@bot.message_handler(commands=["room"])
def room(m, res=False):

    global calendar
    now = datetime.now()
    if m.chat.id in calendar:
        current_event = get_next_event(calendar[m.chat.id], now)

        if current_event is not None and now < current_event['dtstart'].dt:
            reply = "Тебе в аудиторию: {}\n к {}.".format(
                    current_event['location'], current_event['dtstart'].dt)
            bot.send_message(m.chat.id, reply)
        else:
            bot.send_message(m.chat.id, "Следующих занятий не найдено.")
    else:
        bot.send_message(m.chat.id, "Следующих занятий не найдено. Загрузи ical-файл с расписанием.")

@bot.message_handler(commands=["lec"])
def lec(m, res=False):
    global calendar
    now = datetime.now()
    if m.chat.id in calendar:
        current_event = get_next_event(calendar[m.chat.id], now, ev_type="lec")

        if current_event is not None and now < current_event['dtstart'].dt:
            reply = "Следующая лекция: {}\nНачало: {}\nОкончание: {}".format(
                    current_event['summary'], current_event['dtstart'].dt, current_event['dtend'].dt)
            bot.send_message(m.chat.id, reply)
        else:
            bot.send_message(m.chat.id, "Следующих лекций не найдено.")
    else:
        bot.send_message(m.chat.id, "Следующих занятий не найдено. Загрузи ical-файл с расписанием.")

@bot.message_handler(commands=["sem"])
def sem(m, res=False):
    global calendar
    now = datetime.now()
    if m.chat.id in calendar:
        current_event = get_next_event(calendar[m.chat.id], now, ev_type="sem")

        if current_event is not None and now < current_event['dtstart'].dt:
            reply = "Следующий семинар: {}\nНачало: {}\nОкончание: {}".format(
                    current_event['summary'], current_event['dtstart'].dt, current_event['dtend'].dt)
            bot.send_message(m.chat.id, reply)
        else:
            bot.send_message(m.chat.id, "Следующих семинаров не найдено.")
    else:
        bot.send_message(m.chat.id, "Следующих занятий не найдено. Загрузи ical-файл с расписанием.")


def get_tom(clnd, date):
    tom_events = []
    now = datetime.now()
    for component in clnd.walk():
        if component.name == "VEVENT":
            if date > component['dtstart'].dt and now < component['dtstart'].dt:
                tom_events.append(component)
    return tom_events

@bot.message_handler(commands=["tom"])
def tom(m, res=False):

    global calendar
    tom = date.today() + timedelta(days=2)
    tom = datetime(tom.year, tom.month, tom.day)
    if m.chat.id in calendar:
        t_events = get_tom(calendar[m.chat.id], tom)

        reply = ""
        for ev in t_events:
            reply += "{} c {} до {}\n".format(
                    ev['summary'], ev['dtstart'].dt, ev['dtend'].dt)
        if reply:
            bot.send_message(m.chat.id, "Расписание на завтра:")
            bot.send_message(m.chat.id, reply)
        else:
            bot.send_message(m.chat.id, "Занятий на завтра не найдено.")
    else:
        bot.send_message(m.chat.id, "Следующих занятий не найдено. Загрузи ical-файл с расписанием.")

# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(m):
    bot.send_message(m.chat.id, 'Привет! Я бот-помощник по учебе. '
            'Скинь ical-файл c РУЗ (https://ruz.hse.ru/ruz/main) '
            'и я помогу тебе сориентироваться в расписании.'
            'Мои команды:\n'
            '"/help", "Помощь."\n'
            '"/next", "Какая моя следующая пара?"\n'
            '"/tom", "Какие у меня пары завтра?"\n'
            '"/room", "В какую аудиторию мне нужно идти сейчас?"\n'
            '"/sem", "Ближайший семенар."\n'
            '"/lec", "Ближайшая лекция."'
            )

@bot.message_handler(content_types=['document'])
def cal(m):
    file_info = bot.get_file(m.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    global calendar
    try:
        calendar[m.chat.id] = Calendar.from_ical(downloaded_file)
    except:
        bot.send_message(m.chat.id, "Не удалось прочитать расписание.")

# Запускаем бота
bot.polling(none_stop=True, interval=0)
