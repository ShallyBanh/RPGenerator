import pygame, sys, random
from pygame.locals import *
from game_engine.map import Map
import os
import math
import re
import ptext

# sources for examples:
# http://usingpython.com/pygame-tilemaps/
# http://usingpython.com/list-comprehension/

# utilized for testing of actions drop down menu
class Entity:
    def __init__(self, x, y, width, height, name, actions):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.name = name
        self.actions = actions
        self.attributes = ["example attributes", "example 2", "example 3"]

    def __str__(self):
        return  "Entity:\nName: "+self.name+"\nwidth: "+str(self.width)+"\nheight: "+str(self.height)+"\nx: "+ str(self.x)+ "\ny: " + str(self.y) +"\nactions: "+str(self.actions)+"\nattributes: "+str(self.attributes)


def offset_blit(x,y):
    return (x+MAPOFFSET[0],y+MAPOFFSET[1])

def which_tile(mousepos):
    return math.ceil(mousepos[1]/myMap.tilesize)-1, math.ceil(mousepos[0]/myMap.tilesize)-1

def tile_location(size):
    return size[1]*myMap.tilesize, size[0]*myMap.tilesize

def make_popup(x, y, entity):
    global OLDSURF

    # draw drop down
    options = entity.actions
    textSurf = []
    width = 0
    height = 0
    OLDSURF = DISPLAYSURF.copy()
     # newsize = img1.get_width()+4, img1.get_height()+4
    for i in options:
        textSurf.append(FONTTYPE.render(i, 1, (255, 255, 255)))
        local_width, height = FONTTYPE.size(i) 
        if (local_width>width):
            width = local_width
    popupSurf = pygame.Surface((width+4,height*len(options)))
    DISPLAYSURF.blit(popupSurf, offset_blit(x,y))    
    for i in range(len(textSurf)):
        DISPLAYSURF.blit(textSurf[i], offset_blit(x+2,y+(height*i)))

    # draw rectangle surrounding the actual box
    left, top = tile_location((entity.x, entity.y))
    left, top = offset_blit(left, top)
    pygame.draw.lines(DISPLAYSURF, (255,0,0), True, [(left, top), (left+entity.width*myMap.tilesize, top), (left+entity.width*myMap.tilesize, top+entity.height*myMap.tilesize), (left, top+entity.height*myMap.tilesize)], 3)

    # entity information
    ptext.draw(str(entity), (5, 5), sysfontname="arial", color=COLOR_WHITE, fontsize=30, width = 200)

    return (popupSurf.get_width(), popupSurf.get_height()), (x,y)

def remove_previous_popup():
    DISPLAYSURF.blit(OLDSURF, (0,0))

def load_pictures():
    # Grab all pictures located in the textures directory
    direc = os.getcwd() + "/images/textures/"
    images = {}
    pictures = [i for i in os.listdir(direc)]
    for p in pictures:
        images[p] = pygame.image.load("images/textures/"+p)

    return images

class InputBox:
    # https://stackoverflow.com/questions/46390231/how-to-create-a-text-input-box-with-pygame

    def __init__(self, x, y, w, h, screen, text=''):
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = ptext.getsurf(self.text, sysfontname="arial", color=COLOR_WHITE, fontsize=30, width = w)
        self.height = self.txt_surface.get_height() + 5
        self.rect = pygame.Rect(x, y, w, self.height)
        self.active = False
        self.screen = screen

    def handle_event(self, event, transcript):
        if event.type == MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == KEYDOWN:
            if self.active:
                if event.key == K_RETURN:
                    print(self.text)
                    # append to the transcript view
                    transcript += "\n" + str(self.text)
                    print(transcript)
                    self.text = ""
                    self.remove_old_block()
                elif event.key == K_BACKSPACE:
                    self.text = self.text[:-1]
                    tmp_surface = ptext.getsurf(self.text, sysfontname="arial", color=COLOR_WHITE, fontsize=30, width = self.rect.w)
                    if tmp_surface.get_height() < (self.rect.h-5):
                        self.remove_old_block()
                else:
                    self.text += event.unicode

        return transcript

    def remove_old_block(self):
        self.rect.h += 5
        pygame.draw.rect(self.screen, COLOR_BLACK, self.rect, 0)
        self.rect.h = self.height

    def draw(self):
        # Blit the text.
        self.txt_surface, tpos = ptext.draw(self.text, (self.rect.x+5, self.rect.y+5), sysfontname="arial", color=COLOR_WHITE, fontsize=30, width = self.rect.w)
        self.rect.h = self.txt_surface.get_height() + 5
        # Blit the rect.
        pygame.draw.rect(self.screen, self.color, self.rect, 2)

    def wipe(self):
        # Blit the rect box.
        pygame.draw.rect(self.screen, COLOR_BLACK, self.rect, 0)
        pygame.draw.rect(self.screen, self.color, self.rect, 2)

