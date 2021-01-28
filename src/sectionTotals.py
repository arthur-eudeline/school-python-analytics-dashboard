import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

import utils


# Calcule les différents totaux en fonction de la date de début et de fin
from src import htmlComponents


def getTotals(df: pd.DataFrame, startDate=None, endDate=None):
    # Reformate les date de fin pour les utiliser dans df.loc
    startDate = utils.convertDate(startDate, df, True)
    endDate = utils.convertDate(endDate, df, False)

    # Différents totaux
    totalUsers = df.loc[startDate:endDate]['ga:users'].sum()

    totalSessions = df.loc[startDate:endDate]['ga:sessions'].sum()

    totalTransactions = df.loc[startDate:endDate]['ga:transactions'].sum()

    totalRevenues = round(
        df.loc[startDate:endDate]['ga:transactionRevenue'].sum(),
        2
    )

    # Calcul du total de taux de convertion
    totalConversion = totalTransactions / totalSessions * 100
    totalConversion = round(totalConversion, 2)
    totalConversion = str(totalConversion) + "%"

    return totalUsers, totalSessions, totalTransactions, totalRevenues, totalConversion


# Génère les éléments HTML
def build(df: pd.DataFrame):
    totals = getTotals(df)
    content = htmlComponents.totalCardsWrapper([
        htmlComponents.totalCard(
            label="Total utilisateurs",
            value=totals[0],
            id="total-users"
        ),
        htmlComponents.totalCard(
            label="Total sessions",
            value=totals[1],
            id="total-sessions"
        ),
        htmlComponents.totalCard(
            label="Total transactions",
            value=totals[2],
            id="total-transactions"
        ),
        htmlComponents.totalCard(
            label="Chiffre d'affaire total",
            value=totals[3],
            id="total-revenues"
        ),
        htmlComponents.totalCard(
            label="Taux de conversion",
            value=totals[4],
            suffix="%",
            id="total-conversion"
        ),
    ])

    return html.Div([content], className="row")


# Outputs à utiliser pour le @app.callback
def output():
    return [
        Output(
            component_id="total-users",
            component_property="children"
        ),
        Output(
            component_id="total-sessions",
            component_property="children"
        ),
        Output(
            component_id="total-transactions",
            component_property="children"
        ),
        Output(
            component_id="total-revenues",
            component_property="children"
        ),
        Output(
            component_id="total-conversion",
            component_property="children"
        ),
    ]


# Permet de mettre à jour les différents totaux
def update(df: pd.DataFrame, startDate, endDate):
    return getTotals(df, startDate, endDate)