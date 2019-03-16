import pygame, sys, random
from pygame.locals import *
from game_engine.map import Map
import os

# sources for examples:
# http://usingpython.com/pygame-tilemaps/
# http://usingpython.com/list-comprehension/


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

myMap.textures = [Map.Texture(0,0,1,1,"coal.png"),Map.Texture(5,5,2,2,"water.png"),Map.Texture(2,2,1,1,"rock.png"),Map.Texture(2,3,1,1,"rock.png")]

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

MY_FONT = pygame.font.SysFont('arial', 30)

def make_popup(mousepos):
    popupSurf = pygame.Surface((60, 60))
    options = ['Attack',
               'Talk']
    for i in options:
        textSurf = MY_FONT.render(i, 1, (255, 255, 255))
        textRect = textSurf.get_rect()
        textRect.top = mousepos[0]
        textRect.left = mousepos[1]
        mousepos = (mousepos[0]+pygame.font.Font.get_linesize(MY_FONT),mousepos[1])
        popupSurf.blit(textSurf, textRect)
    popupRect = popupSurf.get_rect()
    popupRect.centerx = DISPLAYSURF.get_size()[0]/2
    popupRect.centery = DISPLAYSURF.get_size()[1]/2
    DISPLAYSURF.blit(popupSurf, popupRect)
    pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            mousepos = pygame.mouse.get_pos()
            make_popup(mousepos)


    pygame.display.update()