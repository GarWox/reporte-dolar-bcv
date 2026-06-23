import streamlit as st
from monitor import PriceMonitor

st.set_page_config(
    page_title="Monitor de Divisas Venezuela",
    page_icon="💵",
    layout="centered"
)

st.title("💵 Monitor de Divisas")

monitor = PriceMonitor()
monitor.fetch_data()

  # --- Botón de refrescar ---
if st.button("🔄 Actualizar datos"):
      st.rerun()

  # --- Sección BCV --- 

st.header("📘 Tasas BCV")
col1, col2 = st.columns(2)

with col1:
  st.metric("Dólar BCV", f"{monitor.bcv_usd} VES")

with col2:
  st.metric("Euro BCV", f"{monitor.bcv_eur} VES")

# --- Sección Binance ---

st.header("📘 Tasas Binance")

col3, col4 = st.columns(2)

with col3:
  st.metric("Compra USDT", f"{monitor.binance_buy} VES")

with col4:
  st.metric("Venta USDT", f"{monitor.binance_sell} VES")