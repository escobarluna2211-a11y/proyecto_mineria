def total_expedientes(df):
    return df["CODIGO_EXPEDIENTE"].nunique()


def total_departamentos(df):
    return df["DEPARTAMENTO"].nunique()


def total_municipios(df):
    return df["MUNICIPIO"].nunique()


def total_minerales(df):
    return df["MINERAL_NORMALIZADO"].nunique()