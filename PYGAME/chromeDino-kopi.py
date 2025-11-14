import pygame as pg
import random as rn

pg.init()

# Initialiserer/starter pygame
VINDULENGDE = 1000
VINDUHOYDE = 500

slutt = False


breddeObjekter = 20

poeng = 0
font = pg.font.Font(None, 50)

vindu = pg.display.set_mode((VINDULENGDE, VINDUHOYDE))
pg.display.set_caption("Google dinosaur")

# Lager farger
SVART = (0, 0, 70)
HVIT = (255, 255, 255)
GRONN = (0, 255, 0)
ROD = (255, 0, 0)
BLÅ = (0, 0, 255)


class Dinos:
    def __init__(self, xPosisjon, yPosisjon, fart, farge):
        self.yPosisjon = yPosisjon
        self.xPosisjon = xPosisjon
        self.fart = fart
        self.farge = farge
        self.hopper = False

    def hopp(self):
        if not self.hopper:
            self.hopper = True
            self.fart = 10 

    def plassering(self):
        if self.hopper:
            self.yPosisjon -= self.fart 
            self.fart -= 0.5 


            if self.yPosisjon >= 300:
                self.yPosisjon = 300  
                self.hopper = False 

        pg.draw.rect(vindu, self.farge, (self.xPosisjon, self.yPosisjon, breddeObjekter, breddeObjekter))

class Kaktus:
    def __init__(self, xPosisjon, yPosisjon, farge, bredde, hoyde, fart):
        self.xPosisjon = xPosisjon
        self.yPosisjon = yPosisjon
        self.farge = farge
        self.bredde = bredde
        self.hoyde = hoyde
        self.fart = fart
        
    def plassering(self):
        self.xPosisjon -= self.fart
        pg.draw.rect(vindu, self.farge, (self.xPosisjon, self.yPosisjon, self.bredde, self.hoyde))
        
    def kollisjon(self, dino):
        global slutt
        if abs(dino.xPosisjon - self.xPosisjon) <= breddeObjekter and abs(dino.yPosisjon - self.yPosisjon) <= self.hoyde:
            slutt = True

kaktusene = []

for i in range(1000):
    hoyden = rn.randint(20, 60)
    kaktusene.append(Kaktus(1000*i, 300 - hoyden + breddeObjekter, GRONN,  breddeObjekter, hoyden, 10))


dino = Dinos(300, 300, 0, BLÅ)

# Gjenta helt til brukeren lukker vinduet
fortsett = True
while fortsett:

    # Sjekker om brukeren har lukket vinduet
    for event in pg.event.get():
        if event.type == pg.QUIT:
            fortsett = False

    # Farger bakgrunnen lyseblå
    vindu.fill((135, 206, 235))

    pg.draw.rect(vindu, SVART, (0, 320, VINDULENGDE, VINDUHOYDE))

    keys = pg.key.get_pressed()
    if keys[pg.K_SPACE]:
        dino.hopp()
        
    for kaktus in kaktusene:
        kaktus.plassering()
        kaktus.kollisjon(dino)
        if slutt:
            kaktus.fart = 0
            dino.fart = 0
            tekst = font.render("Da var det over!", True, (0, 0, 0))
            vindu.blit(tekst, (VINDULENGDE/2-50, 200))
    
    if kaktusene[0].xPosisjon % 1000 == 0:
        poeng += 1
        
    poeng_tekst = font.render(f'{poeng}', True, (0, 0, 0))
    vindu.blit(poeng_tekst, (VINDULENGDE/2-50, 10))

    dino.plassering()
    pg.display.flip()

    pg.time.Clock().tick(60)

# Avslutter pygam
pg.quit()
