
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
import pygame.locals as pl


parser = SyntaxParser()

print("Shally's dank test suite for the parser:\n")
print("adding entity goblin..")
goblin = Entity("goblin", "steve", 1)
print("adding atrributes for goblin: hp..")
testAttribute = Attribute("hp", 1, 1)
goblin.add_attribute(testAttribute)
print("adding actions for goblin: Attack..")
testAction = Action("Attack", 1)
goblin.add_action(testAction)
print("adding status for goblin: Dodge..")
goblin.add_status("Dodge")

class RuleInputView:
    def __init__(self):
        self._user_input = ""
        self._submitButtonImg = pygame.image.load('img/submit.png')
        self._checkmark = pygame.image.load('img/checkmark.png')
        self._arrowImg = pygame.image.load('img/arrow.png')
        self._errormark = pygame.image.load('img/errormark.png')
        self._playing = True
        self._invalidSubmission = False
        self._currentlySelected = False
        self._unvalid = False
        self._valid = False

    def main(self): 
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
        
        while self._playing:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        self._currentlySelected = False
                        if x in range(1100,1300) and y in range(600,750):
                            if parser.is_valid_rule(self._user_input) == True:
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
                ptext.draw(name, size, fontname="Bubblegum_Sans", color="white", owidth=0.5, fontsize=40)
                ptext.drawbox("", box, fontname="Bubblegum_Sans", color = "white", owidth=0.5)
                
            ptext.draw(self._user_input, (70, 170), fontname="Boogaloo", color="white", fontsize=30)

            if self._unvalid == True:
                screen.blit(self._errormark,(350,100))
            
            if self._valid == True:
                screen.blit(self._checkmark,(450,150))

            pygame.display.flip()