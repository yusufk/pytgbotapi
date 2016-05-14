import requests, json
from collections import namedtuple
from pprint import pprint
from twisted.application.internet import TCPServer
from twisted.application.service import Application
from twisted.web.resource import Resource
from twisted.web.server import Site


class WebHookHost(Resource):
    def __init__(self,listener):
        self.listener = listener
    def render_GET(self, request):
        return ''

    def render_POST(self, request):
        pprint(request.__dict__)
        newdata = request.content.getvalue()
        print newdata
        update = json.loads(newdata)
        updateObject = Update(update["update_id"],update["message"])
        self.listener.handle(updateObject)
        return ''

class User:
    """User Object"""
    def __init__(self, userid, first_name,last_name=None,username=None):
        self.userid = userid
        self.first_name = first_name
        self.last_name = last_name
        self.username = username

class Location:
    """Location Object"""
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

class Update:
    """Update Object"""
    def __init__(self, update_id,message=None):
        self.update_id = update_id
        if message != None:
            #print(message)
            self.message = Message(message_id=message['message_id'],msg_date=message['date'], chat=message['chat'], msg_from=message['from'])
            if "text" in message:
                self.message.set_text(message['text'])
            if "location" in message:
                self.message.set_location(message['location'])
        else: self.message = None

class Chat:
    """Chat Object"""
    def __init__(self, chat_id, chat_type, chat_title=None, chat_username=None, chat_first_name=None, chat_last_name=None):
        self.chat_id = chat_id
        self.chat_type = chat_type
        self.title = chat_title
        self.username = chat_username
        self.first_name = chat_first_name
        self.last_name = chat_last_name

    def set_title(self,title):
        self.title = title

    def set_username(self,username):
        self.username = username

class Message:
    """Message Object"""
    def __init__(self, message_id, msg_date, chat, msg_from=None,text=None,location=None):
        self.message_id = message_id
        #print(msg_from)i
        if msg_from != None:
            self.msg_from = User(msg_from['id'],msg_from['first_name'])
        self.msg_date = msg_date
        self.text = text
        if location != None:
            self.location = Location(location['longitude'],location['latitude'])
        else: self.location = None
        self.chat = Chat(chat['id'],chat['type'])
        if "title" in chat:
            self.chat.set_title(chat['title'])
        if "username" in chat:
            self.chat.set_username(chat['username'])

    def set_text(self,text):
        self.text = text

    def set_location(self,location):
        self.location = Location(location['longitude'],location['latitude'])

class BotApi:
    """Factory Base Class """
    def __init__(self, token, **arg):
        self.arg = arg
        self.api_url = "https://api.telegram.org"
        self.token = token
        self.lastFetchedUpdate = 0

    def send_request(self,method,parameters=None):
        #print(parameters)
        r = requests.post(self.api_url+"/bot"+self.token+"/"+method, parameters)#, data, auth=('user', '*****'))
        response = json.loads(r.text)
        if "result" in response:
            #print(response)
            return response['result']
        else:
            print(response)
            return None

    def getMe(self):
        me = self.send_request("getMe")
        #print(me)
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

    def startHost(self,listener,port=8880):
        root = Resource()
        root.putChild("form", WebHookHost(listener))
        application = Application("My Bot Service")
        TCPServer(port, Site(root)).setServiceParent(application)
