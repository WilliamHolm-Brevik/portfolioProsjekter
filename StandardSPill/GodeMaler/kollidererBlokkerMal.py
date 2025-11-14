# Importerer pygame-biblioteket
import pygame as pg
import random as rd

# Importerer piltastene
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT)

# Initialisering av pygame
pg.init()
clock = pg.time.Clock()

# Lager en standard for bredden til alle objekter

font = pg.font.Font(None, 40)


# Lager farger
SVART = (0, 0, 70)
HVIT = (255, 255, 255)
GRONN = (0, 255, 0)
ROD = (255, 0, 0)

# Klasse for spillbrettet
class SpilleBrett:
    hoyde = 500
    bredde = 800
    objekter = []
    
    sluttSpillet = False
    poeng = 0
    
    # Lager vinduet
    vindu = pg.display.set_mode([bredde, hoyde])
    font = pg.font.SysFont("Tahoma", 18)
    
    def leggTilObjekter(self, objekt):
        self.objekter.append(objekt)
        
    def fjernObjekt(self, objekt):
        self.objekter.remove(objekt)

# Klasse for spillobjektet
class SpillObjekt:
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde):
        self.xPosisjon = xPosisjon
        self.yPosisjon = yPosisjon
        self.farge = farge
        self.hoyde = hoyde
        self.bredde = bredde
        self.rektangel = pg.Rect(self.xPosisjon, self.yPosisjon, self.bredde, self.hoyde)
        self.brett = spillebrett
    
    def plassering(self):
        pg.draw.rect(vindu, self.farge, self.rektangel)
        
    def oppdaterRektangel(self):
        self.rektangel.topleft = (self.xPosisjon, self.yPosisjon)
    
    def sjekkKollisjon(self, objekt):
        return self.rektangel.colliderect(objekt.rektangel)

# Lager en klasse for spilleren
class Spiller(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde, fart, poeng, retning):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)
        self.fart = fart
        self.poeng = poeng
        self.fartRetning = retning
        
    def flytt(self, brett):
        original_x = self.xPosisjon
        original_y = self.yPosisjon

        if self.fartRetning == (1, 0) and self.xPosisjon < brett.bredde - self.bredde:
            self.xPosisjon += self.fart
        elif self.fartRetning == (-1, 0) and self.xPosisjon > 0:
            self.xPosisjon -= self.fart
        elif self.fartRetning == (0, -1) and self.yPosisjon > 0:
            self.yPosisjon -= self.fart
        elif self.fartRetning == (0, 1) and self.yPosisjon < brett.hoyde - self.hoyde:
            self.yPosisjon += self.fart

        self.oppdaterRektangel()

        for objekt in brett.objekter:
            if objekt is not self and self.sjekkKollisjon(objekt):
                self.xPosisjon = original_x
                self.yPosisjon = original_y
                self.oppdaterRektangel()
                break

class AnnetObjekt(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde, gjennom):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)
        self.gjennom = gjennom
        
class Baller(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde, gjennom):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)
        self.gjennom = gjennom
        
        self.dx = rd.randint(1, 10) / 10
        self.dy = rd.randint(1, 10) / 10
    
    def flytt(self, brett):
        original_x = self.xPosisjon
        original_y = self.yPosisjon

        self.xPosisjon += self.dx
        self.yPosisjon += self.dy

        if self.xPosisjon < 0 or self.xPosisjon > brett.bredde - self.bredde:
            self.dx = -self.dx
        if self.yPosisjon < 0 or self.yPosisjon > brett.hoyde - self.hoyde:
            self.dy = -self.dy

        self.oppdaterRektangel()
        self.kollisjoner(brett, original_x, original_y)

    def kollisjoner(self, brett, original_x, original_y):
        for objekt in brett.objekter:
            if objekt is not self and self.sjekkKollisjon(objekt):
                # Calculate the overlap between the two rectangles
                dx = self.xPosisjon - objekt.xPosisjon
                dy = self.yPosisjon - objekt.yPosisjon

                if abs(dx) > abs(dy):
                    # Horizontal collision
                    if dx < 0:
                        self.xPosisjon = objekt.xPosisjon - self.bredde
                    else:
                        self.xPosisjon = objekt.xPosisjon + objekt.bredde
                    self.dx *= -1
                else:
                    # Vertical collision
                    if dy < 0:
                        self.yPosisjon = objekt.yPosisjon - self.hoyde
                    else:
                        self.yPosisjon = objekt.yPosisjon + objekt.hoyde
                    self.dy *= -1

                self.oppdaterRektangel()


brett = SpilleBrett()
vindu = pg.display.set_mode((brett.bredde, brett.hoyde))
pg.display.set_caption("Pygame vindu")

storrelse = 0
fargen = GRONN
def sluttSpill():
    spiller.fart = 0
    pg.draw.rect(vindu, GRONN, (0, 0, 10*storrelse, 10*storrelse))
    pg.draw.rect(vindu, SVART, (0, 0, 10, brett.hoyde))
    pg.draw.rect(vindu, SVART, (0, 0, brett.bredde, 10))
    pg.draw.rect(vindu, SVART, (brett.bredde-10, 0, brett.bredde, brett.hoyde))
    pg.draw.rect(vindu, SVART, (0, brett.hoyde-10, brett.bredde, brett.hoyde))
    tekst = font.render("Da er spillet over!", True, fargen)
    vindu.blit(tekst, (brett.bredde/2-120, 200))

spiller = Spiller(brett.bredde/2, brett.hoyde/2, GRONN, brett, 20, 20, 3, 10, (1, 0))
annet_objekt = AnnetObjekt(100, 100, ROD, brett, 20, 20, True)
ball = Baller(150, 150, ROD, brett, 20, 20, False)
ball2 = Baller(200, 200, ROD, brett, 20, 20, False)

brett.leggTilObjekter(spiller)
brett.leggTilObjekter(annet_objekt)
brett.leggTilObjekter(ball)
brett.leggTilObjekter(ball2)

fortsett = True
while fortsett:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            fortsett = False
    
    brett.vindu.fill(HVIT)

    for objekt in brett.objekter:
        objekt.plassering()
    
    taster = pg.key.get_pressed()
    if taster[K_UP]:
        spiller.fartRetning = (0, -1)
    elif taster[K_DOWN]:
        spiller.fartRetning = (0, 1)
    elif taster[K_LEFT]:
        spiller.fartRetning = (-1, 0)
    elif taster[K_RIGHT]:
        spiller.fartRetning = (1, 0) 
    
    spiller.flytt(brett)
    
    ball.flytt(brett)
    ball2.flytt(brett)
    
    tekst = font.render("Dine poeng er: " + str(brett.poeng), True, (0, 0, 0))
    vindu.blit(tekst, (brett.bredde/2 - brett.bredde/4, 60))     

    if brett.sluttSpillet:
        sluttSpill()
        storrelse += 10
        fargen = (rd.randint(0, 255), rd.randint(0, 255), rd.randint(0, 255))
    
    pg.display.flip()
    
    clock.tick(60)

pg.quit()
