# Import pygame and libraries
import pygame
from pygame.locals import *
from random import randrange
import os
import pygame_textinput

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
FPS = 60.0
MENU_BACKGROUND_COLOR = (228, 55, 36)
WINDOW_SIZE = (800, 600)
MY_FONT = pygame.font.Font(pygameMenu.fonts.FONT_FRANCHISE, 40)

# -----------------------------------------------------------------------------
# Init pygame
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Create pygame screen and objects
surface = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('RPGenerator')
clock = pygame.time.Clock()
dt = 1 / FPS

# -----------------------------------------------------------------------------
def random_color():
    """
    Return random color.
    
    :return: Color tuple
    """
    return randrange(0, 255), randrange(0, 255), randrange(0, 255)

def login_function():
    """
    Login game function
    
    :return: None
    """

    # Reset main menu and disable
    # You also can set another menu, like a 'pause menu', or just use the same
    # main_menu as the menu that will check all your input.
    main_menu.disable()
    main_menu.reset(1)

    email = pygame_textinput.TextInput()
    password = pygame_textinput.TextInput()
    login_view = pygame.image.load("images/menu/login-copy.png")
    surface.fill(COLOR_BACKGROUND)
    

    selected = "email"
    
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
                    selected = "email"
                elif mouse_pos[0] in range(190,610) and mouse_pos[1] in range(266,322):
                    selected = "password"
                elif mouse_pos[0] in range(300,530) and mouse_pos[1] in range(517,530):
                    create_new_account()
                    return
                elif mouse_pos[0] in range(335,480) and mouse_pos[1] in range(360,375):
                    forgot_password()
                    return
                elif mouse_pos[0] in range(186,612) and mouse_pos[1] in range(430,477):
                    login()
                    return
                elif mouse_pos[0] in range(562,617) and mouse_pos[1] in range(62,77):
                    main_menu.enable()
                    main_menu.mainloop(playevents)
                    return
                # continue to make the rest of the buttons connect to different places
                # elif e.key != K_ESCAPE and main_menu.is_disabled():
                #     # Feed it with events every frame
                      
                # elif e.key == K_RETURN and main_menu.is_disabled():
                #     surface.fill(COLOR_BACKGROUND)

        
        if selected == "email":
            email.update(playevents)   
        elif selected == "password":
            password.update(playevents, passProtect=True)
            
        surface.blit(login_view, ((WINDOW_SIZE[0] - login_view.get_size()[0]) / 2, (WINDOW_SIZE[1] - login_view.get_size()[1]) / 2))
        if len(email.get_text()) >= 1:
            surface.blit(email.get_surface(), (250,170))  
        else:
            surface.blit(MY_FONT.render('Email', 1, COLOR_BLACK), (250,160))  
        if len(password.get_text()) >= 1:
            surface.blit(password.get_surface(), (250,290))
        else:
            surface.blit(MY_FONT.render('Password', 1, COLOR_BLACK), (250,280))  

        pygame.display.flip()

    return

def create_new_account():
    """
    Create new account game function
    
    :return: None
    """

    email = pygame_textinput.TextInput()
    username = pygame_textinput.TextInput()
    password = pygame_textinput.TextInput()
    login_view = pygame.image.load("images/menu/create-account.png")
    surface.fill(COLOR_BACKGROUND)

    selected = "email"
    
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
                    login_function()
                    return
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)
                if mouse_pos[0] in range(190,610) and mouse_pos[1] in range(148,210):
                    selected = "email"
                elif mouse_pos[0] in range(190,610) and mouse_pos[1] in range(235,298):
                    selected = "username"
                elif mouse_pos[0] in range(190,610) and mouse_pos[1] in range(330,392):
                    selected = "password"
                elif mouse_pos[0] in range(186,612) and mouse_pos[1] in range(430,477):
                    login()
                    return
                elif mouse_pos[0] in range(562,617) and mouse_pos[1] in range(62,77):
                    login_function()
                    return
        
        if selected == "email":
            email.update(playevents)   
        elif selected == "username":
            username.update(playevents)   
        elif selected == "password":
            password.update(playevents, passProtect=True)
            
        surface.blit(login_view, ((WINDOW_SIZE[0] - login_view.get_size()[0]) / 2, (WINDOW_SIZE[1] - login_view.get_size()[1]) / 2))
        if len(email.get_text()) >= 1:
            surface.blit(email.get_surface(), (250,170))  
        else:
            surface.blit(MY_FONT.render('Email', 1, COLOR_BLACK), (250,160))  
        if len(username.get_text()) >= 1:
            surface.blit(username.get_surface(), (250,257))  
        else:
            surface.blit(MY_FONT.render('Username', 1, COLOR_BLACK), (250,247))  
        if len(password.get_text()) >= 1:
            surface.blit(password.get_surface(), (250,352))
        else:
            surface.blit(MY_FONT.render('Password', 1, COLOR_BLACK), (250,342))  
        pygame.display.flip()

    return

def forgot_password():
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
                    login_function()
                    return
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)
                if mouse_pos[0] in range(186,612) and mouse_pos[1] in range(430,477):
                    send_recovery_email()
                    return
                elif mouse_pos[0] in range(562,617) and mouse_pos[1] in range(62,77):
                    login_function()
                    return
        
        email.update(playevents)   
            
        surface.blit(login_view, ((WINDOW_SIZE[0] - login_view.get_size()[0]) / 2, (WINDOW_SIZE[1] - login_view.get_size()[1]) / 2))
        if len(email.get_text()) >= 1:
            surface.blit(email.get_surface(), (250,170))  
        else:
            surface.blit(MY_FONT.render('Email', 1, COLOR_BLACK), (250,160))  

        pygame.display.flip()

    return


def login():
    return

def send_recovery_email():
    return

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
main_menu.add_option('Login', login_function)
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