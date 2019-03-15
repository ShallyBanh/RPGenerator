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
COLOR_BACKGROUND = (128, 0, 128)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
FPS = 60.0
MENU_BACKGROUND_COLOR = (228, 55, 36)
WINDOW_SIZE = (800, 600)

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
def change_difficulty(d):
    """
    Change difficulty of the game.
    
    :return: 
    """
    print ('Selected difficulty: {0}'.format(d))
    DIFFICULTY[0] = d


def random_color():
    """
    Return random color.
    
    :return: Color tuple
    """
    return randrange(0, 255), randrange(0, 255), randrange(0, 255)


# def play_function(difficulty, font):
#     """
#     Main game function
    
#     :param difficulty: Difficulty of the game
#     :param font: Pygame font
#     :return: None
#     """
#     difficulty = difficulty[0]
#     assert isinstance(difficulty, str)

#     if difficulty == 'EASY':
#         f = font.render('Playing as baby', 1, COLOR_WHITE)
#     elif difficulty == 'MEDIUM':
#         f = font.render('Playing as normie', 1, COLOR_WHITE)
#     elif difficulty == 'HARD':
#         f = font.render('Playing as god', 1, COLOR_WHITE)
#     else:
#         raise Exception('Unknown difficulty {0}'.format(difficulty))

#     # Draw random color and text
#     bg_color = random_color()
#     f_width = f.get_size()[0]


#     # Reset main menu and disable
#     # You also can set another menu, like a 'pause menu', or just use the same
#     # main_menu as the menu that will check all your input.
#     main_menu.disable()
#     main_menu.reset(1)
#     surface.blit(f, ((WINDOW_SIZE[0] - f_width) / 2, WINDOW_SIZE[1] / 2))

#     while True:

#         # Clock tick
#         clock.tick(60)

#         # Application events
#         playevents = pygame.event.get()
#         for e in playevents:
#             if e.type == QUIT:
#                 exit()
#             elif e.type == KEYDOWN:
#                 if e.key == K_ESCAPE and main_menu.is_disabled():
#                     main_menu.enable()
#                     # Pass events to main_menu
#                     main_menu.mainloop(playevents)
#                     # Quit this function, then skip to loop of main-menu on line 217
#                     return

#         # Feed it with events every frame
#         textinput.update(playevents)        

#         # Continue playing
#         # bg_color = random_color()
#         surface.fill(bg_color)
#         surface.blit(f, ((WINDOW_SIZE[0] - f_width) / 2, WINDOW_SIZE[1] / 2))
#         surface.blit(textinput.get_surface(), (10,10))

#         pygame.display.flip()

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
    login_view = pygame.image.load("images/login-copy.png")
    bg_color = (21,156,207)  
    surface.fill(bg_color)

    email_bool = True
    password_bool = False
    
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
                    main_menu.enable()
                    # Pass events to main_menu
                    main_menu.mainloop(playevents)
                    # Quit this function, then skip to loop of main-menu on line 217
                    return
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # print(mouse_pos)
                if mouse_pos[0] in range(190,610) and mouse_pos[1] in range(148,210):
                    email_bool = True
                    password_bool = False
                elif mouse_pos[0] in range(190,610) and mouse_pos[1] in range(266,322):
                    email_bool = False
                    password_bool = True

                # elif e.key != K_ESCAPE and main_menu.is_disabled():
                #     # Feed it with events every frame
                      
                # elif e.key == K_RETURN and main_menu.is_disabled():
                #     surface.fill(bg_color)

        
        if email_bool:
            email.update(playevents)   
        if password_bool:
            password.update(playevents, passProtect=True)
            
        surface.blit(login_view, ((WINDOW_SIZE[0] - login_view.get_size()[0]) / 2, (WINDOW_SIZE[1] - login_view.get_size()[1]) / 2))
        surface.blit(email.get_surface(), (250,170))  
        surface.blit(password.get_surface(), (250,290))
        pygame.display.flip()

    return

def new_account_function():
    """
    Create new account game function
    
    :return: None
    """

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

# login_menu = pygameMenu.Menu(surface,
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
# login_menu.add_option('Login', login_function)
# login_menu.add_option('Create New Account', new_account_function)
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

        # Feed it with events every frame
        # textinput.update(events)
        # Main menu
        main_menu.mainloop(events)
        
        # surface.blit(textinput.get_surface(), (10,10))

        # Flip surface
        pygame.display.flip()