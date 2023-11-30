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

# Define the layout of the app
app.layout = app.layout = dbc.Container(
    [
    html.Div([
    html.H1("Rats, Rodents & NYC"),
    dcc.Slider(
        id='page-slider',
        min=1,
        max=5,
        step=1,
        marks={1: 'rats sightings over time', 2: 'sightings in YOUR community', 3: 'Critical Resturants', 4: 'Rodent Investigations', 5: 'Conclusions'},
        value=2,
    ),
    html.Div(id='page-content')
])
    ],
    className='p-3',  # This applies padding to all sides of the container
)
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
    df = rat_sightings()
    app.layout = html.Div([
    html.H3("Community Board Data Visualization", className="text-center"),
    html.P("Select a borough and a community board to see their respective data visualizations."),

    dcc.Dropdown(
        id='borough-dropdown',
        options=[{'label': b, 'value': b} for b in df['Borough'].unique()],
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
        html.P("Note: Data collection practices may have changed in recent years. This has led to fewer sightings being attributed to unspecified community boards, resulting in a significant increase in sightings tracked over the past few years.")
    ], style={'textAlign': 'center', 'marginTop': '20px', 'fontSize': '0.9em'})
])

# Callback to display the graphs only when options are selected
@app.callback(
    Output('visualization-container', 'children'),
    [Input('borough-dropdown', 'value'), Input('community-dropdown', 'value')]
)
def update_graphs(borough, community_board):
    if borough and community_board:
        # Assuming you have functions or methods to create your map and additional visualizations
        map_figure, additional_figure = update_visualizations(borough, community_board)  # Replace with your actual function
        return [
            dcc.Graph(figure=map_figure),
            dcc.Graph(figure=additional_figure)
        ]
    return html.Div("Select both a borough and a community board to display the visualizations.", style={'textAlign': 'center', 'marginTop': '10px'})


@app.callback(
    Output('community-dropdown', 'options'),
    Input('borough-dropdown', 'value'))
def set_community_options(selected_borough):
    if selected_borough is not None:
        data = rat_sightings()
        filtered_df = data[data['Borough'] == selected_borough]
        return sorted([cb for cb in filtered_df['Community Board'].unique()])
    return []

def update_visualizations(selected_community, selected_borough):
    if selected_community is not None and selected_borough is not None:
        # Filter data based on selections
        filtered_df = df[(df['Borough'] == selected_borough) & 
                           (df['Community Board'] == selected_community)]

        # Assuming filtered_df is already defined
        filter_df = filtered_df.copy()  # Create an independent copy of filtered_df
        filter_df['Date'] = pd.to_datetime(filter_df['Created Date'])  # Now it's safe to modify filter_df
        df_line = filter_df.groupby([filter_df['Date'].copy().dt.year, 'Complaint Type']).size().reset_index(name='Counts')

        # Use px.scatter instead of px.line to add a trendline
        line_fig = px.scatter(df_line, x='Date', y='Counts', color='Complaint Type', 
                            trendline="ols",  # Ordinary Least Squares regression line
                            title='Complaints Over Time')

        # Modify the line mode to connect data points
        line_fig.update_traces(mode='lines+markers')
        
        # Mapbox Chart
        map_fig = px.scatter_mapbox(filtered_df, lat='Latitude', lon='Longitude', color='Complaint Type',
                                    hover_name='Complaint Type', zoom=12,
                                    title='Geographical Distribution of Complaints',
                                    mapbox_style='open-street-map')


        return map_fig, line_fig
    return {}, {}

        
        
        
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



# Callback to update page content based on slider input
@app.callback(Output('page-content', 'children'),
              [Input('page-slider', 'value')])
def display_page(slider_value):
    if slider_value == 1:
        return story_page_one()
    elif slider_value == 2:
        return story_page_two()
    elif slider_value == 3:
        return story_page_three()
    elif slider_value == 4:
        return story_page_four()
    elif slider_value == 5:
        return story_page_five() 
    else:
        return '404 Page Not Found'

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8050)
