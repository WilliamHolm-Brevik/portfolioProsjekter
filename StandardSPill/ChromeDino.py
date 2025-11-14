# Importerer pygame-biblioteket
import pygame as pg
import random as rd
import math as m

# Importerer piltastene
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE)

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
class Dino(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde, fart, retning):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)
        self.fart = fart
        self.fartRetning = retning
        self.frysPosisjon = False
        
    def tyngdekraft(self, brett):
        if self.yPosisjon >= brett.hoyde/2+100 - self.hoyde -3:
            self.fart = 0
        else:
            self.fart += 0.1
        self.yPosisjon += self.fart
        self.oppdaterRektangel()
        
    def hopp(self, brett):
        self.fart = -5
        self.yPosisjon = brett.hoyde/2+100 - self.hoyde -4


# Klasse for annet objekt
class AnnetObjekt(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)

# Klasse for annet objekt
class Kaktus(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)
    

# Spillbrett
brett = SpilleBrett()

# Vindu og tittel
vindu = pg.display.set_mode((brett.bredde, brett.hoyde))
pg.display.set_caption("Pygame vindu")



# Lager en funksjon som stopper spillet
def sluttSpill():
    dinoen.fart = 0
    pg.draw.rect(vindu, GRONN, (0, 0, brett.bredde, brett.hoyde))
    tekst = font.render("Da er spillet over!", True, (0, 0, 0))
    vindu.blit(tekst, (brett.bredde/2-120, 200))

# Lager spiller
dinoen = Dino(brett.bredde/2, brett.hoyde/2, GRONN, brett, 20, 20, 3, 0)

# Legger til objekter på brettet
brett.leggTilObjekter(dinoen)


kaktusene = []

for i in range(1000):
    hoyden = rd.randint(50, 100)
    kaktusen = Kaktus(i*500+100, brett.hoyde/2+100 - hoyden, GRONN, brett, 30, hoyden)
    kaktusene.append(kaktusen)
    brett.leggTilObjekter(kaktusen)


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
    
    # Lage
    for kaktusa in kaktusene:
        kaktusa.xPosisjon -= 1
        kaktusa.oppdaterRektangel()
        if dinoen.sjekkKollisjon(kaktusa):
            brett.sluttSpillet = True
    
    pg.draw.line(brett.vindu, SVART, (0, brett.hoyde/2+100), (brett.bredde, brett.hoyde/2+100))
    
    
    # Henter en ordbok med status for alle tastatur-taster
    taster = pg.key.get_pressed()

    if taster[K_SPACE]:
        if dinoen.yPosisjon >= brett.hoyde/2 + 100 - dinoen.hoyde - 3:
            dinoen.hopp(brett)
        
    dinoen.tyngdekraft(brett)
    
         
    tekst = font.render("Dine poeng er: " + str(brett.poeng), True, (0, 0, 0))
    vindu.blit(tekst, (brett.bredde/2 - brett.bredde/4, 60))     


    
    if brett.sluttSpillet:
        sluttSpill()
    
    # Oppdaterer alt innhold i vinduet
    pg.display.flip()
    
    clock.tick(60)

# Avslutter pygame
pg.quit()
