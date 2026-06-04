import streamlit as st
import pandas as pd

from dotenv import load_dotenv
import os

from utils.carga_datos import cargar_datos
from utils.ia_indicadores import generar_contexto
from utils.groq_client import generar_informe_groq

load_dotenv()

# ==================================
# CONFIG
# ==================================

st.set_page_config(
    page_title="Informe IA",
    page_icon="🤖",
    layout="wide"
)

# ==================================
# DATOS
# ==================================

df = cargar_datos()

# ==================================
# TITULO
# ==================================

st.title(
    "🤖 Generador Inteligente de Informes"
)

st.markdown("""
Genere informes ejecutivos, técnicos y territoriales
a partir de los filtros seleccionados.
""")

# ==================================
# FILTROS
# ==================================

st.sidebar.header(
    "Filtros"
)

departamentos = st.sidebar.multiselect(
    "Departamento",
    sorted(
        df["DEPARTAMENTO"]
        .dropna()
        .unique()
    )
)

municipios = st.sidebar.multiselect(
    "Municipio",
    sorted(
        df["MUNICIPIO"]
        .dropna()
        .unique()
    )
)

minerales = st.sidebar.multiselect(
    "Mineral",
    sorted(
        df["MINERAL_NORMALIZADO"]
        .dropna()
        .unique()
    )
)

categorias = st.sidebar.multiselect(
    "Categoría",
    sorted(
        df["CATEGORIAS"]
        .dropna()
        .unique()
    )
)

# ==================================
# FILTRO
# ==================================

df_filtrado = df.copy()

if departamentos:

    df_filtrado = (
        df_filtrado[
            df_filtrado["DEPARTAMENTO"]
            .isin(departamentos)
        ]
    )

if municipios:

    df_filtrado = (
        df_filtrado[
            df_filtrado["MUNICIPIO"]
            .isin(municipios)
        ]
    )

if minerales:

    df_filtrado = (
        df_filtrado[
            df_filtrado["MINERAL_NORMALIZADO"]
            .isin(minerales)
        ]
    )

if categorias:

    df_filtrado = (
        df_filtrado[
            df_filtrado["CATEGORIAS"]
            .isin(categorias)
        ]
    )

# ==================================
# TIPO INFORME
# ==================================

tipo_informe = st.selectbox(

    "Tipo de Informe",

    [
        "Gerencial",
        "Técnico",
        "Territorial",
        "Minerales",
        "Formalización"
    ]
)

# ==================================
# KPIS
# ==================================

c1,c2,c3,c4 = st.columns(4)

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

# ==================================
# BOTON
# ==================================

if st.button(
    "🚀 Generar Informe"
):

    contexto = (
        generar_contexto(
            df_filtrado
        )
    )

    with st.spinner(
        "Generando informe..."
    ):

        informe = (
            generar_informe_groq(
                os.getenv(
                    "GROQ_API_KEY"
                ),
                contexto,
                tipo_informe
            )
        )

    st.markdown(
        informe
    )