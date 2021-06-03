import requests
import sqlite3
import datetime
import time
from rich import print
from rich.console import Console

# Grab the ISS' location as coordinates and timestamp as timestamp
def get_iss_data():
    global __COORDINATES__
    global __TIMESTAMP__
    __API__ = requests.get("http://api.open-notify.org/iss-now.json").json()
    __COORDINATES__ = __API__["iss_position"]
    __TIMESTAMP__ = __API__["timestamp"]

# Track the ISS in real time and log the coordinates to the database
def track_iss():
    get_iss_data()
    print("The ISS is currently at [blue][underline]Latitude:", __COORDINATES__["latitude"], "and [blue][underline]Longitude:", __COORDINATES__["longitude"], "Timestamp:", datetime.datetime.fromtimestamp(__TIMESTAMP__).strftime('%Y-%m-%d %H:%M:%S'))
    log_coordinates_to_db()


# Save coordinates to Database
def log_coordinates_to_db():
    dbConnect = sqlite3.connect("ISS.db")
    c = dbConnect.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS iss_position (id integer primary key autoincrement, timestamp text, latitude real, longitude real)")
    values = [datetime.datetime.fromtimestamp(__TIMESTAMP__).strftime('%Y-%m-%d %H:%M:%S'), (__COORDINATES__["latitude"]), (__COORDINATES__["longitude"])]
    c.execute("INSERT INTO iss_position (timestamp, latitude, longitude) VALUES (?, ?, ?)", values)
    dbConnect.commit()
    c.close()
    dbConnect.close()
    #print("Done saving to database.")

# Check who and how many are on board and print to screen
def astronauts():
    astronauts = requests.get("http://api.open-notify.org/astros.json").json()
    print("There are currently", astronauts["number"], "people on board the ISS. They are...")
    for astronaut in astronauts["people"]:
        print("Astronaut",  astronaut["name"], "who is on board the", astronaut["craft"])

# Make sure the service is up before proceeding
def api_service_check():
    open_notify_api = requests.get("http://api.open-notify.org")
    if open_notify_api.status_code != 200:
        print("Looks like the API service is down. Trying again in 5 minutes.")
        time.sleep(300)
        api_service_check()
    else:
        print("[bold green] API is service is good to go! :white_check_mark:")
        astronauts()

# Start tracking the ISS
if __name__ == "__main__":
    api_service_check()
    print("\n:earth_americas: [bold green]Starting tracking, press 'Ctrl + C' to stop...\n")
    try:
        console = Console()
        while True:
            track_iss()
            with console.status("[bold green]Tracking the ISS ", spinner='earth') as status:
                time.sleep(3)
    except KeyboardInterrupt:
        print("Stopping tracking.")
        exit()
