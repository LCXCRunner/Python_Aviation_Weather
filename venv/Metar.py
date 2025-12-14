import requests
from requests.models import Response
from datetime import datetime, timezone

class Metar:
    def __init__(self, airports : str, format : str, hours : float, date : str) -> None:
        """
        Initialize Metar object with given parameters.
        
        Args:
            airports (str): Single airport code (e.g., 'KSLC').
            format (str): Data format (e.g., 'json').
            taf (bool): Whether to include TAF data.
            hours (float): Number of hours for data retrieval.
            date (str): Date string. Format: 'YYYYMMDD_HHMM'.
        """
        # Store parameters
        self.airports : str = airports
        self.format : str = format
        self.taf : bool = False
        self.hours : float = hours
        self.date : str = date

        # Construct the API URL
        self.url : str = "https://aviationweather.gov/api/data/metar?ids=" + airports + \
                        f"&format={format}&taf={str(self.taf).lower()}&hours={hours}&date={date}"
        self.request : Response = requests.get(self.url)
        self.data : dict = self.request.json()

        # data decoded from the API
        # Observation Time, Temperature, Dewpoint
        self.observationTime : str = self.data[0]['obsTime'] # note that this is in UNIX time format
        self.observationTime = datetime.fromtimestamp(int(self.observationTime)).strftime('%B %d, %Y %H:%M UTC') # Month Day, Year Hour:Minute UTC
        self.temperatureC : float = self.data[0]['temp']
        self.dewpointC : float = self.data[0]['dewp']

        # Altimeter Setting and Density Altitude
        self.pressureHectopascals : float = self.data[0]['altim'] # in hPa
        self.pressureInchesHg : float = round(self.pressureHectopascals * 0.02953, 2) # convert hPa to inHg
        self.elevationFeet : float = round(self.data[0]['elev'] * 3.28084) # in feet
        self.pressureAltitude : float = round(self.elevationFeet + (29.92 - self.pressureInchesHg) * 1000) # in feet
        self.densityAltitude : float = round(self.pressureAltitude + (120 * (self.temperatureC - ((15 - (self.elevationFeet / 1000) * 2))))) # in feet

        # Winds, visibility, sky conditions
        self.windSpeedKts : float = self.data[0]['wspd']
        self.windDirectionDeg : float = self.data[0]['wdir']
        if 'wgst' in self.data[0]:
            self.windGustKts : float = self.data[0]['wgst']
        else:
            self.windGustKts : float = 0.0
        self.visibilityStatuteMiles : float = self.data[0]['visib']
        # self.clousds : list = self.data[0]['']


if __name__ == "__main__":
    metar : Metar = Metar("KSLC", "json", 2.0, "20251214_0400")
    print(metar.url)

    utc_now = datetime.now(timezone.utc)
    print("Current UTC Time:", utc_now.strftime('%B %d, %Y %H:%M UTC'))

    print("Fetched data:")
    print("KSLC METAR:", metar.data[0]['icaoId'])
    print("Observation Time:", metar.observationTime)
    print("Temperature (C):", metar.temperatureC)
    print("Dewpoint (C):", metar.dewpointC)
    print("Pressure (inHg):", metar.pressureInchesHg)
    print("Elevation (ft):", metar.elevationFeet)
    print("Pressure Altitude (ft):", metar.pressureAltitude)
    print("Density Altitude (ft):", metar.densityAltitude)
    print("Wind:", f"{metar.windDirectionDeg}° at {metar.windSpeedKts} kts, Gusts: {metar.windGustKts} kts")
    print("Visibility (statute miles):", metar.visibilityStatuteMiles)