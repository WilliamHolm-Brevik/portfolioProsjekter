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
breddeObjekter = 20

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
    
    # Lager vinduet
    vindu = pg.display.set_mode([bredde, hoyde])
    font = pg.font.SysFont("Tahoma", 18)
    
    # Legger til objekter 
    def leggTilObjekter(self, objekt):
        self.objekter.append(objekt)
        
    def fjernObjekt(self, objekt):
        self.objekter.remove(objekt)

# Klasse for et spillobjekt
class SpillObjekt:
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde):
        self.xPosisjon = xPosisjon
        self.yPosisjon = yPosisjon
        self.farge = farge
        self.bredde = bredde
        self.hoyde = hoyde
        
        self.brett = spillebrett
        
    def plassering(self):
        pg.draw.rect(vindu, self.farge, (self.xPosisjon, self.yPosisjon, self.bredde, self.hoyde))
        
    def sjekkKollisjon(self, objekt):
        AvstandX = (self.xPosisjon - objekt.xPosisjon)**2
        AvstandY = (self.yPosisjon - objekt.yPosisjon)**2
        
        avstand = m.sqrt(AvstandX + AvstandY)
        
        if avstand < breddeObjekter:
            return True
    
# Klasse for spilleren
class Spiller(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde, fart, poeng, retning):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)
        self.fart = fart
        self.poeng = poeng
        self.fartRetning = retning
        
        # Lager variabel for å spise mat
        self.kollisjon = False
        
    def flytt(self, brett):
        if self.fartRetning == "hoyre":
            self.xPosisjon += self.fart
        elif self.fartRetning == "venstre":
            self.xPosisjon -= self.fart
        elif self.fartRetning == "opp":
            self.yPosisjon -= self.fart
        elif self.fartRetning == "ned":
            self.yPosisjon += self.fart
            
    def kollisjonVegg(self):
        if self.xPosisjon > brett.bredde - breddeObjekter:
            return True
        elif self.xPosisjon < 0:
            return True
        elif self.yPosisjon < 0:
            return True
        elif self.yPosisjon > brett.hoyde - breddeObjekter:
            return True
            

class Matbit(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde, farlig):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)
        self.farlig = farlig


# Spillbrett
brett = SpilleBrett()

# Vindu og tittel
vindu = pg.display.set_mode((brett.bredde, brett.hoyde))
pg.display.set_caption("Pygame vindu")

# Lager spiller
spiller = Spiller(brett.bredde/2, brett.bredde/2, GRONN, brett, 20, 20,  3, 0, 0)

# Legger til spiller på brettet
brett.leggTilObjekter(spiller)

# Lager gruppe for matbit
matbiter = []

for i in range(3):
    matbiten = Matbit(rd.randint(0, brett.bredde), rd.randint(0, brett.hoyde), 20, 20, ROD, brett, False)
    matbiter.append(matbiten)
    brett.leggTilObjekter(matbiten)


# Lager en funksjon som stopper spillet
def sluttSpill():
    spiller.fart = 0
    pg.draw.rect(vindu, GRONN, (0, 0, brett.bredde, brett.hoyde))
    tekst = font.render("Da er spillet over!", True, (0, 0, 0))
    vindu.blit(tekst, (brett.bredde/2-120, 200))
    
# Slutter spillet
sluttSpillet = False

# Evig Løkke 
fortsett = True
while fortsett:
    
    # Sjekker hendelser fra brukeren
    for event in pg.event.get():
        
        # Trykke på "X" i vinduet
        if event.type == pg.QUIT:
            print(event)
            fortsett = False
    
    # Fyller vinduet med fargen hvit
    brett.vindu.fill((HVIT))

    for objekt in brett.objekter:
        objekt.plassering()
    
    # Henter en ordbok med status for alle tastatur-taster
    taster = pg.key.get_pressed()
    
    # Lager setninger for å bytte retning til spiller
    if taster[K_UP]:
        spiller.fartRetning = "opp"
    elif taster[K_DOWN]:
        spiller.fartRetning = "ned"
    elif taster[K_LEFT]:
        spiller.fartRetning = "venstre"
    elif taster[K_RIGHT]:
        spiller.fartRetning = "hoyre"   
    
    
    
    
    
    # Sjekker om det er kollisjon mellom spiller og matobjekt
    kollisjonSjekk = False
    for matbit in matbiter:
        if spiller.sjekkKollisjon(matbit):
            kollisjonSjekk = True
    
        if spiller.sjekkKollisjon(matbit) and not matbit.farlig:
            spiller.poeng += 1
            matbit.farlig = True
            matbit.farge = BLAA
            spiller.kollisjon = True
            spiller.spiserMat = True
            spiller.fart += 1
            
            matbita = Matbit(rd.randint(0, brett.bredde), rd.randint(0, brett.hoyde), ROD, brett, False)
            matbiter.append(matbita)
            brett.leggTilObjekter(matbita)
            
            
        if spiller.sjekkKollisjon(matbit) and matbit.farlig and not kollisjon:
            sluttSpillet = True

    if not kollisjonSjekk:
        kollisjon = False      
    
    if sluttSpillet:
        sluttSpill()
    
    spiller.flytt(brett)
    if spiller.kollisjonVegg():
       sluttSpillet = True
        
    tekst = font.render(str(spiller.poeng), True, (0, 0, 0))
    vindu.blit(tekst, (brett.bredde/2, 60))     
    
    # Oppdaterer alt innhold i vinduet
    pg.display.flip()
    
    clock.tick(60)

# Avslutter pygame
pg.quit()
