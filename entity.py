import pygame



class PhysicsEntity:
    def __init__(self,game,pos,size):
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.velocity = [0,0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.rects=[]
        self.max_jumps = 2
        self.curr_jumps = 0
        self.airtime = False

        self.my_font = pygame.font.SysFont("monospace", 10)
        self.flip = False
        self.dash = False
        self.dead = False
    def rect(self):
        return pygame.Rect(self.pos[0],self.pos[1], self.size[0] ,self.size[1])

    def update(self, movement, tilemap):
        self.dash = False
        self.dead = False
        frame_movement = (movement[0] + self.velocity[0] , movement[1] + self.velocity[1])

        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.pos[0] += frame_movement[0]
        self.rects = tilemap.rect_around(self.pos, self.size, 1)
        self.spikes = tilemap.rect_around(self.pos, self.size,.5)
        player_rect = self.rect()
        for rect in self.rects:

            if player_rect.colliderect(rect):

                if frame_movement[0] > 0:
                    player_rect.right = rect.left
                if frame_movement[0] < 0:
                    player_rect.left = rect.right
            self.pos[0] = player_rect.x



        self.pos[1] += frame_movement[1]
        player_rect = self.rect()
        for rect in self.rects:

            if player_rect.colliderect(rect):

                if frame_movement[1] > 0:
                    player_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    player_rect.top = rect.bottom
                    self.collisions['up'] = True
            self.pos[1] = player_rect.y

        for spike in self.spikes:
            if player_rect.colliderect(spike):
                self.dead = True
        if self.pos[1] > 350:
            self.dead = True
        #self.velocity[1] += .1

        self.velocity[1] = min(5, self.velocity[1] + 0.1)
        if self.velocity[0] > 0:
            self.velocity[0] = max(0, self.velocity[0] - 0.1)

        if self.velocity[0] < 0:
            self.velocity[0] = min(0, self.velocity[0] + 0.1)

        if self.velocity[0] > -1 and self.velocity[0] < 1: #limit dash
            self.dash = True

        if(movement[0] > 0):
            self.flip = False
        elif (movement[0] < 0):
            self.flip = True


        if self.collisions['up'] or self.collisions['down']:
            self.velocity[1] = 0

        if not self.collisions['down']:
            self.airtime = True
        if self.collisions['down']:
            self.curr_jumps = 0
            self.airtime = False


        # if self.curr_jumps == 0 and not self.collisions['down']:
        #     self.curr_jumps = 1



    def render(self,screen, offset,tilemap):
        screen.blit(pygame.transform.flip(self.game.assets['player'],self.flip,False), (self.pos[0] - offset[0], self.pos[1] - offset[1]))  # Temp
        player = self.rect()
        #pygame.draw.rect(screen,(255,255,0),(player.x - offset[0], player.y - offset[1],player.width,player.height),1)


        for rect in self.rects:
            rect.x -= offset[0]
            rect.y -= offset[1]
            pygame.draw.rect(screen, (255, 0, 0), rect, 1)
        for spike in self.spikes:
            spike.x -= offset[0]
            spike.y -= offset[1]
            pygame.draw.rect(screen, (255, 255, 0), spike, 1)

        label = self.my_font.render(f"{self.pos[0]} {round(self.pos[1])}", 1, (255, 255, 0))
        screen.blit(label, (0,0))
        if tilemap.iteration == -1:
            message = self.my_font.render(f"Congratulations", 5, (255, 0, 0))
            screen.blit(message,(self.pos[0] - offset[0] - 20, self.pos[1] - offset[1] - 20))

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]