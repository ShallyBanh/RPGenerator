"""This module contains the Server class."""
import sys
import time
from flask import Flask, request, jsonify, Response
import status

from account.account_manager import AccountManager
import configparser
from configurator import Configurator
import network.email_sender

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
IP_ADDRESS = "0.0.0.0"
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

if len(sys.argv) > 1:
    print("creating server with config file {}".format(sys.argv[1]))
    server = Server(sys.argv[1])
else:
    server = Server()

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
    server.account_manager.database.query(query, "")
    rows = server.account_manager.database.cur.fetchall()
    return jsonify(rows)
    
app.run(host=IP_ADDRESS, port=PORT, debug=False, use_reloader=False)
