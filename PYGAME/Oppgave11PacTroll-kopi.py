# Importerer pygame-biblioteket
import pygame as pg
import random as rd

# Importerer piltastene
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT)

# Initialisering av pygame
pg.init()

# Lengde og høyde på vindu angitt i piksler
VINDULENGDE = 600
VINDUHOYDE = 450

poeng = 0
breddeObjekter = 20
font = pg.font.Font(None, 30)

# Vindu og tittel
vindu = pg.display.set_mode((VINDULENGDE, VINDUHOYDE))
pg.display.set_caption("Pygame vindu")

# Lager farger
SVART = (0, 0, 70)
HVIT = (255, 255, 255)
GRONN = (0, 255, 0)
ROD = (255, 0, 0)
BLAA = (0, 0, 255)
GUL = (255, 255, 0)
GRAA = (200, 200, 200)

# Lager en overordnet gruppe for alle  
class SpillObjekt:
    def __init__(self, xPosisjon, yPosisjon, bokstav, farge):
        self.xPosisjon = xPosisjon
        self.yPosisjon = yPosisjon
        self.bokstav = bokstav
        self.farge = farge
    
    def tegn(self):
        pg.draw.rect(vindu, self.farge, (self.xPosisjon, self.yPosisjon, breddeObjekter, breddeObjekter))
        tekst = font.render(self.bokstav, True, (0, 0, 0))
        vindu.blit(tekst, (self.xPosisjon + 5, self.yPosisjon + 5))
        
        
        
class Troll(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, bokstav, farge,  poeng, fartRetning, farten):
        super().__init__(xPosisjon, yPosisjon, bokstav, farge)
        self.poeng = poeng
        self.fartRetning = fartRetning
        self.farten = farten
        
    def fart(self):
            
        if self.fartRetning == "hoyre":
            self.xPosisjon += self.farten
        
        if self.fartRetning == "venstre":
            self.xPosisjon -= self.farten
            
        if self.fartRetning == "opp":
            self.yPosisjon -= self.farten
        
        if self.fartRetning == "ned":
            self.yPosisjon += self.farten
            
        if self.xPosisjon + breddeObjekter > VINDULENGDE or self.xPosisjon - breddeObjekter<= 0 or self.yPosisjon + breddeObjekter >= VINDUHOYDE or self.yPosisjon - breddeObjekter <= 0:
            return True
        print(self.xPosisjon)
            
        
class MatObjekt(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, bokstav, farge,  spist):
        super().__init__(xPosisjon, yPosisjon, bokstav, farge)
        self.spist = False
        
    
    def sjekkKollisjon(self, troll):
        xAvstand = troll.xPosisjon - self.xPosisjon
        yAvstand = troll.yPosisjon - self.yPosisjon
        
        if abs(xAvstand) <= breddeObjekter and abs(yAvstand) <= breddeObjekter:
            self.spist = True
            self.farge = GRAA
            troll.farten += 1
            return True
        else:
            return False
        
trollet = Troll(VINDULENGDE/2, VINDUHOYDE/2, "T", GRONN, 0, 0, 1)
  
matBiter = []
    
for i in range(3):
    matBiter.append(MatObjekt(rd.randint(0, VINDULENGDE), rd.randint(0, VINDUHOYDE), "M", GUL, 0))

# Evig Løkke 
slutt = False
fortsett = True
while fortsett:
        
    # Sjekker hendelser fra brukeren
    for event in pg.event.get():
        
        # Trykke på "X" i vinduet
        if event.type == pg.QUIT:
            print(event)
            fortsett = False
            # Endrer retning hvis en piltast er trykket
    
    vindu.fill(HVIT)
        
    # Henter en ordbok med status for alle tastatur-taster
    taster = pg.key.get_pressed()
    
    if taster[K_UP]:
        trollet.fartRetning = "opp"   
    elif taster[K_DOWN]:
        trollet.fartRetning = "ned"
    elif taster[K_LEFT]:
        trollet.fartRetning = "venstre"
    elif taster[K_RIGHT]:
        trollet.fartRetning = "hoyre"
        
    for i in range(len(matBiter)):
        if matBiter[i].spist and matBiter[i].sjekkKollisjon(trollet):
            fortsett = False
        elif matBiter[i].sjekkKollisjon(trollet):
            poeng += 1
            matBiter.append(MatObjekt(rd.randint(0, VINDULENGDE), rd.randint(0, VINDUHOYDE), "M", GUL, 0))
            if trollet.fartRetning == "opp":
                trollet.fartRetning = "ned"
            elif trollet.fartRetning == "ned":
                trollet.fartRetning = "opp"
            elif trollet.fartRetning == "hoyre":
                trollet.fartRetning = "venstre"
            elif trollet.fartRetning == "venstre":
                trollet.fartRetning = "hoyre"
    
    if trollet.fart() == True:
        fortsett = False
    
    for i in range(len(matBiter)):
        matBiter[i].tegn()
        
    tekst = font.render(str(poeng), True, (0, 0, 0))
    vindu.blit(tekst, (VINDULENGDE/2 -10, 50))
        
    
    trollet.tegn()
         
    # Oppdaterer alt innhold i vinduet
    pg.display.flip()

# Avslutter pygame
pg.quit()