// don't forget to compile the TypeScript file to JavaScript using tsc

// To debug, make sure your launch.json in .vscode is set up correctly to run Flask app
// Select the Flask + TypeScript Debug configuration before running

// Wait for DOM to load
document.addEventListener('DOMContentLoaded', () => {
    // Add event listeners for airport input fields
    const airport1Input = document.getElementById('airport1') as HTMLInputElement;
    const airport2Input = document.getElementById('airport2') as HTMLInputElement;
    const airport3Input = document.getElementById('airport3') as HTMLInputElement;

    // Load saved values from localStorage on page load
    const savedAirport1 = localStorage.getItem('airport1');
    const savedAirport2 = localStorage.getItem('airport2');
    const savedAirport3 = localStorage.getItem('airport3');
    
    if (savedAirport1) {
        airport1Input.value = savedAirport1;
    }
    if (savedAirport2) {
        airport2Input.value = savedAirport2;
    }
    if (savedAirport3) {
        airport3Input.value = savedAirport3;
    }

    // Save airport1 to localStorage when it changes
    airport1Input.addEventListener('input', () => {
        localStorage.setItem('airport1', airport1Input.value);
    });

    // Save airport2 to localStorage when it changes
    airport2Input.addEventListener('input', () => {
        localStorage.setItem('airport2', airport2Input.value);
    });

    // Save airport3 to localStorage when it changes
    airport3Input.addEventListener('input', () => {
        localStorage.setItem('airport3', airport3Input.value);
    });

    // update the metar data for all three airports on page load
    fetchMetarData(airport1Input.value, 1);
    fetchMetarData(airport2Input.value, 2);
    fetchMetarData(airport3Input.value, 3);

    // Function to fetch and update METAR data
    function fetchMetarData(airportCode: string, columnNumber: number) {
        if (!airportCode || airportCode.trim() === '') {
            return;
        }

        // Get the appropriate input field
        let inputField: HTMLInputElement | null = null;
        if (columnNumber === 1) inputField = airport1Input;
        if (columnNumber === 2) inputField = airport2Input;
        if (columnNumber === 3) inputField = airport3Input;

        fetch('/get-metar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ airport: airportCode.toUpperCase() })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log(`METAR data for ${airportCode}:`, data);
                updateDisplay(data, columnNumber);
            } else {
                console.error('Error fetching METAR:', data.error);
                // Clear the input field if airport doesn't exist
                if (inputField) {
                    inputField.value = '';
                    localStorage.removeItem(`airport${columnNumber}`);
                }
                alert(`Error: Airport "${airportCode}" not found or invalid.`);
            }
        })
        .catch(error => {
            console.error('Error calling Flask:', error);
            // Clear the input field on network error
            if (inputField) {
                inputField.value = '';
                localStorage.removeItem(`airport${columnNumber}`);
            }
            alert(`Failed to fetch METAR data: ${error}`);
        });
    }

    // Function to update the display with METAR data
    function updateDisplay(data: any, columnNumber: number) {
        const column = document.querySelector(`.column${columnNumber}`) as HTMLElement;
        if (!column) return;

        const values = column.querySelectorAll('.value');
        // Update each field based on the data
        if (values[0]) {
            values[0].textContent = data.observationTime || '--';
        }
        if (values[1]) {
            values[1].textContent = data.flightCategory !== null ? `${data.flightCategory}` : '--';
        }
        if (values[2]) {
            values[2].textContent = data.temperature !== null ? `${data.temperature} °F` : '--';
        }
        if (values[3]) {
            values[3].textContent = data.dewpoint !== null ? `${data.dewpoint} °F` : '--';
        }
        if (values[4]) {
            values[4].textContent = data.altimeter !== null ? `${data.altimeter} inHg` : '--';
        }
        if (values[5]) {
            values[5].textContent = data.pressureAltitude !== null ? `${data.pressureAltitude} ft` : '--';
        }
        if (values[6]) {
            values[6].textContent = data.densityAltitude !== null ? `${data.densityAltitude} ft` : '--';
        }
        if (values[7]) {
            values[7].textContent = data.windDirection !== null && data.windSpeed !== null ? `${data.windDirection}° at ${data.windSpeed} kt` : '--';
        }
        if (values[8]) {
            values[8].textContent = data.windGust !== null ? `Gusts: ${data.windGust} kt` : '';
        }
        if (values[9]) {
            values[9].textContent = data.visibility !== null ? `${data.visibility} SM` : '--';
        }
        if (values[10]) {
            values[10].textContent = data.clouds !== null ? `${data.clouds}` : '--';
        }
        if (values[11]) {
            values[11].textContent = data.weather !== null ? `${data.weather}` : '--';
        }
        console.log(`Updating column ${columnNumber} with data:`, data);
    }

    // Add blur event listeners (when user leaves input field)
    if (airport1Input) {
        airport1Input.addEventListener('blur', () => {
            fetchMetarData(airport1Input.value, 1);
        });
        // Also trigger on Enter key
        airport1Input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                fetchMetarData(airport1Input.value, 1);
            }
        });
    }

    if (airport2Input) {
        airport2Input.addEventListener('blur', () => {
            fetchMetarData(airport2Input.value, 2);
        });
        airport2Input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                fetchMetarData(airport2Input.value, 2);
            }
        });
    }

    if (airport3Input) {
        airport3Input.addEventListener('blur', () => {
            fetchMetarData(airport3Input.value, 3);
        });
        airport3Input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                fetchMetarData(airport3Input.value, 3);
            }
        });
    }

    // Update UTC time display every second
    function updateZuluTime() {
        const now = new Date();
        const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 
                          'July', 'August', 'September', 'October', 'November', 'December'];
        const utcDay = now.getUTCDate();
        const utcMonth = monthNames[now.getUTCMonth()];
        const hours = String(now.getUTCHours()).padStart(2, '0');
        const minutes = String(now.getUTCMinutes()).padStart(2, '0');
        const seconds = String(now.getUTCSeconds()).padStart(2, '0');
        
        const zuluTimeDisplay = document.getElementById('zuluTimeDisplay');
        if (zuluTimeDisplay) {
            zuluTimeDisplay.textContent = `${utcMonth} ${utcDay} - ${hours}:${minutes}:${seconds} UTC`;
        }
    }

    // Update immediately and then every second
    updateZuluTime();
    setInterval(updateZuluTime, 1000);

    // Auto-refresh page every 15 minutes (900000 milliseconds)
    setInterval(() => {
        location.reload();
    }, 900000);
});