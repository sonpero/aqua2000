import json
from datetime import datetime
# import time 
import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
from streamlit_autorefresh import st_autorefresh



st.set_page_config(layout="wide", page_title="Aqua2000")
# Apply custom CSS
# st.markdown(
#     """
#     <style>
#     .main-title {
#         font-family: 'Helvetica', sans-serif;
#         font-size: 3em;
#         color: #4CAF50;
#         text-align: center;
#         margin-top: 20px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Autorefresh:
count = st_autorefresh(interval=5000, limit=100, key="fizzbuzzcounter")

# Display the styled title
st.markdown("<h1 class='main-title'>Aqua2000</h1>", unsafe_allow_html=True)


# Add a subheader or tagline
st.subheader("Your one-stop solution for amazing content")

# Optionally, add more content or interactive elements below
st.write("Here you can add more details about your website...")

logo = Image.open("poisson.jpeg")
logo = logo.resize((200, 100))  # and make it to whatever size you want.

# Row A
a1, a2, a3 = st.columns(3)
a1.image(logo)
a2.metric("Stockholm Temperature", f"{10}", f"{-0.5}" + "%")
current_time = datetime.now().strftime("%H:%M:%S")
a3.metric("Paris time", str(current_time))

# Row B
b1, b2, b3, b4 = st.columns(4)
b1.metric("Humidity", f"{20}" + "%")
b2.metric("Feels like", f"{3}")
b3.metric("Highest temperature", f"{17}")
b4.metric("Lowest temperature", f"{15}")

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    "what  you need on Aqua2000 ?", ("temperature", "lights", "camera")
)

# reading data
# Opening JSON file
f = open(
    "/Users/alex/Documents/VSCode_project/aqua2000/aqua2000/temperature_2024_06_14.json"
)

# returns JSON object as
# a dictionary
values = json.load(f)
sensor = values["sensor_name"]
sensor_values = values["measurements"]
print(sensor_values)

# create temperature tab
temperature_tab = pd.DataFrame(sensor_values)
temperature_tab.rename(columns={"value": "temperature"}, inplace=True)
temperature_tab["timestamp"] = pd.to_datetime(temperature_tab["timestamp"])
temperature_tab.set_index("timestamp", inplace=True)
temperature_tab["day"] = temperature_tab.index.date
temperature_tab["hour"] = temperature_tab.index.time

temperature_tab = temperature_tab.reset_index()
temperature_tab.drop(columns=["timestamp"], inplace=True)

# display tab
st.title("Temperature")
st.dataframe(temperature_tab.style.highlight_max(axis=0))

# temperature graph
temperature_graph = temperature_tab[["temperature", "hour"]]
temperature_graph["hour"] = pd.to_datetime(temperature_graph["hour"], format="%H:%M:%S")

# define min and max
y_min = temperature_graph["temperature"].min() - 0.5
y_max = temperature_graph["temperature"].max() + 0.5

# set chart
line_chart = (
    alt.Chart(temperature_graph)
    .mark_line()
    .encode(
        x="dayhoursminutes(hour):T",
        y=alt.Y(
            "temperature:Q", title="Temperature", scale=alt.Scale(domain=[y_min, y_max])
        ),
    )
    .properties(
        title="Temperature Over Time",
        width=600,
        height=400,
    )
)

# display chart
st.altair_chart(line_chart)
