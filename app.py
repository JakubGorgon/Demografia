import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Demografia Kanady",
    page_icon="🇨🇦",
    layout="wide"
)
st.markdown("# Demografia Kanady")


df = pd.read_pickle("data/interim/population.csv")

st.sidebar.subheader("Filtry")
filtry_plec = st.sidebar.multiselect(label="Płeć", placeholder="Wybierz Płeć",
               options=["Wszyscy", "Kobiety", "Mężczyźni"],
               default="Wszyscy")
filtry_wiek = st.sidebar.multiselect(label="Wiek", 
                             placeholder="Wybierz Przedział Wiekowy",
                             options=df["Wiek"].unique(),
                             default="Wszyscy")

def prepare_plot_data(selected_plec_filters, selected_wiek_filters, obszar):
    filt = (df["Plec"].isin(selected_plec_filters)) & (df["Obszar"] == obszar) & (df["Wiek"].isin(selected_wiek_filters))
    return df[filt]

df = prepare_plot_data(filtry_plec, filtry_wiek, "Canada")
df['Wiek_Plec'] = df['Wiek'].astype("str") + " - " + df['Plec'].astype("str")


fig = px.line(df, x="Rok", y="Wartosc", color="Wiek_Plec", line_group="Plec",
                  labels={"Plec":"Płeć"}, 
                  title="Liczba ludności Kanady w latach 1971-2024")
fig.update_layout(dragmode="pan",
                  width=1200,
                  height=700)
st.plotly_chart(fig, config={"scrollZoom": True})
