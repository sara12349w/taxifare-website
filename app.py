import streamlit as st
import requests
import datetime
import pandas as pd

st.title("🚖 Taxi Fare Prediction")

st.markdown("""
Use this app to estimate the price of a taxi ride in NYC!
Enter the ride details below 👇
""")

pickup_date = st.date_input("📅 Pickup date", datetime.date.today())
pickup_time = st.time_input("⏰ Pickup time", datetime.datetime.now().time())
pickup_long = st.number_input("📍 Pickup longitude", value=-73.985428)
pickup_lat = st.number_input("📍 Pickup latitude", value=40.748817)
dropoff_long = st.number_input("🏁 Dropoff longitude", value=-73.985428)
dropoff_lat = st.number_input("🏁 Dropoff latitude", value=40.748817)
passenger_count = st.number_input("👥 Passenger count", min_value=1, max_value=8, value=1)


pickup_datetime = f"{pickup_date} {pickup_time}"


url = "https://taxifare.lewagon.ai/predict"

if st.button("Predict fare 💰"):
    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_long,
        "pickup_latitude": pickup_lat,
        "dropoff_longitude": dropoff_long,
        "dropoff_latitude": dropoff_lat,
        "passenger_count": passenger_count
    }


    response = requests.get(url, params=params)


    if response.status_code == 200:
        prediction = response.json()
        fare = prediction.get("fare", None)
        if fare:
            st.success(f"💵 Estimated fare: ${fare:.2f}")


            locations = pd.DataFrame({
                'lat': [pickup_lat, dropoff_lat],
                'lon': [pickup_long, dropoff_long]
            })
            st.map(locations)
        else:
            st.error("⚠️ Prediction not found in the response.")
    else:
        st.error("⚠️ Could not retrieve prediction. Please check your API or parameters.")


st.markdown("---")
st.info("Enjoy your ride predictions! 🚖💨")
