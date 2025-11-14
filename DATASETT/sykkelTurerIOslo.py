import json
from collections import Counter
import matplotlib.pyplot as plt

# Skriver inn filnavn
filnavn = "IT2/TYPER/DATASETT/05 (1).json"

with open(filnavn, encoding="utf-8-sig") as jsonfil:
    innhold = json.load(jsonfil)
    
    lokasjoner = []
    
    # Finner land med den spesifikke verdien
    for lokasjon in innhold:
        lokasjoner.append(lokasjon["start_station_name"])
        
    plasser_antall = Counter(lokasjoner)
    
    print(plasser_antall)
    
    
    mest_normal = plasser_antall.most_common(3)
    
    
    minst_normal = []
    
    for i in range(3):
        minstNormal = plasser_antall[-i]
        minst_normal.append(minstNormal)
    
    print(mest_normal)
    
    """
    print("De minst besøkte stedene er:")
    for i in range(3):
        print(f"{minst_normal[i][0]} med {minst_normal[i][1]} besøk")
        """
    
    x_verdier = []
    y_verdier = []
    
    for i in range(len(mest_normal)):
        x_verdier.append(mest_normal[i][0])
        y_verdier.append(mest_normal[i][1])
    
    # Sorterer listen med en labda funksjon    
    #sortertListe = sorted(antall.items(), key=lambda x:x[1])
    

plt.figure(figsize=(8, 6))  # Adjust the figure size as needed
plt.bar(x_verdier, y_verdier)
plt.xlabel('X-axis Label')
plt.ylabel('Y-axis Label')
plt.title('Title of the Plot')
plt.grid(True)  # Add gridlines
plt.legend()     # Show legend based on label in plot()
plt.savefig('plot.png')  # Save the plot to a file
plt.show()               # Show the plot interactively
