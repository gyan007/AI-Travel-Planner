# 🗺️ AI Travel Planner

This project lets users plan a personalized trip including:
- Top places to visit
- Weather forecast
- Hotel & food recommendations
- Route planning
- Budget estimation

## 🔧 Tech Stack
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **APIs**: OpenStreetMap, Yelp, OpenWeatherMap, OSRM

## 🚀 Run Locally

```bash
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   cd streamlit_ui
   streamlit run ui_app.py
