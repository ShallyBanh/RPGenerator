# Import pygame and libraries
import sys
import os
import pygame
from pygame.locals import *
from random import randrange
import os
import pygame_textinput
import threading
import time
import select
import socket
import pickle
from client import Client
import ptext
sys.path.append('rule_interpreter/')
sys.path.append('rule_interpreter/models')
from rule_interpreter.models import *
from rule_interpreter.ruleset_view import RulesetView
from game_engine.game_history_view.game_history_view import GameHistoryView
from game_engine.game import Game


# Import pygameMenu
import pygameMenu
from pygameMenu.locals import *
# PYGAMEMENU_TEXT_NEWLINE

# Global variables
DIFFICULTY = ['EASY']
ABOUT = ['RPGenerator {0}'.format("V1.0.0"),
         'Author: {0}'.format("2019-Group-04")]
# COLOR_BACKGROUND = (128, 0, 128)
COLOR_BACKGROUND = (0,50,50)  
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
FPS = 60.0
MENU_BACKGROUND_COLOR = (228, 55, 36)
WINDOW_SIZE = (800, 600)
MY_FONT = pygame.font.Font(pygameMenu.fonts.FONT_FRANCHISE, 40)
BUFFERSIZE = 2048
client_id = None
current_game = None
# -----------------------------------------------------------------------------
# Init pygame
pygame.init()
client = Client()
os.environ['SDL_VIDEO_CENTERED'] = '1'
currentUsername = ""
async_transcript = ""

# Create pygame screen and objects
surface = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('RPGenerator')
clock = pygame.time.Clock()
dt = 1 / FPS

# Asynchronous communication setup
general_async_port = 4321
voice_async_port = 4322
serverAddr = '127.0.0.1'
if len(sys.argv) == 2:
    serverAddr = sys.argv[1]
general_async_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
general_async_connection.connect((serverAddr, general_async_port))

# voice_async_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# voice_async_connection.bind((serverAddr, voice_async_port))

# -----------------------------------------------------------------------------
# ASYNCHRONOUS COMMUNICATION FUNCTIONS
def async_send(async_message):
    global client_id
    global voice_async_port
    global serverAddr
    print("going to send async message {}".format(async_message))
    general_async_connection.send(pickle.dumps(async_message))
    print("sent async message")
    # register_command = ['register_client']

def async_command_loop():
    global client_id
    global async_transcript
    while True:
    # ge = ['position update', playerid, cc.x, cc.y]
        command = input("async command > ")
        if command:
            command = command.split()
            # print("the client id is {}".format(client_id))
            # async_message = ['chat', "client {} sending".format(client_id)]
            async_message = [command[0], " ".join(command[1:])]
            if command[0] == 'start_game':
                async_message = [command[0], [command[1], command[2]]]
                # async_transcript += "{} has left the game".format(client.user.get_username) + "\n"
            async_send(async_message)
            
            # async_voice = ['voice', "this should be voice data from client {}".format(client_id)]
            # print("-trying to send voice data-")
            # voice_async_connection.sendto(pickle.dumps(async_voice), (serverAddr, voice_async_port))
            # time.sleep(2)

def async_receive():
    global async_transcript
    global client_id
    global current_game    
    while True:
        ins, outs, ex = select.select([general_async_connection], [], [], 0)
        # ins, outs, ex = select.select([general_async_connection, voice_async_connection], [], [], 0)
        for inm in ins: 
            # how do you know which one was chosen? if equal probably
            print("selected was: {}".format(inm))
            if inm == general_async_connection:
                print("equal to general connection")
                async_message = pickle.loads(inm.recv(BUFFERSIZE))
                print("the async message is {}".format(async_message))
                message_type = async_message[0]
                message_content = async_message[1]
            # elif inm == voice_async_connection:
            #     print("equal to voice connection")
            #     async_message = pickle.loads(inm.recvfrom(BUFFERSIZE))
            else:
                print("connection equality check did not work")
                continue
            
            print("recieved something via select!")
            if message_type == 'assign_id':
                print("assigning client_id")
                client_id = message_content
                print("client_id is now {}".format(client_id))
                # inm.send(pickle.dumps(['register_username', client.user.get_username]))
            elif message_type == 'id update':
                    print("was id update")
            elif message_type == 'start_game_accept':
                print("game successfully started, update your game object and loop")
            elif message_type == 'start_game_reject':
                print("failed to start game")
            elif message_type == "join_request":
                answer = input("join request from {}\ny/n?".format(message_content[0][1]))
                if answer.lower() in ["y", "yes"]:
                    async_send(['accept_join', message_content])
                else:
                    async_send(['reject_join', message_content])
            elif message_type == 'join_accept':
                print("join request accepted!")
                print("@TODO update game object")
            elif message_type == 'join_invalid':
                print("there is no active game with that id")
            elif message_type == 'join_reject':
                # get the game
                print("join request rejected")
                # async_message.pop(0)
                # minions = []
                # for minion in async_message:
                #     if minion[0] != playerid:
                #         minions.append(Minion(minion[1], minion[2], minion[0]))

