import os
import sys
sys.path.append('../')
from validator import Validator
from entity import Entity
from action import Action
from attribute import Attribute
from syntax_parser import SyntaxParser
sys.path.append('../../account')
from database import Database
sys.path.append('../rule_interpreter/rule_interpreter_view')
import pygame
import ptext
import pygame_textinput
from entity_creation_view import EntityCreationView
from action_attribute_view import AttributeActionCreationView
import pickle

class RulesetCreationEditView:
    def __init__(self):
        self._arrowImg = pygame.image.load('img/arrow.png')
        self._plusImage = pygame.image.load('img/plussign.png')
        self._moreButtonList = []
        self._database = Database("../../account/shallysdb.db")
        self._moreImage = pygame.image.load('img/moreButton.png')
        self._saveButtonImage = pygame.image.load('img/saveButton.png')
        self._exportButtonImage = pygame.image.load('img/exportButton.png')
        self._currentlySelected = False
        self._newRuleset = False
        self._entity_view = False
        self._playing = True
        self._attribute_action_view = False
        self._unvalid = False
        self._rulesetName = ""
        self._entities = [entity.get_name() for entity in Validator().get_entities()]
        self._invalidSubmission = False

    def save_ruleset(self, database, user, rulesetName, jsonBlob):
        self._database.cur.execute("SELECT MAX(ID) FROM Ruleset;")
        data = self._database.cur.fetchone()
        if data[0] is None:
            currentIdx = 0
        else: 
            currentIdx = data[0] + 1
        self._database.cur.execute("insert into Ruleset values(?, ?, ?, ?);", (currentIdx, user, rulesetName, jsonBlob,))
        self._database.conn.commit()

    def update_database(self, database, user, rulesetName, jsonBlob):
        self._database.cur.execute("UPDATE Ruleset SET rules = ? WHERE rulename = ?;", (jsonBlob, rulesetName, ))
        self._database.conn.commit()

    def main(self, rulesetName):
        if rulesetName == "":
            self._newRuleset = True
            self._entities = []
            Validator().clear_entities()
        else:
            self._rulesetName = rulesetName

        ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"

        pygame.init()

        sx, sy = 1300, 750
        screen = pygame.display.set_mode((sx, sy))
        pygame.display.set_caption("Main")

        buttonrects = [pygame.Rect((60, 175, 950, 500))]
        textSizes = [(60, 125)]
        if self._newRuleset:
            buttonrects.append(pygame.Rect((60, 50, 950, 50)))
            textSizes.append((60, 5))
        buttonnames = ["Entities", "Ruleset Name"]
        currentEntityName = ""

        if self._newRuleset == False:
            titleargs = ptext.draw("{}".format(rulesetName), midtop=(sx/2, 10), owidth=1.2, color = "0x884400", gcolor="0x442200", surf=None, cache = False, fontsize=64, fontname="CherryCreamSoda")

        while self._playing:
            screen.fill((0, 50, 50))
            screen.blit(self._plusImage,(960, 135))
            screen.blit(self._saveButtonImage,(1050, 160))
            screen.blit(self._exportButtonImage,(1050, 240))
            screen.blit(self._arrowImg,(10, 10))
            clickpos = None
            events = pygame.event.get()

            if self._entity_view == True:
                entityTuple = EntityCreationView().main()
                if entityTuple[0] is not None:
                    self._entities.append(entityTuple[0])
                    Validator().add_entity(Entity(entityTuple[0], entityTuple[1], entityTuple[2], entityTuple[3], entityTuple[4], entityTuple[5]))
                self._entity_view = False
            
            if self._attribute_action_view == True:
                AttributeActionCreationView(currentEntityName).main()
                self._attribute_action_view = False

            for event in events:
                if event.type == pygame.QUIT:
                    self._playing = False
                    exit()
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE:
                        self._playing = False
                        return
                    if event.key == pygame.K_DELETE:
                        screen.fill((0, 50, 50))
                        screen.blit(self._plusImage,(960, 135))
                        screen.blit(self._saveButtonImage,(1050, 160))
                        screen.blit(self._exportButtonImage,(1050, 240))
                        screen.blit(self._arrowImg,(10, 10))
                        self._rulesetName = self._rulesetName [:len(self._rulesetName)-1]
                
                    elif event.key == pygame.K_BACKSPACE:
                        screen.fill((0, 50, 50))
                        screen.blit(self._plusImage,(960, 135))
                        screen.blit(self._saveButtonImage,(1050, 160))
                        screen.blit(self._exportButtonImage,(1050, 240))
                        screen.blit(self._arrowImg,(10, 10))
                        self._rulesetName = self._rulesetName [:len(self._rulesetName)-1]

                    else:
                        # If no special key is pressed, add unicode of key to input_string
                        self._rulesetName += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self._currentlySelected = False
                    clickpos = event.pos
                    x, y = clickpos
                    if self._newRuleset == True:
                        if buttonrects[1].collidepoint(x,y):
                            self._currentlySelected = True
                    if x in range(10,40) and y in range(10,40):
                        return True
                    if x in range(960, 1000) and y in range(135, 175):
                        self._entity_view = True
                    #save button
                    if x in range(1050, 1200) and y in range(160, 200):
                        database = Database("../../account/shallysdb.db")
                        picklestring = pickle.dumps(Validator())
                        if self._newRuleset == False:
                            self.update_database(database, "shally", self._rulesetName, picklestring)
                        else:
                            if self._rulesetName == "":
                                self._invalidSubmission = True
                            else:
                                self.save_ruleset(database, "shally", self._rulesetName, picklestring)
                                self._newRuleset = False
                                if len(buttonrects) > 1:
                                    buttonrects.pop()
                                
                        titleargs = ptext.draw("{}".format(self._rulesetName), midtop=(sx/2, 10), owidth=1.2, color = "0x884400", gcolor="0x442200", surf=None, cache = False, fontsize=64, fontname="CherryCreamSoda")

                    for moreIdx in range(len(self._moreButtonList)):
                        x1 = int(self._moreButtonList[moreIdx][0])
                        y1 = int(self._moreButtonList[moreIdx][1])
                        if x in range(x1, x1 + 60) and y in range(y1, y1+30):
                            self._attribute_action_view = True
                            currentEntityName = self._entities[moreIdx]

            for rect, name, size in zip(buttonrects, buttonnames, textSizes):
                if self._currentlySelected == True and name == "Ruleset Name":
                    screen.fill(pygame.Color("#2693bf"), rect)
                else:
                    screen.fill(pygame.Color("#553300"), rect)
                screen.fill(pygame.Color("#332200"), rect.inflate(-8, -8))
                box = rect.inflate(-8, 100)
                ptext.draw(name, size, fontname="Bubblegum_Sans", color="white", owidth=0.5, fontsize=40)
                ptext.drawbox("", box, fontname="Bubblegum_Sans", color = "white", owidth=0.5)
            
            entites_str = ""
            self._moreButtonList = []
            for entityIdx in range(len(self._entities)):
                entites_str += self._entities[entityIdx] + "\n"
                screen.blit(self._moreImage,(900, 210 + entityIdx * 30 + entityIdx*0.05*100))
                self._moreButtonList.append((900, 210 + entityIdx * 30 + entityIdx*0.05*100))
            ptext.draw(entites_str, (70, 200), fontname="Boogaloo", color="white", fontsize=30)
            if self._newRuleset == True:
                ptext.draw(self._rulesetName, (70, 60), fontname="Boogaloo", color="white", fontsize=30)
            
            if self._invalidSubmission == True:
                ptext.draw("Ruleset name cannot be empty", (60, 690), fontname="Boogaloo", color="red", fontsize=30)

            if self._newRuleset == False:
                screen.blit(*titleargs)
            pygame.display.flip()



