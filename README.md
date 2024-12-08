# Forecast Solar API Script

This script uses the **Forecast.Solar** API to retrieve solar energy production estimates based on geographic coordinates, panel tilt and orientation, and installed power (kWp).

## Features

- Calculates production estimates for today or tomorrow based on available data.
- Provides detailed information on times and estimated production in Watts.
- Displays remaining API calls (optional).
- Handles API errors and rate limits, providing helpful details.

## Requirements

- **Python 3.7+**
- Python modules:
  - `requests`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MirkoCesari/SolarProductionForecast.git
   cd SolarProductionForecast

2. Install dependencies:
    
       pip install requests

3. Create a configuration file ConfigSolar.json in the script directory with the following structure:
   ```bash
       {
        "Forecast": {
            "latitude": 41.8902,
            "longitude": 12.4922,
            "declination": 30,
            "azimuth": 180,
            "kwp": 5.0
        }
       }

4. Usage

     Run the script from the terminal:
    
       python ForecastSolarAPI.py

 The script will display production estimates for today or tomorrow, depending on the data availability.

## Options

Debug Mode: You can enable debug mode by passing debug=True to the function get_production_estimate, which will display additional information such as remaining API calls.

## Common Errors

Error 429: API rate limit exceeded. The script will return the error message with the time when new requests will be allowed.

Error 200 with no data: If no production data is available for today, the script will attempt to fetch estimates for tomorrow.

## License

This project is licensed under the MIT License. See the LICENSE file for details.


## Contributing

Contributions are welcome! Feel free to open issues or pull requests.

