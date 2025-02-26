import os
import telebot
from flask import Flask, request

# Load Telegram bot token from environment variables
TOKEN = os.getenv("7310806246:AAFtzq-rFjCkTKS0hnhZvs7z4u2TJDNcaDM")
if not TOKEN:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN environment variable")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Webhook URL (Replace with your Render service URL)
WEBHOOK_URL = "https://your-render-service.onrender.com"

@app.route('/')
def home():
    return "Bot is running!"

# Set webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming Telegram messages via webhook"""
    if request.method == "POST":
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

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")  # Set Render webhook
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
