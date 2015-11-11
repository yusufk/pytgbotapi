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

class Update:
    """Update Object"""
    def __init__(self, update_id,message=None):
        self.update_id = update_id
        if message != None:
            #print(message)
            if "text" in message:
                self.message = Message(message['message_id'],message['from'],message['date'],message['chat'],text=message['text'])
            else: self.message = Message(message['message_id'],message['from'],message['date'],message['chat'])
        else: self.message = None

class Chat:
	"""Chat Object"""
	def __init__(self, msg_id, msg_type=None,**optional):
		self.msg_id = msg_id
		self.msg_type = msg_type
        self.title = optional.get('title',None)
        self.username = optional.get('username',None)

class Message:
    """Message Object"""

    def __init__(self, message_id=None, msg_from=None, msg_date=None, chat=None,**optional):
        self.message_id = message_id
        #print(msg_from)
        self.msg_from = User(msg_from['id'],msg_from['first_name'])
        self.msg_date = msg_date
        self.chat = Chat(chat['id'],chat['type'],title = chat['title'], username = chat['username']
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
        if "result" in response:
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