class Transcript:
    def __init__(self, x, y, w, h, screen, transcript=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.transcript = transcript
        self.screen = screen
        self.color = COLOR_RED

    def update(self, transcript):
        if self.transcript != transcript:
            self.transcript = transcript

    def draw(self):
        # Blit the text.
        ptext.draw(self.transcript, (self.rect.x+5, self.rect.y+5), sysfontname="arial", color=COLOR_WHITE, fontsize=30, width = self.rect.w)
        # Blit the rect.
        pygame.draw.rect(self.screen, self.color, self.rect, 2)

    def wipe(self):
        # Blit the rect.
        pygame.draw.rect(self.screen, COLOR_BLACK, self.rect, 0)

    def scroll_up(self):
        print("scrolling up")

    def scroll_down(self):
        print("scrolling down")

# GLOBAL VAR
myMap = Map(tilesize = 50, height = 10, width = 18)
MAPOFFSET = (200,0)
OLDSURF = None

pygame.init()
# FONTTYPE = pygame.font.SysFont('arial', 25)
FONTTYPE = pygame.font.Font(None, 32)

DISPLAYSURF = pygame.display.set_mode((1300,750))
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)


if __name__ == "__main__":

    images = load_pictures()

    # create the map and add add textures to it
    myMap.textures = [Map.Texture(3,3,1,1,"coal.png"),Map.Texture(3,4,1,1,"coal.png")]
    ENTITIES = [Entity(5,5,2,2,"water.png",["Attack","Defend"]),Entity(2,2,1,1,"rock.png",["Sit"]),Entity(2,3,1,1,"rock.png",["Defend"])]
    #example fog
    myMap.fogOfWar[8][15] = False
    myMap.fogOfWar[8][16] = False
    myMap.fogOfWar[9][15] = False
    myMap.fogOfWar[9][16] = False

    # create the entire background
    greyImage = pygame.transform.scale(images["grey.png"], (myMap.tilesize,myMap.tilesize))
    fogImage = pygame.transform.scale(images["fog.png"], (myMap.tilesize,myMap.tilesize))
    for rw in range(myMap.height):
        for cl in range(myMap.width):
            if myMap.fogOfWar[rw][cl]:
                DISPLAYSURF.blit(greyImage, offset_blit(cl*myMap.tilesize, rw*myMap.tilesize))
            else: 
                DISPLAYSURF.blit(fogImage, offset_blit(cl*myMap.tilesize, rw*myMap.tilesize))

    # put all the textures on the map
    for texture in myMap.textures:
        texture_image = pygame.transform.scale(images[texture.name], (texture.width*myMap.tilesize,texture.height*myMap.tilesize))
        DISPLAYSURF.blit(texture_image, offset_blit(texture.y*myMap.tilesize, texture.x*myMap.tilesize))

    # put all the entities on the map
    for entity in ENTITIES:
        entity_image = pygame.transform.scale(images[entity.name], (entity.width*myMap.tilesize,entity.height*myMap.tilesize))
        DISPLAYSURF.blit(entity_image, offset_blit(entity.y*myMap.tilesize, entity.x*myMap.tilesize))

    my_entity = None
    input_box = InputBox(MAPOFFSET[0]+myMap.width*myMap.tilesize, DISPLAYSURF.get_height()-200, 200, 32, DISPLAYSURF)
    history = Transcript(MAPOFFSET[0]+myMap.width*myMap.tilesize, MAPOFFSET[1], 200, DISPLAYSURF.get_height()-(DISPLAYSURF.get_height()-input_box.rect.y), DISPLAYSURF)
    # transcript = ""

    while True:    
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                mousepos = (mousepos[0]-MAPOFFSET[0],mousepos[1]-MAPOFFSET[1])
                print(mousepos)
                if my_entity is not None:
                    remove_previous_popup()
                    if mousepos[0] in range(location[0],location[0]+size[0]) and mousepos[1] in range(location[1],location[1]+size[1]):
                        rowsize = size[1]/len(my_entity.actions)
                        option_selected = math.floor((mousepos[1]-location[1])/rowsize)
                        action_requested = my_entity.actions[option_selected]
                        print(action_requested)
                    my_entity = None
                else:
                    x, y = which_tile(mousepos)
                    for e in ENTITIES:
                        if x in range(e.x,e.x+e.width) and y in range(e.y,e.y+e.height):
                            my_entity = e
                            break
                    if my_entity is not None:
                        loc_x, loc_y = tile_location((my_entity.width+my_entity.x,my_entity.height+my_entity.y))
                        size, location = make_popup(loc_x, loc_y, my_entity)
            # input box handling + transcript update
            transcript = input_box.handle_event(event, history.transcript)
            history.update(transcript)
            # transcript = input_box.handle_event(event, transcript)

        input_box.wipe()
        history.wipe()
        # input_box.update()
        input_box.draw()
        history.draw()

        pygame.display.flip()