import json
import math
import pygame

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
class Tilemap:
    def __init__(self, game, tile_size = 16,iteration = 1):
        self.game = game
        self.tile_size = tile_size

        self.tile_map_arr = []
        self.tile_map_dict={}
        self.name = ""
        self.iteration = iteration
        self.startPOS = []
        self.backPOS = []
    def tiles_around(self, pos, player_size):
        tiles = []

        #added the + player_size to start from the middle of the player and not from the top left
        player_loc = ((int(pos[0]) + player_size[0]//2) // self.tile_size , (int(pos[1]) + player_size[1]//2) // self.tile_size) #give pos of place in terms of tiles position

        for offset in NEIGHBOR_OFFSETS:
            checkX = player_loc[0] + offset[0]
            checkY = player_loc[1] + offset[1]
            if (f'{checkY};{checkX}') in self.tile_map_dict and self.tile_map_dict[f'{checkY};{checkX}']['type'] == 1:
                tiles.append((checkX,checkY))

        return tiles


    def rect_around(self, pos, player_size, scale):
        rects = []
        if scale == 1:
            around = self.tiles_around(pos,player_size)
        else:
            around = self.spike_around(pos, player_size)
        for tile in around:
            if scale == 1:
                rects.append(pygame.Rect(tile[0] * self.tile_size, tile[1] * self.tile_size, self.tile_size, self.tile_size * scale))
            else:
                rects.append(pygame.Rect(tile[0] * self.tile_size, tile[1] * self.tile_size + self.tile_size*scale, self.tile_size, self.tile_size * scale))
        return rects
    def spike_around(self, pos, player_size):
        spikes = []

        #added the + player_size to start from the middle of the player and not from the top left
        player_loc = ((int(pos[0]) + player_size[0]//2) // self.tile_size , (int(pos[1]) + player_size[1]//2) // self.tile_size) #give pos of place in terms of tiles position

        for offset in NEIGHBOR_OFFSETS:
            checkX = player_loc[0] + offset[0]
            checkY = player_loc[1] + offset[1]
            if (f'{checkY};{checkX}') in self.tile_map_dict and self.tile_map_dict[f'{checkY};{checkX}']['type'] == 6:
                spikes.append((checkX,checkY))

        return spikes
    def check_door(self, pos, player_size):
        player_loc = ((int(pos[0]) + player_size[0] // 2) // self.tile_size, (int(pos[1]) + player_size[1] // 2) // self.tile_size)
        checkX = player_loc[0]
        checkY = player_loc[1]

        if (f'{checkY};{checkX}') in self.tile_map_dict and self.tile_map_dict[f'{checkY};{checkX}']['type'] == 2:
            return True
        else:
            return False
    def check_backdoor(self, pos, player_size):
        player_loc = ((int(pos[0]) + player_size[0] // 2) // self.tile_size, (int(pos[1]) + player_size[1] // 2) // self.tile_size)
        checkX = player_loc[0]
        checkY = player_loc[1]

        if (f'{checkY};{checkX}') in self.tile_map_dict and self.tile_map_dict[f'{checkY};{checkX}']['type'] == 5:
            return True
        else:
            return False
    def check_exit(self, pos, player_size):
        player_loc = ((int(pos[0]) + player_size[0] // 2) // self.tile_size, (int(pos[1]) + player_size[1] // 2) // self.tile_size)
        checkX = player_loc[0]
        checkY = player_loc[1]

        if (f'{checkY};{checkX}') in self.tile_map_dict and self.tile_map_dict[f'{checkY};{checkX}']['type'] == 4:
            return True
        else:
            return False
    def clear(self):
        self.tile_map_arr = []
        self.tile_map_dict = {}
        self.startPOS = []
        self.backPOS = []
    def restart(self,foward):
        if(foward):
            self.iteration += 1
        else:
            self.iteration -= 1
        self.clear()
        self.load()
        self.load_toDict()
    def restart_final(self):
        self.iteration = -1
        self.clear()
        self.load()
        self.load_toDict()
    def load(self):
        f = open(f'map{self.iteration}.txt', 'r')
        lines = f.readlines()
        for i , line in enumerate(lines):
            row = []

            for j in range(len(line)):
                row.append(line[j])
            self.tile_map_arr.append(row)
        f.close()

    def load_toDict(self):
        for i , line in enumerate(self.tile_map_arr):

            for j in range(len(line)):
                if line[j] == '1':
                    name = str(f'{i};{j}')
                    self.tile_map_dict[name] = {'type':1,'pos':[i,j]}
                elif line[j] == '2':
                    name = str(f'{i};{j}')
                    self.tile_map_dict[name] = {'type':2,'pos':[i,j]}
                    self.backPOS.append(j * self.tile_size)
                    self.backPOS.append(i * self.tile_size)
                elif line[j] == '3':
                    self.startPOS.append(j * self.tile_size)
                    self.startPOS.append(i * self.tile_size)
                elif line[j] == '4':
                    name = str(f'{i};{j}')
                    self.tile_map_dict[name] = {'type': 4, 'pos': [i, j]}
                elif line[j] == '5':
                    name = str(f'{i};{j}')
                    self.tile_map_dict[name] = {'type':5,'pos':[i,j]}
                elif line[j] == '6':
                    name = str(f'{i};{j}')
                    self.tile_map_dict[name] = {'type':6,'pos':[i,j]}


    def render(self, display, offset):
        # for x in self.tile_map:
        #     display.blit(self.game.assets['tile'],(self.tile_map[x]['pos'][0] * self.tile_size , self.tile_map[x]['pos'][1] * self.tile_size))
        #
        #

        # for i , line in enumerate(self.tile_map_arr): FOR ANGEL
        #
        #     for j in range(len(line)):
        #         if line[j] == '1':
        #             display.blit(self.game.assets['tile'],(j * self.tile_size -offset[0], i * self.tile_size - offset[1]))

        for x in range(offset[0] // self.tile_size, (offset[0] + display.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + display.get_height()) // self.tile_size + 1):
                loc = str(y) + ';' + str(x)

                if loc in self.tile_map_dict:

                    tile = self.tile_map_dict[loc]
                    if tile['type'] == 1: #draw tiles
                        display.blit(self.game.assets['tile'], (tile['pos'][1] * self.tile_size - offset[0], tile['pos'][0] * self.tile_size - offset[1]))
                    elif tile['type'] == 2: #draw the door rectangle
                        display.blit(self.game.assets['door'], (tile['pos'][1] * self.tile_size - offset[0], tile['pos'][0] * self.tile_size - offset[1]))
                    elif tile['type'] == 4: #draw the exit rectangle
                        display.blit(self.game.assets['exit'], (tile['pos'][1] * self.tile_size - offset[0], tile['pos'][0] * self.tile_size - offset[1]))
                    elif tile['type'] == 5:  # draw the exit rectangle
                        display.blit(pygame.transform.flip(self.game.assets['door'],True,False), (tile['pos'][1] * self.tile_size - offset[0], tile['pos'][0] * self.tile_size - offset[1]))
                    if tile['type'] == 6: #draw spike
                        display.blit(self.game.assets['spike'], (tile['pos'][1] * self.tile_size - offset[0], tile['pos'][0] * self.tile_size - offset[1] + 8))
