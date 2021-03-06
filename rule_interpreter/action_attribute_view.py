"""
In this file, the following requirements are covered:
REQ-3.1.3.1 Ruleset Syntax
REQ-3.1.3.2: Ruleset Syntax Validation
REQ-3.1.3.4: Relationship Creation
"""
import os
import sys
from models.validator import Validator
from models.action import Action
from models.attribute import Attribute
from models.entity import Entity
import pygame
import text_manipulation.ptext as ptext
import text_manipulation.pygame_textinput as pygame_textinput
from action_creation_view import ActionCreationView
from attribute_creation_view import AttributeCreationView
from entity_creation_view import EntityCreationView

class AttributeActionCreationView:
    def __init__(self, currentEntityType, fontsize):
        self._submitButtonImg = pygame.image.load('images/buttons/submit.png')
        self._arrowImg = pygame.image.load('images/buttons/arrow.png')
        self._plusImage = pygame.image.load('images/buttons/plussign.png')
        self._playing = True
        self._invalidSubmission = False
        self._action_view = False
        self._attribute_view = False
        self._currentEntityType = currentEntityType
        self._fontsize = fontsize
        self._editButtonImage = pygame.image.load('images/buttons/editButtonSmall.png')
        self._editButtonImageLarge = pygame.image.load('images/buttons/editButton.png')
        self._editActionList = []
        self._editAttributeList = []

    def get_entity_info(self):
        entityIdx = Validator().get_entity_idx(self._currentEntityType)
        if entityIdx != -1:
            return Validator().get_entities()[entityIdx]
        return -1

        
    def main(self):
        ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"
        entity = self.get_entity_info()
        entityIdx = Validator().get_entity_idx(self._currentEntityType)

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
                actionName, rule = ActionCreationView(self._fontsize, entity).main()
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
                    if x in range(57,240) and y in range(640,690):
                        entityTuple = EntityCreationView(self._fontsize).main(currentEntity)
                        if entityTuple[0] is not None:
                            Validator().update_entity(entityIdx, entityTuple[0], entityTuple[1], entityTuple[2], entityTuple[3], entityTuple[4])
                            self._currentEntityType = entityTuple[0]
                            entity = self.get_entity_info()
                            break
                    for joinIdx in range(len(self._editActionList)):
                        x1 = int(self._editActionList[joinIdx][0])
                        y1 = int(self._editActionList[joinIdx][1])
                        if x in range(x1, x1 + 100) and y in range(y1, y1+30):
                            entityIdx = Validator().get_entity_idx(self._currentEntityType)
                            action = Validator().get_entities()[entityIdx].get_actions()[joinIdx]
                            actionName = action.get_action_name()
                            ruleContent = action.get_rule_content()
                            newActionName, rule = ActionCreationView(self._fontsize, entity).main(actionName, ruleContent)
                            if newActionName is None or rule is None:
                                break
                            actionNames[joinIdx] = newActionName
                            Validator().update_action(entityIdx, joinIdx, newActionName, rule) 
                            break
                    
                    for joinIdx in range(len(self._editAttributeList)):
                        x1 = int(self._editAttributeList[joinIdx][0])
                        y1 = int(self._editAttributeList[joinIdx][1])
                        if x in range(x1, x1 + 100) and y in range(y1, y1+30):
                            entityIdx = Validator().get_entity_idx(self._currentEntityType)
                            attribute = Validator().get_entities()[entityIdx].get_attributes()[joinIdx]
                            attributeName = attribute.get_attribute_name()
                            attributeValue = attribute.get_attribute_value()
                            attrName, attrValue = AttributeCreationView(self._fontsize).main(attributeName, attributeValue)
                            if attrName is None or attrValue is None:
                                break
                            attributes[joinIdx] = attrName
                            Validator().update_attribute(entityIdx, joinIdx, attrName, attrValue)
                            break

            for rect, name, size in zip(buttonrects, buttonnames, textSizes):
                screen.fill(pygame.Color("#553300"), rect)
                screen.fill(pygame.Color("#332200"), rect.inflate(-8, -8))
                box = rect.inflate(-8, 100)
                ptext.draw(name, size, fontname="Bubblegum_Sans", color="white", owidth=0.5, fontsize=35)
                ptext.drawbox("", box, fontname="Bubblegum_Sans", color = "white", owidth=0.5)

            self._editActionList = []
            actionStr = ""
            actionNames = [action.get_action_name() for action in currentEntity.get_actions()]
            for actionIdx in range(len(actionNames)):
                actionStr += actionNames[actionIdx] + "\n"
                screen.blit(self._editButtonImage,(1000, 425 + actionIdx * 39))
                self._editActionList.append((1000, 425 + actionIdx * 39))
            ptext.draw(actionStr, (420, 420), fontname="Boogaloo", color="white", fontsize=30, width=570)

            self._editAttributeList = []
            attributeStr = ""
            attributes = [attribute.get_attribute_name() for attribute in currentEntity.get_attributes()]
            for attrIdx in range(len(attributes)):
                attributeStr += attributes[attrIdx] + "\n"
                screen.blit(self._editButtonImage,(1000, 65 + attrIdx * 39))
                self._editAttributeList.append((1000, 65 + attrIdx * 39))
            ptext.draw(attributeStr, (420, 60), fontname="Boogaloo", color="white", fontsize=30, width=570)

            if entity != -1:
                ptext.draw(entity.get_basic_entity_info_to_str(), (60, 60), fontname="Boogaloo", color="white", fontsize=20, width=290)
                screen.blit(self._editButtonImageLarge,(57, 640))

            pygame.display.flip()

