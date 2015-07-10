from BotApi import BotApi

def main():
    print("Starting...")
    bot = BotApi("47745865:AAFgsfC2QWsmRNEFYJ3EZPTgBLGrhMMOTCQ")
    print(bot.getMe())
    updates = bot.getUpdates(offset=bot.getLastFetchedId()+1)
    updates = bot.getUpdates(offset=bot.getLastFetchedId()+1)
    for update in updates:
        if update.message.msg_from != None:
            print(str(update.update_id)+": "+str(update.message.msg_from.userid)+": "+update.message.text)
            bot.sendMessage(str(update.message.msg_from.userid),"Hello World")
if __name__ == "__main__":
    main()
