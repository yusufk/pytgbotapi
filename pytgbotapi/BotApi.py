import requests, json

class User:
    """User Object"""
    def __init__(self, userid, first_name, last_name, username):
        self.userid = userid
        self.first_name = first_name
        self.last_name = last_name
        self.username = username

class Update:
    """Update Object"""
    def __init__(self, update_id,message=None):
        self.update_id = update_id
        self.message = message

class Message:
    """Message Object"""
    def __init__(self, message_id, msg_from, msg_date, chat,**optional):
        self.message_id = message_id
        self.msg_from = msg_from
        self.msg_date = msg_date
        self.chat = chat
        self.text = optional.get('text',None)

class BotApi:
    """Factory Base Class """
    def __init__(self, token, **arg):
        self.arg = arg
        self.api_url = "https://api.telegram.org"
        self.token = token
        self.lastFetchedUpdate = 0

    def send_request(self,method,parameters=None):
        r = requests.post(self.api_url+"/bot"+self.token+"/"+method, parameters)#, data, auth=('user', '*****'))
        response = json.loads(r.text)
        return response['result']

    def getMe(self):
        me = self.send_request("getMe")
        print(me)
        return me

    def getUpdates(self,**parameters):
        updates = self.send_request("getUpdates",parameters)
        updateObjects=[]
        for update in updates:
            updateObject = Update(update["update_id"],update["message"])
            updateObjects.append(updateObject)
        return updateObjects

    def sendMessage(self,chat_id,text,**optional):
        parameters = {"chat_id":chat_id,"text":text}
        disable_web_page_preview=optional.get('disable_web_page_preview',None)
        reply_to_message_id=optional.get('reply_to_message_id',None)
        reply_markup=optional.get('reply_markup',None)
        if disable_web_page_preview != None: parameters.append({"disable_web_page_preview":disable_web_page_preview})
        if reply_to_message_id != None: parameters.append({"reply_to_message_id":reply_to_message_id})
        if reply_markup != None: parameters.append({"reply_markup":reply_markup})
        messageResponse = self.send_request("sendMessage",parameters)
