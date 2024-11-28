import streamlit as st
import pandas as pd
import plotly.express as px

# Configurar la página
st.set_page_config(page_title="Dashboard SIKA", layout="wide")

# Estilo personalizado con CSS
st.markdown(
    """
    <style>
    /* Título personalizado */
    h1 {
        color: #D8282F;
    }
    
    /* Estilo para los botones */
    div.stButton > button, div.stDownloadButton > button {
        background-color: #D8282F; /* Rojo */
        color: FFC510; /* Amarillo */
        font-size: 18px;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
    }

    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background-color: #b71c1c; /* Rojo más oscuro */
    }

    /* Imagen personalizada */
    img {
        max-width: 200px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Imagen con tamaño específico
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/4/49/Sika_logo.svg", use_column_width=False)

# Título
st.title("Proyecciones en cada región")

# Cargar archivo CSV
@st.cache
def load_data():
    return pd.read_csv('bogota.csv')

data = load_data()

# Selector de Región
regiones = data['regional_txt'].unique()
region_seleccionada = st.selectbox("Selecciona una región", regiones)

# Botón "Consultar"
if st.button("Consultar"):
    # Filtrar datos por región
    datos_filtrados = data[data['regional_txt'] == region_seleccionada]

    # Agrupar datos por mes y SKU
    datos_filtrados['mes'] = pd.to_datetime(datos_filtrados['mes']).dt.strftime('%b')
    top_skus_mensuales = datos_filtrados.groupby(['mes', 'sku_cd'])['forecast_val'].sum().reset_index()
    top_skus_mensuales = top_skus_mensuales.sort_values(['mes', 'forecast_val'], ascending=[True, False]).groupby('mes').head(5)

    # Gráfica
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

    # Botón de descarga
    csv = datos_filtrados.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="DESCARGAR",
        data=csv,
        file_name=f'informe_{region_seleccionada}.csv',
        mime='text/csv',
    )
else:
    st.write("Presiona 'Consultar' para generar el informe.")
