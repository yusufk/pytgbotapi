from BotApi import BotApi

def main():
    print("Starting...")
    bot = BotApi("111111111:AAAAAAaJrJrJebfRF55njXPn5rxTfSD3Y90")
    print(bot.getMe())
    updates = bot.getUpdates(offset=bot.getLastFetchedId()+1)
    for update in updates:
        if update.message.chat != None:
            print(str(update.message.chat.chat_id ))
            #bot.sendMessage(str(update.message.msg_from.userid),"Hello World")
if __name__ == "__main__":
    main()
