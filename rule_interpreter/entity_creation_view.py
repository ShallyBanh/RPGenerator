"""
In this file, the following requirements are covered:
REQ-3.1.3.1 Ruleset Syntax
REQ-3.1.3.2: Ruleset Syntax Validation
REQ-3.1.3.3: Entity Creation
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

class EntityCreationView:

    def __init__(self, fontsize):
        self._entityNameInput = ""
        self._entityTypeInput = ""
        self._widthInput = ""
        self._heightInput = ""
        self._isTemplateInput = ""
        self._inheritanceInput = ""
        self._submitButtonImg = pygame.image.load('images/buttons/submit.png')
        self._arrowImg = pygame.image.load('images/buttons/arrow.png')
        self._playing = True
        self._invalidSubmission = False
        self._currentlySelectedColorList = ["#553300", "#553300", "#553300", "#553300", "#553300", "#553300"]
        self._allInputList = [self._entityTypeInput, self._widthInput, self._heightInput, self._isTemplateInput, self._inheritanceInput]
        self._currentlySelectedInputIdx = 0
        self._invalidSubmissionText = "All fields must be complete in order to submit"
        self._fontsize = fontsize

    def does_entity_with_type_exist(self, entityType):
        allEntities = Validator().get_entities()
        for entity in allEntities:
            if entity.get_type() == entityType:
                return True
        return False
    
    def get_entity_with_type(self, entityType):
        allEntities = Validator().get_entities()
        for entity in allEntities:
            if entity.get_type() == entityType:
                return entity
        return None

    def main(self, currentEntity = None):
        if currentEntity is not None:
            self._allInputList = [currentEntity.get_type(), currentEntity.get_size().get_width_as_string(), currentEntity.get_size().get_height_as_string(), str(currentEntity.get_is_template()), "none"]

        ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"
        pygame.init()
        sx, sy = 1300, 750
        screen = pygame.display.set_mode((sx, sy))
        pygame.display.set_caption("Entity Creation")

        buttonrects = [pygame.Rect((50, 150, 500, 70)), pygame.Rect((50, 150 + 160 * 1, 500, 70)), pygame.Rect((50, 150 + 160 * 2, 500, 70)), pygame.Rect((50, 150 + 160 * 3, 500, 70)), pygame.Rect((600, 150, 500, 70))]
        textSizes = [(50, 100), (50, 100 + 155 * 1), (50, 100 + 155 * 2), (50, 100 + 155 * 3), (600, 100)]
        buttonnames = ["Entity Type", "Width", "Height", "Is Template?", "Is Inherited From?"]
        size = ""
        titleargs = ptext.draw("Entity Creation", midtop=(sx/2, 10), color = "0xc0c0c0", gcolor="0xF3F3F3", surf=None, cache = False, fontsize=64, fontname="CherryCreamSoda")

        while self._playing:
            clickpos = None
            events = pygame.event.get()

            screen.fill((0, 50, 50))
            screen.blit(self._submitButtonImg,(1100, 600))
            screen.blit(self._arrowImg,(10, 10))

            for event in events:
                if event.type == pygame.QUIT:
                    self._playing = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self._playing = False
                    return
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE:
                        self._playing = False
                        return
                    if event.key == pygame.K_DELETE:
                        screen.fill((0, 50, 50))
                        screen.blit(self._submitButtonImg,(1100, 600))
                        screen.blit(self._arrowImg,(10, 10))
                        self._allInputList[self._currentlySelectedInputIdx] = self._allInputList[self._currentlySelectedInputIdx] [:len(self._allInputList[self._currentlySelectedInputIdx])-1]
                
                    elif event.key == pygame.K_BACKSPACE:
                        screen.fill((0, 50, 50))
                        screen.blit(self._submitButtonImg,(1100, 600))
                        screen.blit(self._arrowImg,(10, 10))
                        self._allInputList[self._currentlySelectedInputIdx] = self._allInputList[self._currentlySelectedInputIdx] [:len(self._allInputList[self._currentlySelectedInputIdx])-1]

                    else:
                        # If no special key is pressed, add unicode of key to input_string
                        self._allInputList[self._currentlySelectedInputIdx] += event.unicode

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self._invalidSubmission = False
                    clickpos = event.pos
                    x, y = clickpos
                    for j in range(len(buttonrects)):
                        rect = buttonrects[j]
                        if rect.collidepoint(x,y):
                            self._currentlySelectedColorList = ["#553300", "#553300", "#553300", "#553300", "#553300", "#553300"]
                            self._currentlySelectedColorList[j] = "#2693bf"
                            self._currentlySelectedInputIdx = j
                            
                    if x in range(10,40) and y in range(10,40):
                        self._playing = False
                        return None, None, None, None, None
                    if x in range(1100,1300) and y in range(600,750):
                        if self._allInputList[0] == "" or self._allInputList[1] == "" or self._allInputList[2]== "" or self._allInputList[3]== "":
                            self._invalidSubmission = True
                            self._invalidSubmissionText = "All fields must be complete in order to submit"
                        elif self._allInputList[1].isdigit() == False or self._allInputList[2].isdigit() == False :
                            self._invalidSubmission = True
                            self._invalidSubmissionText = "Width and Height fields must be a number"
                        elif self._allInputList[0].find(" ") != -1: 
                            self._invalidSubmission = True
                            self._invalidSubmissionText = "Cannot have spaces in entity type"
                        elif self._allInputList[3].lower() != "false" and self._allInputList[3].lower() != "true" :
                            self._invalidSubmission = True
                            self._invalidSubmissionText = "isTemplate must be true or false"
                        elif self.does_entity_with_type_exist(self._allInputList[4]) == False and self._allInputList[4].lower() != "none":
                            self._invalidSubmission = True
                            self._invalidSubmissionText = "No such inherited type. If none type None."
                        else:
                            if self._allInputList[3].lower() == "false":
                                isTemplate = False
                            else:
                                isTemplate = True
                            self._playing = False
                            return self._allInputList[0], self._allInputList[1], self._allInputList[2], isTemplate, self.get_entity_with_type(self._allInputList[4])

            for rect, name, size, color in zip(buttonrects, buttonnames, textSizes, self._currentlySelectedColorList):
                screen.fill(pygame.Color(color), rect)
                screen.fill(pygame.Color("#332200"), rect.inflate(-8, -8))
                box = rect.inflate(-16, 16)
                ptext.draw(name, size, fontname="Bubblegum_Sans", color="white", owidth=0.5, fontsize=35)
                ptext.drawbox("", box, fontname="Bubblegum_Sans", color = "white", owidth=0.5)
            
            if self._invalidSubmission == True:
                ptext.draw(self._invalidSubmissionText, (615, 500), fontname="Boogaloo", color="red", fontsize=35)


            ptext.draw(self._allInputList[0], (60, 165 + 185 * 0), fontname="Boogaloo", color="white", fontsize=35, width=490)
            ptext.draw(self._allInputList[1], (60, 145 + 185 * 1), fontname="Boogaloo", color="white", fontsize=35, width=490)
            ptext.draw(self._allInputList[2], (60, 125 + 185 * 2), fontname="Boogaloo", color="white", fontsize=35, width=490)
            ptext.draw(self._allInputList[3], (60, 100 + 185 * 3), fontname="Boogaloo", color="white", fontsize=35, width=490)
            ptext.draw(self._allInputList[4], (610, 165 + 185 * 0), fontname="Boogaloo", color="white", fontsize=35, width=490)

            screen.blit(*titleargs)
            pygame.display.flip()