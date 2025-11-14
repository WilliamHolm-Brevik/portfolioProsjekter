import pygame as pg
import random as rn
import math as m

pg.init()

# Initialiserer/starter pygame
VINDULENGDE = 1000
VINDUHOYDE = 500

sone1 = 200
sone2 = 600
sone3 = 200

slutt = False

vindu = pg.display.set_mode((VINDULENGDE, VINDUHOYDE))
pg.display.set_caption("Multipong")

# Lager farger
SVART = (0, 0, 0)
HVIT = (255, 255, 255)
GRONN = (0, 255, 0)
ROD = (255, 0, 0)
BLÅ = (0, 0, 255)




breddeObjekter = 20
font = pg.font.Font(None, 50)


class SpillObjekt:
    def __init__(self, xPosisjon: int, yPosisjon: int):
        """Konstruktør"""
        self.xPosisjon = xPosisjon
        self.yPosisjon = yPosisjon
    
    def plassering(self):
        pg.draw.rect(vindu, self.farge, (self.xPosisjon, self.yPosisjon, breddeObjekter, breddeObjekter))
  
class Menneske(SpillObjekt):
    def __init__(self, xPosisjon: int, yPosisjon: int, fart: int, poeng: int, bærerSau, farge):
        super().__init__(xPosisjon, yPosisjon)
        self.fart = fart
        self.poeng = poeng
        self.bærerSau = False
        self.farge = farge
    
    def reduserFart(self):
        if self.bærerSau:
            self.fart = 2
        else:
            self.fart = 5
        
    def økPoeng(self):
        self.poeng += 1
    
    def bærSau(self, Sau):
        Sau.xPosisjon = self.xPosisjon
        Sau.yPosisjon = self.yPosisjon
        self.reduserFart()

class Hindring(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, farge):
        super().__init__(xPosisjon, yPosisjon)
        self.farge = farge
        
    def kollisjonMenneske(self, menneske):       
        #Kollisjon med venstre side av rektangel
        if(self.xPosisjon + breddeObjekter >= menneske.xPosisjon and self.yPosisjon > menneske.yPosisjon and self.yPosisjon < menneske.yPosisjon + breddeObjekter):
            return 1
            
    
        # Kollisjon med høyre side av rektangelet
        if(self.xPosisjon - breddeObjekter > menneske.xPosisjon + breddeObjekter and self.yPosisjon > menneske.yPosisjon and self.yPosisjon < menneske.yPosisjon + breddeObjekter): 
            return 2
            
        # Kollisjon med toppen av rektangelet
        if(self.yPosisjon + breddeObjekter >= menneske.yPosisjon and self.xPosisjon > menneske.xPosisjon and self.xPosisjon < menneske.xPosisjon + breddeObjekter):
            return 3
            
            
        # Kollisjon med bunnen  av rektangelet
        if(self.yPosisjon - breddeObjekter > menneske.yPosisjon + breddeObjekter and self.xPosisjon > menneske.xPosisjon and self.xPosisjon < menneske.xPosisjon + breddeObjekter):
            return 4
            
            
            
        
class Spøkelse(SpillObjekt):
    def __init__(self, xPosisjon: int, yPosisjon: int, yFart, xFart, farge):
        super().__init__(xPosisjon, yPosisjon)
        self.yFart = yFart
        self.xFart = xFart
        self.farge = farge
    
    def endreRetning(self):
        
        if self.xPosisjon - breddeObjekter <= sone1 or self.xPosisjon + breddeObjekter >= sone1 + sone2:
            self.xFart *= -1
        elif self.yPosisjon - breddeObjekter <= 0 or self.yPosisjon + breddeObjekter >= VINDUHOYDE:
            self.yFart *= -1
        
        self.yPosisjon += self.yFart
        self.xPosisjon += self.xFart
        
            
    def kollisjonMenneske(self, menneske):
        if abs(menneske.xPosisjon - self.xPosisjon) <= breddeObjekter and abs(menneske.yPosisjon - self.yPosisjon) <= breddeObjekter:
            menneske.poeng -= 1
            
        
        
            
            
