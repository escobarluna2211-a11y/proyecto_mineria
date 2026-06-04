import plotly.express as px


def grafico_departamentos(df):

    top = (
        df.groupby("DEPARTAMENTO")
        ["CODIGO_EXPEDIENTE"]
        .nunique()
        .reset_index()
        .sort_values(
            "CODIGO_EXPEDIENTE",
            ascending=False
        )
        .head(15)
    )

    fig = px.bar(
        top,
        x="CODIGO_EXPEDIENTE",
        y="DEPARTAMENTO",
        orientation="h",
        title="Top Departamentos"
    )

    return fig