...    
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
