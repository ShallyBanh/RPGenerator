import requests
from flask import jsonify
import json
from account.user import User

class Client():

    def __init__(self, ip_address="0.0.0.0", port=5493, encoding="utf-8"):
        self.ip_address = ip_address
        self.port = port
        self.URL = "http://{}:{}".format(self.ip_address, self.port)
        self.encoding = "utf-8"
        self.user = None

    def default(self, line):
        print("\"{0}\" is not one of the given commands. Type in 'help' for more options.".format(line))

    def login(self, username, password):
        print("[client] [login] attempting to login with username,password = {},{}".format(username,password))
        payload = {'username': username, 'password': password}
        response = requests.post("{}/login".format(self.URL), params = payload)
        # response = requests.get("{}/login/username={}?password={}".format(self.URL,username,password), params = payload)
        print("[client] [login] response was \n{} ({})\n{}\n{}".format(response, type(response), response.status_code, response.text))       
        # @TODO why does this one end up a different type even though the code is exactly the same
        # if type(response) == requests.models.Response:
        #     response = str(response.text)
        # return response
        print("response.status_code: {} ({})".format(response.status_code, type(response.status_code)))
        if response.status_code == 200:
            print("got a successful response, trying to build user from \n{}\n({})".format(response.text, type(response.text)))
            # response
            data = json.loads(response.text)
            print("the data is now {}".format(data))
            self.user = User(data["username"], data["email"], data["assets"], None)
            print("self.user is now {}".format(self.user))
            return 0
        else:
            print("status was not 200")
            return -1
        # return 0 if (response == "200") else -1

    def create_account(self, username, password, email):
        print("[client] [create_account] attempting to create account with username,password,email = {},{},{}".format(username,password,email))        
        payload = {'username': username, 'password': password, 'email': email}
        response = requests.post("{}/create_account".format(self.URL), params = payload)
        print("[client] [create_account] response was {}/{}/{}".format(response, response.status_code, response.text))       
        # @TODO why does this one end up a different type even though the code is exactly the same
        # if type(response) == requests.models.Response:
        #     response = str(response.text)
        return 0 if (response.status_code == 200) else -1
    
    def change_credentials(self, username, old_password, new_password): #,email):
        print("[client] [change_credentials] attempting to change credentials of with username,old_password,new_password = {},{},{}".format(username,old_password, new_password))        
        payload = {'username': username, 'old_password': old_password, 'new_password': new_password}
        response = requests.post("{}/change_credentials".format(self.URL), params = payload)
        print("[client] [change_credentials] response was {}/{}/{}".format(response, response.status_code, response.text))       
        # @TODO why does this one end up a different type even though the code is exactly the same
        # if type(response) == requests.models.Response:
        #     response = str(response.text)
        # if response.status_code == 200:
            # self.user.password
        return 0 if (response.status_code == 200) else -1

    def send_recovery(self, email):
        print("[client] [send_recovery] attempting to send recovery to email = {}".format(email))
        payload = {'email': email}
        response = requests.post("{}/send_recovery".format(self.URL), params = payload)
        print("[client] [send_recovery] response was {}/{}/{}".format(response, response.status_code, response.text))       
        print("send recovery type {}".format(type(response)))
        # if type(response) == requests.models.Response:
        #     print("converting response type")
        #     response = str(response.text) 
        #     print("response type converted, new response is {} ({})".format(response, type(response)))
        return 0 if (response.status_code == 200) else -1
        
    def recover_account(self, username, code, password1, password2):
        print("[client] [recover_account] attempting to recover account with username,code,password,email = {}, {}, {}"
              .format(username, code, password1))        
        payload = {'username': username, 'code': code, 'password1': password1, 'password2': password2}
        response = requests.post("{}/recover_account".format(self.URL), params = payload)
        print("[client] [recover_account] response was {}".format(response.status_code))
        # if type(response) == requests.models.Response:
        #     response = str(response.status_code)
        return 0 if (response.status_code == 200) else -1
        
    def reset_database(self):
        """ WARNING: for test purposes only, @TODO remove """
        response = requests.post("{}/reset_database".format(self.URL))
        return 0 if (response.status_code == 200) else -1

if __name__ == "__main__":
    client = Client()
    client.login("user1", "pass1")
    client.create_account("user1", "password", "thomas.tetz@gmail.com")
    client.login("user1", "password")

    # client.send_recovery("thomas.tetz@gmail.com")
    # code = input("code: ")
    # client.recover_account("user1", code, "newpass", "newpass")
    # client.login("user1", "newpass")