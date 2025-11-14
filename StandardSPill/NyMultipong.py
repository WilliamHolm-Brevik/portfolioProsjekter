"""

I denne koden har jeg brukt collideRect() funksjon for å se om objektene kolliderer med hverandre. Det er mulig at jeg kunne ha brukt andre former for å detektere, men dette er den mest fleksible og enkleste måten å se om objektene kolliderer.

"""



# Importerer pygame-biblioteket
import pygame as pg
import random as rd
import math as m

# Importerer piltastene
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT)

# Initialisering av pygame
pg.init()
clock = pg.time.Clock()

# Lager en standard for bredden til alle objekter

font = pg.font.Font(None, 30)

# Lager farger
SVART = (0, 0, 70)
GRAA = (70, 70, 70)
HVIT = (255, 255, 255)
GRONN = (0, 255, 0)
ROD = (255, 0, 0)
BLAA = (0, 0, 255)


"""
  Tegne rektangel
        pg.draw.rect(vindu, self.farge, (self.xPosisjon, self.yPosisjon, breddeObjekter, breddeObjekter))
"""

# Klasse for spillbrettet
class SpilleBrett:
    # Lager diverse variabler til brettet
    hoyde = 500
    bredde = 800
    objekter = []
    
    sluttSpillet = False
    
    poeng = 0
    
    # Lager vinduet
    vindu = pg.display.set_mode([bredde, hoyde])
    font = pg.font.SysFont("Tahoma", 18)
    
    # Legger til objekter 
    def leggTilObjekter(self, objekt):
        self.objekter.append(objekt)
        
    def fjernObjekt(self, objekt):
        self.objekter.remove(objekt)

# Lager en klasse for spillobjektet
class SpillObjekt:
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde):
        self.xPosisjon = xPosisjon
        self.yPosisjon = yPosisjon
        self.farge = farge
        self.hoyde = hoyde
        self.bredde = bredde
        self.rektangel = pg.Rect(self.xPosisjon, self.yPosisjon, self.bredde, self.hoyde)
        self.brett = spillebrett
    
    # Lager en metode for plassering, altså tegner selve objektet
    def plassering(self):
        pg.draw.rect(vindu, self.farge, self.rektangel)
        
    # Oppdaterer rektangelets posisjon
    def oppdaterRektangel(self):
        self.rektangel.topleft = (self.xPosisjon, self.yPosisjon)
    
    # Sjekker om det er en kollisjon i spillet
    def sjekkKollisjon(self, objekt):
        return self.rektangel.colliderect(objekt.rektangel)
        

# Lager en klasse for spilleren
class Spiller(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde, fart, poeng, retning):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)
        self.fart = fart
        self.poeng = poeng
        self.fartRetning = retning
        self.frysPosisjon = False
        
    # Lager en bevegelsesfunkjon for spilleren
    def flytt(self, brett):
        if self.fartRetning == "hoyre" and self.xPosisjon < brett.bredde - self.bredde:
            self.xPosisjon += self.fart
        elif self.fartRetning == "venstre" and self.xPosisjon > 0:
            self.xPosisjon -= self.fart
        elif self.fartRetning == "opp" and self.yPosisjon > 0:
            self.yPosisjon -= self.fart
        elif self.fartRetning == "ned" and self.yPosisjon < brett.hoyde - self.hoyde:
            self.yPosisjon += self.fart
        self.oppdaterRektangel()


# Klasse for annet objekt
class AnnetObjekt(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)

# Klasse for annet objekt
class Ball(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)
        self.vx = rd.randint(0, 1)
        self.vy = rd.randint(0, 1)
        
    def flytt(self, brett, objekt):
        
        
        if self.vx == 0:
            self.vx = -1
        
        if self.vy == 0:
            self.vy = -1
        
        if self.xPosisjon + self.bredde >= brett.bredde or self.xPosisjon - self.bredde <= 0:
            self.vx *= -1

        if self.yPosisjon - self.hoyde <= 0:
            self.vy *= -1
            
        if self.yPosisjon + self.hoyde >= brett.hoyde:
            return True
        
        self.xPosisjon += self.vx
        self.yPosisjon += self.vy
        self.oppdaterRektangel()
    
    def sjekkKollisjonen(self, objekt):
        xAvstand = abs(self.xPosisjon - objekt.xPosisjon)
        yAvstand = abs(self.yPosisjon - objekt.yPosisjon)
        
        if xAvstand <= self.bredde /2 + objekt.bredde/2 and yAvstand <= self.hoyde/2 + self.hoyde/2:
            self.vy *= -1
            return True
        self.oppdaterRektangel()
        
            
    
""""""

# Spillbrett
brett = SpilleBrett()

# Vindu og tittel
vindu = pg.display.set_mode((brett.bredde, brett.hoyde))
pg.display.set_caption("Pygame vindu")

# Lager en funksjon som stopper spillet
def sluttSpill():
    spiller.fart = 0
    pg.draw.rect(vindu, GRONN, (0, 0, brett.bredde, brett.hoyde))
    tekst = font.render("Da er spillet over!", True, (0, 0, 0))
    vindu.blit(tekst, (brett.bredde/2-120, 200))

# Lager spiller
spiller = Spiller(brett.bredde/2, brett.hoyde/2 + 200, GRONN, brett, 200, 20, 3, 10, "hoyre")

# Legger til objekter på brettet
brett.leggTilObjekter(spiller)

ballene = []

for i in range(3):
    ballen = Ball(rd.randint(100, brett.bredde), rd.randint(100, brett.hoyde/2), (rd.randint(0, 255), rd.randint(0, 255), rd.randint(0, 255)), brett, 20, 20)
    brett.leggTilObjekter(ballen)
    ballene.append(ballen)


# Evig Løkke 
fortsett = True
while fortsett:
    
    # Sjekker hendelser fra brukeren
    for event in pg.event.get():
        
        # Trykke på "X" i vinduet
        if event.type == pg.QUIT:
            print(event)
            fortsett = False
    
    brett.vindu.fill(HVIT)

    for objekt in brett.objekter:
        objekt.plassering()
    
    # Henter en ordbok med status for alle tastatur-taster
    taster = pg.key.get_pressed()
    
    
    for ball in ballene:
        if ball.sjekkKollisjonen(spiller):
            nyBall = Ball(rd.randint(100, brett.bredde), rd.randint(100, brett.hoyde/2), (rd.randint(0, 255), rd.randint(0, 255), rd.randint(0, 255)), brett, 20, 20)
            ballene.append(nyBall)
            brett.leggTilObjekter(nyBall)
            brett.poeng += 1
        if ball.flytt(brett, spiller):
            brett.sluttSpillet = True
    
    if taster[K_LEFT]:
        spiller.fartRetning = "venstre"
    elif taster[K_RIGHT]:
        spiller.fartRetning = "hoyre"   
    
    # Gjør så spilleren kan bevege seg
    spiller.flytt(brett)
         
    tekst = font.render("Dine poeng er: " + str(brett.poeng), True, (0, 0, 0))
    vindu.blit(tekst, (brett.bredde/2 - brett.bredde/4, 60))     

    
    if brett.sluttSpillet:
        sluttSpill()
    
    # Oppdaterer alt innhold i vinduet
    pg.display.flip()
    
    clock.tick(60)

# Avslutter pygame
pg.quit()
