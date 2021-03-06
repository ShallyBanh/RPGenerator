"""
In this file, the following requirements are covered:
REQ-3.1.3.5: Ruleset File Output
REQ-3.1.3.6: Ruleset Sharing
REQ-3.1.3.7: Remote Ruleset Storage
REQ-3.1.3.8: Ruleset Encryption
REQ-3.1.3.9: Ruleset Decryption
REQ-3.2.3.1: Engine Reads File
REQ-3.2.3.5: Request Action
REQ-3.2.3.6: Approve Action
REQ-3.2.3.10: Import visual assets
REQ-3.3.3.1: Account Creation
REQ-3.3.3.2: Credential Storage
REQ-3.3.3.3: Credential Modification
REQ-3.3.3.4: Credential Recovery
REQ-3.3.3.5: Login
REQ-3.4.3.1: Game Creation
REQ-3.6.3.1: Game History View
"""
import sys
import time
from flask import Flask, request, jsonify, Response
import status
import threading

from account.account_manager import AccountManager
import configparser
from configurator import Configurator
import network.email_sender
from cryptography.fernet import Fernet
import network.communications as communication 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
IP_ADDRESS = "0.0.0.0"
PORT = 5493
testkey = ""

class Server:
    """A User account.

    Attributes:
        name (str) -- User's name.

    """

    # @TODO database stuff

    def __init__(self, config_file="config.conf"):
        """Initialize a Server

        Keyword arguments:
            name (str) -- User's name
        """
        # if exists/None?
        
        self.configurator = Configurator("SERVER", config_file)
        self.config = self.configurator.config
        print("[server] self.config['database_file'] = {}".format(self.config["database_file"]))
        self.account_manager = AccountManager(self.config["database_file"])
        self.clients = []
        self.running = False

if len(sys.argv) > 2:
    print("creating server with config file {}".format(sys.argv[1]))
    testkey = sys.argv[1]
    server = Server(sys.argv[2])
elif len(sys.argv) > 1:
    testkey = sys.argv[1]
    server = Server()
else:
    server = Server()

testkey.encode('utf8')

@app.route("/login", methods=['POST'])
def login():
    username = request.args.get("username")
    password = request.args.get("password")
    if username is None or password is None:
        print("received NoneType\n\tusername ({}), password ({})".format(type(username), type(password)))
        return Response(status=400)
    print("[server] [login] got username,password = {},{}".format(username, password))
    response = server.account_manager.login(username, password)
    print("[server] [login] response from account_manager was {}".format(response))
    # @TODO assets if success?
    if response is not None:
        print("attempting to jsonify the response \n{}".format(response))
        return jsonify(username=response[0], email=response[2], assets={})
    else:
        return Response(status=400)
    # return "200" if (response == 0) else "400"

@app.route("/create_account", methods=['POST'])
def create_account():
    username = request.args.get("username")
    password = request.args.get("password")
    email = request.args.get("email")
    if username is None or password is None or email is None:
        return Response(status=400)
    print("[server] [create_account] got username,password,email = {},{},{}".format(username, password, email))
    response = server.account_manager.create_account(username, password, email)
    print("[server] [create_account] response from account_manager was {}".format(response))
    response_status = 200 if (response == 0) else 400
    return Response(status=response_status)

@app.route("/change_credentials", methods=['POST'])
def change_credentials():
    username = request.args.get("username")
    old_password = request.args.get("old_password")
    new_password = request.args.get("new_password")
    if username is None or old_password is None or new_password is None:
        return Response(status=400)
    print("[server] [change_credentials] got username,old_password,new_password= {},{},{}".format(username, old_password, new_password))
    old_credentials = server.account_manager.get_credentials(username)
    print("the old credentials are {}".format(old_credentials))
    if old_credentials is not None:
        print("[server] [change_credentials] comparing hashed passwords\n\t{}\n\t{}".format(old_credentials[1], server.account_manager.generate_hash(old_password, username)))
    if old_credentials is not None and old_credentials[1] == server.account_manager.generate_hash(old_password, username):
        server.account_manager.set_credentials(username, new_password)
        print("[server] [change_credentials] given were correct and not None query result")
        response_status = 200
    else:
        response_status = 400
    return Response(status=response_status)
    # print("[server] [change_credentials] response from account_manager was {}".format(response))
    # return "200" if (response == 0) else "400"

@app.route("/send_recovery", methods=['POST'])
def send_recovery():
    email = request.args.get("email")
    if email is None:
        return Response(status=400)
    print("\n[server] [send_recovery] got email = {}\n".format(email))
    response = server.account_manager.send_recovery(email)
    print("\n[server] [send_recovery] response from account_manager was {}\n".format(response))
    # @TODO maybe no response of success/fail?
    response_status = 200 if (response == 0) else 400
    return Response(status=response_status)

