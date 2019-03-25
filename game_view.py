import pygame, sys, random
from pygame.locals import *
from game_engine.map import Map
import os
import math
import re
import ptext
from shutil import copyfile


# sources for examples:
# http://usingpython.com/pygame-tilemaps/
# http://usingpython.com/list-comprehension/

class GameView:

    def __init__(self):
        return

    def offset_blit(self,x,y):
        return (x+MAPOFFSET[0],y+MAPOFFSET[1])

    def which_tile(self,mousepos):
        x = math.ceil(mousepos[1]/myMap.tilesize)-1
        y = math.ceil(mousepos[0]/myMap.tilesize)-1
        if y in range(0,myMap.width) and x in range(0,myMap.height):
            return x,y
        return -1,-1

    def check_entity_fit(self,width, height, x, y, entity):
        if (y + width) > myMap.width or (x + height) > myMap.height:
            return False
        for i in range(0,width):
            for j in range(0,height):
                en = self.which_entity(x+j, y+i)
                if en is not None and en != entity:
                    return False
        return True

    def tile_location(self,size):
        return size[1]*myMap.tilesize, size[0]*myMap.tilesize

    def make_popup(self,x, y, entity):
        global OLDSURF

        # draw drop down
        options = ["Move"] # mandatory option to have
        options += entity.actions
        textSurf = []
        width = 0
        height = 0
        OLDSURF = DISPLAYSURF.copy()
         # newsize = img1.get_width()+4, img1.get_height()+4
        for i in options:
            textSurf.append(FONTTYPE.render(i, 1, (255, 255, 255)))
            local_width, height = FONTTYPE.size(i) 
            if (local_width>width):
                width = local_width
        popupSurf = pygame.Surface((width+4,height*len(options)))
        DISPLAYSURF.blit(popupSurf, self.offset_blit(x,y))    
        for i in range(len(textSurf)):
            DISPLAYSURF.blit(textSurf[i], self.offset_blit(x+2,y+(height*i)))

        # draw rectangle surrounding the actual box
        left, top = self.tile_location((entity.x, entity.y))
        left, top = self.offset_blit(left, top)
        pygame.draw.lines(DISPLAYSURF, (255,0,0), True, [(left, top), (left+entity.width*myMap.tilesize, top), (left+entity.width*myMap.tilesize, top+entity.height*myMap.tilesize), (left, top+entity.height*myMap.tilesize)], 3)

        # entity information to display on the left
        ptext.draw(str(entity), (5, 5), sysfontname="arial", color=COLOR_WHITE, fontsize=30, width = 200)

        return (popupSurf.get_width(), popupSurf.get_height()), (x,y)

    def remove_previous_popup(self):
        DISPLAYSURF.blit(OLDSURF, (0,0))

    def load_pictures(self):
        # Grab all pictures located in the textures directory and temporary folder
        images = {}

        direc = os.getcwd() + "/images/textures/"
        pictures = [i for i in os.listdir(direc)]
        for p in pictures:
            if p.endswith(".png") or p.endswith(".jpg") or p.endswith(".jpeg"):
                images[p] = pygame.image.load("images/textures/"+p)

        if os.path.exists("/tmp"):
            direc = os.getcwd() + "/tmp/"
            pictures = [i for i in os.listdir(direc)]
            for p in pictures:
                if p.endswith(".png") or p.endswith(".jpg") or p.endswith(".jpeg"):
                    images[p] = pygame.image.load("tmp/"+p)

        return images

    def which_entity(self,x, y):
        for e in ENTITIES:
            if x in range(e.x,e.x+e.width) and y in range(e.y,e.y+e.height):
                return e
        return None

    # GM FUNCTIONS ------------------------------------------------------------------------------------------------

    def toggle_fog(self):
        self.clear_GM_info()
        self.display_message("_Toggle Fog Mode_\n\nPress ESC to exit this mode.")

        RUNNING = True
        while RUNNING:    
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mousepos = pygame.mouse.get_pos()
                    mousepos = (mousepos[0]-MAPOFFSET[0],mousepos[1]-MAPOFFSET[1])
                    x, y = gameview.which_tile(mousepos)
                    # draw rectangle surrounding the actual box
                    left, top = self.tile_location((x, y))
                    left, top = self.offset_blit(left, top)
                    if myMap.fogOfWar[x][y]:
                        myMap.fogOfWar[x][y] = False
                        pygame.draw.lines(DISPLAYSURF, (0,0,255), True, [(left, top), (left+myMap.tilesize, top), (left+myMap.tilesize, top+myMap.tilesize), (left, top+myMap.tilesize)], 3)
                    else: 
                        myMap.fogOfWar[x][y] = True
                        pygame.draw.lines(DISPLAYSURF, (255,255,255), True, [(left, top), (left+myMap.tilesize, top), (left+myMap.tilesize, top+myMap.tilesize), (left, top+myMap.tilesize)], 3)
                    # test if fog of war works in the right location
                    # self.update_fog()
                elif event.type == KEYDOWN:   
                    if event.key == K_ESCAPE:
                        self.clear_GM_info()
                        self.help_screen()
                        return
        return

    def add_texture(self):
        string = "_Add Texture Mode_\nPress ESC to exit this mode.\n\nSelect a texture:\n"
        images = self.load_pictures()
        for key in images:
            string += key + ", "
        
        self.clear_GM_info()
        self.display_message(string)

        input_box = InputBox(MAPOFFSET[0] + 200, myMap.tilesize*myMap.height, 500, 32, DISPLAYSURF)

        RUNNING = True
        text = ""
        selected_image = None
        blit_input = True
        while RUNNING:    
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mousepos = pygame.mouse.get_pos()
                    mousepos = (mousepos[0]-MAPOFFSET[0],mousepos[1]-MAPOFFSET[1])
                    if selected_image is not None:
                        x, y = gameview.which_tile(mousepos)
                        texture = Map.Texture(x,y,1,1,selected_image)
                        myMap.textures.append(texture)
                        texture_image = pygame.transform.scale(selected_image, (texture.width*myMap.tilesize,texture.height*myMap.tilesize))
                        DISPLAYSURF.blit(texture_image, gameview.offset_blit(texture.y*myMap.tilesize, texture.x*myMap.tilesize))
                        self.clear_GM_info()
                        self.display_message(string)
                        blit_input = True
                        selected_image = None
                elif event.type == KEYDOWN:   
                    if event.key == K_ESCAPE:
                        self.clear_GM_info()
                        self.help_screen()
                        return
                    elif event.key == K_RETURN:
                        text = input_box.handle_event(event)
                        text = text.rstrip()
                        if text in images:
                            self.clear_GM_info()
                            blit_input = False
                            self.display_message("Please select tile you would like to place this texture")
                            selected_image = images[text]
                text = input_box.handle_event(event)
            if blit_input:
                input_box.wipe()
                input_box.draw()
            pygame.display.flip()            

        return

    def create_new_entity(self):
        self.clear_GM_info()
        self.display_message("Create New Entity _ACTIVE_")
        return

    def edit_entity(self):
        self.clear_GM_info()
        self.display_message("Edit Entity _ACTIVE_")
        return

    def delete_entity(self):
        self.clear_GM_info()
        self.display_message("Delete Entity _ACTIVE_")
        return

    def add_asset(self):
        self.clear_GM_info()
        general_message = "_Add Asset Mode_\nEnter in the path to an image.\nPress ESC to exit this mode."
        self.display_message(general_message)
        if not os.path.exists("/tmp"):
            os.makedirs('/tmp')

        input_box = InputBox(MAPOFFSET[0] + 300, myMap.tilesize*myMap.height, 500, 32, DISPLAYSURF)

        RUNNING = True
        text = ""
        while RUNNING:    
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    pass
                elif event.type == KEYDOWN:   
                    if event.key == K_ESCAPE:
                        self.clear_GM_info()
                        self.help_screen()
                        return
                    elif event.key == K_RETURN:
                        text = input_box.handle_event(event)
                        text = text.rstrip()
                        if os.path.isfile(text):
                            if text.split(".")[1] not in ["png", "jpg", "jpeg"]:
                                self.clear_GM_info()
                                self.display_message("_FILE IS NOT AN IMAGE_\n"+general_message)
                            else:
                                new_name = os.getcwd() + "/tmp/" + text.split("/")[-1]
                                copyfile(text, new_name)
                                self.clear_GM_info()
                                self.display_message("_FILE ADDED_\n"+general_message)
                        else: 
                            self.clear_GM_info()
                            self.display_message("_FILE DOES NOT EXIST_\n"+general_message)
                text = input_box.handle_event(event)
            input_box.wipe()
            input_box.draw()
            pygame.display.flip()  

        return
    
    def remove_player(self):
        self.clear_GM_info()
        self.display_message("Remove Player")
        return

    def roll_die(self):
        self.clear_GM_info()
        surf, tpos = self.display_message("Roll:")

        buf = MAPOFFSET[0] + surf.get_width() + 10
        number_of = InputBox(buf, myMap.tilesize*myMap.height, 50, 32, DISPLAYSURF)
        surf, tpos = ptext.draw("d", (buf + 60, myMap.tilesize*myMap.height + 10), sysfontname="arial", color=COLOR_WHITE, fontsize=30)
        buf = tpos[0] + surf.get_width() + 10
        d_roll = InputBox(buf, myMap.tilesize*myMap.height, 50, 32, DISPLAYSURF)

        myrect = pygame.Rect(MAPOFFSET[0], myMap.tilesize*myMap.height + surf.get_height() + 10, myMap.width*myMap.tilesize, DISPLAYSURF.get_height()-(myMap.tilesize*myMap.height))

        RUNNING = True
        while RUNNING:    
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    pass
                elif event.type == KEYDOWN:   
                    if event.key == K_ESCAPE:
                        self.clear_GM_info()
                        self.help_screen()
                        return
                    elif event.key == K_RETURN:
                        if len(number_of.text)>0 and len(d_roll.text)>0:
                            pygame.draw.rect(DISPLAYSURF, COLOR_BLACK, myrect, 0)
                            result = int(number_of.text.rstrip())*int(d_roll.text.rstrip()) # NEED TO CHANGE MATH HERE -- ANDREW
                            surf, tpos = ptext.draw(number_of.text + " d" + d_roll.text +" = "+ str(result), (MAPOFFSET[0] + 10, myMap.tilesize*myMap.height + surf.get_height() + 10), sysfontname="arial", color=COLOR_WHITE, fontsize=30)
                            number_of.text = ""
                            d_roll.text = ""
                number_of.handle_event(event)
                d_roll.handle_event(event)
            number_of.wipe()
            number_of.draw()
            d_roll.wipe()
            d_roll.draw()
            pygame.display.flip()
        return

    def clear_GM_info(self):
        # clear screen 
        myrect = pygame.Rect(MAPOFFSET[0], myMap.tilesize*myMap.height, myMap.width*myMap.tilesize, DISPLAYSURF.get_height()-(myMap.tilesize*myMap.height))
        pygame.draw.rect(DISPLAYSURF, COLOR_BLACK, myrect, 0)
        return

    def help_screen(self):
        self.clear_GM_info()
        # blit hotkey information
        info = "_GM HOTKEYS:_\n"
        for key, pair in GM_HOTKEYS.items():
            info += key + ": " + pair["name"] + "\n"
        self.display_message(info)
        return

    def display_message(self, message):
        txt_surface, tpos = ptext.draw(message, (MAPOFFSET[0] + 10, myMap.tilesize*myMap.height + 10), sysfontname="arial", color=COLOR_WHITE, fontsize=30, width = myMap.width*myMap.tilesize, underlinetag="_")
        return txt_surface, tpos

    def update_fog(self):
        fogImage = pygame.transform.scale(images["fog.png"], (myMap.tilesize,myMap.tilesize))
        for rw in range(myMap.height):
            for cl in range(myMap.width):
                if not myMap.fogOfWar[rw][cl]:
                    DISPLAYSURF.blit(fogImage, gameview.offset_blit(cl*myMap.tilesize, rw*myMap.tilesize))
        return

