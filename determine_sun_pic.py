import urllib.request
import json
import sys
import datetime


# Function to get sunrise and sunset times from the Open-Meteo API
def get_sunrise_sunset(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=sunrise,sunset&timezone=auto"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)

        if "daily" not in data:
            print("Error: Missing daily data in response.")
            sys.exit(1)

        sunrise = data["daily"]["sunrise"][0]
        sunset = data["daily"]["sunset"][0]

        # Convert from ISO 8601 to datetime
        sunrise_time = datetime.datetime.fromisoformat(sunrise)
        sunset_time = datetime.datetime.fromisoformat(sunset)

        return sunrise_time, sunset_time
    except Exception as e:
        print(f"Error getting sunrise and sunset data: {e}")
        sys.exit(1)


# Function to get the current time in the provided location using TimeZoneDB API
def get_current_time(lat, lon):
    api_key = "YOUR_API_KEY"
    url = f"http://api.timezonedb.com/v2.1/get-time-zone?key={api_key}&format=json&by=position&lat={lat}&lng={lon}"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)

        if data.get("status") != "OK":
            print("Error: Invalid response from TimeZoneDB.")
            sys.exit(1)

        # Extract current time from the response
        current_time_utc = data["formatted"]
        current_time = datetime.datetime.strptime(current_time_utc, "%Y-%m-%d %H:%M:%S")

        return current_time
    except Exception as e:
        print(f"Error getting current time data: {e}")
        sys.exit(1)


# Function to determine which wallpaper to use based on current time and sun position
def determine_wallpaper(sunrise, sunset, current_time):
    sunrise_time = sunrise.time()
    sunset_time = sunset.time()
    current_time_only = current_time.time()

    # Combine time with date to create datetime objects for arithmetic
    today = datetime.date.today()
    sunrise_datetime = datetime.datetime.combine(today, sunrise_time)
    sunset_datetime = datetime.datetime.combine(today, sunset_time)
    current_datetime = datetime.datetime.combine(today, current_time_only)

    # Define time ranges for different wallpapers

    # Morning start: 30 minutes after sunrise
    morning_start = sunrise_datetime + datetime.timedelta(minutes=30)

    # Morning end: 6 hours after sunrise
    morning_end = sunrise_datetime + datetime.timedelta(hours=6)

    # Noon start: 6 hours after sunrise
    noon_start = sunrise_datetime + datetime.timedelta(hours=6)

    # Evening start: 1 hour before sunset
    evening_start = sunset_datetime - datetime.timedelta(hours=1)

    # Sunset start: sunset time
    sunset_start = sunset_datetime

    # Night start: 30 minutes after sunset
    night_start = sunset_datetime + datetime.timedelta(minutes=30)

    # Determine which time period it is
    if sunrise_datetime <= current_datetime < morning_start:
        return "sunrise.png"
    elif morning_start <= current_datetime < morning_end:
        return "morning.png"
    elif noon_start <= current_datetime < evening_start:
        return "noon.png"
    elif evening_start <= current_datetime < sunset_start:
        return "evening.png"
    elif (
        sunset_start
        <= current_datetime
        < (sunset_datetime + datetime.timedelta(minutes=30))
    ):
        return "sunset.png"
    elif current_datetime >= night_start:
        return "night.png"
    else:
        return "night.png"


# Main function to take in coordinates and compute the result
def main():
    while True:
        if len(sys.argv) != 3:
            print("Please provide latitude and longitude.")
            latitude = float(input("Enter latitude: "))
            longitude = float(input("Enter longitude: "))
        else:
            latitude = float(sys.argv[1])
            longitude = float(sys.argv[2])

        # Get the sunrise and sunset times from the Open-Meteo API
        sunrise, sunset = get_sunrise_sunset(latitude, longitude)

        # Get the current time from the TimeZoneDB API
        current_time = get_current_time(latitude, longitude)

        # Print the relevant times to debug
        print(f"Sunrise: {sunrise}, Sunset: {sunset}, Current Time: {current_time}")

        # Determine the correct wallpaper to display based on the times
        wallpaper = determine_wallpaper(sunrise, sunset, current_time)
        print(f"Wallpaper: {wallpaper}")

        # Ask the user to press any key to continue, or 'q' to quit
        continue_choice = (
            input("\nPress any key to continue or 'q' to quit: \n").strip().lower()
        )
        if continue_choice == "q":
            print("Exiting the program.")
            break  # Exit the loop if the user chooses 'q'


if __name__ == "__main__":
    main()
