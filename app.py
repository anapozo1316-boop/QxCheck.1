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
st.subheader("Verificación de Equipos Quirúrgicos")

st.write("""
Sistema básico para validar instrumental quirúrgico,
detectar faltantes y controlar equipos quirúrgicos.
""")

# =========================================================
# DATOS
# =========================================================
datos = pd.DataFrame({

    "Instrumento": [
        "Pinza Kelly",
        "Pinza Mosquito",
        "Tijera Mayo"
    ],

    "Cantidad Requerida": [
        10,
        8,
        4
    ],

    "Cantidad Disponible": [
        10,
        7,
        4
    ]

})

# =========================================================
# TABLA EDITABLE
# =========================================================
tabla = st.data_editor(
    datos,
    num_rows="dynamic",
    use_container_width=True
)

# =========================================================
# CÁLCULOS
# =========================================================
tabla["Faltantes"] = (
    tabla["Cantidad Requerida"] -
    tabla["Cantidad Disponible"]
)

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
# PIE DE PÁGINA
# =========================================================
st.markdown("---")

st.caption(
    "QxCheck | Software básico de verificación quirúrgica."
)
