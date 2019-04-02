import pygame, sys, random, os, math, re, ptext, pyautogui, time, platform, subprocess, clipboard, jsonpickle
import base64, PIL.Image
from pygame.locals import *
from game_engine.map import Map
from client import Client
from shutil import copyfile
sys.path.append('rule_interpreter/')
sys.path.append('rule_interpreter/models')
from game_engine.game import Game
from game_engine.rule_enactor import RuleEnactor
from rule_interpreter.models.validator import _Validator
from rule_interpreter.models.attribute import Attribute
from rule_interpreter.models.entity import Entity
from rule_interpreter.models.action import Action
from rule_interpreter.models.point import Point
from play_game import async_send
import shared_var

# sources for examples:
# http://usingpython.com/pygame-tilemaps/
# http://usingpython.com/list-comprehension/

class GameView:

    def __init__(self):
        self.images = {}
        self.load_pictures()
        return

    def leave_game(self, full_exit=True):
        if GM_STATUS:
            print("trying to end game")
            end_game_message = "GM {} ended the game session".format(client.user.get_username())
            game.append_transcript(end_game_message)
            client.update_game(game.get_uniqueID(), jsonpickle.encode(game))
            async_send(['chat', [client_id, end_game_message]])
            async_send(['end_game', [client_id, game.get_uniqueID()]])
        else:
            print("player leaving game")
            leave_game_message = "{} left the game".format(client.user.get_username())
            game.append_transcript(leave_game_message)
            async_send(['chat', [client_id, leave_game_message]])
            async_send(['leave_game', [client_id]])
        if full_exit:
            pygame.quit()
            sys.exit()
        return

    def send_update_to_all(self):
        client.update_game(game.get_uniqueID(), jsonpickle.encode(game))
        async_send(["update_game", [client_id, game.get_uniqueID()]])       
        return

    def offset_blit(self,x,y):
        return (x+MAPOFFSET[0],y+MAPOFFSET[1])

    def which_tile(self,mousepos):
        x = math.ceil(mousepos[1]/game.map.tilesize)-1
        y = math.ceil(mousepos[0]/game.map.tilesize)-1
        if y in range(0,game.map.width) and x in range(0,game.map.height):
            return x,y
        return -1,-1

    def check_entity_fit(self, width, height, x, y, entity):
        # in the case of moving where entity already is
        if str((x, y)) in game.ruleset_copy.all_created_entities:
            if game.ruleset_copy.all_created_entities[str((x, y))] == entity: # is it itself
                return True
            else: # another entity is there
                return False

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
        options += entity.get_action_names()
        textSurf = []
        width = 0
        height = 0
        OLDSURF = DISPLAYSURF.copy()

        self.draw_entity_box(entity.x, entity.y, width = entity.size.get_width(), height = entity.size.get_height())
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

        # entity information to display on the left
        ptext.draw(str(entity), (5, 100), sysfontname="arial", color=COLOR_WHITE, fontsize=FONTSIZE, width = 200)

        return (popupSurf.get_width(), popupSurf.get_height()), (x,y)

    def remove_previous_popup(self):
        DISPLAYSURF.blit(OLDSURF, (0,0))

    def load_pictures_from_database(self, asset_name=None):
        # Grab all pictures located in database and put into tmp folder
        if not os.path.exists("./tmp/"):
            os.makedirs('./tmp')
        direc = os.getcwd() + "/tmp/"
        arr = []
        if asset_name:
            arr = client.get_asset(game.GM.get_username(), asset_name)    
        else:
            arr = client.get_assets(game.GM.get_username(), game.get_assets())

        try:
            for asset in arr:
                print(asset)
                decoded_image = base64.b64decode(asset[1][0])        
                with open(direc+asset[0], 'wb') as recreated:
                    recreated.write(bytearray(decoded_image))
        except Exception as e:
            print("ITEM WAS NOT PROPERLY GRABBED")
            print(e)

        self.load_pictures()
        return 

    def load_pictures(self):
        # Grab all pictures located in the textures directory and temporary folder
        direc = os.getcwd() + "/images/textures/"
        pictures = [i for i in os.listdir(direc)]
        for p in pictures:
            if p.endswith(".png") or p.endswith(".jpg") or p.endswith(".jpeg"):
                self.images[p] = pygame.image.load("images/textures/"+p)

        if os.path.exists("./tmp/"):
            direc = os.getcwd() + "/tmp/"
            pictures = [i for i in os.listdir(direc)]
            for p in pictures:
                if p.endswith(".png") or p.endswith(".jpg") or p.endswith(".jpeg"):
                    self.images[p] = pygame.image.load("tmp/"+p)
        return 

    def which_entity(self, x, y):
        for key, e in game.ruleset_copy.all_created_entities.items():
            if x in range(e.x,e.x+e.size.get_width()) and y in range(e.y,e.y+e.size.get_height()):
                return e
        return None

    def draw_entity_box(self, x, y, color = (255, 0, 0), width = 1, height = 1):    
        left, top = self.tile_location((x, y))
        left, top = self.offset_blit(left, top)
        pygame.draw.lines(DISPLAYSURF, color, True, [(left, top), (left+game.map.tilesize*width, top), (left+game.map.tilesize*width, top+game.map.tilesize*height), (left, top+game.map.tilesize*height)], 3)
        return 

    def action_sequence(self, result):
        self.clear_bottom_info()
        self.display_message("Please select a(n) " + result + " from the map!")
        pygame.display.flip()
        # pick which one from the map

        RUNNING = True
        while RUNNING:    
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.leave_game()
                elif event.type == MOUSEBUTTONDOWN:
                    mousepos = pygame.mouse.get_pos()
                    mousepos = (mousepos[0]-MAPOFFSET[0],mousepos[1]-MAPOFFSET[1])
                    x, y = GAMEVIEW.which_tile(mousepos)
                    if x != -1 and y != -1:
                        my_entity = GAMEVIEW.which_entity(x, y)
                        if result == "point":
                            return Point(x,y)
                        elif my_entity is not None and my_entity.is_of_type(result):
                            return my_entity
        return

    def blit_entire_map(self):
        # create the entire background
        for rw in range(game.map.height):
            for cl in range(game.map.width):
                self.blit_default(rw,cl)
                
        # put all the textures on the map
        for key, texture in game.map.textures.items():
            self.blit_texture(texture)

        # put all the entities on the map
        for location, entity in game.ruleset_copy.all_created_entities.items():
            entity_image = pygame.transform.scale(self.images[entity.get_image_filename()], (entity.size.get_width()*game.map.tilesize,entity.size.get_height()*game.map.tilesize))
            DISPLAYSURF.blit(entity_image, self.offset_blit(entity.y*game.map.tilesize, entity.x*game.map.tilesize))
        
        # blit fog of war overtop everything
        if not GM_STATUS:
            for rw in range(game.map.height):
                for cl in range(game.map.width):
                    if not game.map.fogOfWar[rw][cl]:
                        DISPLAYSURF.blit(FOG_IMAGE, self.offset_blit(cl*game.map.tilesize, rw*game.map.tilesize))
        return

    # GM FUNCTIONS ------------------------------------------------------------------------------------------------
    def join_request_popup(self):
        print("IM IN THE JOIN REQUEST POPUP")
        OLDSURF = DISPLAYSURF.copy()
        popup = pygame.image.load("images/menu/joinRequestPopup2.png").convert_alpha()

        join_request_timeout = 40
        start = time.time()
        running = True
        while(time.time()-start < join_request_timeout and running):
            DISPLAYSURF.blit(popup, (0,0))  
            ptext.draw("{}".format(shared_var.MESSAGE_CONTENT[0][1]), (610, 325), sysfontname="arial", color=COLOR_WHITE, fontsize=24, width = 100)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.leave_game()
                elif event.type == KEYDOWN:   
                    if event.key == K_y:
                        # send the request yes
                        game.append_transcript("player {} joined the game".format(shared_var.MESSAGE_CONTENT[0][1]))
                        # shared_var.MESSAGE_CONTENT.append(game.get_uniqueID())
                        async_send(['accept_join', shared_var.MESSAGE_CONTENT])
                        running = False
                    elif event.key == K_n:
                        # send the request no
                        async_send(['reject_join', shared_var.MESSAGE_CONTENT])
                        running = False
        if running:
            # send the request no
            async_send(['reject_join', shared_var.MESSAGE_CONTENT])
        DISPLAYSURF.blit(OLDSURF, (0,0))
        pygame.display.flip()
        return

    def gm_leaves_room_popup(self):
        print("IM IN THE LEAVE ROOM POPUP")
        # popupSurf = pygame.Surface((200,200))
        # popupSurf.fill(COLOR_BLACK)
        # x = DISPLAYSIZE[0]/2-popupSurf.get_width()+MAPOFFSET[0]
        # y = DISPLAYSIZE[1]/2-popupSurf.get_height()+MAPOFFSET[1]

        # DISPLAYSURF.blit(popupSurf, (x,y))  
        # ptext.draw("The GM left the room! Closing in 8seconds.", (x+5,y+5), sysfontname="arial", color=COLOR_WHITE, fontsize=FONTSIZE, width = 200)
        # pygame.display.update()

        # time.sleep(5)

        # join_request_timeout = 5
        # start = time.time()
        # while(time.time()-start < join_request_timeout):  
        #     pass
        shared_var.GM_LEAVES_FLAG = False
        return

    def action_request_popup(self):
        global game
        print("IM IN THE ACTION REQUEST POPUP")
        OLDSURF = DISPLAYSURF.copy()
        popup = pygame.image.load("images/menu/actionRequestPopup.png").convert_alpha()

        join_request_timeout = 40
        start = time.time()
        running = True
        print(shared_var.MESSAGE_CONTENT)
        while(time.time()-start < join_request_timeout and running): 
            DISPLAYSURF.blit(popup, (0,0))  
            ptext.draw("{}".format(shared_var.MESSAGE_CONTENT[2]), (600, 300), sysfontname="arial", color=COLOR_WHITE, fontsize=24, width = 250)
            ptext.draw("{}".format(shared_var.MESSAGE_CONTENT[3]), (505, 365), sysfontname="arial", color=COLOR_WHITE, fontsize=20, width = 300)
            pygame.display.flip() 
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.leave_game()
                elif event.type == KEYDOWN:   
                    if event.key == K_y:
                        gameObj = client.get_game_from_room_number(game.get_uniqueID())
                        game = jsonpickle.decode(gameObj[0][0])
                        game.append_transcript("player {} did an action: {}".format(shared_var.MESSAGE_CONTENT[2], shared_var.MESSAGE_CONTENT[3]))
                        running = False
                    elif event.key == K_n:
                        # send the request no
                        game.append_transcript("player {} action rejected".format(shared_var.MESSAGE_CONTENT[2]))
                        running = False
        
        DISPLAYSURF.blit(OLDSURF, (0,0))
        # whether timed out or the GM responded, send the GM's game to everyone
        self.blit_entire_map()
        self.send_update_to_all()
        pygame.display.flip()
        return

    def toggle_fog(self):
        self.clear_bottom_info()
        self.display_message("_Toggle Fog Mode_\n\nA blue box around a tile indicates it is hidden by the Fog of War.\nPress ESC to exit this mode.")

        RUNNING = True
        while RUNNING:    
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.leave_game()
                elif event.type == MOUSEBUTTONDOWN:
                    mousepos = pygame.mouse.get_pos()
                    mousepos = (mousepos[0]-MAPOFFSET[0],mousepos[1]-MAPOFFSET[1])
                    x, y = GAMEVIEW.which_tile(mousepos)
                    if x != -1 or y != -1:
                        # draw rectangle surrounding the actual box
                        if game.map.fogOfWar[x][y]:
                            game.map.fogOfWar[x][y] = False
                            color = (0,0,255)
                        else: 
                            game.map.fogOfWar[x][y] = True
                            color = (255,255,255)
                        self.draw_entity_box(x,y,color)
                        # test if fog of war works in the right location
                        # self.update_fog()
                elif event.type == KEYDOWN:   
                    if event.key == K_ESCAPE:
                        self.clear_bottom_info()
                        return
            pygame.display.flip()
        return

    def add_texture(self):
        display_string = "*Add Texture Mode*\nPress ESC to exit this mode.\n\nSelect a texture:\n"
        display_string += self._images_string()
        
        self.clear_bottom_info()
        self.display_message(display_string, "*")

        add_texture_box = InputBox(MAPOFFSET[0] + 200, game.map.tilesize*game.map.height, game.map.tilesize*game.map.width - 200, 32, DISPLAYSURF)

        RUNNING = True
        text = ""
        selected_image = None
        blit_input = True
        while RUNNING:    
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.leave_game()
                elif event.type == MOUSEBUTTONDOWN:
                    mousepos = pygame.mouse.get_pos()
                    mousepos = (mousepos[0]-MAPOFFSET[0],mousepos[1]-MAPOFFSET[1])
                    x, y = GAMEVIEW.which_tile(mousepos)
                    if selected_image is not None and x != -1 and y != -1:
                        texture = Map.Texture(x,y,1,1,selected_image)
                        game.map.textures[(x,y)] = texture
                        if self.which_entity(x,y) is None:
                            self.blit_default(x,y)
                            self.blit_texture(texture)
                elif event.type == KEYDOWN:   
                    if event.key == K_ESCAPE:
                        if selected_image is not None:
                            self.clear_bottom_info()
                            self.display_message(display_string, "*")
                            blit_input = True
                            selected_image = None
                        else:
                            self.clear_bottom_info()
                            return
                    elif event.key == K_RETURN:
                        text = add_texture_box.text.rstrip()
                        if text in self.images:
                            self.clear_bottom_info()
                            blit_input = False
                            self.display_message("Please select tile you would like to place this texture")
                            selected_image = text
                add_texture_box.handle_event(event)
            if blit_input:
                add_texture_box.wipe()
                add_texture_box.draw()
            pygame.display.flip()            

        return

    def _x_coordinate(self, surf, tpos):
        return tpos[0]+surf.get_width()+10

    def _y_coordinate(self, surf, tpos):
        return tpos[1]+surf.get_height()+10

    def _input_box_width(self, surf):
        return game.map.tilesize*game.map.width - surf.get_width() - 30

    def _create_entity_help(self, reblit, error=""):
        self.clear_bottom_info()
        buf, tpos = self.display_message("_Create New Entity_ ")

        if len(error)>0:
            ptext.draw(error, (tpos[0] + buf.get_width() + 10, tpos[1]), sysfontname="arial", color=COLOR_RED, fontsize=FONTSIZE)

        surf_name, tpos_name = ptext.draw("Name: ", (tpos[0], self._y_coordinate(buf, tpos)), sysfontname="arial", color=COLOR_WHITE, fontsize=FONTSIZE)
        surf_type, tpos_type = ptext.draw("Type: ", (tpos[0], self._y_coordinate(surf_name, tpos_name)), sysfontname="arial", color=COLOR_WHITE, fontsize=FONTSIZE)
        surf_image, tpos_image = ptext.draw("Image: ", (tpos[0], self._y_coordinate(surf_type, tpos_type)), sysfontname="arial", color=COLOR_WHITE, fontsize=FONTSIZE)
        if not reblit:
            input_name = InputBox(self._x_coordinate(surf_name, tpos_name), tpos_name[1]-5, self._input_box_width(surf_name), 32, DISPLAYSURF)
            input_type = InputBox(self._x_coordinate(surf_type, tpos_type), tpos_type[1]-5, self._input_box_width(surf_type), 32, DISPLAYSURF)
            input_image_filename = InputBox(self._x_coordinate(surf_image, tpos_image), tpos_image[1]-5, self._input_box_width(surf_image), 32, DISPLAYSURF)
        else:
            input_name = None
            input_type = None
            input_image_filename = None
        
        display_string = "Type Options: " + ", ".join(CONCRETE_TYPES_OF_ENTITIES) + "\nImage Options: "
        display_string += self._images_string()
        ptext.draw(display_string, (tpos[0], self._y_coordinate(surf_image, tpos_image)), sysfontname="arial", color=COLOR_WHITE, fontsize=FONTSIZE,  width = game.map.width*game.map.tilesize)
        
        return input_name, input_type, input_image_filename

    def create_new_entity(self):
        
        input_name, input_type, input_image_filename = self._create_entity_help(False)
        
        RUNNING = True
        selected_name = ""
        selected_type = ""
        selected_image_filename = ""
        blit_input = True
        while RUNNING:    
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.leave_game()
                elif event.type == MOUSEBUTTONDOWN:
                    mousepos = pygame.mouse.get_pos()
                    mousepos = (mousepos[0]-MAPOFFSET[0],mousepos[1]-MAPOFFSET[1])
                    x, y = GAMEVIEW.which_tile(mousepos)
                    if len(selected_type)>0 and x != -1 and y != -1 and self.which_entity(x,y) is None:
                        entity = game.ruleset_copy.add_new_entity(selected_type, selected_name, x, y)
                        if GAMEVIEW.check_entity_fit(entity.size.get_width(), entity.size.get_height(), x, y, entity):
                            entity.set_image_filename(selected_image_filename)
                            texture_image = pygame.transform.scale(self.images[entity.get_image_filename()], (entity.size.get_width()*game.map.tilesize,entity.size.get_height()*game.map.tilesize))
                            DISPLAYSURF.blit(texture_image, GAMEVIEW.offset_blit(entity.y*game.map.tilesize, entity.x*game.map.tilesize))
                        else:
                            game.ruleset_copy.remove_entity(entity)
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
                        self.clear_bottom_info()
                        return
                    elif event.key == K_RETURN:
                        selected_name = input_name.text.rstrip()
                        selected_type = input_type.text.rstrip()
                        selected_image_filename = input_image_filename.text.rstrip()
                        if selected_image_filename not in self.images:
                            selected_image_filename = "default-image.png"
                        if selected_type in CONCRETE_TYPES_OF_ENTITIES:
                            blit_input = False
                            self.clear_bottom_info()
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
        self.clear_bottom_info()
        buf, tpos = self.display_message("_Edit Entity_\nSelect an entity, then enter the name of an attribute and its new value, then press ENTER.\nPress ESC to exit this mode.")

        surf_name, tpos_name = ptext.draw("Name: ", (tpos[0], self._y_coordinate(buf, tpos)), sysfontname="arial", color=COLOR_WHITE, fontsize=FONTSIZE)
        surf_value, tpos_value = ptext.draw("Value: ", (tpos[0], self._y_coordinate(surf_name, tpos_name)), sysfontname="arial", color=COLOR_WHITE, fontsize=FONTSIZE)
        input_name = InputBox(self._x_coordinate(surf_name, tpos_name), tpos_name[1]-5, self._input_box_width(surf_name), 32, DISPLAYSURF)
        input_value = InputBox(self._x_coordinate(surf_value, tpos_value), tpos_value[1]-5, self._input_box_width(surf_value), 32, DISPLAYSURF)

        RUNNING = True
        saved_entity = None
        attributes = {}
        while RUNNING:    
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.leave_game()
                elif event.type == MOUSEBUTTONDOWN:
                    if saved_entity is None:
                        mousepos = pygame.mouse.get_pos()
                        mousepos = (mousepos[0]-MAPOFFSET[0],mousepos[1]-MAPOFFSET[1])
                        print(mousepos)
                        x, y = GAMEVIEW.which_tile(mousepos)
                        if x != -1 and y != -1:
                            my_entity = GAMEVIEW.which_entity(x, y)
                            if my_entity is not None:
                                # draw rectangle surrounding the actual box
                                saved_entity = my_entity
                                self.draw_entity_box(saved_entity.x,saved_entity.y, width = saved_entity.size.get_width(), height = saved_entity.size.get_height())
                                self.clear_bottom_info(tpos[0], self._y_coordinate(surf_value, tpos_value))
                                attributes = []
                                for attr in my_entity.get_attributes():
                                    attributes.append(attr.get_attribute_name())
                                display_string = "Attribute Option Name: " + ", ".join(attributes)
                                surf_attr, tpos_attr = ptext.draw(display_string, (tpos[0], self._y_coordinate(surf_value, tpos_value)), sysfontname="arial", color=COLOR_WHITE, fontsize=FONTSIZE)
                elif event.type == KEYDOWN:   
                    if event.key == K_ESCAPE:
                        self.clear_bottom_info()
                        if saved_entity:
                            self.draw_entity_box(saved_entity.x, saved_entity.y, COLOR_WHITE, width = saved_entity.size.get_width(), height = saved_entity.size.get_height())
                        return
                    elif event.key == K_RETURN:
                        # if there is an entity and its attribute given exists
                        modifying_attr = input_name.text.strip()
                        if saved_entity is not None:
                            if modifying_attr in attributes:
                                new_value = input_value.text.strip()
                                type_of_attr = saved_entity.get_attribute(modifying_attr).get_attribute_type()
                                if type_of_attr == bool:
                                    if new_value.lower() == "true":
                                        game.ruleset_copy.modify_attribute(saved_entity, modifying_attr, True)
                                    elif new_value.lower() == "false":
                                        game.ruleset_copy.modify_attribute(saved_entity, modifying_attr, False)
                                elif type_of_attr == float:
                                    try:
                                        game.ruleset_copy.modify_attribute(saved_entity, modifying_attr, float(new_value))
                                    except Exception as e:
                                        pass
                                elif type_of_attr == str:
                                    game.ruleset_copy.modify_attribute(saved_entity, modifying_attr, new_value)
                            self.draw_entity_box(saved_entity.x, saved_entity.y, COLOR_WHITE, width = saved_entity.size.get_width(), height = saved_entity.size.get_height())
                        saved_entity = None
                        input_name.text = ""
                        input_value.text = ""
                        # wipe the attr info
                        self.clear_bottom_info(tpos[0], self._y_coordinate(surf_value, tpos_value))
                input_name.handle_event(event)
                input_value.handle_event(event)
            input_name.wipe()
            input_name.draw()
            input_value.wipe()
            input_value.draw()
            pygame.display.flip()

        return


    def delete_entity(self):
        self.clear_bottom_info()
        self.display_message("_Delete Entity_\nTo delete an entity please select a tile.\nOnce it is selected RED, press ENTER as a confirmation you wish to delete it.\nOtherwise, press ESC or another spot on the map to deselect it.")
        # pick which one from the map and delete it

        RUNNING = True
        saved_entity = None
        while RUNNING:    
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.leave_game()
                elif event.type == MOUSEBUTTONDOWN:
                    mousepos = pygame.mouse.get_pos()
                    mousepos = (mousepos[0]-MAPOFFSET[0],mousepos[1]-MAPOFFSET[1])
                    x, y = GAMEVIEW.which_tile(mousepos)
                    if x != -1 and y != -1:
                        my_entity = GAMEVIEW.which_entity(x, y)
                        if saved_entity is not None:
                            self.draw_entity_box(saved_entity.x, saved_entity.y, COLOR_WHITE, width = saved_entity.size.get_width(), height = saved_entity.size.get_height())
                            saved_entity = None
                        if my_entity is not None:
                            # draw rectangle surrounding the actual box
                            saved_entity = my_entity
                            self.draw_entity_box(saved_entity.x,saved_entity.y, width = saved_entity.size.get_width(), height = saved_entity.size.get_height())
                elif event.type == KEYDOWN:   
                    if event.key == K_ESCAPE:
                        if saved_entity is not None:
                            self.draw_entity_box(saved_entity.x, saved_entity.y, COLOR_WHITE, width = saved_entity.size.get_width(), height = saved_entity.size.get_height())
                            saved_entity = None
                        else:
                            self.clear_bottom_info()
                            return
                    elif event.key == K_RETURN:
                        if saved_entity is not None:
                            game.ruleset_copy.remove_entity(saved_entity)
                            if (saved_entity.x,saved_entity.y) in game.map.textures:
                                self.blit_texture(game.map.textures[(saved_entity.x,saved_entity.y)])
                            else:
                                self.blit_default(saved_entity.x, saved_entity.y)
                            self.draw_entity_box(saved_entity.x, saved_entity.y, COLOR_WHITE, width = saved_entity.size.get_width(), height = saved_entity.size.get_height())
                            saved_entity = None
            pygame.display.flip()
        return

    def add_asset(self):
        self.clear_bottom_info()
        general_message = "_Add Asset Mode_\nEnter in the path to an image.\nRight click the input box to paste a file name path.\nPress ESC to exit this mode."
        self.display_message(general_message)
        if not os.path.exists("./tmp/"):
            os.makedirs('./tmp')

        add_asset_box = InputBox(MAPOFFSET[0] + 300, game.map.tilesize*game.map.height, game.map.tilesize*game.map.width - 300, 32, DISPLAYSURF)

        RUNNING = True
        text = ""
        while RUNNING:    
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.leave_game()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 3:
                        add_asset_box.text = clipboard.paste()
                elif event.type == KEYDOWN:   
                    if event.key == K_ESCAPE:
                        self.clear_bottom_info()
                        return
                    elif event.key == K_RETURN:
                        text = add_asset_box.text.rstrip()
                        if os.path.isfile(text):
                            if text.split(".")[-1] not in ["png", "jpg", "jpeg"]:
                                self.clear_bottom_info()
                                self.display_message("_FILE IS NOT AN IMAGE_\n"+general_message)
                            else:
                                if platform.system() == "Windows":
                                    filename = text.split("\\")[-1]
                                else:
                                    filename = text.split("/")[-1]
                                new_name = os.getcwd() + "/tmp/" + filename
                                copyfile(text, new_name)
                                self.load_pictures()
                                # insert into database
                                with open(new_name, 'rb') as f:
                                    photo = f.read()
                                encoded_image = base64.b64encode(photo)
                                client.add_asset(client.user.get_username(), filename, encoded_image)
                                game.add_asset(filename)
                                # send request to everyone to grab this asset
                                async_send(["asset_added",[client_id, filename]])
                                self.clear_bottom_info()
                                self.display_message("_FILE ADDED_\n"+general_message)
                        else: 
                            self.clear_bottom_info()
                            self.display_message("_FILE DOES NOT EXIST_\n"+general_message)
                add_asset_box.handle_event(event)
            add_asset_box.wipe()
            add_asset_box.draw()
            pygame.display.flip()  

        return
    
    def remove_player(self):
        self.clear_bottom_info()
        self.display_message("_Remove Player_\n")
        return

    def roll_dice(self):
        self.clear_bottom_info()
        surf, tpos = self.display_message("Roll:")

        buf = MAPOFFSET[0] + surf.get_width() + 10
        number_of = InputBox(buf, game.map.tilesize*game.map.height, 50, 32, DISPLAYSURF)
        surf, tpos = ptext.draw("d", (buf + 60, game.map.tilesize*game.map.height + 10), sysfontname="arial", color=COLOR_WHITE, fontsize=FONTSIZE)
        buf = tpos[0] + surf.get_width() + 10
        d_roll = InputBox(buf, game.map.tilesize*game.map.height, 50, 32, DISPLAYSURF)
        ptext.draw("Max die: 100. Max sides: 120. Press ESC to exit this mode.", (buf + 60, game.map.tilesize*game.map.height + 10), sysfontname="arial", color=COLOR_WHITE, fontsize=FONTSIZE, width=game.map.width*game.map.tilesize*0.5)
        myrect = pygame.Rect(MAPOFFSET[0], game.map.tilesize*game.map.height + surf.get_height() + 10, game.map.width*game.map.tilesize, DISPLAYSURF.get_height()-(game.map.tilesize*game.map.height))

        RUNNING = True
        while RUNNING:    
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.leave_game()
                elif event.type == MOUSEBUTTONDOWN:
                    pass
                elif event.type == KEYDOWN:   
                    if event.key == K_ESCAPE:
                        self.clear_bottom_info()
                        return
                    elif event.key == K_RETURN:
                        if len(d_roll.text)>0:
                            pygame.draw.rect(DISPLAYSURF, COLOR_BLACK, myrect, 0)
                            d_string = number_of.text + "d" + d_roll.text
                            result = game.ruleset_copy.roll_dice(d_string)
                            if result is None:
                                result = "ERROR: IMPROPER ENTRY"
                            surf, tpos = ptext.draw(d_string +" = "+ str(result), (MAPOFFSET[0] + 10, game.map.tilesize*game.map.height + surf.get_height() + 10), sysfontname="arial", color=COLOR_WHITE, fontsize=FONTSIZE)
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

    def clear_bottom_info(self, x=None, y=None):
        # clear screen 
        if x is None or y is None:
            x = MAPOFFSET[0]
            y = game.map.tilesize*game.map.height
        myrect = pygame.Rect(x, y, game.map.width*game.map.tilesize, DISPLAYSURF.get_height()-y)
        pygame.draw.rect(DISPLAYSURF, COLOR_BLACK, myrect, 0)
        return

    def help_screen(self, status):
        self.clear_bottom_info()
        # blit hotkey information
        if status:
            info = "_GM HOTKEYS:_\n"
            hotkeys = GM_HOTKEYS
        else:
            info = "_PLAYER HOTKEYS:_\n"
            hotkeys = PLAYER_HOTKEYS
        
        for key, pair in hotkeys.items():
            info += key + ": " + pair["name"] + "\n"

        self.display_message(info)
        return

    def display_message(self, message, notation="_"):
        txt_surface, tpos = ptext.draw(message, (MAPOFFSET[0] + 10, game.map.tilesize*game.map.height + 10), sysfontname="arial", color=COLOR_WHITE, fontsize=FONTSIZE, width = game.map.width*game.map.tilesize, underlinetag=notation)
        return txt_surface, tpos

    def update_fog(self):
        for rw in range(game.map.height):
            for cl in range(game.map.width):
                if not game.map.fogOfWar[rw][cl]:
                    DISPLAYSURF.blit(FOG_IMAGE, GAMEVIEW.offset_blit(cl*game.map.tilesize, rw*game.map.tilesize))
        return

    def update_fog_GM(self):
        for rw in range(game.map.height):
            for cl in range(game.map.width):
                if not game.map.fogOfWar[rw][cl]:
                    self.draw_entity_box(rw, cl, (0,0,255))
        return

    def _images_string(self):
        self.load_pictures()
        display_string = ""
        for key in self.images:
            display_string += key + ", "
        return display_string

    def blit_texture(self, texture):
        texture_image = pygame.transform.scale(self.images[texture.name], (texture.width*game.map.tilesize,texture.height*game.map.tilesize))
        DISPLAYSURF.blit(texture_image, GAMEVIEW.offset_blit(texture.y*game.map.tilesize, texture.x*game.map.tilesize))
        return

    def blit_default(self, x, y):
        DISPLAYSURF.blit(DEFAULT_IMAGE, GAMEVIEW.offset_blit(y*game.map.tilesize, x*game.map.tilesize))
        return

