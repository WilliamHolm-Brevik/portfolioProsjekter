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
    hoyde = 800
    bredde = 800
    objekter = []
    poeng = 0
    
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


class Kule(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)
        self.gjennom = True
        self.fart = 5
        self.truffet = False
        
    def bevegKule(self, brett):
        self.yPosisjon -= self.fart 
        self.oppdaterRektangel()
        

class Romvesen(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde, gjennom, fart):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)
        self.gjennom = gjennom
        self.fart = fart
        self.retning = 0
        self.liv = 10
        
        
        # Lager posisjoner som rundes opp senere
        self.posisjonX = self.xPosisjon
        self.posisjonY = self.yPosisjon
        
    def bevegelse(self):    
        
        if self.retning <= 8:
            self.retning += 0.1
            self.posisjonX += 0.3
        elif self.retning >= 8:
            if self.retning <= 16:
                self.retning += 0.1
                self.posisjonX -= 0.3
            else:
                self.retning = 0
            
        
        self.posisjonY += self.fart*0.1 # Beveger seg sakte nedover
        
        self.xPosisjon = round(self.posisjonX)
        self.yPosisjon = round(self.posisjonY)
        
        self.oppdaterRektangel()
        
    
    def treffe(self, brett):
        for objekt in brett.objekter:
            if objekt is not self and self.sjekkKollisjon(objekt):
                if objekt.farge == SVART and not objekt.truffet:
                    objekt.truffet = True
                    self.liv -= 1
                    if self.liv > 0:
                        self.farge = (0, 255 - 10*self.liv, 0)
                    if self.liv == 0:
                        brett.poeng += 1
                        brett.fjernObjekt(self)
                        self.oppdaterRektangel()
                    
                elif objekt.farge == SVART:
                    print("Hei")
                else:
                    brett.sluttSpillet = True
                    
                



"""Lager brettet"""

# Spillbrett
brett = SpilleBrett()

# Vindu og tittel
vindu = pg.display.set_mode((brett.bredde, brett.hoyde))
pg.display.set_caption("Pygame vindu")

"""Lager objektene på banen"""

# Lager spiller
spiller = Spiller(brett.bredde/2, brett.hoyde/2 + 200, BLAA, brett, 20, 20, 3, 10, "hoyre")


# Lager romvesen

romvesene = []

for i in range(5):
    for j in range(5):
        romvesen = Romvesen(brett.bredde/2 - 200 + 100*i, brett.hoyde/2 - 200 + 50*j, GRONN, brett, 10, 10, True, 1)
        romvesene.append(romvesen)
        brett.leggTilObjekter(romvesen)

# Legger til objekter på brettet
brett.leggTilObjekter(spiller)
brett.leggTilObjekter(romvesen)


# Lager kulesamling

kuler = []


# Lager en funksjon som stopper spillet
def sluttSpill():
    spiller.fart = 0
    pg.draw.rect(vindu, GRONN, (0, 0, brett.bredde, brett.hoyde))
    tekst = font.render("Da er spillet over!", True, (0, 0, 0))
    vindu.blit(tekst, (brett.bredde/2-120, 200))

# Evig Løkke 
fortsett = True
while fortsett:
    
    # Sjekker hendelser fra brukeren
    for event in pg.event.get():
        
        # Trykke på "X" i vinduet
        if event.type == pg.QUIT:
            print(event)
            fortsett = False
    
    """Tegner alt på skjermen"""
    
    brett.vindu.fill(HVIT)

    for objekt in brett.objekter:
        objekt.plassering()
    
    """Bevegelse til romvesen"""
    
    for romvesenet in romvesene:
        romvesenet.bevegelse()
        romvesenet.treffe(brett)
    
    """Bevegelse til spilleren"""
    
    # Henter en ordbok med status for alle tastatur-taster
    taster = pg.key.get_pressed()

    if taster[K_LEFT]:
        spiller.fartRetning = "venstre"
    elif taster[K_RIGHT]:
        spiller.fartRetning = "hoyre"   
    elif taster[K_SPACE]:
        kule = Kule(spiller.xPosisjon, spiller.yPosisjon, SVART, brett, 2, 2)
        kuler.append(kule)
        brett.leggTilObjekter(kule)
    
    for kulen in kuler:
        kulen.bevegKule(brett)
    
    # Gjør så spilleren kan bevege seg
    spiller.flytt(brett)
    
    
    
    """Displayer poengsummen"""
      
    tekst = font.render("Dine poeng er: " + str(brett.poeng), True, (0, 0, 0))
    vindu.blit(tekst, (brett.bredde/2 - brett.bredde/4, 60))     
    
    if brett.sluttSpillet:
        sluttSpill()
    
    # Oppdaterer alt innhold i vinduet
    pg.display.flip()
    
    clock.tick(60)

# Avslutter pygame
pg.quit()
