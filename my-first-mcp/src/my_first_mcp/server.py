from mcp.server import MCPServer
import requests
from datetime import date

mcp = MCPServer("My First MCP")

@mcp.tool()
def get_weather(latitude: float, longitude: float) -> str:
    """Get the current weather for a given latitude and longitude."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "sunrise",
        "current_weather": True
    }
    response = requests.get(url, params=params)
    data = response.json()
    weather = data["current_weather"]
    return f"Temperature: {weather['temperature']}°C, Windspeed: {weather['windspeed']} km/h"

@mcp.tool()
def get_weather_archive(latitude: float, longitude:float, start_date: date, end_date:date) -> str:
    """Get the historical weather from archive for a given latitude and longitude."""
    a_url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "daily": "temperature_2m_max,temperature_2m_min",
    }
    response = requests.get(a_url, params=params)
    data = response.json()
    daily = data["daily"]
    return (
        f"Max temperatures: {daily['temperature_2m_max']}, " "\n"
        f"Min temperatures: {daily['temperature_2m_min']}"
    )

if __name__ == "__main__":
    mcp.run(transport='streamable-http', port=6275, stateless_http=True)
   #mcp.run()