# TODO FOR REVIEW TO ENSURE THAT CHAT WITH OTHER USERS CAN WORK + REUSE INPUT BOX FOR OTHER
# NEEDS
class InputBox:
    # https://stackoverflow.com/questions/46390231/how-to-create-a-text-input-box-with-pygame

    def __init__(self, x, y, w, h, screen, text='', client = None):
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = ptext.getsurf(self.text, sysfontname="arial", color=COLOR_WHITE, fontsize=FONTSIZE, width = w)
        self.height = self.txt_surface.get_height() + 5
        self.rect = pygame.Rect(x, y, w, self.height)
        self.active = False
        self.screen = screen
        self.client = client

    def handle_event(self, event, chatting=False):
        if event.type == MOUSEBUTTONDOWN:
            # If the user clicked on the chat_input_box rect.
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
                    if len(self.text) > 0:
                        if chatting:
                            my_message = self.client.user.get_username() + ": " + str(self.text)
                            game.append_transcript(my_message)
                            async_send(['chat', [client_id, my_message]])
                        self.text = ""
                        self.remove_old_block()
                elif event.key == K_BACKSPACE:
                    self.text = self.text[:-1]
                    tmp_surface = ptext.getsurf(self.text, sysfontname="arial", color=COLOR_WHITE, fontsize=FONTSIZE, width = self.rect.w)
                    if tmp_surface.get_height() < (self.rect.h-5):
                        self.remove_old_block()
                else:
                    self.text += event.unicode

        return

    def remove_old_block(self):
        self.rect.h += 5
        pygame.draw.rect(self.screen, COLOR_BLACK, self.rect, 0)
        self.rect.h = self.height

    def draw(self):
        # Blit the text.
        self.txt_surface, tpos = ptext.draw(self.text, (self.rect.x+5, self.rect.y+5), sysfontname="arial", color=COLOR_WHITE, fontsize=FONTSIZE, width = self.rect.w)
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
            # If the user clicked on the chat_input_box rect.
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
        self.txt_surface, tpos = ptext.draw(self.transcript_in_view, (self.rect.x+5, self.rect.y+5), sysfontname="arial", color=COLOR_WHITE, fontsize=FONTSIZE, width = self.rect.w)
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
        self.transcript_in_view += self.transcript.split("\n")[-2] + "\n"

    def adjust_transcript_view(self):
        tmp_surface = ptext.getsurf(self.transcript_in_view, sysfontname="arial", color=COLOR_WHITE, fontsize=FONTSIZE, width = self.rect.w)
        if len(self.transcript_in_view) < len(self.transcript):
        # if not down:
            while (tmp_surface.get_height() < self.rect.h):
                # add to top of string last part of whole transcript before it
                try:
                    beforehand = self.transcript.split(self.transcript_in_view,1)[0]
                    first_line = beforehand.split("\n")[-2]
                    self.transcript_in_view = first_line + "\n" + self.transcript_in_view 
                    tmp_surface = ptext.getsurf(self.transcript_in_view, sysfontname="arial", color=COLOR_WHITE, fontsize=FONTSIZE, width = self.rect.w)
                except Exception as e:
                    break
        while (tmp_surface.get_height() > self.rect.h):
            self.transcript_in_view = self.transcript_in_view.split("\n",1)[-1]
            tmp_surface = ptext.getsurf(self.transcript_in_view, sysfontname="arial", color=COLOR_WHITE, fontsize=FONTSIZE, width = self.rect.w)

