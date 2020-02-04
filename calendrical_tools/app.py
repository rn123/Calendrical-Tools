import dash
import dash_core_components as dcc
import dash_html_components as html

# iexfinance example data, sign up and use free sandbox api, get token
# Save token to IEX_TOKEN, specify sandbox API 
# with export IEX_API_VERSION='iexcloud-sandbox'
from iexfinance.stocks import get_historical_data
import datetime
from dateutil.relativedelta import relativedelta

start = datetime.datetime.today() - relativedelta(years=5)
end = datetime.datetime.today()

df = get_historical_data("GE", start=start, end=end, output_format="pandas")
print(df.head())

# app = dash.Dash()

# app.layout = html.Div(
# 	html.H1(children="Hello World!")
# )

# if __name__ == "__main__":
# 	app.run_server(debug=True)