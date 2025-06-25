import pandas as pd
# from logs import logger

def cargar_columnas_estandarizadas(archivo):
    '''
    Carga y estandariza los nombres de columnas del archivo Excel.
    Elimina espacios pasando todo a minúsculas, y renombra columnas. 
    '''
    
    columnas = archivo.parse(archivo.sheet_names[0]).columns.str.strip().str.lower()
    columnas = columnas.str.replace('temp 9:00', 'temp_9', regex=False)
    columnas = columnas.str.replace('temp 12.00', 'temp_12', regex=False)
    return columnas

def cargar_datos_excel(ruta_excel: str) -> pd.DataFrame:
    '''
    Carga un archivo Excel con múltiples hojas, asignando nombres de columnas estandarizados
    y concatenando todas las hojas en un único DataFrame.
    '''
    
    # logger.info(f'Leyendo el archivo Excel de esta ruta: {ruta_excel}')
    # logger.warning(f'Leyendo el archivo Excel de esta ruta: {ruta_excel}')
    
    archivo = pd.ExcelFile(ruta_excel)
    columnas = cargar_columnas_estandarizadas(archivo)
    dfs = []
    for hoja in archivo.sheet_names:
        df = archivo.parse(hoja, header=None)
        df.columns = columnas
        dfs.append(df)
    df_final = pd.concat(dfs, ignore_index=True)
    return df_final

def limpieza_basica(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Limpieza básica:
    - Convierte fechas a formato estándar
    - Elimina encabezados duplicados y columnas vacías
    - Ordena por fecha y elimina columnas innecesarias
    '''
    
    # logger.info(f'Limpiando el archivo Excel')
    
    df = df[df["fecha"] != "fecha"]
    df["fecha"] = pd.to_datetime(df["fecha"], format="%d-%m-%Y", errors="coerce")
    df["fecha"] = df["fecha"].dt.strftime("%Y-%m-%d")
    df = df.dropna(subset=["fecha"])
    df = df.loc[:, df.columns.str.strip() != '']
    df = df.sort_values(by="fecha")
    columnas_a_eliminar = ['unnamed: 19', 'unnamed: 20', 'unnamed: 21', 'unnamed: 22', 'unnamed: 23', 'observaciones del dia']
    df = df.drop(columns=[col for col in columnas_a_eliminar if col in df.columns])
    
    return df

def limpiar_columnas_texto(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Limpia las columnas de texto:
    - Extrae primer nombre en 'granjero'
    - Aplica capitalización a nombres y granjas
    - Sustituye nulos y elimina caracteres especiales en 'granjero'
    '''
    
    df['granja'] = df['granja'].str.title()
    df['granjero'] = df['granjero'].str.split().str[0]
    df['granjero'] = df['granjero'].str.title()
    df["granjero"] = df["granjero"].fillna('sin asignar')
    df["granjero"] = df["granjero"].str.replace(r'[^\w\s]', '', regex=True)
    
    return df

def limpiar_columna_corte_pienso(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Normaliza la columna 'corte de pienso', dejando solo valores booleanos equivalentes a 'si' o 'no'.
    '''
    
    df['corte de pienso'] = df['corte de pienso'].str.lower().isin(["si", "no"])
    
    return df

def limpieza_tratamientos(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Limpia y transforma tratamientos:
    - Elimina columnas 
    - Normaliza tratamiento de agua y piojos
    - Limpia 'tratamientos'
    '''
    
    # logger.info(f'Limpiando columna de tratamientos')
    df = df.drop(columns=['introduce solo agua calculo pienso automático'])
    df = df[df["tratamiento piojos"] != 6910.0]
    
    df["tratamiento agua"] = df["tratamiento agua"].str.replace("\n", " ", regex=False)
    df["tratamiento agua"] = df["tratamiento agua"].str.split().str[0]
    df = df[df["tratamiento agua"] != "SI"]
    
    df["tratamiento agua"] = df["tratamiento agua"].replace("NO", "NADA")
    df["tratamiento agua"] = pd.to_numeric(df["tratamiento agua"], errors="coerce")
    df.loc[df["tratamiento agua"] < 0, "tratamiento agua"] = 0
    
    df["tratamientos"] = df["tratamientos"].str.lower()
    df["tratamientos"] = df["tratamientos"].str.replace(r"\(\d+\)", "", regex=True)
    
    return df

def limpiar_columnas_numericas(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Limpia columnas numéricas:
    - Rellena y filtra nulos
    - Convierte datos a tipo adecuado
    - Elimina  no válidos o extremos
    '''
    
    # logger.info(f'Limpiando columnas numéricas')
    df["bajas"] = df["bajas"].fillna(0)
    df["bajas"] = df["bajas"].apply(lambda x: max(0, int(x)) if isinstance(x, (int, float)) and not pd.isna(x) and x != '.0' else x)
    
    df = df.dropna(subset=["agua", "pienso"])
    df.loc[:, "temp_9"] = pd.to_numeric(df["temp_9"], errors='coerce')
    
    df = df.loc[df["temp_9"].notna()]
    df = df.loc[df["temp_9"] <= 43]
    
    df["temp_9"] = pd.to_numeric(df["temp_9"], errors='coerce').fillna(0).astype(int)
    df.loc[:, "temp_12"] = pd.to_numeric(df["temp_12"], errors='coerce')
    
    df = df.loc[df["temp_12"].notna()]
    df = df.loc[df["temp_12"] <= 43]
    df["temp_12"] = pd.to_numeric(df["temp_12"], errors='coerce').fillna(0).round().astype(int)
    
    return df

def crear_columna_no_suelo(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Crea una nueva columna 'no_suelo' a partir de la diferencia entre 'totales' y 'suelo'.
    Ajusta valores negativos y reorganiza la posición de las columnas.
    '''
    # logger.info('Creando columna no_suelo')
    df["totales"] = pd.to_numeric(df["totales"], errors="coerce")
    df["suelo"] = pd.to_numeric(df["suelo"], errors="coerce").fillna(0).astype(int)
    df["no_suelo"] = (df["totales"].fillna(0) - df["suelo"]).astype(int)
    
    df.loc[df["no_suelo"] < 0, "no_suelo"] = df["totales"]
    columnas = list(df.columns)
    
    suelo_idx = columnas.index('suelo')
    no_suelo_idx = columnas.index('no_suelo')
    
    columnas.insert(suelo_idx + 1, columnas.pop(no_suelo_idx))
    df = df[columnas]
    
    return df

def procesar_funciones(path_entrada: str, path_salida: str) -> None:
    '''
    Ejecuta todas las funciones anteriores pasándole la ruta del archivo con el origen de los datos junto con la ruta y nombre del nuevo archivo.
    '''

    df = cargar_datos_excel(path_entrada)
    df = limpieza_basica(df)
    df = limpiar_columnas_texto(df)
    df = limpiar_columna_corte_pienso(df)
    df = limpieza_tratamientos(df)
    df = limpiar_columnas_numericas(df)
    df = crear_columna_no_suelo(df)
    # logger.info(f'Guardando el archivo')
    df.to_excel(path_salida, index=False)

