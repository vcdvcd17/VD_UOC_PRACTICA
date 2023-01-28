
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px


app = Dash()
px.set_mapbox_access_token(open(".mapbox_token").read())

df = pd.DataFrame()
for a in range(2020, 2023):
    for m in range(1, 13):
        if 202006 <= a*100 + m <= 202211:
            f = "data/stats_{}_{:02d}.csv".format(a, m)
            df = pd.concat([df, pd.read_csv(f)])

df["w_bike"] = df["avg_bikes"]*df["weight"]
df["w_buida"] = df["full"]*df["weight"]
df["w_plena"] = df["empty"]*df["weight"]
df["w_ocupacio"] = df["ocupacio"]*df["weight"]

info = pd.read_csv("data/info.csv")

app.layout = html.Div([
    html.H2("Estat de les estacions del bicing", style={"text_align": "center"}),
    dcc.RadioItems(
        id="viz",
        options=["Bicicletes", "Estació completa", "Estació buida", "Ocupació"],
        value="Bicicletes",
        inline=True
    ),
    html.H2(""),

    html.Div([
        html.Div([
            dcc.RadioItems(
                [{"label": '2020', "value": 2020, }, {"label": '2021', "value": 2021, },
                 {"label": '2022', "value": 2022, }, {"label": "Tots", "value": 9999},
                 ], value=9999,
                id="anys",
                inline=True,
                style={"text_align": "center"}
            )], style={"margin": "5px"}
        ),
        html.Div([
            dcc.RadioItems(
                [{"label": 'Gener', "value": 1, }, {"label": 'Febrer', "value": 2, },
                 {"label": 'Març', "value": 3, }, {"label": 'Abril', "value": 4, },
                 {"label": 'Maig', "value": 5, }, {"label": 'Juny', "value": 6, },
                 {"label": 'Juliol', "value": 7, }, {"label": "Agost", "value": 8},
                 {"label": 'Setembre', "value": 9, }, {"label": 'Octubre', "value": 10, },
                 {"label": 'Novembre', "value": 11, }, {"label": "Desembre", "value": 12},
                 {"label": 'Tots', "value": 99, }
                 ], value=99,
                id="mes",
                inline=True,
                style={"text_align": "center"}
            )], style={"margin": "5px"}
        ),
        html.Div([
            dcc.RadioItems(
                [{"label": 'Dilluns', "value": 0, }, {"label": 'Dimarts', "value": 1, },
                 {"label": 'Dimecres', "value": 2, }, {"label": 'Dijous', "value": 3, },
                 {"label": 'Divendres', "value": 4, }, {"label": 'Dissabte', "value": 5, },
                 {"label": 'Diumenge', "value": 6, }, {"label": "Tots", "value": 9},
                 ], value=9,
                id="dia",
                inline=True,
                style={"text_align": "center"}
            )], style={"margin": "5px"}
        ),
        html.Div([
            dcc.RangeSlider(
                0, 24, 1,
                id="franja",
                count=1,
                value=[0, 24],
                marks={
                    0: '00h', 1: '01h', 2: '02h', 3: '03h', 4: '04h',
                    5: '05h', 6: '06h', 7: '07h', 8: '08h', 9: '09h',
                    10: '10h', 11: '11h', 12: '12h', 13: '13h', 14: '14h',
                    15: '15h', 16: '16h', 17: '17h', 18: '18h', 19: '19h',
                    20: '20h', 21: '21h', 22: '22h', 23: '23h', 24: '24h'
                }
            )], style={"margin": "5px", "text_align": "center"}
        ),
    ], style={"width": "45%"}),
    html.Div([
        dcc.Graph(
            id='mapa',
            selectedData={'points': [{'customdata': [1, "GRAN VIA CORTS CATALANES, 760"]}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id="grafic"),
    ], style={'display': 'inline-block', 'width': '49%'}),
])

dict_viz = {"Bicicletes": "avg_bikes", "Estació completa": "full", "Estació buida": "empty", "Ocupació": "ocupacio"}
yaxis_fmt_dict = {"Bicicletes": "", "Estació completa": ".2%", "Estació buida": ".2%", "Ocupació": ".2%"}
template_fmt_dict = {"Bicicletes": ".2f", "Estació completa": ".2%", "Estació buida": ".2%", "Ocupació": ".2%"}
title_dict = {"Bicicletes": "Bicicletes", "Estació completa": "Temps completa",
              "Estació buida": "Temps buida", "Ocupació": "Ocupació"}


@app.callback(
    Output("mapa", "figure"),
    Input("viz", "value"),
    Input("franja", "value"),
    Input("anys", "value"),
    Input("mes", "value"),
    Input("dia", "value")
)
def visualitza(viz, franja, anys, mes, dia):
    agg_df = df[(df.hour.isin(range(franja[0], max(franja[1], franja[0] + 1)))) & (
            (anys == 9999) | (df.year == anys)) & (
                        (mes == 99) | (df.month == mes)) & (
                        (dia == 9) | (df.weekday == dia))
                ].groupby(["station_id"]).agg(
        avg_bikes=pd.NamedAgg(column="w_bike", aggfunc="sum"),
        full=pd.NamedAgg(column="w_buida", aggfunc="sum"),
        empty=pd.NamedAgg(column="w_plena", aggfunc="sum"),
        ocupacio=pd.NamedAgg(column="w_ocupacio", aggfunc="sum"),
        weight=pd.NamedAgg(column="weight", aggfunc="sum")
    )
    agg_df.loc[:, "avg_bikes"] = agg_df["avg_bikes"] / agg_df["weight"]
    agg_df.loc[:, "full"] = agg_df["full"] / agg_df["weight"]
    agg_df.loc[:, "empty"] = agg_df["empty"] / agg_df["weight"]
    agg_df.loc[:, "ocupacio"] = agg_df["ocupacio"] / agg_df["weight"]
    agg_df = pd.merge(
        info,
        agg_df,
        on="station_id",
        sort=False
    )

    if viz in ("Ocupació", "Bicicletes"):
        scale = "rdylgn"
    else:
        scale = "rdylgn_r"

    fig = px.scatter_mapbox(agg_df, lat="lat", lon="lon",
                            custom_data=["station_id", "name", "avg_bikes",
                                         "ocupacio", "full", "empty"],
                            zoom=11.8,
                            size=dict_viz[viz], color=dict_viz[viz],
                            color_continuous_scale=scale,
                            width=1000, height=700, mapbox_style="light",
                            center={"lat": 41.3954, "lon": 2.159943})
    fig.update_mapboxes(bearing=-45)
    fig.update_traces(hovertemplate=" %{customdata[1]} <br> Mitjana bicicletes: %{customdata[2]:.0f} <br>"
                                    " Ocupació mitjana: %{customdata[3]:.0%} <br>"
                                    " Temps buida: %{customdata[5]:.0%} <br> Temps plena: %{customdata[4]:.0%}"
                      )
    fig.update_layout(clickmode='event+select')
    fig.update_coloraxes(colorbar_title=None)
    return fig


@app.callback(
    Output('grafic', 'figure'),
    Input('mapa', 'selectedData'),
    Input("viz", "value"),
    Input("anys", "value"),
    Input("mes", "value"),
    Input("dia", "value")
)
def plot_time_series(selecteddata, viz, anys, mes, dia):
    stations = [x["customdata"][0] for x in selecteddata["points"]]
    address = {str(x["customdata"][0]): x["customdata"][1] for x in selecteddata["points"]}
    df_plot = df[(df.station_id.isin(stations)) & (
            (anys == 9999) | (df.year == anys)) & (
            (mes == 99) | (df.month == mes)) & (
            (dia == 9) | (df.weekday == dia))
        ].groupby(["station_id", "hour"]).agg(
        avg_bikes=pd.NamedAgg(column="w_bike", aggfunc="sum"),
        full=pd.NamedAgg(column="w_buida", aggfunc="sum"),
        empty=pd.NamedAgg(column="w_plena", aggfunc="sum"),
        ocupacio=pd.NamedAgg(column="w_ocupacio", aggfunc="sum"),
        weight=pd.NamedAgg(column="weight", aggfunc="sum")
    ).reset_index()
    df_plot.loc[:, "avg_bikes"] = df_plot["avg_bikes"] / df_plot["weight"]
    df_plot.loc[:, "full"] = df_plot["full"] / df_plot["weight"]
    df_plot.loc[:, "empty"] = df_plot["empty"] / df_plot["weight"]
    df_plot.loc[:, "ocupacio"] = df_plot["ocupacio"] / df_plot["weight"]
    df_plot_aux = df_plot[df_plot["hour"] == 0].copy()
    df_plot_aux["hour"] = 24
    df_plot = pd.concat([df_plot, df_plot_aux])
    fig = px.line(df_plot, x="hour", y=dict_viz[viz], color="station_id")
    fig.for_each_trace(lambda t: t.update(name=address[t.name]))
    fig.update_traces(hovertemplate=None)
    fig.update_layout(hovermode="x unified")
    fig.update_layout(
        title={
            'text': title_dict[viz],
            'y': .95,
            'x': 0.4,
            'xanchor': 'center',
            'yanchor': 'top'},
        legend_title="Estació",
        yaxis_title=None,
        xaxis_title=None,
        width=1000, height=700,
        yaxis_tickformat=yaxis_fmt_dict[viz]
    )
    fig.update_xaxes(
        tickvals=[3, 6, 9, 12, 15, 18, 21, 24],
        minor_tickvals=[0, 1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20, 22, 23],
        ticksuffix="h",
        showgrid=False
    )
    fig.update_yaxes(
        range=[0, df_plot[dict_viz[viz]].max()*1.1],
        showgrid=False
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port=8080)