# ------------------------------------------------------------------------------------------------------------
# GLOBAL VAR
game = Game()
GAMEVIEW = GameView()
pygame.init()
# GENERAL COLORS AND ITEMS
RESOLUTION_SCALING = 1600
if platform.system() == "Darwin":
    res = subprocess.check_output(["system_profiler","SPDisplaysDataType"])
    res_val = str(res).split("Resolution")[1].split("\\n")[0].split("x")[1].split()[0]
    res_val = int(res_val)
    if res_val < 800: 
        res_val = 800 #added for other computers being too small in res
    FONTSIZE = int(30*res_val/RESOLUTION_SCALING)
elif platform.system() == "Windows":
    FONTSIZE = int(30*pyautogui.size()[1]/RESOLUTION_SCALING)
FONTTYPE = pygame.font.SysFont('arial', FONTSIZE)
DISPLAYSIZE = (1300,750)
DISPLAYSURF = pygame.display.set_mode(DISPLAYSIZE)
OLDSURF = None
MAPOFFSET = (200,0)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
# COLOR_ACTIVE = pygame.Color('dodgerblue2')
COLOR_ACTIVE = COLOR_RED
GM_STATUS = True
GM_HOTKEYS = {"f": {"name": "Toggle FOG", "function": GAMEVIEW.toggle_fog},
              "t": {"name": "Add Texture", "function": GAMEVIEW.add_texture},
              "e": {"name": "Edit Entity", "function": GAMEVIEW.edit_entity},
              "c": {"name": "Create New Entity", "function": GAMEVIEW.create_new_entity},
              "a": {"name": "Add Asset", "function": GAMEVIEW.add_asset},
              "d": {"name": "Delete Entity", "function": GAMEVIEW.delete_entity},
              "p": {"name": "Remove Player", "function": GAMEVIEW.remove_player},
              "r": {"name": "Roll Dice", "function": GAMEVIEW.roll_dice}}
