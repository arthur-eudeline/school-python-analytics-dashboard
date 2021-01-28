import json
import plotly.express as px
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd


def build(df):
    # ATTENTION : renommer les noms de régions en supprimant les caractères spéciaux
    # Pour savoir le nom des régions, faire `print(data)` (ex : "Bretagne" > "Brittany")
    fileContent = open('../include/france-regions.json')
    geoJson = json.load(fileContent)

    # Isole les transactions par région
    data = pd.DataFrame(df[['ga:region', 'ga:transactions']].groupby(['ga:region']).sum())

    fig = px.choropleth_mapbox(
        data,
        geojson=geoJson,
        locations=data.index, # data.index = Le nom des régions
        color='ga:transactions',
        # Défini les couleurs pour le plus bas de l'échelle (0) et le plus haut (1.0)
        color_continuous_scale=[
            [0, "rgb(196, 225, 255)"],
            [1.0, "rgb(9, 132, 227)"]
        ],
        mapbox_style="carto-positron",
        zoom=3,
        # Centre par défaut sur la France
        center={
            "lat": 46.71109,
            "lon": 1.7191036
        },
        opacity=0.75,
        # Légende
        labels={
            'ga:transactions': 'Transactions',
            'ga:region': 'Région'
        },
        featureidkey="properties.nom"
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return html.Div([
        dcc.Graph(id='transactions-per-region-map', figure=fig)
    ])
