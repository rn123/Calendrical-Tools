import dash
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
df = get_historical_data(inputStock, start=start, end=end, output_format="pandas")

trace_close = go.Scatter(x=list(df.index),
	                     y=list(df.close),
	                     name="Close",
	                     line=dict(color="#ebfe00"))

data = [trace_close]

layout = dict(title=inputStock,
			  showlegend=False)

fig = dict(data=data, layout=layout)

app = dash.Dash()

app.layout = html.Div([
	html.Div(html.H1(children="Hello World!")),
	html.Label("DASH GRAPH"),
	html.Div(
		dcc.Input(
			id="stock-input",
			placeholder="Enter a stock to be charted",
			type="text",
			value=''
		),
	),
	html.Div(
		dcc.Dropdown(
			options=[
				{'label': 'Candlestick', 'value': 'Candlestick'},
				{'label': 'Line', 'value': 'Line'}
			]
		)
	),
	html.Div(
		dcc.Graph(id="Stock Chart",
			      figure=fig)
	)
])

if __name__ == "__main__":
	app.run_server(debug=True)