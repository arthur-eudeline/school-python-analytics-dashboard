import dash_html_components as html

def build(df):
    totalUsers = df['ga:users'].sum()
    totalSessions = df['ga:sessions'].sum()
    totalTransactions = df['ga:transactions'].sum()
    totalRevenues = df['ga:transactionRevenue'].sum()

    totalConversion = totalTransactions / totalSessions * 100
    totalConversion = round(totalConversion, 2)
    totalConversion = str(totalConversion) + "%"

    return html.Div([
        html.H1("Analyse analytics"),
        html.H2("Total utilisateurs"),
        html.P(totalUsers),
        html.H2("Total sessions"),
        html.P(totalSessions),
        html.H2("Total transactions"),
        html.P(totalTransactions),
        html.H2("Chiffre d'affaires total"),
        html.P(totalRevenues),
        html.H2("Taux de conversion total"),
        html.P(totalConversion),
    ])

