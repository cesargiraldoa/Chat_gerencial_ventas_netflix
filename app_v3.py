import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from io import BytesIO
from reportlab.pdfgen import canvas
from datetime import datetime

st.set_page_config(layout="wide", page_title="Chat Gerencial - Modo Oscuro", page_icon="🔟")

# Logo y título
logo = Image.open("assets/logo.png")
st.image(logo, width=180)
st.markdown("<h1 style='color:#FF4B4B;'>🎬 Chat Gerencial Estilo Netflix - Modo Oscuro</h1>", unsafe_allow_html=True)

# Cargar datos
data = pd.read_excel("data/ventas_ejemplo.xlsx")

# Filtro por fechas
fecha_inicio = st.date_input("🗓️ Fecha inicial", value=pd.to_datetime("2025-01-01"))
fecha_fin = st.date_input("🗓️ Fecha final", value=pd.to_datetime("2025-12-31"))

# Tabs
tab_inicio, tab_productos, tab_sucursales, tab_tendencias, tab_chat = st.tabs(["🏠 Inicio", "📦 Productos", "🏢 Sucursales", "📈 Tendencias", "💬 Chat Gerencial"])

# [...] otras tabs se mantienen igual

with tab_sucursales:
    st.subheader("🏢 Ranking de Sucursales")
    vista = st.radio("Selecciona vista:", ["📂 Vista estándar", "🎬 Vista tipo Netflix (Top)"], horizontal=True)
    top_sucursales = data.groupby("sucursal").agg({'ventas': 'sum', 'meta': 'sum'}).reset_index()
    top_sucursales["cumplimiento"] = (top_sucursales["ventas"] / top_sucursales["meta"]) * 100
    top_sucursales = top_sucursales.sort_values(by="ventas", ascending=False).reset_index(drop=True)

    if vista == "🎬 Vista tipo Netflix (Top)":
        st.markdown("### 🏆 Sucursales Top (estilo Netflix)")
        st.markdown("""
        <style>
        .netflix-carousel {
            display: flex;
            overflow-x: auto;
            scroll-snap-type: x mandatory;
            gap: 40px;
            padding-bottom: 20px;
        }
        .netflix-card {
            position: relative;
            flex: 0 0 auto;
            width: 200px;
            height: 320px;
            background-color: #111;
            border-radius: 10px;
            color: white;
            padding: 15px;
            scroll-snap-align: start;
        }
        .netflix-rank {
            position: absolute;
            top: 0;
            left: -30px;
            font-size: 200px;
            color: rgba(255,255,255,0.05);
            font-weight: bold;
            z-index: 0;
        }
        .netflix-content {
            position: relative;
            z-index: 1;
            text-align: center;
        }
        </style>
        <div class="netflix-carousel">
        """, unsafe_allow_html=True)

        for i, row in top_sucursales.iterrows():
            rank = i + 1
            color = "#00FFAA" if row["cumplimiento"] >= 100 else "#FF4B4B" if row["cumplimiento"] < 70 else "#FFD700"
            st.markdown(f"""
            <div class='netflix-card'>
                <div class='netflix-rank'>{rank}</div>
                <div class='netflix-content'>
                    <h4 style='color:{color};'>🏢 {row['sucursal']}</h4>
                    <p>💰 ${row['ventas']:,.0f}</p>
                    <p>📊 {row['cumplimiento']:.2f}%</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# [...] otras tabs continúan
