import requests, json

class BotApi:
    """Factory Base Class """
    def __init__(self, token, **arg):
        self.arg = arg
        self.api_url = "https://api.telegram.org"
        self.bot_name = "nokita_bot"
        self.token = token
        self.lastFetchedUpdate = 0

    def send_request(self,method,parameters):
        r = requests.post(self.api_url+"/bot"+self.token+"/"+method, parameters)#, data, auth=('user', '*****'))
        response = json.loads(r.text)
        return response['result']

    def getUpdates(self,**parameters):
        updates = self.send_request("getUpdates",parameters)
        for update in updates:
            print(update['update_id'])
        return updates
