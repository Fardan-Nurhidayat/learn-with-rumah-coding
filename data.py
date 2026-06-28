import pandas as pd

# df = pd.read_csv("data_no_dup.csv" , header=None)
# df_all_no_dup = pd.read_csv("data_all_no_dup.csv" , header=None)
#
# hasil = pd.concat([df , df_all_no_dup])
#
# hasil.drop_duplicates(inplace=True)
#
# hasil.to_csv("gabungan.csv" , index=False)

df2_no_dup = pd.read_csv("data2_no_dup.csv" , header=None)
df_gabungan = pd.read_csv("gabungan.csv" , header=None)

hasil = pd.concat([df2_no_dup , df_gabungan])
hasil.drop_duplicates(inplace=True)

hasil.to_csv("gabungan2.csv" , index=True)