import streamlit as st
import requests
import datetime

BACKEND_URL = "https://ai-travel-planner-85vp.onrender.com/"

st.set_page_config(page_title="🧳 AI Travel Planner", layout="wide")
st.title("🗺️ AI Travel Planner")

with st.form("travel_form"):
    source = st.text_input("Source City", "Pune")
    destination = st.text_input("Destination City", "Lonavala")
    start_date = st.date_input("Start Date", datetime.date.today())
    end_date = st.date_input("End Date", datetime.date.today() + datetime.timedelta(days=1))
    preferences = st.multiselect("Preferences", ["nature", "hiking", "museum", "attraction", "hotel"], default=["nature", "hotel"])
    budget = st.number_input("Approx. Budget (INR)", min_value=0, step=500, value=4000)
    transport = st.selectbox("Transport Mode", ["car", "bike", "foot"])
    submit = st.form_submit_button("Plan My Trip")

if submit:
    with st.spinner("Planning your trip..."):
        payload = {
            "source": source,
            "destination": destination,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "preferences": preferences,
            "budget": budget,
            "transport_mode": transport
        }

        try:
            res = requests.post(f"{BACKEND_URL}/plan", json=payload)
            res.raise_for_status()
            data = res.json()

            st.success("✅ Trip Successfully Planned!")

            
            st.subheader("🛣️ Route Information")
            route = data.get("route", {})
            
            distance = route.get("distance_km")
            duration = route.get("duration_min")
            steps = route.get("steps")
            
            if distance is not None and duration is not None and steps:
                st.markdown(f"**From:** {source} → **To:** {destination}")
                st.markdown(f"**Distance:** {distance} km")
                st.markdown(f"**Duration:** {duration} minutes")
                st.markdown("**Steps:**")
                for step in steps:
                    st.markdown(f"- {step}")
            else:
                st.warning("⚠️ Could not fetch route information. Please try manually below.")



            # Coordinates
            st.subheader("📍 Coordinates")
            st.json({
                "source": data.get("source_coordinates"),
                "destination": data.get("destination_coordinates")
            })

            #  Weather Forecast
            st.subheader("🌦️ Weather Forecast at Destination")
            for forecast in data["weather"]["forecast"]:
                st.markdown(
                    f"{forecast['datetime']} | {forecast['description']} | 🌡️ {forecast['temperature']}°C | 💨 {forecast['wind_speed']} m/s"
                )

            # Attractions
            st.subheader("🏞️ Attractions / POIs")
            if data["places"]:
                for p in data["places"]:
                    st.markdown(f"**{p['name']}** — {p['type']}")
            else:
                st.info("No major attractions found.")

            # Recommendations
            st.subheader("🏨 Recommendations")
            if data["recommendations"]:
                for rec in data["recommendations"]:
                    st.markdown(f"**{rec['name']}** ({rec['category']})")
            else:
                st.info("No specific recommendations found.")

            # Budget Info
            st.subheader("💰 Budget Estimate")
            budget_data = data["budget"]
            st.metric("Hotel", f"₹{budget_data['total_hotel']}")
            st.metric("Food", f"₹{budget_data['total_food']}")
            st.metric("Transport", f"₹{budget_data['total_transport']}")
            st.metric("Total", f"₹{budget_data['total_budget_estimate']}")

        except Exception as e:
            st.error(f"Error occurred: {e}")

# Optional: Use /route API directly
st.markdown("---")
st.subheader("🧭 Optional: Manually Check Route")

with st.form("route_form"):
    col1, col2 = st.columns(2)
    with col1:
        start_lat = st.number_input("Start Latitude", value=18.5213738)
        start_lon = st.number_input("Start Longitude", value=73.8545071)
    with col2:
        end_lat = st.number_input("End Latitude", value=18.7503694)
        end_lon = st.number_input("End Longitude", value=73.4069436)

    mode = st.selectbox("Travel Mode", ["car", "bike", "foot"])
    route_submit = st.form_submit_button("Get Route")

if route_submit:
    try:
        route_url = f"{BACKEND_URL}/route"
        params = {
            "start_lat": start_lat,
            "start_lon": start_lon,
            "end_lat": end_lat,
            "end_lon": end_lon,
            "mode": mode
        }
        route_resp = requests.get(route_url, params=params)
        route_resp.raise_for_status()
        route_data = route_resp.json()

        st.success("📍 Route Fetched Successfully")
        st.markdown(f"**Distance:** {route_data['distance_km']} km")
        st.markdown(f"**Duration:** {route_data['duration_min']} minutes")
        st.markdown("**Steps:**")
        for step in route_data["steps"]:
            st.markdown(f"- {step}")

    except Exception as e:
        st.error(f"Error fetching route: {e}")
