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

    # draw drop down
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

    # draw rectangle surrounding the actual box
    left, top = tile_location((entity.x, entity.y))
    pygame.draw.lines(DISPLAYSURF, (255,0,0), True, [(left, top), (left+entity.width*myMap.tilesize, top), (left+entity.width*myMap.tilesize, top+entity.height*myMap.tilesize), (left, top+entity.height*myMap.tilesize)], 3)

    return (popupSurf.get_width(), popupSurf.get_height()), (x,y)

def remove_previous_popup():
    DISPLAYSURF.blit(OLD_SURF, (0,0))

# Grab all pictures located in the textures directory
direc = os.getcwd() + "/images/textures/"
textures = {} 
pictures = [i for i in os.listdir(direc)]
for p in pictures:
    textures[p] = pygame.image.load("images/textures/"+p)

# create the map and add add textures to it
myMap = Map(tilesize = 40, height = 15, width = 25)

# myMap.textures = [Map.Texture(0,0,1,1,"coal.png"),Map.Texture(5,5,2,2,"water.png"),Map.Texture(2,2,1,1,"rock.png"),Map.Texture(2,3,1,1,"rock.png")]
myMap.textures = [Entity(0,0,1,1,"coal.png",["Attack","Defend"]),Entity(5,5,2,2,"water.png",["Attack","Defend"]),Entity(2,2,1,1,"rock.png",["Sit"]),Entity(2,3,1,1,"rock.png",["Defend"])]
#example fog
myMap.fogOfWar[12][15] = False
myMap.fogOfWar[12][16] = False
myMap.fogOfWar[13][15] = False
myMap.fogOfWar[13][16] = False

pygame.init()
DISPLAYSURF = pygame.display.set_mode((myMap.width*myMap.tilesize, myMap.height*myMap.tilesize))

# create the entire background
greyImage = pygame.transform.scale(textures["grey.png"], (myMap.tilesize,myMap.tilesize))
fogImage = pygame.transform.scale(textures["fog.png"], (myMap.tilesize,myMap.tilesize))
for rw in range(myMap.height):
    for cl in range(myMap.width):
        if myMap.fogOfWar[rw][cl]:
            DISPLAYSURF.blit(greyImage, (cl*myMap.tilesize, rw*myMap.tilesize))
        else: 
            DISPLAYSURF.blit(fogImage, (cl*myMap.tilesize, rw*myMap.tilesize))

# put all the entities on the map
for entity in myMap.textures:
    entity_image = pygame.transform.scale(textures[entity.name], (entity.width*myMap.tilesize,entity.height*myMap.tilesize))
    DISPLAYSURF.blit(entity_image, (entity.y*myMap.tilesize, entity.x*myMap.tilesize))

MY_FONT = pygame.font.SysFont('arial', 25)
OLD_SURF = None

entity = None

if __name__ == "__main__":
    while True:    
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                if entity is not None:
                    remove_previous_popup()
                    if mousepos[0] in range(location[0],location[0]+size[0]) and mousepos[1] in range(location[1],location[1]+size[1]):
                        rowsize = size[1]/len(entity.actions)
                        option_selected = math.floor((mousepos[1]-location[1])/rowsize)
                        action_requested = entity.actions[option_selected]
                        print(action_requested)
                    entity = None
                else:
                    x, y = which_tile(mousepos)
                    for e in myMap.textures:
                        if x in range(e.x,e.x+e.width) and y in range(e.y,e.y+e.height):
                            entity = e
                            break
                    if entity is not None:
                        loc_x, loc_y = tile_location((entity.width+entity.x,entity.height+entity.y))
                        size, location = make_popup(loc_x, loc_y, entity)

        pygame.display.flip()