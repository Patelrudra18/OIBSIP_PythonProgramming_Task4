import streamlit as st
import requests
import datetime

API_KEY = "49170f8b19acd6577fa582f2c463d65f"
BASE_URL = "https://api.openweathermap.org/data/2.5"

ICONS = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Drizzle": "🌦️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Haze": "🌫️",
    "Fog": "🌫️",
    "Smoke": "💨",
}

POPULAR_CITIES = [
    "Ahmedabad",
    "Mumbai",
    "Delhi",
    "Bangalore",
    "Chennai",
    "Hyderabad",
    "Kolkata",
    "Pune",
    "Surat",
    "Jaipur",
]


def get_wind_dir(deg):
    return ["N", "NE", "E", "SE", "S", "SW", "W", "NW"][round(deg / 45) % 8]


def fetch_current(city, units):
    url = f"{BASE_URL}/weather?q={city}&appid={API_KEY}&units={units}"
    r = requests.get(url, timeout=10)
    return r.status_code, r.json()


def fetch_forecast(city, units):
    url = f"{BASE_URL}/forecast?q={city}&appid={API_KEY}&units={units}&cnt=40"
    r = requests.get(url, timeout=10)
    return r.status_code, r.json()


st.set_page_config(
    page_title="Weather App | OIBSIP",
    page_icon="🌤️",
    layout="centered",
)

st.markdown(
    """
    <style>
        .weather-card {
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            margin-bottom: 16px;
        }
        .city-name  { font-size: 22px; color: #aaa; margin-bottom: 4px; }
        .weather-icon { font-size: 72px; margin: 10px 0; }
        .temp-main  { font-size: 64px; font-weight: 800; color: white; margin: 0; }
        .weather-desc { font-size: 18px; color: #ccc; margin: 6px 0; }
        .feels-like { font-size: 14px; color: #999; }
        .detail-box {
            background: #16213e;
            border-radius: 12px;
            padding: 14px;
            text-align: center;
        }
        .detail-val  { font-size: 20px; font-weight: 700; color: #e2b96f; }
        .detail-name { font-size: 12px; color: #888; margin-top: 4px; }
        .fc-box {
            background: #16213e;
            border-radius: 12px;
            padding: 12px 8px;
            text-align: center;
            min-height: 140px;
        }
        .fc-day  { font-size: 12px; color: #aaa; }
        .fc-icon { font-size: 28px; margin: 8px 0; }
        .fc-temp { font-size: 13px; color: #ddd; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("## 🌤️ Weather App")
st.markdown("*Oasis Infobyte Internship | OIBSIP*")
st.divider()

if API_KEY == "49170f8b19acd6577fa582f2c463d65f":
    st.info("Your API key is added in the code. If the app still shows an API error, wait a few minutes and try again.")

col1, col2 = st.columns([3, 1])

with col1:
    selected_city = st.selectbox("🏙️ Choose City", POPULAR_CITIES, index=0)
    custom_city = st.text_input("Or enter any city", placeholder="e.g. London, Dubai, New York")

with col2:
    unit_label = st.radio("Unit", ["°C", "°F"], horizontal=True)

units = "metric" if unit_label == "°C" else "imperial"
sym = unit_label

city = custom_city.strip() if custom_city.strip() else selected_city

if st.button("Get Weather", type="primary", use_container_width=True):
    if not city.strip():
        st.info("Enter a city name above and click Get Weather")
    else:
        try:
            status, data = fetch_current(city, units)

            if status == 401:
                st.error("❌ Invalid API key.")
            elif status == 404:
                st.error(f"❌ City '{city}' not found. Check spelling and try again.")
            elif status != 200:
                st.error("❌ Something went wrong. Please try again.")
            else:
                cond = data["weather"][0]["main"]
                desc = data["weather"][0]["description"].title()
                temp = round(data["main"]["temp"], 1)
                feels = round(data["main"]["feels_like"], 1)
                hum = data["main"]["humidity"]
                wind_s = round(data["wind"]["speed"], 1)
                wind_d = get_wind_dir(data["wind"].get("deg", 0))
                pres = data["main"]["pressure"]
                vis = round(data.get("visibility", 0) / 1000, 1)
                city_n = data["name"]
                country = data["sys"]["country"]
                sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
                sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")
                icon = ICONS.get(cond, "🌡️")

                alt_temp = round((temp * 9 / 5) + 32, 1) if sym == "°C" else round((temp - 32) * 5 / 9, 1)
                alt_sym = "°F" if sym == "°C" else "°C"

                st.markdown(
                    f"""
                    <div class="weather-card">
                        <div class="city-name">📍 {city_n}, {country}</div>
                        <div class="weather-icon">{icon}</div>
                        <div class="temp-main">{temp}{sym}</div>
                        <div class="weather-desc">{desc}</div>
                        <div class="feels-like">Feels like {feels}{sym} &nbsp;|&nbsp; Also {alt_temp}{alt_sym}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                d1, d2, d3, d4 = st.columns(4)
                details = [
                    (d1, "💧", f"{hum}%", "Humidity"),
                    (d2, "🌬️", f"{wind_s} m/s {wind_d}", "Wind"),
                    (d3, "📊", f"{pres} hPa", "Pressure"),
                    (d4, "👁️", f"{vis} km", "Visibility"),
                ]

                for col, ico, val, name in details:
                    col.markdown(
                        f"""
                        <div class="detail-box">
                            <div style="font-size:22px">{ico}</div>
                            <div class="detail-val">{val}</div>
                            <div class="detail-name">{name}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown("<br>", unsafe_allow_html=True)
                s1, s2 = st.columns(2)

                s1.markdown(
                    f"""
                    <div class="detail-box">
                        <div style="font-size:22px">🌅</div>
                        <div class="detail-val">{sunrise}</div>
                        <div class="detail-name">Sunrise</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                s2.markdown(
                    f"""
                    <div class="detail-box">
                        <div style="font-size:22px">🌇</div>
                        <div class="detail-val">{sunset}</div>
                        <div class="detail-name">Sunset</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                fstatus, fdata = fetch_forecast(city, units)
                if fstatus == 200 and fdata:
                    st.markdown("#### 📅 5-Day Forecast")

                    seen = {}
                    for item in fdata["list"]:
                        dt = datetime.datetime.fromtimestamp(item["dt"])
                        day = dt.strftime("%a\n%d %b")
                        ic = ICONS.get(item["weather"][0]["main"], "🌡️")
                        lo = round(item["main"]["temp_min"], 1)
                        hi = round(item["main"]["temp_max"], 1)

                        if day not in seen:
                            seen[day] = {"ic": ic, "lo": lo, "hi": hi}
                        else:
                            seen[day]["lo"] = min(seen[day]["lo"], lo)
                            seen[day]["hi"] = max(seen[day]["hi"], hi)

                    days = list(seen.items())[:5]
                    cols = st.columns(5)

                    for col, (day, v) in zip(cols, days):
                        col.markdown(
                            f"""
                            <div class="fc-box">
                                <div class="fc-day">{day}</div>
                                <div class="fc-icon">{v['ic']}</div>
                                <div class="fc-temp">⬇ {v['lo']}{sym}<br>⬆ {v['hi']}{sym}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                st.caption(f"Last updated: {datetime.datetime.now().strftime('%d %b %Y, %H:%M:%S')}")

        except requests.exceptions.ConnectionError:
            st.error("❌ No internet connection. Please check your network.")
        except Exception as e:
            st.error("❌ Something went wrong. Please try again.")
            st.caption(str(e))

st.markdown("---")
st.caption("Patel Rudra | AICTE OIB-SIP May 2026 | Python Programming Internship")