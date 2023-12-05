# Import necessary libraries
import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from src.read_data import rat_sightings, resurant_inspections
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go

data = rat_sightings()
resturant_data = resurant_inspections()
# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

def apply_standard_layout(fig):
    standard_layout = go.Layout(
        font=dict(family="Arial, sans-serif", size=12, color="black"),
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )
    fig.update_layout(standard_layout)
    return fig

# Set Mapbox token
mapbox_token = 'pk.eyJ1IjoiZXRyYXV0c2NoIiwiYSI6ImNscGo3ems1djA1bGcybW52c3RyNzVqc3IifQ.HTNefJHbqlRr9kxjS60HcA'

# Ensure the date column is in datetime format
data['year'] = pd.to_datetime(data['Created Date']).dt.year
data = data.sort_values(by='year')

# Cumulatively append data for each year
cumulative_data = pd.DataFrame()
for year in data['year'].unique():
    yearly_data = data[data['year'] <= year].copy()
    yearly_data['animation_year'] = year  # add a column to indicate the animation frame
    cumulative_data = pd.concat([cumulative_data, yearly_data])

# Define the first story page layout
def story_page_zero():
    return html.Div([
    html.Div(
        className="jumbotron text-center",
        children=[
            html.H1("Rats in New York City", className="display-4"),
            html.P("Welcome to our exploration of rat sightings in the Big Apple. New York City, known for its vibrant culture and towering skyscrapers, also has a hidden resident – rats. Join us as we delve into the world of rat sightings from the perspective of its citizens.Welcome to our interactive dashboard on rat sightings in our community. Through detailed charts, uncover trends, locations, and response efforts related to rat sightings. Gain insights to understand this urban challenge better and learn what you can do to help address it effectively.", className="lead"),
        ],
    ),
    dcc.Location(id='url', refresh=False),
])



# Define the first story page layout
def story_page_one():

    # Create the animated scatter mapbox plot
    fig = px.scatter_mapbox(cumulative_data, 
                            lat="Latitude", 
                            lon="Longitude", 
                            animation_frame="animation_year", 
                            #color="some_other_column", 
                            #size="another_column",
                            hover_name="Unique Key",
                            # hover_data=['Complaint Type', 'Descriptor', 'Street Name', 'Borough'], 
                            zoom=9,
                            mapbox_style="open-street-map",
                            color_discrete_sequence=['gray']
                            )
    fig.update_traces(
        marker=dict(
            size=3,  # Smaller points, adjust size as needed
            color='gray',  # Monochrome color, you can adjust the shade as needed
            opacity=0.7,  # Adjust opacity for better visibility if needed
            symbol='circle'
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
        ),
        mapbox_style="open-street-map",  # A monochrome-like, light-colored style
        showlegend=False,
        transition={'duration': 30000},  # Transition duration in milliseconds
    )

    # Prevent automatic animation start and add custom buttons
    fig.layout.updatemenus = [
        dict(
            type="buttons",
            showactive=False,
            buttons=[
                dict(label="Play",
                    method="animate",
                    args=[None, {"frame": {"duration": 3000, "redraw": True}, "fromcurrent": True}]),
            ],
        )
    ]

    # Set the initial frame to the first frame (adjust as needed)
    fig.layout.sliders[0].steps[0]['args'][1]['frame']['duration'] = 0

    return html.Div([
        # Use a single column layout

        html.P("Explore the evolving landscape of rat sightings in our community since 2010", className="lead"),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id='map-animation', 
                    figure=fig, 
                    config={'displayModeBar': False}, 
                    style={'height': '650px'}
                )
            ], width=12, className="d-flex justify-content-center")  # Center the column
        ], justify="center", align="center", className="h-100"),  # Center the row
    ], className="container-fluid")  # Use full width of the screen

