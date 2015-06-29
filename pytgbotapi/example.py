from BotApi import BotApi

def main():
    print("Starting...")
    bot = BotApi("1234567:DSGDFGFDGFDwegregerberEBFGBFGBGB")
    print(bot.getMe())
    updates = bot.getUpdates(offset=bot.getLastFetchedId()+1)
    while len(updates)>0:
        updates = bot.getUpdates(offset=bot.getLastFetchedId()+1)
        for update in updates:
            print(str(update.update_id)+": "+update.message.msg_from.username+": "+update.message.text)
    bot.sendMessage(11111111,"Hello World")
if __name__ == "__main__":
    main()
