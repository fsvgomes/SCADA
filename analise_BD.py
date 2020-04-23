import sqlite3
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html

# Create your connection.
cnx = sqlite3.connect('ammonit.db')

df = pd.read_sql_query("SELECT * FROM Tabela", cnx)

print(df.tail)

### DASH  #####
app = dash.Dash()

app.layout = html.Div([
    html.Div([
        html.Img(src="/assets/UFPB.jpg"),
        html.H2("Sistema Supervisório Estação Climática"),
        html.Img(src="/assets/CEAR.jpg")
    ], className='banner'),

    html.Div('Weather Station SCADA'),
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                {'x': df['vel_vento'], 'y': df['vel_vento'], 'type': 'bar', 'name': 'SF'}          
            ],
            'layout': {'title': 'Visualização de Dados Dash'}
        }
    )
#app.css.append.css({
#   'external_url':'https://codepen.io/chriddyp/pen/bWLwgP.css'
#})
])

if __name__ == '__main__':
    app.run_server(port=8010, debug=True)