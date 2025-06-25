from clean_excel.limpieza_excel import procesar_funciones
from clean_excel.mezclar_excels import exportar_datos
from clean_excel.limpieza_excel2 import procesado_completo

path_entrada = "data/datos.xlsx"
path_salida = "data/resultado_1.xlsx"
path_externo = "data/datos_numero_gallinas_2.xlsx"

procesar_funciones(path_entrada, path_salida)

exportar_datos(path_salida, path_externo, "data/excel_combinado_3.xlsx")

procesado_completo("data/excel_combinado_3.xlsx", path_externo, "data/excel_limpio_4.xlsx", "data/resultado.csv")