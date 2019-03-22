import pygame
import ptext
import pygame_textinput
import entity_creation_view as eview
import action_attribute_view as aview


ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"
textinput1 = pygame_textinput.TextInput()
textinput2 = pygame_textinput.TextInput()
textinput3 = pygame_textinput.TextInput()
img = pygame.image.load('img/submit.png')
plusImage = pygame.image.load('img/plussign.png')
moreButtonList = []

pygame.init()

sx, sy = 1300, 750
screen = pygame.display.set_mode((sx, sy))
pygame.display.set_caption("Main")
moreImage = pygame.image.load('img/moreButton.png')

buttonrects = [pygame.Rect((50, 150, 1100, 550))]
textSizes = [(50, 100)]
buttonnames = ["Entities"]
entities = []
actionNames = []
attributes = []
entites_str = ""
action_str = ""
attributeStr = ""
entity_name_input = ""
entity_type_input = ""
size = ""
entity_view = False
attribute_action_view = False

titleargs = ptext.draw("Main", midtop=(sx/2, 10), owidth=1.2, color = "0x884400", gcolor="0x442200", surf=None, cache = False, fontsize=64, fontname="CherryCreamSoda")
playing = True

while playing:
    screen.fill((0, 50, 50))
    screen.blit(plusImage,(1110, 110))
    clickpos = None
    events = pygame.event.get()

    if entity_view == True:
        print("calling entity creation main")
        name = eview.main()
        if name is not None:
            entities.append(name[0])
        entity_view = False
    
    if attribute_action_view == True:
        print("calling action creation main")
        aview.main()
        attribute_action_view = False

    for event in events:
        if event.type == pygame.QUIT:
            playing = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            playing = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clickpos = event.pos
            x, y = clickpos
            if x in range(1110, 1140) and y in range(110, 140):
                entity_view = True
            if x in range(610, 640) and y in range(365, 395):
                action_view = True
            if x in range(670, 700) and y in range(115, 145):
                attribute_view = True
            if x in range(600,800) and y in range(450,600):
                print(textinput1.get_text())
                print(textinput2.get_text())
                print(textinput3.get_text())
                entity_view = True
            
            for moreIdx in range(len(moreButtonList)):
                print(moreButtonList)
                x1 = int(moreButtonList[moreIdx][0])
                y1 = int(moreButtonList[moreIdx][1])
                if x in range(x1, x1 + 60) and y in range(y1, y1+30):
                    attribute_action_view = True

    for rect, name, size in zip(buttonrects, buttonnames, textSizes):
        screen.fill(pygame.Color("#553300"), rect)
        screen.fill(pygame.Color("#332200"), rect.inflate(-8, -8))
        box = rect.inflate(-8, 100)
        ptext.draw(name, size, fontname="Bubblegum_Sans", color="white", owidth=0.5, fontsize=40)
        ptext.drawbox("", box, fontname="Bubblegum_Sans", color = "white", owidth=0.5)
    
    entites_str = ""
    moreButtonList = []
    for entityIdx in range(len(entities)):
        entites_str += entities[entityIdx] + "\n"
        screen.blit(moreImage,(1050, 210 + entityIdx * 30 + entityIdx*0.05*100))
        moreButtonList.append((1050, 210 + entityIdx * 30 + entityIdx*0.05*100))
    ptext.draw(entites_str, (70, 200), fontname="Boogaloo", color="white", fontsize=30)

    action_str = ""
    for action in actionNames:
        action_str += action + "\n"
    ptext.draw(action_str, (70, 420), fontname="Boogaloo", color=(0,0,0), fontsize=30)

    attributeStr = ""
    for attr in attributes:
        attributeStr += attr + "\n"
    ptext.draw(attributeStr, (420, 200), fontname="Boogaloo", color=(0,0,0), fontsize=30)

    screen.blit(*titleargs)
    pygame.display.flip()





