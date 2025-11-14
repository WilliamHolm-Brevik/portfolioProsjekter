import pandas as pd
from collections import Counter

# Skriver inn filnavn
filnavn = "IT2/TYPER/DATASETT/googleplaystore copy.json"

# Lese inn data ved hjelp av pandas
df = pd.read_json(filnavn, encoding="utf-8-sig")

df = df[df["Category"] != "nan"]

storste_kategorier = df["Category"].value_counts().nlargest(10)

print(storste_kategorier)

for storst_kategori in storste_kategorier:
    gjennomsnitt = df[df["Categori"] == storst_kategori]["Installs"]


#print(storste_kategorier)

filter = df["Category"] == "FAMILY"

#print(df[df["Country"] == "India"]["video views"].mean())



#print(df[df["Category"] == "FAMILY"])

filter = (df["Category"] =="FAMILY") & (df["Type"] == "Free")



