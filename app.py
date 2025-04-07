
import streamlit as st
import pandas as pd
import plotly.express as px

from PIL import Image

# Mostrar logo
logo = Image.open("assets/logo.png")
st.image(logo, width=200)


st.set_page_config(layout="wide", page_title="Chat Gerencial - Ventas", page_icon="📊")

st.markdown("""<h1 style='color:#FF4B4B;'>🎬 Chat Gerencial Estilo Netflix</h1>""", unsafe_allow_html=True)

# Cargar datos
data = pd.read_excel("data/ventas_ejemplo.xlsx")

# KPIs
st.subheader("📈 Indicadores clave")
col1, col2, col3 = st.columns(3)
col1.metric("Ventas totales", f"${data['ventas'].sum():,.0f}")
col2.metric("Meta total", f"${data['meta'].sum():,.0f}")
col3.metric("Cumplimiento (%)", f"{(data['ventas'].sum()/data['meta'].sum())*100:.2f}%")

# Gráfico de barras
fig = px.bar(data, x="producto", y="ventas", color="sucursal", barmode="group", title="Ventas por Producto y Sucursal")
st.plotly_chart(fig, use_container_width=True)

# Preguntas sugeridas tipo tarjetas (simulado)
st.markdown("### 🎯 Preguntas sugeridas")
questions = ["¿Qué producto vendió más?", "¿Qué sucursal superó la meta?", "¿Cuál es la tendencia semanal?"]
for q in questions:
    st.button(q)

# Análisis gerencial simulado
st.markdown("### 🧠 Análisis Gerencial")
st.info("🔍 Como CEO: Las ventas están alineadas con la meta general. Recomendamos enfocar esfuerzos en el producto con menor rotación en Barranquilla.")
