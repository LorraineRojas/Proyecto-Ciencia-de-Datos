import streamlit as st
import pandas as pd
import plotly.express as px

# Título y logo
st.set_page_config(page_title="Dashboard SIKA", layout="wide")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/4/49/Sika_logo.svg", use_column_width=True)

st.title("Proyección por Región y SKU")

# Cargar archivo CSV preexistente
@st.cache
def load_data():
    return pd.read_csv('bogota.csv')

# Botón "Consultar"
if st.button("Consultar"):
    data = load_data()

    # Selector de Región
    regiones = data['regional_txt'].unique()
    region_seleccionada = st.selectbox("Región", regiones)

    # Filtrar datos por región
    datos_filtrados = data[data['regional_txt'] == region_seleccionada]

    # Top 5 de SKU según forecast
    top_skus = datos_filtrados.groupby('sku_cd')['forecast_val'].sum().nlargest(5).reset_index()

    # Gráfica
    fig = px.bar(top_skus, x='sku_cd', y='forecast_val', 
                 title=f"Top 5 de productos vendidos - {region_seleccionada}", 
                 labels={'forecast_val': 'Proyección', 'sku_cd': 'Productos x mes'})
    st.plotly_chart(fig, use_container_width=True)

    # Descargar informe
    csv = datos_filtrados.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="DESCARGAR",
        data=csv,
        file_name=f'informe_{region_seleccionada}.csv',
        mime='text/csv',
    )
else:
    st.write("Presiona 'Consultar' para generar el informe.")