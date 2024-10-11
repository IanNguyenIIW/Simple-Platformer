import os
import pygame


def load_image(path):
    img = pygame.image.load(path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(path)):
        images.append(load_image(path + '/' + img_name))
    return images

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)


class button:
    def __init__(self,path,pos,scale):
        self.scale = scale
        self.img = load_image(path)
        self.size = self.img.get_size()
        self.img = pygame.transform.scale(self.img,(self.size[0]*scale,self.size[1]*scale))

        self.pos = pos
        self.rect = self.get_rect()

    def get_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0] * self.scale, self.size[1] * self.scale)