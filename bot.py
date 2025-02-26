import os
import telebot
from flask import Flask

# Get Telegram bot token from environment variables
TOKEN = "7310806246:AAFtzq-rFjCkTKS0hnhZvs7z4u2TJDNcaDM"
if not TOKEN:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN environment variable")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Basic start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I am your Telegram bot, running on Render.")

# Echo function (repeats messages)
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

# Flask route to keep Render service alive
@app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    bot.polling(none_stop=True)
