import pygame
import ptext
import pygame_textinput


def main():
    ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"
    attributeNameInput = pygame_textinput.TextInput()
    attributeTypeInput = pygame_textinput.TextInput()
    attributeValueInput = pygame_textinput.TextInput()
    img = pygame.image.load('img/submit.png')
    arrowImg = pygame.image.load('img/arrow.png')

    pygame.init()

    sx, sy = 1300, 750
    screen = pygame.display.set_mode((sx, sy))
    pygame.display.set_caption("Attribute Creation")

    buttonrects = [pygame.Rect((50, 150 + 160 * j, 1100, 70)) for j in range(3)]
    textSizes = [(50, 100 + 155 * j) for j in range(3)]
    buttonnames = ["Attribute Name", "Attribute Type", "Attribute Value"]

    titleargs = ptext.draw("Attribute Creation", midtop=(sx/2, 10), owidth=1.2, color = "0x884400", gcolor="0x442200", surf=None, cache = False, fontsize=64, fontname="CherryCreamSoda")
    didSelectAttrNameInputBox= False 
    didSelectAttrTypeInputBox = False 
    didSelectAttrValueInputBox = False
    playing = True
    invalidSubmission = False

    while playing:
        clickpos = None
        events = pygame.event.get()

        screen.fill((0, 50, 50))
        screen.blit(img,(1100, 600))
        screen.blit(arrowImg,(10, 10))

        for event in events:
            if event.type == pygame.QUIT:
                playing = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                playing = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                invalidSubmission = False
                clickpos = event.pos
                x, y = clickpos
                for j in range(len(buttonrects)):
                    rect = buttonrects[j]
                    if rect.collidepoint(x,y):
                        if j == 0:
                            didSelectAttrNameInputBox = True
                            didSelectAttrTypeInputBox = False
                            didSelectAttrValueInputBox = False
                        elif j == 1:
                            didSelectAttrNameInputBox = False
                            didSelectAttrTypeInputBox = True
                            didSelectAttrValueInputBox = False
                        elif j == 2:
                            didSelectAttrNameInputBox = False
                            didSelectAttrTypeInputBox = False
                            didSelectAttrValueInputBox = True

                if x in range(10,40) and y in range(10,40):
                    playing = False
                    return None, None, None

                if x in range(1100,1300) and y in range(600,750):
                    if attributeNameInput.get_text() == "" or attributeTypeInput.get_text() == "" or attributeValueInput.get_text() == "":
                        invalidSubmission = True
                    else:
                        playing = False
                        return attributeNameInput.get_text(), attributeTypeInput.get_text(), attributeValueInput.get_text()

        for rect, name, size in zip(buttonrects, buttonnames, textSizes):
            screen.fill(pygame.Color("#553300"), rect)
            screen.fill(pygame.Color("#332200"), rect.inflate(-8, -8))
            box = rect.inflate(-16, 16)
            ptext.draw(name, size, fontname="Bubblegum_Sans", color="white", owidth=0.5, fontsize=40)
            ptext.drawbox("", box, fontname="Bubblegum_Sans", color = "white", owidth=0.5)

        if didSelectAttrNameInputBox == True:
            attributeNameInput.update(events)
        elif didSelectAttrTypeInputBox == True:
            attributeTypeInput.update(events)
        elif didSelectAttrValueInputBox == True:
            attributeValueInput.update(events)

        if invalidSubmission == True:
            ptext.draw("All fields must be complete in order to submit", (60, 555), fontname="Boogaloo", color="red", fontsize=30)

        screen.blit(attributeNameInput.get_surface(), (60, 165 + 185 * 0))
        screen.blit(attributeTypeInput.get_surface(), (60, 150 + 185 * 1)) 
        screen.blit(attributeValueInput.get_surface(), (60, 130 + 185 * 2))

        
        screen.blit(*titleargs)
        pygame.display.flip()


