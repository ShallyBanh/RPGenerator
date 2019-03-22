
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

def main(): 
    ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"
    img = pygame.image.load('img/submit.png')
    checkmark = pygame.image.load('img/checkmark.png')
    errormark = pygame.image.load('img/errormark.png')
    pygame.transform.scale(img, (10, 10))
    pygame.transform.scale(checkmark, (100, 100))
    pygame.transform.scale(errormark, (100, 100))
    arrowImg = pygame.image.load('img/arrow.png')

    screen = pygame.display.set_mode((1300, 750))
    screen.fill((0, 50, 50))
    screen.blit(img,(1100, 600))

    buttonrects = [pygame.Rect((50, 150, 1000, 550))]
    textSizes = [(50, 100)]
    buttonnames = ["Rule"]

    user_input = "" 
    unvalid = False
    valid = False

    pygame.display.flip()
    playing = True
    while playing:
        screen.blit(arrowImg,(10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    print(mouse_pos)
                    if mouse_pos[0] in range(1100,1300) and mouse_pos[1] in range(600,750):
                        if parser.is_valid_rule(user_input) == True:
                            valid = True
                            return user_input
                        else:
                            unvalid = True
                    
                    if mouse_pos[0] in range(10,40) and mouse_pos[1] in range(10,40):
                        playing = False
                        return None

            if event.type == pygame.KEYDOWN:
                unvalid = False
                screen.fill((0, 50, 50))
                screen.blit(img,(1100, 600))
                if event.key == pl.K_RETURN:
                    user_input += "\n"
                
                elif event.key == pl.K_DELETE:
                    screen.fill((0, 50, 50))
                    screen.blit(img,(1100, 600))
                    user_input = user_input[:len(user_input)-1]
                
                elif event.key == pl.K_BACKSPACE:
                    screen.fill((0, 50, 50))
                    screen.blit(img,(1100, 600))
                    user_input = user_input[:len(user_input)-1]

                else:
                    # If no special key is pressed, add unicode of key to input_string
                    user_input += event.unicode

        for rect, name, size in zip(buttonrects, buttonnames, textSizes):
            screen.fill(pygame.Color("#553300"), rect)
            screen.fill(pygame.Color("#332200"), rect.inflate(-8, -8))
            box = rect.inflate(-16, 16)
            ptext.draw(name, size, fontname="Bubblegum_Sans", color="white", owidth=0.5, fontsize=40)
            ptext.drawbox("", box, fontname="Bubblegum_Sans", color = "white", owidth=0.5)
            
        ptext.draw(user_input, (70, 170), fontname="Boogaloo", color="white", fontsize=30)

        if unvalid == True:
            screen.blit(errormark,(350,100))
        
        if valid == True:
            screen.blit(checkmark,(450,150))

        pygame.display.flip()
