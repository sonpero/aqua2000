import json
import fcntl

from datetime import datetime

import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
from streamlit_autorefresh import st_autorefresh


st.set_page_config(layout="wide", page_title="Aqua2000")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Autorefresh:
count = st_autorefresh(interval=5000, key="fizzbuzzcounter")

# logo aqua 2000
logo = Image.open("logo_aqua2000.png")
logo = logo.resize((400, 200))

# Row A
a1, a2, a3 = st.columns(3)
a1.image(logo)
a2.metric("Last Temperature", f"{10}", f"{-0.5}" + "%")
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
current_date = datetime.now().strftime("%Y_%m_%d")
year = datetime.now().strftime("%Y")
path_to_temperature = f"/Volumes/aqua2000/{year}/temperature_{current_date}.json"

with open(path_to_temperature, 'r') as file:
    # Shared lock for reading
    fcntl.flock(file, fcntl.LOCK_SH) 
    # returns JSON object as
    # a dictionary
    values = json.load(file)
    # Unlock the file
    fcntl.flock(file, fcntl.LOCK_UN)


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

# Row C
c1, c2 = st.columns(2)
c1.write("temperature")
c1.dataframe(temperature_tab.style.highlight_max(axis=0))


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
        width=500,
        height=400,
    )
)

c2.altair_chart(line_chart)
