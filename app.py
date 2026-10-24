
import requests
import streamlit as st
from datetime import datetime

st.title("🚕 TaxiFareModel")

st.write("Preveja o valor de uma corrida de táxi em Nova York!")

st.subheader("Informações da corrida")

with st.form("ride_form"):

    col1, col2 = st.columns(2)

    with col1:
        pickup_date = st.date_input("Data da corrida")

    with col2:
        pickup_time = st.time_input("Horário da corrida")

    pickup_longitude = st.number_input(
        "Longitude de origem",
        value=-73.9857,
        format="%.6f"
    )

    pickup_latitude = st.number_input(
        "Latitude de origem",
        value=40.7484,
        format="%.6f"
    )

    dropoff_longitude = st.number_input(
        "Longitude de destino",
        value=-73.9776,
        format="%.6f"
    )

    dropoff_latitude = st.number_input(
        "Latitude de destino",
        value=40.7614,
        format="%.6f"
    )

    passenger_count = st.number_input(
        "Número de passageiros",
        min_value=1,
        max_value=8,
        value=1
    )

    submitted = st.form_submit_button("Prever tarifa")

if submitted:

    pickup_datetime = datetime.combine(
        pickup_date, pickup_time
    ).strftime("%Y-%m-%d %H:%M:%S")

    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }


    # API publicada no Cloud Run na aula anterior
    url = "https://taxifare.lewagon.ai/predict"

    try:
        with st.spinner("Calculando tarifa..."):
            response = requests.get(
                url,
                params=params,
                timeout=20
            )

            response.raise_for_status()
            prediction = response.json()

        fare = prediction["fare"]

        st.success("Previsão realizada com sucesso!")

        st.metric(
            label="Tarifa estimada",
            value=f"US$ {float(fare):,.2f}"
        )

        st.subheader("📍 Localização da corrida")

        st.map({
            "lat": [pickup_latitude, dropoff_latitude],
            "lon": [pickup_longitude, dropoff_longitude]
        })


    except (requests.RequestException, ValueError, KeyError, TypeError) as error:
        st.error(f"Não foi possível obter a previsão: {error}")