# -----------------------------------------------------------------------------
# VIEW FUNCTIONS
def account_login_view():
    """
    Login game function
    
    :return: None
    """
    
    # Reset main menu and disable
    # You also can set another menu, like a 'pause menu', or just use the same
    # main_menu as the menu that will check all your input.
    main_menu.disable()
    main_menu.reset(1)

    username = pygame_textinput.TextInput()
    password = pygame_textinput.TextInput()
    login_view = pygame.image.load("images/menu/login-copy.png")
    surface.fill(COLOR_BACKGROUND)
    global currentUsername


    selected = "username"
    
    while True:
        # Clock tick
        clock.tick(30)

        # Application events
        playevents = pygame.event.get()

        for e in playevents:
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE and main_menu.is_disabled():
                    main_menu.enable()
                    # Pass events to main_menu
                    main_menu.mainloop(playevents)
                    # Quit this function, then skip to loop of main-menu on line 217
                    return
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)
                if mouse_pos[0] in range(190,610) and mouse_pos[1] in range(148,210):
                    selected = "username"
                elif mouse_pos[0] in range(190,610) and mouse_pos[1] in range(266,322):
                    selected = "password"
                elif mouse_pos[0] in range(300,530) and mouse_pos[1] in range(517,530):
                    # create an account screen
                    create_new_account_view()
                    return
                elif mouse_pos[0] in range(335,480) and mouse_pos[1] in range(360,375):
                    # forget your password screen
                    forgot_password_view()
                    return
                elif mouse_pos[0] in range(320,482) and mouse_pos[1] in range(477,490):
                    # change your account info screen
                    update_account_view()
                    return
                elif mouse_pos[0] in range(186,612) and mouse_pos[1] in range(400,450):
                    # login
                    if len(username.get_text()) < 1 or len(password.get_text()) < 1:
                        break
                    success = login(username = username.get_text(), password = password.get_text())
                    if success == 0:
                        global client_id
                        currentUsername = username.get_text()
                        async_send(['register_username', [client_id, currentUsername]])
                        option_menu.enable()
                        option_menu.mainloop(playevents)
                        return
                    else:
                        ptext.draw("Error occured during login.", (162, 10), sysfontname="arial", color=COLOR_RED, fontsize=35)
                elif mouse_pos[0] in range(562,617) and mouse_pos[1] in range(62,77):
                    # go back
                    main_menu.enable()
                    main_menu.mainloop(playevents)
                    return
                # continue to make the rest of the buttons connect to different places
                # elif e.key != K_ESCAPE and main_menu.is_disabled():
                #     # Feed it with events every frame
                      
                # elif e.key == K_RETURN and main_menu.is_disabled():
                #     surface.fill(COLOR_BACKGROUND)

        
        if selected == "username":
            username.update(playevents)   
        elif selected == "password":
            password.update(playevents, passProtect=True)
            
        # blit information to the menu based on user input from above
        surface.blit(login_view, ((WINDOW_SIZE[0] - login_view.get_size()[0]) / 2, (WINDOW_SIZE[1] - login_view.get_size()[1]) / 2))
        if len(username.get_text()) >= 1:
            surface.blit(username.get_surface(), (250,170))  
        else:
            surface.blit(MY_FONT.render('Username', 1, COLOR_BLACK), (250,160))  
        if len(password.get_text()) >= 1:
            surface.blit(password.get_surface(), (250,290))
        else:
            surface.blit(MY_FONT.render('Password', 1, COLOR_BLACK), (250,280))  

        pygame.display.flip()

    return

