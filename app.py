import streamlit as st
import plotly.express as px

from utils.carga_datos import cargar_datos

# ==================================================
# CONFIGURACIÓN
# ==================================================

st.set_page_config(
    page_title="Formalización Minera Colombia",
    page_icon="⛏️",
    layout="wide"
)

# ==================================================
# ESTILOS MODERNOS
# ==================================================

st.markdown("""
<style>

/* Fondo */

.stApp {
    background-color: #F8FAFC;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background-color: white;
    border-right: 1px solid #E5E7EB;
}

/* Menu */

[data-testid="stSidebarNav"] {
    background-color: white;
}

/* Títulos */

h1 {
    color: #0F172A !important;
    font-weight: 800 !important;
}

h2,h3 {
    color: #1E293B !important;
}

/* KPI Cards */

[data-testid="metric-container"] {

    background-color: white;

    border-radius: 15px;

    padding: 20px;

    border: 1px solid #E5E7EB;

    box-shadow:
    0px 2px 8px rgba(0,0,0,0.05);
}

/* Dataframe */

[data-testid="stDataFrame"] {

    border-radius: 15px;

    border: 1px solid #E5E7EB;
}

/* Alert */

.stAlert {

    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# CARGAR DATOS
# ==================================================

df = cargar_datos()

# ==================================================
# HEADER
# ==================================================

st.title(
    "⛏️ Dashboard Ejecutivo de Formalización Minera"
)

st.markdown("""
### Colombia - Solicitudes de Formalización y Legalización Minera

Monitoreo territorial de expedientes mineros, categorías y minerales estratégicos.
""")

st.divider()

# ==================================================
# KPIS
# ==================================================

c1,c2,c3,c4 = st.columns(4)

with c1:

    st.metric(
        "📂 Expedientes",
        f"{df['CODIGO_EXPEDIENTE'].nunique():,}"
    )

with c2:

    st.metric(
        "🗺️ Departamentos",
        df["DEPARTAMENTO"].nunique()
    )

with c3:

    st.metric(
        "🏙️ Municipios",
        df["MUNICIPIO"].nunique()
    )

with c4:

    st.metric(
        "⛏️ Minerales",
        df["MINERAL_NORMALIZADO"].nunique()
    )

st.divider()

# ==================================================
# FILA 1
# ==================================================

col1,col2 = st.columns(2)

with col1:

    st.subheader(
        "🏆 Top Departamentos"
    )

    deptos = (
        df.groupby("DEPARTAMENTO")
        ["CODIGO_EXPEDIENTE"]
        .nunique()
        .reset_index()
        .sort_values(
            "CODIGO_EXPEDIENTE",
            ascending=False
        )
        .head(10)
    )

    fig1 = px.bar(
        deptos,
        x="CODIGO_EXPEDIENTE",
        y="DEPARTAMENTO",
        orientation="h",
        text="CODIGO_EXPEDIENTE",
        color="CODIGO_EXPEDIENTE",
        color_continuous_scale="Blues"
    )

    fig1.update_layout(
        height=500,
        yaxis=dict(
            categoryorder="total ascending"
        )
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with col2:

    st.subheader(
        "📊 Categorías Mineras"
    )

    categorias = (
        df["CATEGORIAS"]
        .value_counts()
        .reset_index()
    )

    categorias.columns = [
        "CATEGORIA",
        "TOTAL"
    ]

    fig2 = px.treemap(
        categorias,
        path=["CATEGORIA"],
        values="TOTAL",
        color="TOTAL",
        color_continuous_scale="Blues"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ==================================================
# FILA 2
# ==================================================

col3,col4 = st.columns(2)

with col3:

    st.subheader(
        "⛏️ Top Minerales"
    )

    minerales = (
        df["MINERAL_NORMALIZADO"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    minerales.columns = [
        "MINERAL",
        "TOTAL"
    ]

    fig3 = px.bar(
        minerales,
        x="MINERAL",
        y="TOTAL",
        text="TOTAL",
        color="TOTAL",
        color_continuous_scale="Teal"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

with col4:

    st.subheader(
        "📍 Participación Territorial"
    )

    fig4 = px.pie(
        deptos,
        names="DEPARTAMENTO",
        values="CODIGO_EXPEDIENTE",
        hole=0.5
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# ==================================================
# HALLAZGOS
# ==================================================

st.divider()

depto_top = (
    df["DEPARTAMENTO"]
    .value_counts()
    .idxmax()
)

mineral_top = (
    df["MINERAL_NORMALIZADO"]
    .value_counts()
    .idxmax()
)

st.info(
    f"""
📌 Hallazgos ejecutivos

• Departamento líder: {depto_top}

• Mineral predominante: {mineral_top}

• Total expedientes: {df['CODIGO_EXPEDIENTE'].nunique():,}
"""
)

# ==================================================
# TABLA
# ==================================================

st.subheader(
    "📋 Vista rápida"
)

st.dataframe(
    df.head(20),
    use_container_width=True
)