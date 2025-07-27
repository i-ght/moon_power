import pprint
from typing import Union, Literal
import requests
from datetime import datetime


Product = Union[
    Literal["water_level"],  # Preliminary or verified 6-minute interval water levels
    Literal["hourly_height"],  # Verified hourly height water level data
    Literal["high_low"],  # Verified high tide / low tide water level data
    Literal["daily_mean"],  # Verified daily mean water level data (Great Lakes only)
    Literal["Daily Maximum"],  # Verified daily maximum water level data
    Literal["Daily Minimum"],  # Verified daily minimum water level data
    Literal["monthly_mean"],  # Verified monthly mean water level data
    Literal["one_minute_water_level"],  # Preliminary 1-minute interval water level data
    Literal["predictions"],  # Water level / tide prediction data
    Literal["datums"],  # Observed tidal datum values
    Literal["air_gap"],  # Air Gap data
    Literal["air_temperature"],  # Air temperature
    Literal["water_temperature"],  # Water temperature
    Literal["wind"],  # Wind speed, direction, and gusts
    Literal["air_pressure"],  # Barometric pressure
    Literal["conductivity"],  # Water's conductivity
    Literal["visibility"],  # Visibility
    Literal["humidity"],  # Relative humidity
    Literal["salinity"],  # Salinity and specific gravity
]

def con_data(
    station_id: str,
    product: Product,
    # begin_date: datetime = None,
    # end_date: datetime = None,
    time_zone: str = "lst_ldt"
) -> dict:
    """
    Fetches data from NOAA Tides and Currents API
    
    Args:
        station_id: NOAA station ID (e.g., "9414290" for San Francisco)
        data_type: One of the supported data types
        begin_date: Start date for data range
        end_date: End date for data range
        time_zone: "GMT" or "LST" (Local Standard Time)
    
    Returns:
        Dictionary containing the API response
    """
    base_url = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
    
    params = {
        "station": station_id,
        "product": product,
        "units": "metric",
        "time_zone": time_zone,
        "application": "CSW",  # NOAA requests identifying your app
        "format": "json",
        "date": "today",
        "datum": "MLLW"
    }
    
    match product:
        case "predictions":
            params.update([("interval", "hilo")])

    # if begin_date and end_date:
    #     params.update({
    #         "begin_date": begin_date.strftime("%Y%m%d"),
    #         "end_date": end_date.strftime("%Y%m%d")
    #     })
    # elif product in ["predictions", "hourly_height"]:
    #     # Default to 1 day if no date range provided for these types
    #     # default_date = datetime.now().strftime("%Y%m%d")
    #     params["date"] = "today"
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    return response.json()

def con_air_pressure(station_id: str):
    return con_data(
        station_id=station_id,
        product="air_pressure"
    )["data"][-1]["v"]

def con_water_level(station_id: str):
    return con_data(
        station_id=station_id,
        product="water_level"
    )["data"][-1]["v"]

def con_water_temp(station_id: str):
    return con_data(
        station_id=station_id,
        product="water_temperature"
    )["data"][-1]["v"]

def con_air_temp(station_id: str):
    return con_data(
        station_id=station_id,
        product="air_temperature"
    )["data"][-1]["v"]

def con_wind(station_id: str):
    return con_data(
        station_id=station_id,
        product="wind"
    )["data"][-1]["v"]

def con_tides(station_id: str):
    data = con_data(
        station_id=station_id,
        product="predictions"
    )["predictions"]

    data = {
        "H": {"time": data[0]["t"], "water_level": data[0]["v"]},
        "L": {"time": data[1]["t"], "water_level": data[1]["v"]}
    }

    return data

# https://aa.usno.navy.mil/api/rstt/oneday?date=2025-07-27%20&coords=30.1588,%2085.6602&tz=6&dst=true

if __name__ == "__main__":
    panama_city = "8729108"
    station_id = panama_city
    air_pressure = con_air_pressure(station_id)
    water_level = con_water_level(station_id)
    water_temp = con_water_temp(station_id)
    air_temp = con_air_temp(station_id)
    tides = con_tides(station_id)
    # wind = con_wind(station_id)
    
    data = {
        "barometric_pressure": air_pressure,
        "water_level": water_level,
        "water_temp": water_temp,
        "air_temperature": air_temp,
        "tides": tides,
        # "wind": wind
    }

    pprint.pprint(data)