import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px



st.set_page_config(
    page_title="Demografia Kanady",
    page_icon="🇨🇦",
    # layout="wide"
)

st.markdown("# Demografia Kanady")
st.markdown("## *Populacja*")

df = pd.read_pickle("data/interim/population.csv")
df_avg = pd.read_pickle("data/interim/population_averages.csv")


filtr_obszar = st.selectbox(label="Obszar", 
                                     placeholder="Wybierz Obszar", 
                                     options=df["Obszar"].unique())
filtry_plec = st.multiselect(label="Płeć", placeholder="Wybierz Płeć",
               options=["Wszyscy", "Kobiety", "Mężczyźni"],
               default="Wszyscy")

st.markdown("---")

def prepare_plot_data(df, selected_plec_filters, selected_wiek_filters, obszar):
    filt = (df["Plec"].isin(selected_plec_filters)) & (df["Obszar"].isin(obszar)) & (df["Wiek"].isin(selected_wiek_filters))
    return df[filt]



col1, col2 = st.columns(2)

with col1:
    if filtr_obszar != "Canada":
        title = f"Liczba ludności {filtr_obszar} w latach 1971-2024"
    else:
        title = "Liczba ludności Kanady w latach 1971-2024"
    
    filtry_wiek = st.multiselect(label="Wiek", 
                             placeholder="Wybierz Przedział Wiekowy",
                             options=df["Wiek"].unique(),
                             default="Wszyscy")
    df_plot = prepare_plot_data(df, filtry_plec, filtry_wiek, [filtr_obszar])
    df_plot['Wiek_Plec'] = df_plot['Wiek'].astype("str") + " - " + df_plot['Plec'].astype("str")
    fig = px.line(df_plot, x="Rok", y="Wartosc", color="Wiek_Plec", line_group="Plec",
                  labels={"Plec":"Płeć"}, 
                  title=title)
    fig.update_layout(dragmode="pan",
                  width=1200,
                  height=600)
    st.plotly_chart(fig, config={"scrollZoom": True})

with col2:
    filtry_miary = st.multiselect("Miara położenia", 
                   options=["Średnia", "Mediana"],
                   default="Średnia")
    
    if (len(filtry_miary) > 1) & (filtr_obszar == "Canada"):
        title = f"Mediana i Średnia wieku w Kanadzie w latach 1971-2024"
    elif (len(filtry_miary) > 1) & (filtr_obszar != "Canada"):
        title = f"Mediana i Średnia wieku w {filtr_obszar} w latach 1971-2024"
    elif (len(filtry_miary) < 2) & (filtr_obszar == "Canada"):
        title = f"{filtry_miary[0]} wieku w Kanadzie w latach 1971-2024"
    else:
        title = f"Mediana i Średnia wieku {filtr_obszar} w latach 1971-2024"

    df_plot_avg = prepare_plot_data(df=df_avg,
                                selected_plec_filters=filtry_plec, 
                                selected_wiek_filters=filtry_miary,
                                obszar=[filtr_obszar])

    df_plot_avg['Miara_Plec'] = df_plot_avg['Wiek'].astype("str") + " - " + df_plot_avg['Plec'].astype("str")



    fig = px.line(df_plot_avg, x="Rok", y="Wartosc", color="Miara_Plec", line_group="Plec",
                    labels={"Plec":"Płeć"}, 
                    title=title)
    fig.update_layout(dragmode="pan",
                    width=1200,
                    height=600)    
    st.plotly_chart(fig, config={"scrollZoom": True})

st.markdown("---")
filtr_rok = st.selectbox(label="Rok", placeholder="Wybierz rok",
                         options=df["Rok"].unique())

def prepare_map(df):
    geojson = gpd.read_file("data/raw/canada_provinces.geo.json")
    geojson.rename(columns={"name": "Obszar"}, inplace=True)

    df = prepare_plot_data(df, ["Wszyscy"], ["Wszyscy"], df["Obszar"].unique()[0:12])
    filt = df["Rok"] == filtr_rok
    df_filt = df[filt]
    df_filt["Wartosc"] = df_filt["Wartosc"].astype('int64')

    filt = df_filt["Obszar"] == "Canada"
    liczba_ludnosci_ogolem = df_filt[filt]["Wartosc"][0]
    
    filt = df_filt["Wartosc"] == df_filt[~filt]["Wartosc"].max()
    max_prowincja = df_filt[filt][["Obszar", "Wartosc"]]
    
    filt = df_filt["Wartosc"] == df_filt[~filt]["Wartosc"].min()
    min_prowincja = df_filt[filt][["Obszar", "Wartosc"]]    
    
    
    geo_df = gpd.GeoDataFrame.from_features(geojson).merge(df_filt, on="Obszar").set_index("Obszar")
    return geo_df, liczba_ludnosci_ogolem, max_prowincja, min_prowincja

geo_df, liczba_ludnosci_ogolem, max_prowincja, min_prowincja = prepare_map(df)

fig = px.choropleth(
    geo_df,
    geojson=geo_df.geometry,
    locations=geo_df.index,
    color="Wartosc",
     projection="mercator",
    color_continuous_scale="Viridis"
)

fig.update_geos(
    fitbounds="locations", 
    visible=False,
    projection_scale=5,
    center={"lat": 60, "lon": -95}
)
fig.update_layout(
    width=1200,  
    height=600, 
    margin={"r": 0, "t": 0, "l": 0, "b": 0}
)

st.markdown(f"### Liczba ludności w prowincjach Kanady w {int(geo_df["Rok"].unique())}:")
st.write(f"* {liczba_ludnosci_ogolem} mieszkańców w całej Kanadzie")
st.write(f"* **{max_prowincja.iloc[0,0]}** najbardziej liczną prowincją ({max_prowincja.iloc[0,1]} mieszkańców)")
st.write(f"* **{min_prowincja.iloc[0,0]}** najmniej liczną prowincją ({min_prowincja.iloc[0,1]} mieszkańców)")

st.plotly_chart(fig, use_container_width=False)
