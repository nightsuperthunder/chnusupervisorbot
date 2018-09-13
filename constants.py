token = '624978899:AAHo3bgD0eSC0v8dXXArn_J20FLyxxd34vU'
stiker = 'CAADAgADKQEAAnmyPgQ-rNllRYk49QI'
dialogapi = '3d60f863d80240a6b9fd267573536717'
owmapi = 'bc96319d28889b242c88cdb749655b9f'
startrepl = 'Hello'
startreplo = 'Hello again'
helprepl = '/weather - теперішня погода \n/timetable - розклад \n/regtogr - реєстрація у групу'
bossid = '304206657'
chatlogid = '-280745551'
pari = {
    1 : 'Інженерна графіка',
    2 : 'Вища математика',
    3 : 'Персональні комп\'ютери',
    4 : 'Охорона праці',
    5 : 'Іноземна мова',
    6 : 'Іноземна мова (спецкурс)',
    7 : 'Основи алгоритмізації та програмування',
    8 : 'Фізика',
    9 : 'Фізика (лаб)',
}
def log (message):
    import telebot
    bot = telebot.TeleBot(token)
    bot.send_message(chatlogid, 'Повід від {0} {1}. (id = {2}) \n Текст - {3} \n'.format(message.from_user.first_name,
                                                                                         message.from_user.last_name,
                                                                                         str(message.from_user.id),
                                                                                         message.text, ))


users = set()
st142a1 = set()
st142a2 = set()
st142b1 = set()
st142b2 = set()
