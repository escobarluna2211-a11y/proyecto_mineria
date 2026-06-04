from groq import Groq


def generar_informe_groq(
    api_key,
    contexto,
    tipo_informe
):

    client = Groq(
        api_key=api_key
    )

    prompt = f"""
Eres un consultor senior del sector minero colombiano.

TIPO DE INFORME:
{tipo_informe}

INDICADORES:

Registros:
{contexto["registros"]}

Expedientes:
{contexto["expedientes"]}

Departamentos:
{contexto["departamentos"]}

Municipios:
{contexto["municipios"]}

Minerales:
{contexto["minerales"]}

TOP DEPARTAMENTOS:
{contexto["top_departamentos"]}

TOP MUNICIPIOS:
{contexto["top_municipios"]}

TOP MINERALES:
{contexto["top_minerales"]}

TOP CATEGORIAS:
{contexto["top_categorias"]}

Genera un informe profesional.

Estructura:

1. Resumen Ejecutivo

2. Hallazgos Clave

3. Análisis Territorial

4. Análisis Minero

5. Riesgos

6. Oportunidades

7. Recomendaciones

8. Conclusiones

Usa lenguaje profesional.
"""

    respuesta = (
        client.chat.completions.create(
            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.3
        )
    )

    return (
        respuesta
        .choices[0]
        .message
        .content
    )