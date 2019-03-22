import pygame
import ptext
import pygame_textinput


def main():

    ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"
    entityNameInput = pygame_textinput.TextInput()
    entityTypeInput = pygame_textinput.TextInput()
    widthInput = pygame_textinput.TextInput()
    heightInput = pygame_textinput.TextInput()
    isTemplateInput = pygame_textinput.TextInput()
    inheritanceInput = pygame_textinput.TextInput()
    img = pygame.image.load('img/submit.png')
    arrowImg = pygame.image.load('img/arrow.png')

    pygame.init()

    sx, sy = 1300, 750
    screen = pygame.display.set_mode((sx, sy))
    pygame.display.set_caption("Entity Creation")

    buttonrects = [pygame.Rect((50, 150, 500, 70)), pygame.Rect((50, 150 + 160 * 1, 500, 70)), pygame.Rect((50, 150 + 160 * 2, 500, 70)), pygame.Rect((50, 150 + 160 * 3, 500, 70)), pygame.Rect((600, 150, 500, 70)), pygame.Rect((600, 150 + 160 * 1, 500, 70))]
    textSizes = [(50, 100), (50, 100 + 155 * 1), (50, 100 + 155 * 2), (50, 100 + 155 * 3), (600, 100), (600, 100 + 155 * 1)]
    buttonnames = ["Entity Name", "Entity Type", "Width", "Height", "Is Template?", "Is Inherited From?"]
    size = ""

    titleargs = ptext.draw("Entity Creation", midtop=(sx/2, 10), owidth=1.2, color = "0x884400", gcolor="0x442200", surf=None, cache = False, fontsize=64, fontname="CherryCreamSoda")
    didSelectEntityNameInputBox= False 
    didSelectEntityTypeInputBox = False 
    didSelectEntityWidthInputBox = False
    didSelectEntityHeightInputBox= False 
    didSelectEntityIsTemplateInputBox = False 
    didSelectEntityInheritanceInputBox = False
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
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                invalidSubmission = False
                clickpos = event.pos
                x, y = clickpos
                for j in range(len(buttonrects)):
                    rect = buttonrects[j]
                    if rect.collidepoint(x,y):
                        if j == 0:
                            didSelectEntityNameInputBox = True
                            didSelectEntityTypeInputBox = False
                            didSelectEntityWidthInputBox = False
                            didSelectEntityHeightInputBox= False 
                            didSelectEntityIsTemplateInputBox = False 
                            didSelectEntityInheritanceInputBox = False
                        elif j == 1:
                            didSelectEntityNameInputBox = False
                            didSelectEntityTypeInputBox = True
                            didSelectEntityWidthInputBox = False
                            didSelectEntityHeightInputBox= False 
                            didSelectEntityIsTemplateInputBox = False 
                            didSelectEntityInheritanceInputBox = False
                        elif j == 2:
                            didSelectEntityNameInputBox = False
                            didSelectEntityTypeInputBox = False
                            didSelectEntityWidthInputBox = True
                            didSelectEntityHeightInputBox= False 
                            didSelectEntityIsTemplateInputBox = False 
                            didSelectEntityInheritanceInputBox = False
                        if j == 3:
                            didSelectEntityNameInputBox = False
                            didSelectEntityTypeInputBox = False
                            didSelectEntityWidthInputBox = False
                            didSelectEntityHeightInputBox= True 
                            didSelectEntityIsTemplateInputBox = False 
                            didSelectEntityInheritanceInputBox = False
                        elif j == 4:
                            didSelectEntityNameInputBox = False
                            didSelectEntityTypeInputBox = False
                            didSelectEntityWidthInputBox = False
                            didSelectEntityHeightInputBox= False 
                            didSelectEntityIsTemplateInputBox = True 
                            didSelectEntityInheritanceInputBox = False
                        elif j == 5:
                            didSelectEntityNameInputBox = False
                            didSelectEntityTypeInputBox = False
                            didSelectEntityWidthInputBox = False
                            didSelectEntityHeightInputBox= False 
                            didSelectEntityIsTemplateInputBox = False 
                            didSelectEntityInheritanceInputBox = True
                        

                if x in range(10,40) and y in range(10,40):
                    playing = False
                    return None, None, None
                if x in range(1100,1300) and y in range(600,750):
                    if entityNameInput.get_text() == "" or entityTypeInput.get_text() == "" or widthInput.get_text() == "" or heightInput.get_text() == "" or isTemplateInput.get_text() == "":
                        invalidSubmission = True
                    else:
                        playing = False
                        return entityNameInput.get_text(), entityTypeInput.get_text(), widthInput.get_text(), heightInput.get_text(), isTemplateInput.get_text(), inheritanceInput.get_text()

        for rect, name, size in zip(buttonrects, buttonnames, textSizes):
            screen.fill(pygame.Color("#553300"), rect)
            screen.fill(pygame.Color("#332200"), rect.inflate(-8, -8))
            box = rect.inflate(-16, 16)
            ptext.draw(name, size, fontname="Bubblegum_Sans", color="white", owidth=0.5, fontsize=40)
            ptext.drawbox("", box, fontname="Bubblegum_Sans", color = "white", owidth=0.5)

        if didSelectEntityNameInputBox == True:
            entityNameInput.update(events)
        elif didSelectEntityTypeInputBox == True:
            entityTypeInput.update(events)
        elif didSelectEntityWidthInputBox == True:
            widthInput.update(events)
        elif didSelectEntityHeightInputBox == True:
            heightInput.update(events)
        elif didSelectEntityIsTemplateInputBox == True:
            isTemplateInput.update(events)
        elif didSelectEntityInheritanceInputBox == True:
            inheritanceInput.update(events)
        
        if invalidSubmission == True:
            ptext.draw("All fields must be complete in order to submit", (615, 500), fontname="Boogaloo", color="red", fontsize=30)

        screen.blit(entityNameInput.get_surface(), (60, 165 + 185 * 0))
        screen.blit(entityTypeInput.get_surface(), (60, 150 + 185 * 1)) 
        screen.blit(widthInput.get_surface(), (60, 130 + 185 * 2))
        screen.blit(heightInput.get_surface(), (60, 110 + 185 * 3))
        screen.blit(isTemplateInput.get_surface(), (610, 165 + 185 * 0))
        screen.blit(inheritanceInput.get_surface(), ((610, 150 + 185 * 1)))

        screen.blit(*titleargs)
        pygame.display.flip()
