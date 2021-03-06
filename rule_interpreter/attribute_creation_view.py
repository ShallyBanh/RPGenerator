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


class AttributeCreationView:

    def __init__(self, fontsize):
        self._submitButtonImg = pygame.image.load('images/buttons/submit.png')
        self._arrowImg = pygame.image.load('images/buttons/arrow.png')
        self._playing = True
        self._invalidSubmission = False
        self._currentlySelectedColorList = ["#553300", "#553300", "#553300"]
        #attribute name, attribute type and attribute value
        self._allInputList = ["", ""]
        self._currentlySelectedInputIdx = 0
        self._fontsize = fontsize

    def main(self, attrName = "", attrValue = ""):
        if attrName != "" and attrValue != "":
            self._allInputList = [str(attrName), str(attrValue)]
        ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"
        pygame.init()

        sx, sy = 1300, 750
        screen = pygame.display.set_mode((sx, sy))
        pygame.display.set_caption("Attribute Creation")

        buttonrects = [pygame.Rect((50, 150 + 160 * j, 1100, 70)) for j in range(2)]
        textSizes = [(50, 100 + 155 * j) for j in range(2)]
        buttonnames = ["Attribute Name", "Attribute Value"]

        titleargs = ptext.draw("Attribute Creation", midtop=(sx/2, 10), color = "0xc0c0c0", gcolor="0xF3F3F3", surf=None, cache = False, fontsize=64, fontname="CherryCreamSoda")

        while self._playing:
            clickpos = None
            events = pygame.event.get()

            screen.fill((0, 50, 50))
            screen.blit(self._submitButtonImg,(1100, 600))
            screen.blit(self._arrowImg,(10, 10))

            for event in events:
                if event.type == pygame.QUIT:
                    self._playing = False
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
                            self._currentlySelectedColorList = ["#553300", "#553300", "#553300"]
                            self._currentlySelectedColorList[j] = "#2693bf"
                            self._currentlySelectedInputIdx = j

                    if x in range(10,40) and y in range(10,40):
                        self._playing = False
                        return None, None

                    if x in range(1100,1300) and y in range(600,750):
                        if self._allInputList[0] == "" or self._allInputList[1] == "":
                            self._invalidSubmission = True
                        else:
                            self._playing = False
                            return self._allInputList[0], self._allInputList[1]

            for rect, name, size, color in zip(buttonrects, buttonnames, textSizes, self._currentlySelectedColorList):
                screen.fill(pygame.Color(color), rect)
                screen.fill(pygame.Color("#332200"), rect.inflate(-8, -8))
                box = rect.inflate(-16, 16)
                ptext.draw(name, size, fontname="Bubblegum_Sans", color="white", owidth=0.5, fontsize=35)
                ptext.drawbox("", box, fontname="Bubblegum_Sans", color = "white", owidth=0.5)

            if self._invalidSubmission == True:
                ptext.draw("All fields must be complete in order to submit", (60, 555), fontname="Boogaloo", color="red", fontsize=35)

            ptext.draw(self._allInputList[0], (60, 165 + 185 * 0), fontname="Boogaloo", color="white", fontsize=35, width=1050)
            ptext.draw(self._allInputList[1], (60, 150 + 185 * 1), fontname="Boogaloo", color="white", fontsize=35, width=1050)
            
            screen.blit(*titleargs)
            pygame.display.flip()



