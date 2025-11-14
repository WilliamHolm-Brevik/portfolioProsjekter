import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Skriver inn filnavn
filnavn = "IT2/Eksamensoppgaver/Eksamen Høst 2023/Global YouTube Statistics.json"

# Lese inn data ved hjelp av pandas
df = pd.read_json(filnavn, encoding="utf-8-sig")

# Fjerner alle verdier med "nan"
df = df[df["Country"] != "nan"]

# Finn de tre største kategoriene etter antall apper
top_land = df['Country'].value_counts().nlargest(10).index

cloumn_array = df["Country"].values

print(cloumn_array)


print("Topp 10 land med antall apper:")
print(df['Country'].value_counts().nlargest(10))

gjennomsnittlig_visninger = []
gjennomsnittlig_abonnenter = []


for land in top_land:
    avg_videoViews = df[df['Country'] == land]['video views'].mean()
    gjennomsnittlig_visninger.append(avg_videoViews)
    avg_abonnenter = df[df['Country'] == land]['subscribers'].mean()
    gjennomsnittlig_abonnenter.append(avg_abonnenter)
    count_apps = df[df['Country'] == land].shape[0]
    print(f"Landet: {land}, Antall kanaler: {count_apps}, Gjennomsnittlig visninger: {avg_videoViews:.2f}, Gjennomsnittlige abonnenter: {avg_abonnenter:.2f}")

print("\n\n\n")


for land in top_land[3:]:
    appene = df[df["Country"] == land].nlargest(3, "subscribers")[["Youtuber", "subscribers"]]
    print(appene)

plt.bar(top_land, gjennomsnittlig_abonnenter)
plt.show()