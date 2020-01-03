import json
import requests
import sqlite3
import time

# Grab ISS' location and add the JSON to a variable 
iss_location = requests.get("http://api.open-notify.org/iss-now.json")
iss_json = iss_location.json()

# Parse the some data from the returned JSON
coordinates = iss_json["iss_position"]
timestamp = iss_json["timestamp"]

# Define functions

# Save to Database
def log_to_db():
    dbConnect = sqlite3.connect("ISS.db")
    c = dbConnect.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS iss_position (timestamp text, latitude int, longitude int)")
    values = [(timestamp), (coordinates["latitude"]), (coordinates["longitude"])]
    c.execute("INSERT INTO iss_position (timestamp, latitude, longitude) VALUES (?, ?, ?)", values)
    dbConnect.commit()
    print("Saving to database...")
    dbConnect.close()
    print("Done")

# Track the ISS in real time
def track_iss():
    print("The ISS is currently at Latitude:", coordinates["latitude"], "and Longitude:", coordinates["longitude"], "Timestamp:", time.ctime(timestamp))
    log_to_db()

# Check who and how many are on board and print to screen

# Grab JSON data
astronauts = requests.get("http://api.open-notify.org/astros.json")
astronauts_json = astronauts.json()

#Loop through the astronauts name
print("There are currently", astronauts_json["number"], "people on board the ISS. They are...")
for astronaut in astronauts_json["people"]:
     print("Astronaut",  astronaut["name"], "who is on board the", astronaut["craft"])

# Start tracking the ISS
print("Starting tracking, press 'Ctrl + C' to stop...")

try:
    while iss_location.status_code == 200:
        iss_location = requests.get("http://api.open-notify.org/iss-now.json")
        iss_json = iss_location.json()
        coordinates = iss_json["iss_position"]
        timestamp = iss_json["timestamp"]
        track_iss()
        time.sleep(5)
except KeyboardInterrupt:
    print("Stopping tracking.\nThanks for using!")
    exit()
