import streamlit as st
import pandas as pd

st.set_page_config(page_title="QxCheck", layout="wide")

equipos_df = pd.read_csv("equipos.csv")
disponibles_df = pd.read_csv("disponibles.csv")

st.title("QxCheck - Verificación quirúrgica")

equipo = st.selectbox("Selecciona un equipo", equipos_df["equipo"].unique())

df = equipos_df[equipos_df["equipo"] == equipo]

resultado = df.merge(disponibles_df, on="instrumento", how="left")

resultado["cantidad_disponible"] = resultado["cantidad_disponible"].fillna(0)

resultado["faltante"] = resultado["cantidad_requerida"] - resultado["cantidad_disponible"]

st.dataframe(resultado)

if (resultado["faltante"] > 0).any():
    st.error("⚠️ Equipo incompleto")
else:
    st.success("🟢 Equipo completo")