# CLASSES ------------------------------------------------------------------------------------------------
# utilized for testing of actions drop down menu
class Entity:
    def __init__(self, x, y, width, height, name, actions):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.name = name
        self.actions = actions
        self.attributes = ["example attributes", "example 2", "example 3"]

    def __str__(self):
        return  "Entity:\nName: "+self.name+"\nwidth: "+str(self.width)+"\nheight: "+str(self.height)+"\nx: "+ str(self.x)+ "\ny: " + str(self.y) +"\nactions: "+str(self.actions)+"\nattributes: "+str(self.attributes)

class InputBox:
    # https://stackoverflow.com/questions/46390231/how-to-create-a-text-input-box-with-pygame

    def __init__(self, x, y, w, h, screen, text=''):
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = ptext.getsurf(self.text, sysfontname="arial", color=COLOR_WHITE, fontsize=30, width = w)
        self.height = self.txt_surface.get_height() + 5
        self.rect = pygame.Rect(x, y, w, self.height)
        self.active = False
        self.screen = screen

    def handle_event(self, event, transcript=""):
        if event.type == MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == KEYDOWN:
            if self.active:
                if event.key == K_RETURN:
                    # append to the transcript view
                    if len(self.text) > 0:
                        transcript += str(self.text) + "\n"
                        self.text = ""
                        self.remove_old_block()
                elif event.key == K_BACKSPACE:
                    self.text = self.text[:-1]
                    tmp_surface = ptext.getsurf(self.text, sysfontname="arial", color=COLOR_WHITE, fontsize=30, width = self.rect.w)
                    if tmp_surface.get_height() < (self.rect.h-5):
                        self.remove_old_block()
                else:
                    self.text += event.unicode

        return transcript

    def remove_old_block(self):
        self.rect.h += 5
        pygame.draw.rect(self.screen, COLOR_BLACK, self.rect, 0)
        self.rect.h = self.height

    def draw(self):
        # Blit the text.
        self.txt_surface, tpos = ptext.draw(self.text, (self.rect.x+5, self.rect.y+5), sysfontname="arial", color=COLOR_WHITE, fontsize=30, width = self.rect.w)
        self.rect.h = self.txt_surface.get_height() + 5
        # Blit the rect.
        pygame.draw.rect(self.screen, self.color, self.rect, 2)

    def wipe(self):
        # Blit the rect box.
        pygame.draw.rect(self.screen, COLOR_BLACK, self.rect, 0)
        pygame.draw.rect(self.screen, self.color, self.rect, 2)

