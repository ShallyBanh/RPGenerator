import os
import sys
from models.validator import Validator
from models.action import Action
from models.attribute import Attribute
from models.entity import Entity
import pygame
import ptext
import pygame_textinput
from ruleset_creation_edit_view import RulesetCreationEditView
import jsonpickle
sys.path.append('/account/')
from account.database import Database
from account.account_manager import AccountManager
from client import Client


class RulesetView:
    def __init__(self, username, client, fontsize):
        self._submitButtonImg = pygame.image.load("img/submit.png")
        self._arrowImg = pygame.image.load('img/arrow.png')
        self._plusImage = pygame.image.load('img/plussign.png')
        self._editButton = pygame.image.load('img/editButton.png')
        self._editButtonList = []
        self._playing = True
        self._edit_ruleset_view = False
        self._create_ruleset_view = False
        self._database = Database("database.db")
        self._dbManager = AccountManager
        self._rulesetList = []
        self._rulesetPositionList =[]
        self._client = client
        self._username = username
        self._fontsize = fontsize

    def main(self):
        ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"

        pygame.init()
        self._rulesetList = self._client.load_existing_rulesets(self._username)

        sx, sy = 1300, 750
        screen = pygame.display.set_mode((sx, sy))
        pygame.display.set_caption("Rulesets")
        titleargs = ptext.draw("Existing Rulesets", midtop=(sx/2, 10), owidth=1.2, color = "0x884400", gcolor="0x442200", surf=None, cache = False, fontsize=self._fontsize*2, fontname="CherryCreamSoda")

        buttonrects = [pygame.Rect((50, 150, 1100, 550))]
        textSizes = [(50, 100)]
        buttonnames = ["Rulesets"]

        while self._playing:
            screen.fill((0, 50, 50))
            screen.blit(self._plusImage,(1110, 110))
            screen.blit(self._arrowImg,(10, 10))
            clickpos = None
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self._playing = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self._playing = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clickpos = event.pos
                    x, y = clickpos
                    if x in range(1110, 1150) and y in range(110, 140):
                        validator = RulesetCreationEditView( self._username, self._client, self._fontsize).main("")
                        if validator is not None:
                            return validator
                        self._rulesetList = self._client.load_existing_rulesets(self._username)
                    if x in range(10,40) and y in range(10,40):
                        self._playing = False
                    for editIdx in range(len(self._rulesetPositionList)):
                        x1 = int(self._rulesetPositionList[editIdx][0])
                        y1 = int(self._rulesetPositionList[editIdx][1])
                        if x in range(x1, x1 + 200) and y in range(y1, y1+60):
                            rule = self._rulesetList[editIdx][1]
                            deserializedValidator = jsonpickle.decode(rule)
                            Validator().clear_entities()
                            Validator().set_entities(deserializedValidator.get_entities())
                            Validator().set_relationships(deserializedValidator.get_relationships())
                            validator = RulesetCreationEditView(self._username, self._client, self._fontsize).main(self._rulesetList[editIdx][0])
                            if validator is not None:
                                return validator
                            self._rulesetList = self._client.load_existing_rulesets(self._username)

            for rect, name, size in zip(buttonrects, buttonnames, textSizes):
                screen.fill(pygame.Color("#553300"), rect)
                screen.fill(pygame.Color("#332200"), rect.inflate(-8, -8))
                box = rect.inflate(-8, 100)
                ptext.draw(name, size, fontname="Bubblegum_Sans", color="white", owidth=0.5, fontsize=self._fontsize)
                ptext.drawbox("", box, fontname="Bubblegum_Sans", color = "white", owidth=0.5)
            
            ruleNamesString = ""
            self._rulesetPositionList = []
            for ruleIdx in range(len(self._rulesetList)):
                ruleNamesString += self._rulesetList[ruleIdx][0] + "\n\n"
                screen.blit(self._editButton,(900, 210 + ruleIdx * 50 + ruleIdx*0.17*100))
                self._rulesetPositionList.append((900, 210 + ruleIdx * 50 + ruleIdx*0.17*100))
            ptext.draw(ruleNamesString, (70, 200), fontname="Boogaloo", color="white", fontsize=self._fontsize)
            
            screen.blit(*titleargs)
            pygame.display.flip()



