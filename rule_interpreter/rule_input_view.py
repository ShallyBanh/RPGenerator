
import os
import sys
from models.validator import Validator
from models.action import Action
from models.attribute import Attribute
from models.entity import Entity
from models.syntax_parser import SyntaxParser
import pygame
import ptext
import pygame.locals as pl

class RuleInputView:
    def __init__(self, fontsize):
        self._user_input = ""
        self._submitButtonImg = pygame.image.load('images/buttons/submit.png')
        self._checkmark = pygame.image.load('images/buttons/checkmark.png')
        self._arrowImg = pygame.image.load('images/buttons/arrow.png')
        self._errormark = pygame.image.load('images/buttons/errormark.png')
        self._playing = True
        self._invalidSubmission = False
        self._currentlySelected = False
        self._unvalid = False
        self._valid = False
        self._fontsize = fontsize
        self._parser = SyntaxParser()

    def main(self, ruleContent = ""): 
        if ruleContent != "":
            self._user_input = str(ruleContent)
        ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"
        pygame.transform.scale(self._submitButtonImg, (10, 10))
        pygame.transform.scale(self._checkmark, (100, 100))
        pygame.transform.scale(self._errormark, (100, 100))

        screen = pygame.display.set_mode((1300, 750))
        screen.fill((0, 50, 50))
        screen.blit(self._submitButtonImg,(1100, 600))
        screen.blit(self._arrowImg,(10, 10))
        buttonrects = [pygame.Rect((50, 150, 1000, 550))]
        textSizes = [(50, 100)]
        buttonnames = ["Rule"]
        print("in rule input view")
        print(Validator().get_entities())
        
        while self._playing:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        self._currentlySelected = False
                        if x in range(1100,1300) and y in range(600,750):
                            if self._parser.is_valid_rule(self._user_input, Validator()) == True:
                                self._valid = True
                                return self._user_input
                            else:
                                self._unvalid = True
                        
                        if x in range(10,40) and y in range(10,40):
                            self._playing = False
                            return None

                        if buttonrects[0].collidepoint(x,y):
                            self._currentlySelected = True
                            self._unvalid = False
                            screen.fill((0, 50, 50))
                            screen.blit(self._submitButtonImg,(1100, 600))
                            screen.blit(self._arrowImg,(10, 10))

                if event.type == pygame.KEYDOWN:
                    self._unvalid = False
                    screen.fill((0, 50, 50))
                    screen.blit(self._submitButtonImg,(1100, 600))
                    screen.blit(self._arrowImg,(10, 10))
                    if event.key == pygame.K_RETURN:
                        self._user_input += "\n"
                    
                    elif event.key == pygame.K_DELETE:
                        screen.fill((0, 50, 50))
                        screen.blit(self._arrowImg,(10, 10))
                        screen.blit(self._submitButtonImg,(1100, 600))
                        self._user_input = self._user_input[:len(self._user_input)-1]
                    
                    elif event.key == pygame.K_BACKSPACE:
                        screen.fill((0, 50, 50))
                        screen.blit(self._arrowImg,(10, 10))
                        screen.blit(self._submitButtonImg,(1100, 600))
                        self._user_input = self._user_input[:len(self._user_input)-1]

                    else:
                        # If no special key is pressed, add unicode of key to input_string
                        self._user_input += event.unicode

            for rect, name, size in zip(buttonrects, buttonnames, textSizes):
                if self._currentlySelected == False:
                    screen.fill(pygame.Color("#553300"), rect)
                else: 
                    screen.fill(pygame.Color("#2693bf"), rect)
                screen.fill(pygame.Color("#332200"), rect.inflate(-8, -8))
                box = rect.inflate(-16, 16)
                ptext.draw(name, size, fontname="Bubblegum_Sans", color="white", owidth=0.5, fontsize=35)
                ptext.drawbox("", box, fontname="Bubblegum_Sans", color = "white", owidth=0.5)
                
            ptext.draw(self._user_input, (70, 170), fontname="Boogaloo", color="white", fontsize=35)

            if self._unvalid == True:
                screen.blit(self._errormark,(350,100))
            
            if self._valid == True:
                screen.blit(self._checkmark,(450,150))

            pygame.display.flip()