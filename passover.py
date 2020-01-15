import json
import requests
import time
from datetime import datetime
import sqlite3

def global_position():
    print("Grabbing location now...")
    lat = float(input("What is your latitude? "))
    lon = float(input("What is your longitude? "))
    values = [(lat), (lon)]
    db_connect = sqlite3.connect("ISS.db")
    c = db_connect.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS location (id integer primary key, lat real, lon real)")
    c.execute("INSERT INTO location (lat, lon) VALUES (?, ?)", values)
    c.close()
    db_connect.commit()
    db_connect.close()
    print("Location saved to database")
    passing_times_with_db()

def check_for_location():
    db_connect = sqlite3.connect("ISS.db")
    c = db_connect.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS location (id integer primary key, lat real, lon real)")
    db_connect.commit()
    c.execute("SELECT id FROM location WHERE id = 1")
    query = c.fetchone()
    if query is None:
        print("User Location not found")
        c.close()
        db_connect.close()
        global_position()
    else:
        print("Location found..")
        c.close()
        db_connect.close()
        passing_times_with_db()

def passing_times_with_db():
    db_connect = sqlite3.connect("ISS.db")
    c = db_connect.cursor()
    c.execute("SELECT lat, lon FROM location WHERE id = 1")
    query = c.fetchone()
    coordinates = {"lat": (query[0]), "lon": (query[1])}
    next_fly_over = requests.get("http://api.open-notify.org/iss-pass.json", params=coordinates)
    pass_times = next_fly_over.json()['response']
    print("The next time the ISS will pass over your location, in a 7 hour period, is...")
    # Grab Rise Times
    rise_times = []
    for rise_time in pass_times:
        time = datetime.fromtimestamp(rise_time['risetime'])
        rise_times.append(time)
        print(time)

def passing_times_with_parameters():
    print("Where would you like to check the rise times for?")
    lat_p = float(input("Please enter a latitude: "))
    lon_p = float(input("Please enter a longitude: "))
    values = {"lat": (lat_p), "lon": (lon_p)}
    fly_over = requests.get("http://api.open-notify.org/iss-pass.json", params=values)
    pass_times = fly_over.json()['response']
    print("The next time the ISS will pass over your location, in a 7 hour period, is...")
    rise_times = []
    for rise_time in pass_times:
        time = datetime.fromtimestamp(rise_time['risetime'])
        rise_times.append(time)
        print(time)
    choices()


def choices():
    print("What would you like to do next?")
    print("1. Clear the database and save a new location")
    print("2. Check another location (Without saving to the dabase)")
    print("3. Exit the program")
    while True:
        try:
            x = int(input(">>> Choose 1-3: "))
            break
        except ValueError:
            print("Oops! Incorrect selection, choose a number between 1 and 3")
    if x == 1:
        print("Clearing the database..")
        db_connect = sqlite3.connect("ISS.db")
        c = db_connect.cursor()
        c.execute("DELETE FROM location WHERE id = 1")
        c.close()
        db_connect.commit()
        db_connect.close()
        print("Database cleared")
        global_position()
    elif x == 2:
        print("Checking times with user parameters") 
        passing_times_with_parameters()
    elif x == 3:
        print("Exiting the program.")
        exit() 
    elif x > 3:
        print("Please enter a number between 1 and 3")
    else:
        print("Please make a proper selection")
    choices()

if __name__ == "__main__":
    check_for_location()
    choices()
