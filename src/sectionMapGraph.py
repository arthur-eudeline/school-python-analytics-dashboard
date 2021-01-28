import json
import plotly.express as px
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import dash.dependencies as dd

# Evite les erreurs d'imports circulaires
import plotly.validator_cache
import plotly.graph_objects

from src import htmlComponents

fileContent = open('../include/france-regions.json')
geoJson = json.load(fileContent)


def getFig(df: pd.DataFrame, regionLists: list = None):
    # Renomme les régions pour rendre compatible avec celles de Google Analytics
    renameRegionNames(geoJson)

    # Isole la some transactions par région
    data = pd.DataFrame(df[['ga:region', 'ga:transactions']].groupby(['ga:region']).sum())

    # Si on filtre par region, on ne garde que les indexes du df correspondant à la liste de `regionLists`
    if regionLists is not None and len(regionLists) > 0:
        data = data[data.index.isin(regionLists)]

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
        zoom=4,
        # Centre par défaut sur la France
        center={
            "lat": 46.71109,
            "lon": 1.7191036
        },
        height=600,
        opacity=0.75,
        # Légende
        labels={
            'ga:transactions': 'Transactions',
            'ga:region': 'Région'
        },
        featureidkey="properties.nom"
    )

    return mapFigure


# Génère le html pour la map et le selector
def build(df):
    return html.Div(
        className="row",
        children=htmlComponents.mapCard(
            title="Nombre de transaction par région en France",
            dropDown=dcc.Dropdown(
                id="map-region-selector",
                options=buildDropdownOptions(geoJson),
                multi=True
            ),
            map=dcc.Graph(
                id='transactions-per-region-map',
                figure={}
            )
        )
    )


# Réécrit les noms de Régions de France qui diffèrent
# des noms de régions utilisés par Google Maps
def renameRegionNames(geoJSON: dict):
    # Parcours le GeoJSON et remplace les noms de régions incorrects
    # par les bons noms de région
    for item in geoJSON['features']:
        item['properties']['nom'] = renameRegionName(item['properties']['nom'])


def renameRegionName(regionName: str):
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

    if (regionName in overrideNames.keys()):
        regionName = overrideNames[regionName]
    return regionName


# Recupère les noms des régions depuis le geoJSON
def getRegionsNames(geoJSON: dict):
    renameRegionNames(geoJSON)
    output = []
    for item in geoJSON['features']:
        output.append(item['properties']['nom'])
    return output


# Génère la liste de régions pour la dropdown
def buildDropdownOptions(geoJSON: dict):
    output = []
    for item in geoJSON['features']:
        output.append({
            'label': item['properties']['nom'],
            'value': renameRegionName(item['properties']['nom'])
        })
    return sorted(output, key=lambda el: el['label'])


def output():
    return dd.Output(
        component_id="transactions-per-region-map",
        component_property="figure"
    )


def update(df: pd.DataFrame, regionsLists):
    return getFig(df, regionsLists)
