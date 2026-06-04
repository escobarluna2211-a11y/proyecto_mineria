import streamlit as st
import pandas as pd
import plotly.express as px

from utils.carga_datos import cargar_datos

# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="Categorías Mineras",
    page_icon="📊",
    layout="wide"
)

df = cargar_datos()

# ==========================================
# TITULO
# ==========================================

st.title("📊 Categorías Mineras")

st.markdown("""
Análisis de las categorías mineras presentes en las solicitudes
de formalización y legalización minera en Colombia.
""")

# ==========================================
# FILTROS
# ==========================================

st.sidebar.header("🔎 Filtros")

departamento = st.sidebar.multiselect(
    "Departamento",
    sorted(df["DEPARTAMENTO"].unique())
)

if departamento:

    df = df[
        df["DEPARTAMENTO"].isin(departamento)
    ]

# ==========================================
# KPIS
# ==========================================

c1, c2, c3 = st.columns(3)

c1.metric(
    "Categorías",
    df["CATEGORIAS"].nunique()
)

c2.metric(
    "Solicitudes",
    len(df)
)

c3.metric(
    "Minerales",
    df["MINERAL_NORMALIZADO"].nunique()
)

st.divider()

# ==========================================
# PARTICIPACIÓN NACIONAL
# ==========================================

cat = (
    df["CATEGORIAS"]
    .value_counts()
    .reset_index()
)

cat.columns = [
    "CATEGORIA",
    "TOTAL"
]

fig1 = px.treemap(
    cat,
    path=["CATEGORIA"],
    values="TOTAL",
    title="Participación por Categoría"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ==========================================
# BARRAS HORIZONTALES
# ==========================================

fig2 = px.bar(
    cat.sort_values(
        "TOTAL",
        ascending=True
    ),
    x="TOTAL",
    y="CATEGORIA",
    orientation="h",
    text="TOTAL",
    title="Ranking de Categorías"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==========================================
# DEPARTAMENTOS POR CATEGORIA
# ==========================================

st.subheader(
    "🏆 Departamentos líderes por categoría"
)

categoria_seleccionada = st.selectbox(
    "Seleccione una categoría",
    sorted(
        df["CATEGORIAS"].dropna().unique()
    )
)

tmp = df[
    df["CATEGORIAS"]
    ==
    categoria_seleccionada
]

ranking = (
    tmp.groupby("DEPARTAMENTO")
    ["CODIGO_EXPEDIENTE"]
    .nunique()
    .reset_index()
)

ranking = ranking.sort_values(
    "CODIGO_EXPEDIENTE",
    ascending=False
)

fig3 = px.bar(
    ranking.head(15),
    x="CODIGO_EXPEDIENTE",
    y="DEPARTAMENTO",
    orientation="h",
    text="CODIGO_EXPEDIENTE",
    title=f"Top Departamentos - {categoria_seleccionada}"
)

fig3.update_layout(
    yaxis=dict(
        categoryorder="total ascending"
    )
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==========================================
# MINERALES DE LA CATEGORIA
# ==========================================

st.subheader(
    "⛏️ Minerales asociados"
)

minerales = (
    tmp["MINERAL_NORMALIZADO"]
    .value_counts()
    .reset_index()
)

minerales.columns = [
    "MINERAL",
    "TOTAL"
]

fig4 = px.bar(
    minerales.head(20),
    x="MINERAL",
    y="TOTAL",
    text="TOTAL",
    title=f"Minerales de {categoria_seleccionada}"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ==========================================
# TABLA DETALLADA
# ==========================================

st.subheader(
    "📋 Resumen de categorías"
)

st.dataframe(
    cat,
    use_container_width=True
)