class Transcript:
    def __init__(self, x, y, w, h, screen, transcript=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.transcript = transcript
        self.transcript_in_view = transcript
        self.screen = screen
        self.color = COLOR_INACTIVE
        self.txt_surface = None
        self.active = False

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == KEYDOWN:
            if self.active:
                if event.key == K_DOWN:
                    self.scroll_down()
                elif event.key == K_UP:
                    self.scroll_up()

    def update(self, transcript):
        if self.transcript != transcript:
            self.transcript = transcript
            self.next_line()
            self.adjust_transcript_view()
            
    def draw(self):
        # Blit the text.
        self.txt_surface, tpos = ptext.draw(self.transcript_in_view, (self.rect.x+5, self.rect.y+5), sysfontname="arial", color=COLOR_WHITE, fontsize=30, width = self.rect.w)
        # Blit the rect.
        pygame.draw.rect(self.screen, self.color, self.rect, 2)

    def wipe(self):
        # Blit the rect.
        pygame.draw.rect(self.screen, COLOR_BLACK, self.rect, 0)

    def scroll_up(self):
        if len(self.transcript_in_view) < len(self.transcript):
            try:
                # add to top of string last part of whole transcript before it
                beforehand = self.transcript.split(self.transcript_in_view,1)[0]
                first_line = beforehand.split("\n")[-2]
                self.transcript_in_view = first_line + "\n" + self.transcript_in_view 
                # pop off the bottom of transcript in view
                lines = self.transcript_in_view.split("\n")
                copyof = lines[0:len(lines)-2]
                self.transcript_in_view = "\n".join(copyof) + "\n"
                # display this
                self.adjust_transcript_view()
            except Exception as e:
                # print(e)
                if e != "list index out of range":
                    print(e)

    def scroll_down(self):
        if len(self.transcript_in_view) < len(self.transcript):
            # add the next line in the transcript
            afterwards = self.transcript.split(self.transcript_in_view,1)[-1]
            if len(afterwards) >= 1:
                first_line = afterwards.split("\n")[0]
                self.transcript_in_view = self.transcript_in_view + first_line + "\n"
                # pop off the top
                self.transcript_in_view = self.transcript_in_view.split("\n",1)[-1]
                # display this 
                self.adjust_transcript_view()

    def next_line(self):
        self.transcript_in_view += transcript.split("\n")[-2] + "\n"

    def adjust_transcript_view(self):
        tmp_surface = ptext.getsurf(self.transcript_in_view, sysfontname="arial", color=COLOR_WHITE, fontsize=30, width = self.rect.w)
        if len(self.transcript_in_view) < len(self.transcript):
        # if not down:
            while (tmp_surface.get_height() < self.rect.h):
                # add to top of string last part of whole transcript before it
                beforehand = self.transcript.split(self.transcript_in_view,1)[0]
                first_line = beforehand.split("\n")[-2]
                self.transcript_in_view = first_line + "\n" + self.transcript_in_view 
                tmp_surface = ptext.getsurf(self.transcript_in_view, sysfontname="arial", color=COLOR_WHITE, fontsize=30, width = self.rect.w)
        while (tmp_surface.get_height() > self.rect.h):
            self.transcript_in_view = self.transcript_in_view.split("\n",1)[-1]
            tmp_surface = ptext.getsurf(self.transcript_in_view, sysfontname="arial", color=COLOR_WHITE, fontsize=30, width = self.rect.w)

# ------------------------------------------------------------------------------------------------------------
# GLOBAL VAR
myMap = Map(tilesize = 50, height = 10, width = 18)
MAPOFFSET = (200,0)
OLDSURF = None
gameview = GameView()

pygame.init()
# FONTTYPE = pygame.font.SysFont('arial', 25)
FONTTYPE = pygame.font.Font(None, 32)
DISPLAYSURF = pygame.display.set_mode((1300,750))
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
ENTITIES = [Entity(5,5,2,2,"water.png",["Attack","Defend"]),Entity(2,2,1,1,"rock.png",["Sit"]),Entity(2,3,1,1,"rock.png",["Defend"])]
GM_STATUS = False
GM_HOTKEYS = {"f": {"name": "Toggle FOG", "function": gameview.toggle_fog},
              "t": {"name": "Add Texture", "function": gameview.add_texture},
              "e": {"name": "Edit Entity", "function": gameview.edit_entity},
              "c": {"name": "Create New Entity", "function": gameview.create_new_entity},
              "a": {"name": "Add Asset", "function": gameview.add_asset},
              "d": {"name": "Delete Entity", "function": gameview.delete_entity},
              "p": {"name": "Remove Player", "function": gameview.remove_player},
              "r": {"name": "Roll Die", "function": gameview.roll_die},
              "h": {"name": "Show this help screen", "function": gameview.help_screen}
              }

# -----------------------------------------------------------------------------------------------------------------------

def main():

    images = gameview.load_pictures()

    # create the map and add add textures to it
    myMap.textures = [Map.Texture(3,3,1,1,"grass.png"),Map.Texture(3,4,1,1,"grass.png")]
    
    #example fog
    myMap.fogOfWar[8][15] = False
    myMap.fogOfWar[8][16] = False
    myMap.fogOfWar[9][15] = False
    myMap.fogOfWar[9][16] = False

    # create the entire background
    greyImage = pygame.transform.scale(images["grey.png"], (myMap.tilesize,myMap.tilesize))
    fogImage = pygame.transform.scale(images["fog.png"], (myMap.tilesize,myMap.tilesize))
    for rw in range(myMap.height):
        for cl in range(myMap.width):
            if myMap.fogOfWar[rw][cl]:
                DISPLAYSURF.blit(greyImage, gameview.offset_blit(cl*myMap.tilesize, rw*myMap.tilesize))
            else: 
                DISPLAYSURF.blit(fogImage, gameview.offset_blit(cl*myMap.tilesize, rw*myMap.tilesize))

    # put all the textures on the map
    for texture in myMap.textures:
        texture_image = pygame.transform.scale(images[texture.name], (texture.width*myMap.tilesize,texture.height*myMap.tilesize))
        DISPLAYSURF.blit(texture_image, gameview.offset_blit(texture.y*myMap.tilesize, texture.x*myMap.tilesize))

    # put all the entities on the map
    for entity in ENTITIES:
        entity_image = pygame.transform.scale(images[entity.name], (entity.width*myMap.tilesize,entity.height*myMap.tilesize))
        DISPLAYSURF.blit(entity_image, gameview.offset_blit(entity.y*myMap.tilesize, entity.x*myMap.tilesize))

    gameview.help_screen()

    my_entity = None
    input_box = InputBox(MAPOFFSET[0]+myMap.width*myMap.tilesize, DISPLAYSURF.get_height()-200, 200, 32, DISPLAYSURF)
    history = Transcript(MAPOFFSET[0]+myMap.width*myMap.tilesize, MAPOFFSET[1], 200, DISPLAYSURF.get_height()-(DISPLAYSURF.get_height()-input_box.rect.y), DISPLAYSURF)
    # transcript = ""
    action_requested = ""

    RUNNING = True
    while RUNNING:    
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                mousepos = (mousepos[0]-MAPOFFSET[0],mousepos[1]-MAPOFFSET[1])
                print(mousepos)
                if my_entity is not None and action_requested is not "Move":
                    gameview.remove_previous_popup()
                    if mousepos[0] in range(location[0],location[0]+size[0]) and mousepos[1] in range(location[1],location[1]+size[1]):
                        rowsize = size[1]/(len(my_entity.actions)+1)
                        option_selected = math.floor((mousepos[1]-location[1])/rowsize)
                        if option_selected == 0:
                            action_requested = "Move"
                        else:
                            action_requested = my_entity.actions[option_selected-1]
                            my_entity = None
                        print(action_requested)
                    else:
                        my_entity = None
                elif my_entity is not None and action_requested is "Move":
                    # grab new location
                    x, y = gameview.which_tile(mousepos)
                    # if it is a valid locatin and there are no other entities there
                    if x != -1 and y != -1 and gameview.check_entity_fit(my_entity.width, my_entity.height, x, y, my_entity):
                        # remove old image and replace with generic block, then cover with texture if there are any       
                        for i in range(0,my_entity.width):
                            for j in range(0,my_entity.height):
                                DISPLAYSURF.blit(greyImage, gameview.offset_blit((my_entity.y+i)*myMap.tilesize, (my_entity.x+j)*myMap.tilesize))
                                for texture in myMap.textures:
                                    if texture.x == (my_entity.x+j) and texture.y == (my_entity.y+i):
                                        texture_image = pygame.transform.scale(images[texture.name], (texture.width*myMap.tilesize,texture.height*myMap.tilesize))
                                        DISPLAYSURF.blit(texture_image, gameview.offset_blit(texture.y*myMap.tilesize, texture.x*myMap.tilesize))  
                                        break # to speed up the loop checking
                        # blit entity to it
                        my_entity.x = x
                        my_entity.y = y
                        my_entity_image = pygame.transform.scale(images[my_entity.name], (my_entity.width*myMap.tilesize,my_entity.height*myMap.tilesize))
                        DISPLAYSURF.blit(my_entity_image, gameview.offset_blit(my_entity.y*myMap.tilesize, my_entity.x*myMap.tilesize))
                    # wipe signals
                    action_requested = ""
                    my_entity = None
                else:
                    x, y = gameview.which_tile(mousepos)
                    my_entity = gameview.which_entity(x, y)
                    if my_entity is not None:
                        if (my_entity.y + my_entity.width) >= myMap.width or (my_entity.x + my_entity.height) >= myMap.height:
                            loc_x, loc_y = gameview.tile_location((my_entity.x,my_entity.y))
                        else:    
                            loc_x, loc_y = gameview.tile_location((my_entity.width+my_entity.x,my_entity.height+my_entity.y))
                        size, location = gameview.make_popup(loc_x, loc_y, my_entity)
            elif event.type == KEYDOWN:   
                if event.key == K_ESCAPE:
                    RUNNING = False
                elif event.unicode in GM_HOTKEYS:
                    print(GM_HOTKEYS[event.unicode]["name"])
                    # execute functionality
                    GM_HOTKEYS[event.unicode]["function"]()
            # input box handling + transcript update
            transcript = input_box.handle_event(event, history.transcript)
            history.handle_event(event)
            history.update(transcript)
            # transcript = input_box.handle_event(event, transcript)

        # chat commands
        input_box.wipe()
        history.wipe()
        input_box.draw()
        history.draw()

        pygame.display.flip()


if __name__ == "__main__":
    main()