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

# Vise diagrammet
plt.show()
