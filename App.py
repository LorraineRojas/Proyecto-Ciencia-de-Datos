import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Configurar la página
st.set_page_config(page_title="Dashboard SIKA", layout="wide")

# Estilo personalizado con CSS
st.markdown(
    """
    <style>
    h1 {
        color: #d32f2f;
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

# Selector de Región
regiones = data['regional_txt'].unique()
region_seleccionada = st.selectbox("Selecciona una región", regiones)

# Definir mes actual y calcular mes correspondiente
mes_actual = datetime.now().replace(day=1)  # Primer día del mes actual
data['mes'] = data.index.map(lambda x: (mes_actual + timedelta(days=x*30)).strftime('%b'))

if st.button("Consultar"):
    datos_filtrados = data[data['regional_txt'] == region_seleccionada]

    # Agrupar por mes y SKU, obteniendo el top 5
    top_skus_mensuales = datos_filtrados.groupby(['mes', 'sku_cd'])['forecast_val'].sum().reset_index()
    top_skus_mensuales = top_skus_mensuales.sort_values(['mes', 'forecast_val'], ascending=[True, False]).groupby('mes').head(5)

    fig = px.bar(
        top_skus_mensuales,
        x='mes',
        y='forecast_val',
        color='sku_cd',
        title=f"Top 5 de productos vendidos por mes - Región: {region_seleccionada}",
        labels={'mes': 'Mes', 'forecast_val': 'Proyección', 'sku_cd': 'SKU'},
        barmode='group'
    )
    st.plotly_chart(fig, use_container_width=True)

    csv = datos_filtrados.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="DESCARGAR",
        data=csv,
        file_name=f'informe_{region_seleccionada}.csv',
        mime='text/csv',
    )
else:
    st.write("Presiona 'Consultar' para generar el informe.")
