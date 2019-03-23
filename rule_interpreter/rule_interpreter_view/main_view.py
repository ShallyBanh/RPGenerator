import os
import sys
sys.path.append('../')
from validator import Validator
from entity import Entity
from action import Action
from attribute import Attribute
from syntax_parser import SyntaxParser
sys.path.append('/rule_interpreter_view')
import pygame
import ptext
import pygame_textinput
from entity_creation_view import EntityCreationView
from action_attribute_view import AttributeActionCreationView


ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"
plusImage = pygame.image.load('img/plussign.png')
moreButtonList = []

pygame.init()

sx, sy = 1300, 750
screen = pygame.display.set_mode((sx, sy))
pygame.display.set_caption("Main")
moreImage = pygame.image.load('img/moreButton.png')

buttonrects = [pygame.Rect((50, 150, 1100, 550))]
textSizes = [(50, 100)]
buttonnames = ["Entities"]
entities = []
actionNames = []
attributes = []
entites_str = ""
action_str = ""
attributeStr = ""
entity_name_input = ""
entity_type_input = ""
size = ""
entity_view = False
attribute_action_view = False

titleargs = ptext.draw("Main", midtop=(sx/2, 10), owidth=1.2, color = "0x884400", gcolor="0x442200", surf=None, cache = False, fontsize=64, fontname="CherryCreamSoda")
playing = True

while playing:
    screen.fill((0, 50, 50))
    screen.blit(plusImage,(1110, 110))
    clickpos = None
    events = pygame.event.get()

    if entity_view == True:
        name = EntityCreationView().main()
        if name[0] is not None:
            entities.append(name[0])
        entity_view = False
    
    if attribute_action_view == True:
        AttributeActionCreationView().main()
        attribute_action_view = False

    for event in events:
        if event.type == pygame.QUIT:
            playing = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            playing = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clickpos = event.pos
            x, y = clickpos
            if x in range(1110, 1140) and y in range(110, 140):
                entity_view = True
            for moreIdx in range(len(moreButtonList)):
                print(moreButtonList)
                x1 = int(moreButtonList[moreIdx][0])
                y1 = int(moreButtonList[moreIdx][1])
                if x in range(x1, x1 + 60) and y in range(y1, y1+30):
                    attribute_action_view = True

    for rect, name, size in zip(buttonrects, buttonnames, textSizes):
        screen.fill(pygame.Color("#553300"), rect)
        screen.fill(pygame.Color("#332200"), rect.inflate(-8, -8))
        box = rect.inflate(-8, 100)
        ptext.draw(name, size, fontname="Bubblegum_Sans", color="white", owidth=0.5, fontsize=40)
        ptext.drawbox("", box, fontname="Bubblegum_Sans", color = "white", owidth=0.5)
    
    entites_str = ""
    moreButtonList = []
    for entityIdx in range(len(entities)):
        entites_str += entities[entityIdx] + "\n"
        screen.blit(moreImage,(1050, 210 + entityIdx * 30 + entityIdx*0.05*100))
        moreButtonList.append((1050, 210 + entityIdx * 30 + entityIdx*0.05*100))
    ptext.draw(entites_str, (70, 200), fontname="Boogaloo", color="white", fontsize=30)

    screen.blit(*titleargs)
    pygame.display.flip()





