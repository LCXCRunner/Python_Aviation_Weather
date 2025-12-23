# Aviation Weather Display

A Flask-based web application that fetches and displays real-time METAR (Meteorological Aerodrome Report) data for up to three airports simultaneously.

## Features

- **Real-time METAR Data**: Fetches current weather observations from the Aviation Weather API
- **Multi-Airport Support**: Display weather for up to three airports simultaneously
- **Automatic Calculations**:
  - Pressure altitude
  - Density altitude
  - Temperature conversions (Celsius to Fahrenheit)
- **Flight Categories**: Visual indicators for VFR, MVFR, IFR, and LIFR conditions
- **Persistent Storage**: Remembers your selected airports using localStorage
- **Responsive Design**: Clean, readable interface for desktop and mobile devices
- **Raspberry Pi Compatible**: Can be deployed as a fullscreen kiosk display

## Technologies

- **Backend**: Python 3, Flask
- **Frontend**: HTML, CSS, TypeScript
- **API**: Aviation Weather Center (aviationweather.gov)

## Project Structure

```
Python_Aviation_Weather/
├── aviationWeatherGovAPI.py   # Flask application and API routes
├── Metar.py                    # METAR data parser and calculator
├── index.html                  # Main web interface
├── styles.css                  # Styling
├── Typescript/
│   ├── eventListeners.ts       # TypeScript source
│   ├── eventListeners.js       # Compiled JavaScript
│   └── tsconfig.json          # TypeScript configuration
├── Visual_Assets/             # Images and graphics
└── venv/                      # Python virtual environment
```

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/LCXCRunner/Python_Aviation_Weather.git
   cd Python_Aviation_Weather
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Compile TypeScript (optional)**
   ```bash
   cd Typescript
   tsc
   ```

## Usage

### Development Mode

Run the Flask application:
```bash
python aviationWeatherGovAPI.py
```

Visit `http://localhost:5000` in your web browser.

### Debugging in VS Code

#### Flask Instance

1. Ensure proper `launch.json` configuration for Flask debugging
2. Select "Python: Flask Debug" configuration
3. Press F5 to start debugging

#### Flask and Event Listeners

1. Ensure proper `launch.json` configuration for Flask + Typescript debugging
2. Select "Flask + TypeScript Debug" configuration
3. Press F5 to start debugging, make sure the flask app is running and you are accessing the `http://localhost:5000` on your browser. You can then click buttons, typing in inputs, ect to debug. 

## Deployment

### Raspberry Pi Kiosk Setup

The project includes instructions for deploying on a Raspberry Pi as a fullscreen kiosk display:

1. **Create systemd service** (`/etc/systemd/system/flaskapp.service`):
   ```ini
   [Unit]
   Description=Flask App
   After=network-online.target

   [Service]
   User=jakeg
   WorkingDirectory=/home/jakeg/Documents/Python_Aviation_Weather
   ExecStart=/usr/bin/python /home/jakeg/Documents/Python_Aviation_Weather/aviationWeatherGovAPI.py
   Restart=always
   Environment="FLASK_ENV=production"

   [Install]
   WantedBy=multi-user.target
   ```

2. **Enable and start the service**:
   ```bash
   sudo systemctl enable flaskapp.service
   sudo systemctl start flaskapp.service
   sudo systemctl status flaskapp.service
   ```

3. **Create desktop launcher** for Chromium fullscreen mode:
   ```bash
   #!/bin/bash
   /usr/bin/chromium-browser http://localhost:5000 --start-fullscreen \
     --disable-gpu --disable-software-rasterizer \
     --disable-accelerated-2d-canvas --disable-infobars \
     --disable-session-crashed-bubble --no-sandbox \
     --force-device-scale-factor=0.67
   ```
   NOTE: F11 to exit fullscreen mode

4. **Changing the .service file will require you to restart the systemctl deamon if you are troubleshooting**
    ```bash
    restart it if needed and then check if it is running again:
    sudo systemctl daemon-reload
    sudo systemctl restart flaskapp.service
    systemctl status flaskapp.service
    ```

## API Endpoints

### `GET /`
Serves the main HTML interface

### `GET /styles.css`
Serves the stylesheet

### `GET /Typescript/eventListeners.js`
Serves the compiled JavaScript

### `POST /get-metar`
Fetches METAR data for a specified airport

**Request Body:**
```json
{
  "airport": "KSLC"
}
```

**Response:**
```json
{
  "success": true,
  "airport": "KSLC",
  "observationTime": "December 22, 2025 18:53 UTC",
  "temperature": 32,
  "dewpoint": 25,
  "altimeter": 30.12,
  "pressureAltitude": 4220,
  "densityAltitude": 3890,
  "windSpeed": 8,
  "windDirection": 160,
  "windGust": null,
  "visibility": 10,
  "clouds": [...],
  "weather": [...],
  "flightCategory": "VFR"
}
```

## Data Sources

Weather data is retrieved from the [Aviation Weather Center API](https://aviationweather.gov/), which provides official METAR observations from airports worldwide.

## License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Author

Jake G. ([@LCXCRunner](https://github.com/LCXCRunner))

## Acknowledgments

- Aviation Weather Center for providing the METAR API
- Built for the aviation community and computer hobbiests
