import re
import time
import requests
import telebot

from telebot import types

token = '6952899655:AAFvqhb9Raoh81Lmco_jTaRXoIheA8O3Pg0'

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def main(message):
    users_data = requests.get(url='http://127.0.0.1:8000/api/users/')
    user_list = [users_id['user_id'] for users_id in users_data.json()]
    if message.from_user.id in user_list:
        user_state = get_user_state(message.from_user.id)
        markup = menu_button()
        if user_state['current_state'] == 'initial':
            bot.send_message(message.chat.id, 'Виберіть пункт меню', reply_markup=markup)
        elif user_state['current_state'] == 'crypto_info_menu':
            bot.register_next_step_handler(message, crypto_info_menu)

        elif user_state['current_state'] == 'menu_calculator':
            bot.register_next_step_handler(message, menu_calculator)
    else:
        bot.send_message(message.chat.id, "Введіть свій номер телефону для реєстрації: формат +380987654321 ")
        bot.register_next_step_handler(message, add_user)


def get_user_state(user_id):
    user_state_data = requests.get(url=f'http://127.0.0.1:8000/api/user_state/{user_id}/')
    return user_state_data.json()


"""  РЕЄСТРАЦІЯ  """


def is_valid_phone_number(phone_number):
    pattern = re.compile(r'^\+380\d{9}$')
    return bool(pattern.match(phone_number))


