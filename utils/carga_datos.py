import pandas as pd
import streamlit as st


@st.cache_data
def cargar_datos():

    df = pd.read_excel(
        "data/dataframe_limpio_final.xlsx"
    )

    return df