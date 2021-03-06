"""
In this file, the following requirements are covered:
REQ-3.1.3.7: Remote Ruleset Storage
REQ-3.2.3.1: Engine Reads File
REQ-3.2.3.10: Import visual assets
REQ-3.3.3.1: Account Creation
REQ-3.3.3.2: Credential Storage
REQ-3.3.3.3: Credential Modification
REQ-3.3.3.4: Credential Recovery
REQ-3.3.3.5: Login
REQ-3.4.3.1: Game Creation
REQ-3.4.3.2: Join Request
REQ-3.6.3.1: Game History View
REQ-3.6.3.2: Resume Game Session
REQ-3.6.3.3: Game Role
"""

#!/usr/bin/env python3
import requests
from flask import jsonify
import json
from account.user import User
from game_engine.game import Game

class Client():

    def __init__(self, ip_address="0.0.0.0", port=5493, encoding="utf-8"):
        self.ip_address = ip_address
        self.port = port
        self.URL = "http://{}:{}".format(self.ip_address, self.port)
        self.encoding = "utf-8"
        self.user = None
        self.help = "Usage:"
        self.help += "\n\tlogin [username] [password]"
        self.help += "\n\tcreate_account [username] [password] [email]"
        self.help += "\n\tchange_credentials [username] [old_password] [new_password]"
        self.help += "\n\tsend_recovery [email]"
        self.help += "\n\trecover_account [username] [code] [new_password] [new_password]"
        self.help += "\n\nDebug commands (to be removed)"
        self.help += "\n\treset_database"
        self.help += "\n\tsql_debug [query]"
        self.help += "\n\tcreate_game"
        self.test_game = None

    def default(self, line):
        print("\"{0}\" is not one of the given commands. Type in 'help' for more options.".format(line))

    def login(self, username, password):
        print("[client] [login] attempting to login with username,password = {},{}".format(username,password))
        payload = {'username': username, 'password': password}
        response = requests.post("{}/login".format(self.URL), params=payload)
        # response = requests.get("{}/login/username={}?password={}".format(self.URL,username,password), params=payload)
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
        response = requests.post("{}/create_account".format(self.URL), params=payload)
        print("[client] [create_account] response was {}/{}/{}".format(response, response.status_code, response.text))       
        # @TODO why does this one end up a different type even though the code is exactly the same
        # if type(response) == requests.models.Response:
        #     response = str(response.text)
        return 0 if (response.status_code == 200) else -1
    
    def create_ruleset(self, username, rulesetName, jsonBlob):
        print("[client] [create_ruleset] attempting to create a ruleset with username,rulesetName,jsonBlob = {},{},{}".format(username,rulesetName,jsonBlob))        
        payload = {'username': username, 'rulesetName': rulesetName, 'jsonBlob': jsonBlob}
        response = requests.post("{}/create_ruleset".format(self.URL), params=payload)
        print("[client] [create_ruleset] response was {}/{}/{}".format(response, response.status_code, response.text))       
        return 0 if (response.status_code == 200) else -1

    def create_game_history_entry(self, gameName, userName, gameId):
        print("[client] [create_game_history_entry] attempting to create a ruleset with gameName,userName,gameId = {},{},{}".format(gameName, userName, gameId))        
        payload = {'gameName': gameName, 'username': userName, 'gameid': gameId}
        response = requests.post("{}/create_game_history_entry".format(self.URL), params=payload)
        print("[client] [create_game_history_entry] response was {}/{}/{}".format(response, response.status_code, response.text))       
        return 0 if (response.status_code == 200) else -1
    
    def update_ruleset(self, username, rulesetName, jsonBlob):
        print("[client] [update_ruleset] attempting to update a ruleset with username,rulesetName,jsonBlob = {},{},{}".format(username,rulesetName,jsonBlob))        
        payload = {'username': username, 'rulesetName': rulesetName, 'jsonBlob': jsonBlob}
        response = requests.post("{}/update_ruleset".format(self.URL), params=payload)
        print("[client] [update_ruleset] response was {}/{}/{}".format(response, response.status_code, response.text))       
        return 0 if (response.status_code == 200) else -1
    
    def change_credentials(self, username, old_password, new_password): #,email):
        print("[client] [change_credentials] attempting to change credentials of with username,old_password,new_password = {},{},{}".format(username,old_password, new_password))        
        payload = {'username': username, 'old_password': old_password, 'new_password': new_password}
        response = requests.post("{}/change_credentials".format(self.URL), params=payload)
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
        response = requests.post("{}/send_recovery".format(self.URL), params=payload)
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
        response = requests.post("{}/recover_account".format(self.URL), params=payload)
        print("[client] [recover_account] response was {}".format(response.status_code))
        # if type(response) == requests.models.Response:
        #     response = str(response.status_code)
        return 0 if (response.status_code == 200) else -1
        
    def add_asset(self, username, asset_name, json_blob):
        print("[client] [add asset] attempting to add asset with username,asset_name = {},{}".format(username,asset_name))        
        payload = {'username': username, 'asset_name': asset_name, 'json_blob': json_blob}
        response = requests.post("{}/add_asset".format(self.URL), params=payload)
        print("[client] [add asset] response was {}/{}/{}".format(response, response.status_code, response.text))       
        # @TODO why does this one end up a different type even though the code is exactly the same
        # if type(response) == requests.models.Response:
        #     response = str(response.text)
        return 0 if (response.status_code == 200) else -1

    def get_asset(self, username, asset_name):
        print("[client] [get_asset] attempting to get_asset with username,asset_name = {},{}".format(username, asset_name))        
        payload = {'username': username, 'asset_name': asset_name}
        response = requests.post("{}/get_asset".format(self.URL), params=payload)
        print("[client] [get_asset] response was {}/{}/{}".format(response, response.status_code, response.text))       
        # @TODO why does this one end up a different type even though the code is exactly the same
        # if type(response) == requests.models.Response:
        #     response = str(response.text)
        print("response.status_code: {} ({})".format(response.status_code, type(response.status_code)))
        if response.status_code == 200:
            data = json.loads(response.text)
            print("appending the asset name to return value in get_asset")
            asset_with_name = (asset_name, data['assets'])
            print("returning asset with name {}".format(asset_with_name[0]))
            return asset_with_name
        else:
            print("status was not 200")
            return -1

    def get_assets(self, username, asset_list):
        print("[client] [get_assets] getting {}'s assets {}".format(username, asset_list))
        assets = []
        for asset in asset_list:
            data = self.get_asset(username, asset)
            if data != -1:
                assets.append(data)
        print("returning the assets: {}".format(assets))
        return assets

        # payload = {'username': username}
        # response = requests.post("{}/get_assets".format(self.URL), params=payload)
        # # print("[client] [get_assets] response was {}/{}/{}".format(response, response.status_code, response.text))       
        # # @TODO why does this one end up a different type even though the code is exactly the same
        # # if type(response) == requests.models.Response:
        # #     response = str(response.text)
        # print("response.status_code: {} ({})".format(response.status_code, type(response.status_code)))
        # if response.status_code == 200:
        #     data = json.loads(response.text)
        #     return data['assets']
        # else:
        #     print("status was not 200")
        #     return -1

    def reset_database(self):
        """ WARNING: for test purposes only, @TODO remove """
        response = requests.post("{}/reset_database".format(self.URL))
        return 0 if (response.status_code == 200) else -1

    def sql_debug(self, query):
        """ WARNING: for test purposes only, @TODO remove """
        payload = {'query': query}
        response = requests.post("{}/sql_debug".format(self.URL), params=payload)
        data = json.loads(response.text)
        print("query resulted in: {}".format(data))
        if response.status_code == 400:
            return -1
        return data

    def load_existing_rulesets(self, username):
        print("[client] [load_existing_rulesets] attempting to load rulesets from user with username {}".format(username))        
        payload = {'username': username}
        header_content = {'Content-type': 'application/json'} 
        response = requests.post("{}/load_existing_rulesets".format(self.URL), headers=header_content, params=payload)
        data = json.loads(response.text)
        return data

    def load_game_history(self, username):
        print("[client] [load_game_history] attempting to load game history from user with username {}".format(username))        
        payload = {'username': username}
        header_content = {'Content-type': 'application/json'} 
        response = requests.post("{}/load_game_history".format(self.URL), headers=header_content, params=payload)
        data = json.loads(response.text)
        return data

    def create_game(self, gameBlob, gameName, username):
        """ WARNING: for test purposes only, @TODO remove """
        print("[client] [create_game] attempting to create a game with gameBlob, gameName, username = {},{},{}".format(gameBlob, gameName, username))        
        payload = {'gameBlob': gameBlob, 'gameName': gameName, 'username': username}
        response = requests.post("{}/create_game".format(self.URL), params=payload)
        print("[client] [create_game] response was {}/{}/{}".format(response, response.status_code, response.text))      
        return 0 if (response.status_code == 200) else -1
    
    def get_game_id(self, username):
        print("[client] [get_game_id] attempting to load game history from user with username {}".format(username))        
        payload = {'username': username}
        response = requests.post("{}/get_game_id".format(self.URL), params=payload)
        data = json.loads(response.text)
        return data

    def get_game_history_from_id(self, gameid, username):
        print("[client] [get_game_id] attempting to load game history from user with username, gameid {}, {}".format(username, gameid))        
        payload = {'username': username, 'gameid': gameid}
        response = requests.post("{}/get_game_history_from_id".format(self.URL), params=payload)
        data = json.loads(response.text)
        return data
    
    def get_list_of_games_and_their_gms(self):
        print("[client] [get_list_of_games_and_their_gms] attempting to get list of games and their gms")        
        response = requests.post("{}/get_list_of_games_and_their_gms".format(self.URL), params={})
        print(response.text)
        data = json.loads(response.text)
        return data

    def get_game_from_room_number(self, gameId):
        print("[client] [get_game_from_room_number] attempting to get a game blob from the {}".format(gameId))  
        payload = {'gameId': gameId}      
        response = requests.post("{}/get_game_from_room_number".format(self.URL), params=payload)
        data = json.loads(response.text)
        return data

    def update_game(self, gameId, gameObj):
        print("[client] [update_game] attempting to update a game with gameId= {}".format(gameId))        
        payload = {'gameId': gameId, 'gameObj': gameObj}
        response = requests.post("{}/update_game".format(self.URL), params=payload)
        print("[client] [update_game] response was {}/{}/{}".format(response, response.status_code, response.text))       
        return 0 if (response.status_code == 200) else -1
    

    # def create_game(self):
    #     """ WARNING: for test purposes only, @TODO remove """
    #     game = Game()
    #     game.set_players = []
    #     print(type(game))
    #     payload = {'query': "insert into game (game) values ('some game blob')"}
    #     response = requests.post("{}/sql_debug".format(self.URL), params=payload)
    #     data = json.loads(response.text)
    #     print("query resulted in: {}".format(data))
    #     retval = response
    #     payload = {'query': "select max(id) from game"}
    #     response = requests.post("{}/sql_debug".format(self.URL), params=payload)
    #     data = json.loads(response.text)
    #     print("query resulted in: {}".format(data))
    #     return 0 if (retval.status_code == 200) else -1

    def parse_command(self, command):
        # @TODO argparse/getops would be cleaner but is it worth it
        tokens = command.split()
        try:
            if tokens[0] == "login":
                if len(tokens) < 3:
                    raise ValueError("Incorrect number of args for {}".format(tokens[0]))                    
                self.login(tokens[1], tokens[2])
            elif tokens[0] == "create_account":
                if len(tokens) < 4:
                    raise ValueError("Incorrect number of args for {}".format(tokens[0]))
                self.create_account(tokens[1], tokens[2], tokens[3])
            elif tokens[0] == "change_credentials":
                if len(tokens) < 4:
                    raise ValueError("Incorrect number of args for {}".format(tokens[0]))
                self.change_credentials(tokens[1], tokens[2], tokens[3])
            elif tokens[0] == "send_recovery":
                if len(tokens) < 2:
                    raise ValueError("Incorrect number of args for {}".format(tokens[0]))
                self.send_recovery(tokens[1])
            elif tokens[0] == "recover_account":
                if len(tokens) < 5:
                    raise ValueError("Incorrect number of args for {}".format(tokens[0]))
                self.recover_account(tokens[1], tokens[2], tokens[3], tokens[4])
            elif tokens[0] == "reset_database":
                self.reset_database()
            elif tokens[0] == "sql_debug":
                if len(tokens) < 2:
                    raise ValueError("Incorrect number of args for {}".format(tokens[0]))
                query = " ".join(tokens[1:])
                self.sql_debug(query)
            elif tokens[0] == "create_game":
                # self.create_game()
                self.test_game = self.sql_debug("select game, max(id) from game")[0]
                print("test game is now {}".format(self.test_game))
            else:
                raise ValueError("Invalid command")
        except ValueError as error_msg:
            print(error_msg)
            print(self.help)

    def run(self):
        while True:
            command = input("client > ")
            print("the command was {}".format(command))
            if command:
                self.parse_command(command)

if __name__ == "__main__":
    client = Client()
    client.run()