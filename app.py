import streamlit as st
import pandas as pd

st.set_page_config(page_title="QxCheck", layout="wide")

# =========================
# CARGAR DATOS
# =========================
def cargar():
    try:
        equipos = pd.read_csv("equipos.csv")
    except:
        equipos = pd.DataFrame(columns=["equipo","instrumento","cantidad_requerida"])

    try:
        disponibles = pd.read_csv("disponibles.csv")
    except:
        disponibles = pd.DataFrame(columns=["instrumento","cantidad_disponible"])

    return equipos, disponibles


def guardar(df, nombre):
    df.to_csv(nombre, index=False)


equipos_df, disponibles_df = cargar()

st.title("QxCheck - Sistema Hospitalario Editable")

menu = st.sidebar.radio("Menú", ["Ver equipos", "Agregar equipos", "Inventario"])

# =========================
# VER EQUIPOS
# =========================
if menu == "Ver equipos":

    if len(equipos_df) == 0:
        st.warning("No hay equipos creados aún")
    else:
        equipo = st.selectbox("Selecciona equipo", equipos_df["equipo"].unique())

        df = equipos_df[equipos_df["equipo"] == equipo]

        resultado = df.merge(disponibles_df, on="instrumento", how="left")

        resultado["cantidad_disponible"] = resultado["cantidad_disponible"].fillna(0)
        resultado["faltante"] = resultado["cantidad_requerida"] - resultado["cantidad_disponible"]

        st.dataframe(resultado)

        if (resultado["faltante"] > 0).any():
            st.error("⚠️ Equipo incompleto")
        else:
            st.success("🟢 Equipo completo")

# =========================
# AGREGAR EQUIPOS
# =========================
elif menu == "Agregar equipos":

    st.subheader("Crear equipo o agregar instrumentos")

    equipo = st.text_input("Nombre del equipo (ej: Cesárea)")
    instrumento = st.text_input("Instrumento (ej: Allis)")
    cantidad = st.number_input("Cantidad requerida", min_value=0, step=1)

    if st.button("➕ Agregar"):

        nuevo = pd.DataFrame([[equipo, instrumento, cantidad]],
                             columns=["equipo","instrumento","cantidad_requerida"])

        equipos_df = pd.concat([equipos_df, nuevo], ignore_index=True)
        guardar(equipos_df, "equipos.csv")

        st.success("Agregado correctamente")

# =========================
# INVENTARIO
# =========================
elif menu == "Inventario":

    st.subheader("Inventario de pinzas")

    instrumento = st.text_input("Nombre de la pinza")

    cantidad = st.number_input("Cantidad", min_value=0, step=1)

    if st.button("➕ Agregar / Sumar"):

        if instrumento in disponibles_df["instrumento"].values:

            disponibles_df.loc[
                disponibles_df["instrumento"] == instrumento,
                "cantidad_disponible"
            ] += cantidad

        else:

            nueva = pd.DataFrame([[instrumento, cantidad]],
                                 columns=["instrumento","cantidad_disponible"])

            disponibles_df = pd.concat([disponibles_df, nueva])

        guardar(disponibles_df, "disponibles.csv")

        st.success("Inventario actualizado")

    st.dataframe(disponibles_df)
