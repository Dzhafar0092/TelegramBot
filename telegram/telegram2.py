import telebot
import requests
import json


Token = "5913638617:AAHc7iS100sBhlUkkXNmZ8zUutviWugV2Og"


exchanges = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB'}

bot = telebot.TeleBot(Token)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Привет! Я помогу тебе конвертировать валюту! Для ознакомления с возможными валютами нажмите /values"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "ВНИМАНИЕ: Напишите первую валюту, затем вторую валюту и сумму, которую хотите конвертировать! (введение через пробел!)\nДоступные валюты:"
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        quote, base, amount = message.text.split(' ')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={exchanges[quote]}&tsyms={exchanges[base]}')
        total_base = json.loads(r.content)[exchanges[base]]
        text = f'Цена {amount} {quote} в {base} - {total_base*int(amount)} {base}'
        bot.send_message(message.chat.id, text)
    except ValueError:
        bot.send_message(message.chat.id, "Введите команду правильно!")
    except KeyError:
        bot.send_message(message.chat.id, "Проверьте написание!")

bot.polling (non_stop=True)
