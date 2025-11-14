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
        # Kopierer posisjonen før bevegelse for å kunne gå tilbake ved kollisjon
        original_x = self.xPosisjon
        original_y = self.yPosisjon

        if self.fartRetning == "hoyre" and self.xPosisjon < brett.bredde - self.bredde:
            self.xPosisjon += self.fart
        elif self.fartRetning == "venstre" and self.xPosisjon > 0:
            self.xPosisjon -= self.fart
        elif self.fartRetning == "opp" and self.yPosisjon > 0:
            self.yPosisjon -= self.fart
        elif self.fartRetning == "ned" and self.yPosisjon < brett.hoyde - self.hoyde:
            self.yPosisjon += self.fart

        self.oppdaterRektangel()

        # Sjekker kollisjon med alle andre objekter
        for objekt in brett.objekter:
            if objekt is not self and self.sjekkKollisjon(objekt) and not objekt.gjennom:
                # Hvis kollisjon skjer, går tilbake til original posisjon
                self.xPosisjon = original_x
                self.yPosisjon = original_y
                self.oppdaterRektangel()
                break

class AnnetObjekt(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde, gjennom):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)
        self.gjennom = gjennom

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
spiller = Spiller(brett.bredde/2, brett.hoyde/2, GRONN, brett, 20, 20, 3, 10, "hoyre")
annet_objekt = AnnetObjekt(100, 100, ROD, brett, 20, 20, False)

# Legger til objekter på brettet
brett.leggTilObjekter(spiller)
brett.leggTilObjekter(annet_objekt)

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

    if taster[K_UP]:
        spiller.fartRetning = "opp"
    elif taster[K_DOWN]:
        spiller.fartRetning = "ned"
    elif taster[K_LEFT]:
        spiller.fartRetning = "venstre"
    elif taster[K_RIGHT]:
        spiller.fartRetning = "hoyre"   
    
    # Gjør så spilleren kan bevege seg
    spiller.flytt(brett)
         
    tekst = font.render("Dine poeng er: " + str(spiller.poeng), True, (0, 0, 0))
    vindu.blit(tekst, (brett.bredde/2 - brett.bredde/4, 60))     

    # Oppdaterer alt innhold i vinduet
    pg.display.flip()
    
    clock.tick(60)

# Avslutter pygame
pg.quit()
