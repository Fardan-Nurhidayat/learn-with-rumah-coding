from statistics import mean

import numpy as np
import pandas as pd

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


df_copy["surface_area"] = df_copy["surface_area"].apply(hilangkanLTdanm2)
df_copy["building_area"] = df_copy["building_area"].apply(hilangkanLBdanm2)

df_copy["surface_area"] = pd.to_numeric(df_copy["surface_area"])
df_copy["building_area"] = pd.to_numeric(df_copy["building_area"])

print(df_copy["surface_area"].isna().sum())
print(df_copy["building_area"].isna().sum())


# Define a column with null values
null_columns = ["surface_area", "building_area"]
df_copy[null_columns] = df_copy[null_columns].fillna(df_copy[null_columns].median())

print(df_copy.describe())