def story_page_eda():
    data['Created Date'] = pd.to_datetime(data['Created Date'])
    data['Closed Date'] = pd.to_datetime(data['Closed Date'])

    # Aggregate     data by borough and count the occurrences
    borough_counts = data['Borough'].value_counts().reset_index()
    borough_counts.columns = ['Borough', 'Count']

    # Sort by count
    borough_counts = borough_counts.sort_values(by='Count', ascending=False)

    # Plot using the sorted data
    fig2 = px.bar(borough_counts, x='Borough', y='Count', title='Rat Sighting Frequency per Borough')
    fig2 = apply_standard_layout(fig2)

    data['DAY_OF_WEEK'] = data['Closed Date'].dt.day_name()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    data['DAY_OF_WEEK'] = pd.Categorical(data['Closed Date'].dt.day_name(), categories=day_order, ordered=True)

    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    data['MONTH'] = pd.Categorical(data['Closed Date'].dt.month_name(), categories=month_order, ordered=True)

    fig3 = px.histogram(data, x='DAY_OF_WEEK', title='Rat Sightings by Day of the Week')
    fig3 = apply_standard_layout(fig3)

    fig4 = px.histogram(data, x='MONTH', title='Rat Sightings by Month')
    fig4 = apply_standard_layout(fig4)

    fig3.update_layout(
    xaxis=dict(
        categoryorder='array',
        categoryarray=day_order
    )
)

    fig4.update_layout(
        xaxis=dict(
            categoryorder='array',
            categoryarray=month_order
        )
    )


    return dbc.Container([
    dbc.Row([
        html.P("Notice the frequency of Rat Sightings over the Boroughs, Brooklyn having the largest proportion", className="lead"),
        dbc.Col(dcc.Graph(id='frequency-borough-chart', figure=fig2), width=12)
    ]),
    
    dbc.Row([
        html.P("Sightings are rarely on the weekend, during the week sightings are more likely to be recorded and logged", className="lead"),
        dbc.Col(dcc.Graph(id='day-of-week-chart', figure=fig3), width=12)
    ]),
    
    dbc.Row([
        html.P("Notice a decrease in sightings over the Winter months, with the population increasing throughout the Spring and Summer", className="lead"),
        dbc.Col(dcc.Graph(id='time-of-year-chart', figure=fig4), width=12)
    ]),
], fluid=True)

# Define the second story page layout
def story_page_two():
    return html.Div([
    html.P("Select your borough community board to learn more about rat sightings in your neighborhood"),

    dcc.Dropdown(
        id='borough-dropdown',
        options=[{'label': b, 'value': b} for b in rat_sightings()['Borough'].unique()],
        placeholder="Select a Borough"
    ),
    dcc.Dropdown(
        id='community-dropdown',
        placeholder="Select a Community Board"
    ),

    # Conditional rendering of Graphs
    html.Div(id='visualization-container'),

    # Note at the bottom of the page
    html.Div([
        html.P("Note: Data collection practices may have changed in recent years. This has led to fewer sightings being attributed to unspecified community boards, resulting in a significant increase in sightings tracked over the past few years")
    ], style={'textAlign': 'center', 'marginTop': '20px', 'fontSize': '0.9em'})
])

# Callback to display the graphs when options are selected
@app.callback(
    Output('visualization-container', 'children'),
    [Input('borough-dropdown', 'value'), Input('community-dropdown', 'value')]
)
def update_graphs(borough, community_board):
    if borough and community_board:
        # Update visualizations based on selections
        map_figure, additional_figure, final_fig = update_visualizations(borough, community_board) 
        return [
            html.Div([
                # Map on top
                html.Div([
                    dcc.Graph(id='map', figure=map_figure)
                ], className='row'),

                # Line chart and bar graph next to each other below the map
                html.Div([
                    # Line Chart
                    html.Div([
                        dcc.Graph(id='line-chart', figure=additional_figure)
                    ], className='col-md-6'),

                    # Bar Graph
                    html.Div([
                        dcc.Graph(id='bar-graph', figure=final_fig)
                    ], className='col-md-6')
                ], className='row')
            ], className='container-fluid')
        ]
    return html.Div("Select both a borough and a community board to display the visualizations.", style={'textAlign': 'center', 'marginTop': '10px'})

# Callback to populate the community dropdown based on the selected borough
@app.callback(
    Output('community-dropdown', 'options'),
    Input('borough-dropdown', 'value')
)
def set_community_options(selected_borough):
    if selected_borough is not None:
        filtered_data = data[data['Borough'] == selected_borough]
        return [{'label': cb, 'value': cb} for cb in sorted(filtered_data['Community Board'].unique()) if selected_borough in cb]
    return []

