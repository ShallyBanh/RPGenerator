
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
import pygame_textinput
import rule_input_view as ruleInputView


def main():
    rule = ""
    plusImage = pygame.image.load('img/plussign.png')
    ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"
    actionNameInput = pygame_textinput.TextInput()
    img = pygame.image.load('img/submit.png')
    arrowImg = pygame.image.load('img/arrow.png')

    pygame.init()

    sx, sy = 800, 600
    screen = pygame.display.set_mode((sx, sy))
    pygame.display.set_caption("Action Creation")

    buttonrects = [pygame.Rect((50, 150, 500, 70)), pygame.Rect((50, 325, 500, 170))]
    textSizes = [(50, 100 + 170 * j) for j in range(2)]
    buttonnames = ["Action Name", "Rule"]
    size = ""

    titleargs = ptext.draw("Action Creation", midtop=(sx/2, 10), owidth=1.2, color = "0x884400", gcolor="0x442200", surf=None, cache = False, fontsize=64, fontname="CherryCreamSoda")
    didSelectActionNameInputBox= False 
    playing = True

    while playing:
        clickpos = None
        events = pygame.event.get()

        screen.fill((0, 50, 50))
        screen.blit(img,(600, 450))
        screen.blit(plusImage,(510, 290))
        screen.blit(arrowImg,(10, 10))

        for event in events:
            if event.type == pygame.QUIT:
                playing = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                playing = False
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clickpos = event.pos
                x, y = clickpos
                didSelectActionNameInputBox = False
                for j in range(len(buttonrects)):
                    rect = buttonrects[j]
                    if rect.collidepoint(x,y):
                        if j == 0:
                            didSelectActionNameInputBox = True

                if x in range(600,800) and y in range(450,600):
                    playing = False
                    return actionNameInput.get_text(), rule
                
                if x in range(10,40) and y in range(10,40):
                    playing = False
                    return None, None
                
                if x in range (510, 540) and y in range (290, 320):
                    rule_input = ruleInputView.main()
                    if rule_input is not None:
                        rule = rule_input

        for rect, name, size in zip(buttonrects, buttonnames, textSizes):
            screen.fill(pygame.Color("#553300"), rect)
            screen.fill(pygame.Color("#332200"), rect.inflate(-8, -8))
            box = rect.inflate(-16, 16)
            ptext.draw(name, size, fontname="Bubblegum_Sans", color="white", owidth=0.5, fontsize=40)
            ptext.drawbox("", box, fontname="Bubblegum_Sans", color = "white", owidth=0.5)

        if didSelectActionNameInputBox == True:
            actionNameInput.update(events)

        screen.blit(actionNameInput.get_surface(), (60, 165 + 185 * 0))
        ptext.draw(rule, (60, 345), fontname="Boogaloo", color=(0,0,0), fontsize=20)
        
        screen.blit(*titleargs)
        pygame.display.flip()
    
    print("out of while loop")
