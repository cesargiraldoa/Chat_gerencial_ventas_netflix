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

with tab_inicio:
    st.subheader("📊 Métricas Generales")
    total_ventas = data["ventas"].sum()
    total_meta = data["meta"].sum()
    cumplimiento = (total_ventas / total_meta) * 100
    producto_top = data.groupby("producto")["ventas"].sum().idxmax()

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("🧶 Ventas Totales", f"${total_ventas:,.0f}")
    kpi2.metric("🎯 Meta Total", f"${total_meta:,.0f}")
    kpi3.metric("📈 Cumplimiento (%)", f"{cumplimiento:.2f}%")
    kpi4.metric("🔥 Producto Más Vendido", producto_top)

    if cumplimiento < 70:
        st.error("🚨 Alerta: El cumplimiento está por debajo del 70% de la meta.")
    else:
        st.success("✅ Buen rendimiento general frente a la meta.")

with tab_productos:
    st.subheader("🍿 Productos Destacados")
    if 'producto_seleccionado' not in st.session_state:
        st.session_state.producto_seleccionado = None

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
            if st.button(f"Ver análisis {i+1}"):
                st.session_state.producto_seleccionado = row['producto']

    producto = st.session_state.producto_seleccionado
    if producto:
        st.markdown(f"### 📌 Análisis de *{producto}*")
        df_prod = data[data['producto'] == producto]
        fig = px.bar(df_prod, x="sucursal", y="ventas", color="sucursal", title=f"Ventas por sucursal de {producto}")
        st.plotly_chart(fig, use_container_width=True)

        total_ventas = df_prod["ventas"].sum()
        media_ventas = data.groupby("producto")["ventas"].sum().mean()

        if total_ventas >= media_ventas:
            comentario = f"✅ El producto **{producto}** está vendiendo por encima del promedio general."
        else:
            comentario = f"⚠️ El producto **{producto}** está por debajo del promedio. Requiere atención."
        st.info(f"🧠 Análisis gerencial: {comentario}")

        if st.button("📄 Exportar análisis a PDF"):
            buffer = BytesIO()
            p = canvas.Canvas(buffer)
            p.setFont("Helvetica", 12)
            p.drawString(100, 800, f"Análisis de Producto: {producto}")
            p.drawString(100, 780, f"Total Ventas: ${total_ventas:,.0f}")
            p.drawString(100, 760, f"Comentario Gerencial:")
            p.drawString(100, 740, comentario)
            p.drawString(100, 720, f"Fecha: {datetime.now().strftime('%Y-%m-%d')}")
            p.showPage()
            p.save()
            st.download_button(
                label="📅 Descargar PDF",
                data=buffer.getvalue(),
                file_name=f"analisis_{producto}.pdf",
                mime="application/pdf"
            )

with tab_sucursales:
    st.subheader("🏢 Ranking de Sucursales")
    vista = st.radio("Selecciona vista:", ["📂 Vista estándar", "🎬 Vista tipo Netflix (Top)"], horizontal=True)
    top_sucursales = data.groupby("sucursal").agg({'ventas': 'sum', 'meta': 'sum'}).reset_index()
    top_sucursales["cumplimiento"] = (top_sucursales["ventas"] / top_sucursales["meta"]) * 100
    top_sucursales = top_sucursales.sort_values(by="ventas", ascending=False).reset_index(drop=True)

    if vista == "📂 Vista estándar":
        cols2 = st.columns(len(top_sucursales))
        for i, row in top_sucursales.iterrows():
            color = "#FFB84B" if row["cumplimiento"] >= 70 else "#FF4B4B"
            mensaje = "✅ Buen desempeño" if row["cumplimiento"] >= 70 else "⚠️ Bajo rendimiento"
            with cols2[i]:
                st.markdown(f'''
                <div style="background-color:#1a1a1a;padding:20px;border-radius:15px;">
                    <h4 style="color:{color};">🌇 {row['sucursal']}</h4>
                    <p style="color:white;">Ventas: ${row['ventas']:,.0f}</p>
                    <p style="color:white;">Cumplimiento: {row['cumplimiento']:.2f}%</p>
                    <p style="color:white;">{mensaje}</p>
                </div>
                ''', unsafe_allow_html=True)

    elif vista == "🎬 Vista tipo Netflix (Top)":
        st.markdown("### 🏆 Sucursales Top (estilo Netflix)")
        st.markdown("""
            <style>
            .scrolling-wrapper {
                display: flex;
                overflow-x: auto;
                gap: 20px;
                padding-bottom: 20px;
            }
            .scrolling-wrapper::-webkit-scrollbar {
                height: 8px;
            }
            .scrolling-wrapper::-webkit-scrollbar-thumb {
                background: #FF4B4B;
                border-radius: 4px;
            }
            .card-netflix {
                flex: 0 0 auto;
                width: 300px;
                background-color: #1a1a1a;
                padding: 20px;
                border-radius: 20px;
                text-align: center;
            }
            </style>
            <div class="scrolling-wrapper">
        """, unsafe_allow_html=True)

        for i, row in top_sucursales.iterrows():
            rank = i + 1
            color = "#00FFAA" if row["cumplimiento"] >= 100 else "#FF4B4B" if row["cumplimiento"] < 70 else "#FFD700"
            st.markdown(f"""
            <div class="card-netflix">
                <div style='font-size:70px; font-weight:bold; color:#2E2E2E;'>{rank}</div>
                <h3 style='color:{color};'>🏢 {row['sucursal']}</h3>
                <p style='color:white;'>💰 Ventas: ${row['ventas']:,.0f}</p>
                <p style='color:white;'>📊 Cumplimiento: {row['cumplimiento']:.2f}%</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""</div>""", unsafe_allow_html=True)

with tab_tendencias:
    st.subheader("📈 Comparación General")
    fig = px.bar(data, x="producto", y="ventas", color="sucursal", barmode="group", title="Ventas por Producto y Sucursal")
    st.plotly_chart(fig, use_container_width=True)

with tab_chat:
    st.subheader("💬 Asistente Gerencial Inteligente")
    pregunta = st.text_input("Escribe tu pregunta:", placeholder="Ej: ¿Qué producto superó la meta?")
    if pregunta:
        if "superó la meta" in pregunta.lower():
            df = data.groupby("producto").sum().reset_index()
            df["cumplimiento"] = df["ventas"] / df["meta"]
            top = df[df["cumplimiento"] >= 1.0]
            if not top.empty:
                nombres = ", ".join(top["producto"].tolist())
                st.success(f"🌟 Productos que superaron la meta: {nombres}")
            else:
                st.warning("Ningún producto ha superado la meta.")
        elif "peor sucursal" in pregunta.lower():
            df = data.groupby("sucursal").sum().reset_index()
            peor = df[df["ventas"] == df["ventas"].min()]["sucursal"].values[0]
            st.error(f"🔻 La sucursal con menor rendimiento es: {peor}")
        else:
            st.info("🧠 Estoy en entrenamiento. Prueba con: ¿Qué producto superó la meta?")
