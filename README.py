from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import requests
import datetime
import plotly.express as px


API_ENDPOINT = "http://api.openweathermap.org/data/2.5/forecast"
API_KEY = "41a1a3edd5af27415a85b88296f1bf5d"  # Replace with your own API key


zip_code = "50311"

params = {
    'zip': f"{zip_code},us", 
    'appid': API_KEY,
    'units': 'imperial'  
}

response = requests.get(API_ENDPOINT, params=params)
DATA = response.json()

if "list" not in DATA:
    print("Couldn't fetch the weather details.")


relevant_forecasts = DATA["list"]

# def format_forecast_data(forecasts):
#     formatted_data = []
#     for forecast in forecasts:
#         formatted_data.append({
#             'time': datetime.datetime.utcfromtimestamp(forecast["dt"]),
#             'temp': forecast['main']['temp'],
#             'humidity': forecast['main']['humidity'],
#             'feels_like': forecast['main']['feels_like']
#         })
#     return formatted_data

def format_forecast_data(relevant_forecasts):
    forecast_times = [datetime.datetime.utcfromtimestamp(forecast["dt"]) for forecast in relevant_forecasts]
    #You need to figure out what this should be, and make sure it works with the rest of your code, especially below.
    forecast_data = [x["main"] for x in relevant_forecasts]
    formatted_data = []

    for i in range(len(forecast_data)):
        formatted_data.append(forecast_data[i])
        formatted_data[i]["time"] = forecast_times[i]
    return formatted_data

#Very important to know how this data is structured.
forecast_data = format_forecast_data(relevant_forecasts)


# def format_forecast_data(relevant_forecasts):
#     forecast_times = [datetime.datetime.utcfromtimestamp(forecast["dt"]) for forecast in relevant_forecasts]
    
#     forecast_data = [x["main"] for x in relevant_forecasts]
#     formatted_data = []

#     for i in range(len(forecast_data)):
#         formatted_data.append(forecast_data[i])
#         formatted_data[i]["time"] = forecast_times[i]
#     return formatted_data


# forecast_data = format_forecast_data(relevant_forecasts)


# fig = px.line(forecast_data, x="time", y="temp", title='Forecast')
# fig2 = px.line(forecast_data, x="time", y="humidity", title='Humidity')
# fig3 = px.line(forecast_data, x="time", y="feels_like", title='feels_like')

app = Dash(__name__)

app.layout = html.Div(children = [
    dcc.Markdown( 
        id = "title",
        children = "## Weather Forecast for " + zip_code
    ),

    dcc.Dropdown( 
        id = "measure_select_dropdown",
        # options = ["temp", "humidity", "feels like"],
        options=[
            {'label': 'Temperature', 'value': 'temp'},
            {'label': 'Humidity', 'value': 'humidity'},
            {'label': 'Feels Like', 'value': 'feels_like'}
        ],
        # value = 'choose', 
        # multi = True
        value='temp',
        multi=False
    ),

    dcc.Graph(id = 'graph')
    #dcc.Graph( #displays the graph on the page
    #    id = "weather_line_graph",
    #    figure = fig
    #),

    #dcc.Graph( #displays humidity graph
    #    id = "humidity_line_graph",
    #    figure = fig2
    #),

    #dcc.Graph( #displays real feel graph
    #    id = "realfeel_line_graph",
    #    figure = fig3
    #)
])



@app.callback(
    Output("graph","figure"),
    Input("measure_select_dropdown","value"),
)
def update_weather_graph(chosen_graph): #takes arguments?
    if chosen_graph == "temp":
        graph = px.line(forecast_data, x="time", y="temp", title='Forecast')
    elif chosen_graph == "humidity":
        graph = px.line(forecast_data, x="time", y="humidity", title='Humidity')
    elif chosen_graph == "feels_like":
        graph = px.line(forecast_data, x="time", y="feels_like", title='feels_like')
    return graph

if __name__ == '__main__': # starts the server
    app.run_server(debug=True)
