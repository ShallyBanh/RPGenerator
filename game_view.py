import pygame, sys, random
from pygame.locals import *
from game_engine.map import Map
import os
import math
import re
import ptext
from shutil import copyfile
sys.path.append('rule_interpreter/')
sys.path.append('rule_interpreter/models')
from game_engine.game import Game
from game_engine.rule_enactor import RuleEnactor
from rule_interpreter.models.validator import _Validator
from rule_interpreter.models.attribute import Attribute
from rule_interpreter.models.entity import Entity

# sources for examples:
# http://usingpython.com/pygame-tilemaps/
# http://usingpython.com/list-comprehension/

class GameView:

    def __init__(self):
        return

    def offset_blit(self,x,y):
        return (x+MAPOFFSET[0],y+MAPOFFSET[1])

    def which_tile(self,mousepos):
        x = math.ceil(mousepos[1]/game.map.tilesize)-1
        y = math.ceil(mousepos[0]/game.map.tilesize)-1
        if y in range(0,game.map.width) and x in range(0,game.map.height):
            return x,y
        return -1,-1

    def check_entity_fit(self,width, height, x, y, entity):
        if (y + width) > game.map.width or (x + height) > game.map.height:
            return False
        for i in range(0,width):
            for j in range(0,height):
                en = self.which_entity(x+j, y+i)
                if en is not None and en != entity:
                    return False
        return True

    def tile_location(self,size):
        return size[1]*game.map.tilesize, size[0]*game.map.tilesize

    def make_popup(self,x, y, entity):
        global OLDSURF

        # draw drop down
        options = ["Move"] # mandatory option to have
        options += entity.get_actions()
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
        pygame.draw.lines(DISPLAYSURF, (255,0,0), True, [(left, top), (left+entity.size.get_width()*game.map.tilesize, top), (left+entity.size.get_width()*game.map.tilesize, top+entity.size.get_height()*game.map.tilesize), (left, top+entity.size.get_height()*game.map.tilesize)], 3)

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
        for e in ruleenactor.all_created_entities:
            if x in range(e.x,e.x+e.size.get_width()) and y in range(e.y,e.y+e.size.get_height()):
                return e
        return None

    # GM FUNCTIONS ------------------------------------------------------------------------------------------------

    def toggle_fog(self):
        self.clear_GM_info()
        self.display_message("_Toggle Fog Mode_\n\nA blue box around a tile indicates it is hidden by the Fog of War.\nPress ESC to exit this mode.")

        RUNNING = True
        while RUNNING:    
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
                    if game.map.fogOfWar[x][y]:
                        game.map.fogOfWar[x][y] = False
                        pygame.draw.lines(DISPLAYSURF, (0,0,255), True, [(left, top), (left+game.map.tilesize, top), (left+game.map.tilesize, top+game.map.tilesize), (left, top+game.map.tilesize)], 3)
                    else: 
                        game.map.fogOfWar[x][y] = True
                        pygame.draw.lines(DISPLAYSURF, (255,255,255), True, [(left, top), (left+game.map.tilesize, top), (left+game.map.tilesize, top+game.map.tilesize), (left, top+game.map.tilesize)], 3)
                    # test if fog of war works in the right location
                    # self.update_fog()
                elif event.type == KEYDOWN:   
                    if event.key == K_ESCAPE:
                        self.clear_GM_info()
                        self.help_screen()
                        return
            pygame.display.flip()
        return

    def add_texture(self):
        display_string = "_Add Texture Mode_\nPress ESC to exit this mode.\n\nSelect a texture:\n"
        display_string += self._images_string()
        
        self.clear_GM_info()
        self.display_message(display_string)

        input_box = InputBox(MAPOFFSET[0] + 200, game.map.tilesize*game.map.height, 500, 32, DISPLAYSURF)

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
                    x, y = gameview.which_tile(mousepos)
                    if selected_image is not None and x != -1 and y != -1:
                        texture = Map.Texture(x,y,1,1,selected_image)
                        game.map.textures[(x,y)] = texture
                        if self.which_entity(x,y) is None:
                            self.blit_texture(texture)
                elif event.type == KEYDOWN:   
                    if event.key == K_ESCAPE:
                        if selected_image is not None:
                            self.clear_GM_info()
                            self.display_message(display_string)
                            blit_input = True
                            selected_image = None
                        else:
                            self.clear_GM_info()
                            self.help_screen()
                            return
                    elif event.key == K_RETURN:
                        text = input_box.handle_event(event)
                        text = text.rstrip()
                        if text in IMAGES:
                            self.clear_GM_info()
                            blit_input = False
                            self.display_message("Please select tile you would like to place this texture")
                            selected_image = text
                text = input_box.handle_event(event)
            if blit_input:
                input_box.wipe()
                input_box.draw()
            pygame.display.flip()            

        return

    def _x_coordinate(self, surf, tpos):
        return tpos[0]+surf.get_width()+10

    def _y_coordinate(self, surf, tpos):
        return tpos[1]+surf.get_height()+10

    def _create_entity_help(self, reblit, error=""):
        self.clear_GM_info()
        buf, tpos = self.display_message("Create New Entity")

        if len(error)>0:
            ptext.draw(error, (tpos[0] + buf.get_width() + 10, tpos[1]), sysfontname="arial", color=COLOR_RED, fontsize=30)

        surf_name, tpos_name = ptext.draw("Name: ", (tpos[0], self._y_coordinate(buf, tpos)), sysfontname="arial", color=COLOR_WHITE, fontsize=30)
        surf_type, tpos_type = ptext.draw("Type: ", (tpos[0], self._y_coordinate(surf_name, tpos_name)), sysfontname="arial", color=COLOR_WHITE, fontsize=30)
        surf_image, tpos_image = ptext.draw("Image: ", (tpos[0], self._y_coordinate(surf_type, tpos_type)), sysfontname="arial", color=COLOR_WHITE, fontsize=30)
        if not reblit:
            input_name = InputBox(self._x_coordinate(surf_name, tpos_name), tpos_name[1]-5, 300, 32, DISPLAYSURF)
            input_type = InputBox(self._x_coordinate(surf_type, tpos_type), tpos_type[1]-5, 300, 32, DISPLAYSURF)
            input_image_filename = InputBox(self._x_coordinate(surf_image, tpos_image), tpos_image[1]-5, 300, 32, DISPLAYSURF)
        else:
            input_name = None
            input_type = None
            input_image_filename = None
        
        types = []
        for entity_type in ruleenactor.entity_types:
            types.append(entity_type.get_type())
        
        display_string = "Type Options: " + ", ".join(types) + "\nImage Options: "
        display_string += self._images_string()
        ptext.draw(display_string, (tpos[0], self._y_coordinate(surf_image, tpos_image)), sysfontname="arial", color=COLOR_WHITE, fontsize=30,  width = game.map.width*game.map.tilesize)
        
        return types, input_name, input_type, input_image_filename

    def create_new_entity(self):
        
        types, input_name, input_type, input_image_filename = self._create_entity_help(False)
        
        RUNNING = True
        selected_name = ""
        selected_type = ""
        selected_image_filename = ""
        blit_input = True
        while RUNNING:    
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mousepos = pygame.mouse.get_pos()
                    mousepos = (mousepos[0]-MAPOFFSET[0],mousepos[1]-MAPOFFSET[1])
                    x, y = gameview.which_tile(mousepos)
                    if len(selected_type)>0 and x != -1 and y != -1 and self.which_entity(x,y) is None:
                        entity = ruleenactor.add_new_entity(selected_type, selected_name, x, y)
                        entity.set_image_filename(selected_image_filename)
                        texture_image = pygame.transform.scale(IMAGES[entity.get_image_filename()], (entity.size.get_width()*game.map.tilesize,entity.size.get_height()*game.map.tilesize))
                        DISPLAYSURF.blit(texture_image, gameview.offset_blit(entity.y*game.map.tilesize, entity.x*game.map.tilesize))
                        selected_name = ""
                        selected_type = ""
                        selected_image_filename = ""
                        input_name.text = ""
                        input_type.text = ""
                        input_image_filename.text = ""
                        # game.entities.append(entity)
                        blit_input = True
                        self._create_entity_help(True)
                elif event.type == KEYDOWN:   
                    if event.key == K_ESCAPE:
                        self.clear_GM_info()
                        self.help_screen()
                        return
                    elif event.key == K_RETURN:
                        selected_name = input_name.text.rstrip()
                        selected_type = input_type.text.rstrip()
                        selected_image_filename = input_image_filename.text.rstrip()
                        if selected_image_filename not in IMAGES:
                            selected_image_filename = "default-image.png"
                        if selected_type in types:
                            blit_input = False
                            self.clear_GM_info()
                            self.display_message("Please select tile you would like to place this " + selected_name)
                        else:
                            input_name.text = ""
                            input_type.text = ""
                            input_image_filename.text = ""
                            self._create_entity_help(True, "WRONG TYPE")
                input_name.handle_event(event)
                input_type.handle_event(event)
                input_image_filename.handle_event(event)
            if blit_input:
                input_name.wipe()
                input_name.draw()
                input_type.wipe()
                input_type.draw()
                input_image_filename.wipe()
                input_image_filename.draw()
            pygame.display.flip()  

        return

    def edit_entity(self):
        self.clear_GM_info()
        self.display_message("Edit Entity _ACTIVE_")
        return

    def delete_entity(self):
        self.clear_GM_info()
        self.display_message("_Delete Entity_\nTo delete an entity please select a tile.\nOnce it is selected RED, press ENTER as a confirmation you wish to delete it.")
        # pick which one from the map and delete it

        RUNNING = True
        while RUNNING:    
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mousepos = pygame.mouse.get_pos()
                    mousepos = (mousepos[0]-MAPOFFSET[0],mousepos[1]-MAPOFFSET[1])
                    x, y = gameview.which_tile(mousepos)
                    if x != -1 and y != -1:
                        my_entity = gameview.which_entity(x, y)
                        if my_entity is not None:
                            # draw rectangle surrounding the actual box
                            left, top = self.tile_location((x, y))
                            saved_left, saved_top = self.offset_blit(left, top)
                            saved_x = x
                            saved_y = y
                            saved_entity = my_entity
                            pygame.draw.lines(DISPLAYSURF, COLOR_RED, True, [(saved_left, saved_top), (saved_left+game.map.tilesize, saved_top), (saved_left+game.map.tilesize, saved_top+game.map.tilesize), (saved_left, saved_top+game.map.tilesize)], 3)
                elif event.type == KEYDOWN:   
                    if event.key == K_ESCAPE:
                        if saved_entity is not None:
                            saved_entity = None
                            pygame.draw.lines(DISPLAYSURF, COLOR_WHITE, True, [(saved_left, saved_top), (saved_left+game.map.tilesize, saved_top), (saved_left+game.map.tilesize, saved_top+game.map.tilesize), (saved_left, saved_top+game.map.tilesize)], 3)
                        else:
                            self.clear_GM_info()
                            self.help_screen()
                            return
                    elif event.key == K_RETURN:
                        if saved_entity is not None:
                            ruleenactor.remove_entity(saved_entity)
                            if (saved_x,saved_y) in game.map.textures:
                                self.blit_texture(game.map.textures[(saved_x,saved_y)])
                            else:
                                self.blit_default(saved_x, saved_y)
                            saved_entity = None
                            pygame.draw.lines(DISPLAYSURF, COLOR_WHITE, True, [(saved_left, saved_top), (saved_left+game.map.tilesize, saved_top), (saved_left+game.map.tilesize, saved_top+game.map.tilesize), (saved_left, saved_top+game.map.tilesize)], 3)
            pygame.display.flip()
        return

    def add_asset(self):
        self.clear_GM_info()
        general_message = "_Add Asset Mode_\nEnter in the path to an image.\nPress ESC to exit this mode."
        self.display_message(general_message)
        if not os.path.exists("/tmp"):
            os.makedirs('/tmp')

        input_box = InputBox(MAPOFFSET[0] + 300, game.map.tilesize*game.map.height, 500, 32, DISPLAYSURF)

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
                                global IMAGES
                                IMAGES = self.load_pictures() # update the current IMAGES stored
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
        number_of = InputBox(buf, game.map.tilesize*game.map.height, 50, 32, DISPLAYSURF)
        surf, tpos = ptext.draw("d", (buf + 60, game.map.tilesize*game.map.height + 10), sysfontname="arial", color=COLOR_WHITE, fontsize=30)
        buf = tpos[0] + surf.get_width() + 10
        d_roll = InputBox(buf, game.map.tilesize*game.map.height, 50, 32, DISPLAYSURF)

        myrect = pygame.Rect(MAPOFFSET[0], game.map.tilesize*game.map.height + surf.get_height() + 10, game.map.width*game.map.tilesize, DISPLAYSURF.get_height()-(game.map.tilesize*game.map.height))

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
                            d_string = number_of.text + "d" + d_roll.text
                            result = ruleenactor.roll_dice(d_string)
                            surf, tpos = ptext.draw(d_string +" = "+ str(result), (MAPOFFSET[0] + 10, game.map.tilesize*game.map.height + surf.get_height() + 10), sysfontname="arial", color=COLOR_WHITE, fontsize=30)
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
        myrect = pygame.Rect(MAPOFFSET[0], game.map.tilesize*game.map.height, game.map.width*game.map.tilesize, DISPLAYSURF.get_height()-(game.map.tilesize*game.map.height))
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
        txt_surface, tpos = ptext.draw(message, (MAPOFFSET[0] + 10, game.map.tilesize*game.map.height + 10), sysfontname="arial", color=COLOR_WHITE, fontsize=30, width = game.map.width*game.map.tilesize, underlinetag="_")
        return txt_surface, tpos

    def update_fog(self):
        fogImage = pygame.transform.scale(IMAGES["fog.png"], (game.map.tilesize,game.map.tilesize))
        for rw in range(game.map.height):
            for cl in range(game.map.width):
                if not game.map.fogOfWar[rw][cl]:
                    DISPLAYSURF.blit(fogImage, gameview.offset_blit(cl*game.map.tilesize, rw*game.map.tilesize))
        return

    def update_fog_GM(self):
        for rw in range(game.map.height):
            for cl in range(game.map.width):
                if not game.map.fogOfWar[rw][cl]:
                    left, top = self.tile_location((rw, cl))
                    left, top = self.offset_blit(left, top)
                    pygame.draw.lines(DISPLAYSURF, (0,0,255), True, [(left, top), (left+game.map.tilesize, top), (left+game.map.tilesize, top+game.map.tilesize), (left, top+game.map.tilesize)], 3)    
        return

    def _images_string(self):
        global IMAGES
        IMAGES = self.load_pictures()
        display_string = ""
        for key in IMAGES:
            display_string += key + ", "
        return display_string

    def blit_texture(self, texture):
        texture_image = pygame.transform.scale(IMAGES[texture.name], (texture.width*game.map.tilesize,texture.height*game.map.tilesize))
        DISPLAYSURF.blit(texture_image, gameview.offset_blit(texture.y*game.map.tilesize, texture.x*game.map.tilesize))
        return

    def blit_default(self, x, y):
        DISPLAYSURF.blit(DEFAULT_IMAGE, gameview.offset_blit(y*game.map.tilesize, x*game.map.tilesize))
        return

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

