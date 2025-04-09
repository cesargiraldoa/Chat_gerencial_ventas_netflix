import streamlit as st
import pandas as pd
import plotly.express as px
import face_recognition
from datetime import datetime
from PIL import Image

st.set_page_config(layout="wide", page_title="Chat Gerencial Netflix")

# --- Estilo Netflix ---
st.markdown("""
    <style>
        body { background-color: #111; }
        .big-title { font-size: 36px; color: red; font-weight: bold; }
        .sub { font-size: 22px; color: white; }
        .kpi-title { color: white; font-size: 16px; }
        .kpi-value { font-size: 24px; color: white; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- Cabecera estilo Netflix ---
col_logo, col_title = st.columns([1, 6])
with col_logo:
    st.image("assets/chat_logo.png", width=100)
with col_title:
    st.markdown("<div class='big-title'>Chat Gerencial Estilo Netflix</div>", unsafe_allow_html=True)

# --- Selección de perfil ---
perfil = st.sidebar.selectbox("👤 Selecciona tu perfil", ["Gerente General", "Director de Ventas", "Director de Marketing"])
st.session_state.perfil = perfil

# --- Función para cargar datos ---
@st.cache_data
def cargar_datos():
    df = pd.read_excel("data/ventas_ejemplo_v4.xlsx")
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    return df

# --- Función para verificación facial (solo gerente) ---
def desbloqueo_facial():
    st.warning("🔐 Se requiere autenticación facial para continuar")
    foto = st.camera_input("Captura tu rostro para validar acceso")

    if foto:
        try:
            user_img = face_recognition.load_image_file(foto)
            user_encoding = face_recognition.face_encodings(user_img)
            if not user_encoding:
                st.error("❌ No se detectó ningún rostro. Intenta de nuevo.")
                return False

            base_img = face_recognition.load_image_file("usuario_base.jpg")
            base_encoding = face_recognition.face_encodings(base_img)[0]
            match = face_recognition.compare_faces([base_encoding], user_encoding[0])

            if match[0]:
                st.success("✅ Acceso concedido")
                return True
            else:
                st.error("🚫 Rostro no coincide")
                return False
        except Exception as e:
            st.error(f"⚠️ Error al procesar imagen: {str(e)}")
            return False
    return False

# --- Desbloqueo si es Gerente General
acceso = True
if perfil == "Gerente General":
    acceso = desbloqueo_facial()

if acceso:
    df = cargar_datos()
    fecha_inicio = st.sidebar.date_input("📅 Desde", df["Fecha"].min())
    fecha_fin = st.sidebar.date_input("📅 Hasta", df["Fecha"].max())
    df = df[(df["Fecha"] >= pd.to_datetime(fecha_inicio)) & (df["Fecha"] <= pd.to_datetime(fecha_fin))]

    st.markdown("<div class='sub'>📊 Indicadores clave</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Ventas totales", f"${df['Ventas'].sum():,.0f}")
    col2.metric("Meta total", f"${df['Meta'].sum():,.0f}")
    col3.metric("Cumplimiento (%)", f"{(df['Ventas'].sum() / df['Meta'].sum()) * 100:.2f}%")

    st.plotly_chart(
        px.bar(df, x="Producto", y="Ventas", color="Sucursal", barmode="group", title="Ventas por Producto y Sucursal"),
        use_container_width=True
    )

    st.markdown("<br><div class='sub'>🎯 Preguntas sugeridas</div>", unsafe_allow_html=True)
    st.button("¿Qué producto vendió más?")
    st.button("¿Qué sucursal superó la meta?")
    st.button("¿Cuál es la tendencia semanal?")
else:
    st.error("🔒 Acceso denegado. Debes completar autenticación facial.")
