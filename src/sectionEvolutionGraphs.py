import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


# Génère les graphiques d'évolution grâce à une date de début,
# une date de fin et le dataframe
def getFig(df: pd.DataFrame, startDate=None, endDate=None):
    if startDate is None:
        startDate = df.index.min()

    if endDate is None:
        endDate = df.index.max()

    # Reformate les date de fin pour les utiliser dans df.loc
    startDate = str(startDate).split(" ")[0]
    startDate = str(startDate).split("T")[0]
    endDate = str(endDate).split(" ")[0]
    endDate = str(endDate).split("T")[0]

    # Evite les erreurs axe same-length car on fait l'indexing par
    # date après avoir fait la requête
    dataSessions = df[['ga:sessions']].groupby(df.index).sum()
    dataTransactions = df[['ga:transactions']].groupby(df.index).sum()

    # Créer les graphiques avec les start et end dates
    figureSessionEvolution = px.line(dataSessions.loc[startDate:endDate])
    figureTransactionEvolution = px.line(dataTransactions.loc[startDate:endDate])

    # On return un tuple (example : getFig()[0])
    return figureSessionEvolution, figureTransactionEvolution


# Génère le HTML à injecter dans le app.layout
def build(df):
    return html.Div([
        dcc.Graph(
            id="sessions-evolution-graph",
            figure={}
        ),
        dcc.Graph(
            id="transactions-evolution-graph",
            figure={}
        )
    ])


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
