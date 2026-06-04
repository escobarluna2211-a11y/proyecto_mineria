import streamlit as st
import pandas as pd
import plotly.express as px

from utils.carga_datos import cargar_datos


# -------------------------------------
# CONFIGURACIÓN
# -------------------------------------

st.set_page_config(
    page_title="Análisis de Minerales",
    page_icon="⛏️",
    layout="wide"
)

# -------------------------------------
# CARGAR DATOS
# -------------------------------------

df = cargar_datos()

# -------------------------------------
# TÍTULO
# -------------------------------------

st.title("⛏️ Análisis de Minerales")

st.markdown("""
Analice la distribución de minerales reportados en las solicitudes
de formalización y legalización minera en Colombia.
""")

# -------------------------------------
# FILTROS
# -------------------------------------

st.sidebar.header("🔎 Filtros")

departamentos = st.sidebar.multiselect(
    "Departamento",
    sorted(df["DEPARTAMENTO"].unique())
)

if departamentos:

    municipios_disponibles = sorted(
        df[
            df["DEPARTAMENTO"].isin(departamentos)
        ]["MUNICIPIO"].unique()
    )

else:

    municipios_disponibles = sorted(
        df["MUNICIPIO"].unique()
    )

municipios = st.sidebar.multiselect(
    "Municipio",
    municipios_disponibles
)

categorias = st.sidebar.multiselect(
    "Categoría Minera",
    sorted(df["CATEGORIAS"].unique())
)

# -------------------------------------
# APLICAR FILTROS
# -------------------------------------

df_filtrado = df.copy()

if departamentos:

    df_filtrado = df_filtrado[
        df_filtrado["DEPARTAMENTO"].isin(
            departamentos
        )
    ]

if municipios:

    df_filtrado = df_filtrado[
        df_filtrado["MUNICIPIO"].isin(
            municipios
        )
    ]

if categorias:

    df_filtrado = df_filtrado[
        df_filtrado["CATEGORIAS"].isin(
            categorias
        )
    ]

# -------------------------------------
# KPIs
# -------------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Minerales diferentes",
        df_filtrado["MINERAL_NORMALIZADO"].nunique()
    )

with col2:

    st.metric(
        "Solicitudes",
        len(df_filtrado)
    )

with col3:

    st.metric(
        "Categorías",
        df_filtrado["CATEGORIAS"].nunique()
    )

st.divider()

# -------------------------------------
# TOP MINERALES
# -------------------------------------

top_minerales = (
    df_filtrado["MINERAL_NORMALIZADO"]
    .value_counts()
    .reset_index()
)

top_minerales.columns = [
    "MINERAL",
    "TOTAL"
]

fig = px.bar(
    top_minerales.head(15),
    x="MINERAL",
    y="TOTAL",
    text="TOTAL",
    title="Top 15 Minerales",
)

fig.update_layout(
    xaxis_title="Mineral",
    yaxis_title="Cantidad",
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------
# TABLA DETALLADA
# -------------------------------------

st.subheader(
    "📋 Detalle de Minerales"
)

st.dataframe(
    top_minerales,
    use_container_width=True
)