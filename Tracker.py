import json
import requests
import sqlite3
import time

# Track the ISS in real time and log the coordinates to the database
def track_iss():
    iss_location = requests.get("http://api.open-notify.org/iss-now.json") 
    iss_json = iss_location.json()
    coordinates = iss_json["iss_position"]
    timestamp = iss_json["timestamp"]
    print("The ISS is currently at Latitude:", coordinates["latitude"], "and Longitude:", coordinates["longitude"], "Timestamp:", time.ctime(timestamp))
    log_to_db()

# Save to Database
def log_to_db():
    iss_location = requests.get("http://api.open-notify.org/iss-now.json") 
    iss_json = iss_location.json()
    coordinates = iss_json["iss_position"]
    timestamp = iss_json["timestamp"]
    dbConnect = sqlite3.connect("ISS.db")
    c = dbConnect.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS iss_position (timestamp text, latitude int, longitude int)")
    values = [(timestamp), (coordinates["latitude"]), (coordinates["longitude"])]
    c.execute("INSERT INTO iss_position (timestamp, latitude, longitude) VALUES (?, ?, ?)", values)
    dbConnect.commit()
    print("Saving to database...")
    dbConnect.close()
    print("Done")

# Check who and how many are on board and print to screen
def astronauts():
    astronauts = requests.get("http://api.open-notify.org/astros.json")
    astronauts_json = astronauts.json()
    print("There are currently", astronauts_json["number"], "people on board the ISS. They are...")
    for astronaut in astronauts_json["people"]:
        print("Astronaut",  astronaut["name"], "who is on board the", astronaut["craft"])

def api_service_check():
    open_notify_api = requests.get("http://api.open-notify.org")
    if open_notify_api.status_code != 200:
        print("Looks like the API service is down. Please try again later.")
        exit()
    else:
        astronauts()

#Check API 
api_service_check()

# Start tracking the ISS
print("Starting tracking, press 'Ctrl + C' to stop...")

try:
    while True:
        track_iss()
        log_to_db()
        time.sleep(5)
except KeyboardInterrupt:
    print("Stopping tracking.\nThanks for using!")
    exit()
