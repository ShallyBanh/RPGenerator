
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

img = pygame.image.load('img/submit.png')
checkmark = pygame.image.load('img/checkmark.png')
errormark = pygame.image.load('img/errormark.png')
pygame.transform.scale(img, (10, 10))
pygame.transform.scale(checkmark, (100, 100))
pygame.transform.scale(errormark, (100, 100))

screen = pygame.display.set_mode((1200, 700))
screen.fill((255, 255, 255))
screen.blit(img,(1000, 550))

user_input = "" 

pygame.display.flip()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)
                if mouse_pos[0] in range(1000,1200) and mouse_pos[1] in range(550,700):
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
                    print(parser.is_valid_rule("\"{}\"".format(user_input)))
                    if parser.is_valid_rule(user_input) == True:
                        screen.blit(checkmark,(450,150))
                        print("valid")
                    else:
                        screen.blit(errormark,(350,100))

                    print(user_input)

        if event.type == pygame.KEYDOWN:

            if event.key == pl.K_RETURN:
                user_input += "\n"
            
            elif event.key == pl.K_DELETE:
                screen.fill((255, 255, 255))
                print(user_input)
                screen.blit(img,(1000, 550))
                user_input = user_input[:len(user_input)-1]
            
            elif event.key == pl.K_BACKSPACE:
                screen.fill((255, 255, 255))
                print(user_input)
                screen.blit(img,(1000, 550))
                user_input = user_input[:len(user_input)-1]

            else:
                # If no special key is pressed, add unicode of key to input_string
                user_input += event.unicode
        
        ptext.draw(user_input, (0, 0), fontname="fonts/Boogaloo.ttf", color=(0,0,0), fontsize=30)

    pygame.display.update()
