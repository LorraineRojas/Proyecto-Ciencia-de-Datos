import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import calendar

# Configurar la página
st.set_page_config(page_title="Dashboard SIKA", layout="wide")

# Estilo personalizado con CSS
st.markdown(
    """
    <style>
    h1 {
        color: #D8282F;
    }
    div.stButton > button, div.stDownloadButton > button {
        background-color: #D8282F;
        color: #FFC510;
        font-size: 18px;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background-color: #b71c1c;
        color: #FFC510;
    }
    img {
        max-width: 200px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Imagen con tamaño específico
st.sidebar.image("logoSika.png", use_column_width=False)

st.title("Proyecciones en cada región")

@st.cache
def load_data():
    return pd.read_csv('bogota.csv')

data = load_data()

# Creación de columnas para los selectores
col1, col2 = st.columns(2)

with col1:
    regiones = data['regional_txt'].unique()
    region_seleccionada = st.selectbox("Selecciona una región", regiones)

with col2:
    skus = ["Total"] + list(data['sku_cd'].unique())
    sku_seleccionado = st.selectbox("Selecciona un SKU", skus)

# Definir mes actual y calcular mes correspondiente
mes_actual = datetime.now().month

def calcular_mes(index):
    mes = (mes_actual + index + 1)
    return calendar.month_abbr[mes] 

if st.button("CONSULTAR"):
    datos_filtrados = data[data['regional_txt'] == region_seleccionada].copy()
    datos_filtrados['mes'] = datos_filtrados.index.map(calcular_mes)

    if sku_seleccionado == "Total":
        # Agrupar por mes y sumar valores para todos los SKUs
        datos_agrupados = datos_filtrados.groupby('mes')['forecast_val'].sum().reset_index()
        titulo_grafico = f"Proyección Total de Ventas por Mes - Región: {region_seleccionada}"
    else:
        # Filtrar por SKU seleccionado
        datos_agrupados = datos_filtrados[datos_filtrados['sku_cd'] == sku_seleccionado].groupby('mes')['forecast_val'].sum().reset_index()
        titulo_grafico = f"Proyección de Ventas del SKU {sku_seleccionado} por Mes - Región: {region_seleccionada}"

    # Crear gráfico de serie de tiempo
    fig = px.line(
        datos_agrupados,
        x='mes',
        y='forecast_val',
        title=titulo_grafico,
        labels={'mes': 'Mes', 'forecast_val': 'Proyección'},
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

    # Botón para descargar el informe
    csv = datos_filtrados.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="DESCARGAR",
        data=csv,
        file_name=f'informe_{region_seleccionada}_{sku_seleccionado}.csv',
        mime='text/csv',
    )
else:
    st.write("Selecciona una región y un SKU, luego presiona 'Consultar' para generar el informe.")
