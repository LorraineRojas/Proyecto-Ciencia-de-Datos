MINE-4101: Ciencia de Datos Aplicada Entrega Final Proyecto Sika

Integrantes:
Alvaro Andres Castiblanco 
Camilo Andrés Morrillo Cervantes
Lorraine Jazlady Rojas Parra
Vladimir Emil Rueda Gómez
Instrucciones para ejecutar el proyecto
ejecutar en el siguiente orden:
EN el archivo requirements se enceuntran todos los requisitos para la ejcución del notebook y streamlit
En el notebook eda_proy_cda.ipynb se encuentra todo el EDA de los datos.
  - Este notebok contiene el analisis exploratiro, identificación de productos y regionales.
  - generación de matriz de calor, validación de productos tops de ventas por regional.
En el notebook models.ipynb se encuentra la creación y pruebas de los modelos.  
  -se crean 3 modelos para evalución:
    - Modelo de series de tiempo SARIMA
    - Modelo de Random Forest
    - Red neuronal recurrente LSTM.

se evaluan los modelos y con los datos obtenidos se identifica que para la aprticularidad de los productos no se puede generar un unico modelo para todos los productos.
Teniendo en cuenta la matriz de calor se evidencia que el top de ventas por cada regional tiene porductos diferentes se reliza una evaluación  de los modelos sote el top 5 de cada regional.
El despliegue del entorno se realiza en Streamlit Community Cloud 
El Link desplegado es el siguiente https://proyecto-ciencia-de-datos-zkvx9daf9xp7znownbpcmv.streamlit.app/
