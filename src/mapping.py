#!/usr/bin/env python

"""
Create folium maps
"""
import numpy as np
import pandas as pd
import folium
import branca.colormap as cm
import pydeck as pdk
import streamlit as st

def create_map(data, year1, year2):
    """
    Takes a Data class instance as input
    """
    # create map
    fmap = folium.Map(
        tiles="Stamen Toner",
        location=[40.75, -73.9], 
        zoom_start=11,
    )

    # use colorscale normalized by all years values
    colormap = cm.LinearColormap(
        colors=['green', 'red'], 
    )

    # get the difference in consumption between two years
    diff = data.tds_by_year.loc[:, year1] - data.tds_by_year.loc[:, year2]

    # create markers colored by the difference in consumption
    for tds in diff.index:

        if not pd.isna(diff.loc[tds]):

            # get lat,long of this tds
            lat = data.coords[data.coords.tds == tds].latitude.values[0]
            lon = data.coords[data.coords.tds == tds].longitude.values[0]

            # add marker to this year
            marker = folium.Circle(
                location=[lat, lon],
                radius=150,
                color=colormap(diff.loc[tds]),
                fill=True,
                tooltip=folium.Tooltip(
                    text=f"tds={tds}, delta-consumption={diff.loc[tds]:.0f} KWH",
                )
            )
            fmap.add_child(marker)

    # show map
    return fmap

#to create a map built with pydeck
def create_hex_map(data):
    data = data[["latitude","longitude","consumption_hcf"]]
    midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))
    largest = int(data.consumption_hcf.max())
    st.write(data)
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",
        initial_view_state={
            "latitude": midpoint[0],
            "longitude": midpoint[1],
            "zoom": 11,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["longitude", "latitude"],
                radius=100,
                elevation_scale=1,
                elevation_range=[0, largest],
                pickable=True,
                extruded=True,
            ),
        ],
        #tooltip = {"text": "Consumption: {consumption_hcf}"},
    ))