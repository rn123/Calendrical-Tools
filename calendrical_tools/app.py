import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

# iexfinance example data, sign up and use free sandbox api, get token
# Save token to IEX_TOKEN, specify sandbox API
# with export IEX_API_VERSION='iexcloud-sandbox'
from iexfinance.stocks import get_historical_data
import datetime
from dateutil.relativedelta import relativedelta

start = datetime.datetime.today() - relativedelta(years=5)
end = datetime.datetime.today()

inputStock = "VZ"


app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.Div([dcc.Input(id="stock-input", value="SPY", type="text")]),
        html.Div(
            [html.H2("Stock App"), html.Img(src="/assets/astrolabe_generated.svg")],
            className="banner",
        ),
        html.Div(
            [html.Div([dcc.Graph(id="graph_close",),], className="six columns",),],
            className="row",
        ),
    ]
)


@app.callback(
    dash.dependencies.Output("graph_close", "figure"),
    [dash.dependencies.Input("stock-input", "value")],
)
def update_fig(input_value):
    df = get_historical_data(input_value, start=start, end=end, output_format="pandas")
    data = []
    trace_close = go.Scatter(
        x=list(df.index), y=list(df.close), name="Close", line=dict(color="#ebfe00")
    )
    data.append(trace_close)
    layout = {"title": "Callback Graph"}

    return {
        "data": data,
        "layout": layout,
    }


app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

if __name__ == "__main__":
    app.run_server(debug=True)
