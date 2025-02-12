import pygame
from sys import exit
from random import randint
import pkg_resources
 
WIDTH = 288
HEIGHT = 512
FPS = 60

def path(semi_path):
    return pkg_resources.resource_filename(__name__, semi_path)

class Flappy(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__() 

        flappy = pygame.image.load(path("immagini\\uccello.png")).convert()
        self.image = flappy
        self.rect = self.image.get_rect(center = (40, 200))
        self.gravità = 0
        self.salto = 0

    def input(self):
        
        keys = pygame.key.get_pressed()  
        if keys[pygame.K_SPACE] and pygame.time.get_ticks() - self.salto > 200: 
            self.gravità = -10 
            self.salto = pygame.time.get_ticks()

    def gravità_uccello(self):
        self.gravità += 0.8
        self.rect.y += self.gravità

    def collisione(self):
        if self.rect.bottom >= 400 or self.rect.top <= 0:
            return True
        
        return False

    def update(self):

        self.input()
        self.gravità_uccello()
        
        if self.collisione():
            return True
        
        return False

class Tubi1(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        super().__init__()
    
        tubo = pygame.image.load(path("immagini\\tubo.png")).convert()

        self.image = tubo
        self.rect = self.image.get_rect(midtop  = (x, y))
             
    def elimina_tubi(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.rect.x -= 5
        self.elimina_tubi()

class Tubi2(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        super().__init__()
    
        tubo1 = pygame.image.load(path("immagini\\tubo.png")).convert()
        tubo2 = pygame.transform.flip(tubo1, False, True)

        self.image = tubo2
        self.rect = self.image.get_rect(midbottom  = (x, (y - 100)))


    def elimina_tubi(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.rect.x -= 5
        self.elimina_tubi()


def punti():

    tempo = pygame.time.get_ticks() - timer_inizio 
    tempo = int(tempo / 1000)            
    punteggio = font.render(f"{tempo}", False, "Black")              
    rettangolo_punteggio = punteggio.get_rect(center = (WIDTH / 2, 50))       
    schermo.blit(punteggio, rettangolo_punteggio)
    
    return tempo

def morte():

    if pygame.sprite.spritecollide(giocatore.sprite, ostacoli_group, False, pygame.sprite.collide_mask) or giocatore.sprite.collisione():
        ostacoli_group.empty()     
        return True
    
    return False
    

pygame.init()

schermo = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy bird")

clock = pygame.time.Clock()

ground = pygame.image.load(path("immagini\\base.png")).convert()
cielo = pygame.image.load(path("immagini\\sfondo.png")).convert()

font = pygame.font.SysFont("Comic Sans", 30)
titolo = font.render("Press Space", False, "black")

game_over = pygame.image.load(path("immagini\\gameover.png")).convert_alpha()
rect_g = game_over.get_rect(center = ((WIDTH / 2), (HEIGHT / 2)))


giocatore = pygame.sprite.GroupSingle()  
giocatore.add(Flappy())                
ostacoli_group = pygame.sprite.Group()

punteggio_fine = 0
timer_inizio = 0
movimento_ground = 0
running = True

timer_tubi = pygame.USEREVENT + 1
pygame.time.set_timer(timer_tubi, 1000)

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not running:
            running = True
            giocatore = pygame.sprite.GroupSingle()
            giocatore.add(Flappy())
            ostacoli_group = pygame.sprite.Group()
            timer_inizio = pygame.time.get_ticks()

        if event.type == timer_tubi and running:

            x = randint(300, 320)
            y = randint(192, 380)
            ostacoli_group.add(Tubi1(x, y), Tubi2(x, y))

    if running:

        schermo.blit(cielo, (0, 0))
        schermo.blit(ground, (movimento_ground, 400))
        movimento_ground -= 5

        if movimento_ground <= -46:
            movimento_ground = 0
        
        punteggio_fine = punti()

        if giocatore.sprite.update():
            running = False

        giocatore.draw(schermo)

        ostacoli_group.update()
        ostacoli_group.draw(schermo)

        if morte():
            running = False

    else:
        schermo.blit(game_over, rect_g)

    pygame.display.update()
    clock.tick(FPS)
