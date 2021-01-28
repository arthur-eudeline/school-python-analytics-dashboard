import json
import plotly.express as px
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd


def build(df):
    fileContent = open('../include/france-regions.json')
    geoJson = json.load(fileContent)

    # Renomme les régions pour rendre compatible avec celles de Google Analytics
    renameRegionNames(geoJson)

    # Isole la some transactions par région
    data = pd.DataFrame(df[['ga:region', 'ga:transactions']].groupby(['ga:region']).sum())

    mapFigure = px.choropleth_mapbox(
        data,
        geojson=geoJson,
        locations=data.index,  # data.index = Le nom des régions
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

    mapFigure.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return html.Div([
        dcc.Graph(id='transactions-per-region-map', figure=mapFigure)
    ])


# Réécrit les noms de Régions de France qui diffèrent
# des noms de régions utilisés par Google Maps
def renameRegionNames(geoJSON: dict):
    # Map où :
    # - key = l'occurence GeoJSON à remplacer
    # - value = la valeur à remplacer
    overrideNames = {
        "Île-de-France": "Ile-de-France",
        "Bourgogne-Franche-Comté": "Bourgogne-Franche-Comte",
        "Normandie": "Normandy",
        "Bretagne": "Brittany",
        "La Réunion": "La Reunion",
        "Auvergne-Rhône-Alpes": "Auvergne-Rhone-Alpes",
        "Provence-Alpes-Côte d'Azur": "Provence-Alpes-Cote d'Azur",
        "Corse": "Corsica"
    }

    # Parcours le GeoJSON et remplace les noms de régions incorrects
    # par les bons noms de région
    for item in geoJSON['features']:
        if(item['properties']['nom'] in overrideNames.keys()):
            item['properties']['nom'] = overrideNames[item['properties']['nom']]
