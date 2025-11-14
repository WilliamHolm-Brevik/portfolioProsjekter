import json
from collections import Counter
import matplotlib.pyplot as plt

# Skriver inn filnavn
filnavn = ""

with open(filnavn, encoding="utf-8-sig") as jsonfil:
    innhold = json.load(jsonfil)
    
    land = []
    
    # Finner land med den spesifikke verdien
    for kanal in innhold:
        land.append(kanal["Country"])
        
    land_antall = Counter(land)
    
    # Finner de 10 største landene med Counter funksjon
    mest_normal = land_antall.most_common(3)
    
    # Printer de ti største landene
    print(mest_normal)
    
    x_verdier = []
    y_verdier = []
    
    for i in range(len(mest_normal)):
        x_verdier.append(mest_normal[i][0])
        y_verdier.append(mest_normal[i][1])
    
    # Sorterer listen med en labda funksjon    
    sortertListe = sorted(antall.items(), key=lambda x:x[1])
    

plt.figure(figsize=(8, 6))  # Adjust the figure size as needed
plt.plot(x, y, marker='o', linestyle='-', color='b', label='Data')
plt.xlabel('X-axis Label')
plt.ylabel('Y-axis Label')
plt.title('Title of the Plot')
plt.grid(True)  # Add gridlines
plt.legend()     # Show legend based on label in plot()
plt.savefig('plot.png')  # Save the plot to a file
plt.show()               # Show the plot interactively