###############################################################
# IMPORTING REQUIRED PACKAGES
###############################################################
import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc

from dash.dependencies import Output, Input, State

from database import *  # importing all variables from the database.py
import article  # importing the article.py

from collections import Counter
from functools import reduce
import random

import datetime
import plotly.io as pio

pio.renderers.default = "browser"

app = dash.Dash(__name__,
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1 , maximum-scale=1.5"}
                ],
                title='Significant Innings Percentage', update_title='Bowling...',
                external_stylesheets=[dbc.themes.PULSE])

app.config.suppress_callback_exceptions = True
pd.options.plotting.backend = "plotly"


###############################################################
# FUNCTIONS FOR COUNTERS
###############################################################
def counter_sum(a, b):
    count_dict = dict(Counter(a) + Counter(b))
    for i in range(1, 12):
        if i in count_dict:
            pass
        else:
            count_dict[i] = 0
    return count_dict


def division_dict(dict_a, dict_b):
    dict_out = {}
    for k in dict_b:
        try:
            dict_out[k] = float(dict_a[k]) / dict_b[k]
        except ZeroDivisionError:
            dict_out[k] = 0
    return dict_out


###############################################################
# NAVIGATION BAR FUNCTION
###############################################################

# This function is called to render the navigation bar

def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(html.A(
                [html.Img(src=app.get_asset_url('howstat.ico'), alt="HOWSTAT", height="65px", id="wc",
                          draggable="False"),
                 html.Figcaption("Howstat", style={"color": "white", "margin-left": "9px"})],
                href="http://www.howstat.com/cricket/Statistics/WorldCup/MatchListMenu.asp",
                target='_blank', draggable="False"), style={"margin-left": "15px"}
            ),
            dbc.NavItem(html.A([html.Img(
                src=app.get_asset_url('Github.png'), alt="GITHUB", height="65px", id="github", draggable="False"
            ), html.Figcaption("Github", style={"color": "white", "margin-left": "12px"})
            ], href="https://github.com/FahidLatheef/World-Cup-Cricket-Significant-Innings-Dashboard", target='_blank',
                draggable="False"),
                style={"margin-left": "15px"}),
            dbc.NavItem(html.A([html.Img(
                src=app.get_asset_url('Linkedin.png'), alt="LINKEDIN", height="65px", id="linkedin", draggable="False"
            ), html.Figcaption("LinkedIn", style={"color": "white", "margin-left": "8px"})
            ], href="https://www.linkedin.com/in/fahid-latheef-a-266b08164/", target='_blank', draggable="False"),
                style={"margin-left": "15px"}),
            dbc.NavItem(html.A([html.Img(
                src=app.get_asset_url('qm.png'), alt="FAQ", height="65px", id="faq", draggable="False"
            ), html.Figcaption("FAQ", style={"color": "white", "margin-left": "20px"})
            ], href="#details", draggable="False", n_clicks=0, id="faq_click"),
                style={"margin-left": "15px"}),
        ],
        brand="World Cup Cricket: Significant Innings %",
        color="primary",
        dark=True,
        fluid=False,
        expand="lg"  # anything below large device will have toggle-able menu
    ),
    return navbar


###############################################################
# PRE-PROCESSING
###############################################################
all_teams_list = []
for year in years:
    all_teams_list = all_teams_list + locals()["teams_list_{}".format(year)]

all_teams_list = list(set(all_teams_list))
all_teams_list.sort()  # Sorting the team list
# print(all_teams_list)


# For year Checkboxes
participation_years_teams = dict()

for team in all_teams_list:
    participation_years_teams[team] = []

for team in all_teams_list:
    for year in years:
        if team in locals()["teams_list_{}".format(year)]:
            participation_years_teams[team].append(year)
# print(participation_years_teams)

###############################################################
# WEB APP PAGE LAYOUT
###############################################################