@app.route("/recover_account", methods=['POST'])
def recover_account():
    username = request.args.get("username")
    code = request.args.get("code")
    password1 = request.args.get("password1")
    password2 = request.args.get("password2")
    if username is None or code is None or password1 is None or password2 is None:
        return Response(status=400)
    print("[server] [recover_account] got username,code,password1,password2 = {},{},{},{}".format(username, code, password1, password2))
    response = server.account_manager.recover_account(username, code, password1, password2)
    print("[server] [recover_account] response from account_manager was {}".format(response))
    # @TODO maybe no response of success/fail?
    response_status = 200 if (response == 0) else 400
    return Response(status=response_status)

@app.route("/add_asset", methods=['POST'])
def add_asset():
    username = request.args.get("username")
    asset_name = request.args.get("asset_name")
    json_blob = request.args.get("json_blob")
    if username is None or asset_name is None or json_blob is None:
        return Response(status=400)
    print("[server] [add_asset] got username,asset_name,json_blob = {},{},json_blob size {}".format(username, asset_name, len(json_blob)))
    # print("[server] [add_asset] got username,asset_name,json_blob = {},{},{}".format(username, asset_name, json_blob))
    response = server.account_manager.add_asset(username, asset_name, json_blob)
    print("[server] [add_asset] response from account_manager was {}".format(response))
    response_status = 200 if (response == 0) else 400
    return Response(status=response_status)

@app.route("/get_asset", methods=['POST'])
def get_asset():
    username = request.args.get("username")
    asset_name = request.args.get("asset_name")
    if username is None or asset_name is None:
        return Response(status=400)
    print("[server] [get_asset] got username,asset_name = {},{}".format(username, asset_name))
    # print("[server] [get_asset] got username,asset_name,json_blob = {},{},{}".format(username, asset_name, json_blob))
    response = server.account_manager.get_asset(username, asset_name)
    # print("[server] [get_asset] response from account_manager was {}".format(response))
    response_status = 200 if (response) else 400
    return jsonify(assets=response)

@app.route("/get_assets", methods=['POST'])
def get_assets():
    username = request.args.get("username")
    if username is None:
        return Response(status=400)
    print("[server] [get_assets] got username = {}".format(username))
    # print("[server] [get_assets] got username,asset_name,json_blob = {},{},{}".format(username, asset_name, json_blob))
    response = server.account_manager.get_assets(username)
    # print("[server] [get_assets] response from account_manager was {}".format(response))
    response_status = 200 if (response) else 400
    return jsonify(assets=response)

@app.route("/reset_database", methods=['POST'])
def reset_database():
    """ WARNING: for test purposes only, @TODO remove """
    response = server.account_manager.reset_database()
    response_status = 200 if (response == 0) else 400
    return Response(status=response_status)

@app.route("/sql_debug", methods=['POST', 'GET'])
def sql_debug():
    """ WARNING: for test purposes only, @TODO remove """
    query = request.args.get("query")
    data = request.args.get("data")
    if data is None:
        data = ""
    server.account_manager.database.query(query, data)
    rows = server.account_manager.database.cur.fetchall()
    return jsonify(rows)

@app.route("/load_existing_rulesets", methods=['POST'])
def load_existing_rulesets():
    username = request.args.get("username")
    if username is None:
        return Response(status=400)
    print("[server] [load_existing_rulesets] got username = {}".format(username))
    response = server.account_manager.load_existing_rulesets(username)
    if response is not None:
        decryptedResponse = []
        #start decryption
        f = Fernet(testkey)
        for rulename, rulecontent in response:
            decryptedResponse.append((rulename, f.decrypt(rulecontent).decode("utf")))
        return jsonify(decryptedResponse)

    print("[server] [load_existing_rulesets] response from account_manager was {}".format(response))
    response_status = 200 if (response == 0) else 400
    return Response(status=response_status)

@app.route("/create_ruleset", methods=['POST'])
def create_ruleset():
    username = request.args.get("username")
    rulesetName = request.args.get("rulesetName")
    jsonBlob = request.args.get("jsonBlob")
    if username is None or rulesetName is None or jsonBlob is None:
        return Response(status=400)
    print("[server] [create_ruleset] got username,rulesetName,jsonBlob = {},{},{}".format(username, rulesetName, jsonBlob))
    #start encryption
    f = Fernet(testkey)
    response = server.account_manager.create_ruleset(username, rulesetName, f.encrypt(jsonBlob.encode('utf-8')))

    print("[server] [create_ruleset] response from account_manager was {}".format(response))
    response_status = 200 if (response == 0) else 400
    return Response(status=response_status)

