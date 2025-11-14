import pandas as pd
import matplotlib.pyplot as plt

# Skriver inn filnavn
filnavn = "IT2/TYPER/DATASETT/05 (2).json"

# Lese inn data ved hjelp av pandas
df = pd.read_json(filnavn, encoding="utf-8-sig")

# Konvertere starttidspunkt til datetime og ekstrahere ukedag
df['started_at'] = pd.to_datetime(df['started_at'])
df['weekday'] = df['started_at'].dt.day_name()

# Telle antall turer per ukedag
turer_per_ukedag = df['weekday'].value_counts().sort_index()

# Finne de lokasjonene med flest og minst starter
flest_startlokasjoner = df['start_station_name'].value_counts().nlargest(3).index
minst_startlokasjoner = df['start_station_name'].value_counts().nsmallest(3).index

# Skrive ut lokasjonene med flest og minst starter
print("De lokasjonene der flest starter er: \n")
for lokasjon in flest_startlokasjoner:
    count_lokasjoner = df[df['start_station_name'] == lokasjon].shape[0]
    print(f"Lokasjonen {lokasjon} har over {count_lokasjoner} startlokasjoner")

print("De lokasjonene der minst starter er: \n")    
for lokasjon in minst_startlokasjoner:
    count_lokasjoner = df[df['start_station_name'] == lokasjon].shape[0]
    print(f"Lokasjonen {lokasjon} har over {count_lokasjoner} startlokasjoner")

# Plotting av antall turer per ukedag
plt.figure(figsize=(10, 6))
turer_per_ukedag.plot(kind='bar', color='skyblue')
plt.xlabel('Ukedag')
plt.ylabel('Antall turer')
plt.title('Totalt antall turer per ukedag')
plt.xticks(rotation=45)
plt.grid(axis='y')

# Vise diagrammet
plt.show()

"""

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
"""