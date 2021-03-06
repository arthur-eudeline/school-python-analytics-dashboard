import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from src import utils


# Génère les graphiques d'évolution grâce à une date de début,
# une date de fin et le dataframe
from src import htmlComponents


def getFig(df: pd.DataFrame, startDate=None, endDate=None):
    # Reformate les date de fin pour les utiliser dans df.loc
    startDate = utils.convertDate(startDate, df, True)
    endDate = utils.convertDate(endDate, df, False)

    # Evite les erreurs axe same-length car on fait l'indexing par
    # date après avoir fait la requête
    dataSessions = df[['ga:sessions']].groupby(df.index).sum()
    dataTransactions = df[['ga:transactions']].groupby(df.index).sum()

    # Créer les graphiques avec les start et end dates
    figureSessionEvolution = px.line(
        dataSessions.loc[startDate:endDate],
        labels={
            'ga:date': 'Date',
            'ga:sessions': 'Nombre de sessions',
            'value': 'Nombre de sessions',
            'variable': 'Légende',
        },
        color_discrete_map={'ga:sessions': '#74b9ff'}
    )
    figureSessionEvolution.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    figureTransactionEvolution = px.line(
        dataTransactions.loc[startDate:endDate],
        labels={
            'ga:date': 'Date',
            'ga:transactions': 'Nombre de transactions',
            'value': 'Nombre de transactions',
            'variable': 'Légende',
        },
        color_discrete_map={'ga:transactions': '#74b9ff'}
    )
    figureTransactionEvolution.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # On return un tuple (example : getFig()[0])
    return figureSessionEvolution, figureTransactionEvolution


# Génère le HTML à injecter dans le app.layout
def build(df):
    return html.Div(
        className="row",
        children=[
            htmlComponents.graphCard(
                title="Évolution du nombre de sessions",
                children=dcc.Graph(
                    id="sessions-evolution-graph",
                    figure={},
                ),
            ),
            htmlComponents.graphCard(
                title="Évolution du nombre de transactions",
                children=dcc.Graph(
                    id="transactions-evolution-graph",
                    figure={},
                ),
            ),
        ]
    )


# Déclare les output à appeler dans le app.callback
def output():
    return [
        Output(
            component_id="sessions-evolution-graph",
            component_property="figure"
        ),
        Output(
            component_id="transactions-evolution-graph",
            component_property="figure"
        )
    ]


# Fonction qui met à jour les graphiques en fonction de la nouvelle
# date de début et de fin qui lui est donné
def update(df: pd.DataFrame, startDate, endDate):
    return getFig(df, startDate, endDate)
