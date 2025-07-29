# P-PAZ-012025-P.Vilane
Limpieza de datos de P. Vilane para su integración en BI

Dentro de la carpeta data están los nuevos archivos .xlsx que se van generando. El principal es el archivo datos.xlsx que es donde están los datos originales.

Se crean tres archivos de python en la carpeta 'sources/clean-excel/clean_excel' con funciones que van modificando otros archivos y generando nuevos:
  - El primer archivo es 'limpieza_excel'.py que coge datos.xlsx y devuelve 'resultado_1'
  - El segundo archivo es 'mezclar_excels' que coge el 'resultado_1' y lo junta con 'datos_numeros_gallinas_2' que es un excel aparte con otra información, a la vez que limpia cosas. Como resultante sale 'excel_combinado_3'.
  - El tercer archivo es 'limpieza_excel2' que coge 'excel_combinado_3' y lo modifica hasta que está listo para ser pasado a PowerBI y presentado con el nombre 'excel_limpio_4'.


📂 Estructura principal
data/

  - Contiene archivos .xlsx generados en el proceso.

  - Archivo principal: datos.xlsx (datos originales)

  - Otros archivos auxiliares generados en cada etapa del flujo de limpieza.

sources/clean-excel/clean_excel/

Contiene scripts de Python que procesan y transforman los archivos .xlsx en varias fases:
⚙️ Flujo de procesamiento de datos

  - limpieza_excel.py

     - Entrada: data/datos.xlsx

     - Salida: resultado_1.xlsx

     - Objetivo: Limpieza inicial del archivo original.

  - mezclar_excels.py

     - Entradas:

        - resultado_1.xlsx (generado previamente)

        - datos_numeros_gallinas_2.xlsx (archivo auxiliar con más info)

      - Salida: excel_combinado_3.xlsx

        - Objetivo: Fusión y limpieza conjunta de datos.

    limpieza_excel2.py

     - Entrada: excel_combinado_3.xlsx

     - Salida: excel_limpio_4.xlsx

     - Objetivo: Limpieza final y formato adecuado para Power BI.
  

📊 Resultado final

   + Archivo final: resultado.csv

   + Uso: Importado directamente en Power BI para visualización.
