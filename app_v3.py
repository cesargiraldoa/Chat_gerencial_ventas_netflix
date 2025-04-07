import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

st.set_page_config(layout="wide", page_title="Chat Gerencial - Netflix Style", page_icon="🎬")

# Logo e introducción
logo = Image.open("assets/logo.png")
st.image(logo, width=180)
st.markdown("## Chat Gerencial Estilo Netflix")

# Cargar datos
data = pd.read_excel("data/ventas_ejemplo.xlsx")

# KPIs principales
st.markdown("### 🔢 Métricas Generales")
col1, col2, col3, col4 = st.columns(4)
col1.metric("🧮 Ventas Totales", f"${data['ventas'].sum():,.0f}")
col2.metric("🎯 Meta Total", f"${data['meta'].sum():,.0f}")
col3.metric("📈 Cumplimiento (%)", f"{(data['ventas'].sum()/data['meta'].sum())*100:.2f}%")
producto_top = data.groupby("producto")["ventas"].sum().idxmax()
col4.metric("🔥 Producto Más Vendido", producto_top)

# Carrusel 1: Productos destacados
st.markdown("### 🍿 Top Productos del Mes")
top_productos = data.groupby("producto").agg({'ventas': 'sum'}).reset_index()
cols = st.columns(len(top_productos))
for i, row in top_productos.iterrows():
    with cols[i]:
        st.markdown(f"#### 🎬 {row['producto']}")
        st.metric("Ventas", f"${row['ventas']:,.0f}")
        st.button(f"Ver análisis {i+1}")

# Carrusel 2: Sucursales
st.markdown("### 🏢 Sucursales en Ranking")
top_sucursales = data.groupby("sucursal").agg({'ventas': 'sum'}).reset_index()
cols2 = st.columns(len(top_sucursales))
for i, row in top_sucursales.iterrows():
    with cols2[i]:
        st.markdown(f"#### 🏙️ {row['sucursal']}")
        st.metric("Ventas", f"${row['ventas']:,.0f}")
        st.button(f"Ver análisis sucursal {i+1}")

# Carrusel 3: Análisis extra
st.markdown("### 📊 Análisis Comparativo")
fig = px.bar(data, x="producto", y="ventas", color="sucursal", barmode="group", title="Comparación de Ventas por Producto")
st.plotly_chart(fig, use_container_width=True)