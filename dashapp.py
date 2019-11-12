import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Output, Input
import plotly.graph_objs as go

from analyze_tweets import TweetObject
from live_tweets import *


''''
export FLASK_ENV=development
python dashapp.py
'''

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


X = deque(maxlen=20)
Y0 = deque(maxlen=20)
Y1 = deque(maxlen=20)
Y2 = deque(maxlen=20)

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1*10000
        ),
    ]
)


@app.callback(
    Output('live-graph', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter(input_data):

    t = TweetObject( host='localhost', database='tweet', user='root')
    data  = t.MySQLConnect("SELECT created_at, tweet FROM `tweet`.`tweets`;")
    data = t.clean_tweets(data)

    data['Sentiment'] = np.array([t.sentiment(x) for x in data['clean_tweets']])

    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # neg_tweets[0][0][17:]
    dated_data = data[['date', 'clean_tweets']].to_dict('split')['data']
    pos_tweets = [tweet for index, tweet in enumerate(dated_data) if data["Sentiment"][index] > 0]
    neg_tweets = [tweet for index, tweet in enumerate(dated_data) if data["Sentiment"][index] < 0]
    neu_tweets = [tweet for index, tweet in enumerate(dated_data) if data["Sentiment"][index] == 0]

    print('X________', X, '\n','Y________',  Y)
    X.append(now)
    Y0.append(len(pos_tweets))
    Y1.append(len(neg_tweets))
    Y2.append(len(neu_tweets))

    trace0 = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(Y0),
        name='Scatter',
        mode='lines+markers'
    )
    trace1 = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(Y1),
        name='Scatter',
        mode='lines+markers'
    )
    trace2 = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(Y2),
        name='Scatter',
        mode='lines+markers'
    )
    data = [trace0, trace1, trace2]
    Y = [Y0, Y1, Y2]
    Y.sort()


    return {
        'data': data,
        'layout': go.Layout(
            xaxis=dict(range=[min(X), max(X)]),
            yaxis=dict(range=[min(Y), max(Y)])
        )
    }


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080 ,debug=True)
