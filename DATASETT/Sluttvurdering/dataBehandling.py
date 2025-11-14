"""

I denne oppgaven finner jeg de filialene med flest medlemmer og deretter regner ut gjennomsnittalder. For å gjøre dette bruker jeg forskjellige biblioteker som json og collections. Grunnen til at jeg valgte å bruke Counter i stedet for lange algoritmer, er fordi Counter er en enkel funksjon som gir en mer kompakt kode. 

"""

# Importerer biblioteker
import json # Importerer json for å lese filen 
from collections import Counter # Importerer Counter for å finne forekomster
import matplotlib.pyplot as plt # Importerer matplotlib for å tegn grafer

# Skriver inn filnavn
filnavn = "IT2/Sluttvurdering/libraryusage.json"

# Definerer arrayer for senere plotting av grafer
x_verdier = []
y_verdier = []

# Leser filen
with open(filnavn, encoding="utf-8-sig") as jsonfil:
    innhold = json.load(jsonfil)
    
    # Lager en liste for kundene
    kundene = []
    
    # Finner land med den spesifikke verdien
    for kunde in innhold:
        if kunde["Age Range"] != "null":
            kundene.append(kunde["Home Library Definition"])
    
    # Counter i Python er en innebygd datatypemodul som teller forekomster av elementer i en samling og gir en praktisk måte. Den kan finne de mest vanlige elementene i samlingen ved hjelp av metoden most_common().
    kunde_antall = Counter(kundene)
    
    # Her finner counter de tre største 
    mest_normal = kunde_antall.most_common(3)
    
    # Printer de ti største landene
    print(mest_normal)
    
    # Legger verdiene for mest_normal i egne arrayer for plotting og andre oppgaver
    for i in range(len(mest_normal)):
        x_verdier.append(mest_normal[i][0])
        y_verdier.append(mest_normal[i][1])
        
    # Lager liste for gjennomsnittsalder
    gjennomsnittsalder = []    
    
    for i in range(3): # Regner alderen for de tre kategoriene med flest mennesker
        alder = 0
        for filal in innhold: # Søker etter hver filal i filen og sjekker om den er lik en av de tre mest brukte filalene
            if filal["Home Library Definition"] == x_verdier[i]:
                if filal["Age Range"] == "0 to 9 years":
                    alder += 9/2
                
                if filal["Age Range"] == "10 to 19 years":
                    alder += (10+19)/2
                
                if filal["Age Range"] == "20 to 24 years":
                    alder += (20+24)/2
                
                if filal["Age Range"] == "25 to 34 years":
                    alder += (25+34)/2
                
                if filal["Age Range"] == "35 to 44 years":
                    alder += (35+44)/2
                
                if filal["Age Range"] == "45 to 54 years":
                    alder += (45+54)/2
                
                if filal["Age Range"] == "55 to 59 years":
                    alder += (55+59)/2
                
                if filal["Age Range"] == "60 to 64 years":
                    alder += (60+64)/2
                
                if filal["Age Range"] == "65 to 74 years":
                    alder += (65+74)/2
                    
                if filal["Age Range"] == "75 years and over":
                    alder += (75)
        gjennomsnittsalder.append(alder/y_verdier[i])     
    
    for i in range(3): # Srkiver ut gjennomsnittsalder og antall medlemmer.
        print(f"Filialen {x_verdier[i]} har {y_verdier[i]} medlemmer og har en gjennomsnittsalser på {gjennomsnittsalder[i]:.2f} år")

# Plotter diagram for gjennomsnittsalder
plt.bar(x_verdier, gjennomsnittsalder, label='Gjennomsnittalder') # Plotter bardiagram
plt.xlabel('Biblioteker') # Label for x-akse
plt.ylabel('Alder') # Label for y-akse
plt.title('De tre største filialene sin gjennomsnittsalder') # Tittel på plot
plt.legend() # Viser label
plt.show() # Viser plotten


