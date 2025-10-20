import streamlit as st
import requests
import datetime
import pandas as pd

st.title("🚖 Taxi Fare Prediction")

st.markdown("""
Use this app to estimate the price of a taxi ride in NYC!
Enter the ride details below 👇
""")

# --- Date and Time Inputs ---
pickup_date = st.date_input("📅 Pickup date", datetime.date.today())

# استخدام session_state لتخزين الوقت وتحديثه
if 'pickup_time' not in st.session_state:
    st.session_state.pickup_time = datetime.datetime.now().time()

pickup_time = st.time_input(
    "⏰ Pickup time",
    value=st.session_state.pickup_time,
    key="pickup_time_input"
)
st.session_state.pickup_time = pickup_time

# --- Location Inputs ---
pickup_long = st.number_input("📍 Pickup longitude", value=-73.985428)
pickup_lat = st.number_input("📍 Pickup latitude", value=40.748817)
dropoff_long = st.number_input("🏁 Dropoff longitude", value=-73.985428)
dropoff_lat = st.number_input("🏁 Dropoff latitude", value=40.748817)

# --- Passenger Count ---
passenger_count = st.number_input("👥 Passenger count", min_value=1, max_value=8, value=1)

# --- Combine Date & Time ---
pickup_datetime = f"{pickup_date} {pickup_time}"

# --- API URL ---
url = "https://taxifare.lewagon.ai/predict"

# --- Predict Button ---
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

            # --- Show map ---
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
