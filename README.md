# Wallpaper Time Based on Sunrise and Sunset

## Overview
------------------------------------------------------------
This Python script determines which wallpaper to display based on the current time of day, considering the user's location. The script retrieves the sunrise and sunset times, along with the current time for the provided latitude and longitude. Based on this data, it selects an appropriate wallpaper (e.g., sunrise, morning, noon, evening, sunset, night). This is useful for creating a dynamic wallpaper system that adapts to natural lighting conditions.

## Key Functionality
------------------------------------------------------------
1. **Get Sunrise and Sunset Times**:
   - Uses the Open-Meteo API to retrieve the daily sunrise and sunset times for the given latitude and longitude.
   - The times are parsed from ISO 8601 format into Python `datetime` objects for easier manipulation.

2. **Get Current Time**:
   - Uses the TimeZoneDB API to fetch the current local time at the provided latitude and longitude.
   - This allows the program to account for the user's time zone and compare it with the sunrise and sunset times.

3. **Wallpaper Selection Logic**:
   Based on the current time, the script classifies the day into different periods (morning, noon, evening, sunset, and night). Each period corresponds to a different wallpaper:
   
   - **Sunrise**: 30 minutes before sunrise until morning starts.
   - **Morning**: From 30 minutes after sunrise to 6 hours after sunrise.
   - **Noon**: From 6 hours after sunrise until 1 hour before sunset.
   - **Evening**: From 1 hour before sunset until sunset time.
   - **Sunset**: The actual sunset time.
   - **Night**: From 30 minutes after sunset onward.

4. **User Input and Loop**:
   - The script accepts latitude and longitude as command-line arguments or prompts the user for input.
   - After displaying the wallpaper based on the current time, the user is asked if they want to continue or quit the program.

## Workflow
------------------------------------------------------------
1. The program fetches sunrise and sunset data based on the provided location.
2. It retrieves the current time in the same location.
3. Using these times, it compares the current time to the defined time periods and selects the corresponding wallpaper image.
4. The wallpaper choice is then printed to the console.
5. The program asks the user if they want to continue or quit.

## API Endpoints
------------------------------------------------------------
1. **Open-Meteo API**: Used to fetch the sunrise and sunset times.
   - Endpoint: [https://api.open-meteo.com/v1/forecast](https://api.open-meteo.com/v1/forecast)
   - Parameters: `latitude`, `longitude`, `daily=sunrise,sunset`, `timezone=auto`

2. **TimeZoneDB API**: Used to fetch the current local time.
   - Endpoint: [http://api.timezonedb.com/v2.1/get-time-zone](http://api.timezonedb.com/v2.1/get-time-zone)
   - Parameters: `key=<Your API Key>`, `format=json`, `by=position`, `lat=<latitude>`, `lng=<longitude>`

## Notes
------------------------------------------------------------
- The `API_KEY` API key is used for the TimeZoneDB API. You need to replace it with your own key.