def create_new_account_view():
    """
    Create new account game function
    
    :return: None
    """

    email = pygame_textinput.TextInput()
    username = pygame_textinput.TextInput()
    password1 = pygame_textinput.TextInput()
    password2 = pygame_textinput.TextInput()

    login_view = pygame.image.load("images/menu/create-account.png")
    surface.fill(COLOR_BACKGROUND)

    selected = "email"
    displayNotMatching = False
    errorTime = 0
    surfaceCopy = None
    
    while True:
        # Clock tick
        clock.tick(60)

        # Application events
        playevents = pygame.event.get()

        for e in playevents:
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE and main_menu.is_disabled():
                    account_login_view()
                    return
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)
                if mouse_pos[0] in range(190,610) and mouse_pos[1] in range(148,210):
                    selected = "email"
                elif mouse_pos[0] in range(190,610) and mouse_pos[1] in range(235,298):
                    selected = "username"
                elif mouse_pos[0] in range(190,610) and mouse_pos[1] in range(320,385):
                    selected = "password1"
                elif mouse_pos[0] in range(190,610) and mouse_pos[1] in range(403,470):
                    selected = "password2"
                elif mouse_pos[0] in range(186,612) and mouse_pos[1] in range(483,535):
                    # account creation
                    if len(email.get_text()) < 1 or len(username.get_text()) < 1 or len(password1.get_text()) < 1 or len(password2.get_text()) < 1:
                        break
                    if password1.get_text() == password2.get_text():
                        success = login(username = username.get_text(), email = email.get_text(), password = password1.get_text())
                        if success == 0:
                            return
                        else:
                            ptext.draw("Error occured during account creation.", (162, 10), sysfontname="arial", color=COLOR_RED, fontsize=35)
                    else:
                        displayNotMatching = True
                        errorTime = clock.get_time()
                        surfaceCopy = surface.copy()
                elif mouse_pos[0] in range(562,617) and mouse_pos[1] in range(62,77):
                    # go back
                    account_login_view()
                    return
        
        if selected == "email":
            email.update(playevents)   
        elif selected == "username":
            username.update(playevents)   
        elif selected == "password1":
            password1.update(playevents, passProtect=True)
        elif selected == "password2":
            password2.update(playevents, passProtect=True)
            
        # blit information to the menu based on user input from above
        surface.blit(login_view, ((WINDOW_SIZE[0] - login_view.get_size()[0]) / 2, (WINDOW_SIZE[1] - login_view.get_size()[1]) / 2))
        if len(email.get_text()) >= 1:
            surface.blit(email.get_surface(), (250,170))  
        else:
            surface.blit(MY_FONT.render('Email', 1, COLOR_BLACK), (250,160))  
        if len(username.get_text()) >= 1:
            surface.blit(username.get_surface(), (250,257))  
        else:
            surface.blit(MY_FONT.render('Username', 1, COLOR_BLACK), (250,247))  
        if len(password1.get_text()) >= 1:
            surface.blit(password1.get_surface(), (250,352))
        else:
            surface.blit(MY_FONT.render('Password', 1, COLOR_BLACK), (250,342))  
        if len(password2.get_text()) >= 1:
            surface.blit(password2.get_surface(), (250,432))
        else:
            surface.blit(MY_FONT.render('Password', 1, COLOR_BLACK), (250,422))  

        displayNotMatching = display_error_message(displayNotMatching, errorTime, surfaceCopy, 'Passwords do not match')
                
        pygame.display.flip()

    return

