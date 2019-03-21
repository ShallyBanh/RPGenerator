import pygame, sys, random
from pygame.locals import *
from game_engine.map import Map
import os
import math
import re


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

def multi_line_blit(text):
    label = []
    text = re.split(',|\[|\]|\n',text)
    for i in range(len(text)): 
        label.append(FONTTYPE.render(text[i], True, (255,255,255)))
    for line in range(len(label)):
        DISPLAYSURF.blit(label[line],(0,(line*label[line].get_height())))
    return

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
    multi_line_blit(str(entity))

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

# GLOBAL VAR
myMap = Map(tilesize = 50, height = 10, width = 18)
MAPOFFSET = (200,0)
OLDSURF = None

pygame.init()
FONTTYPE = pygame.font.SysFont('arial', 25)
DISPLAYSURF = pygame.display.set_mode((1300,750))

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

    while True:    
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                mousepos = (mousepos[0]-MAPOFFSET[0],mousepos[1]-MAPOFFSET[1])
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

        pygame.display.flip()