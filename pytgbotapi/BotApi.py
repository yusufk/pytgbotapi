import requests, json

class User:
    """User Object"""
    def __init__(self, userid, first_name,**optional):
        self.userid = userid
        self.first_name = first_name
        #self.last_name = last_name
        #self.username = username

class Update:
    """Update Object"""
    def __init__(self, update_id,message=None):
        self.update_id = update_id
        self.message = Message(message['message_id'],message['from'],message['date'],message['chat'])

class Message:
    """Message Object"""

    def __init__(self, message_id=None, msg_from=None, msg_date=None, chat=None,**optional):
        self.message_id = message_id
        print(msg_from)
        self.msg_from = User(msg_from['id'],msg_from['first_name'])
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

    def getUpdates(self,**optional):
        updates = self.send_request("getUpdates",optional)
        updateObjects=[]
        for update in updates:
            updateObject = Update(update["update_id"],update["message"])
            updateObjects.append(updateObject)
            self.lastFetchedUpdate = updateObject.update_id
        return updateObjects

    def sendMessage(self,chat_id,text,**optional):
        parameters = {"chat_id":chat_id,"text":text}
        parameters.update(optional)
        messageResponse = self.send_request("sendMessage",parameters)

    def getLastFetchedId(self):
        return self.lastFetchedUpdate
