import os
import sys
sys.path.append('/account/')
from account.database import Database
from account.account_manager import AccountManager
from client import Client
from models.validator import Validator
from models.action import Action
from models.attribute import Attribute
from models.entity import Entity
import pygame
import ptext
import pygame_textinput
from entity_creation_view import EntityCreationView
from action_attribute_view import AttributeActionCreationView
from relationship_creation_view import RelationshipCreationView
import pickle

class RulesetCreationEditView:
    def __init__(self, username, client):
        self._arrowImg = pygame.image.load('img/arrow.png')
        self._plusImage = pygame.image.load('img/plussign.png')
        self._moreButtonList = []
        self._database = Database("database.db")
        self._moreImage = pygame.image.load('img/moreButton.png')
        self._saveButtonImage = pygame.image.load('img/saveButton.png')
        self._exportButtonImage = pygame.image.load('img/exportButton.png')
        self._currentlySelected = False
        self._newRuleset = False
        self._entity_view = False
        self._relationship_view = False
        self._playing = True
        self._attribute_action_view = False
        self._unvalid = False
        self._rulesetName = ""
        self._entities = [entity.get_name() for entity in Validator().get_entities()]
        self._relationships = [relationship.get_name() for relationship in Validator().get_relationships()]
        self._invalidSubmission = False
        self._client = client
        self._username = username

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

        buttonrects = [pygame.Rect((60, 175, 575, 500)), pygame.Rect((650, 175, 575, 500))]
        textSizes = [(60, 125), (650, 125)]
        if self._newRuleset:
            buttonrects.append(pygame.Rect((60, 50, 575, 50)))
            textSizes.append((60, 5))
        buttonnames = ["Entities", "Relationship Name", "Ruleset Name"]
        currentEntityName = ""

        if self._newRuleset == False:
            titleargs = ptext.draw("{}".format(rulesetName), midtop=(sx/2, 10), owidth=1.2, color = "0x884400", gcolor="0x442200", surf=None, cache = False, fontsize=64, fontname="CherryCreamSoda")

        while self._playing:
            screen.fill((0, 50, 50))
            screen.blit(self._plusImage,(565, 135))
            screen.blit(self._plusImage,(1200, 135))
            screen.blit(self._saveButtonImage,(1100, 10))
            screen.blit(self._exportButtonImage,(1100, 70))
            screen.blit(self._arrowImg,(10, 10))
            clickpos = None
            events = pygame.event.get()

            if self._entity_view == True:
                entityTuple = EntityCreationView().main()
                if entityTuple[0] is not None:
                    self._entities.append(entityTuple[0])
                    Validator().add_entity(Entity(entityTuple[0], entityTuple[1], entityTuple[2], entityTuple[3], entityTuple[4], entityTuple[5]))
                self._entity_view = False

            if self._relationship_view == True:
                relationshipTuple = RelationshipCreationView().main()
                if relationshipTuple[0] is not None:
                    self._relationships.append(relationshipTuple[0])
                    Validator().add_relationship(Relationship(relationshipTuple[0], relationshipTuple[1]))
                self._relationship_view = False
            
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
                        screen.blit(self._plusImage,(565, 135))
                        screen.blit(self._plusImage,(1200, 135))
                        screen.blit(self._saveButtonImage,(1100, 10))
                        screen.blit(self._exportButtonImage,(1100, 70))
                        screen.blit(self._arrowImg,(10, 10))
                        self._rulesetName = self._rulesetName [:len(self._rulesetName)-1]
                
                    elif event.key == pygame.K_BACKSPACE:
                        screen.fill((0, 50, 50))
                        screen.blit(self._plusImage,(565, 135))
                        screen.blit(self._plusImage,(1200, 135))
                        screen.blit(self._saveButtonImage,(1100, 10))
                        screen.blit(self._exportButtonImage,(1100, 70))
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
                        if buttonrects[2].collidepoint(x,y):
                            self._currentlySelected = True
                    if x in range(10,40) and y in range(10,40):
                        return
                    if x in range(565, 600) and y in range(135, 175):
                        self._entity_view = True
                    if x in range(1200, 1250) and y in range(135, 175):
                        self._relationship_view = True
                    #save button
                    if x in range(1100, 1300) and y in range(10, 60):
                        picklestring = pickle.dumps(Validator())
                        if self._newRuleset == False:
                            self.update_database(database, "shally", self._rulesetName, picklestring)
                        else:
                            if self._rulesetName == "":
                                self._invalidSubmission = True
                            else:
                                self._client.create_ruleset(self._username, self._rulesetName, picklestring)
                                self._newRuleset = False
                                if len(buttonrects) > 1:
                                    buttonrects.pop()
                                
                        titleargs = ptext.draw("{}".format(self._rulesetName), midtop=(sx/2, 10), owidth=1.2, color = "0x884400", gcolor="0x442200", surf=None, cache = False, fontsize=64, fontname="CherryCreamSoda")

                    #fake export button for andrew to shoot out an object for him
                    if x in range(1100, 1300) and y in range(70, 130):
                        return Validator()

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
                screen.blit(self._moreImage,(465, 210 + entityIdx * 30 + entityIdx*0.05*100))
                self._moreButtonList.append((465, 210 + entityIdx * 30 + entityIdx*0.05*100))
            ptext.draw(entites_str, (70, 200), fontname="Boogaloo", color="white", fontsize=30)


            relationship_str = ""
            for relationshipIdx in range(len(self._relationships)):
                relationship_str += self._relationships[relationshipIdx] + "\n"
            ptext.draw(relationship_str, (660, 200), fontname="Boogaloo", color="white", fontsize=30)

            if self._newRuleset == True:
                ptext.draw(self._rulesetName, (70, 60), fontname="Boogaloo", color="white", fontsize=30)
            
            if self._invalidSubmission == True:
                ptext.draw("Ruleset name cannot be empty", (60, 690), fontname="Boogaloo", color="red", fontsize=30)

            if self._newRuleset == False:
                screen.blit(*titleargs)
            pygame.display.flip()



