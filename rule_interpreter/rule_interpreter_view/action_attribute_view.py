import pygame
import ptext
import pygame_textinput
import action_creation_view as actionView
import attribute_creation_view as attributeView

def main():
    ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"
    textinput1 = pygame_textinput.TextInput()
    textinput2 = pygame_textinput.TextInput()
    textinput3 = pygame_textinput.TextInput()
    img = pygame.image.load('img/submit.png')
    arrowImg = pygame.image.load('img/arrow.png')
    plusImage = pygame.image.load('img/plussign.png')

    pygame.init()

    sx, sy = 1300, 750
    screen = pygame.display.set_mode((sx, sy))

    buttonrects = [pygame.Rect((50, 50, 300, 650)),  pygame.Rect((400, 50, 800, 300)), pygame.Rect((400, 400, 800, 300))]
    textSizes = [(50, 10), (400, 10), (400, 360),]
    buttonnames = ["Entity Info", "Attributes", "Actions"]
    actionNames = []
    attributes = []
    entites_str = ""
    action_str = ""
    attributeStr = ""
    entity_name_input = ""
    entity_type_input = ""
    size = ""
    entity_view = False
    action_view = False
    attribute_view = False

    playing = True

    while playing:
        screen.fill((0, 50, 50))
        screen.blit(arrowImg,(10, 10))
        screen.blit(plusImage,(1175, 15))
        screen.blit(plusImage,(1175, 364))
        clickpos = None
        events = pygame.event.get()
        
        if action_view == True:
            print("calling action creation main")
            actionName, rule = actionView.main()
            if actionName is not None:
                actionNames.append(actionName)
            action_view = False
        
        if attribute_view == True:
            attrName, attrType, attrValue = attributeView.main()
            if attrName is not None:
                attributes.append(attrName)
            attribute_view = False

        for event in events:
            if event.type == pygame.QUIT:
                playing = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                playing = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clickpos = event.pos
                x, y = clickpos
                if x in range(1175, 1200) and y in range(15, 50):
                    action_view = True
                if x in range(1175, 1200) and y in range(365, 400):
                    attribute_view = True
                if x in range(10,40) and y in range(10,40):
                    playing = False
                    return None, None, None

        for rect, name, size in zip(buttonrects, buttonnames, textSizes):
            screen.fill(pygame.Color("#553300"), rect)
            screen.fill(pygame.Color("#332200"), rect.inflate(-8, -8))
            box = rect.inflate(-8, 100)
            ptext.draw(name, size, fontname="Bubblegum_Sans", color="white", owidth=0.5, fontsize=40)
            ptext.drawbox("", box, fontname="Bubblegum_Sans", color = "white", owidth=0.5)

        action_str = ""
        for action in actionNames:
            action_str += action + "\n"
        ptext.draw(action_str, (70, 420), fontname="Boogaloo", color=(0,0,0), fontsize=30)

        attributeStr = ""
        for attr in attributes:
            attributeStr += attr + "\n"
        ptext.draw(attributeStr, (420, 200), fontname="Boogaloo", color=(0,0,0), fontsize=30)

        pygame.display.flip()





