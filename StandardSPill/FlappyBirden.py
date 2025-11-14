"""

I denne koden har jeg brukt klasser for å danne byggesteinene til spillet.

"""

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
        
        
    def tyngdeKraft(self, brett):
        self.fart -= 0.1
        
    def hopp(self):
        self.fart += 1
    
    # Lager en bevegelsesfunkjon for spilleren
    def flytt(self, brett):
        self.tyngdeKraft(brett)
        self.yPosisjon -= self.fart
        self.oppdaterRektangel()

class Ror(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)
    

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
spiller = Spiller(brett.bredde/2, brett.hoyde/2, GRONN, brett, 20, 20, 3, 10, 0)

rorene = [Ror(-400, 0, HVIT, brett, 0, 0)]

for i in range(1000):
    hull = rd.randint(300, 400)
    
    ovreRor = Ror(500 + i*500, 0, GRONN, brett, 50, hull-200)
    nedreRor = Ror(500 + i*500, hull, GRONN, brett, 50, 1000)
    brett.leggTilObjekter(ovreRor)
    brett.leggTilObjekter(nedreRor)
    rorene.append(ovreRor)
    rorene.append(nedreRor)



# Legger til objekter på brettet
brett.leggTilObjekter(spiller)

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
    
    spiller.poeng = - rorene[0].xPosisjon//500
    
    # Henter en ordbok med status for alle tastatur-taster
    taster = pg.key.get_pressed()

    if taster[K_SPACE]:
        spiller.hopp()
        
    for roren in rorene:
        roren.xPosisjon += -1
        roren.oppdaterRektangel()
        if spiller.sjekkKollisjon(roren):
            brett.sluttSpillet = True
    
    # Gjør så spilleren kan bevege seg
    spiller.flytt(brett)
         
    tekst = font.render("Dine poeng er: " + str(spiller.poeng), True, (0, 0, 0))
    vindu.blit(tekst, (brett.bredde/2 - brett.bredde/4, 60))     

    # Sjekker kollisjon mellom spilleren og annet objekt
    if spiller.sjekkKollisjon(nedreRor):
        brett.sluttSpillet = True
    
    if brett.sluttSpillet:
        sluttSpill()
    
    # Oppdaterer alt innhold i vinduet
    pg.display.flip()
    
    clock.tick(60)

# Avslutter pygame
pg.quit()
