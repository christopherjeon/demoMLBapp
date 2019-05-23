import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import os

df = pd.read_excel('ALMVP.xlsx', sheet_name='Sheet1')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

stats = ['WAR', 'H', 'RBI', 'BA', 'OBP', 'SLG']

colors = {
    'background': '#ffffff',
    'text': '#000000'
}

players = []

for i in df.index:
    rawName = df['Name'][i]
    editName = rawName[:-10]
    players.append(editName)
    

app.layout = html.Div([
    html.H1(
        children='Breakdown of American League MVP Candidates (2018 Season)',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    multi=True,
                    id="player-column",
                    options=[{'label': i, 'value': i} for i in players]
                )
            ]),
            html.Div(
                id ='player-pics',
                style={
                    'height': '25%'
                }
            )
            
        ], className='four columns'),
        html.Div([
            dcc.Dropdown(
                id="stat-column",
                options=[{'label': i, 'value': i} for i in stats],
                value="WAR"
            ),
            dcc.Graph(id='model-graphic')
        ], className='eight columns')
        
    ], className='row')
])



@app.callback(
    dash.dependencies.Output('player-pics', 'children'),
    [dash.dependencies.Input('player-column', 'value')]
)
def display_image(player_list):
    toReturn = []
    if player_list is not None:
        for player in player_list: 
            toReturn.append( html.Img(src='/assets/images/%s.jpg' % player))
        print('hello')
        print(toReturn)
    
    return toReturn



@app.callback(
    dash.dependencies.Output('model-graphic', 'figure'),
    [dash.dependencies.Input('stat-column', 'value')]
)


def update_model(variable_column):

    return {
        'data': [go.Scatter(
            x=players,
            y=df[variable_column],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.9,
                'line': {'width': 0.1, 'color': 'white'}
            }
        )],

        'layout': go.Layout(
            xaxis={
                'title': 'MVP Candidates'

            },
            yaxis={
                'title': variable_column

            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }



if __name__ == '__main__':
    app.run_server(debug=True)
