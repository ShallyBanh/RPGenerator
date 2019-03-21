# Import pygame and libraries
import pygame
from pygame.locals import *
from random import randrange
import os
import pygame_textinput
from client import Client

# Import pygameMenu
import pygameMenu
from pygameMenu.locals import *
# PYGAMEMENU_TEXT_NEWLINE

# Global variables
DIFFICULTY = ['EASY']
ABOUT = ['RPGenerator {0}'.format("V1.0.0"),
         'Author: {0}'.format("2019-Group-04")]
# COLOR_BACKGROUND = (128, 0, 128)
COLOR_BACKGROUND = (21,156,207)  
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
FPS = 60.0
MENU_BACKGROUND_COLOR = (228, 55, 36)
WINDOW_SIZE = (800, 600)
MY_FONT = pygame.font.Font(pygameMenu.fonts.FONT_FRANCHISE, 40)

# -----------------------------------------------------------------------------
# Init pygame
pygame.init()
client = Client()
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Create pygame screen and objects
surface = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('RPGenerator')
clock = pygame.time.Clock()
dt = 1 / FPS

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
                    login(username = username.get_text(), password = password.get_text())
                    return
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
                        login(username = username.get_text(), email = email.get_text(), password = password1.get_text())
                        return
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

# -----------------------------------------------------------------------------
# CALLING EXTERNAL FUNCTIONS 
def login(username, password, email=None):
    if email is None:
        print("logging in")
        client.login(username, password)
    else:
        print("creating account")
        client.create_account(username, password, email)
    return

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