PLAYER_HOTKEYS = {"r": {"name": "Roll Dice", "function": GAMEVIEW.roll_dice}}
DEFAULT_IMAGE = pygame.transform.scale(GAMEVIEW.images["grey.png"], (50,50))
FOG_IMAGE = pygame.transform.scale(GAMEVIEW.images["fog.png"], (50,50))

# -----------------------------------------------------------------------------------------------------------------------

def main(clientObj, gameObj, clientID, gmOrPlayer = True, validatorObj = None):
    global game
    global GM_STATUS
    global client
    global client_id

    game = gameObj
    GM_STATUS = gmOrPlayer
    client = clientObj
    client_id = clientID

    GAMEVIEW.load_pictures_from_database()
    
    if validatorObj is not None:
        game.ruleset_copy = RuleEnactor()
        game.ruleset_copy.parse_validator(validatorObj)
        game.set_ruleset_copy(game.ruleset_copy)
        client.update_game(int(game.get_uniqueID()), jsonpickle.encode(game))

    # # START TO DISPLAY MAP
    DISPLAYSURF.fill(COLOR_BLACK)
    ptext.draw("Game Id: {}".format(game.uniqueID), (5, 0), sysfontname="arial", color=COLOR_WHITE, fontsize=FONTSIZE)
    ptext.draw("Game Name: {}".format(game.name), (5, 35), sysfontname="arial", color=COLOR_WHITE, fontsize=FONTSIZE, width = 200)

    GAMEVIEW.blit_entire_map()
    GAMEVIEW.help_screen(GM_STATUS)

    my_entity = None
    chat_input_box = InputBox(MAPOFFSET[0]+game.map.width*game.map.tilesize, DISPLAYSURF.get_height()-200, 200, 32, DISPLAYSURF, client = client)
    history = Transcript(MAPOFFSET[0]+game.map.width*game.map.tilesize, MAPOFFSET[1], 200, DISPLAYSURF.get_height()-(DISPLAYSURF.get_height()-chat_input_box.rect.y), DISPLAYSURF)
    # transcript = ""
    action_requested = ""

    global TYPES_OF_ENTITIES
    TYPES_OF_ENTITIES = []
    for entity_type in game.ruleset_copy.entity_types:
        TYPES_OF_ENTITIES.append(entity_type.get_type())
    global CONCRETE_TYPES_OF_ENTITIES
    CONCRETE_TYPES_OF_ENTITIES = []
    for entity_type in game.ruleset_copy.concrete_entity_types:
        CONCRETE_TYPES_OF_ENTITIES.append(entity_type.get_type())

    print(TYPES_OF_ENTITIES)
    print(CONCRETE_TYPES_OF_ENTITIES)

    RUNNING = True
    while RUNNING:   
        if GM_STATUS and my_entity is None:
            GAMEVIEW.update_fog_GM() 
        if shared_var.JOIN_REQUEST_FLAG:
            print("JOIN REQUEST FLAG")
            print(shared_var.MESSAGE_CONTENT)
            GAMEVIEW.join_request_popup()
            shared_var.JOIN_REQUEST_FLAG = False
        if shared_var.ACTION_REQUEST_FLAG:
            print("ACTION REQUEST FLAG")
            print(shared_var.MESSAGE_CONTENT)
            GAMEVIEW.action_request_popup()
            shared_var.ACTION_REQUEST_FLAG = False
        if shared_var.GM_LEAVES_FLAG:
            print("GM LEFT THE ROOM")
            GAMEVIEW.gm_leaves_room_popup()
            shared_var.GM_LEAVES_FLAG = False
            return
        if shared_var.ASSET_ADDED_FLAG:
            print("GM ADDED AN ASSEET")
            GAMEVIEW.load_pictures_from_database(shared_var.MESSAGE_CONTENT)
            shared_var.ASSET_ADDED_FLAG = False
        if shared_var.UPDATE_GAME_FLAG:
            print("GM UPDATED THE GAME, GETTING GAME")
            gameObj = client.get_game_from_room_number(game.get_uniqueID())
            game = jsonpickle.decode(gameObj[0][0])
            print(game.ruleset_copy.all_created_entities)
            shared_var.UPDATE_GAME_FLAG = False
            GAMEVIEW.blit_entire_map()
            pygame.display.flip()
        if shared_var.CHAT_FLAG:
            for chat in shared_var.CHAT_CONTENT:
                print("chat from CHAT_CONTENT: {}".format(chat))
                game.append_transcript(chat)
            shared_var.CHAT_CONTENT = []
            shared_var.CHAT_FLAG = False

        # start the loop that handles the events
        for event in pygame.event.get():
            if event.type == QUIT:
                GAMEVIEW.leave_game()
            elif event.type == MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                mousepos = (mousepos[0]-MAPOFFSET[0],mousepos[1]-MAPOFFSET[1])
                print(mousepos)
                if my_entity is not None and action_requested is not "Move":
                    GAMEVIEW.remove_previous_popup()
                    if mousepos[0] in range(location[0],location[0]+size[0]) and mousepos[1] in range(location[1],location[1]+size[1]):
                        rowsize = size[1]/(len(my_entity.get_actions())+1)
                        option_selected = math.floor((mousepos[1]-location[1])/rowsize)
                        if option_selected == 0:
                            action_requested = "Move"
                        else:
                            action_requested = my_entity.get_actions()[option_selected-1]
                            result = game.ruleset_copy.perform_action(action_requested, my_entity)
                            print(TYPES_OF_ENTITIES)
                            if result == "point" or result in TYPES_OF_ENTITIES:
                                item = GAMEVIEW.action_sequence(result)
                                result = game.ruleset_copy.perform_action_given_target(action_requested, my_entity, item)
                            game.append_transcript(result)
                            GAMEVIEW.help_screen(GM_STATUS)
                            my_entity = None
                            print(result)
                            if GM_STATUS:
                                GAMEVIEW.send_update_to_all()
                            else:
                                print("TODO SEND THIS ACTION AS A REQUEST TO THE GM TO APPROVE IF YOU ARE A PLAYER.")
                                # TODO APPEND TO TRANSCRIPT
                                client.update_game(game.get_uniqueID(), jsonpickle.encode(game))
                                async_send(["request_action", [client_id, game.get_uniqueID(), client.user.get_username(), result]])    
                        print(action_requested)
                    else:
                        my_entity = None
                elif my_entity is not None and action_requested is "Move":
                    # grab new location
                    x, y = GAMEVIEW.which_tile(mousepos)
                    # if it is a valid locatin and there are no other game.entities there
                    if x != -1 and y != -1 and GAMEVIEW.check_entity_fit(my_entity.size.get_width(), my_entity.size.get_height(), x, y, my_entity):
                        # remove old image and replace with generic block, then cover with texture if there are any       
                        for i in range(0,my_entity.size.get_width()):
                            for j in range(0,my_entity.size.get_height()):
                                if (my_entity.x+j, my_entity.y+i) in game.map.textures:
                                    GAMEVIEW.blit_texture(game.map.textures[(my_entity.x+j, my_entity.y+i)])
                                else:
                                    GAMEVIEW.blit_default((my_entity.x+j), (my_entity.y+i))
                        
                        result = client.user.get_username() + " moved " + my_entity.get_name() + " from " + str((my_entity.x, my_entity.y)) 
                        my_entity = game.ruleset_copy.move_entity(my_entity, (x,y))
                        result += " to " + str((my_entity.x, my_entity.y)) 
                        game.append_transcript(result)
                        # blit entity to it
                        my_entity_image = pygame.transform.scale(GAMEVIEW.images[my_entity.get_image_filename()], (my_entity.size.get_width()*game.map.tilesize,my_entity.size.get_height()*game.map.tilesize))
                        DISPLAYSURF.blit(my_entity_image, GAMEVIEW.offset_blit(my_entity.y*game.map.tilesize, my_entity.x*game.map.tilesize))
                        
                        if GM_STATUS:
                            GAMEVIEW.send_update_to_all()
                        else:
                            print("TODO SEND THIS ACTION AS A REQUEST TO THE GM TO APPROVE IF YOU ARE A PLAYER.")
                            # TODO APPEND TO TRANSCRIPT
                            client.update_game(game.get_uniqueID(), jsonpickle.encode(game))
                            async_send(["request_action", [client_id, game.get_uniqueID(), client.user.get_username(), result]]) 
                    # wipe signals
                    action_requested = ""
                    my_entity = None
                else:
                    x, y = GAMEVIEW.which_tile(mousepos)
                    if x in range(game.map.height) and y in range(game.map.width) and (GM_STATUS or (not GM_STATUS and game.map.fogOfWar[x][y])):
                        my_entity = GAMEVIEW.which_entity(x, y)
                        if my_entity is not None:
                            if (my_entity.y + my_entity.size.get_width()) >= game.map.width or (my_entity.x + my_entity.size.get_height()) >= game.map.height:
                                loc_x, loc_y = GAMEVIEW.tile_location((my_entity.x,my_entity.y))
                            else:    
                                loc_x, loc_y = GAMEVIEW.tile_location((my_entity.size.get_width()+my_entity.x,my_entity.size.get_height()+my_entity.y))
                            size, location = GAMEVIEW.make_popup(loc_x, loc_y, my_entity)

            elif event.type == KEYDOWN:   
                if event.key == K_ESCAPE:
                    GAMEVIEW.leave_game(False)
                    RUNNING = False
                elif GM_STATUS and event.unicode in GM_HOTKEYS and not chat_input_box.active:
                    if my_entity is not None:
                        # wipe what is currently on the screen before continuing
                        GAMEVIEW.remove_previous_popup()
                        my_entity = None
                        action_requested = ""
                        pygame.display.flip()
                    print(GM_HOTKEYS[event.unicode]["name"])
                    GM_HOTKEYS[event.unicode]["function"]()
                    GAMEVIEW.help_screen(GM_STATUS)
                    if GM_HOTKEYS[event.unicode]["name"] != "Add Asset":
                        GAMEVIEW.send_update_to_all()
                elif not GM_STATUS and event.unicode in PLAYER_HOTKEYS and not chat_input_box.active:
                    print(PLAYER_HOTKEYS[event.unicode]["name"])
                    PLAYER_HOTKEYS[event.unicode]["function"]()
                    GAMEVIEW.help_screen(GM_STATUS)
            # input box handling + transcript update
            chat_input_box.handle_event(event,True)
            history.handle_event(event)
            history.update(game.transcript)
            # transcript = chat_input_box.handle_event(event, transcript)

        # chat commands
        chat_input_box.wipe()
        history.wipe()
        chat_input_box.draw()
        history.draw()

        pygame.display.flip()


