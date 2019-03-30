import os
import sys
import pygame
import pickle
# sys.path.append('../../account')
# from database import Database
import ptext
import pyautogui

class GameHistoryView:
    def __init__(self, username, client):
        self._joinButtonImage = pygame.image.load('img/joinButton.png')
        self._joinButtonList = []
        self._playing = True
        #contains a tuples with room code and status
        self._gameHistoryList = []
        self._gameHistoryPositionList =[]
        self._arrowImg = pygame.image.load('img/arrow.png')
        self._client = client
        self._username = username

    def main(self):
        ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"

        pygame.init()
        self._gameHistoryList = self._client.load_game_history(self._username)

        sx, sy = 1300, 750
        screen = pygame.display.set_mode((sx, sy))
        pygame.display.set_caption("Game History")
        titleargs = ptext.draw("Game History", midtop=(sx/2, 10), owidth=1.2, color = "0x884400", gcolor="0x442200", surf=None, cache = False, fontsize=64, fontname="CherryCreamSoda")

        buttonrects = [pygame.Rect((50, 150, 1200, 550))]
        textSizes = [(50, 100)]
        buttonnames = ["Game Name                           Room code       Status     Timestamp"]

        while self._playing:
            screen.fill((0, 50, 50))
            clickpos = None
            events = pygame.event.get()
            screen.blit(self._arrowImg,(10, 10))

            for event in events:
                if event.type == pygame.QUIT:
                    self._playing = False
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pyautogui.alert(text='', title='', button='OK')
                    #self._playing = False
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
                            return
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
            
            gameHistoryRoomCodeStr = ""
            gameHistoryStatusStr = ""
            gameHistoryNameStr = ""
            gameHistoryTimestampStr = ""
            for gameIdx in range(len(self._gameHistoryList)):
                gameHistoryRoomCodeStr += str(self._gameHistoryList[gameIdx][0]) + "\n\n"
                gameHistoryStatusStr += str(self._gameHistoryList[gameIdx][1]) + "\n\n"
                gameHistoryNameStr += str(self._gameHistoryList[gameIdx][2]) + "\n\n"
                gameHistoryTimestampStr += str(self._gameHistoryList[gameIdx][3].split(' ')[0]) + "\n\n"
                screen.blit(self._joinButtonImage,(1050, 200 + gameIdx * 50 + gameIdx*0.17*100))
                self._gameHistoryPositionList.append((1050, 200 + gameIdx * 50 + gameIdx*0.17*100))
            ptext.draw(gameHistoryNameStr, (70, 200), fontname="Boogaloo", color="white", fontsize=30)
            ptext.draw(gameHistoryRoomCodeStr, (500, 200), fontname="Boogaloo", color="white", fontsize=30)
            ptext.draw(gameHistoryStatusStr, (700, 200), fontname="Boogaloo", color="white", fontsize=30)
            ptext.draw(gameHistoryTimestampStr, (850, 200), fontname="Boogaloo", color="white", fontsize=30)
            
            screen.blit(*titleargs)
            pygame.display.flip()





