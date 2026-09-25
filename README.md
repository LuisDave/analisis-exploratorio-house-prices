# Análisis exploratorio de precios de vivienda

Este repositorio utiliza un conjunto de datos sobre ventas de viviendas en Ames, Iowa, para desarrollar un flujo integral de análisis exploratorio. A partir de las características registradas para cada propiedad, se examinan la distribución de los precios, la integridad de la información y las variables que muestran mayor relación con el valor de venta.

El análisis se centra en `SalePrice`, el precio de venta en dólares. Antes de intentar construir un modelo predictivo, revisa la calidad de los datos, trata los valores faltantes de forma transparente y compara características físicas, calidad de construcción, antigüedad, ubicación y equipamiento. El resultado es un recorrido verificable desde los datos originales hasta hallazgos que puedan explicarse con claridad.

## Qué encontrarás aquí

El repositorio reúne una versión concreta y pequeña del flujo de trabajo:

- Un archivo de datos y su diccionario, para que cualquier persona parta de la misma información.
- Un script que deja los datos listos para analizarlos sin ocultar las decisiones tomadas.
- Un notebook donde se observan distribuciones, comparaciones y relaciones entre las características de las viviendas.

No es necesario conocer el proyecto original ni usar herramientas externas para repetir el análisis: se instala Python, se ejecuta el script y se abre el notebook.

## Preguntas que orientan el análisis

- ¿Qué variables numéricas y categóricas describen mejor las viviendas disponibles?
- ¿Dónde se concentran los valores faltantes y cómo cambia el conjunto de datos al tratarlos?
- ¿Qué características presentan mayor asociación con el precio de venta?
- ¿Cómo varía `SalePrice` entre zonas, tipos de vivienda y niveles de calidad?

## Datos

La fuente es el dataset [House Prices dataset](https://www.kaggle.com/datasets/lespin/house-prices-dataset), una distribución del conjunto **House Prices: Advanced Regression Techniques** de Kaggle.

El proyecto incluye los dos insumos utilizados en el análisis:

- `data/raw/house-prices/train.csv`: 1,460 viviendas y 81 variables.
- `data/raw/house-prices/data_description.txt`: diccionario técnico original de las variables.

`SalePrice` se usa como variable objetivo. `Id` se excluye de los predictores porque solo identifica registros. El dataset combina variables numéricas y categóricas; los faltantes numéricos se concentran principalmente en `LotFrontage`, `MasVnrArea` y `GarageYrBlt`.

## Flujo de preparación

El script de preparación sigue una secuencia documentada:

1. Lee los datos y reconoce tanto celdas vacías como la etiqueta `NA` como valores faltantes.
2. Separa `SalePrice` como variable dependiente (`y`) y conserva las demás características como predictores (`X`), excepto `Id`.
3. Imputa cada faltante de predictor numérico con la media calculada a partir de sus valores observados.
4. Conserva una versión con códigos enteros para las variables categóricas.
5. Genera una matriz alternativa con variables dummy para el análisis que no debe imponer orden entre categorías.
6. Guarda un resumen de lo que hizo para poder revisar o repetir cada paso.

Los archivos generados no se versionan: pueden recrearse en cualquier momento a partir del código y los datos fuente.

## Análisis realizado

El análisis se organiza en cuatro componentes:

1. **Perfilado de datos.** Cuenta registros, identifica el tipo de cada columna, busca duplicados y mide los valores faltantes.
2. **Preparación.** Completa faltantes numéricos con la media de su propia variable y transforma las categorías en códigos o columnas binarias (variables dummy).
3. **Estadística descriptiva.** Calcula medidas de tendencia central, dispersión, posición, sesgo y curtosis para entender el comportamiento de los precios y de los predictores relevantes.
4. **Exploración visual.** Usa histogramas para observar distribuciones, tablas de frecuencia para resumir categorías, diagramas de caja para comparar grupos y una matriz de correlación para detectar relaciones lineales con `SalePrice`.

El notebook contiene esta exploración paso a paso. El script de preparación, en cambio, deja los resultados intermedios listos para reutilizarlos en otros análisis o modelos sin tener que repetir manualmente la limpieza.

## Estructura del proyecto

```text
.
├── data/
│   ├── raw/house-prices/
│   └── processed/
├── src/
│   └── prepare_data.py
├── notebooks/
│   └── 01_house_prices_eda.ipynb
├── requirements.txt
└── README.md
```

## Instalación y ejecución local

Requiere Python 3.10 o posterior.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python src\prepare_data.py
python -m jupyter lab
```

Al abrir JupyterLab, ejecuta `notebooks/01_house_prices_eda.ipynb` desde la primera celda. El notebook encuentra automáticamente la raíz del proyecto tanto si se abre desde la carpeta principal como desde `notebooks/`.

La ejecución crea en `data/processed/` los siguientes artefactos:

- `dataset_profile.json`: dimensiones, tipos de variable y faltantes detectados.
- `numeric_means_used.csv`: medias empleadas en la imputación.
- `X_numeric_imputed.csv`: predictores tras la imputación numérica.
- `X_categorical_codes.csv`: predictores con categorías codificadas.
- `X_dummies.csv`: predictores con variables dummy.
- `y_sale_price.csv`: variable objetivo sin modificaciones.

## Alcance y consideraciones

Este repositorio documenta una práctica de análisis exploratorio, no una tasación inmobiliaria ni un modelo productivo. Los datos describen ventas históricas de Ames, Iowa, por lo que sus patrones no deben extrapolarse sin validación a otros mercados, periodos o contextos.

La imputación por media se conserva como una decisión metodológica simple y auditable. Para un modelo predictivo posterior, convendría comparar estrategias de imputación y analizar si la ausencia de datos contiene información relevante por sí misma.