def add_user(message):
    if is_valid_phone_number(message.text):
        data = {
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'phone_number': message.text,
            'username': message.from_user.username,
            'user_id': message.from_user.id
        }
        response = requests.post(url='http://127.0.0.1:8000/api/users/', data=data)
        initial_state = {
            'current_state': 'initial',
            'user': response.json()['id']
        }

        requests.post(url=f'http://localhost:8000/api/users_state/', data=initial_state)
        markup = menu_button()
        bot.send_message(message.chat.id, 'Виберіть пункт меню', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Номер телефону не коректний. Спробуйте ще раз')
        bot.register_next_step_handler(message, add_user)

# ------------------------------------------------------------------------------------ #


def save_user_state(user_id, state_data):
    requests.put(url=f'http://127.0.0.1:8000/api/user_state/{user_id}/', data=state_data)


def menu_button():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    info = types.KeyboardButton('Інформація про криптовалюти')
    cal = types.KeyboardButton('Калькулятор обміну')
    markup.add(info, cal)
    return markup


@bot.message_handler(func=lambda message: message.text == "Інформація про криптовалюти")
def crypto_info_menu(message):
    user_state = get_user_state(message.from_user.id)
    updata_data = {
        'current_state': 'crypto_info_menu',
        'user': user_state['user'],
    }
    requests.put(url=f'http://127.0.0.1:8000/api/user_state/{message.from_user.id}/', data=updata_data)
    markup = types.InlineKeyboardMarkup(row_width=1)
    bitcoin_markup = types.InlineKeyboardButton("Bitcoin", callback_data="crypto_info_bitcoin")
    ethereum_markup = types.InlineKeyboardButton("Ethereum", callback_data="crypto_info_ethereum")
    litecoin_markup = types.InlineKeyboardButton("Litecoin", callback_data="crypto_info_litecoin")

    #Конпка для повернення в головне меню
    return_markup = types.InlineKeyboardButton("Повернутися в головне меню", callback_data='return_main_manu')

    markup.add(bitcoin_markup, ethereum_markup, litecoin_markup, return_markup)
    bot.send_message(message.chat.id, 'Виберіть криптовалюту:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('crypto_info_'))
def handler_cripto_info(call):
    crypto_symbol = call.data.split('_')[-1]
    crypto_info_text = take_crypto_info(crypto_symbol)
    bot.send_message(call.message.chat.id, crypto_info_text)


@bot.callback_query_handler(func=lambda call: call.data == 'return_main_manu')
def return_main_manu(call):
    markup = menu_button()
    user_state = get_user_state(call.from_user.id)
    updata_data = {
        'current_state': 'initial',
        'user': user_state['user'],
    }
    requests.put(url=f'http://127.0.0.1:8000/api/user_state/{call.from_user.id}/', data=updata_data)
    bot.send_message(call.message.chat.id, 'Виберіть пункт меню', reply_markup=markup)


def take_crypto_info(crypto):
    url = f'https://api.coingecko.com/api/v3/coins/{crypto}'
    response = requests.get(url)
    data = response.json()
    crypto_info_text = f"Name: {data['name']}\n" \
                       f"Symbol: {data['symbol']}\n" \
                       f"Exchange Rate (BTC to USD): {data['market_data']['current_price']['usd']}\n" \
                       f"Exchange Rate (USD to BTC): {format(1 / data['market_data']['current_price']['usd'], '.6f')}\n" \
                       f"High (24h): {data['market_data']['high_24h']['usd']}\n" \
                       f"Low (24h): {data['market_data']['low_24h']['usd']}\n" \
                       f"Available Supply: {data['market_data']['circulating_supply']}\n" \
                       f"Total Supply: {data['market_data']['total_supply']}"

    return crypto_info_text


@bot.message_handler(func=lambda message: message.text == "Калькулятор обміну")
def menu_calculator(message):
    user_state = get_user_state(message.from_user.id)
    updata_data = {
        'id': user_state['id'],
        'current_state': 'menu_calculator',
        'user': user_state['user'],
    }
    requests.put(url=f'http://127.0.0.1:8000/api/user_state/{message.from_user.id}/', data=updata_data)


    bot.send_message(message.chat.id, 'Введіть суму для конвертації: ')
    bot.register_next_step_handler(message, exchange_amount)


def exchange_amount(message):
    global amount
    try:
        amount = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, 'Невірний формат. Введіть суму')
        bot.register_next_step_handler(message, exchange_amount)
        return

    if amount > 0:
        murkap = types.InlineKeyboardMarkup(row_width=2)
        btc_usd_button = types.InlineKeyboardButton('BTC/USD', callback_data="bitcoin_usd")
        usd_btc_button = types.InlineKeyboardButton('USD/BTC', callback_data="usd_bitcoin")
        eth_usd_button = types.InlineKeyboardButton('ETH/USD', callback_data="ethereum_usd")
        usd_eth_button = types.InlineKeyboardButton('USD/ETH', callback_data="usd_ethereum")
        ltc_usd_button = types.InlineKeyboardButton('LTC/USD', callback_data="litecoin_usd")
        usd_ltc_button = types.InlineKeyboardButton('USD/LTC', callback_data="usd_litecoin")

        #Конпка для повернення в головне меню
        return_markup = types.InlineKeyboardButton("Повернутися в головне меню", callback_data='return_main_manu')
        murkap.add(btc_usd_button, usd_btc_button, eth_usd_button, usd_eth_button, ltc_usd_button, usd_ltc_button
                   , return_markup)
        bot.send_message(message.chat.id, 'Виберіть валюти для конвертації: ', reply_markup=murkap)

    else:
        bot.send_message(message.chat.id, 'Сума повинна бути більше нуля. Впишіть суму')
        bot.register_next_step_handler(message, exchange_amount)


@bot.callback_query_handler(func=lambda call: 'usd' in call.data)
def exchange_calculator(call):
    currency = call.data.split('_')
    if 'usd' == currency[1]:
        url = f'https://api.coingecko.com/api/v3/simple/price?ids={currency[0]}&vs_currencies=usd'
        response = requests.get(url)
        time.sleep(1)
        data = response.json()
        result = amount * data[currency[0]][currency[1]]
    else:
        url = f'https://api.coingecko.com/api/v3/simple/price?ids={currency[1]}&vs_currencies=usd'
        response = requests.get(url)
        data = response.json()
        result = amount * data[currency[1]][currency[0]]
        result = format(amount * (1 / data[currency[1]][currency[0]]), '.6f')

    bot.send_message(call.message.chat.id, result)


bot.polling(none_stop=True)

