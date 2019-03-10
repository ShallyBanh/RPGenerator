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
    "SAND": pygame.image.load("images/fine-sand.jpg"),
    "GREY": pygame.image.load("images/grey.png"),
    "FOG": pygame.image.load("images/fog.png")
}

GameListEntities = [Map.Texture(0,0,1,1,"COAL"),Map.Texture(5,5,2,2,"WATER"),Map.Texture(2,2,1,1,"ROCK"),Map.Texture(2,3,1,1,"ROCK")]

pygame.init()
DISPLAYSURF = pygame.display.set_mode((myMap.width*myMap.tilesize, myMap.height*myMap.tilesize))

# create the entire background
greyImage = pygame.transform.scale(textures["GREY"], (myMap.tilesize,myMap.tilesize))
fogImage = pygame.transform.scale(textures["FOG"], (myMap.tilesize,myMap.tilesize))
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
for entity in GameListEntities:
    imag = pygame.transform.scale(textures[entity.name], (entity.width*myMap.tilesize,entity.height*myMap.tilesize))
    DISPLAYSURF.blit(imag, (entity.y*myMap.tilesize, entity.x*myMap.tilesize))


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()