# Importerer pygame-biblioteket
import pygame as pg
import random as rd
import math as m

# Importerer piltastene
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT)

# Initialisering av pygame
pg.init()
clock = pg.time.Clock()

# Lengde og høyde på vindu angitt i piksler
VINDULENGDE = 600
VINDUHOYDE = 450

# Lager en standard for bredden til alle objekter

breddeObjekter = 20

font = pg.font.Font(None, 30)


# Vindu og tittel
vindu = pg.display.set_mode((VINDULENGDE, VINDUHOYDE))
pg.display.set_caption("Pygame vindu")

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


class SpillObjekt:
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett):
        self.xPosisjon = xPosisjon
        self.yPosisjon = yPosisjon
        self.farge = farge
        
        self.brett = spillebrett
        
    def plassering(self):
        pg.draw.rect(vindu, self.farge, (self.xPosisjon, self.yPosisjon, breddeObjekter, breddeObjekter))
        
    def sjekkKollisjon(self, objekt):
        AvstandX = (self.xPosisjon - objekt.xPosisjon)**2
        AvstandY = (self.yPosisjon - objekt.yPosisjon)**2
        
        avstand = m.sqrt(AvstandX + AvstandY)
        
        if avstand < breddeObjekter:
            return True
    
    
class Mennesket(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, fart, bererSau, poeng, retning):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett)
        self.fart = fart
        self.bererSau = False
        self.poeng = poeng
        self.fartRetning = retning
        self.frysPosisjon = False
        
    def flytt(self, brett):
        if self.fartRetning == "hoyre" and self.xPosisjon < brett.bredde - breddeObjekter:
            self.xPosisjon += self.fart
        elif self.fartRetning == "venstre" and self.xPosisjon > 0:
            self.xPosisjon -= self.fart
        elif self.fartRetning == "opp" and self.yPosisjon > 0:
            self.yPosisjon -= self.fart
        elif self.fartRetning == "ned" and self.yPosisjon < brett.hoyde - breddeObjekter:
            self.yPosisjon += self.fart

class Spøkelse(SpillObjekt):
    def __init__(self, farge, xPosisjon, yPosisjon, spillebrett, vx, vy):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett)
        self.vx = vx
        self.vy = vy
    
    def flytt(self, brett):
        if self.xPosisjon + breddeObjekter <= 200 or self.xPosisjon + breddeObjekter >= brett.bredde-200:
            self.vx *= -1
        elif self.yPosisjon - breddeObjekter <= 0 or self.yPosisjon + breddeObjekter >= brett.hoyde:
            self.vy *= -1
        self.xPosisjon += self.vx
        self.yPosisjon += self.vy
        
class Sau(SpillObjekt):
    def __init__(self, farge, xPosisjon, yPosisjon, spillebrett, bert):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett)
        self.bert = False
    
    def plukkOpp(self):
        self.xPosisjon = 100000
        self.yPosisjon = 100000
        
    def tilbake(self, brett):
        self.xPosisjon = rd.randint(brett.bredde-200, brett.bredde)
        self.yPosisjon = rd.randint(0, brett.hoyde)
        
class Hindring(SpillObjekt):
    def __init__(self, farge, xPosisjon, yPosisjon, spillebrett):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett)
    

brett = SpilleBrett()

spøkelse = Spøkelse(SVART, rd.randint(200, 600), rd.randint(100, 400), brett,  1, 1)
mennesket = Mennesket(rd.randint(0, 100), rd.randint(0, 100), GRONN, brett, 2, False, 0, 0)


sauer = []

for i in range(3):
    sau = Sau(SVART, rd.randint(brett.bredde-200, brett.bredde), rd.randint(0, brett.hoyde), brett, False)
    sauer.append(sau)
    brett.leggTilObjekter(sau)
    
hindringer = []

for i in range(3):
    hindring = Hindring(GRAA, 200 + rd.randint(0, 400), 100 + rd.randint(0, 400), brett)
    hindringer.append(hindring)
    brett.leggTilObjekter(hindring)
    

brett.leggTilObjekter(spøkelse)
brett.leggTilObjekter(mennesket)

kollisjon = False

# Evig Løkke 
fortsett = True
while fortsett:
    
    # Sjekker hendelser fra brukeren
    for event in pg.event.get():
        
        # Trykke på "X" i vinduet
        if event.type == pg.QUIT:
            print(event)
            fortsett = False
    
    brett.vindu.fill((HVIT))
    
    spøkelse.flytt(brett)
    
    for objekt in brett.objekter:
        objekt.plassering()
        
    
    if mennesket.sjekkKollisjon(spøkelse):
        if not kollisjon:
            mennesket.poeng -= 1
            kollisjon = True
    else:
        kollisjon = False
        
    for sau in sauer:
        if mennesket.sjekkKollisjon(sau) and not mennesket.bererSau:
            mennesket.bererSau = True
            sau.plukkOpp()
            sau.bert = True
            mennesket.fart -= 1
            
        if mennesket.sjekkKollisjon(sau) and mennesket.bererSau:
            fortsett = False
            
        if mennesket.xPosisjon <= 200 and mennesket.bererSau and sau.bert:
            mennesket.poeng += 1
            sau.bert = False
            mennesket.bererSau = False
            mennesket.fart += 1
            sau.tilbake(brett)
    
    for hindring in hindringer:
        if mennesket.sjekkKollisjon(hindring):
            mennesket.fartRetning = 0
    
    
    # Henter en ordbok med status for alle tastatur-taster
    taster = pg.key.get_pressed()

    if taster[K_UP]:
        mennesket.fartRetning = "opp"
    elif taster[K_DOWN]:
        mennesket.fartRetning = "ned"
    elif taster[K_LEFT]:
        mennesket.fartRetning = "venstre"
    elif taster[K_RIGHT]:
        mennesket.fartRetning = "hoyre"   
    
        
    mennesket.flytt(brett) 
         
    tekst = font.render(str(mennesket.poeng), True, (0, 0, 0))
    vindu.blit(tekst, (VINDULENGDE/2, 60))     
    
    # Oppdaterer alt innhold i vinduet
    pg.display.flip()
    
    clock.tick(60)

# Avslutter pygame
pg.quit()
