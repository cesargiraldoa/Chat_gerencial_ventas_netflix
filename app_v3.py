import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

st.set_page_config(layout="wide", page_title="Chat Gerencial - Modo Oscuro", page_icon="🖤")

# Logo y título
logo = Image.open("assets/logo.png")
st.image(logo, width=180)
st.markdown("<h1 style='color:#FF4B4B;'>🎬 Chat Gerencial Estilo Netflix - Modo Oscuro</h1>", unsafe_allow_html=True)

# Cargar datos
data = pd.read_excel("data/ventas_ejemplo.xlsx")

# KPIs
st.markdown("## 📊 Métricas Generales")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("🧮 Ventas Totales", f"${data['ventas'].sum():,.0f}")
kpi2.metric("🎯 Meta Total", f"${data['meta'].sum():,.0f}")
kpi3.metric("📈 Cumplimiento (%)", f"{(data['ventas'].sum()/data['meta'].sum())*100:.2f}%")
producto_top = data.groupby("producto")["ventas"].sum().idxmax()
kpi4.metric("🔥 Producto Más Vendido", producto_top)

# Estilo oscuro para secciones
st.markdown("## 🍿 Top Productos del Mes")
top_productos = data.groupby("producto").agg({'ventas': 'sum'}).reset_index()
cols = st.columns(len(top_productos))
for i, row in top_productos.iterrows():
    with cols[i]:
        st.markdown(f'''
        <div style="background-color:#1a1a1a;padding:20px;border-radius:15px;">
            <h4 style="color:#FF4B4B;">🎬 {row['producto']}</h4>
            <p style="color:white;">Ventas: ${row['ventas']:,.0f}</p>
        </div>
        ''', unsafe_allow_html=True)
        st.button(f"Ver análisis {i+1}")

# Sucursales
st.markdown("## 🏢 Ranking de Sucursales")
top_sucursales = data.groupby("sucursal").agg({'ventas': 'sum'}).reset_index()
cols2 = st.columns(len(top_sucursales))
for i, row in top_sucursales.iterrows():
    with cols2[i]:
        st.markdown(f'''
        <div style="background-color:#1a1a1a;padding:20px;border-radius:15px;">
            <h4 style="color:#FFB84B;">🏙️ {row['sucursal']}</h4>
            <p style="color:white;">Ventas: ${row['ventas']:,.0f}</p>
        </div>
        ''', unsafe_allow_html=True)
        st.button(f"Ver análisis sucursal {i+1}")

# Análisis comparativo
st.markdown("## 📊 Comparación de Productos")
fig = px.bar(data, x="producto", y="ventas", color="sucursal", barmode="group", title="Ventas por Producto y Sucursal")
st.plotly_chart(fig, use_container_width=True)