def forgot_password_view():
    email = pygame_textinput.TextInput()
    login_view = pygame.image.load("images/menu/forgot-password.png")
    surface.fill(COLOR_BACKGROUND)
    while True:
        # Clock tick
        clock.tick(60)

        # Application events
        playevents = pygame.event.get()

        for e in playevents:
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE and main_menu.is_disabled():
                    account_login_view()
                    return
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)
                if mouse_pos[0] in range(186,612) and mouse_pos[1] in range(430,477):
                    # recover email
                    if len(email.get_text()) < 1:
                        break
                    send_recovery_email(email = email.get_text())
                    return
                elif mouse_pos[0] in range(277,510) and mouse_pos[1] in range(496,513):
                    recover_account_view()
                    return
                elif mouse_pos[0] in range(562,617) and mouse_pos[1] in range(62,77):
                    # go back
                    account_login_view()
                    return
        
        email.update(playevents)   
            
        # blit information to the menu based on user input from above
        surface.blit(login_view, ((WINDOW_SIZE[0] - login_view.get_size()[0]) / 2, (WINDOW_SIZE[1] - login_view.get_size()[1]) / 2))
        if len(email.get_text()) >= 1:
            surface.blit(email.get_surface(), (250,170))  
        else:
            surface.blit(MY_FONT.render('Email', 1, COLOR_BLACK), (250,160))  

        pygame.display.flip()

    return

def update_account_view():
    """
    Update account game function
    
    :return: None
    """

    username = pygame_textinput.TextInput()
    oldPassword = pygame_textinput.TextInput()
    password = pygame_textinput.TextInput()
    login_view = pygame.image.load("images/menu/update-account.png")
    surface.fill(COLOR_BACKGROUND)

    selected = "username"
    
    while True:
        # Clock tick
        clock.tick(60)

        # Application events
        playevents = pygame.event.get()

        for e in playevents:
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE and main_menu.is_disabled():
                    account_login_view()
                    return
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)
                if mouse_pos[0] in range(190,610) and mouse_pos[1] in range(148,210):
                    selected = "username"
                elif mouse_pos[0] in range(190,610) and mouse_pos[1] in range(235,298):
                    selected = "oldPassword"
                elif mouse_pos[0] in range(190,610) and mouse_pos[1] in range(330,392):
                    selected = "password"
                elif mouse_pos[0] in range(186,612) and mouse_pos[1] in range(430,477):
                    # update account
                    if len(oldPassword.get_text()) < 1 or len(username.get_text()) < 1 or len(password.get_text()) < 1:
                        break
                    update_account(username = username.get_text(), oldPassword = oldPassword.get_text(), password = password.get_text())
                    return
                elif mouse_pos[0] in range(562,617) and mouse_pos[1] in range(62,77):
                    # go back
                    account_login_view()
                    return
        
        if selected == "username":
            username.update(playevents)   
        elif selected == "oldPassword":
            oldPassword.update(playevents, passProtect=True)   
        elif selected == "password":
            password.update(playevents, passProtect=True)
            
        # blit information to the menu based on user input from above
        surface.blit(login_view, ((WINDOW_SIZE[0] - login_view.get_size()[0]) / 2, (WINDOW_SIZE[1] - login_view.get_size()[1]) / 2))
        if len(username.get_text()) >= 1:
            surface.blit(username.get_surface(), (250,170))  
        else:
            surface.blit(MY_FONT.render('Username', 1, COLOR_BLACK), (250,160))  
        if len(oldPassword.get_text()) >= 1:
            surface.blit(oldPassword.get_surface(), (250,257))  
        else:
            surface.blit(MY_FONT.render('Old Password', 1, COLOR_BLACK), (250,247))  
        if len(password.get_text()) >= 1:
            surface.blit(password.get_surface(), (250,352))
        else:
            surface.blit(MY_FONT.render('Password', 1, COLOR_BLACK), (250,342))  
        pygame.display.flip()

    return

