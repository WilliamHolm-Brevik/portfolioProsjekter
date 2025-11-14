# Importerer pygame-biblioteket
import pygame as pg
import random as rd

# Initialisering av pygame
pg.init()

# Lengde og høyde på vindu angitt i piksler
VINDULENGDE = 1450
VINDUHOYDE = 1000

# Farger
HVIT = (255, 255, 255)
SVART = (0, 0, 0)
ROD = (255, 127, 127)
GRONN = (127, 255, 127)
GRAA = (200, 200, 200)
BLAA = (0, 0, 255)


# Tekst
tekst = "Kast terning"

# Vindu og tittel
vindu = pg.display.set_mode((VINDULENGDE, VINDUHOYDE))
pg.display.set_caption("Pygame vindu")

# Stiger og slanger
stiger = {
    "1": "38",
    "4": "14",
    "9": "31",
    "21": "42",
    "28": "84",
    "36": "44",
    "51": "67",
    "71": "91",
    "80": "100"
}

slanger = {
    "16": "6",
    "48": "26",
    "49": "11",
    "56": "53",
    "62": "19",
    "64": "60",
    "87": "24",
    "93": "73",
    "95": "75",
    "98": "78"
}

# Posisjonene til rutenene
xPosisjoner = []
yPosisjoner = []

k = 0.7 # Velger størrelse
offset = VINDULENGDE/2 - 0.22*VINDULENGDE # Adjust this value to move the squares to the right by a desired amount

# Generate coordinates for each square
i = 0
y = 1000*k 
o = 1

while y >= 100*k:
    
    if o == 1:
        x = 100*i*k + offset
        i += 1
        xPosisjoner.append(x)
        yPosisjoner.append(y) 
        if x == 900*k + offset:
            y -= 100*k
            i = 0
            o = 2
    elif o == 2:
        x = (900 - i*100)*k + offset
        i += 1
        xPosisjoner.append(x)
        yPosisjoner.append(y) 
        if x == 0 + offset:
            y -= 100*k
            i = 0
            o = 1

            
        
print(xPosisjoner)
print(yPosisjoner)
# Print the first few coordinates  # printing the first 10 coordinates as an example


class Spiller:
    def __init__(self, xIndex, yIndex, farge):
        self.xIndex = xIndex
        self.yIndex = yIndex
        self.farge = farge
        
    def tegnSpiller(self):
        if self.xIndex >= 0:
            pg.draw.circle(vindu, self.farge, (xPosisjoner[self.xIndex], yPosisjoner[self.yIndex]), 10)
        elif self.xIndex < 0:
            pg.draw.circle(vindu, self.farge, (xPosisjoner[0]-50, yPosisjoner[0]), 10)
        
spiller1 = Spiller(-1, -1, BLAA)

spillere = [spiller1]

# Danner klasse for pilene
class Pil:
    def __init__(self, start, slutt, farge):
        self.start = start
        self.slutt = slutt
        self.farge = farge
        
    def tegnPil(self):
        pg.draw.line(vindu, self.farge, self.start, self.slutt, width=30)


slangene = []

for slange_key, slange_value in slanger.items():  # Iterate over dictionary items
    slangene.append(Pil((xPosisjoner[int(slange_key)-1], yPosisjoner[int(slange_key)-1]),  
                        (xPosisjoner[int(slange_value)-1], yPosisjoner[int(slange_value)-1]), ROD))
    
stigene = []

for stige_key, stige_value in stiger.items():
    stigene.append(Pil((xPosisjoner[int(stige_key)-1], yPosisjoner[int(stige_key)-1]),  
                        (xPosisjoner[int(stige_value)-1], yPosisjoner[int(stige_value)-1]), GRONN))

# Definerer kanppen
knapp = pg.Rect(xPosisjoner[0]-10, yPosisjoner[0]+50, 200, 100)

terning = 0
terning2 = 0

# Evig Løkke 
fortsett = True
while fortsett:
    
    # Sjekker hendelser fra brukeren
    for event in pg.event.get():
        # Trykke på "X" i vinduet
        if event.type == pg.QUIT:
            print(event)
            fortsett = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1: 
                if knapp.collidepoint(event.pos):
                    terning = rd.randint(1, 6)
                    terning2 = terning

        
    vindu.fill(HVIT)
    
    for slang in slangene:
        slang.tegnPil()
    
    for stige in stigene:
        stige.tegnPil()    
    
    # Drawing rectangles for each coordinate
    for i in range(len(xPosisjoner)):
        
        #pg.draw.rect(vindu, SVART, (xPosisjon[i], yPosisjon[i], 10, 10))
        
                # Create a font object
        font = pg.font.Font(None, 36)
        
        # Render the text
        text = font.render(f"{i+1}", True, SVART)
        
        # Get the text rectangle
        text_rect = text.get_rect(center=(xPosisjoner[i], yPosisjoner[i]))
        
        # Draw the text onto the surface
        vindu.blit(text, text_rect)
         
    # Oppdaterer alt innhold i vinduet
    
    if spiller1.xIndex >= 100:
        tekst = font.render("Da var det over!", True, (0, 0, 0))
        vindu.blit(tekst, (VINDULENGDE/2-50, VINDUHOYDE/2+300))
    else:
        # Tegner knapp
        pg.draw.rect(vindu, GRAA, knapp)
        
        # Tegner Knapp tekst
        text_surface = font.render(tekst, True, SVART)
        text_rect = text_surface.get_rect(center=knapp.center)
        vindu.blit(text_surface, text_rect)
        for spill in spillere:
            spill.tegnSpiller()
        
        tekst2 = font.render(f"{terning}", True, (0, 0, 0))
        vindu.blit(tekst2, (VINDULENGDE/2-50, VINDUHOYDE/2+300))
            
    if terning2 > 0:
        spiller1.xIndex += 1
        spiller1.yIndex += 1
        terning2 -= 1
    else:
        for slange_key in slanger:  # Gå gjennom nøklene i slanger-dictionaryet
            if slange_key == str(spiller1.xIndex+1):  # Sjekk om nøkkelen matcher spillerens nåværende posisjon
                slange_verdi = slanger[slange_key]  # Hent den tilhørende verdien (posisjonen spilleren skal flytte til)
                spiller1.xIndex = int(slange_verdi)-1  # Oppdater spillerens x-indeks
                spiller1.yIndex = int(slange_verdi)-1  # Oppdater spillerens y-indeks

        for stige_key in stiger:  # Gå gjennom nøklene i slanger-dictionaryet
            if stige_key == str(spiller1.xIndex+1):  # Sjekk om nøkkelen matcher spillerens nåværende posisjon
                stige_verdi = stiger[stige_key]  # Hent den tilhørende verdien (posisjonen spilleren skal flytte til)
                spiller1.xIndex = int(stige_verdi)-1  # Oppdater spillerens x-indeks
                spiller1.yIndex = int(stige_verdi)-1  # Oppdater spillerens y-indeks
    
    
    pg.display.flip()

# Avslutter pygame
pg.quit()
