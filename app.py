import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import os
import unicodedata

df = pd.read_excel('ALMVP.xlsx', sheet_name='Sheet1')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

stats = ['WAR', 'H', 'RBI', 'BA', 'OBP', 'SLG']

colors = {
    'background': '#ffffff',
    'text': '#000000'
}

players = []

chosen = []

for i in df.index:
    rawName = df['Name'][i]
    editName = rawName[:-10]
    players.append(editName)
    

app.layout = html.Div([
    html.Div([
        html.Img(
            src='/assets/images/logo.svg',
            style={
                'display':'inline-block'
            } 
        ),

        html.H2(
    
            children='Breakdown of American League MVP Candidates (2018 Season)',
            style={
                'textAlign': 'center',
                'color': colors['text'],
                'display':'inline-block',
                'padding-left':'50px',
                'margin-top': '-100px'
            }
        )

    ]),
    

    html.Div([
        html.Div([
            html.H3(
                children='Choose player...'
            ),
            html.Div([
                dcc.Dropdown(
                    multi=True,
                    id="player-column",
                    options=[{'label': i, 'value': i} for i in players]
                )
            ]),
            html.Div(
                id ='player-pics'
            
            )
            
        ], className='four columns'),
        html.Div([
            html.H3(
                children='Select a stat...'
            ),

            html.Div([
                dcc.Dropdown(
                    id="stat-column",
                    options=[{'label': i, 'value': i} for i in stats],
                    value="WAR"
                ),
                dcc.Graph(id='model-graphic')
            ])
            
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
            toReturn.append( 
                html.Img(
                    alt= player,
                    src='/assets/images/%s.jpg' % player,
                    style={
                        'height': '200px',
                        'width': '150px',
                        'margin-top': '10px',
                        'margin-bottom': '10px',
                        'margin-right': '10px',
                        'margin-left': '10px'
                    },
                    
                )
            )
        #print(toReturn)
    
    return toReturn



@app.callback(
    dash.dependencies.Output('model-graphic', 'figure'),
    [dash.dependencies.Input('stat-column', 'value'),
    dash.dependencies.Input('player-column', 'value')]
)


def update_model(variable_column, player_column):
    selected_players = []
   
    if player_column is not None:
        selected_players = [x.encode('UTF8') for x in player_column]

    print(selected_players)

    return {

        'data': [go.Bar(
            x= selected_players,
            y=df[variable_column],
            marker=dict(
                color=['rgba(254, 44, 11, 1)',
                       'rgba(11, 80, 254, 1)',
                       'rgba(19, 221, 23, 1)',
                       'rgba(243, 109, 176, 1)',
                       'rgba(222, 233, 28, 1)',
                       'rgba(177, 51, 235, 1)',
                       'rgba(235, 140, 51, 1)']
            )
            
        )],

        'layout': go.Layout(
            xaxis={
                'title': 'MVP Candidates'

            },
            yaxis={
                'title': variable_column

            },
            margin={'l': 60, 'b': 100, 't': 60, 'r': 60},
            hovermode='closest'
        )
    }



if __name__ == '__main__':
    app.run_server(debug=True)
