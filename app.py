
import dash                     # pip install dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px     # pip install plotly==5.2.2
import pandas as pd   # pip install pandas

df = pd.read_csv("country_vaccinations.csv")
df.isnull().sum()
# Fill NaNs with 0 and then drop all countries with iso_code = 0.
# df.fillna(0, inplace=True)
# df.drop(df.index[df['iso_code'] == 0], inplace=True)
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
# Find the mean
df['total_vaccinations'].mean()
df['people_fully_vaccinated'].mean()
df['daily_vaccinations'].mean()
df['total_vaccinations_per_hundred'].mean()

# filling the missing values in "Mileage column" with "Mean" value
df['total_vaccinations'].fillna(df['total_vaccinations'].mean(), inplace=True)
df['people_fully_vaccinated'].fillna(df['people_fully_vaccinated'].mean(), inplace=True)
df['daily_vaccinations'].fillna(df['daily_vaccinations'].mean(), inplace=True)
df['total_vaccinations_per_hundred'].fillna(df['total_vaccinations_per_hundred'].mean(), inplace=True)
print(df.head())

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Analytics Dashboard of COVID-19 World Vaccination (Dash Plotly)", style={"textAlign": "center"}),
    html.Hr(),
    html.P("Data is collected daily from https://ourworldindata.org/ and the GitHub repository for https://github.com/owid/covid-19-data, and you can get more information from the website. Covid-19 has affected the entire world, and the only way to protect ourselves is through vaccination. I decided to make my project COVID-19 vaccination, so I want to know how vaccination is going in my country and the rest of the world.", style={"textAlign": "left"}), 
   # html.Hr(),
    html.P("Choose country of interest:"),
    html.Div(html.Div([
        dcc.Dropdown(id='country', clearable=False,
                     value="Afghanistan",
                     options=[{'label': x, 'value': x} for x in
                              df["country"].unique()]),
    ], className="two columns"), className="row"),

    html.Div(id="output-div", children=[]),
])


@app.callback(Output(component_id="output-div", component_property="children"),
              Input(component_id="country", component_property="value"),
              )
def make_graphs(country_chosen):
    # LINE CHART
    df_hist = df[df["country"] == country_chosen]
    # fig_ecdf = px.ecdf(df_hist, x="date", color="vaccines")
    fig_line = px.line(df_hist, x="date", y="total_vaccinations",
                       color="vaccines", markers=True)
    # scatter plot
    fig1_line =px.scatter(df_hist, x="date", y="daily_vaccinations")
    # fig2_line = px.bar(df, x="people_fully_vaccinated", y="vaccines")
    # scatter plot
    fig2_line = px.scatter(df_hist, x="date", y="people_fully_vaccinated")
    # map plot
    fig_map= px.choropleth(df_hist,locations='iso_code',color='total_vaccinations_per_hundred',hover_name="country",template='plotly_dark',
                        title='Total vaccinated by hundred')

    return [
        html.Div([
            html.Div([dcc.Graph(figure=fig_line)],className="twelve columns"),
        ], className="row"),
        html.Div([
            html.Div([dcc.Graph(figure=fig1_line)], className="six columns"),
            html.Div([dcc.Graph(figure=fig2_line)], className="six columns"),
        ], className="row"),
        html.Div([
            html.Div([dcc.Graph(figure=fig_map)], className="twelve columns"),
        ], className="row"),

    ]


if __name__=='__main__':
    app.run_server(port=8053)


