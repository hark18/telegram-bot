import os
import telebot
import requests  # <-- Added missing import
from flask import Flask, request

# Load Telegram bot token from environment variables
TOKEN = "7310806246:AAFtzq-rFjCkTKS0hnhZvs7z4u2TJDNcaDM"
if not TOKEN:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN environment variable")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Webhook URL (Replace with your actual Render service URL)
WEBHOOK_URL = "https://your-render-service.onrender.com"

@app.route('/')
def home():
    return "Bot is running!"

# Webhook route
@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming Telegram messages via webhook"""
    update = request.get_json()
    if update:
        bot.process_new_updates([telebot.types.Update.de_json(update)])
    return "OK", 200

# Start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello! I am your Telegram bot, running on Render.")

# Echo function (Avoids reply-to errors)
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    try:
        bot.send_message(message.chat.id, message.text)
    except telebot.apihelper.ApiTelegramException:
        bot.send_message(message.chat.id, "Sorry, I couldn't reply!")

# Webhook Setup
with app.app_context():
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")

# Function to send messages to Telegram
def post_to_telegram(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, params=params)
    return response.json()

# Example Usage
telegram_response = post_to_telegram("your_bot_token", "your_chat_id", "Hello, Telegram!")

# Gunicorn does NOT need app.run()
if __name__ == "__main__":
    pass  # <-- Keeping this for Gunicorn deployment
