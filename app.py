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
Sistema básico para verificar equipos quirúrgicos,
comparar instrumental requerido y detectar faltantes.
""")

# =========================================================
# BASE DE DATOS DE EQUIPOS
# =========================================================
equipos = {

    "Equipo de Plastia": {

        "Pinza Kelly": 27,
        "Tijera Mayo": 4,
        "Porta Agujas": 3,
        "Pinza Allis": 6

    },

    "Equipo de Cesárea": {

        "Pinza Kelly": 15,
        "Pinza Allis": 10,
        "Porta Agujas": 2,
        "Tijera Mayo": 3

    },

    "Equipo de Hernia": {

        "Pinza Kelly": 12,
        "Tijera Mayo": 2,
        "Separador": 2,
        "Porta Agujas": 2

    }

}

# =========================================================
# SELECCIÓN DE EQUIPO
# =========================================================
equipo_seleccionado = st.selectbox(

    "Seleccionar equipo quirúrgico",

    list(equipos.keys())

)

# =========================================================
# CREAR DATAFRAME
# =========================================================
datos = pd.DataFrame({

    "Instrumento":
    list(
        equipos[equipo_seleccionado].keys()
    ),

    "Cantidad Requerida":
    list(
        equipos[equipo_seleccionado].values()
    )

})

# =========================================================
# INGRESAR CANTIDAD DISPONIBLE
# =========================================================
datos["Cantidad Disponible"] = (
    datos["Cantidad Requerida"]
)

# =========================================================
# TABLA EDITABLE
# =========================================================
st.header("📋 Verificación del Equipo")

tabla = st.data_editor(

    datos,

    use_container_width=True,

    num_rows="dynamic"

)

# =========================================================
# CÁLCULOS
# =========================================================
tabla["Faltantes"] = (

    tabla["Cantidad Requerida"] -

    tabla["Cantidad Disponible"]

)

# =========================================================
# ESTADO
# =========================================================
tabla["Estado"] = tabla["Faltantes"].apply(

    lambda x:

    "✅ Completo"

    if x <= 0

    else "❌ Incompleto"

)

# =========================================================
# RESULTADOS
# =========================================================
st.header("📊 Resultado")

st.dataframe(

    tabla,

    use_container_width=True

)

# =========================================================
# TOTAL DE FALTANTES
# =========================================================
faltantes = tabla["Faltantes"].clip(lower=0).sum()

# =========================================================
# ALERTAS
# =========================================================
if faltantes == 0:

    st.success(
        "✅ Equipo quirúrgico completo."
    )

else:

    st.error(

        f"❌ Existen {faltantes} instrumentos faltantes."

    )

    st.warning(
        "Revisar instrumental antes del procedimiento."
    )

# =========================================================
# RESUMEN
# =========================================================
st.header("📌 Resumen General")

col1, col2 = st.columns(2)

with col1:

    st.metric(

        "Instrumentos Evaluados",

        len(tabla)

    )

with col2:

    st.metric(

        "Faltantes Totales",

        int(faltantes)

    )

# =========================================================
# PIE DE PÁGINA
# =========================================================
st.markdown("---")

st.caption(
    "QxCheck | Software de verificación de equipos quirúrgicos."
)
