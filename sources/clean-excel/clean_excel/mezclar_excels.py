import pandas as pd
# from logs import logger

def cargar_datos(path_df1: str, path_df2: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    '''
    Carga ambos Excel y limpieza:
    - Elimina columnas innecesarias en df2 y estandarizar fechas y nombres
    '''
    # logger.info(f'Cargando datos')
    df1 = pd.read_excel(path_df1)
    df2 = pd.read_excel(path_df2)

    columnas_a_eliminar = ["Nº Animales Actual", "Unnamed: 6", "Unnamed: 7"]
    df2 = df2.drop(columns=[col for col in columnas_a_eliminar if col in df2.columns])

    df1['fecha'] = pd.to_datetime(df1['fecha'], errors='coerce').dt.date
    df2['fecha'] = pd.to_datetime(df2['fecha'], errors='coerce').dt.date
    df1['granja'] = df1['granja'].astype(str).str.strip()
    df2['granja'] = df2['granja'].astype(str).str.strip()

    return df1, df2

def combinar_datos(df1: pd.DataFrame, df2: pd.DataFrame, ruta_salida: str) -> None:
    '''
    Combinar DataFrames por 'fecha' y 'granja', ordena y exporta a Excel.
    '''
    # logger.info(f'Combinando dataframes')
    df_merged = pd.merge(df1, df2, on=['fecha', 'granja'], how='left')
    df_merged.sort_values(by=["granja", "fecha"], inplace=True)
    df_merged.to_excel(ruta_salida, index=False)

def exportar_datos(path_df1: str, path_df2: str, ruta_salida: str) -> None:
    '''
    Orquesta el proceso de carga, limpieza, combinación y exportación de los datos.
    '''
    
    df1, df2 = cargar_datos(path_df1, path_df2)
    combinar_datos(df1, df2, ruta_salida)
    # logger.info(f'Generando nuevo dataframe')
