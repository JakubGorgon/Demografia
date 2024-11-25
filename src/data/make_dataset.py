import pandas as pd
from stats_can import StatsCan

sc = StatsCan()
df = sc.table_to_df("17-10-0005-01")
df.to_csv("../../data/raw/population_age_gender.csv")

df["TERMINATED"].unique()
filt = (df["TERMINATED"] == "t")
df[filt].head(50)

df["GEO"].value_counts()

df.drop(columns=["DGUID", "UOM_ID", "SCALAR_FACTOR", "SCALAR_ID",
                       "STATUS", "SYMBOL", "TERMINATED", "DECIMALS",
                       "VECTOR", "COORDINATE"],
        inplace=True)

df.columns = ["Data", "Obszar", "Plec", "Wiek", "UOM", "Wartosc"]
df["Plec"] = df["Plec"].replace({"Total - gender": "Wszyscy",
                    "Women+": "Kobiety",
                    "Men+": "Mężczyźni"})

df["Rok"] = df["Data"].dt.year

df.set_index("Data", inplace=True)

cols_to_keep = ["Rok", "Obszar", "Plec", "Wiek", "UOM", "Wartosc"]
df = df[cols_to_keep]

filt = df["UOM"]!="Persons"
df_avg = df[filt]
df_avg["Wiek"] = df_avg["Wiek"].replace({"Median age": "Mediana", "Average age": "Średnia"})
df_avg.to_pickle("../../data/interim/population_averages.csv")

list(df["Wiek"].unique())
przedzialy_wiekowe = {
    "All ages": "Wszyscy",
    "0 to 4 years": "0 do 4 lat",
    "5 to 9 years": "5 do 9 lat",
    "10 to 14 years": "10 do 14 lat",
    "15 to 19 years": "15 do 19 lat",
    "20 to 24 years": "20 do 24 lat",
    "25 to 29 years": "25 do 29 lat",
    "30 to 34 years": "30 do 34 lat",
    "35 to 39 years": "35 do 39 lat",
    "40 to 44 years": "40 do 44 lat",
    "45 to 49 years": "45 do 49 lat",
    "50 to 54 years": "50 do 54 lat",
    "55 to 59 years": "55 do 59 lat",
    "60 to 64 years": "60 do 64 lat",
    "65 to 69 years": "65 do 69 lat",
    "70 to 74 years": "70 do 74 lat",
    "75 to 79 years": "75 do 79 lat",
    "80 to 84 years": "80 do 84 lat",
    "85 to 89 years": "85 do 89 lat",
    "90 to 94 years": "90 do 94 lat",
    "95 to 99 years": "95 do 99 lat",
    "100 years and older": "100 lat i więcej"
}
df["Wiek"] = df["Wiek"].replace(przedzialy_wiekowe, )
filt = df["Wiek"].isin(przedzialy_wiekowe.values())
df = df[filt]

df.to_pickle("../../data/interim/population.csv")

