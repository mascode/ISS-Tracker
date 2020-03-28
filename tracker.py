import requests
import sqlite3
import time

__API__ = requests.get("http://api.open-notify.org/iss-now.json")
__JSON__ = __API__.json()
__COORDINATES__ = __JSON__["iss_position"]
__TIMESTAMP__ = __JSON__["timestamp"]

# Grab the ISS' location as coordinates and timestamp as timestamp
def get_iss_data():
    global __COORDINATES__
    global __TIMESTAMP__
    __API__ = requests.get("http://api.open-notify.org/iss-now.json")
    __JSON__ = __API__.json()
    __COORDINATES__ = __JSON__["iss_position"]
    __TIMESTAMP__ = __JSON__["timestamp"]

# Track the ISS in real time and log the coordinates to the database
def track_iss():
    get_iss_data()
    print("The ISS is currently at Latitude:", __COORDINATES__["latitude"], "and Longitude:", __COORDINATES__["longitude"], "Timestamp:", time.ctime(__TIMESTAMP__))
    log_coordinates_to_db()
    
# Save coordinates to Database
def log_coordinates_to_db():
    dbConnect = sqlite3.connect("ISS.db")
    c = dbConnect.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS iss_position (id integer primary key autoincrement, timestamp text, latitude real, longitude real)")
    values = [time.ctime(__TIMESTAMP__), (__COORDINATES__["latitude"]), (__COORDINATES__["longitude"])]
    c.execute("INSERT INTO iss_position (timestamp, latitude, longitude) VALUES (?, ?, ?)", values)
    dbConnect.commit()
    c.close()
    dbConnect.close()
    print("Done saving to database.")

# Check who and how many are on board and print to screen
def astronauts():
    astronauts = requests.get("http://api.open-notify.org/astros.json")
    astronauts_json = astronauts.json()
    print("There are currently", astronauts_json["number"], "people on board the ISS. They are...")
    for astronaut in astronauts_json["people"]:
        print("Astronaut",  astronaut["name"], "who is on board the", astronaut["craft"])

# Make sure the service is up before proceeding
def api_service_check():
    open_notify_api = requests.get("http://api.open-notify.org")
    if open_notify_api.status_code != 200:
        print("Looks like the API service is down. Please try again later.")
        exit()
    else:
        astronauts()

# Start tracking the ISS
if __name__ == "__main__":
    api_service_check()
    print("\nStarting tracking, press 'Ctrl + C' to stop...\n")
    try:
        while True:
            track_iss()
            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopping tracking.\nThanks for using!")
        exit()


