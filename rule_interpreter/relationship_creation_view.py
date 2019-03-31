
import os
import sys
from models.validator import Validator
from models.action import Action
from models.attribute import Attribute
from models.entity import Entity
from models.relationship import Relationship
import pygame
import ptext
import pygame.locals as pl
import pygame_textinput
from rule_input_view import RuleInputView


class RelationshipCreationView:
    def __init__(self, fontsize):
        self._rule = ""
        self._submitButtonImg = pygame.image.load('img/submit.png')
        self._arrowImg = pygame.image.load('img/arrow.png')
        self._plusImage = pygame.image.load('img/plussign.png')
        self._playing = True
        self._invalidSubmission = False
        self._currentlySelectedColorList = ["#553300", "#553300", "#553300", "#553300", "#553300", "#553300"]
        #Action name and then rule content
        self._allInputList = ["", ""]
        self._currentlySelectedInputIdx = 0
        self._fontsize = fontsize

    def main(self):
        ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"

        pygame.init()

        sx, sy = 1300, 750
        screen = pygame.display.set_mode((sx, sy))
        pygame.display.set_caption("Action Creation")

        buttonrects = [pygame.Rect((50, 150, 1000, 70)), pygame.Rect((50, 325, 1000, 350))]
        textSizes = [(50, 100 + 170 * j) for j in range(2)]
        buttonnames = ["Relationship Name", "Relationship"]
        titleargs = ptext.draw("Relationship Creation", midtop=(sx/2, 10), owidth=1.2, color = "0x884400", gcolor="0x442200", surf=None, cache = False, fontsize=64, fontname="CherryCreamSoda")

        while self._playing:
            clickpos = None
            events = pygame.event.get()

            screen.fill((0, 50, 50))
            screen.blit(self._submitButtonImg,(1100, 600))
            screen.blit(self._plusImage,(1010, 290))
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
                            if j == 0:
                                self._currentlySelectedColorList = ["#553300", "#553300"]
                                self._currentlySelectedColorList[j] = "#2693bf"
                            self._currentlySelectedInputIdx = j

                    if x in range(1100,1300) and y in range(600, 750):
                        if self._allInputList[0] == "" or self._rule == "":
                            self._invalidSubmission = True
                        else:
                            self._playing = False
                            return self._allInputList[0], self._rule
                    
                    if x in range(10,40) and y in range(10,40):
                        self._playing = False
                        return None, None
                    
                    if x in range (1010, 1050) and y in range (290, 320):
                        rule_input = RuleInputView(self._fontsize).main()
                        if rule_input is not None:
                            self._rule = rule_input

            for rect, name, size, color in zip(buttonrects, buttonnames, textSizes, self._currentlySelectedColorList):
                screen.fill(pygame.Color(color), rect)
                screen.fill(pygame.Color("#332200"), rect.inflate(-8, -8))
                box = rect.inflate(-16, 16)
                ptext.draw(name, size, fontname="Bubblegum_Sans", color="white", owidth=0.5, fontsize=35)
                ptext.drawbox("", box, fontname="Bubblegum_Sans", color = "white", owidth=0.5)

            
            if self._invalidSubmission == True:
                ptext.draw("Both fields must be complete in order to submit", (60, 700), fontname="Boogaloo", color="red", fontsize=35)

            ptext.draw(self._rule, (60, 345), fontname="Boogaloo", color="white", fontsize=35)
            ptext.draw(self._allInputList[0], (60, 165 + 185 * 0), fontname="Boogaloo", color="white", fontsize=35)

            
            screen.blit(*titleargs)
            pygame.display.flip()
