# mastrobot_example.py
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

STATE = None

BIRTH_YEAR = 1
BIRTH_MONTH = 2
BIRTH_DAY = 3

# function to handle the /start command
def start(update, context):
    first_name = update.message.chat.first_name
    update.message.reply_text(f"Hi {first_name}, nice to meet you!")
    start_getting_birthday_info(update, context)

def start_getting_birthday_info(update, context):
    global STATE
    STATE = BIRTH_YEAR
    update.message.reply_text(f"I would need to know your birthday, so tell me what year did you born in...")

# function to handle the /help command
def help(update, context):
    update.message.reply_text('help command received')

# function to handle errors occured in the dispatcher
def error(update, context):
    update.message.reply_text('an error occured')

# function to handle normal text
def text(update, context):
    global STATE

    if STATE == BIRTH_YEAR:
        return received_birth_year(update, context)

    if STATE == BIRTH_MONTH:
        return received_birth_month(update, context)

    if STATE == BIRTH_DAY:
        return received_birth_day(update, context)


def received_birth_year(update, context):
    global STATE

    try:
        today = datetime.date.today()
        year = int(update.message.text)

        if year > today.year:
            raise ValueError("invalid value")

        context.user_data['birth_year'] = year
        update.message.reply_text(f"ok, now I need to know the month (in numerical form)...")
        STATE = BIRTH_MONTH
    except:
        update.message.reply_text("it's funny but it doesn't seem to be correct...")

def received_birth_month(update, context):
    global STATE

    try:
        today = datetime.date.today()
        month = int(update.message.text)

        if month > 12 or month < 1:
            raise ValueError("invalid value")

        context.user_data['birth_month'] = month
        update.message.reply_text(f"great! And now, the day...")
        STATE = BIRTH_DAY
    except:
        update.message.reply_text("it's funny but it doesn't seem to be correct...")

def received_birth_day(update, context):
    global STATE

    try:
        today = datetime.date.today()
        dd = int(update.message.text)
        yyyy = context.user_data['birth_year']
        mm = context.user_data['birth_month']
        birthday = datetime.date(year=yyyy, month=mm, day=dd)

        if today - birthday < datetime.timedelta(days=0):
            raise ValueError("invalid value")

        context.user_data['birthday'] = birthday
        STATE = None
        update.message.reply_text(f'ok, you born on {birthday}')

    except:
        update.message.reply_text("it's funny but it doesn't seem to be correct...")

def main():
    TOKEN = "1651091717:AAGIb112p3wgd-ai2tZ4nO1t0QLp4nVRo6M"

    # create the updater, that will automatically create also a dispatcher and a queue to
    # make them dialoge
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # add handlers for start and help commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))

    # add an handler for normal text (not commands)
    dispatcher.add_handler(MessageHandler(Filters.text, text))

    # dispatcher.add_handler(CommandHandler("biorhythm", biorhythm))

    # add an handler for errors
    dispatcher.add_error_handler(error)


    # start your shiny new bot
    updater.start_polling()

    # run the bot until Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