def recover_account_view():
    """
    Recover account

    :return: None
    """

    username = pygame_textinput.TextInput()
    code = pygame_textinput.TextInput()
    password1 = pygame_textinput.TextInput()
    password2 = pygame_textinput.TextInput()

    login_view = pygame.image.load("images/menu/recover-account.png")
    surface.fill(COLOR_BACKGROUND)

    selected = "username"
    displayNotMatching = False
    errorTime = 0
    surfaceCopy = None

    while True:
        # Clock tick
        clock.tick(60)

        # Application events
        playevents = pygame.event.get()

        for e in playevents:
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE and main_menu.is_disabled():
                    account_login_view()
                    return
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)
                if mouse_pos[0] in range(190,610) and mouse_pos[1] in range(148,210):
                    selected = "username"
                elif mouse_pos[0] in range(190,610) and mouse_pos[1] in range(235,298):
                    selected = "code"
                elif mouse_pos[0] in range(190,610) and mouse_pos[1] in range(320,385):
                    selected = "password1"
                elif mouse_pos[0] in range(190,610) and mouse_pos[1] in range(403,470):
                    selected = "password2"
                elif mouse_pos[0] in range(186,612) and mouse_pos[1] in range(483,535):
                    # update account
                    if len(code.get_text()) < 1 or len(username.get_text()) < 1 or len(password1.get_text()) < 1 or len(password2.get_text()) < 1:
                        break
                    if password1.get_text() == password2.get_text():
                        recover_account_credentials(username = username.get_text(), code = code.get_text(), password = password1.get_text())
                        return
                    else:
                        displayNotMatching = True
                        errorTime = clock.get_time()
                        surfaceCopy = surface.copy()
                elif mouse_pos[0] in range(562,617) and mouse_pos[1] in range(62,77):
                    # go back
                    account_login_view()
                    return
        
        if selected == "username":
            username.update(playevents)   
        elif selected == "code":
            code.update(playevents)   
        elif selected == "password1":
            password1.update(playevents, passProtect=True)
        elif selected == "password2":
            password2.update(playevents, passProtect=True)
            
        # blit information to the menu based on user input from above
        surface.blit(login_view, ((WINDOW_SIZE[0] - login_view.get_size()[0]) / 2, (WINDOW_SIZE[1] - login_view.get_size()[1]) / 2))
        if len(username.get_text()) >= 1:
            surface.blit(username.get_surface(), (250,170))  
        else:
            surface.blit(MY_FONT.render('Username', 1, COLOR_BLACK), (250,160))  
        if len(code.get_text()) >= 1:
            surface.blit(code.get_surface(), (250,257))  
        else:
            surface.blit(MY_FONT.render('Code', 1, COLOR_BLACK), (250,247))  
        if len(password1.get_text()) >= 1:
            surface.blit(password1.get_surface(), (250,352))
        else:
            surface.blit(MY_FONT.render('Password', 1, COLOR_BLACK), (250,342))  
        if len(password2.get_text()) >= 1:
            surface.blit(password2.get_surface(), (250,432))
        else:
            surface.blit(MY_FONT.render('Password', 1, COLOR_BLACK), (250,422))  

        displayNotMatching = display_error_message(displayNotMatching, errorTime, surfaceCopy, 'Passwords do not match')

        pygame.display.flip()

    return

def display_error_message(displayNotMatching, errorTime, surfaceCopy, message):
    # If the text should be displayed.
    if displayNotMatching and surfaceCopy is not None:
        # quick show passwords are wrong
        passworderror = MY_FONT.render(message, 1, COLOR_RED)
        pygame.draw.rect(surface, COLOR_WHITE, [190,320,610-190,385-320])
        surface.blit(passworderror, (250,342))  
        # Check if three seconds have passed. This assumes that "get_current_time()" operates on seconds.
        if clock.get_time() - errorTime > 3:
            surface.blit(surfaceCopy, (0,0))
            return False
        return True
    return False

def join_game_view():

    option_menu.disable()
    option_menu.reset(1)

    room_number = pygame_textinput.TextInput()
    login_view = pygame.image.load("images/menu/join-game.png")
    surface.fill(COLOR_BACKGROUND)
    error_surface = False
    
    while True:
        # Clock tick
        clock.tick(60)

        # Application events
        playevents = pygame.event.get()

        for e in playevents:
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE and main_menu.is_disabled():
                    option_menu.enable()
                    option_menu.mainloop(playevents)
                    return
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)
                if mouse_pos[0] in range(186,612) and mouse_pos[1] in range(400,450):
                    # recover room_number
                    if len(room_number.get_text()) < 1: 
                        break
                    if not room_number.get_text().isdigit():
                        error_surface = True
                        break
                    enter_room(room_number = room_number.get_text())
                    return
                elif mouse_pos[0] in range(562,617) and mouse_pos[1] in range(62,77):
                    option_menu.enable()
                    option_menu.mainloop(playevents)
                    return
        
        room_number.update(playevents)   
            
        # blit information to the menu based on user input from above
        surface.blit(login_view, ((WINDOW_SIZE[0] - login_view.get_size()[0]) / 2, (WINDOW_SIZE[1] - login_view.get_size()[1]) / 2))
        if error_surface:
            ptext.draw("Room Number can only contain numbers, not letters", (200, 300), sysfontname="arial", color=COLOR_RED, fontsize=35, width = 300)
            error_surface = False
        if len(room_number.get_text()) >= 1:
            surface.blit(room_number.get_surface(), (250,170))  
        else:
            surface.blit(MY_FONT.render('Room Number', 1, COLOR_BLACK), (250,160))  

        pygame.display.flip()

    return

