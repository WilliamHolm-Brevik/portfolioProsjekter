import json
filnavn = "IT2/TYPER/DATASETT/Global YouTube Statistics.json"

# Leser inn filen
with open(filnavn, encoding="utf-8") as fil:
    data = json.load(fil)
    
    
print("Noen sjekker av datasettet")
# Sjekker om alle linjene kan leses og en stikkprøve på antall kanaler i Spania

linjer = 0
spania = 0
for l in data:
    linjer += 1
    if l["Country"] == "Spain":
        spania += 1
        
print(f"Antall linjer lest er {linjer}. Antall kanaler i Spania er {spania}.")
print("--------- Slutt sjekk ----------")

class Land:
    """Klasse for å representere land"""
    def __init__(self, land):
        self.land = land
        
        self.antallKanaler = 0
        
        self.sumAbonnenter = 0
        self.sumVisninger = 0
        
        self.kanalListe = []
        
    def leggTilKanal(self, nyKanal):
        
        self.kanalListe.append(nyKanal)
        
        self.antallKanaler += 1
        self.sumAbonnenter += nyKanal.abonnenter
        self.sumVisninger += nyKanal.visninger
        
    def visKanalListe(self):
        print(f"Dette er en kanalliste til {self.land}")
        
        for k in self.kanalListe:
            k.visInfo(self.sumAbonnenter, self.sumVisnginer)
            
    def visInfo(self):
        print(f"LAndet {self.land} har {self.antallKanaler} YouTube kanaler.")
        print(f"I snitt {(self.sumVisnigner/self.antallKanaler)/1000000:.2f} millioner visninger")
        print("")
        
class Kanal:
    """Klasse for å representere en kanal"""
    def __init__(self, navn, abonnenter, visninger):
        """Konstruktør"""
        self.navn = navn
        self.abonnenter = abonnenter
        self.visninger = visninger
    
    def visInfo(self, landAbonnenter, landVisninger):
        print(f"Kanalen {self.navn} har {self.abonnenter:.3f} abonnenter og {self.visninger:.3f} visninger")
        
landListe = []

# Lager en liste over land med tilhørende kanaler basert på informasjonen lest fra fil
for kanal in data:
    if kanal["Country"] != "nan":
        funnet = False
        for land in landListe:
            if kanal["Country"] == land.land :
                funnet = True
                land.leggTilKanal(Kanal(kanal["Title"], int[kanal["subscribers"]], int(kanal["video views"])))
        if not funnet:
            # Nytt land-objekt
            nyttLand = Land(kanal["Country"])
            landListe.append(nyttLand)
            # Legger kanalen inn i listen
            nyttLand.leggTilKanal(Kanal(kanal["Title"], int(kanal["subscribers"]), int(kanal["video views"])))   

#Sorterer etter flest kanaler
def sortKanaler(l):
    return(l.antallKanaler)

landSortert = sorted(landListe, key = sortKanaler, reverse = True)

# Viser de 10 landene med flest YouTube kanaler:
print("Landene med flest YouTube kanaler er: ")
for i in range(9):
    landSortert[i].visInfo()
        