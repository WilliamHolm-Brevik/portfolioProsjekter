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

# Vindu og tittel
vindu = pg.display.set_mode((VINDULENGDE, VINDUHOYDE))
pg.display.set_caption("Pygame vindu")

# Lager farger
SVART = (0, 0, 70)
HVIT = (255, 255, 255)
GRONN = (0, 255, 0)
ROD = (255, 0, 0)
BLAA = (0, 0, 255)


"""
  Tegne rektangel
        pg.draw.rect(vindu, self.farge, (self.xPosisjon, self.yPosisjon, breddeObjekter, breddeObjekter))
"""
# Evig Løkke 
fortsett = True
while fortsett:
    
    # Sjekker hendelser fra brukeren
    for event in pg.event.get():
        
        # Trykke på "X" i vinduet
        if event.type == pg.QUIT:
            print(event)
            fortsett = False
         
    # Oppdaterer alt innhold i vinduet
    pg.display.flip()

# Avslutter pygame
pg.quit()