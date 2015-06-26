# pytgbotapi
A python implementation of the Telegram Bot API - https://core.telegram.org/bots/api

Please feel free to contribute!

Example usage:

from BotApi import BotApi

def main():
    print("Starting...")
    bot = BotApi("123456:AAaaaabbbbcccddddddEEEEEfffffGGggghhh")
    print(bot.getMe())
    for update in bot.getUpdates():
        print(update.update_id)

if __name__ == "__main__":
    main()

