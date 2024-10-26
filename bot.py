import telebot  
from telebot import types  
from logic import CityGame  

API_TOKEN = ''  

bot = telebot.TeleBot(API_TOKEN)  
  
games = {}  

@bot.message_handler(commands=['start'])  
def start_game(message):  
    chat_id = message.chat.id  
    game = CityGame()  
    games[chat_id] = game  
    bot.send_message(chat_id, "Игра началась! Назовите город:")  

@bot.message_handler(func=lambda message: True)  
def handle_message(message):  
    chat_id = message.chat.id  
    game = games.get(chat_id)  

    if not game:  
        bot.send_message(chat_id, "Пожалуйста, начните игру с командой /start")  
        return  

    player_city = message.text  
    game.used_cities.add(player_city)  

    bot_city = game.get_city(player_city)  
    if bot_city:  
        bot.send_message(chat_id, f"Бот называет город: {bot_city}")  
    else:  
        bot.send_message(chat_id, "Бот не может назвать город. Вы выиграли!")  
        game.close()  
        del games[chat_id]  

@bot.message_handler(func=lambda message: False)  
def unknown_command(message):  
    bot.reply_to(message, "Неизвестная команда. Используйте /start для начала игры.")  

if __name__ == '__main__':  
    bot.polling(none_stop=True)