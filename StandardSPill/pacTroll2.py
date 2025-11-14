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

font = pg.font.Font(None, 40)

# Lager farger
SVART = (0, 0, 70)
GRAA = (70, 70, 70)
HVIT = (255, 255, 255)
GRONN = (0, 255, 0)
ROD = (255, 0, 0)
BLAA = (0, 0, 255)
GUL = (255, 255, 0)


"""
  Tegne rektangel
        pg.draw.rect(vindu, self.farge, (self.xPosisjon, self.yPosisjon, breddeObjekter, breddeObjekter))
"""

"""--------- Klassene i spillet -----------"""

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

"""Lager klasse for spillobjektet"""

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

"""Klassene under arver fra hovedklassen"""

# Lager en klasse for spilleren
class Spiller(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde, fart, poeng, retning):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)
        self.fart = fart
        self.poeng = poeng
        self.fartRetning = retning
        self.frysPosisjon = False
        
        self.matBit = False
        
        
    # Lager en bevegelsesfunkjon for spilleren
    def flytt(self, brett):
        # Kopierer posisjonen før bevegelse for å kunne gå tilbake ved kollisjon
        original_x = self.xPosisjon
        original_y = self.yPosisjon
        
        
        if self.xPosisjon > brett.bredde - self.bredde or self.xPosisjon - self.bredde/2 < 0:
            self.sluttSpillet = True
        if self.yPosisjon > brett.hoyde - self.hoyde or self.yPosisjon - self.hoyde < 0:
            brett.sluttSpillet = True
        

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
        """Sjekker kollisjon og bestemmer om karakteren kan gå gjennom objektet"""
        for objekt in brett.objekter:
            """
            if objekt is not self and self.sjekkKollisjon(objekt) and objekt.gjennom and objekt.farlig:
                brett.sluttSpillet = True
            """
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
        
class Matbit(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde, gjennom):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)
        self.gjennom = gjennom
        self.farlig = False


"""Lager spillbrett og vinduet"""

# Spillbrett
brett = SpilleBrett()

# Vindu og tittel
vindu = pg.display.set_mode((brett.bredde, brett.hoyde))
pg.display.set_caption("Pygame vindu")

# Lager en funksjon som stopper spillet
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



""" -------   Lager objektene og plasserer dem på spillbrettet    -----"""


# Lager spiller
spiller = Spiller(brett.bredde/2, brett.hoyde/2, GRONN, brett, 20, 20, 3, 10, 0)
annet_objekt = AnnetObjekt(100, 100, ROD, brett, 200, 20, False)

# Legger til objekter på brettet
brett.leggTilObjekter(spiller)

matBiter = []
for i in range(3):
    matBiten = Matbit(rd.randint(0, brett.bredde), rd.randint(0, brett.hoyde), GUL, brett, 20, 20, True)
    matBiter.append(matBiten)
    brett.leggTilObjekter(matBiten)
    



"""Her starter loopen på spillet """

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
    
    # Plasserer objektene på brettet
    for objekt in brett.objekter:
        objekt.plassering()
    
    
    """ Går gjennom kollisjoner til matbitene """
    kollisjon = False
    for matbit in matBiter:
        if matbit.sjekkKollisjon(spiller) and not spiller.matBit and not matbit.farlig:
            matbit.farlig = True
            brett.poeng += 1
            spiller.matBit = True
            matbit.farge = SVART
            spiller.fart += 1
            
            nyMatBit = Matbit(rd.randint(0, brett.bredde), rd.randint(0, brett.hoyde), GUL, brett, 20, 20, True)
            brett.leggTilObjekter(nyMatBit)
            matBiter.append(nyMatBit)
            
            
        if matbit.sjekkKollisjon(spiller):
            kollisjon = True
        
        if matbit.sjekkKollisjon(spiller) and not spiller.matBit and matbit.farlig:
            brett.sluttSpillet = True
    if kollisjon:
        spiller.matBit = True
    if not kollisjon:
        spiller.matBit = False
            
            
        
            
        
    
    
    
    
    
    """ -----  Gjør så spiller kan bevege seg -----  """
   
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
        
     
        
    tekst = font.render("Dine poeng er: " + str(brett.poeng), True, (0, 0, 0))
    vindu.blit(tekst, (brett.bredde/2 - brett.bredde/4, 60))     

    """ ------- Starter spillet på nytt og sjekker om spillet er over ------ """
    
    if brett.sluttSpillet:
        sluttSpill()
        storrelse += 10
        fargen = (rd.randint(0, 255), rd.randint(0, 255), rd.randint(0, 255))
        
    
    # Oppdaterer alt innhold i vinduet
    pg.display.flip()
    
    clock.tick(60)

# Avslutter pygame
pg.quit()