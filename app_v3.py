import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from fpdf import FPDF
import tempfile
from matplotlib import pyplot as plt
from datetime import datetime
import time
import face_recognition
import cv2
import numpy as np

st.set_page_config(layout="wide")
st.title("📊 Análisis Gerencial - Modo Netflix")

archivo = st.file_uploader("📂 Cargar archivo Excel de ventas", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo)
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['hora'] = df['hora'].astype(str)
    df['dia'] = df['fecha'].dt.day_name()

    ventas_total = df['ventas_reales'].sum()
    cumplimiento_prom = df['cumplimiento'].mean()
    producto_top = df.groupby('producto')['ventas_reales'].sum().idxmax()
    sucursal_top = df.groupby('sucursal')['ventas_reales'].sum().idxmax()
    vendedor_top = df.groupby('vendedor')['ventas_reales'].sum().idxmax()

    fig_dia = px.bar(df.groupby('dia')['ventas_reales'].sum().reindex([
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    ]).reset_index(), x='dia', y='ventas_reales', title="Ventas por Día")

    fig_hora = px.bar(df.groupby('hora')['ventas_reales'].sum().reset_index(), x='hora', y='ventas_reales', title="Ventas por Hora")
    fig_suc = px.bar(df.groupby('sucursal')['ventas_reales'].sum().reset_index(), x='sucursal', y='ventas_reales', title="Ventas por Sucursal")

    tab_inicio, tab_productos, tab_sucursales, tab_tendencias, tab_chat, tab_gerencial, tab_facial = st.tabs([
        "🏠 Inicio", "📦 Productos", "🏢 Sucursales", "📈 Tendencias", "💬 Chat Gerencial", "📑 Informe Gerencial", "🔐 Acceso Facial"
    ])

    with tab_inicio:
        st.subheader("Resumen Ejecutivo")
        col1, col2, col3 = st.columns(3)
        col1.metric("Ventas Totales", f"${ventas_total:,.0f}")
        col2.metric("Cumplimiento Promedio", f"{cumplimiento_prom:.2f}%")
        col3.metric("Producto Top", producto_top)
        st.plotly_chart(fig_dia, use_container_width=True)

    with tab_productos:
        st.subheader("Análisis por Producto")
        fig_prod = px.bar(df.groupby('producto')['ventas_reales'].sum().sort_values().reset_index(), x='ventas_reales', y='producto', orientation='h', title="Ventas por Producto")
        st.plotly_chart(fig_prod, use_container_width=True)

    with tab_sucursales:
        st.subheader("Análisis por Sucursal")
        st.plotly_chart(fig_suc, use_container_width=True)

    with tab_tendencias:
        st.subheader("Tendencias por Hora")
        st.plotly_chart(fig_hora, use_container_width=True)

    preguntas = [
        "¿Cuál es el producto más vendido?",
        "¿Qué sucursal vendió más?",
        "¿Quién es el vendedor con más ventas?",
        "¿Cuál es el promedio de cumplimiento?",
        "¿En qué día se vendió más?"
    ]
    respuestas = [
        f"El producto más vendido es **{producto_top}**, con un total de ${df.groupby('producto')['ventas_reales'].sum().max():,.0f}.",
        f"La sucursal con más ventas es **{sucursal_top}**, alcanzando ${df.groupby('sucursal')['ventas_reales'].sum().max():,.0f} en ventas.",
        f"El vendedor con más ventas es **{vendedor_top}**, con un total de ${df.groupby('vendedor')['ventas_reales'].sum().max():,.0f}.",
        f"El promedio de cumplimiento es **{cumplimiento_prom:.2f}%** en todo el periodo evaluado.",
        f"El día con más ventas fue **{df.groupby('dia')['ventas_reales'].sum().idxmax()}**, con ${df.groupby('dia')['ventas_reales'].sum().max():,.0f} en total."
    ]

    with tab_chat:
        st.subheader("Asistente de Análisis")
        user_input = st.text_input("💬 Escribe tu pregunta sobre ventas, productos o desempeño:")
        if user_input:
            respuesta = "No tengo una respuesta para esa pregunta."
            for i, preg in enumerate(preguntas):
                if preg.lower() in user_input.lower():
                    respuesta = respuestas[i]
                    break
            with st.chat_message("assistant"):
                st.markdown(f"🧠 Estoy analizando tu pregunta: **{user_input}**")
                placeholder = st.empty()
                texto = "✍️ "
                for c in respuesta:
                    texto += c
                    placeholder.markdown(texto)
                    time.sleep(0.03)
        else:
            st.info("🔍 Aquí puedes hacer preguntas sobre ventas, productos o desempeño. Escribe tu consulta arriba.")

        st.markdown("---")
        st.subheader("🧠 Preguntas y Respuestas Frecuentes")
        for i in range(len(preguntas)):
            st.markdown(f"**❓ {preguntas[i]}**")
            st.markdown(f"✅ {respuestas[i]}")

    with tab_gerencial:
        st.subheader("📥 Informe Gerencial PDF")
        if st.button("📥 Descargar análisis en PDF"):
            with tempfile.TemporaryDirectory() as tmpdirname:
                fig_dia.write_image(f"{tmpdirname}/dia.png")
                fig_hora.write_image(f"{tmpdirname}/hora.png")
                fig_suc.write_image(f"{tmpdirname}/suc.png")

                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 20)
                pdf.cell(0, 60, '', ln=True)
                pdf.cell(0, 10, "Reporte de Análisis Gerencial", ln=True, align='C')
                pdf.set_font("Arial", '', 14)
                pdf.cell(0, 10, "Versión Ejecutiva - CEO & Gerencia Comercial", ln=True, align='C')
                pdf.cell(0, 10, f"Fecha: {datetime.today().strftime('%Y-%m-%d')}", ln=True, align='C')

                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, f"ANÁLISIS GERENCIAL COMPLETO\n\nVentas Totales: ${ventas_total:,.0f}\nCumplimiento Promedio: {cumplimiento_prom:.2f}%\nProducto Top: {producto_top}\nSucursal Líder: {sucursal_top}\nVendedor Destacado: {vendedor_top}\n")
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, "\nGráfico: Ventas por Día", ln=1)
                pdf.image(f"{tmpdirname}/dia.png", w=180)
                pdf.cell(0, 10, "\nGráfico: Ventas por Hora", ln=1)
                pdf.image(f"{tmpdirname}/hora.png", w=180)
                pdf.cell(0, 10, "\nGráfico: Ventas por Sucursal", ln=1)
                pdf.image(f"{tmpdirname}/suc.png", w=180)
                pdf.set_font("Arial", '', 11)
                pdf.multi_cell(0, 10, "\nRecomendaciones:\n- CEO: Estrategia basada en ciudades con mejor desempeño.\n- Marketing: Campañas en horas y días clave.\n- Comercial: Metas dinámicas, incentivos.\n- Vendedores: Técnicas de economía conductual.\n")

                pdf_bytes = pdf.output(dest='S').encode('latin1')
                st.download_button("📄 Descargar Informe PDF", data=pdf_bytes, file_name="analisis_gerencial.pdf", mime="application/pdf")

    with tab_facial:
        st.subheader("🔐 Acceso Facial al Informe Gerencial")
        imagen_base_path = "usuario_base.jpg"  # Debe estar en el mismo directorio
        try:
            imagen_registrada = face_recognition.load_image_file(imagen_base_path)
            codificacion_registrada = face_recognition.face_encodings(imagen_registrada)[0]

            imagen_camera = st.camera_input("📸 Toma una foto para verificar tu identidad")
            if imagen_camera is not None:
                imagen_nueva = face_recognition.load_image_file(imagen_camera)
                codificaciones_nuevas = face_recognition.face_encodings(imagen_nueva)

                if codificaciones_nuevas:
                    coincidencia = face_recognition.compare_faces([codificacion_registrada], codificaciones_nuevas[0])[0]
                    if coincidencia:
                        st.success("✅ Rostro verificado. Acceso concedido al Informe Gerencial.")
                        st.markdown("### 🔓 Acceso desbloqueado: puedes ir a la pestaña '📑 Informe Gerencial'.")
                    else:
                        st.error("❌ Rostro no coincide. Acceso denegado.")
                else:
                    st.warning("⚠️ No se detectó ningún rostro en la imagen capturada.")
        except Exception as e:
            st.error("Error cargando imagen base. Asegúrate de tener 'usuario_base.jpg' en el directorio.")
