import requests
from requests.models import Response
from datetime import datetime, timezone

class Metar:
    def __init__(self, airport : str, format : str, hoursBack : float) -> None:
        """
        Initialize Metar object with given parameters.
        
        Args:
            airports (str): Single airport code (e.g., 'KSLC').
            format (str): Data format (e.g., 'json').
            hours (float): Number of hours for data retrieval.
        """
        # Store parameters
        self.airports : str = airport
        self.format : str = format
        self.taf : bool = False
        self.hours : float = hoursBack
        # Find Zulu time
        self.zuluTime : str = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M')
        self.zuluTimeReadable : str = datetime.now(timezone.utc).strftime('%B %d, %Y %H:%M UTC')

        # Construct the API URL
        self.url : str = "https://aviationweather.gov/api/data/metar?ids=" + airport + \
                        f"&format={format}&taf={str(self.taf).lower()}&hours={hoursBack}&date={self.zuluTime}"
        self.request : Response = requests.get(self.url)
        self.data : dict = self.request.json()

        # data decoded from the API
        # Observation Time, Temperature, Dewpoint
        self.observationTime : str = self.data[0]['obsTime'] # note that this is in UNIX time format
        self.observationTime = datetime.fromtimestamp(int(self.observationTime), timezone.utc).strftime('%B %d, %Y %H:%M UTC') # Month Day, Year Hour:Minute UTC
        self.temperatureC : float = self.data[0]['temp']
        self.dewpointC : float = self.data[0]['dewp']

        # Altimeter Setting and Density Altitude
        self.altimeterSetting : float = round(self.data[0]['altim'] * 0.02953, 2) # in inHg
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
        
        # Clouds
        if 'clouds' in self.data[0]:
            self.clouds : str = self.decodeClouds(self.data[0]['clouds'])
        else:
            self.clouds : str = "No cloud data available"

        if 'wx_string' in self.data[0]:
            self.weather : str = self.decodeWeather(self.data[0]['wx_string'])
        else:
            self.weather : str = "No significant weather"

        # Flight Category
        self.flightCategory : str = self.data[0]['fltCat']

    def decodeClouds(self, clouds_data: list[dict]) -> str:
        """
        Decode cloud information from METAR data.
        
        Args:
            clouds_data (list): List of cloud layer dictionaries from METAR data.
        Returns:
            str: Human-readable cloud description.
        """
        # Cloud coverage abbreviations
        coverage_codes = {
            'CLR': 'Clear',
            'CAVOK': 'Ceiling and Visibility OK',
            'FEW': 'Few',
            'SCT': 'Scattered',
            'BKN': 'Broken',
            'OVC': 'Overcast',
            'OVX': 'Sky Obscured'
        }
        
        # If no cloud data, return clear
        if not clouds_data or len(clouds_data) == 0:
            return 'Clear skies'
        
        # Build cloud description for each layer
        cloud_layers = []
        
        for layer in clouds_data:
            cover = layer.get('cover', None)
            base = layer.get('base', None)
            top = layer.get('top', None)
            
            # Get human-readable coverage
            coverage_text = coverage_codes.get(cover, cover)
            
            # Special cases for clear conditions
            if cover in ['CLR', 'CAVOK']:
                return coverage_text
            
            # Build layer description
            layer_desc = coverage_text
            
            if base is not None:
                layer_desc += f" at {base:,} ft"
            
            if top is not None:
                layer_desc += f" (tops {top:,} ft)"
            
            cloud_layers.append(layer_desc)
        
        # Join all layers with semicolons
        if cloud_layers:
            return '; '.join(cloud_layers)
        else:
            return 'No cloud data available'

    def decodeWeather(self, weather_string: str) -> str:
        """
        Decode METAR weather strings into human-readable descriptions.
        
        Args:
            weather_string (str): METAR weather code (e.g., '+SHRA', 'BLSN', 'VCFG')
            
        Returns:
            str: Human-readable weather description
        """
        result : str = ""
        vicinity : bool = False

        # Intensity prefixes
        intensities : dict= {
            '-': 'Light',
            '+': 'Heavy',
            'VC': 'in vicinity'
        }
        
        # Descriptors (2-letter codes)
        descriptors : dict = {
            'MI': 'shallow',
            'PR': 'partial',
            'BC': 'patches of',
            'DR': 'low drifting',
            'BL': 'blowing',
            'SH': 'showers of',
            'TS': 'thunderstorm',
            'FZ': 'freezing'
        }
        
        # Precipitation types
        precipitation : dict = {
            'DZ': 'drizzle',
            'RA': 'rain',
            'SN': 'snow',
            'SG': 'snow grains',
            'IC': 'ice crystals',
            'PL': 'ice pellets',
            'GR': 'hail',
            'GS': 'small hail/snow pellets',
            'UP': 'unknown precipitation'
        }
        
        # Obscurations
        obscurations : dict = {
            'BR': 'mist',
            'FG': 'fog',
            'FU': 'smoke',
            'VA': 'volcanic ash',
            'DU': 'widespread dust',
            'SA': 'sand',
            'HZ': 'haze',
            'PY': 'spray'
        }
        
        # Other phenomena
        other : dict = {
            'PO': 'dust/sand whirls',
            'SQ': 'squalls',
            'FC': 'funnel cloud',  # tornado/waterspout
            'SS': 'sandstorm/duststorm'
        }
        
        # Special case: +FC always means tornado/waterspout
        if weather_string == '+FC':
            return 'Tornado or waterspout'
        
        # Parse the weather string
        result_parts = []
        remaining = weather_string
        
        # Check for intensity prefix
        intensity = ''
        if remaining.startswith('VC'):
            vicinity = True
            remaining = remaining[2:]
        elif remaining.startswith('-'):
            intensity = intensities['-']
            remaining = remaining[1:]
        elif remaining.startswith('+'):
            intensity = intensities['+']
            remaining = remaining[1:]
        
        # Parse descriptors and phenomena (2-character codes)
        descriptor = ''
        phenomena_list = []
        
        while len(remaining) >= 2:
            code = remaining[:2]
            
            if code in descriptors:
                descriptor = descriptors[code]
                remaining = remaining[2:]
            elif code in precipitation:
                phenomena_list.append(precipitation[code])
                remaining = remaining[2:]
            elif code in obscurations:
                phenomena_list.append(obscurations[code])
                remaining = remaining[2:]
            elif code in other:
                phenomena_list.append(other[code])
                remaining = remaining[2:]
            else:
                # Unknown code, skip it
                remaining = remaining[2:]
        
        # Build the final description
        if intensity:
            if intensity:
                result_parts.append(intensity)
        
        if descriptor:
            result_parts.append(descriptor)
        
        if phenomena_list or vicinity:
            if phenomena_list:
                result_parts.append(' and '.join(phenomena_list))
            if vicinity:
                result_parts.append('in vicinity')
        
        # If no parts were decoded, return the original string
        if not result_parts:
            return weather_string
        
        # Join and capitalize properly
        result = ' '.join(result_parts)
        return result.capitalize() if result else weather_string

