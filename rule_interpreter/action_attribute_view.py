import os
import sys
from models.validator import Validator
from models.action import Action
from models.attribute import Attribute
from models.entity import Entity
import pygame
import ptext
import pygame_textinput
from action_creation_view import ActionCreationView
from attribute_creation_view import AttributeCreationView

class AttributeActionCreationView:
    def __init__(self, currentEntityType, fontsize):
        self._submitButtonImg = pygame.image.load('img/submit.png')
        self._arrowImg = pygame.image.load('img/arrow.png')
        self._plusImage = pygame.image.load('img/plussign.png')
        self._playing = True
        self._invalidSubmission = False
        self._action_view = False
        self._attribute_view = False
        self._currentEntityType = currentEntityType
        self._fontsize = fontsize

    def get_entity_info(self):
        entityIdx = Validator().get_entity_idx(self._currentEntityType)
        if entityIdx != -1:
            return Validator().get_entities()[entityIdx]
        return -1

        
    def main(self):
        ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"
        entity = self.get_entity_info()

        pygame.init()

        sx, sy = 1300, 750
        screen = pygame.display.set_mode((sx, sy))

        buttonrects = [pygame.Rect((50, 50, 300, 650)),  pygame.Rect((400, 50, 800, 300)), pygame.Rect((400, 400, 800, 300))]
        textSizes = [(50, 10), (400, 10), (400, 360),]
        buttonnames = ["Entity Info", "Attributes", "Actions"]
        currentEntity = self.get_entity_info()
        actionNames = [action.get_action_name() for action in currentEntity.get_actions()]
        attributes = [attribute.get_attribute_name() for attribute in currentEntity.get_attributes()]

        while self._playing:
            screen.fill((0, 50, 50))
            screen.blit(self._arrowImg,(10, 10))
            screen.blit(self._plusImage,(1175, 15))
            screen.blit(self._plusImage,(1175, 364))
            clickpos = None
            events = pygame.event.get()
            
            if self._action_view == True:
                actionName, rule = ActionCreationView(self._fontsize).main()
                if actionName is not None:
                    actionNames.append(actionName)
                    entityIdx = Validator().get_entity_idx(self._currentEntityType)
                    if entityIdx != -1:
                        Validator().set_action(entityIdx, actionName, rule)
                self._action_view = False
            
            if self._attribute_view == True:
                attrName, attrValue = AttributeCreationView(self._fontsize).main()
                if attrName is not None:
                    attributes.append(attrName)
                    entityIdx = Validator().get_entity_idx(self._currentEntityType)
                    if entityIdx != -1:
                        Validator().set_attribute(entityIdx, attrName, attrValue)
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
                ptext.draw(name, size, fontname="Bubblegum_Sans", color="white", owidth=0.5, fontsize=self._fontsize*2.5)
                ptext.drawbox("", box, fontname="Bubblegum_Sans", color = "white", owidth=0.5)

            actionStr = ""
            for action in actionNames:
                actionStr += action + "\n"
            ptext.draw(actionStr, (420, 420), fontname="Boogaloo", color="white", fontsize=self._fontsize*2)

            attributeStr = ""
            for attr in attributes:
                attributeStr += attr + "\n"
            ptext.draw(attributeStr, (420, 60), fontname="Boogaloo", color="white", fontsize=self._fontsize*2)

            if entity != -1:
                ptext.draw(entity.get_basic_entity_info_to_str(), (60, 60), fontname="Boogaloo", color="white", fontsize=self._fontsize*2)

            pygame.display.flip()





