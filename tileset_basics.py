import pygame, sys, random
from pygame.locals import *
from game_engine.map import Map

# sources for examples:
# http://usingpython.com/pygame-tilemaps/
# http://usingpython.com/list-comprehension/

myMap = Map(tilesize = 40, height = 15, width = 25)

textures = {
	"ROCK": pygame.transform.scale(pygame.image.load("images/rock.png"), (myMap.tilesize,myMap.tilesize)),
	"GRASS": pygame.transform.scale(pygame.image.load("images/grass.png"), (myMap.tilesize,myMap.tilesize)),
	"WATER": pygame.transform.scale(pygame.image.load("images/water.png"), (myMap.tilesize,myMap.tilesize)),
	"COAL": pygame.transform.scale(pygame.image.load("images/coal.png"), (myMap.tilesize,myMap.tilesize))
}

# tilemap = [[0 for w in range(myMap.width)] for h in range(myMap.height)]

pygame.init()
DISPLAYSURF = pygame.display.set_mode((myMap.width*myMap.tilesize, myMap.height*myMap.tilesize))

for rw in range(myMap.height):
	for cl in range(myMap.width):
		randomNumber = random.randint(0,15)
		if randomNumber == 0:
			tile = "COAL"
		elif randomNumber in [1,2]:
			tile = "WATER"
		elif randomNumber in range(3,8):
			tile = "GRASS"
		else:
			tile = "ROCK"
		myMap._tileset[rw][cl] = tile
		# myMap.set_tileset(row=rw, column=cl, tileset=tile)
		DISPLAYSURF.blit(textures[myMap._tileset[rw][cl]], (cl*myMap.tilesize, rw*myMap.tilesize))

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	pygame.display.update()