import pygame
import ptext
import pygame.locals as pl
img = pygame.image.load('submit.png')
pygame.transform.scale(img, (100, 100))

screen = pygame.display.set_mode((1200, 700))
screen.fill((255, 255, 255))
screen.blit(img,(400,500))

user_input = "" 

pygame.display.flip()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)
                if mouse_pos[0] in range(400,1200) and mouse_pos[1] in range(500,700):
                    print(user_input)

        if event.type == pygame.KEYDOWN:

            if event.key == pl.K_RETURN:
                user_input += "\n"
            
            elif event.key == pl.K_DELETE:
                screen.fill((255, 255, 255))
                print(user_input)
                screen.blit(img,(400,500))
                user_input = user_input[:len(user_input)-1]
            
            elif event.key == pl.K_BACKSPACE:
                screen.fill((255, 255, 255))
                print(user_input)
                screen.blit(img,(400,500))
                user_input = user_input[:len(user_input)-1]

            else:
                # If no special key is pressed, add unicode of key to input_string
                user_input += event.unicode
        
        ptext.draw(user_input, (0, 0), color=(0,0,0))

    pygame.display.update()
