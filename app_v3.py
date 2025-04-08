import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from fpdf import FPDF

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

    # Gráficos
    fig_dia = px.bar(df.groupby('dia')['ventas_reales'].sum().reindex([
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    ]).reset_index(), x='dia', y='ventas_reales', title="Ventas por Día")

    fig_hora = px.bar(df.groupby('hora')['ventas_reales'].sum().reset_index(), x='hora', y='ventas_reales', title="Ventas por Hora")

    fig_suc = px.bar(df.groupby('sucursal')['ventas_reales'].sum().reset_index(), x='sucursal', y='ventas_reales', title="Ventas por Sucursal")

    st.plotly_chart(fig_dia, use_container_width=True)
    st.plotly_chart(fig_hora, use_container_width=True)
    st.plotly_chart(fig_suc, use_container_width=True)

    st.subheader("📥 Informe Gerencial PDF")

    if st.button("📥 Descargar análisis en PDF"):
        import tempfile
        from matplotlib import pyplot as plt
        from datetime import datetime

        with tempfile.TemporaryDirectory() as tmpdirname:
            # Guardar gráficos como imágenes temporales
            fig_dia.write_image(f"{tmpdirname}/dia.png")
            fig_hora.write_image(f"{tmpdirname}/hora.png")
            fig_suc.write_image(f"{tmpdirname}/suc.png")

            pdf = FPDF()
            # Portada
            pdf.add_page()
            pdf.set_font("Arial", 'B', 20)
            pdf.set_text_color(36, 36, 36)
            pdf.cell(0, 60, '', ln=True)  # Espacio superior
            pdf.cell(0, 10, "Reporte de Análisis Gerencial", ln=True, align='C')
            pdf.set_font("Arial", '', 14)
            pdf.cell(0, 10, "Versión Ejecutiva - CEO & Gerencia Comercial", ln=True, align='C')
            pdf.cell(0, 10, f"Fecha: {datetime.today().strftime('%Y-%m-%d')}", ln=True, align='C')

            # Contenido
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

            pdf_output = BytesIO()
            pdf.output(pdf_output)
            st.download_button("📄 Descargar Informe PDF", data=pdf_output.getvalue(), file_name="analisis_gerencial.pdf", mime="application/pdf")
