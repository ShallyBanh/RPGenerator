import os
import sys
sys.path.append('../')
from validator import Validator
from entity import Entity
from action import Action
from attribute import Attribute
from syntax_parser import SyntaxParser
sys.path.append('../../account')
from database import Database
sys.path.append('../rule_interpreter/rule_interpreter_view')
import pygame
import ptext
import pygame_textinput
import ruleset_creation_edit_view as ruleCreate
import pickle

class RulesetView:
    def __init__(self):
        self._submitButtonImg = pygame.image.load('img/submit.png')
        self._arrowImg = pygame.image.load('img/arrow.png')
        self._plusImage = pygame.image.load('img/plussign.png')
        self._editButtonList = []
        self._playing = True
        self._edit_ruleset_view = False
        self._create_ruleset_view = False

    def main(self, rulesetName):
        ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"

        pygame.init()

        sx, sy = 1300, 750
        screen = pygame.display.set_mode((sx, sy))
        pygame.display.set_caption("Rulesets")

        buttonrects = [pygame.Rect((50, 150, 1100, 550))]
        textSizes = [(50, 100)]
        buttonnames = ["Rulesets"]

        titleargs = ptext.draw("{}".format(rulesetName), midtop=(sx/2, 10), owidth=1.2, color = "0x884400", gcolor="0x442200", surf=None, cache = False, fontsize=64, fontname="CherryCreamSoda")

        while self._playing:
            screen.fill((0, 50, 50))
            screen.blit(self._plusImage,(1110, 110))
            clickpos = None
            events = pygame.event.get()

            # if entity_view == True:
            #     entityTuple = EntityCreationView().main()
            #     if entityTuple[0] is not None:
            #         entities.append(entityTuple[0])
            #         Validator().add_entity(Entity(entityTuple[0], entityTuple[1], entityTuple[2], entityTuple[3], entityTuple[4], entityTuple[5]))
            #     entity_view = False
            
            # if attribute_action_view == True:
            #     AttributeActionCreationView(currentEntityName).main()
            #     attribute_action_view = False

            for event in events:
                if event.type == pygame.QUIT:
                    self._playing = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self._playing = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clickpos = event.pos
                    x, y = clickpos
                    if x in range(960, 1000) and y in range(110, 140):
                        ruleCreate.main("")
                    #save button
                    for moreIdx in range(len(self._editButtonList)):
                        print(self._editButtonList)
                        x1 = int(self._editButtonList[moreIdx][0])
                        y1 = int(self._editButtonList[moreIdx][1])
                        if x in range(x1, x1 + 60) and y in range(y1, y1+30):
                            attribute_action_view = True
                            # currentEntityName = entities[moreIdx]

            for rect, name, size in zip(buttonrects, buttonnames, textSizes):
                screen.fill(pygame.Color("#553300"), rect)
                screen.fill(pygame.Color("#332200"), rect.inflate(-8, -8))
                box = rect.inflate(-8, 100)
                ptext.draw(name, size, fontname="Bubblegum_Sans", color="white", owidth=0.5, fontsize=40)
                ptext.drawbox("", box, fontname="Bubblegum_Sans", color = "white", owidth=0.5)
            
            # entites_str = ""
            # moreButtonList = []
            # for entityIdx in range(len(entities)):
            #     entites_str += entities[entityIdx] + "\n"
            #     screen.blit(moreImage,(900, 210 + entityIdx * 30 + entityIdx*0.05*100))
            #     moreButtonList.append((900, 210 + entityIdx * 30 + entityIdx*0.05*100))
            # ptext.draw(entites_str, (70, 200), fontname="Boogaloo", color="white", fontsize=30)

            screen.blit(*titleargs)
            pygame.display.flip()


RulesetView().main("Shally's ruleset")




