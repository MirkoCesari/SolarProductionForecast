import requests, json, os
from datetime import datetime, timedelta

dir_path = os.path.dirname(os.path.realpath(__file__))
ConfigFilePath = os.path.join(dir_path, 'ConfigSolar.json')

with open(ConfigFilePath) as user_file:
    file_contents = user_file.read()
Config = json.loads(file_contents)

def get_production_estimate(latitude, longitude, declination, azimuth, kwp, debug = False):

    url = f'https://api.forecast.solar/estimate/{latitude}/{longitude}/{declination}/{azimuth}/{kwp}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        now = datetime.now()
        today = now.date()

        watts_data = data["result"]["watts"]
        RemainingAPICalls = data["message"]["ratelimit"]["remaining"]

        #Flag used to declare if data has been found
        message = ""
        data_found = False

        for timestamp, watt_value in watts_data.items():

            time_of_production = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

            if time_of_production.date() == today and time_of_production >= now:
                message = "The production estimation for today is: \n"
                message += f"Time: {time_of_production}, Production: {watt_value} W\n"

                data_found = True 

        # Search on the next day only if the data for the current day is empty
        if not data_found:
            message = "The production estimation for tomorrow is: \n"

            # Define the time offset
            tomorrow = (now + timedelta(days=1)).date()

            for timestamp, watt_value in watts_data.items():
                time_of_production = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

                if time_of_production.date() == tomorrow:
                    message += f"Time: {time_of_production}, Production: {watt_value} W\n"

        if debug:
            message += f"Remaining API calls: {RemainingAPICalls}"

        # Return the extracted data
        return message
    else:
        #Return the error code
        message = f"Error code:{response.status_code}"

        # 429 indicate that the API rate limit has been exceeded, 
        # extract from the response the next availability and return it in the Error message
        if response.status_code == 429:
            data = response.json()
            ErrorText = data["message"]["text"]
            NextAvailability = data["message"]["ratelimit"]["retry-at"]
            message = f"Error description: {ErrorText} \nRetry at: {NextAvailability}"
 
        return message

if __name__ == "__main__":
    latitude = Config["Forecast"]["latitude"]
    longitude = Config["Forecast"]["longitude"]
    declination =  Config["Forecast"]["declination"]
    azimuth = Config["Forecast"]["azimuth"]  #  (0=N, 90=E, 180=S, 270=W)
    kwp = Config["Forecast"]["kwp"]   # Solar power installed (kWp)
    print(get_production_estimate(latitude, longitude, declination, azimuth, kwp))
    input("Press any key to close the application\n")