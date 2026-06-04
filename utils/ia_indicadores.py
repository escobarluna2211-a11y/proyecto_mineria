import pandas as pd


def generar_contexto(df_filtrado):

    total_registros = len(df_filtrado)

    total_expedientes = (
        df_filtrado["CODIGO_EXPEDIENTE"]
        .nunique()
    )

    total_departamentos = (
        df_filtrado["DEPARTAMENTO"]
        .nunique()
    )

    total_municipios = (
        df_filtrado["MUNICIPIO"]
        .nunique()
    )

    total_minerales = (
        df_filtrado["MINERAL_NORMALIZADO"]
        .nunique()
    )

    top_departamentos = (
        df_filtrado["DEPARTAMENTO"]
        .value_counts()
        .head(10)
        .to_dict()
    )

    top_municipios = (
        df_filtrado["MUNICIPIO"]
        .value_counts()
        .head(10)
        .to_dict()
    )

    top_minerales = (
        df_filtrado["MINERAL_NORMALIZADO"]
        .value_counts()
        .head(10)
        .to_dict()
    )

    top_categorias = (
        df_filtrado["CATEGORIAS"]
        .value_counts()
        .head(10)
        .to_dict()
    )

    return {

        "registros": total_registros,

        "expedientes": total_expedientes,

        "departamentos": total_departamentos,

        "municipios": total_municipios,

        "minerales": total_minerales,

        "top_departamentos": top_departamentos,

        "top_municipios": top_municipios,

        "top_minerales": top_minerales,

        "top_categorias": top_categorias
    }