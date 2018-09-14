token = '624978899:AAHo3bgD0eSC0v8dXXArn_J20FLyxxd34vU'
stiker = 'CAADAgADKQEAAnmyPgQ-rNllRYk49QI'
dialogapi = '3d60f863d80240a6b9fd267573536717'
owmapi = 'bc96319d28889b242c88cdb749655b9f'
startrepl = 'Hello'
startreplo = 'Hello again'
helprepl = '/weather - теперішня погода'
bossid = '304206657'
chatlogid = '-280745551'


def log (message):
    import telebot
    bot = telebot.TeleBot(token)
    bot.send_message(chatlogid, 'Повід від {0} {1}. (id = {2}) \n Текст - {3} \n'.format(message.from_user.first_name,
                                                                                         message.from_user.last_name,
                                                                                         str(message.from_user.id),
                                                                                         message.text, ))


users = set()
