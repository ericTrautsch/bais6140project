# Import necessary libraries
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from src.visualizations import html_text

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
        marks={1: 'Rats Over Time', 2: 'Sightings', 3: 'Critical Resturants', 4: 'Rodent Investigations', 5: 'Conclusions'},
        value=1,
    ),
    html.Div(id='page-content')
])
    ],
    className='p-3',  # This applies padding to all sides of the container
)
# Define the first story page layout
def story_page_one():
    return html.Div([
        html.H2("Rat Sightings over Time"),
            html.Iframe(srcDoc=html_text, width='100%', height='1200px'),
            html.Img(src='/assets/linechart.png')
        # Add other components as needed
    ])

# Define the second story page layout
def story_page_two():
    return html.Div([
        html.H2("Story Page Two"),
        dcc.Graph(
            figure={
                'data': [{'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'NYC'}],
                'layout': {'title': 'Another Dash Data Visualization'}
            }
        ),
    ])
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
    app.run_server(debug=True, host='0.0.0.0', port=8050)
