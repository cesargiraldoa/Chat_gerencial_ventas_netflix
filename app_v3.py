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
_, tab_inicio, tab_inicio2, tab_productos, tab_sucursales, tab_tendencias, tab_chat = st.tabs(["🏠 Inicio", "🧠 Inicio Alternativo", "📦 Productos", "🏢 Sucursales", "📈 Tendencias", "💬 Chat Gerencial"])

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

with tab_inicio2:
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

with tab_sucursales:
    st.subheader("🏢 Sucursales Top (estilo Netflix)")
    top_sucursales = data.groupby("sucursal").agg({'ventas': 'sum', 'meta': 'sum'}).reset_index()
    top_sucursales["cumplimiento"] = (top_sucursales["ventas"] / top_sucursales["meta"]) * 100
    top_sucursales = top_sucursales.sort_values(by="ventas", ascending=False).reset_index(drop=True)

    selected_sucursal = st.selectbox("Selecciona una sucursal para ver análisis:", top_sucursales["sucursal"])
    cols = st.columns(len(top_sucursales))
    for i, row in top_sucursales.iterrows():
        rank = i + 1
        color = "#00FFAA" if row["cumplimiento"] >= 100 else "#FF4B4B" if row["cumplimiento"] < 70 else "#FFD700"
        with cols[i]:
            st.markdown(f"""
                <div style='border:1px solid #333; border-radius:12px; padding:20px; text-align:center;'>
                    <h3 style='color:{color};'>🏢 {rank}. {row['sucursal']}</h3>
                    <p>💰 Ventas: ${row['ventas']:,.0f}</p>
                    <p>📊 Cumplimiento: {row['cumplimiento']:.2f}%</p>
                </div>
            """, unsafe_allow_html=True)

    if selected_sucursal:
        st.markdown(f"### 📊 Análisis de {selected_sucursal}")
        df_suc = data[data['sucursal'] == selected_sucursal].groupby("producto").agg({'ventas': 'sum'}).reset_index()
        fig = px.bar(df_suc, x="producto", y="ventas", title=f"Ventas por producto en {selected_sucursal}", color="ventas")
        st.plotly_chart(fig, use_container_width=True)

with tab_productos:
    st.subheader("📦 Productos Top (estilo Netflix)")
    top_productos = data.groupby("producto").agg({'ventas': 'sum'}).reset_index()
    top_productos = top_productos.sort_values(by="ventas", ascending=False).reset_index(drop=True)
    cols = st.columns(len(top_productos))
    for i, row in top_productos.iterrows():
        rank = i + 1
        color = "#00FFAA" if i == 0 else "#FFD700" if i == 1 else "#FF4B4B"
        with cols[i]:
            st.markdown(f"""
                <div style='border:1px solid #333; border-radius:12px; padding:20px; text-align:center;'>
                    <h3 style='color:{color};'>📦 {rank}. {row['producto']}</h3>
                    <p>💵 Ventas: ${row['ventas']:,.0f}</p>
                </div>
            """, unsafe_allow_html=True)

with tab_tendencias:
    st.subheader("📈 Tendencias de Ventas")
    tendencia = data.groupby(pd.Grouper(key="fecha", freq="M")).agg({'ventas': 'sum'}).reset_index()
    fig = px.line(tendencia, x="fecha", y="ventas", title="Tendencia mensual de ventas")
    st.plotly_chart(fig, use_container_width=True)

with tab_chat:
    st.subheader("💬 Chat Gerencial")
    pregunta = st.text_input("🤖 Escribe tu pregunta (ej: ¿Cuál es el producto top de esta semana?)")
    if pregunta:
        producto_top = data.groupby("producto")["ventas"].sum().idxmax()
        cumplimiento_global = (data["ventas"].sum() / data["meta"].sum()) * 100
        if "producto top" in pregunta.lower():
            st.info(f"🔍 El producto más vendido es: **{producto_top}**")
        elif "cumplimiento" in pregunta.lower():
            st.info(f"📊 El cumplimiento global actual es de **{cumplimiento_global:.2f}%**")
        elif "promedio" in pregunta.lower() and "ventas" in pregunta.lower():
            promedio_ventas = data['ventas'].mean()
            fig = px.histogram(data, x='producto', y='ventas', histfunc='avg', title="Promedio de ventas por producto")
            st.info(f"📉 El promedio de ventas es **${promedio_ventas:,.0f}**")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("🤔 Lo siento, aún no tengo una respuesta para esa pregunta.")
