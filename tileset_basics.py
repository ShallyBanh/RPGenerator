import pygame, sys, random
from pygame.locals import *
from game_engine.map import Map

# sources for examples:
# http://usingpython.com/pygame-tilemaps/
# http://usingpython.com/list-comprehension/

myMap = Map(tilesize = 40, height = 15, width = 25)

# textures = {
#   "ROCK": pygame.transform.scale(pygame.image.load("images/rock.png"), (myMap.tilesize,myMap.tilesize)),
#   "GRASS": pygame.transform.scale(pygame.image.load("images/grass.png"), (myMap.tilesize,myMap.tilesize)),
#   "WATER": pygame.transform.scale(pygame.image.load("images/water.png"), (myMap.tilesize,myMap.tilesize)),
#   "COAL": pygame.transform.scale(pygame.image.load("images/coal.png"), (myMap.tilesize,myMap.tilesize))
# }

textures = {
    "ROCK": pygame.image.load("images/rock.png"),
    "GRASS": pygame.image.load("images/grass.png"),
    "WATER": pygame.image.load("images/water.png"),
    "COAL": pygame.image.load("images/coal.png"),
    "GREY": pygame.image.load("images/grey.png")
}

class Entity:
    def __init__(self, x, y, width, height, name):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.name = name

GameListEntities = [Entity(0,0,1,1,"COAL"),Entity(5,5,2,2,"WATER"),Entity(2,2,1,1,"ROCK"),Entity(2,3,1,1,"ROCK")]
# tilemap = [[0 for w in range(myMap.width)] for h in range(myMap.height)]

pygame.init()
DISPLAYSURF = pygame.display.set_mode((myMap.width*myMap.tilesize, myMap.height*myMap.tilesize))
imag = pygame.transform.scale(textures["GREY"], (myMap.tilesize,myMap.tilesize))
for rw in range(myMap.height):
    for cl in range(myMap.width):
        # myMap._tileset[rw][cl] = tile
        # myMap.set_tileset(row=rw, column=cl, tileset=tile)
        # DISPLAYSURF.blit(textures[myMap._tileset[rw][cl]], (cl*myMap.tilesize, rw*myMap.tilesize))
        DISPLAYSURF.blit(imag, (cl*myMap.tilesize, rw*myMap.tilesize))

for entity in GameListEntities:
    imag = pygame.transform.scale(textures[entity.name], (entity.width*myMap.tilesize,entity.height*myMap.tilesize))
    DISPLAYSURF.blit(imag, (entity.y*myMap.tilesize, entity.x*myMap.tilesize))


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()