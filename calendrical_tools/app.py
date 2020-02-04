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

trace_high = go.Scatter(x=list(df.index),
	                    y=list(df.high),
	                    name="High",
	                    line=dict(color="#00ebfe"))
app = dash.Dash(__name__)

app.layout = html.Div([
	html.Div([
		html.H2("Stock App"),
		html.Img(src="/assets/astrolabe_generated.svg")
	], className="banner"),

	html.Div([
		html.Div([
			html.H3("Column 1"),
			dcc.Graph(
				id="graph_close",
				figure={
					"data":[trace_close],
					"layout":{
						"title":"Close Graph"
						}
					}
				)
		], className="six columns"),

		html.Div([
			html.H3("Column 2"),
			dcc.Graph(
				id="graph_high",
				figure={
					"data":[trace_high],
					"layout":{
						"title":"High Graph"
						}
					}
				)
		], className="six columns")
	], className="row")
])


app.css.append_css({
	"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

if __name__ == "__main__":
	app.run_server(debug=True)