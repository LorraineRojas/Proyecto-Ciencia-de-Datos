import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar el archivo CSV
@st.cache
def load_data():
    return pd.read_csv('bogota.csv')

data = load_data()

# Título del Dashboard
st.title("Dashboard de Forecast por Región y SKU")

# Selector de Región
regiones = data['regional_txt'].unique()
region_seleccionada = st.selectbox("Selecciona una región:", regiones)

# Filtrar los datos por la región seleccionada
datos_filtrados = data[data['regional_txt'] == region_seleccionada]

# Calcular el top 5 de SKU según su forecast
top_skus = (datos_filtrados.groupby('sku_cd')['forecast_val']
            .sum()
            .nlargest(5)
            .reset_index())

# Gráfica del top 5 SKU
fig = px.bar(top_skus, x='sku_cd', y='forecast_val', title=f"Top 5 SKU en {region_seleccionada}", labels={'forecast_val': 'Forecast', 'sku_cd': 'SKU'})
st.plotly_chart(fig)

# Botón para descargar el informe
@st.cache
def convertir_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convertir_csv(datos_filtrados)
st.download_button(
    label="Descargar informe completo",
    data=csv,
    file_name=f'informe_{region_seleccionada}.csv',
    mime='text/csv',
)
