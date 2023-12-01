# Import necessary libraries
import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from src.visualizations import html_text, fig
from src.read_data import rat_sightings
import plotly.express as px
import pandas as pd

df = rat_sightings()
# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Define the first story page layout
def story_page_zero():
    return html.Div([
    html.Div(
        className="jumbotron text-center",
        children=[
            html.H1("Rats in New York City", className="display-4"),
            html.P("Welcome to our exploration of rat sightings in the Big Apple. New York City, known for its vibrant culture and towering skyscrapers, also has a hidden resident – rats. Join us as we delve into the world of rat sightings from the perspective of its citizens.", className="lead"),
        ],
    ),
    dcc.Location(id='url', refresh=False),
])



# Define the first story page layout
def story_page_one():
    return html.Div([
        html.H2("Rat Sightings over Time", className="text-center mb-4"),  # Centered title with margin
        html.Div([
            # Iframe with adjusted height
            html.Iframe(srcDoc=html_text, width='100%', height='800px', className="mb-3"),  # Height adjusted
        ], className="row"),
        html.Div([
            html.Img(src='/assets/linechart.png'),  # Responsive image
        ], className="row mt-3"),  # Margin top for spacing
        # Add other components as needed
    ], className="container")  # Bootstrap container for overall layout



# Define the second story page layout
def story_page_two():
    return html.Div([
    html.H3("Community Board Data Visualization", className="text-center"),
    html.P("Select a borough and a community board to see their respective data visualizations."),

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
        map_figure, additional_figure = update_visualizations(borough, community_board) 
        return [
            dcc.Graph(figure=map_figure),
            dcc.Graph(figure=additional_figure)
        ]
    return html.Div("Select both a borough and a community board to display the visualizations.", style={'textAlign': 'center', 'marginTop': '10px'})

# Callback to populate the community dropdown based on the selected borough
@app.callback(
    Output('community-dropdown', 'options'),
    Input('borough-dropdown', 'value')
)
def set_community_options(selected_borough):
    if selected_borough is not None:
        data = rat_sightings()
        filtered_df = data[data['Borough'] == selected_borough]
        return [{'label': cb, 'value': cb} for cb in sorted(filtered_df['Community Board'].unique())]
    return []

# Define a function to update visualizations
def update_visualizations(selected_borough, selected_community):
    df = rat_sightings()
    filtered_df = df[(df['Borough'] == selected_borough) & (df['Community Board'] == selected_community)]

    # Assuming filtered_df is already defined
    filter_df = filtered_df.copy()
    filter_df['Date'] = pd.to_datetime(filter_df['Created Date'])    
    filter_df = filter_df[filter_df['Date'].dt.year <= 2018]

    df_line = filter_df.groupby([filter_df['Date'].copy().dt.year, 'Complaint Type']).size().reset_index(name='Counts')

    line_fig = px.line(df_line, x='Date', y='Counts', color='Complaint Type', title='Complaints Over Time')

    # Mapbox Chart
    map_fig = px.scatter_mapbox(filtered_df, lat='Latitude', lon='Longitude', color='Complaint Type',
                                hover_name='Complaint Type', zoom=12,
                                title='Geographical Distribution of Complaints',
                                mapbox_style='open-street-map')

    return map_fig, line_fig

        
        
        
        # Add other components as needed
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
        html.H2("Story Page Two"),
        dcc.Graph(
            figure={
                'data': [{'x': [1, 2, 6], 'y': [2, 4, 5], 'type': 'bar', 'name': 'NYC'}],
                'layout': {'title': 'Another Dash Data Visualization'}
            }
        ),
    ])

def story_page_five():
    return html.Div(
        style={
            'fontFamily': 'Arial, sans-serif',
            'textAlign': 'center',
            'margin': '20px'
        },
        children=[
            html.H2("What YOU can do", style={'color': '#4A4A4A'}),
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


# Define the layout of the app
app.layout = dbc.Container(
    [
    html.Div([
    html.Div([
    # Logo and text field in a container
    html.Div(
        className="container-fluid",
        children=[
            html.Div(
                className="row",
                children=[
                    # Logo column
                    html.Div(
                        className="col-2",
                        children=[
                            html.Img(src="assets/ratlogo.png", alt="Logo", className="img-fluid"),
                        ],
                    ),
                    # Text field column
                ],
            ),
        ],
    ),
]),
    html.Div(id='page-content'),

html.Div([
    # Story slides with borders and padding
    html.Div(id='slide1', className='story-slide', children=[
        html.H1('', className='slide-heading'),
        story_page_zero(),
        # Add your content for Story Slide 1 here
    ]),
    html.Div(id='slide2', className='story-slide', children=[
        html.H1('Rat Sightings Over Time', className='slide-heading'),
        # Add your content for Story Slide 2 here
        story_page_one(),
    ]),
    html.Div(id='slide3', className='story-slide', children=[
        html.H1('Community Board', className='slide-heading'),
        story_page_two(),
    ]),
    html.Div(id='slide4', className='story-slide', children=[
        html.H1('Critical Resturant Violations', className='slide-heading'),
        story_page_three(),
    ]),
    html.Div(id='slide5', className='story-slide', children=[
        html.H1('', className='slide-heading'),
        story_page_five(),
    ]),
    
])


])
    ],
    className='p-3',  # This applies padding to all sides of the container
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
    app.run_server(debug=True, host='127.0.0.1', port=8050)
