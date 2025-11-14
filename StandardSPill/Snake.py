# Importing pygame and other necessary libraries
import pygame as pg
import random as rd

# Importing key constants from pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT

# Initializing pygame
pg.init()
clock = pg.time.Clock()

# Constants
SVART = (0, 0, 0)
HVIT = (255, 255, 255)
GRONN = (0, 255, 0)
ROD = (255, 0, 0)

# Screen dimensions
BRETT_BREDDE = 800
BRETT_HOYDE = 600

# Initialize game window
vindu = pg.display.set_mode((BRETT_BREDDE, BRETT_HOYDE))
pg.display.set_caption("Snake Game")

# Font
font = pg.font.Font(None, 40)

# Snake segment size
SEGMENT_SIZE = 20

class SpilleBrett:
    def __init__(self):
        self.bredde = BRETT_BREDDE
        self.hoyde = BRETT_HOYDE
        self.vindu = pg.display.set_mode([self.bredde, self.hoyde])
        self.poeng = 0
        self.sluttSpillet = False

    def leggTilObjekter(self, objekt):
        pass

    def fjernObjekt(self, objekt):
        pass

class SpillObjekt:
    def __init__(self, xPosisjon, yPosisjon, farge, bredde, hoyde):
        self.xPosisjon = xPosisjon
        self.yPosisjon = yPosisjon
        self.farge = farge
        self.bredde = bredde
        self.hoyde = hoyde
        self.rektangel = pg.Rect(self.xPosisjon, self.yPosisjon, self.bredde, self.hoyde)
    
    def plassering(self):
        pg.draw.rect(vindu, self.farge, self.rektangel)
    
    def oppdaterRektangel(self):
        self.rektangel.topleft = (self.xPosisjon, self.yPosisjon)
    
    def sjekkKollisjon(self, objekt):
        return self.rektangel.colliderect(objekt.rektangel)

class Spiller(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, bredde, hoyde, fart):
        super().__init__(xPosisjon, yPosisjon, farge, bredde, hoyde)
        self.fart = fart
        self.fartRetning = "hoyre"
        self.kropp = [(xPosisjon, yPosisjon)]
        self.vokse = False
    
    def flytt(self):
        original_x = self.xPosisjon
        original_y = self.yPosisjon

        if self.fartRetning == "hoyre":
            self.xPosisjon += self.fart
        elif self.fartRetning == "venstre":
            self.xPosisjon -= self.fart
        elif self.fartRetning == "opp":
            self.yPosisjon -= self.fart
        elif self.fartRetning == "ned":
            self.yPosisjon += self.fart

        self.kropp.insert(0, (self.xPosisjon, self.yPosisjon))
        if not self.vokse:
            self.kropp.pop()
        self.vokse = False

        self.oppdaterRektangel()
    
    def sjekkSelvKollisjon(self):
        if len(self.kropp) != len(set(self.kropp)):
            return True
        return False

class Mat(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, bredde, hoyde):
        super().__init__(xPosisjon, yPosisjon, farge, bredde, hoyde)

def tegn_brett():
    vindu.fill(HVIT)
    for segment in spiller.kropp:
        pg.draw.rect(vindu, GRONN, (segment[0], segment[1], SEGMENT_SIZE, SEGMENT_SIZE))
    mat.plassering()
    tekst = font.render("Dine poeng: " + str(brett.poeng), True, SVART)
    vindu.blit(tekst, (10, 10))
    pg.display.flip()

def plasser_ny_mat():
    return Mat(rd.randint(0, (BRETT_BREDDE-SEGMENT_SIZE) // SEGMENT_SIZE) * SEGMENT_SIZE,
               rd.randint(0, (BRETT_HOYDE-SEGMENT_SIZE) // SEGMENT_SIZE) * SEGMENT_SIZE,
               ROD, SEGMENT_SIZE, SEGMENT_SIZE)

brett = SpilleBrett()
spiller = Spiller(brett.bredde//2, brett.hoyde//2, GRONN, SEGMENT_SIZE, SEGMENT_SIZE, SEGMENT_SIZE)
mat = plasser_ny_mat()

fortsett = True
while fortsett:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            fortsett = False

    taster = pg.key.get_pressed()
    if taster[K_UP] and spiller.fartRetning != "ned":
        spiller.fartRetning = "opp"
    elif taster[K_DOWN] and spiller.fartRetning != "opp":
        spiller.fartRetning = "ned"
    elif taster[K_LEFT] and spiller.fartRetning != "hoyre":
        spiller.fartRetning = "venstre"
    elif taster[K_RIGHT] and spiller.fartRetning != "venstre":
        spiller.fartRetning = "hoyre"

    spiller.flytt()

    if spiller.xPosisjon < 0 or spiller.xPosisjon >= brett.bredde or spiller.yPosisjon < 0 or spiller.yPosisjon >= brett.hoyde or spiller.sjekkSelvKollisjon():
        brett.sluttSpillet = True

    if spiller.sjekkKollisjon(mat):
        spiller.vokse = True
        brett.poeng += 1
        mat = plasser_ny_mat()

    tegn_brett()

    if brett.sluttSpillet:
        tekst = font.render("Spillet er over! Dine poeng: " + str(brett.poeng), True, ROD)
        vindu.blit(tekst, (brett.bredde // 4, brett.hoyde // 2))
        pg.display.flip()
        pg.time.wait(3000)
        fortsett = False

    clock.tick(10)

pg.quit()