app.layout = html.Div([
    dbc.Row(dbc.Col(Navbar(), width={"size": 12, "offset": 0})),
    dbc.Row(html.Br(), style={'background-color': 'rgb(235, 243, 209)'}),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='dropdown',
                options=[{'label': k, 'value': k} for k in participation_years_teams.keys()],
                # placeholder="Select a Country",
                value='Afghanistan',
                className="dd_dropdown",
                clearable=False,
                style={
                    'verticalAlign': "middle",
                },
                persistence_type='memory'
            ),
            xs={"size": 6, "offset": 1},  # extra small devices , For example: Pixel 2 411*731
            sm={"size": 5, "offset": 1},  # small devices , For example: Nexus 7 600*960
            md={"size": 4, "offset": 1},  # medium devices, For example: Ipad 768*1024
            lg={"size": 3, "offset": 1},  # large devices, For example: Ipad Pro 1024*1366
            # omitting extra large devices, will use same specs as Large device
            # Device name  Extra small  Small	  Medium	Large	  Extra Large
            # Screen width	<576px	    >=576px	  >=768px	>=992px	  >=1200px
        ),
        dbc.Col(html.Div([
            html.Button('Select All', id='button',
                        style={'background-color': 'rgb(89,49,150)', 'color': 'white'},
                        n_clicks=0),
            html.Div(id='output-container-button'),
        ]),
            xs={"size": 6, "offset": 1},  # extra small devices , For example: Pixel 2 411*731
            sm={"size": 8, "offset": 1},  # small devices , For example: Nexus 7 600*960
            md={"size": 8, "offset": 1},  # medium devices, For example: Ipad 768*1024
            lg={"size": 4, "offset": 0},  # large devices, For example: Ipad Pro 1024*1366
        ),
    ], style={'background-color': 'rgb(235, 243, 209)'}),
    dbc.Row(className="my-1"),  # Space between rows
    dbc.Row([dbc.Col(html.Div([
        dcc.Checklist(
            id='checkbox',
            value=[],
            persistence_type='memory',
            className='my_box_container',  # class of the container (div)
            # style={'display':'flex'},    # style of the container (div)
            style={'display': 'inline-block'},
            inputClassName='my_box_input',  # class of the <input> checkbox element
            # inputStyle={'cursor':'pointer'},      # style of the <input> checkbox element

            labelClassName='my_box_label',  # class of the <label> that wraps the checkbox input and the option's label
            # labelStyle={'background':'#A5D6A7',   # style of the <label> that wraps the checkbox input and the option's label
            #             'padding':'0.5rem 1rem',
            #             'border-radius':'0.5rem'},
        )
    ], id="checklist_id"), xs={"size": 11, "offset": 1},  # extra small devices , For example: Pixel 2 411*731
        sm={"size": 11, "offset": 1},  # small devices , For example: Nexus 7 600*960
        md={"size": 11, "offset": 1},  # medium devices, For example: Ipad 768*1024
        lg={"size": 11, "offset": 1},  # large devices, For example: Ipad Pro 1024*1366

    )],
        style={'background-color': 'rgb(235, 243, 209)', 'display': 'flex'}),
    html.Div([
        dcc.Graph(id='bar-plots',
                  config={'displayModeBar': False},
                  figure={
                      'data': [],
                      'layout': {'title': 'Significant Innings % in Batting Position'},
                  }

                  )], style={'background-color': 'rgb(235, 243, 209)'}),
    html.Div(id='inference',
             style={'background-color': 'rgb(235, 243, 209)'}),
    html.Hr(),
    html.Details([
        html.Summary('I am totally confused. What is this dashboard about, huh?', id="summary_text"),
        html.Div(article.content, id="article-div")

    ], id="details", open=True),
    html.Footer([dcc.Markdown(f"""
    `Author`: Fahid Latheef A

    `Today's Date`: {datetime.date.today()}

    """)], id="footer")
])


###############################################################
# CALLBACKS
###############################################################


@app.callback(
    Output('details', 'open'),
    Input('faq_click', 'n_clicks'),
    State('details', 'open'))
def toggle_faq(clicked, current_state):
    if current_state:
        if clicked:
            return current_state
    else:
        if clicked:
            current_state = True
            return current_state


@app.callback(
    Output('checkbox', 'options'),
    [Input('dropdown', 'value')])
def set_years_options(selected_country):
    return [{'label': i, 'value': i} for i in participation_years_teams[selected_country]]


@app.callback(
    [Output('checkbox', 'value'),
     Output('button', 'children')],
    [Input('button', 'n_clicks')],
    Input('checkbox', 'options'))