def create_new_game_view():
    option_menu.disable()
    option_menu.reset(1)

    ruleset_name = pygame_textinput.TextInput()
    login_view = pygame.image.load("images/menu/create-new-game.png")
    surface.fill(COLOR_BACKGROUND)
    error_surface = False
    
    while True:
        # Clock tick
        clock.tick(60)

        # Application events
        playevents = pygame.event.get()

        for e in playevents:
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE and main_menu.is_disabled():
                    option_menu.enable()
                    option_menu.mainloop(playevents)
                    return
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)
                if mouse_pos[0] in range(186,612) and mouse_pos[1] in range(400,450):
                    # recover ruleset_name
                    if len(ruleset_name.get_text()) < 1: 
                        break
                    # if not ruleset_name.get_text().isdigit(): # CHECK IF EXISTS
                    #     error_surface = True
                    #     break
                    create_room(ruleset_name = ruleset_name.get_text())
                    return
                elif mouse_pos[0] in range(562,617) and mouse_pos[1] in range(62,77):
                    option_menu.enable()
                    option_menu.mainloop(playevents)
                    return
        
        ruleset_name.update(playevents)   
            
        # blit information to the menu based on user input from above
        surface.blit(login_view, ((WINDOW_SIZE[0] - login_view.get_size()[0]) / 2, (WINDOW_SIZE[1] - login_view.get_size()[1]) / 2))
        if error_surface:
            ptext.draw("Ruleset name does not exist", (200, 300), sysfontname="arial", color=COLOR_RED, fontsize=35, width = 300)
            error_surface = False
        if len(ruleset_name.get_text()) >= 1:
            surface.blit(ruleset_name.get_surface(), (250,170))  
        else:
            surface.blit(MY_FONT.render('Ruleset', 1, COLOR_BLACK), (250,160))  

        pygame.display.flip()

    return

def ruleset_view():
    RulesetView(currentUsername, client).main()
    surface = pygame.display.set_mode(WINDOW_SIZE)
    return

def previous_games_view():
    GameHistoryView(currentUsername, client).main()
    surface = pygame.display.set_mode(WINDOW_SIZE)
    return

# -----------------------------------------------------------------------------
# CALLING EXTERNAL FUNCTIONS 
def login(username, password, email=None):
    if email is None:
        return client.login(username, password)
    else:   
        print("creating account")
        return client.create_account(username, password, email)

def update_account(username, oldPassword, password):
    print("updating account info")
    client.change_credentials(username, oldPassword, password)
    return

def send_recovery_email(email):
    print("send recovery email")
    client.send_recovery(email)
    return

def recover_account_credentials(username, code, password):
    print("recover account credentials")
    client.recover_account(username, code, password, password)
    return

def enter_room(room_number):
    print(room_number)
    return

def create_room(ruleset_name):
    print(ruleset_name)
    return

# -----------------------------------------------------------------------------
def random_color():
    """
    Return random color.
    
    :return: Color tuple
    """
    return randrange(0, 255), randrange(0, 255), randrange(0, 255)

def main_background():
    """
    Function used by menus, draw on background while menu is active.
    
    :return: None
    """
    surface.fill(COLOR_BACKGROUND)


