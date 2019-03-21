import pygame
import ptext
import pygame_textinput

ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"
textinput1 = pygame_textinput.TextInput()
textinput2 = pygame_textinput.TextInput()
textinput3 = pygame_textinput.TextInput()
img = pygame.image.load('img/submit.png')

pygame.init()

sx, sy = 1200, 700
screen = pygame.display.set_mode((sx, sy))
pygame.display.set_caption("Entity Creation")

buttonrects = [pygame.Rect((50, 200 + 175 * j, 800, 70)) for j in range(3)]
textSizes = [(50, 150 + 170 * j) for j in range(3)]
buttonnames = ["Entity Name", "Entity Type", "Size"]
buttoncosts = [10, 400, 12000, 250000]
entity_name_input = ""
entity_type_input = ""
size = ""

titleargs = ptext.draw("Entity Creation", midtop=(sx/2, 10), owidth=1.2, color = "0x884400", gcolor="0x442200", surf=None, cache = False, fontsize=64, fontname="CherryCreamSoda")
t1= False 
t2 = False 
t3 = False
playing = True

while playing:
    clickpos = None
    events = pygame.event.get()

    screen.fill((0, 50, 50))
    screen.blit(img,(1000, 550))

    for event in events:
        if event.type == pygame.QUIT:
            playing = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            playing = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clickpos = event.pos
            x, y = clickpos
            for j in range(len(buttonrects)):
                rect = buttonrects[j]
                if rect.collidepoint(x,y):
                    if j == 0:
                        t1 = True
                        t2 = False
                        t3 = False
                    elif j == 1:
                        t1 = False
                        t2 = True
                        t3 = False
                    elif j == 2:
                        t1 = False
                        t2 = False
                        t3 = True

            if x in range(1000,1200) and y in range(550,700):
                print(textinput1.get_text())
                print(textinput2.get_text())
                print(textinput3.get_text())

    for rect, name, size in zip(buttonrects, buttonnames, textSizes):
        screen.fill(pygame.Color("#553300"), rect)
        screen.fill(pygame.Color("#332200"), rect.inflate(-8, -8))
        box = rect.inflate(-16, 16)
        ptext.draw(name, size, fontname="Bubblegum_Sans", color="white", owidth=0.5, fontsize=40)
        ptext.drawbox("", box, fontname="Bubblegum_Sans", color = "white", owidth=0.5)

    if t1 == True:
        textinput1.update(events)
    elif t2 == True:
        textinput2.update(events)
    elif t3 == True:
        textinput3.update(events)

    screen.blit(textinput1.get_surface(), (60, 200 + 185 * 0))
    screen.blit(textinput2.get_surface(), (60, 200 + 185 * 1)) 
    screen.blit(textinput3.get_surface(), (60, 200 + 185 * 2))

    
    screen.blit(*titleargs)
    pygame.display.flip()




