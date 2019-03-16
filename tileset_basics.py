import pygame, sys, random
from pygame.locals import *
from game_engine.map import Map
import os
import math

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

def which_tile(mousepos):
    return math.ceil(mousepos[1]/myMap.tilesize)-1, math.ceil(mousepos[0]/myMap.tilesize)-1

def tile_location(size):
    return size[1]*myMap.tilesize, size[0]*myMap.tilesize

def make_popup(x, y, entity):
    global OLD_SURF

    options = entity.actions

    textSurf = []
    width = 0
    height = 0
    OLD_SURF = DISPLAYSURF.copy()
     # newsize = img1.get_width()+4, img1.get_height()+4
    for i in options:
        textSurf.append(MY_FONT.render(i, 1, (255, 255, 255)))
        local_width, height = MY_FONT.size(i) 
        if (local_width>width):
            width = local_width
    popupSurf = pygame.Surface((width+4,height*len(options)))
    DISPLAYSURF.blit(popupSurf, (x,y))    
    for i in range(len(textSurf)):
        DISPLAYSURF.blit(textSurf[i], (x+2,y+(height*i)))

    return (popupSurf.get_width(), popupSurf.get_height()), (x,y)

def remove_previous_popup():
    DISPLAYSURF.blit(OLD_SURF, (0,0))

direc = os.getcwd() + "/images/textures/" # Get current working directory
textures = {} 

# Select only files with the ext extension
pictures = [i for i in os.listdir(direc)]
# .split("/")[-1]
# Iterate over your txt files
for p in pictures:
    textures[p] = pygame.image.load("images/textures/"+p)

myMap = Map(tilesize = 40, height = 15, width = 25)

# textures = {
#   "ROCK": pygame.transform.scale(pygame.image.load("images/rock.png"), (myMap.tilesize,myMap.tilesize)),
#   "GRASS": pygame.transform.scale(pygame.image.load("images/grass.png"), (myMap.tilesize,myMap.tilesize)),
#   "WATER": pygame.transform.scale(pygame.image.load("images/water.png"), (myMap.tilesize,myMap.tilesize)),
#   "COAL": pygame.transform.scale(pygame.image.load("images/coal.png"), (myMap.tilesize,myMap.tilesize))
# }

# textures = {
#     "ROCK": pygame.image.load("images/rock.png"),
#     "GRASS": pygame.image.load("images/grass.png"),
#     "WATER": pygame.image.load("images/water.png"),
#     "COAL": pygame.image.load("images/coal.png"),
#     "SAND": pygame.image.load("images/fine-sand.jpg"),
#     "GREY": pygame.image.load("images/grey.png"),
#     "FOG": pygame.image.load("images/fog.png")
# }

# myMap.textures = [Map.Texture(0,0,1,1,"coal.png"),Map.Texture(5,5,2,2,"water.png"),Map.Texture(2,2,1,1,"rock.png"),Map.Texture(2,3,1,1,"rock.png")]
myMap.textures = [Entity(0,0,1,1,"coal.png",["Attack","Defend"]),Entity(5,5,2,2,"water.png",["Attack","Defend"]),Entity(2,2,1,1,"rock.png",["Defend"]),Entity(2,3,1,1,"rock.png",["Defend"])]

pygame.init()
DISPLAYSURF = pygame.display.set_mode((myMap.width*myMap.tilesize, myMap.height*myMap.tilesize))

# create the entire background
greyImage = pygame.transform.scale(textures["grey.png"], (myMap.tilesize,myMap.tilesize))
fogImage = pygame.transform.scale(textures["fog.png"], (myMap.tilesize,myMap.tilesize))
for rw in range(myMap.height):
    for cl in range(myMap.width):
        # myMap._tileset[rw][cl] = tile
        # myMap.set_tileset(row=rw, column=cl, tileset=tile)
        # DISPLAYSURF.blit(textures[myMap._tileset[rw][cl]], (cl*myMap.tilesize, rw*myMap.tilesize))
        if rw < myMap.height/2:
            DISPLAYSURF.blit(greyImage, (cl*myMap.tilesize, rw*myMap.tilesize))
        else: 
            DISPLAYSURF.blit(fogImage, (cl*myMap.tilesize, rw*myMap.tilesize))

# put all the entities on the map
for entity in myMap.textures:
    imag = pygame.transform.scale(textures[entity.name], (entity.width*myMap.tilesize,entity.height*myMap.tilesize))
    DISPLAYSURF.blit(imag, (entity.y*myMap.tilesize, entity.x*myMap.tilesize))

MY_FONT = pygame.font.SysFont('arial', 25)
OLD_SURF = None

entity_selected = False
entity = None

while True:    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            mousepos = pygame.mouse.get_pos()
            # top left of the tile
            if entity_selected:
                entity_selected=False
                remove_previous_popup()
                if mousepos[0] in range(location[0],location[0]+size[0]) and mousepos[1] in range(location[1],location[1]+size[1]):
                    # print(size[0],size[1])
                    # print(mousepos[1]-location[1])
                    rowsize = size[1]/len(entity.actions)
                    option_selected = math.floor((mousepos[1]-location[1])/rowsize)
                    action_requested = entity.actions[option_selected]
                    print(action_requested)
            else:
                x, y = which_tile(mousepos)
                # print(x,y)
                
                for e in myMap.textures:
                    # print(e.x, e.y)
                    if x in range(e.x,e.x+e.width) and y in range(e.y,e.y+e.height):
                        entity = e
                        entity_selected=True
                        break
                
                if entity_selected:
                    loc_x, loc_y = tile_location((entity.width+entity.x,entity.height+entity.y))
                    size, location = make_popup(loc_x, loc_y, entity)

    pygame.display.flip()