# Define a function to update visualizations
def update_visualizations(selected_borough, selected_community):
    filtered_data = data[(data['Borough'] == selected_borough) & (data['Community Board'] == selected_community)]

    # Assuming filtered_data is already defined
    filter_data = filtered_data.copy()
    filter_data['Date'] = pd.to_datetime(filter_data['Created Date'])    
    filter_data = filter_data[filter_data['Date'].dt.year <= 2018]

    data_line = filter_data.groupby([filter_data['Date'].copy().dt.year, 'Complaint Type']).size().reset_index(name='Counts')

    # Mapbox Chart
    map_fig = px.scatter_mapbox(filtered_data, lat='Latitude', lon='Longitude', color='Complaint Type',
                                hover_name='Complaint Type', zoom=12,
                                title=f'Geographical Distribution of Complaints in {selected_community}',
                                hover_data=['Complaint Type', 'Descriptor', 'Street Name'], 
                                mapbox_style='open-street-map', 
                                color_discrete_sequence=['gray'])

    line_fig = px.line(data_line, x='Date', y='Counts', color='Complaint Type', title=f'Complaints Over Time in {selected_community}')
    line_fig = apply_standard_layout(line_fig)

    # Convert 'Created Date' and 'Closed Date' to datetime
    filter_data['Created Date'] = pd.to_datetime(filter_data['Created Date'])
    filter_data['Closed Date'] = pd.to_datetime(filter_data['Closed Date'])

    # Calculate the difference in days
    filter_data['Time to Close'] =(filter_data['Closed Date'] - filter_data['Created Date']).dt.days

    # Filter out negative or nonsensical values (if any)
    filter_data = filter_data[filter_data['Time to Close'] >= 0]

    # Group by month or year (here we use month)
    filter_data['Month'] = filter_data['Created Date'].dt.to_period('M')
    average_time_to_close = filter_data.groupby('Month')['Time to Close'].mean().reset_index()

    # Convert 'Month' back to datetime for plotting
    average_time_to_close['Month'] = average_time_to_close['Month'].dt.to_timestamp()

    close_fig = px.line(average_time_to_close, x='Month', y='Time to Close',
                title=f'Average Time to Close Rat Complaints In {selected_community}',
                labels={'Month': 'Month', 'Time to Close': 'Average Time to Close (days)'})
    close_fig = apply_standard_layout(close_fig)


    return map_fig, line_fig, close_fig

