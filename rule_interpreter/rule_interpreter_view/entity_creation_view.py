import pygame
import ptext
import pygame_textinput


def main():

    ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"
    entityNameInput = pygame_textinput.TextInput()
    entityTypeInput = pygame_textinput.TextInput()
    sizeInput = pygame_textinput.TextInput()
    img = pygame.image.load('img/submit.png')

    pygame.init()

    sx, sy = 800, 600
    screen = pygame.display.set_mode((sx, sy))
    pygame.display.set_caption("Entity Creation")

    buttonrects = [pygame.Rect((50, 150 + 175 * j, 500, 70)) for j in range(3)]
    textSizes = [(50, 100 + 170 * j) for j in range(3)]
    buttonnames = ["Entity Name", "Entity Type", "Size"]
    size = ""

    titleargs = ptext.draw("Entity Creation", midtop=(sx/2, 10), owidth=1.2, color = "0x884400", gcolor="0x442200", surf=None, cache = False, fontsize=64, fontname="CherryCreamSoda")
    didSelectEntityNameInputBox= False 
    didSelectEntityTypeInputBox = False 
    didSelectEntitySizeInputBox = False
    playing = True

    while playing:
        clickpos = None
        events = pygame.event.get()

        screen.fill((0, 50, 50))
        screen.blit(img,(600, 450))

        for event in events:
            if event.type == pygame.QUIT:
                playing = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                playing = False
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clickpos = event.pos
                x, y = clickpos
                for j in range(len(buttonrects)):
                    rect = buttonrects[j]
                    if rect.collidepoint(x,y):
                        if j == 0:
                            didSelectEntityNameInputBox = True
                            didSelectEntityTypeInputBox = False
                            didSelectEntitySizeInputBox = False
                        elif j == 1:
                            didSelectEntityNameInputBox = False
                            didSelectEntityTypeInputBox = True
                            didSelectEntitySizeInputBox = False
                        elif j == 2:
                            didSelectEntityNameInputBox = False
                            didSelectEntityTypeInputBox = False
                            didSelectEntitySizeInputBox = True

                if x in range(600,800) and y in range(450,600):
                    print(entityNameInput.get_text())
                    print(entityTypeInput.get_text())
                    print(sizeInput.get_text())
                    playing = False
                    return entityNameInput.get_text(), entityTypeInput.get_text(), sizeInput.get_text()

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
        elif didSelectEntitySizeInputBox == True:
            sizeInput.update(events)

        screen.blit(entityNameInput.get_surface(), (60, 165 + 185 * 0))
        screen.blit(entityTypeInput.get_surface(), (60, 160 + 185 * 1)) 
        screen.blit(sizeInput.get_surface(), (60, 150 + 185 * 2))

        
        screen.blit(*titleargs)
        pygame.display.flip()
    
    print("out of while loop")




