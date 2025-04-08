import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from io import BytesIO
from reportlab.pdfgen import canvas
from datetime import datetime
import os
import numpy as np

st.set_page_config(layout="wide", page_title="Chat Gerencial - Modo Oscuro", page_icon="🔟")

# Logo y título
logo = Image.open("assets/logo.png")
st.image(logo, width=180)
st.markdown("<h1 style='color:#FF4B4B;'>🎬 Chat Gerencial Estilo Netflix - Modo Oscuro</h1>", unsafe_allow_html=True)

# Crear datos de ejemplo más realistas
np.random.seed(42)
fechas = pd.date_range(start="2025-01-01", end="2025-03-31", freq="D")
sucursales = ["Barranquilla", "Bogotá", "Medellín"]
productos = ["Cepillo", "Crema", "Enjuague", "Hilo dental", "Enjuague premium"]
vendedores = ["Ana", "Luis", "Carlos", "María", "Sofía"]

data = []
for fecha in fechas:
    for sucursal in sucursales:
        for producto in productos:
            vendedor = np.random.choice(vendedores)
            venta = np.random.randint(1000, 10000)
            meta = np.random.randint(5000, 9000)
            data.append([fecha, sucursal, producto, vendedor, venta, meta])

ejemplo = pd.DataFrame(data, columns=["fecha", "sucursal", "producto", "vendedor", "ventas", "meta"])
os.makedirs("data", exist_ok=True)
ejemplo.to_excel("data/ventas_ejemplo.xlsx", index=False)

# Cargar datos
data = pd.read_excel("data/ventas_ejemplo.xlsx")

# Filtro por fechas
fecha_inicio = st.date_input("🗓️ Fecha inicial", value=pd.to_datetime("2025-01-01"))
fecha_fin = st.date_input("🗓️ Fecha final", value=pd.to_datetime("2025-12-31"))
data = data[(data['fecha'] >= pd.to_datetime(fecha_inicio)) & (data['fecha'] <= pd.to_datetime(fecha_fin))]

# Tabs
_, tab_inicio, tab_inicio_alternativo, tab_productos, tab_sucursales, tab_tendencias, tab_chat = st.tabs(["🏠 Inicio", "🧠 Inicio Alternativo", "📦 Productos", "🏢 Sucursales", "📈 Tendencias", "💬 Chat Gerencial"])

with tab_inicio:
    st.markdown("## 🎬 ¡Bienvenido al Chat Gerencial!")
    st.markdown("Este panel te permite visualizar y analizar el desempeño de ventas en tiempo real con una experiencia tipo Netflix. Usa las pestañas para explorar productos, sucursales, tendencias y hacer preguntas al asistente inteligente.")

    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Productos Activos", data['producto'].nunique())
    col2.metric("🏢 Sucursales", data['sucursal'].nunique())
    col3.metric("🧑‍💼 Vendedores", data['vendedor'].nunique())

    st.markdown("---")
    st.markdown("### 📈 Vista rápida: Ventas diarias recientes")
    ultimos_dias = data[data['fecha'] > data['fecha'].max() - pd.Timedelta(days=7)]
    ventas_dia = ultimos_dias.groupby('fecha')['ventas'].sum().reset_index()
    fig_inicio = px.area(ventas_dia, x="fecha", y="ventas", title="Ventas en los últimos 7 días", color_discrete_sequence=["#00FFAA"])
    st.plotly_chart(fig_inicio, use_container_width=True)

with tab_inicio_alternativo:
    st.markdown("## 🧠 Análisis Rápido y Destacados")
    st.markdown("Conoce de un vistazo los elementos clave destacados:")

    top_producto = data.groupby("producto")["ventas"].sum().idxmax()
    top_sucursal = data.groupby("sucursal")["ventas"].sum().idxmax()
    top_vendedor = data.groupby("vendedor")["ventas"].sum().idxmax()

    st.markdown("### 🔝 Resúmenes:")
    col1, col2, col3 = st.columns(3)
    col1.success(f"Producto Top: {top_producto}")
    col2.warning(f"Sucursal Líder: {top_sucursal}")
    col3.info(f"Vendedor Destacado: {top_vendedor}")

    fig_bar = px.bar(data.groupby("producto")["ventas"].sum().reset_index(), x="producto", y="ventas", title="Ventas Totales por Producto", color="producto")
    st.plotly_chart(fig_bar, use_container_width=True)

# El resto del código permanece igual