if __name__ == "__main__":
    client = Client()

    # Game Class
    new_game = Game()
    new_game.name = "Test Suite"
    new_game.uniqueID = 1
    new_game.map = Map(tilesize = 50, height = 10, width = 18)
    
    # create the map and add add textures to it
    new_game.map.textures[(3,3)] = Map.Texture(3,3,1,1,"grass.png")
    new_game.map.textures[(3,4)] = Map.Texture(3,4,1,1,"grass.png")
    
    #example fog
    new_game.map.fogOfWar[8][15] = False
    new_game.map.fogOfWar[8][16] = False
    new_game.map.fogOfWar[9][15] = False
    new_game.map.fogOfWar[9][16] = False

    ###### Rule Validation TEST START #######
    validator = _Validator()
    isTemplate = False
    hp_time = Attribute("HP", "10")    
    ac_time = Attribute("AC", 11)    
    template = Entity("", "entity", 1, 1, isTemplate, None)
    template.add_attribute(hp_time)
    template.add_attribute(ac_time)
            
    attack_rule = "target entity:\nroll = d20\nif roll > target.AC then reduce target.HP by 1d8\n"
    attack_action = Action("Attack", attack_rule)
    fireball_rule = "target point:\nif all entity within(3, 3) of target and d20 > entity.AC then reduce entity.HP by 6d6\n"
    fireball_action = Action("Fireball", fireball_rule)
    template.add_action(attack_action)
    template.add_action(fireball_action)
            
    validator.add_entity(template)
    game.ruleset_copy.parse_validator(validator)

    entity = game.ruleset_copy.add_new_entity("entity", "Andrew", 3, 7)
    entity.set_image_filename("default-image.png")
    ###### Rule Validation TEST END #######

    main(client, gameObj = new_game, gmOrPlayer = True, validatorObj = validator)
