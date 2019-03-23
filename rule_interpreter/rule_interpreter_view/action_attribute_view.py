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
from action_creation_view import ActionCreationView
from attribute_creation_view import AttributeCreationView

class AttributeActionCreationView:
    def __init__(self):
        self._submitButtonImg = pygame.image.load('img/submit.png')
        self._arrowImg = pygame.image.load('img/arrow.png')
        self._plusImage = pygame.image.load('img/plussign.png')
        self._playing = True
        self._invalidSubmission = False
        self._action_view = False
        self._attribute_view = False

    def main(self):
        ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"

        pygame.init()

        sx, sy = 1300, 750
        screen = pygame.display.set_mode((sx, sy))

        buttonrects = [pygame.Rect((50, 50, 300, 650)),  pygame.Rect((400, 50, 800, 300)), pygame.Rect((400, 400, 800, 300))]
        textSizes = [(50, 10), (400, 10), (400, 360),]
        buttonnames = ["Entity Info", "Attributes", "Actions"]
        actionNames = []
        attributes = []
        entites_str = ""

        while self._playing:
            screen.fill((0, 50, 50))
            screen.blit(self._arrowImg,(10, 10))
            screen.blit(self._plusImage,(1175, 15))
            screen.blit(self._plusImage,(1175, 364))
            clickpos = None
            events = pygame.event.get()
            
            if self._action_view == True:
                actionName, rule = ActionCreationView().main()
                if actionName is not None:
                    actionNames.append(actionName)
                self._action_view = False
            
            if self._attribute_view == True:
                attrName, attrType, attrValue = AttributeCreationView().main()
                if attrName is not None:
                    attributes.append(attrName)
                self._attribute_view = False

            for event in events:
                if event.type == pygame.QUIT:
                    self._playing = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self._playing = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clickpos = event.pos
                    x, y = clickpos                 
                    if x in range(1175, 1200) and y in range(15, 50):
                        self._attribute_view = True
                    if x in range(1175, 1200) and y in range(365, 420):
                        self._action_view = True
                    if x in range(10,40) and y in range(10,40):
                        self._playing = False
                        return None, None, None

            for rect, name, size in zip(buttonrects, buttonnames, textSizes):
                screen.fill(pygame.Color("#553300"), rect)
                screen.fill(pygame.Color("#332200"), rect.inflate(-8, -8))
                box = rect.inflate(-8, 100)
                ptext.draw(name, size, fontname="Bubblegum_Sans", color="white", owidth=0.5, fontsize=40)
                ptext.drawbox("", box, fontname="Bubblegum_Sans", color = "white", owidth=0.5)

            actionStr = ""
            for action in actionNames:
                actionStr += action + "\n"
            ptext.draw(actionStr, (420, 420), fontname="Boogaloo", color="white", fontsize=30)

            attributeStr = ""
            for attr in attributes:
                attributeStr += attr + "\n"
            ptext.draw(attributeStr, (420, 60), fontname="Boogaloo", color="white", fontsize=30)

            pygame.display.flip()





