import telebot, constants, json, apiai, pyowm, pickle  # pyowm 2.9.0
from telebot.types import Message

bot = telebot.TeleBot(constants.token)
constants.users = pickle.load(open('save.p', 'rb'))

@bot.message_handler(commands=['start'])
def command_handler(message: Message):
    constants.log(message)
    if message.from_user.id in constants.users:
        bot.reply_to(message, constants.startreplo)
    else:
        bot.reply_to(message, constants.startrepl)
        constants.users.add(message.from_user.id)
        pickle.dump(constants.users, open('save.p', 'wb'))

@bot.message_handler(commands=['help'])
def command_handler(message: Message):
    constants.log(message)
    bot.reply_to(message, constants.helprepl)

@bot.message_handler(commands=['log'])
def cllogch(message: Message):
    constants.log(message)
    if int(message.from_user.id) == int(constants.bossid):
        ver = bot.reply_to(message, 'Логи (очистити , отримати , очистити користувачів) ?')
        bot.register_next_step_handler(ver, cllog)
    else:
        bot.reply_to(message, 'Відмовнено в доступі')

def cllog (message: Message):
    ver = message.text
    constants.log(message)
    if ver == 'очистити':
        open('log.txt', 'w').close()
        bot.send_message(message.chat.id, 'Логи очищено!')
    elif ver == 'отримати':
        file = open('log.txt', 'rb')
        bot.send_document(message.from_user.id, file)
    elif ver == 'очистити користувачів':
        open('save.p', 'w').close()
        constants.users = set()
        #constants.users.add(constants.bossid)
        pickle.dump(constants.users, open('save.p', 'wb'))
        bot.send_message(message.chat.id, 'Користувачів очищено!')
    else:
        bot.send_message(message.chat.id, 'Невдала спроба')

@bot.message_handler(commands=['weather'])
def command_handler(message: Message):
    town =  bot.reply_to(message, 'В якому місті покзати погоду?')
    bot.register_next_step_handler(town, weth)
    constants.log(message)
def weth (message : Message):
    i = 1
    owm = pyowm.OWM(constants.owmapi, language= 'ua')
    town = message.text
    constants.log(message)
    try:
        observa = owm.weather_at_place(town)
    except:
        bot.send_message(message.chat.id, 'Місто не знайдене повторіть ще раз /weather')
        return
    w = observa.get_weather()
    temperature = w.get_temperature(unit='celsius')['temp']
    press = w.get_pressure()['press']
    press = press / 1.33
    wind = w.get_wind()['speed']
    try:
        windnap = w.get_wind()['deg']
    except KeyError:
        i = 0
    if i:
        l = ['Північний ', 'Північно-Східний ', 'Східний ', 'Південно-Східний ', 'Південний ', 'Південно-Західний ',
             'Західний ', 'Північно-Західний ']
        for j in range(0, 8):
            step = 45.
            min = j * step - 45 / 2.
            max = j * step + 45 / 2.
            if j == 0 and windnap > 360 - 45 / 2.:
                windnap = windnap - 360
            if windnap >= min and windnap <= max:
                reswindnap = l[j]
                break
            if int(temperature) == 1:
                bot.send_message(message.chat.id, 'Зараз ' + str(int(temperature)) + ' градус')
            elif int(temperature) == 2 or int(temperature) == 3 or int(temperature) == 4:
                bot.send_message(message.chat.id, 'Зараз ' + str(int(temperature)) + ' градуси')
            else:
                bot.send_message(message.chat.id, 'Зараз ' + str(int(temperature)) + ' градусів')
        bot.send_message(message.chat.id,'Статус ' + w.get_detailed_status())
        bot.send_message(message.chat.id,'Небо грязне на ' + str(w.get_clouds()) + '%')
        if w.get_rain() == {}:
            bot.send_message(message.chat.id,'Дощу нема')
        else:
            bot.send_message(message.chat.id,'Дощ' + str(w.get_rain()))
        if w.get_snow() == {}:
            bot.send_message(message.chat.id,'Снігу нема')
        else:
            bot.send_message(message.chat.id,'Сніг' + str(w.get_snow()))
        bot.send_message(message.chat.id,'Вітер ' + str(reswindnap) + str(wind) + 'м/с')
        bot.send_message(message.chat.id,'Вологість ' + str(w.get_humidity()) + '%')
        bot.send_message(message.chat.id,'Тиск ' + str(int(press)) + ' мм. рт. ст.')
    else:
        if int(temperature) == 1:
                bot.send_message(message.chat.id, 'Зараз ' + str(int(temperature)) + ' градус')
            elif int(temperature) == 2 or int(temperature) == 3 or int(temperature) == 4:
                bot.send_message(message.chat.id, 'Зараз ' + str(int(temperature)) + ' градуси')
            else:
                bot.send_message(message.chat.id, 'Зараз ' + str(int(temperature)) + ' градусів')
        bot.send_message(message.chat.id,'Статус ' + w.get_detailed_status())
        bot.send_message(message.chat.id,'Небо грязне на ' + str(w.get_clouds()) + '%')
        if w.get_rain() == {}:
            bot.send_message(message.chat.id,'Дощу нема')
        else:
            bot.send_message(message.chat.id,'Дощ' + str(w.get_rain()))
        if w.get_snow() == {}:
            bot.send_message(message.chat.id,'Снігу нема')
        else:
            bot.send_message(message.chat.id,'Сніг' + str(w.get_snow()))
        bot.send_message(message.chat.id,'Вітер ' + str(wind) + 'м/с')
        bot.send_message(message.chat.id,'Вологість ' + str(w.get_humidity()) + '%')
        bot.send_message(message.chat.id,'Тиск ' + str(int(press)) + ' мм. рт. ст.')


@bot.message_handler(content_types=['text'])
def text_handler(message):
    constants.log(message)
    request = apiai.ApiAI(constants.dialogapi).text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'BatlabAIBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = message.text # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        bot.reply_to(message, response)
    else:
        bot.reply_to(message, 'я не поняв')


bot.polling(none_stop=True)
