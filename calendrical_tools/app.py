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

app = dash.Dash(__name__)

app.layout = html.Div([
	html.H2("Stock App"),
	html.Img(src="/assets/astrolabe_generated.svg")
], className="banner")

# app.css.append({
# 	"external_url": "http://"
# })

if __name__ == "__main__":
	app.run_server(debug=True)