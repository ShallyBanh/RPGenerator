"""This module contains the Server class."""
import sys
from flask import Flask, request
import status
from flask import Flask, render_template, request
import threading
import time


from Account.AccountManager import AccountManager
import constants
import configparser
from configurator import Configurator
import network.connection_manager
import network.email_sender

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
IP_ADDRESS = "localhost"
PORT = 5493

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

    def process_command(self, request):
        print("\n\n--- Server processing a command --- \n\n")
        if request[0] == constants.RQST_HANDSHAKE:
            print("handshake")
        elif request[0] == constants.RQST_LOGIN:
            print("login with credentials {0}, {1}".format(request[1], request[2]))
            return server.account_manager.login(request[1], request[2])

        elif request[0] == constants.RQST_ADD_USER:
            print("add user")
        elif request[0] == constants.RQST_UPDATE_USER:
            print("update user")
        elif request[0] == constants.RQST_SEND_RECOVERY:
            print("send recovery")
        elif request[0] == constants.RQST_RECOVER:
            print("recover user")
        elif request[0] == constants.RQST_LOGIN:
            print("new game")
        elif request[0] == constants.RQST_LOGIN:
            print("resume game")
        elif request[0] == constants.RQST_LOGIN:
            print("")
        else:
            print("request other")
    def dummy_func(self):
        print("\n\n can you call these \n\n")

    def process_connections(self):
        return
    
    # @app.route("/something", methods=['GET'])
    # def internal_flask_method():
    #     print("called inside class")
    #     return "did something", 201

if len(sys.argv) > 1:
    print("creating server with config file {}".format(sys.argv[1]))
    server = Server(sys.argv[1])
else:
    server = Server()

@app.route("/login", methods=['POST'])
def login():
    username = request.args.get("username")
    password = request.args.get("password")
    print("[server] [login] got username,password = {},{}".format(username, password))
    response = server.account_manager.login(username, password)
    print("[server] [login] response from account_manager was {}".format(response))
    # @TODO assets if success?
    return "200" if (response == 0) else "400"

@app.route("/create_account", methods=['POST'])
def create_account():
    username = request.args.get("username")
    password = request.args.get("password")
    email = request.args.get("email")
    print("[server] [create_account] got username,password,email = {},{},{}".format(username, password, email))
    response = server.account_manager.create_account(username, password, email)
    print("[server] [create_account] response from account_manager was {}".format(response))
    return "200" if (response == 0) else "400"

@app.route("/send_recovery", methods=['POST'])
def send_recovery():
    email = request.args.get("email")
    print("\n[server] [send_recovery] got email = {}\n".format(email))
    response = server.account_manager.send_recovery(email)
    print("\n[server] [send_recovery] response from account_manager was {}\n".format(response))
    # @TODO maybe no response of success/fail?
    return "200" if (response == 0) else "400"

@app.route("/recover_account", methods=['POST'])
def recover_account():
    username = request.args.get("username")
    code = request.args.get("code")
    password1 = request.args.get("password1")
    password2 = request.args.get("password2")
    print("[server] [recover_account] got username,code,password1,password2 = {},{},{},{}".format(username, code, password1, password2))
    response = server.account_manager.recover_account(username, code, password1, password2)
    print("[server] [recover_account] response from account_manager was {}".format(response))
    # @TODO maybe no response of success/fail?
    return "200" if (response == 0) else "400"

@app.route("/reset_database", methods=['POST'])
def reset_database():
    """ WARNING: for test purposes only, @TODO remove """
    response = server.account_manager.reset_database()
    return "200" if (response == 0) else "400"

app.run(host=IP_ADDRESS, port=PORT, debug=False, use_reloader=False)