# -----------------------------------------------------------------------------
# PLAY MENU
# play_menu = pygameMenu.Menu(surface,
#                             bgfun=main_background,
#                             color_selected=COLOR_WHITE,
#                             font=pygameMenu.fonts.FONT_BEBAS,
#                             font_color=COLOR_BLACK,
#                             font_size=30,
#                             menu_alpha=100,
#                             menu_color=MENU_BACKGROUND_COLOR,
#                             menu_height=int(WINDOW_SIZE[1] * 0.6),
#                             menu_width=int(WINDOW_SIZE[0] * 0.6),
#                             onclose=PYGAME_MENU_DISABLE_CLOSE,
#                             option_shadow=False,
#                             title='Login',
#                             window_height=WINDOW_SIZE[1],
#                             window_width=WINDOW_SIZE[0]
#                             )
# # When pressing return -> play(DIFFICULTY[0], font)
# play_menu.add_option('Start', play_function, DIFFICULTY,
#                      pygame.font.Font(pygameMenu.fonts.FONT_FRANCHISE, 50))
# play_menu.add_selector('Select difficulty', [('Easy', 'EASY'),
#                                              ('Medium', 'MEDIUM'),
#                                              ('Hard', 'HARD')],
#                        onreturn=None,
#                        onchange=change_difficulty)
# login_menu.add_option('Return to main menu', PYGAME_MENU_BACK)

# OPTION MENU
option_menu = pygameMenu.Menu(surface,
                            bgfun=main_background,
                            color_selected=COLOR_WHITE,
                            font=pygameMenu.fonts.FONT_BEBAS,
                            font_color=COLOR_BLACK,
                            font_size=30,
                            menu_alpha=100,
                            menu_color=MENU_BACKGROUND_COLOR,
                            menu_height=int(WINDOW_SIZE[1] * 0.6),
                            menu_width=int(WINDOW_SIZE[0] * 0.6),
                            onclose=PYGAME_MENU_DISABLE_CLOSE,
                            option_shadow=False,
                            title='RPGenerator',
                            window_height=WINDOW_SIZE[1],
                            window_width=WINDOW_SIZE[0]
                            )
option_menu.add_option('Join Game', join_game_view)
option_menu.add_option('Create New Game', create_new_game_view)
option_menu.add_option('Rulesets', ruleset_view)
option_menu.add_option('Previous Games', previous_games_view)
option_menu.add_option('Quit', PYGAME_MENU_EXIT)

# ABOUT MENU
about_menu = pygameMenu.TextMenu(surface,
                                 bgfun=main_background,
                                 color_selected=COLOR_WHITE,
                                 font=pygameMenu.fonts.FONT_BEBAS,
                                 font_color=COLOR_BLACK,
                                 font_size_title=30,
                                 font_title=pygameMenu.fonts.FONT_8BIT,
                                 menu_color=MENU_BACKGROUND_COLOR,
                                 menu_color_title=COLOR_WHITE,
                                 menu_height=int(WINDOW_SIZE[1] * 0.6),
                                 menu_width=int(WINDOW_SIZE[0] * 0.6),
                                 onclose=PYGAME_MENU_DISABLE_CLOSE,
                                 option_shadow=False,
                                 text_color=COLOR_BLACK,
                                 text_fontsize=20,
                                 title='About',
                                 window_height=WINDOW_SIZE[1],
                                 window_width=WINDOW_SIZE[0]
                                 )
for m in ABOUT:
    about_menu.add_line(m)
about_menu.add_line(PYGAMEMENU_TEXT_NEWLINE)
about_menu.add_option('Return to main menu', PYGAME_MENU_BACK)

# MAIN MENU
main_menu = pygameMenu.Menu(surface,
                            bgfun=main_background,
                            color_selected=COLOR_WHITE,
                            font=pygameMenu.fonts.FONT_BEBAS,
                            font_color=COLOR_BLACK,
                            font_size=30,
                            menu_alpha=100,
                            menu_color=MENU_BACKGROUND_COLOR,
                            menu_height=int(WINDOW_SIZE[1] * 0.6),
                            menu_width=int(WINDOW_SIZE[0] * 0.6),
                            onclose=PYGAME_MENU_DISABLE_CLOSE,
                            option_shadow=False,
                            title='RPGenerator',
                            window_height=WINDOW_SIZE[1],
                            window_width=WINDOW_SIZE[0]
                            )
main_menu.add_option('Login', account_login_view)
main_menu.add_option('About', about_menu)
main_menu.add_option('Quit', PYGAME_MENU_EXIT)

# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # start asynchronous communication threads
    async_receive_thread = threading.Thread(target=async_receive)
    async_receive_thread.start()

    async_send_thread = threading.Thread(target=async_command_loop)
    async_send_thread.start()

    while True:

        # Tick
        clock.tick(30)

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                exit()

        # Main menu
        main_menu.mainloop(events)

        # Flip surface
        pygame.display.flip()