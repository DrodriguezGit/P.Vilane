import pandas as pd
import numpy as np
# from logs import logger

def cargar_datos(ruta_excel_combinado: str) -> pd.DataFrame:
    '''
    Carga el archivo Excel combinado, renombra columnas y convierte tipos básicos.
    '''
    # logger.info(f'Cargando dataframes y modificando')
    df = pd.read_excel(ruta_excel_combinado)
    df = df.rename(columns={"Números incial de animales": "n_animales"})
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df["n_animales"] = pd.to_numeric(df["n_animales"], errors="coerce")
    df["bajas"] = pd.to_numeric(df["bajas"], errors="coerce").fillna(0)
    return df


def completar_animales(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Completa la columna n_animales restando el número anterior de animales al número anterior de bajas.
    '''
    
    df = df.sort_values(by=["granja", "fecha"])
    for granja in df["granja"].unique():
        df_granja = df[df["granja"] == granja]
        idxs = df_granja.index.tolist()
        last_value = None
        for i, idx in enumerate(idxs):
            if not np.isnan(df.at[idx, "n_animales"]):
                last_value = df.at[idx, "n_animales"]
            elif last_value is not None and i > 0:
                prev_idx = idxs[i - 1]
                bajas_prev = df.at[prev_idx, "bajas"]
                last_value -= bajas_prev
                df.at[idx, "n_animales"] = last_value
    return df.dropna(subset=["n_animales"])

def limpiar_valores(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Corrige tipos, limpia valores negativos y elimina outliers.
    '''
    
    df = df.drop(columns=["Fecha de Fin de Producción", "Semanas de Vida Inicial"], errors="ignore")
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    for col in ["agua", "pienso", "bajas"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df.loc[df[col] < 0, col] = 0
    df["totales"] = pd.to_numeric(df["totales"], errors="coerce")
    df["entrada de pienso"] = pd.to_numeric(df["entrada de pienso"], errors="coerce")
    df = df[
        (df["pienso"] <= 7000) &
        (df["totales"] <= 70000) &
        (df["entrada de pienso"].between(0, 60000))
    ]
    df = df.sort_values(by=["granja", "fecha"])
    return df

def agregar_semana_vida(df: pd.DataFrame, ruta_entradas: str) -> pd.DataFrame:
    '''
    Calcula y agrega la semana de vida según fechas de entrada.
    '''
    
    # logger.info(f'Agregando y completando columna de semanas de vida')
    df_entradas = pd.read_excel(ruta_entradas)
    df_entradas["fecha"] = pd.to_datetime(df_entradas["fecha"], errors="coerce")
    df_entradas["granja"] = df_entradas["granja"].astype(str).str.strip()
    df_entradas = df_entradas.rename(columns={
        "Números incial de animales": "n_animales_entrada",
        "Semanas de Vida Inicial": "sem_vida_inicial"
    })[["granja", "fecha", "n_animales_entrada", "sem_vida_inicial"]]
    df_entradas = df_entradas.dropna(subset=["sem_vida_inicial"])

    df["semana_vida"] = pd.NA
    for granja in df["granja"].unique():
        df_granja = df[df["granja"] == granja].copy()
        entradas_granja = df_entradas[df_entradas["granja"] == granja].sort_values("fecha")
        for i, entrada in entradas_granja.iterrows():
            fecha_inicio = entrada["fecha"]
            semana_inicial = int(entrada["sem_vida_inicial"])
            fecha_fin = entradas_granja.iloc[i + 1]["fecha"] if i < len(entradas_granja) - 1 else df_granja["fecha"].max() + pd.Timedelta(days=1)
            mask = (df["granja"] == granja) & (df["fecha"] >= fecha_inicio) & (df["fecha"] < fecha_fin)
            semanas_vida = df.loc[mask, "fecha"].apply(lambda f: semana_inicial + ((f - fecha_inicio).days // 7))
            df.loc[mask, "semana_vida"] = semanas_vida
    return df

def procesado_completo(path_combinado: str, path_entradas: str, path_salida: str, path_csv: str) -> None:
    '''
    Ejecuta la limpieza y guarda el resultado.
    '''
    
    df = cargar_datos(path_combinado)
    df = completar_animales(df)
    df = limpiar_valores(df)
    df = agregar_semana_vida(df, path_entradas)
    # logger.info(f'Generando archivo csv')
    df.to_excel(path_salida, index=False)
    df.to_csv(path_csv, index=False, sep=";", decimal=",")