if __name__ == "__main__":
    metar : Metar = Metar("KSLC", "json", 2.0)
    print(metar.url)

    print("Current UTC Time:", metar.zuluTimeReadable) 

    print("Fetched data:")
    print("KSLC METAR:", metar.data[0]['icaoId'])
    print("Observation Time:", metar.observationTime)
    print("Temperature (C):", metar.temperatureC)
    print("Dewpoint (C):", metar.dewpointC)
    print("Altimeter Setting (inHg):", metar.altimeterSetting)
    print("Pressure (inHg):", metar.pressureInchesHg)
    print("Elevation (ft):", metar.elevationFeet)
    print("Pressure Altitude (ft):", metar.pressureAltitude)
    print("Density Altitude (ft):", metar.densityAltitude)
    print("Wind:", f"{metar.windDirectionDeg}° at {metar.windSpeedKts} kts, Gusts: {metar.windGustKts} kts")
    print("Visibility (statute miles):", metar.visibilityStatuteMiles)
    print("Clouds:", metar.clouds)
    print("Weather:", metar.weather)
    print("Flight Category:", metar.flightCategory)
    
    # Test weather decoder
    print("\n--- Weather Decoder Tests ---")
    test_codes = ['+RA', '-SN', '+SHRA', 'FG', 'VCFG', 'BLSN', 'TSRA', '+FC', 
                  'BR', 'FZRA', 'MIFG', 'BCFG', 'SHRA', '-DZ', 'GR', 'VCTS']
    
    for code in test_codes:
        decoded = metar.decodeWeather(code)
        print(f"{code:8} -> {decoded}")