# utilized for testing of actions drop down menu
# class Entity:
#     def __init__(self, x, y, width, height, name, actions):
#         self.width = width
#         self.height = height
#         self.x = x
#         self.y = y
#         self.name = name
#         self.actions = actions
#         self.attributes = ["example attributes", "example 2", "example 3"]

#     def __str__(self):
#         return  "Entity:\nName: "+self.name+"\nwidth: "+str(self.width)+"\nheight: "+str(self.height)+"\nx: "+ str(self.x)+ "\ny: " + str(self.y) +"\nactions: "+str(self.actions)+"\nattributes: "+str(self.attributes)


# ------------------------------------------------------------------------------------------------------------
# GLOBAL VAR
MAPOFFSET = (200,0)
OLDSURF = None
gameview = GameView()

IMAGES = gameview.load_pictures()

# Game Class
game = Game()
game.name = "Test Suite"
game.uniqueID = 1
game.map = Map(tilesize = 50, height = 10, width = 18)
# Entities used for testing
# game.entities = [Entity(5,5,2,2,"water.png",["Attack","Defend"]),Entity(2,2,1,1,"rock.png",["Sit"]),Entity(2,3,1,1,"rock.png",["Defend"])]

# Rule Validation
ruleenactor = RuleEnactor()
_validator = _Validator()
isTemplate = False
hp_time = Attribute("HP", 10)    
ac_time = Attribute("AC", 15)    
template = Entity("", "entity", 1, 1, isTemplate, None)
template.add_attribute(hp_time)
template.add_attribute(ac_time)
_validator.add_entity(template)