@app.route("/update_ruleset", methods=['POST'])
def update_ruleset():
    username = request.args.get("username")
    rulesetName = request.args.get("rulesetName")
    jsonBlob = request.args.get("jsonBlob")
    if username is None or rulesetName is None or jsonBlob is None:
        return Response(status=400)
    print("[server] [update_ruleset] got username,rulesetName,jsonBlob = {},{},{}".format(username, rulesetName, jsonBlob))
    #start encryption
    f = Fernet(testkey)
    response = server.account_manager.update_ruleset(username, rulesetName, f.encrypt(jsonBlob.encode('utf-8')))

    print("[server] [update_ruleset] response from account_manager was {}".format(response))
    response_status = 200 if (response == 0) else 400
    return Response(status=response_status)

@app.route("/load_game_history", methods=['POST'])
def load_game_history():
    username = request.args.get("username")
    if username is None:
        return Response(status=400)
    print("[server] [load_game_history] got username = {}".format(username))
    response = server.account_manager.load_game_history(username)
    if response is not None:
        print(response)
        return jsonify(response)

    print("[server] [load_game_history] response from account_manager was {}".format(response))
    response_status = 200 if (response == 0) else 400
    return Response(status=response_status)

@app.route("/get_list_of_games_and_their_gms", methods=['POST'])
def get_list_of_games_and_their_gms():
    response = server.account_manager.get_list_of_games_and_their_gms()
    if response is not None:
        print(response)
        return jsonify(response)

    print("[server] [get_list_of_games_and_their_gms] response from account_manager was {}".format(response))
    response_status = 200 if (response == 0) else 400
    return Response(status=response_status)

@app.route("/get_game_from_room_number", methods=['POST'])
def get_game_from_room_number():
    gameId = request.args.get("gameId")
    if gameId is None:
        return Response(status=400)
    response = server.account_manager.get_game_from_room_number(gameId)
    if response is not None:
        print(response)
        return jsonify(response)

    print("[server] [get_game_from_room_number] response from account_manager was {}".format(response))
    response_status = 200 if (response == 0) else 400
    return Response(status=response_status)

@app.route("/get_game_id", methods=['POST'])
def get_game_id():
    username = request.args.get("username")
    if username is None:
        return Response(status=400)
    print("[server] [get_game_id] got username = {}".format(username))
    response = server.account_manager.get_game_id(username)
    if response is not None:
        print(response)
        return jsonify(response)

    print("[server] [get_game_id] response from account_manager was {}".format(response))
    response_status = 200 if (response == 0) else 400
    return Response(status=response_status)

@app.route("/create_game", methods=['POST'])
def create_game():
    gameBlob = request.args.get("gameBlob")
    gameName = request.args.get("gameName")
    userName = request.args.get("username")
    if gameBlob is None or gameName is None or userName is None:
        return Response(status=400)
    print("[server] [create_game] got gameBlob, gameName, username = {},{},{}".format(gameBlob, gameName, userName))
    response = server.account_manager.create_game(gameBlob, gameName, userName)
    print("[server] [create_game] response from account_manager was {}".format(response))
    response_status = 200 if (response == 0) else 400
    return Response(status=response_status)

@app.route("/get_game_history_from_id", methods=['POST'])
def get_game_history_from_id():
    username = request.args.get("username")
    gameid = request.args.get("gameid")
    if username is None or gameid is None:
        return Response(status=400)
    print("[server] [get_game_history_from_id] got username = {}".format(username))
    response = server.account_manager.get_game_history_from_id(gameid, username)
    if response is not None:
        print(response)
        return jsonify(response)

    print("[server] [get_game_history_from_id] response from account_manager was {}".format(response))
    response_status = 200 if (response == 0) else 400
    return Response(status=response_status)

@app.route("/create_game_history_entry", methods=['POST'])
def create_game_history_entry():
    gameName = request.args.get("gameName")
    username = request.args.get("username")
    gameid = request.args.get("gameid")
    if username is None or gameName is None or id is None:
        return Response(status=400)
    print("[server] [create_game_history_entry] got gameName, username, gameid = {},{},{}".format(gameName, username, gameid))
    response = server.account_manager.create_game_history_entry(gameName, username, gameid)
    print("[server] [create_game_history_entry] response from account_manager was {}".format(response))
    response_status = 200 if (response == 0) else 400
    return Response(status=response_status)

@app.route("/update_game", methods=['POST'])
def update_game():
    gameId = request.args.get("gameId")
    gameObj = request.args.get("gameObj")
    if gameId is None or gameObj is None:
        return Response(status=400)
    print("[server] [update_game] got gameId, gameObj= {}, {}".format(gameId, gameObj))
    #start encryption
    response = server.account_manager.update_game(gameId, gameObj)

    print("[server] [update_game] response from account_manager was {}".format(response))
    response_status = 200 if (response == 0) else 400
    return Response(status=response_status)
    
async_receive_thread = threading.Thread(target=communication.main)
async_receive_thread.start()
app.run(host=IP_ADDRESS, port=PORT, debug=False, use_reloader=False)
