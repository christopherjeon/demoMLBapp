import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

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
    print editName

if __name__ == '__main__':
    app.run_server(debug=True)
