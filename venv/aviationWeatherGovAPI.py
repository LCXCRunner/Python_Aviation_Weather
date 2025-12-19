from flask import Flask, render_template_string, send_from_directory, request, jsonify
import os
import requests
from requests.models import Response
from Metar import Metar

# Set the parent directory as the root folder for templates and static files
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, 
            static_folder=parent_dir,
            template_folder=parent_dir)

@app.route('/')
def index():
    # # grab the metar data as the page loads
    # firstMetar : Metar = Metar("KSLC", "json", 2.0)
    # secondMetar : Metar = Metar("KOGD", "json", 2.0)
    # thirdMetar : Metar = Metar("KHIF", "json", 2.0)

    # Read the HTML file from parent directory
    html_path = os.path.join(parent_dir, 'index.html')
    with open(html_path, 'r') as f:
        html_content = f.read()
    
    return render_template_string(html_content)

@app.route('/styles.css')
def stylesheet():
    # Serve the CSS file from parent directory
    return send_from_directory(parent_dir, 'styles.css')

@app.route('/Typescript/eventListeners.js')
def javascript():
    # Serve the JavaScript file from Typescript directory
    typescript_dir = os.path.join(parent_dir, 'Typescript')
    return send_from_directory(typescript_dir, 'eventListeners.js')

@app.route('/button-click')
def button_click():
    firstMetar : Metar = Metar("KSLC", "json", 2.0)
    secondMetar : Metar = Metar("KOGD", "json", 2.0)
    thirdMetar : Metar = Metar("KHIF", "json", 2.0)
    return 'OK'

@app.route('/get-metar', methods=['POST'])
def get_metar():
    """
    Endpoint to fetch METAR data for a given airport code.
    Expects JSON: {"airport": "KSLC"}
    Returns METAR data as JSON
    """
    try:
        data = request.get_json()
        airport_code = data.get('airport', '').upper()
        
        if not airport_code:
            return jsonify({'error': 'Airport code is required'}), 400
        
        # Fetch METAR data
        metar = Metar(airport_code, "json", 2.0)
        
        # Return relevant data
        return jsonify({
            'success': True,
            'airport': airport_code,
            'observationTime': metar.observationTime,
            'temperature': round(metar.temperatureC * 9/5 + 32),  # Convert to Fahrenheit
            'dewpoint': round(metar.dewpointC * 9/5 + 32),  # Convert to Fahrenheit
            'altimeter': metar.altimeterSetting,
            'pressureAltitude': metar.pressureAltitude,
            'densityAltitude': metar.densityAltitude,
            'windSpeed': metar.windSpeedKts,
            'windDirection': metar.windDirectionDeg,
            'windGust': metar.windGustKts,
            'visibility': metar.visibilityStatuteMiles,
            'clouds': metar.clouds,
            'weather': metar.weather,
            'flightCategory': metar.flightCategory
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

if __name__ == '__main__':
    print("Starting simple Flask app...")
    print(f"Serving files from: {parent_dir}")
    print("Visit http://localhost:5000 to view the page")
    app.run(host='0.0.0.0', port=5000)