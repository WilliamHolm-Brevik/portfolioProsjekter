# Importerer biblioteker
import json
from collections import Counter
import matplotlib.pyplot as plt

# Skriver inn filnavn
filnavn = "IT2/Eksamensprøver/Eksamen vår 2023/googleplaystore.json"


x_verdier = []
y_verdier = []

with open(filnavn, encoding="utf-8-sig") as jsonfil:
    innhold = json.load(jsonfil)
    
    kategorier_antall = []
    kategorier = []
    
    # Finner land med den spesifikke verdien
    for kategori in innhold:
        kategorier.append(kategori["Category"])
        
    
    kategorier_antall = Counter(kategorier)
    
    # Finner de 10 største kategoriene med Counter funksjon
    mest_normal = kategorier_antall.most_common(3)
    
    # Printer de ti største kategoriene
    print(mest_normal)
    
    for i in range(len(mest_normal)):
        x_verdier.append(mest_normal[i][0])
        y_verdier.append(mest_normal[i][1])
        
    gjennomsnittsrating = []
    gjennomsnittInstallasjoner = []
    gjennomsnitt_rating = 0
    gjennomsnitt_installasjoner = 0
    
    
    for i in range(3):
        gjennomsnitt_rating = 0 # Omstarter verdien til 0 hver gang
        gjennomsnitt_installasjoner = 0 # Omstarter veriden av installasjoner til 0 hver gang
        for kategori in innhold: # Finner hver kategori i filen
            if kategori["Category"] == x_verdier[i]: # Leter etter om dette syemmer
                if kategori["Rating"] == "NaN" or kategori["Installs"] == "NaN":
                    print("Idk")
                else:
                    gjennomsnitt_rating += float(kategori["Rating"])
                    gjennomsnitt_installasjoner += int(''.join(kategori["Installs"][:-1].split(',')))
                    print(gjennomsnitt_installasjoner)
        gjennomsnittsrating.append(gjennomsnitt_rating/y_verdier[i])
        gjennomsnittInstallasjoner.append(gjennomsnitt_installasjoner/y_verdier[i])
        
    print(gjennomsnittsrating)
    print(gjennomsnittInstallasjoner)
    
    # Printer ut de tre med kategoriene med flest antall og flest nedlastinger
    
    for i in range(3):
        print(f"Appen {x_verdier[i]} hadde {gjennomsnittInstallasjoner[i]:.2e} gjennomsnittlige installasjoner, det fantes {y_verdier[i]} apper av denne kategorien og gjennomsnittrating var {gjennomsnittsrating[i]:.1f}")
        
        
    # Vi finner deretter den med flest nedlastinger
    
    mest_normal2 = kategorier_antall.most_common()
    
    installasjon = 0
    
    installasjoner_antall = {}

    # Her er x2_verdier allerede definert som de mest vanlige kategoriene, så vi trenger ikke å lage den igjen.

    for kategori, antall in mest_normal:
        total_installasjon = 0
        for app in innhold:
            if app["Category"] == kategori:
                if app["Installs"] != "NaN" and app["Installs"] != '':
                    print(app["Installs"])
                    total_installasjon += int(''.join(app["Installs"][:-1].split(',')))
        installasjoner_antall[kategori] = total_installasjon

    # Deretter kan vi sortere installasjonene_antall og plotte dem.
    sortertListe = sorted(installasjoner_antall.items(), key=lambda x: x[1], reverse=True)

    print(sortertListe)
    
    
        
plt.bar(x_verdier, y_verdier)
plt.show()