# Importerer pygame-biblioteket
import pygame as pg
import random as rd
import math 

# Initialisering av pygame
pg.init()

# Importerer piltastene
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT)


# Lager farger
SVART = (0, 0, 70)
HVIT = (255, 255, 255)
GRONN = (0, 255, 0)
ROD = (255, 0, 0)
BLAA = (0, 0, 255)

class Spillebrett:
    hoyde = 500
    bredde = 700
    
    vindu = pg.display.set_mode([bredde, hoyde])
    font = pg.font.SysFont("Tahoma", 18)
    


class SpillObjekt:
    def __init__


class Spiller:
    def __init__(self, )


# Oppretter spillerobjekt og hindringsobjekt
spiller = Spiller()
hindring = Hindring()

# Evig Løkke
fortsett = True
while fortsett:
    # Sjekker hendelser fra brukeren
    for event in pg.event.get():
        # Trykke på "X" i vinduet
        if event.type == pg.QUIT:
            fortsett = False

    
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
        
    spiller.beveg()
        
    # Tømmer vinduet
    vindu.fill(HVIT)

    # Tegner spilleren og hindringen
    vindu.blit(spiller.image, spiller.rect)
    vindu.blit(hindring.image, hindring.rect)

    # Oppdaterer alt innhold i vinduet
    pg.display.flip()

# Avslutter pygame
pg.quit()