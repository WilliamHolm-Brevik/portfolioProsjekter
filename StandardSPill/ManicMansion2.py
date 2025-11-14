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


sone1 = 200

sone2 = 600

sone3 = 800

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
    poeng = 0
    
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
class Mennesket(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde, fart, poeng, retning):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)
        self.fart = fart
        self.poeng = poeng
        self.fartRetning = retning
        
        
        # Lager verdier for mennesket
        self.bererSau = False
        
        
        
        
    # Lager en bevegelsesfunkjon for spilleren
    def flytt(self, brett):
        # Kopierer posisjonen før bevegelse for å kunne gå tilbake ved kollisjon
        original_x = self.xPosisjon
        original_y = self.yPosisjon
        
        if self.bererSau:
            self.fart = 3
        

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

class Hindring(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde, gjennom):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)
        self.gjennom = gjennom

class Spokelse(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde, gjennom):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)
        self.gjennom = gjennom
        # Gjør så spøkelset kan bevege seg i mange forskjellige retninger
        self.dx = float(rd.randint(5, 10)/10)
        self.dy = float(rd.randint(5, 10)/10)
        
        self.posisjonX = self.xPosisjon
        self.posisjonY = self.yPosisjon
        
    def beveg(self, brett):
        
        if self.xPosisjon <= sone1 + self.bredde or self.xPosisjon >= sone2 - self.bredde:
            self.dx *= -1
        if self.yPosisjon <= 0 + self.bredde or self.yPosisjon >= brett.hoyde - self.hoyde:
            self.dy *= -1
        
        # Bevegelsen av selve objektet
        self.posisjonX += self.dx
        self.posisjonY += self.dy
        self.xPosisjon = round(self.posisjonX)
        self.yPosisjon = round(self.posisjonY)
        self.oppdaterRektangel()
        
        

class Sau(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde, gjennom):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)
        self.gjennom = gjennom
        
        # Lager verdi for sau
        self.blirBert = False
        
    def berSau(self, brett):
        sau.farge = SVART
        
    def leggTilbake(self, brett):
        sau.farge = HVIT
        sau.xPosisjon = rd.randint(sone2, sone3)
        sau.yPosisjon = rd.randint(0, brett.hoyde)
        

# Spillbrett
brett = SpilleBrett()        

# Lager gruppe for hindringer
hindringer = []  
      
for i in range(3):
    hindring = Hindring(rd.randint(sone1 + 100, sone2), rd.randint(0, brett.hoyde), GRAA, brett, 20, 20, False)
    hindringer.append(hindring)
    brett.leggTilObjekter(hindring)

# Lager gruppe for sauer

sauer = []
for i in range(3):
    sau = Sau(rd.randint(sone2, sone3), rd.randint(0, brett.hoyde), HVIT, brett, 20, 20, True)
    sauer.append(sau)
    brett.leggTilObjekter(sau)

# Lager en gruppe for spøkelser

spokelser = []
spokelse = Spokelse(rd.randint(sone1 + 100, sone2), rd.randint(100, brett.hoyde-100), GRONN, HVIT, 20, 20, True)
spokelser.append(spokelse)
brett.leggTilObjekter(spokelse)

# Vindu og tittel
vindu = pg.display.set_mode((brett.bredde, brett.hoyde))
pg.display.set_caption("Pygame vindu")

# Lager en funksjon som stopper spillet
def sluttSpill():
    mennesket.fart = 0
    pg.draw.rect(vindu, GRONN, (0, 0, brett.bredde, brett.hoyde))
    tekst = font.render("Da er spillet over!", True, (0, 0, 0))
    tekst2 = font.render(f"Du fikk totalt {brett.poeng}", True, (0, 0, 0))
    vindu.blit(tekst2, (brett.bredde/2 - 120, 250))
    vindu.blit(tekst, (brett.bredde/2-120, 200))

# Lager spiller
mennesket = Mennesket(sone1-100, brett.hoyde/2, GRONN, brett, 20, 20, 3, 10, 0)

# Legger til objekter på brettet
brett.leggTilObjekter(mennesket)

# Evig Løkke 
kollisjonSpokelse = False
fortsett = True
while fortsett:
    
    # Sjekker hendelser fra brukeren
    for event in pg.event.get():
        
        # Trykke på "X" i vinduet
        if event.type == pg.QUIT:
            print(event)
            fortsett = False
    
    brett.vindu.fill(SVART)

    for objekt in brett.objekter:
        objekt.plassering()
    
    sjekkKollisjon = False

    for spokelsen in spokelser:
        spokelsen.beveg(brett)
        if spokelsen.sjekkKollisjon(mennesket):
            if not kollisjonSpokelse:
                brett.poeng -= 1
            if kollisjonSpokelse:
                pass
            sjekkKollisjon = True
    if sjekkKollisjon:
        kollisjonSpokelse = True
    if not sjekkKollisjon:
        kollisjonSpokelse = False
            
    for sau in sauer:
        if sau.sjekkKollisjon(mennesket) and not mennesket.bererSau:
            mennesket.bererSau = True
            sau.blirBert = True
            sau.berSau(brett)
        if mennesket.xPosisjon <= sone1 and mennesket.bererSau:
            sau.leggTilbake(brett)
            mennesket.bererSau = False
            brett.poeng += 1
            spokelsenen = Spokelse(rd.randint(sone1, sone2), rd.randint(0, brett.hoyde), GRONN, brett, 20, 20, True)
            spokelser.append(spokelsenen)
            brett.leggTilObjekter(spokelsenen)
        if sau.sjekkKollisjon(mennesket) and mennesket.bererSau and not sau.blirBert:
            print("hei")
            brett.sluttSpillet = True
            print(brett.sluttSpillet)
    
    
    
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
    
    # Gjør så spilleren kan bevege seg
    mennesket.flytt(brett)
         
    tekst = font.render("Dine poeng er: " + str(brett.poeng), True, (HVIT))
    vindu.blit(tekst, (brett.bredde/2 - brett.bredde/4, 60))     

        
    if brett.sluttSpillet:
        sluttSpill()
        
    # Oppdaterer alt innhold i vinduet
    pg.display.flip()

    
    clock.tick(60)

# Avslutter pygame
pg.quit()