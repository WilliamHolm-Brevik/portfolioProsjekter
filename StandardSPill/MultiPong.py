"""

I denne koden har jeg brukt klasser for å danne objekter og mange deler av spillet

Dessverre var det slik at 


"""

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
    bredde = 300
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
        self.bredde = bredde
        self.hoyde = hoyde
        
        
        self.brett = spillebrett
    
    # Lager en metode for plassering, altså tegner selve objektet
    def plassering(self):
        pg.draw.rect(vindu, self.farge, (self.xPosisjon, self.yPosisjon, self.bredde, self.hoyde))
        
    # Sjekker om det er en kollisjon i spillet
    def sjekkKollisjon(self, objekt):
        AvstandX = abs(self.xPosisjon - objekt.xPosisjon)
        AvstandY = abs(self.yPosisjon - objekt.yPosisjon)
        
        
        if AvstandX <= self.bredde/2 + objekt.bredde/2 and AvstandY <= self.hoyde/2 + objekt.hoyde/2:
            return True
    
# Lager en klasse for spilleren
class Spiller(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde, fart, poeng, fartRetning):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)
        self.fart = fart
        self.poeng = poeng
        self.fartRetning = fartRetning
        self.frysPosisjon = False
        
    # Lager en bevegelsesfunkjon for spilleren
    def flytt(self, brett):
        if self.fartRetning == "hoyre" and self.xPosisjon + self.bredde  <= brett.bredde:
            self.xPosisjon += self.fart
        elif self.fartRetning == "venstre" and self.yPosisjon + self.bredde >= 0:
            self.xPosisjon -= self.fart
            
            
class Ball(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett,  bredde, hoyde, fart, vx, vy):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)
        self.fart = fart
        self.vx = vx
        self.vy = vy

    def tegnBall(self, brett):
        
        if self.vx == 0:
            self.vx = -1
        
        if self.vy == 0:
            self.vy = -1
        
        if self.xPosisjon + self.bredde >= brett.bredde or self.xPosisjon - self.bredde <= 0:
            self.vx *= -1

        if self.yPosisjon - self.hoyde <= 0:
            self.vy *= -1
            
        if self.yPosisjon + self.hoyde >= brett.hoyde:
            return True

        self.xPosisjon += self.vx
        self.yPosisjon += self.vy

    def handle_collisions(self):
        for ball in ballsamling:
            if ball != self:
                distance = math.sqrt((self.xposisjon - ball.xposisjon)**2 + (self.yposisjon - ball.yposisjon)**2)
                if distance <= self.radius + ball.radius:
                    self.vx, ball.vx = ball.vx, self.vx
                    self.vy, ball.vy = ball.vy, self.vy
    

# Spillbrett
brett = SpilleBrett()

# Vindu og tittel
vindu = pg.display.set_mode((brett.bredde, brett.hoyde))
pg.display.set_caption("Pygame vindu")


baller = []

ball = Ball(rd.randint(100, brett.bredde-100), rd.randint(100, brett.hoyde-200), (rd.randint(0, 255), rd.randint(0, 255), rd.randint(0, 255)), brett, 10, 10, 2, 1, 1)

baller.append(ball)
brett.leggTilObjekter(ball)

# Lager en funksjon som stopper spillet
def sluttSpill():
    spiller.fart = 0
    pg.draw.rect(vindu, GRONN, (0, 0, brett.bredde, brett.hoyde))
    tekst = font.render("Da er spillet over!", True, (0, 0, 0))
    vindu.blit(tekst, (brett.bredde/2-120, 200))


# Lager spiller
spiller = Spiller(brett.bredde /2, brett.hoyde - 100, GRONN, brett, 100, 20, 5, 0, 0)

# Legger til spiller på brettet
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
    
    brett.vindu.fill((HVIT))

    for objekt in brett.objekter:
        objekt.plassering()
    
    # Henter en ordbok med status for alle tastatur-taster
    taster = pg.key.get_pressed()

    if taster[K_LEFT]:
        spiller.fartRetning = "venstre"
    elif taster[K_RIGHT]:
        spiller.fartRetning = "hoyre"   
    
    for ballen in baller:
        ballen.tegnBall(brett)
        if ballen.tegnBall(brett):
            brett.sluttSpillet = True
        if spiller.sjekkKollisjon(ballen):
            nyBall = Ball(rd.randint(brett.bredde/4, brett.bredde-brett.bredde/4), rd.randint(brett.hoyde/4, brett.hoyde-brett.hoyde/2), (rd.randint(0, 255), rd.randint(0, 255), rd.randint(0, 255)), brett, 10, 10, 2, rd.randint(0, 1), rd.randint(0, 1))
            baller.append(nyBall)
            brett.leggTilObjekter(nyBall)
            ballen.vy *= -1
    
    # Gjør så spilleren kan bevege seg
    spiller.flytt(brett)
         
    tekst = font.render("Dine poeng er: " + str(spiller.poeng), True, (0, 0, 0))
    vindu.blit(tekst, (brett.bredde/2-200, 60))     
    

        
    if brett.sluttSpillet:
        sluttSpill()
    
    # Oppdaterer alt innhold i vinduet
    pg.display.flip()
    
    clock.tick(60)

# Avslutter pygame
pg.quit()