def set_years_value(n_clicks, years_options):
    all_or_none = []  # Initializing
    if n_clicks % 2 == 1:
        all_or_none = [i['value'] for i in years_options]
        return all_or_none, "Unselect All"
    else:
        return all_or_none, "Select All"


@app.callback(
    [Output('bar-plots', 'figure'),
     Output('inference', 'children')],
    [Input('dropdown', 'value'),
     Input('checkbox', 'value')])
def plot_bar(selected_country, selected_years):
    if len(selected_years) == 0:
        return go.Figure({
            'data': [{'type': 'bar',
                      'x': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                      'y': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}],
            'layout': {'xaxis': {'type': 'category'},
                       'title': "Significant Innings % in Batting Position",
                       'title_x': 0.5,
                       'xaxis_title': 'Team Batting Position',
                       'yaxis_title': 'Significant Innings %',
                       'font': dict(
                           family="monospace",
                           size=12,
                           color='black'
                       ),

                       # 'height': 500,
                       # 'width': 500
                       }}), html.Center(
            dcc.Markdown(
                "Nothing interesting here! Try selecting World-Cup years."
            ))
    else:
        try:

            selected_db_sig = []
            selected_db_tot = []
            for year_ in selected_years:
                variable_sig = sig_mega_db[year_]
                variable_tot = tot_mega_db[year_]
                selected_db_sig.append(variable_sig[(selected_country, 'sig_count')])
                selected_db_tot.append(variable_tot[(selected_country, 'tot_count')])
            sig_df = reduce(counter_sum, selected_db_sig)
            tot_df = reduce(counter_sum, selected_db_tot)

            div_df = division_dict(sig_df, tot_df)

            # now the colors
            lime = 'rgb(0,255,0)'
            sky_blue = 'rgb(0,191,255)'

            colours = [lime if x == max(div_df.values()) else sky_blue for x in div_df.values()]

            # plotly figure
            fig = go.Figure()

            fig.add_traces([go.Bar(x=list(map(int, div_df.keys())),
                                   y=[100 * i for i in list(map(float, div_df.values()))],
                                   marker=dict(color=colours),
                                   text=[100 * i for i in list(map(float, div_df.values()))], textposition='auto',
                                   texttemplate='%{text:.2f}%',
                                   textfont=dict(
                                       family="Helvetica, Arial",
                                       size=18,
                                       color="black"
                                   )
                                   )])
            fig.update_xaxes(type='category', fixedrange=True)
            fig.update_yaxes(fixedrange=True)
            fig.update_layout(
                title="Significant Innings % in Batting Position",
                title_x=0.5,
                xaxis_title='Team Batting Position',
                yaxis_title='Significant Innings %',
                font=dict(
                    family="monospace",
                    size=12,
                    color='black'
                ),
            )
            fig.add_layout_image(
                source=app.get_asset_url('flags/{}.png'.format(selected_country)),
                x=1,
                y=1,
                xanchor="right",
                yanchor="top",
                sizex=0.4,
                sizey=0.4
            )

            x = list(map(int, div_df.keys()))
            y = list(map(float, div_df.values()))
            maxed = max(zip(x, y), key=lambda x: x[1])[0]
            percent = str(round(100 * max(zip(x, y), key=lambda x: x[1])[1], 2)) + "%"

            return fig, dcc.Markdown("""
            The batting position **{2}** seems to have the maximum percentage ({3}) of significant innings. So, if there is a
            great talent like **{0}** in World-Cup team of **{1}**, it may be better to play him in the **Batting
            Position {2}** based on the selected World-Cup years.
             """.format(random.choice(talent_list[selected_country]), selected_country, maxed, percent))

        except KeyError:
            return go.Figure({
                'data': [{'type': 'bar',
                          'x': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                          'y': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}],
                'layout': {'xaxis': {'type': 'category'},
                           'title': "Significant Innings % in Batting Position",
                           'title_x': 0.5,
                           'xaxis_title': 'Team Batting Position',
                           'yaxis_title': 'Significant Innings %',
                           'font': dict(
                               family="monospace",
                               size=12,
                               color='black'
                           ),

                           # 'height': 500,
                           # 'width': 500
                           }
            }), html.Center(dcc.Markdown(
                "Nothing interesting here! Try selecting World-Cup years."
            ))


###############################################################
# RUNNING THE APP
###############################################################

if __name__ == '__main__':
    app.run_server(debug=False)
