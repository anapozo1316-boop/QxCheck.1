import streamlit as st
import pandas as pd

st.title("QxCheck")

equipos = pd.read_csv("equipos.csv")
disponibles = pd.read_csv("disponibles.csv")

equipo = st.selectbox("Equipo", equipos["equipo"].unique())

df = equipos[equipos["equipo"] == equipo]

resultado = df.merge(disponibles, on="instrumento", how="left")

resultado["cantidad_disponible"] = resultado["cantidad_disponible"].fillna(0)
resultado["faltante"] = resultado["cantidad_requerida"] - resultado["cantidad_disponible"]

st.dataframe(resultado)
