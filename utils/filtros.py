import streamlit as st


def aplicar_filtros(df):

    st.sidebar.header("🔎 Filtros")

    departamentos = st.sidebar.multiselect(
        "Departamento",
        sorted(df["DEPARTAMENTO"].unique())
    )

    categorias = st.sidebar.multiselect(
        "Categoría",
        sorted(df["CATEGORIAS"].unique())
    )

    minerales = st.sidebar.multiselect(
        "Mineral",
        sorted(df["MINERAL_NORMALIZADO"].unique())
    )

    if departamentos:
        df = df[
            df["DEPARTAMENTO"].isin(departamentos)
        ]

    if categorias:
        df = df[
            df["CATEGORIAS"].isin(categorias)
        ]

    if minerales:
        df = df[
            df["MINERAL_NORMALIZADO"].isin(minerales)
        ]

    return df