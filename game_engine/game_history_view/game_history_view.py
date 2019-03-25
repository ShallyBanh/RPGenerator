import os
import sys
import pygame
import pickle
# sys.path.append('../../account')
# from database import Database
import ptext


class GameHistoryView:
    def __init__(self):
        self._joinButtonImage = pygame.image.load('img/joinButton.png')
        self._joinButtonList = []
        self._playing = True
        self._gameHistoryList = []
        self._gameHistoryPositionList =[]
        self._arrowImg = pygame.image.load('img/arrow.png')
    
    def load_game_history(self):
        # self._database.cur.execute("SELECT rulename, rules from Ruleset;")
        # data = self._database.cur.fetchall()
        # self._rulesetList = []
        # for ruleName, rule in data:
        #     self._rulesetList.append((ruleName, rule))
        return

    def main(self):
        ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"

        pygame.init()
        #self.load_game_history()

        sx, sy = 1300, 750
        screen = pygame.display.set_mode((sx, sy))
        pygame.display.set_caption("Game History")
        titleargs = ptext.draw("Game History", midtop=(sx/2, 10), owidth=1.2, color = "0x884400", gcolor="0x442200", surf=None, cache = False, fontsize=64, fontname="CherryCreamSoda")

        buttonrects = [pygame.Rect((50, 150, 1200, 550))]
        textSizes = [(50, 100)]
        buttonnames = ["Name                               Room code                    Status                          "]

        while self._playing:
            screen.fill((0, 50, 50))
            clickpos = None
            events = pygame.event.get()
            screen.blit(self._arrowImg,(10, 10))

            # if entity_view == True:
            #     entityTuple = EntityCreationView().main()
            #     if entityTuple[0] is not None:
            #         entities.append(entityTuple[0])
            #         Validator().add_entity(Entity(entityTuple[0], entityTuple[1], entityTuple[2], entityTuple[3], entityTuple[4], entityTuple[5]))
            #     entity_view = False
            
            # if attribute_action_view == True:
            #     AttributeActionCreationView(currentEntityName).main()
            #     attribute_action_view = False

            for event in events:
                if event.type == pygame.QUIT:
                    self._playing = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self._playing = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clickpos = event.pos
                    x, y = clickpos
                    #save button
                    if x in range(10,40) and y in range(10,40):
                        return
                    for joinIdx in range(len(self._gameHistoryPositionList)):
                        x1 = int(self._gameHistoryPositionList[joinIdx][0])
                        y1 = int(self._gameHistoryPositionList[joinIdx][1])
                        if x in range(x1, x1 + 200) and y in range(y1, y1+60):
                            l = 1
                            # rule = self._gameHistoryPositionList[joinIdx][1]
                            # deserializedRule = pickle.loads(rule)
                            # Validator().clear_entities()
                            # Validator().set_entities(deserializedRule.get_entities())
                            # RulesetCreationEditView().main(self._rulesetList[editIdx][0])
                            # self.load_ruleset()
                            # currentEntityName = entities[moreIdx]

            for rect, name, size in zip(buttonrects, buttonnames, textSizes):
                screen.fill(pygame.Color("#553300"), rect)
                screen.fill(pygame.Color("#332200"), rect.inflate(-8, -8))
                box = rect.inflate(-8, 100)
                ptext.draw(name, size, color="white", owidth=0.5, fontsize=40, fontname="Boogaloo")
                ptext.drawbox("", box, color = "white", owidth=0.5)
            
            # ruleNamesString = ""
            # self._rulesetPositionList = []
            # for ruleIdx in range(len(self._rulesetList)):
            #     ruleNamesString += self._rulesetList[ruleIdx][0] + "\n\n"
            #     screen.blit(self._editButton,(900, 210 + ruleIdx * 50 + ruleIdx*0.17*100))
            #     self._rulesetPositionList.append((900, 210 + ruleIdx * 50 + ruleIdx*0.17*100))
            # ptext.draw(ruleNamesString, (70, 200), fontname="Boogaloo", color="white", fontsize=30)
            
            screen.blit(*titleargs)
            pygame.display.flip()





