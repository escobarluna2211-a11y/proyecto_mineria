import streamlit as st
import pandas as pd
import plotly.express as px

from utils.carga_datos import cargar_datos

# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="Explorador Minero",
    page_icon="🔎",
    layout="wide"
)

df = cargar_datos()

# ==========================================
# TITULO
# ==========================================

st.title("🔎 Explorador Inteligente")

st.markdown("""
Explore las solicitudes mineras aplicando filtros dinámicos.
""")

# ==========================================
# FILTROS
# ==========================================

st.sidebar.header("Filtros Avanzados")

expediente = st.sidebar.text_input(
    "Código Expediente"
)

departamentos = st.sidebar.multiselect(
    "Departamento",
    sorted(df["DEPARTAMENTO"].dropna().unique())
)

municipios = st.sidebar.multiselect(
    "Municipio",
    sorted(df["MUNICIPIO"].dropna().unique())
)

minerales = st.sidebar.multiselect(
    "Mineral",
    sorted(df["MINERAL_NORMALIZADO"].dropna().unique())
)

categorias = st.sidebar.multiselect(
    "Categoría",
    sorted(df["CATEGORIAS"].dropna().unique())
)

# ==========================================
# FILTRADO
# ==========================================

df_filtrado = df.copy()

if expediente:

    df_filtrado = df_filtrado[
        df_filtrado["CODIGO_EXPEDIENTE"]
        .astype(str)
        .str.contains(
            expediente,
            case=False,
            na=False
        )
    ]

if departamentos:

    df_filtrado = df_filtrado[
        df_filtrado["DEPARTAMENTO"]
        .isin(departamentos)
    ]

if municipios:

    df_filtrado = df_filtrado[
        df_filtrado["MUNICIPIO"]
        .isin(municipios)
    ]

if minerales:

    df_filtrado = df_filtrado[
        df_filtrado["MINERAL_NORMALIZADO"]
        .isin(minerales)
    ]

if categorias:

    df_filtrado = df_filtrado[
        df_filtrado["CATEGORIAS"]
        .isin(categorias)
    ]

# ==========================================
# KPIS
# ==========================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Registros",
    len(df_filtrado)
)

c2.metric(
    "Expedientes",
    df_filtrado["CODIGO_EXPEDIENTE"].nunique()
)

c3.metric(
    "Municipios",
    df_filtrado["MUNICIPIO"].nunique()
)

c4.metric(
    "Minerales",
    df_filtrado["MINERAL_NORMALIZADO"].nunique()
)

st.divider()

# ==========================================
# RESUMEN AUTOMÁTICO
# ==========================================

st.subheader("📌 Resumen")

if len(df_filtrado) > 0:

    depto_top = (
        df_filtrado["DEPARTAMENTO"]
        .value_counts()
        .idxmax()
    )

    mineral_top = (
        df_filtrado["MINERAL_NORMALIZADO"]
        .value_counts()
        .idxmax()
    )

    st.info(
        f"""
        El conjunto filtrado contiene **{len(df_filtrado):,} registros**.
        
        El departamento con mayor participación es **{depto_top}**.

        El mineral predominante es **{mineral_top}**.
        """
    )

# ==========================================
# GRAFICOS
# ==========================================

col1, col2 = st.columns(2)

with col1:

    top_minerales = (
        df_filtrado["MINERAL_NORMALIZADO"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_minerales.columns = [
        "MINERAL",
        "TOTAL"
    ]

    fig1 = px.bar(
        top_minerales,
        x="MINERAL",
        y="TOTAL",
        title="Top Minerales"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with col2:

    top_departamentos = (
        df_filtrado["DEPARTAMENTO"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_departamentos.columns = [
        "DEPARTAMENTO",
        "TOTAL"
    ]

    fig2 = px.bar(
        top_departamentos,
        x="DEPARTAMENTO",
        y="TOTAL",
        title="Top Departamentos"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ==========================================
# EXPORTAR
# ==========================================

st.subheader("📥 Exportar Resultados")

excel = df_filtrado.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Descargar CSV",
    data=excel,
    file_name="explorador_minero.csv",
    mime="text/csv"
)

# ==========================================
# TABLA
# ==========================================

st.subheader("📋 Datos Filtrados")

st.dataframe(
    df_filtrado,
    use_container_width=True,
    height=600
)