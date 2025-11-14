import pygame as pg
import random as rn

pg.init()

# Initialiserer/starter pygame
VINDULENGDE = 1900
VINDUHOYDE = 1000

slutt = False


breddeObjekter = 20

poeng = 0
font = pg.font.Font(None, 50)

vindu = pg.display.set_mode((VINDULENGDE, VINDUHOYDE))
pg.display.set_caption("Flappy bird")

# Lager farger
SVART = (0, 0, 0)
HVIT = (255, 255, 255)
GRONN = (0, 255, 0)
RØD = (255, 0, 0)
BLÅ = (0, 0, 255)

class Fugl:
    def __init__(self, xPosisjon, yPosisjon, radius, fart):
        self.xPosisjon = xPosisjon
        self.yPosisjon = yPosisjon
        self.radius = radius
        self.hopper = False
        self.fart = fart
    
    def hopp(self):
        self.fart = 7

    def plassering(self):
        self.yPosisjon -= self.fart 
        self.fart -= 0.3
                
        pg.draw.circle(vindu, RØD, (self.xPosisjon, self.yPosisjon), self.radius)
        
    
class Rør:
    def __init__(self, xPosisjon: int, yPosisjon: int, farge, åpning, fart: int):
        self.xPosisjon = xPosisjon
        self.yPosisjon = yPosisjon
        self.åpning = åpning
        self.farge = farge
        self.fart = fart
 
    def plassering(self):
        bredden = 100
        åpningstørrelse = 150
        self.xPosisjon -= self.fart
        pg.draw.rect(vindu, self.farge, (self.xPosisjon, self.yPosisjon - VINDUHOYDE + self.åpning, bredden, VINDUHOYDE))
        pg.draw.rect(vindu, self.farge, (self.xPosisjon, self.yPosisjon + self.åpning + åpningstørrelse, bredden, VINDUHOYDE))
        
    def kollisjonFugl(self, fugl):  
        bredden = 100
        # Kollisjon med venstre side av rektangel
        if(self.xPosisjon + VINDUHOYDE >= fugl.xPosisjon and self.yPosisjon > fugl.yPosisjon and self.yPosisjon < fugl.yPosisjon + bredden/2):
            return True
        
        # Kollisjon med toppen av rektangelet
        if(self.yPosisjon + VINDUHOYDE >= fugl.yPosisjon and self.xPosisjon > fugl.xPosisjon and self.xPosisjon < fugl.xPosisjon + bredden/2):
            return True
   
røra = []
     
for i in range(1000):
    røra.append(Rør(500*i, 0, GRONN, rn.randint(50, 350), 3))     


fuglen = Fugl(100, VINDUHOYDE/2, 20, 0)

# Gjenta helt til brukeren lukker vinduet
fortsett = True
while fortsett:

    # Sjekker om brukeren har lukket vinduet
    for event in pg.event.get():
        if event.type == pg.QUIT:
            fortsett = False

    # Farger bakgrunnen lyseblå
    vindu.fill((135, 206, 235))
    
    
    keys = pg.key.get_pressed()
    if keys[pg.K_SPACE]:
        fuglen.hopp()
    
    for rør in røra:
        rør.plassering()
        if rør.kollisjonFugl(fuglen):
            slutt = True
    
    if slutt:
        for rør in røra:
            rør.fart = 0
            fuglen.fart = 0
    
    fuglen.plassering()
    
    pg.display.flip()

    pg.time.Clock().tick(60)

# Avslutter pygame
pg.quit()
