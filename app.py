import streamlit as st
import pandas as pd

# =========================================================
# CONFIGURACIÓN
# =========================================================
st.set_page_config(

    page_title="QxCheck",

    page_icon="🩺",

    layout="wide"

)

# =========================================================
# TÍTULO
# =========================================================
st.title("🩺 QxCheck")

st.subheader(
    "Verificación de Equipos Quirúrgicos"
)

st.write("""
Sistema para verificar equipos quirúrgicos,
agregar instrumental y detectar faltantes.
""")

# =========================================================
# MEMORIA TEMPORAL
# =========================================================
if "equipos" not in st.session_state:

    st.session_state.equipos = {

        "Equipo de Plastia": pd.DataFrame({

            "Instrumento": [
                "Pinza Kelly",
                "Tijera Mayo",
                "Porta Agujas"
            ],

            "Cantidad Requerida": [
                27,
                4,
                3
            ]

        })

    }

# =========================================================
# CREAR NUEVO EQUIPO
# =========================================================
st.sidebar.header("➕ Crear Equipo")

nuevo_equipo = st.sidebar.text_input(
    "Nombre del nuevo equipo"
)

if st.sidebar.button("Guardar Equipo"):

    if nuevo_equipo != "":

        st.session_state.equipos[nuevo_equipo] = pd.DataFrame({

            "Instrumento": [],

            "Cantidad Requerida": []

        })

        st.sidebar.success(
            "✅ Equipo agregado"
        )

# =========================================================
# SELECCIONAR EQUIPO
# =========================================================
equipo_actual = st.selectbox(

    "Seleccionar equipo quirúrgico",

    list(
        st.session_state.equipos.keys()
    )

)

# =========================================================
# OBTENER TABLA
# =========================================================
tabla = st.session_state.equipos[equipo_actual]

# =========================================================
# SI NO EXISTE COLUMNA
# =========================================================
if "Cantidad Disponible" not in tabla.columns:

    tabla["Cantidad Disponible"] = (
        tabla["Cantidad Requerida"]
    )

# =========================================================
# TABLA EDITABLE
# =========================================================
st.header("📋 Instrumental del Equipo")

tabla_editada = st.data_editor(

    tabla,

    use_container_width=True,

    num_rows="dynamic"

)

# =========================================================
# GUARDAR CAMBIOS
# =========================================================
st.session_state.equipos[
    equipo_actual
] = tabla_editada

# =========================================================
# CÁLCULOS
# =========================================================
tabla_editada["Faltantes"] = (

    tabla_editada["Cantidad Requerida"]

    -

    tabla_editada["Cantidad Disponible"]

)

# =========================================================
# ESTADO
# =========================================================
tabla_editada["Estado"] = (

    tabla_editada["Faltantes"]

    .apply(

        lambda x:

        "✅ Completo"

        if x <= 0

        else "❌ Incompleto"

    )

)

# =========================================================
# RESULTADOS
# =========================================================
st.header("📊 Resultado")

st.dataframe(

    tabla_editada,

    use_container_width=True

)

# =========================================================
# TOTAL FALTANTES
# =========================================================
faltantes = (

    tabla_editada["Faltantes"]

    .clip(lower=0)

    .sum()

)

# =========================================================
# ALERTAS
# =========================================================
if faltantes == 0:

    st.success(
        "✅ Equipo completo."
    )

else:

    st.error(

        f"❌ Hay {faltantes} instrumentos faltantes."

    )

    st.warning(
        "Revisar instrumental."
    )

# =========================================================
# RESUMEN
# =========================================================
st.header("📌 Resumen")

col1, col2 = st.columns(2)

with col1:

    st.metric(

        "Instrumentos",

        len(tabla_editada)

    )

with col2:

    st.metric(

        "Faltantes",

        int(faltantes)

    )

# =========================================================
# PIE DE PÁGINA
# =========================================================
st.markdown("---")

st.caption(
    "QxCheck | Verificación de equipos quirúrgicos."
)
