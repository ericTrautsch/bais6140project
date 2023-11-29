import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import plotly


import src.read_data as read_data

mapbox_token = 'pk.eyJ1IjoiZXRyYXV0c2NoIiwiYSI6ImNscGo3ems1djA1bGcybW52c3RyNzVqc3IifQ.HTNefJHbqlRr9kxjS60HcA'


# Load your data
data = read_data.rat_sightings()

# Ensure the date column is in datetime format
data['year'] = pd.to_datetime(data['Created Date']).dt.year
data = data.sort_values(by='year')

# Cumulatively append data for each year
cumulative_df = pd.DataFrame()
for year in data['year'].unique():
    yearly_data = data[data['year'] <= year].copy()
    yearly_data['animation_year'] = year  # add a column to indicate the animation frame
    cumulative_df = pd.concat([cumulative_df, yearly_data])

# Create the animated scatter mapbox plot
fig = px.scatter_mapbox(cumulative_df, 
                        lat="Latitude", 
                        lon="Longitude", 
                        animation_frame="animation_year", 
                        #color="some_other_column", 
                        #size="another_column",
                        hover_name="year", 
                        zoom=10,
                        mapbox_style="open-street-map"
                        )
fig.update_traces(
    marker=dict(
        size=3,  # Smaller points, adjust size as needed
        color='gray',  # Monochrome color, you can adjust the shade as needed
        opacity=0.6  # Adjust opacity for better visibility if needed
    )
)

# Update the layout for a monochrome style
fig.update_layout(
    mapbox=dict(
        accesstoken=mapbox_token,  # Insert your Mapbox Access Token here
        style='light',  # Using a light map for a monochrome look
        center=dict(
            lon=data['Longitude'].mean(),
            lat=data['Latitude'].mean()
        ),
        zoom=8
    ),
    mapbox_style="open-street-map",  # A monochrome-like, light-colored style
    showlegend=False
)

fig.update_layout(
    transition={'duration': 4000},  # Transition duration in milliseconds
)

html_text = plotly.offline.plot(fig, output_type='div', include_plotlyjs=True)
