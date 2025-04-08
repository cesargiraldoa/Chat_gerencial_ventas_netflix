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
st.markdown("<h1 style='color:#FF4B4B;'>🎮 Chat Gerencial Estilo Netflix - Modo Oscuro</h1>", unsafe_allow_html=True)

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
tab_inicio, tab_inicio_alternativo, tab_productos, tab_sucursales, tab_tendencias, tab_chat = st.tabs(["🏠 Inicio", "🧠 Inicio Alternativo", "📦 Productos", "🏢 Sucursales", "📈 Tendencias", "💬 Chat Gerencial"])

with tab_inicio:
    st.markdown("## 🎮 ¡Bienvenido al Chat Gerencial!")
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

    top_producto = data.groupby("producto")['ventas'].sum().idxmax()
    top_sucursal = data.groupby("sucursal")['ventas'].sum().idxmax()
    top_vendedor = data.groupby("vendedor")['ventas'].sum().idxmax()

    st.markdown("### 🔝 Resúmenes:")
    col1, col2, col3 = st.columns(3)
    col1.success(f"Producto Top: {top_producto}")
    col2.warning(f"Sucursal Líder: {top_sucursal}")
    col3.info(f"Vendedor Destacado: {top_vendedor}")

    fig_bar = px.bar(data.groupby("producto")["ventas"].sum().reset_index(), x="producto", y="ventas", title="Ventas Totales por Producto", color="producto")
    st.plotly_chart(fig_bar, use_container_width=True)

with tab_productos:
    st.markdown("## 📦 Ventas por Producto")
    filtro = st.selectbox("Filtrar por sucursal:", ["Todas"] + sorted(data['sucursal'].unique()))
    data_filtrada = data if filtro == "Todas" else data[data['sucursal'] == filtro]
    resumen_productos = data_filtrada.groupby("producto")["ventas"].sum().reset_index()
    fig_productos = px.bar(resumen_productos, x="producto", y="ventas", title="Ventas por Producto", color="producto")
    st.plotly_chart(fig_productos, use_container_width=True)

with tab_sucursales:
    st.markdown("## 🏢 Ranking de Sucursales")
    filtro = st.selectbox("Filtrar por producto:", ["Todos"] + sorted(data['producto'].unique()))
    data_filtrada = data if filtro == "Todos" else data[data['producto'] == filtro]
    resumen_suc = data_filtrada.groupby("sucursal")["ventas"].sum().sort_values(ascending=False).reset_index()
    for i, row in resumen_suc.iterrows():
        st.markdown(f"### {i+1}. {row['sucursal']} - 💰 Ventas: ${row['ventas']:,.0f}")

with tab_tendencias:
    st.markdown("## 📈 Tendencia Mensual")
    data_tend = data.copy()
    data_tend["mes"] = pd.to_datetime(data_tend["fecha"]).dt.to_period("M").dt.to_timestamp()
    ventas_mes = data_tend.groupby("mes")["ventas"].sum().reset_index()
    fig_tendencia = px.line(ventas_mes, x="mes", y="ventas", title="Evolución de Ventas por Mes")
    st.plotly_chart(fig_tendencia, use_container_width=True)

with tab_chat:
    st.markdown("## 💬 Chat Gerencial")
    pregunta = st.text_input("Escribe tu pregunta:", "¿Cuál es el producto más vendido?")
    if "producto" in pregunta.lower():
        top = data.groupby("producto")["ventas"].sum().idxmax()
        total = data.groupby("producto")["ventas"].sum().max()
        st.success(f"El producto más vendido es **{top}** con un total de ${total:,.0f} en ventas.")
        fig = px.pie(data.groupby("producto")["ventas"].sum().reset_index(), names="producto", values="ventas", title="Distribución de Ventas")
        st.plotly_chart(fig, use_container_width=True)
    elif "vendedor" in pregunta.lower():
        top = data.groupby("vendedor")["ventas"].sum().idxmax()
        total = data.groupby("vendedor")["ventas"].sum().max()
        st.success(f"El vendedor con más ventas es **{top}** con un total de ${total:,.0f}.")
        fig = px.bar(data.groupby("vendedor")["ventas"].sum().reset_index(), x="vendedor", y="ventas", title="Ventas por Vendedor")
        st.plotly_chart(fig, use_container_width=True)
    elif "sucursal" in pregunta.lower():
        top = data.groupby("sucursal")["ventas"].sum().idxmax()
        total = data.groupby("sucursal")["ventas"].sum().max()
        st.success(f"La sucursal con más ventas es **{top}** con un total de ${total:,.0f}.")
        fig = px.bar(data.groupby("sucursal")["ventas"].sum().reset_index(), x="sucursal", y="ventas", title="Ventas por Sucursal")
        st.plotly_chart(fig, use_container_width=True)
    elif "promedio" in pregunta.lower():
        promedio = data['ventas'].mean()
        st.info(f"El promedio de ventas por registro es de ${promedio:,.0f}.")
        promedio_mes = data.groupby(data['fecha'].dt.to_period("M"))['ventas'].mean().reset_index()
        fig = px.bar(promedio_mes, x="fecha", y="ventas", title="Promedio de Ventas por Mes")
        st.plotly_chart(fig, use_container_width=True)
    elif "cumplimiento" in pregunta.lower():
        data['cumplimiento'] = data['ventas'] / data['meta'] * 100
        promedio = data['cumplimiento'].mean()
        st.success(f"El cumplimiento promedio general es de {promedio:.2f}%")
        fig = px.box(data, x="sucursal", y="cumplimiento", color="sucursal", title="Distribución de Cumplimiento por Sucursal")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Lo siento, aún no tengo una respuesta para esa pregunta.")