def story_page_three():
    return html.Div([
        html.H2("Story Page Two"),
        dcc.Graph(
            figure={
                'data': [{'x': [6, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'NYC'}],
                'layout': {'title': 'Another Dash Data Visualization'}
            }
        ),
    ])

def story_page_four():
    return html.Div([

    html.P("Discover insights into the correlation between rat sightings and restaurants with critical health violations", className="lead"),
    dbc.Row(
        dbc.Col(
            html.Img(
                src='/assets/food_and_rats.png',  # Path to your image
                style={'width': '100%'},
            ),
            # width={'size': 6, 'offset': 3}  # Center the column horizontally
        ),
    ),
])

def final_page():
    return html.Div(
        style={
            'fontFamily': 'Arial, sans-serif',
            'textAlign': 'center',
            'margin': '20px'
        },
        children=[
            #html.H2("What YOU can do", style={'color': '#4A4A4A'}),
            html.Div(
                dcc.Link(
                    'Learn more about direct actions you can take',
                    href='https://www.nyc.gov/site/doh/health/health-topics/rats.page',
                    style={
                        'display': 'block',
                        'marginBottom': '10px',
                        'color': '#1a73e8',
                        'textDecoration': 'none'
                    }
                ),
                style={'marginBottom': '20px'}
            ),
            html.Div(
                dcc.Link(
                    'Contact your community board!',
                    href='https://www.nyc.gov/site/cau/community-boards/community-boards.page',
                    style={
                        'display': 'block',
                        'marginBottom': '10px',
                        'color': '#1a73e8',
                        'textDecoration': 'none'
                    }
                ),
                style={'marginBottom': '20px'}
            ),
            html.Div(
                dcc.Link(
                    'Compost',
                    href='https://www.nyc.gov/assets/dsny/site/services/organics',
                    style={
                        'display': 'block',
                        'marginBottom': '10px',
                        'color': '#1a73e8',
                        'textDecoration': 'none'
                    }
                ),
                style={'marginBottom': '20px'}
            ),
            html.H5('Continue to combat the rat population in NYC!', style={'color': '#2B2B2B'})
        ]
    )

def data_source_section():
    return dbc.Container(
        [
            html.Hr(),
            html.P("Data Sources:", style={'font-weight': 'bold'}),
            html.Ul([
                html.Li(html.A("Rat Sightings Dataset", href="https://data.cityofnewyork.us/SocialServices/Rat-Sightings/3q43-55fe", target="_blank"), style={'margin-bottom': '10px'}),
                html.Li(html.A("New York City Restaurant Inspection Results", href="https://data.cityofnewyork.us/Health/DOHMHNew-York-City-Restaurant-Inspection-Results/43nn-pn8j", target="_blank")),
            ]),
        ],
        className="footer"
    )

# Define the layout of the app
# app.layout = dbc.Container(
#     [
#     html.Div([
#     html.Div([
#     # Logo and text field in a container
#     html.Div(
#         className="container-fluid",
#         children=[
#             html.Div(
#                 className="row",
#                 children=[
#                     # Logo column
#                     html.Div(
#                         className="col-2",
#                         children=[
#                             html.Img(src="assets/ratlogo.png", alt="Logo", className="img-fluid"),
#                         ],
#                     ),
#                     # Text field column
#                 ],
#             ),
#         ],
#     ),
# ]),
#     html.Div(id='page-content'),

# html.Div([
#     # Story slides with borders and padding
#     html.Div(id='slide1', className='story-slide', children=[
#         html.H1('', className='slide-heading'),
#         story_page_zero(),
#         # Add your content for Story Slide 1 here
#     ]),
#     html.Div(id='slide2', className='story-slide', children=[
#         html.H1('Rat Sightings Over Time', className='jumbotron text-center display4'),
#         # Add your content for Story Slide 2 here
#         story_page_one(),
#     ]),

#     html.Div(id='slide4', className='story-slide', children=[
#         html.H1('Public Health and Rat Sightings', className='jumbotron text-center display4'),
#         story_page_four(),
#     ]),
#     html.Div(id='slide5', className='story-slide', children=[
#         html.H1('Rat Sightings by Community Board', className='jumbotron text-center display4'),
#         story_page_two(),
#     ]),

#     html.Div(id='slide6', className='story-slide', children=[
#         html.H1('What You Can Do', className='jumbotron text-center display4'),
#         final_page(),
#     ]),
#     html.Div(id='slide3', className='story-slide', children=[
#         html.H1('Insights About Rat Sightings Data', className='jumbotron text-center display4'),
#         # Add your content for Story Slide 2 here
#         story_page_eda(),
#     ]),
#      html.Div(id='slide7', className='story-slide', children=[
#         html.H1('The Data', className=''),
#         dbc.Container([
#     html.Hr(),
#         html.P("Data Sources:", style={'font-weight': 'bold'}),
#         html.Ul([
#             html.Li(html.A("Rat Sightings Dataset", 
#                         href="https://data.cityofnewyork.us/SocialServices/Rat-Sightings/3q43-55fe", 
#                         target="_blank"), 
#                     style={'margin-bottom': '10px'}),
#             html.Li(html.A("New York City Restaurant Inspection Results", 
#                         href="https://data.cityofnewyork.us/Health/DOHMHNew-York-City-Restaurant-Inspection-Results/43nn-pn8j", 
#                         target="_blank"))
#         ]),
#         ], className="footer")
#     ]),
    
# ])


# ])
#     ],
#     className='p-3',  # This applies padding to all sides of the container
# )
app.layout = dbc.Container(
    [
        # Logo and Header Section
        html.Div(
            [
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src="assets/ratlogo.png", alt="Logo", className="img-fluid"), width=2),
                                # Additional elements for the header can be added here
                            ],
                        ),
                    ],
                    className="container-fluid",
                ),
            ],
            className="header-section",
        ),

        # Main Content Section
        html.Div(id='page-content'),

        # Story Slides Section
        html.Div(
            [
                html.Div(id='slide1', className='story-slide', children=[story_page_zero()]),
                html.Div(id='slide2', className='story-slide', children=[html.H1('Rat Sightings Over Time', className='jumbotron text-center display-4'), story_page_one()]),
                html.Div(id='slide4', className='story-slide', children=[html.H1('Public Health and Rat Sightings', className='jumbotron text-center display-4'), story_page_four()]),
                html.Div(id='slide5', className='story-slide', children=[html.H1('Rat Sightings by Community Board', className='jumbotron text-center display-4'), story_page_two()]),
                html.Div(id='slide6', className='story-slide', children=[html.H1('What You Can Do', className='jumbotron text-center display-4'), final_page()]),
                html.Div(id='slide3', className='story-slide', children=[html.H1('Insights About Rat Sightings Data', className='jumbotron text-center display-4'), story_page_eda()]),
                html.Div(id='slide7', className='story-slide', children=[html.H1('The Data', className='text-center'), data_source_section()]),
            ],
            className="story-section",
        ),
    ],
    className='p-3',
)


# JavaScript for smooth scrolling
app.clientside_callback(
    """
    function scrollToSection(id) {
        const element = document.querySelector(id);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth' });
        }
        return false;  // Prevent default link behavior
    }
    """,
    Output('section1', 'children'),  # Use any Output component
    Input('section1', 'n_clicks_timestamp'),  # Use any Input component
)
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