ruleenactor.parse_validator(_validator) # sets up relationships and entity types

pygame.init()
# FONTTYPE = pygame.font.SysFont('arial', 25)
# GENERAL COLORS AND ITEMS
FONTTYPE = pygame.font.Font(None, 32)
DISPLAYSURF = pygame.display.set_mode((1300,750))
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
GM_STATUS = True
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
DEFAULT_IMAGE = pygame.transform.scale(IMAGES["grey.png"], (game.map.tilesize,game.map.tilesize))

# -----------------------------------------------------------------------------------------------------------------------

def main():
    # create the map and add add textures to it
    game.map.textures[(3,3)] = Map.Texture(3,3,1,1,"grass.png")
    game.map.textures[(3,4)] = Map.Texture(3,4,1,1,"grass.png")
    
    #example fog
    game.map.fogOfWar[8][15] = False
    game.map.fogOfWar[8][16] = False
    game.map.fogOfWar[9][15] = False
    game.map.fogOfWar[9][16] = False

    # create the entire background
    
    for rw in range(game.map.height):
        for cl in range(game.map.width):
            gameview.blit_default(rw,cl)
            
    # put all the textures on the map
    for key, texture in game.map.textures.items():
        gameview.blit_texture(texture)

    fogImage = pygame.transform.scale(IMAGES["fog.png"], (game.map.tilesize,game.map.tilesize))
    if not GM_STATUS:
        for rw in range(game.map.height):
            for cl in range(game.map.width):
                if not game.map.fogOfWar[rw][c]:
                    DISPLAYSURF.blit(fogImage, gameview.offset_blit(cl*game.map.tilesize, rw*game.map.tilesize))

    # put all the entities on the map
    # for entity in game.entities:
    #     entity_image = pygame.transform.scale(IMAGES[entity.name], (entity.size.get_width()*game.map.tilesize,entity.size.get_height()*game.map.tilesize))
    #     DISPLAYSURF.blit(entity_image, gameview.offset_blit(entity.y*game.map.tilesize, entity.x*game.map.tilesize))

    if GM_STATUS:
        gameview.help_screen()

    my_entity = None
    input_box = InputBox(MAPOFFSET[0]+game.map.width*game.map.tilesize, DISPLAYSURF.get_height()-200, 200, 32, DISPLAYSURF)
    history = Transcript(MAPOFFSET[0]+game.map.width*game.map.tilesize, MAPOFFSET[1], 200, DISPLAYSURF.get_height()-(DISPLAYSURF.get_height()-input_box.rect.y), DISPLAYSURF)
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
                        rowsize = size[1]/(len(my_entity.get_actions())+1)
                        option_selected = math.floor((mousepos[1]-location[1])/rowsize)
                        if option_selected == 0:
                            action_requested = "Move"
                        else:
                            action_requested = my_entity.get_actions()[option_selected-1]
                            my_entity = None
                        print(action_requested)
                    else:
                        my_entity = None
                elif my_entity is not None and action_requested is "Move":
                    # grab new location
                    x, y = gameview.which_tile(mousepos)
                    # if it is a valid locatin and there are no other game.entities there
                    if x != -1 and y != -1 and gameview.check_entity_fit(my_entity.size.get_width(), my_entity.size.get_height(), x, y, my_entity):
                        # remove old image and replace with generic block, then cover with texture if there are any       
                        for i in range(0,my_entity.size.get_width()):
                            for j in range(0,my_entity.size.get_height()):
                                if (my_entity.x+j, my_entity.y+i) in game.map.textures:
                                    gameview.blit_texture(game.map.textures[(my_entity.x+j, my_entity.y+i)])
                                else:
                                    gameview.blit_default((my_entity.x+j), (my_entity.y+i))
                        # blit entity to it
                        my_entity.x = x
                        my_entity.y = y
                        my_entity_image = pygame.transform.scale(IMAGES[my_entity.get_image_filename()], (my_entity.size.get_width()*game.map.tilesize,my_entity.size.get_height()*game.map.tilesize))
                        DISPLAYSURF.blit(my_entity_image, gameview.offset_blit(my_entity.y*game.map.tilesize, my_entity.x*game.map.tilesize))
                    # wipe signals
                    action_requested = ""
                    my_entity = None
                else:
                    x, y = gameview.which_tile(mousepos)
                    my_entity = gameview.which_entity(x, y)
                    if my_entity is not None:
                        if (my_entity.y + my_entity.size.get_width()) >= game.map.width or (my_entity.x + my_entity.size.get_height()) >= game.map.height:
                            loc_x, loc_y = gameview.tile_location((my_entity.x,my_entity.y))
                        else:    
                            loc_x, loc_y = gameview.tile_location((my_entity.size.get_width()+my_entity.x,my_entity.size.get_height()+my_entity.y))
                        size, location = gameview.make_popup(loc_x, loc_y, my_entity)
            elif event.type == KEYDOWN:   
                if event.key == K_ESCAPE:
                    RUNNING = False
                elif GM_STATUS and event.unicode in GM_HOTKEYS:
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

        if GM_STATUS:
            gameview.update_fog_GM()

        pygame.display.flip()


if __name__ == "__main__":
    main()