from statistics import mean

import re
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
# Import knn
from sklearn.neighbors import KNeighborsClassifier

encoder = OneHotEncoder(handle_unknown="ignore")
df = pd.read_csv("gabungan2.csv")

df_copy = df.copy()

df_copy.drop(columns=["ID"], inplace=True)
df_copy.drop(columns=["name"], inplace=True)
df_copy.drop(columns=["address"], inplace=True)


def jumlahkan(x):
    parts = str(x).split("+")
    return sum(int(p.strip()) for p in parts)


#
df_copy["bedroom"] = df_copy["bedroom"].apply(jumlahkan)
df_copy["bathroom"] = df_copy["bathroom"].apply(jumlahkan)
df_copy["garage"] = df_copy["garage"].apply(jumlahkan)


def hilangkanLTdanm2(x):
    return (
        x.replace("LT:", "")
        .replace("m²", "")
        .replace("\xa0", "")
        .strip()
    )


def hilangkanLBdanm2(x):
    return (
        x.replace("LB:", "")
        .replace("m²", "")
        .replace("\xa0", "")
        .strip()
    )

def konversi_harga(teks):
    if pd.isna(teks):
        return None

    teks = str(teks).lower()

    teks = teks.replace("rp", "")
    teks = teks.replace("." , "")
    teks = teks.strip()

    # Ambil angka
    angka = re.findall(r'[\d,]+', teks)

    if not angka:
        return None
    angka = float(angka[0].replace(",", "."))
    if "miliar" in teks:
        angka *= 1000000000
    elif "juta" in teks:
        angka *= 1000000
    return int(angka)

df_copy["surface_area"] = df_copy["surface_area"].apply(hilangkanLTdanm2)
df_copy["building_area"] = df_copy["building_area"].apply(hilangkanLBdanm2)

df_copy["surface_area"] = pd.to_numeric(df_copy["surface_area"])
df_copy["building_area"] = pd.to_numeric(df_copy["building_area"])

# Define a column with null values
null_columns = ["surface_area", "building_area"]
df_copy[null_columns] = df_copy[null_columns].fillna(df_copy[null_columns].median())


df_copy["price"] = df_copy["price"].apply(konversi_harga)

encoder = OneHotEncoder(handle_unknown="ignore")
df_copy = pd.get_dummies(df_copy , columns=["city"], drop_first=True)

X_train , X_test , y_train , y_test = train_test_split(df_copy.drop(columns=["price"]) , df_copy["price"] , test_size=0.2 , random_state=42)

KNNModel = KNeighborsClassifier(n_neighbors=5)
KNNModel.fit(X_train , y_train)

pred = KNNModel.predict(X_test)
print(f"Accuracy : {KNNModel.score(X_test , y_test)}")



