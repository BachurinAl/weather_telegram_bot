import telebot
from telebot import types
import requests
import json
from datetime import datetime
import locale



locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
bot = telebot.TeleBot('6269453155:AAH-OydCWcs6gQTrW2MqXlhljBTRb7kpFdU')
API = '91fe06d48438475065d56d66515c1012'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'{message.from_user.first_name}, напиши мне название нужного города...')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Если есть пожелания, то напиши сюда \U0001F449 <a href="@Bachurin_A">@Bachurin_A</a>', parse_mode='html')

@bot.message_handler(commands=['site'])
def site(message):
    bot.send_message(message.chat.id, 'Для ознакомления с проектами разработчика переходи по ссылке <a href="https://github.com/BachurinAl">https://github.com/BachurinAl</a>', parse_mode='html')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Перейти на сайт', url='https://github.com/BachurinAl'))
    emoji = {
        "Clear": "\U00002600 Ясно",
        "Clouds": "\U00002601 Облачно",
        "Rain": "\U00002614 Дождь",
        "Drizzle": "\U00002614 Дождь",
        "Thunderstorm": "\U000026A1 Гроза",
        "Snow": "\U0001F328 Снег",
        "Mist": "\U0001F32B Туман"
    }
    try:
        city = message.text.strip().title()
        res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
        data = json.loads(res.text)
        cur_weather = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        weather_description = data["weather"][0]["main"]
        if weather_description in emoji:
            wd = emoji[weather_description]
        else:
            wd = 'Посмотри в окно, не понимаю какая там погода'
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M:%S")
        sunset_timestamp = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M:%S")
        length_of_the_day = datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.fromtimestamp(data["sys"]["sunrise"])
        bot.send_message(message.chat.id, f'<b>Привет, {message.from_user.first_name}!</b> \U0001F44B\n{datetime.now().strftime("%d.%m.%Y %H:%M (%A)")}\n'
                                          f'Погода в городе на сегодня: {city}\n\n'
                                          f'<b>Температура сейчас: {cur_weather}°C</b>\n{wd} \nОщущается как {feels_like}°C\n\n<b>Подробности:</b>\n'
                                          f'\U0001F4A7 Влажность: {humidity}%\n\U0001F3E7 Давление: {pressure} мм рт.ст.\n'
                                          f'\U0001F32C Скорость ветра: {wind} м/c\n\U0001F307 Восход солнца: {sunrise_timestamp}\n'
                                          f'\U0001F306 Закат солнца: {sunset_timestamp}\n\U0001F505 Продолжительность дня: {length_of_the_day}\n\n'
                                          f'<b>Хорошего дня!</b> \U0001F44D', reply_markup=markup, parse_mode='html')
    except KeyError:
        bot.reply_to(message, 'Не знаю такой город, проверьте название', reply_markup=markup)

bot.polling(none_stop=True)



