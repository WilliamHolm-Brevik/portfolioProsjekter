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


sone1 = 200
sone2 = 600
sone3 = 800


"""
  Tegne rektangel
        pg.draw.rect(vindu, self.farge, (self.xPosisjon, self.yPosisjon, breddeObjekter, breddeObjekter))
"""

"""Klassene i spillet"""

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
class Mennesket(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde, fart, poeng, retning):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)
        self.fart = fart
        self.poeng = poeng
        self.fartRetning = retning
        self.frysPosisjon = False
        
        # Lager egne verdier for spilleren
        self.bererSau = False
        self.kollisjonSpokelse = False
        
    # Lager en bevegelsesfunkjon for spilleren
    def flytt(self, brett):
        # Kopierer posisjonen før bevegelse for å kunne gå tilbake ved kollisjon
        
        if self.bererSau:
            self.fart = 2
        else:
            self.fart = 3
        
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
        """Sjekker kollisjon og bestemmer om karakteren kan gå gjennom objektet"""
        for objekt in brett.objekter:
            if objekt is not self and self.sjekkKollisjon(objekt) and objekt.gjennom:
                print("Hei")
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

class Spokelse(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde, gjennom):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)
        self.gjennom = gjennom
        
        self.dx = rd.randint(0, 1)
        self.dy = rd.randint(0, 1)
    
    def flytt(self, brett):
        
        
        if self.dx == 0:
            self.dx = -1
            
        if self.dy == 0:
            self.dy = -1
            
        if self.xPosisjon + self.bredde >= sone2 or self.xPosisjon - self.bredde <= sone1:
            self.dx *= -1
            
        if self.yPosisjon + self.hoyde >= brett.hoyde or self.yPosisjon - self.hoyde <= 0:
            self.dy *= -1
        
        self.xPosisjon += self.dx
        self.yPosisjon += self.dy
        self.oppdaterRektangel()


class Hindring(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde, gjennom):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)
        self.gjennom = gjennom
    
# Klasse for sauene
class Sau(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde, gjennom):
        super().__init__(xPosisjon, yPosisjon, farge, spillebrett, bredde, hoyde)
        self.gjennom = gjennom
        
        self.blirBaret = False

        
    def blirLoftet(self, brett, mennesket):
        self.xPosisjon = mennesket.xPosisjon
        self.yPosisjon = mennesket.yPosisjon
        
        self.oppdaterRektangel()
        

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
    mennesket.fart = 0
    pg.draw.rect(vindu, GRONN, (0, 0, 10*storrelse, 10*storrelse))
    pg.draw.rect(vindu, SVART, (0, 0, 10, brett.hoyde))
    pg.draw.rect(vindu, SVART, (0, 0, brett.bredde, 10))
    pg.draw.rect(vindu, SVART, (brett.bredde-10, 0, brett.bredde, brett.hoyde))
    pg.draw.rect(vindu, SVART, (0, brett.hoyde-10, brett.bredde, brett.hoyde))
    tekst = font.render("Da er spillet over!", True, fargen)
    tekst2 = font.render(f"Du fikk {brett.poeng} poeng", True, fargen)
    vindu.blit(tekst2, (brett.bredde/2 - 100, 250))
    vindu.blit(tekst, (brett.bredde/2-120, 200))



"""--------- Lager objektene og plasserer dem på spillbrettet ------------"""


# Lager spiller
mennesket = Mennesket(sone1/2, brett.hoyde/2, GRONN, brett, 20, 20, 3, 10, "hoyre")

# Legger til objekter på brettet
brett.leggTilObjekter(mennesket)


# Lager gruppe for sauene
sauene = []
for i in range(3):
    sauen = Sau(rd.randint(sone2, sone3), rd.randint(0, brett.hoyde), GRONN, brett, 20, 20, True)
    sauene.append(sauen)
    brett.leggTilObjekter(sauen)

# Lager gruppe for hindringene
hindringer = []
for i in range(3):
    hindring = Sau(rd.randint(sone1, sone2), rd.randint(0, brett.hoyde), BLAA, brett, 20, 20, False)
    hindringer.append(hindring)
    brett.leggTilObjekter(hindring)


# Lager gruppe for sauene
spokelsene = []
for i in range(1):
    spokelsen = Spokelse(rd.randint(sone1 + 100, sone2-100), rd.randint(0, brett.hoyde), HVIT, brett, 20, 20, True)
    spokelsene.append(spokelsen)
    brett.leggTilObjekter(spokelsen)
    




    
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
    
    # Tegner et rektangel son sonen i midten
    pg.draw.rect(vindu, SVART, (sone1, 0, 400, brett.hoyde))

    # Plasserer objekt på brettet
    for objekt in brett.objekter:
        objekt.plassering()
    
    # Flytter spokelsene på brettet
    for spokelse in spokelsene:
        spokelse.flytt(brett)
        
    for saua in sauene:
        if saua.sjekkKollisjon(mennesket) and not mennesket.bererSau:
            mennesket.bererSau = True
            saua.blirBaret = True
        
        print(mennesket.bererSau)
        
        if saua.sjekkKollisjon(mennesket):
            if mennesket.bererSau and not saua.blirBaret:
                print("Hei")
                brett.sluttSpillet = True
        
        if saua.xPosisjon <= sone1:
            
            # Legger ned sauen på den andre siden igjen
            
            mennesket.bererSau = False
            brett.poeng += 1
            saua.xPosisjon = rd.randint(sone2, sone3)
            saua.yPosisjon = rd.randint(100, brett.hoyde-100)
            saua.oppdaterRektangel()
            saua.blirBaret = False
            
            # Legger til nytt spøkelse
            
            spokelset = Spokelse(rd.randint(sone1, sone2), rd.randint(0, brett.hoyde), HVIT, brett, 20, 20, True)
            spokelsene.append(spokelset)
            brett.leggTilObjekter(spokelset)
             
        if saua.blirBaret:
            saua.blirLoftet(brett, mennesket)
    
    # Ser om mennesket kolliderer med spokelse
    for spokelse in spokelsene:
        kollisjon = False
        if spokelse.sjekkKollisjon(mennesket) and not mennesket.kollisjonSpokelse:
            mennesket.kollisjonSpokelse = True
            brett.poeng -= 1
            kollisjon = True
        elif spokelse.sjekkKollisjon(mennesket):
            mennesket.kollisjonSpokelse = True
            kollisjon = True
    
    if not kollisjon:
            mennesket.kollisjonSpokelse = False

        
    
    """Gjør så spiller kan bevege seg"""
   
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
        
     
    print(brett.sluttSpillet)
        
    tekst = font.render("Dine poeng er: " + str(brett.poeng), True, (100, 100, 100))
    vindu.blit(tekst, (brett.bredde/2 - brett.bredde/4, 60))     

    """Starter spillet på nytt og sjekker om spillet er over"""
    
    if brett.sluttSpillet:
        sluttSpill()
        storrelse += 10
        fargen = (rd.randint(0, 255), rd.randint(0, 255), rd.randint(0, 255))
        
    
    # Oppdaterer alt innhold i vinduet
    pg.display.flip()
    
    clock.tick(60)

# Avslutter pygame
pg.quit()