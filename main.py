import pygame
import sys
import os
from tilemap import Tilemap
from entity import PhysicsEntity, Animation
from utility import *
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480


class Game():

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.display = pygame.Surface((SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
        self.screen.fill((255,255,255))
        self.clock = pygame.time.Clock()
        self.assets = {  # stores the image assets

            'player': load_image('Assets/bomb.png'),
            'tile': pygame.image.load('Assets/tiles/0.png'),
            'door': pygame.image.load('Assets/tiles/2.png'),
            'exit': pygame.image.load('Assets/tiles/1.png'),
            'player_animation': Animation(load_images('Assets/animation')),
            'spike': pygame.image.load('Assets/tiles/spike.png')

        }


        self.tilemap = Tilemap(self , 16, 1)
        self.tilemap.load()
        self.tilemap.load_toDict()
        self.player = PhysicsEntity(self,self.tilemap.startPOS, self.assets['player'].get_size())
        self.movement = [False,False]
        self.jet = False

        self.offset=[0,0]
        self.player_size = self.assets['player'].get_size()
        self.door = False
        self.exit = False
    def run(self):

        self.tilemap.iteration = 0
        self.tilemap.restart(True)
        self.offset = [0, 0]
        self.player.pos = self.tilemap.startPOS.copy()
        self.player.velocity = [0, 0]
        running = True
        while running:
            self.offset[0] += (self.player.pos[0]  - (SCREEN_WIDTH/4) -self.offset[0])/ 30
            self.offset[1] += (self.player.pos[1] - (SCREEN_HEIGHT / 4) - self.offset[1]) / 30
            render_scroll = (int(self.offset[0]) , int(self.offset[1]))

            self.display.fill((0,0,0))

            self.tilemap.render(self.display, render_scroll)

            self.player.update((self.movement[1] - self.movement[0],0), self.tilemap)
            self.player.render(self.display, render_scroll,self.tilemap)

            if self.player.dead:
                self.player.pos = self.tilemap.startPOS.copy()

                self.player.velocity = [0, 0]

            self.door = self.tilemap.check_door(self.player.pos, self.player.size)
            self.exit = self.tilemap.check_exit(self.player.pos, self.player.size)
            self.backdoor = self.tilemap.check_backdoor(self.player.pos, self.player.size)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True

                    if event.key == pygame.K_UP:
                        if self.door:
                            self.tilemap.restart(True)
                            self.offset = [0,0]
                            self.player.pos = self.tilemap.startPOS.copy()
                        elif self.exit:
                            self.tilemap.restart_final()
                            self.offset = [0, 0]
                            self.player.pos = self.tilemap.startPOS.copy()
                        elif self.backdoor:
                            self.tilemap.restart(False)
                            self.offset = [0, 0]
                            self.player.pos = self.tilemap.backPOS.copy()
                        elif self.player.curr_jumps  < self.player.max_jumps:
                            self.player.curr_jumps += 1
                            self.player.velocity[1] = -3
                    if event.key == pygame.K_r:
                        self.player.pos = self.tilemap.startPOS.copy()
                    if event.key == pygame.K_SPACE:
                        if self.player.dash:
                            if self.movement[1]:
                                self.player.velocity[0] = 3
                            if self.movement[0]:
                                self.player.velocity[0] = -3
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()),(0,0))
            #self.screen.blit(self.display, (0, 0))

            pygame.display.update()
            self.clock.tick(60)

    def menu(self):
        font = pygame.font.SysFont(None, 20)
        menu_assets={
            'play' : load_image('Assets/Menu/play.png'),
            'anim' : load_image('Assets/Menu/anim.png'),
            'title' : load_image('Assets/Menu/title.png')
        }
        play_button = button('Assets/Menu/play.png',(15,50) , 2)
        anim_button = button('Assets/Menu/anim.png', (play_button.pos[0], play_button.pos[1] + 50) , 2)
        title_button = button('Assets/Menu/title.png', (15, 20),2)
        click = False
        while True:

            self.display.fill((0,0,0))
            #draw_text('main menu', font,(255,255,255), self.display, 20, 20);

            mx, my = pygame.mouse.get_pos()
            mx /= 2
            my /= 2


            #button_1 = pygame.Rect(50, 100, 200, 50)
            #button_2 = pygame.Rect(50, 200, 200, 50)

            self.display.blit(title_button.img, title_button.pos)
            self.display.blit(play_button.img,play_button.pos)
            self.display.blit(anim_button.img, anim_button.pos)
            pygame.draw.rect(self.display,(255,0,0),play_button.rect, 1)
            pygame.draw.rect(self.display, (255, 255, 0), anim_button.rect, 1)

            if play_button.rect.collidepoint((mx,my)):
                if click:
                    self.run()
            if anim_button.rect.collidepoint((mx,my)):
                if click:
                    self.run2()
            #pygame.draw.rect(self.screen, (255,0,0), button_1)
            #pygame.draw.rect(self.screen, (255,0,0), button_2)
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True;
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

    def run2(self):
        running = True
        while running:



            self.display.fill((0, 0, 0))

            self.display.blit(self.assets['player_animation'].img(),(100,100))

            self.assets['player_animation'].update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


Game().menu()