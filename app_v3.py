import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from io import BytesIO
from datetime import datetime
import os
import numpy as np
import time

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

# Generar alerta por bajo rendimiento
data['cumplimiento'] = data['ventas'] / data['meta'] * 100
alertas = data.groupby('sucursal')['cumplimiento'].mean().reset_index()
alertas_bajas = alertas[alertas['cumplimiento'] < 80]
if not alertas_bajas.empty:
    st.error("⚠️ Alerta: Las siguientes sucursales están por debajo del 80% de cumplimiento:")
    for _, row in alertas_bajas.iterrows():
        st.write(f"🔴 {row['sucursal']}: {row['cumplimiento']:.2f}%")

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

# ... (otras pestañas sin cambio)

with tab_chat:
    st.markdown("## 💬 Chat Gerencial")
    pregunta = st.text_input("Escribe tu pregunta:", "¿Cuál es el producto más vendido?")

    respuesta = ""
    fig = None

    if "producto" in pregunta.lower():
        top = data.groupby("producto")["ventas"].sum().idxmax()
        total = data.groupby("producto")["ventas"].sum().max()
        respuesta = f"El producto más vendido es **{top}** con un total de ${total:,.0f} en ventas."
        fig = px.pie(data.groupby("producto")["ventas"].sum().reset_index(), names="producto", values="ventas", title="Distribución de Ventas")
    elif "vendedor" in pregunta.lower():
        top = data.groupby("vendedor")["ventas"].sum().idxmax()
        total = data.groupby("vendedor")["ventas"].sum().max()
        respuesta = f"El vendedor con más ventas es **{top}** con un total de ${total:,.0f}."
        fig = px.bar(data.groupby("vendedor")["ventas"].sum().reset_index(), x="vendedor", y="ventas", title="Ventas por Vendedor")
    elif "sucursal" in pregunta.lower():
        top = data.groupby("sucursal")["ventas"].sum().idxmax()
        total = data.groupby("sucursal")["ventas"].sum().max()
        respuesta = f"La sucursal con más ventas es **{top}** con un total de ${total:,.0f}."
        fig = px.bar(data.groupby("sucursal")["ventas"].sum().reset_index(), x="sucursal", y="ventas", title="Ventas por Sucursal")
    elif "promedio" in pregunta.lower():
        promedio = data['ventas'].mean()
        respuesta = f"El promedio de ventas por registro es de ${promedio:,.0f}."
        promedio_mes = data.groupby(data['fecha'].dt.to_period("M"))['ventas'].mean().reset_index()
        fig = px.bar(promedio_mes, x="fecha", y="ventas", title="Promedio de Ventas por Mes")
    elif "cumplimiento" in pregunta.lower():
        promedio = data['cumplimiento'].mean()
        respuesta = f"El cumplimiento promedio general es de {promedio:.2f}%"
        fig = px.box(data, x="sucursal", y="cumplimiento", color="sucursal", title="Distribución de Cumplimiento por Sucursal")
    else:
        respuesta = "Lo siento, aún no tengo una respuesta para esa pregunta."

    if respuesta:
        placeholder = st.empty()
        full_text = ""
        for char in respuesta:
            full_text += char
            placeholder.markdown(full_text)
            time.sleep(0.01)

    if fig:
        st.plotly_chart(fig, use_container_width=True)
