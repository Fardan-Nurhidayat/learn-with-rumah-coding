import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("harga_rumah.csv")


df_no_missing = df.copy()

# Drop column that have a missing value
# The colum : building_area , bathrooms, bedrooms
df_no_missing = df_no_missing.dropna(subset=["building_area" , "bathrooms" , "bedrooms"])

# Handling null value in garage column
df_no_missing['garage'] = df_no_missing['garage'].fillna(0)

