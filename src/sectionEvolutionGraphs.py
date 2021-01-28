import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px


def build(df):
    figureSessionEvolution = px.line(df[['ga:sessions']].groupby(df.index).sum())
    figureTransactionEvolution = px.line(df[['ga:transactions']].groupby(df.index).sum())

    return html.Div([
        dcc.Graph(
            id="sessions-evolution-graph",
            figure=figureSessionEvolution
        ),
        dcc.Graph(
            id="transactions-evolution-graph",
            figure=figureTransactionEvolution
        )
    ])
