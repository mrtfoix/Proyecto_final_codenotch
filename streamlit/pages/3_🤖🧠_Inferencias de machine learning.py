import streamlit as st
import pandas as pd

from base64 import b64encode
from modelos.inference import inference1, inference2

st.set_page_config(layout='wide')


st.markdown('## ¡Calcula la probabilidad de cancelación de tus reservas!')

opcion = st.radio("Seleccione una opción:", ("Una reserva", "Varias reservas"))

if opcion == 'Una reserva':
    hotel = st.selectbox("Tipo de hotel", ["City Hotel (Lisboa)", "Resort Hotel (Algarve)"])
    if hotel == "City Hotel (Lisboa)":
        x9 = 1
    else:
        x9 = 0
    x2 = st.number_input("Número de adultos", min_value=0, step=1)
    country = st.selectbox("País de origen del cliente", ["Alemania (DEU)", "Francia (FRA)", "Gran Bretaña (GBR)", "Portugal (PRT)", "España (ESP)", "Otros"])
    if country == "Alemania (DEU)":
        x12 = 1
        x13 = 0
        x14 = 0
        x15 = 0
    elif country == "Francia (FRA)":
        x12 = 0
        x13 = 1
        x14 = 0
        x15 = 0
    elif country == "Gran Bretaña (GBR)":
        x12 = 0
        x13 = 0
        x14 = 1
        x15 = 0
    elif country == "Portugal (PRT)":
        x12 = 0
        x13 = 0
        x14 = 0
        x15 = 1
    else:
        x12 = 0
        x13 = 0
        x14 = 0
        x15 = 0
    is_repeated_guest = st.selectbox("¿El cliente ya había reservado antes?", ["Sí", "No"])
    if is_repeated_guest == "Sí":
        x3 = 1
        x4 = st.number_input("Reservas anteriores canceladas", min_value=0, step=1)
        x5 = st.number_input("Reservas anteriores no canceladas", min_value=0, step=1)
    else:
        x3 = 0
        x4 = 0
        x5 = 0
    x7 = st.number_input("Número de días en lista de espera", min_value=0, step=1)
    x1 = st.number_input("Número de dias entre la reserva y la llegada (lead time)", min_value=0, step=1)
    x6 = st.number_input("Número de cambios en la reserva", min_value=0, step=1)
    x8 = st.number_input("Número de peticiones especiales", min_value=0, step=1)
    meal = st.selectbox("Tipo de pensión", ["Pensión Completa (FB)", "Media Pensión (HB)", "Bed & Breakfast (BB)", "Sin comida incluida"])
    if meal == "Pensión Completa (FB)":
        x10 = 1
        x11 = 0
    elif meal == "Media Pensión (HB)":
        x10 = 0
        x11 = 1
    else:
        x10 = 0
        x11 = 0
    market_segment = st.selectbox("Segmento de mercado", ["TA/TO", "Groups", "Direct", "Corporate", "Complementary", "Aviation"])
    if market_segment == "Corporate":
        x16 = 1
        x17 = 0
        x18 = 0
    elif market_segment == "Groups":
        x16 = 0
        x17 = 1
        x18 = 0
    elif market_segment == "TA/TO":
        x16 = 0
        x17 = 0
        x18 = 1
    else:
        x16 = 0
        x17 = 0
        x18 = 0
    deposit_type = st.selectbox("Tipo de fianza", ["Reembolsable", "No reembolsable", "Sin fianza"])
    if deposit_type == "No reembolsable":
        x19 = 1
    else:
        x19 = 0
    customer_type = st.selectbox("Tipo de cliente", ["Transient", "Transient-party", "Contract", "Group"])
    if customer_type == "Transient":
        x20 = 1
    else:
        x20 = 0

    X = []
    for i in range(20):
        item = 'x' + str(i+1)
        X.append(eval(item))

    calcular = st.button("Calcular")
    if calcular:
        y_proba = inference1(X)
        color = "green" if y_proba < 0.5 else "red"
        texto_coloreado = f'Probabilidad de cancelación:<p style="color:{color};"> {round(y_proba*100,2)}%</p>'
        st.markdown(texto_coloreado, unsafe_allow_html=True)

if opcion == 'Varias reservas':
    archivo_csv = st.file_uploader("Cargar archivo en formato csv con todas las reservas:", type=["csv"])
    features = [
        "lead_time",
        "adults",
        "is_repeated_guest",
        "previous_cancellations",
        "previous_bookings_not_canceled",
        "booking_changes",
        "days_in_waiting_list",
        "total_of_special_requests",
        "hotel_City Hotel",
        "meal_FB",
        "meal_HB",
        "country_DEU",
        "country_FRA",
        "country_GBR",
        "country_PRT",
        "market_segment_Corporate",
        "market_segment_Groups",
        "market_segment_TA/TO",
        "deposit_type_Non Refund",
        "customer_type_Transient"
        ]
    if archivo_csv is not None:
        df = pd.read_csv(archivo_csv)
        if 'market segment' in df.columns:
            df['market_segment'] = df['market_segment'].apply(lambda x: 'TA/TO' if x in ['Online TA', 'Offline TA/TO'] else x)
        if 'meal' in df.columns:
            sin_comida = ['Undefined', 'SC']
            df['meal'] = df['meal'].apply(lambda x: x if x not in sin_comida else 'No_meal')
        if 'country' in df.columns:
            paises_comunes = ['PRT', 'FRA', 'GBR', 'DEU', 'ESP']
            df['country'] = df['country'].apply(lambda x: x if x in paises_comunes else 'otros')
        df = pd.get_dummies(df)
        df = df[features]
        calcular = st.button("Calcular")
        if calcular:
            resultados = inference2(df)
            csv = resultados.to_csv(index=False).encode('utf-8-sig')
            href = f'<a href="data:file/csv;base64,{b64encode(csv).decode()}" download="resultados_inferencias.csv">Descargar Resultados</a>'
            st.markdown(href,unsafe_allow_html=True)