class Sau(SpillObjekt):
    def __init__(self, xPosisjon, yPosisjon, bært, farge):
        super().__init__(xPosisjon, yPosisjon)
        self.bært = bært
        self.farge = farge
    
    def kollisjonMenneske(self, menneske):
        if abs(menneske.xPosisjon - self.xPosisjon) <= breddeObjekter*2 and abs(menneske.yPosisjon - self.yPosisjon) <= breddeObjekter*2:
            self.bært = True
            menneske.bærerSau = True
            
    def sjekkSone(self, menneske):
        if self.xPosisjon <= sone1:
            menneske.bærerSau = False
            self.bært = False
            self.xPosisjon = VINDULENGDE - rn.randint(50, 200)
            self.yPosisjon = VINDUHOYDE - rn.randint(100, 400)
            menneske.økPoeng()
            menneske.reduserFart()


menneske = Menneske(10, VINDUHOYDE/2, 5, 0, False, BLÅ)

spøkelser = []

for i in range(5):
    spøkelser.append(Spøkelse(VINDULENGDE/(6-i)+100, VINDUHOYDE/(6-i)+100, 2*(-1)**(i), 2, SVART))

hindringer = []

for i in range(5):
    hindringer.append(Hindring(sone1 + sone2/2 - rn.randint(-300, 300), VINDUHOYDE/2 - rn.randint(-300, 300), GRONN))

sauene = []

for i in range(1):
    sauene.append(Sau(VINDULENGDE - 100, i*80 + 20, False, HVIT))

# Gjenta helt til brukeren lukker vinduet
fortsett = True
while fortsett:

    # Sjekker om brukeren har lukket vinduet
    for event in pg.event.get():
        if event.type == pg.QUIT:
            fortsett = False


    # Farger bakgrunnen lyseblå
    vindu.fill((135, 206, 235))
    
    pg.draw.rect(vindu, GRONN, (0, 0, sone1, VINDUHOYDE))
    pg.draw.rect(vindu, ROD, (sone1, 0, sone2, VINDUHOYDE))  
    pg.draw.rect(vindu, GRONN, (sone2 + sone1, 0, sone3, VINDUHOYDE))  
     
    
    
    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT] and menneske.xPosisjon > 0:
        for hindring in hindringer:
            if hindring.kollisjonMenneske(menneske) == 1:
                menneske.xPosisjon += menneske.fart
        menneske.xPosisjon -= menneske.fart             
    if keys[pg.K_RIGHT] and menneske.xPosisjon < VINDULENGDE - breddeObjekter:
        for hindring in hindringer:
            if hindring.kollisjonMenneske(menneske) == 2:
                menneske.xPosisjon -= menneske.fart
        menneske.xPosisjon += menneske.fart
    if keys[pg.K_UP] and menneske.yPosisjon > 0:
        for hindring in hindringer:
            if hindring.kollisjonMenneske(menneske) == 3:
                menneske.yPosisjon += menneske.fart
        menneske.yPosisjon -= menneske.fart
    if keys[pg.K_DOWN] and menneske.yPosisjon < VINDUHOYDE - breddeObjekter:
        for hindring in hindringer:
            if hindring.kollisjonMenneske(menneske) == 4:
                menneske.yPosisjon -= menneske.fart
        menneske.yPosisjon += menneske.fart
    menneske.plassering()
    
    
    if menneske.bærerSau:
        for sau in sauene:
            if sau.bært:
                menneske.bærSau(sau)
                sau.sjekkSone(menneske)
            else:
                sau.plassering()     
    else:
        for sau in sauene:
            sau.kollisjonMenneske(menneske)
            sau.plassering()
    
    for hindring in hindringer:
        hindring.plassering()
    
    for spøkelse in spøkelser:
        spøkelse.kollisjonMenneske(menneske) 
        spøkelse.endreRetning()
        spøkelse.plassering()
    
    poeng_text = font.render(f'{menneske.poeng}', True, (0, 0, 0))
    vindu.blit(poeng_text, (VINDULENGDE/2-50, 10))
            
    #poeng_text = font.render(f'{mennske.poeng}', True, (0, 0, 0))
    #window.blit(poeng_text, (WINDOW_WIDTH/2-50, 10))
            

    # Sjekker avstanden mellom spiller og hinder
    #print(spiller.finnAvstand(hinder))

    # Oppdaterer alt innholdet i vinduet
    pg.display.flip()
    
    pg.time.Clock().tick(60)

# Avslutter pygame
pg.quit()