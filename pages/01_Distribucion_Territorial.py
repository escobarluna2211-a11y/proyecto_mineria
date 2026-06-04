import streamlit as st
import pandas as pd
import plotly.express as px

from utils.carga_datos import cargar_datos

# ==================================================
# CONFIGURACIÓN
# ==================================================

st.set_page_config(
    page_title="Distribución Territorial",
    page_icon="🗺️",
    layout="wide"
)

# ==================================================
# CARGAR DATOS
# ==================================================

df = cargar_datos()

# ==================================================
# TITULO
# ==================================================

st.title("🗺️ Distribución Territorial")

st.markdown("""
Análisis geográfico de las solicitudes de formalización y legalización minera en Colombia.
""")

# ==================================================
# FILTROS
# ==================================================

st.sidebar.header("🔎 Filtros")

# Categoría minera
categorias = st.sidebar.multiselect(
    "Categoría Minera",
    sorted(df["CATEGORIAS"].dropna().unique())
)

# Aplicar filtro categoría
if categorias:

    df = df[
        df["CATEGORIAS"].isin(categorias)
    ]

# Departamento
departamentos = st.sidebar.multiselect(
    "Departamento",
    sorted(df["DEPARTAMENTO"].dropna().unique())
)

if departamentos:

    df = df[
        df["DEPARTAMENTO"].isin(departamentos)
    ]

# ==================================================
# KPIs
# ==================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Expedientes",
        df["CODIGO_EXPEDIENTE"].nunique()
    )

with c2:
    st.metric(
        "Departamentos",
        df["DEPARTAMENTO"].nunique()
    )

with c3:
    st.metric(
        "Municipios",
        df["MUNICIPIO"].nunique()
    )

with c4:
    st.metric(
        "Minerales",
        df["MINERAL_NORMALIZADO"].nunique()
    )

st.divider()

# ==================================================
# TOP DEPARTAMENTOS
# ==================================================

deptos = (
    df.groupby("DEPARTAMENTO")
    ["CODIGO_EXPEDIENTE"]
    .nunique()
    .reset_index()
)

deptos = deptos.sort_values(
    "CODIGO_EXPEDIENTE",
    ascending=False
)

fig_depto = px.bar(
    deptos,
    x="CODIGO_EXPEDIENTE",
    y="DEPARTAMENTO",
    orientation="h",
    text="CODIGO_EXPEDIENTE",
    title="Top Departamentos"
)

fig_depto.update_layout(
    height=650,
    yaxis=dict(
        categoryorder="total ascending"
    )
)

st.plotly_chart(
    fig_depto,
    use_container_width=True
)

# ==================================================
# TOP MUNICIPIOS
# ==================================================

municipios = (
    df.groupby("MUNICIPIO")
    ["CODIGO_EXPEDIENTE"]
    .nunique()
    .reset_index()
)

municipios = municipios.sort_values(
    "CODIGO_EXPEDIENTE",
    ascending=False
)

fig_muni = px.bar(
    municipios.head(15),
    x="CODIGO_EXPEDIENTE",
    y="MUNICIPIO",
    orientation="h",
    text="CODIGO_EXPEDIENTE",
    title="Top 15 Municipios"
)

fig_muni.update_layout(
    height=600,
    yaxis=dict(
        categoryorder="total ascending"
    )
)

st.plotly_chart(
    fig_muni,
    use_container_width=True
)

# ==================================================
# PARTICIPACIÓN POR DEPARTAMENTO
# ==================================================

participacion = deptos.copy()

participacion["PORCENTAJE"] = (
    participacion["CODIGO_EXPEDIENTE"]
    /
    participacion["CODIGO_EXPEDIENTE"].sum()
) * 100

st.subheader(
    "📊 Participación Departamental"
)

fig_pie = px.pie(
    participacion,
    names="DEPARTAMENTO",
    values="PORCENTAJE",
    hole=0.4
)

st.plotly_chart(
    fig_pie,
    use_container_width=True
)

# ==================================================
# TABLA DETALLADA
# ==================================================

st.subheader(
    "📋 Ranking Departamental"
)

st.dataframe(
    participacion,
    use_container_width=True,
    hide_index=True
)