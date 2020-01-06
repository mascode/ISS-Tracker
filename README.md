# ISS-Tracker

A simple program to track the current location of the ISS, written in Python 3.7. This project would not be possible without the API which is generously provided by the [Open Notify](http://open-notify.org/) project. Source code for the API is available [here](https://github.com/open-notify/Open-Notify-API). A big thank you to the creator for making this project possible. 

### Usage:

Navigate to the directory where you downloaded the program and simply run 

```python
python tracker.py # to track ISS' location
python passover.py # to check the next fly-over times for your location

```

Location is displayed as longitude and latitude. Your location is stored in a database that is generated at first run. Coordinates obtained from tracking are also saved to the database. Tracker also displays who is on board. 

### Sample Output:

tracker.py

```
There are currently 6 people on board the ISS. They are...
Astronaut Christina Koch who is on board the ISS
Astronaut Alexander Skvortsov who is on board the ISS
Astronaut Luca Parmitano who is on board the ISS
Astronaut Andrew Morgan who is on board the ISS
Astronaut Oleg Skripochka who is on board the ISS
Astronaut Jessica Meir who is on board the ISS

Starting tracking, press 'Ctrl + C' to stop...

The ISS is currently at Latitude: -16.8173 and Longitude: 148.3843 Timestamp: Mon Jan 6 03:03:42 2020
Saving to database...
Done
The ISS is currently at Latitude: -16.5709 and Longitude: 148.5819 Timestamp: Mon Jan 6 03:03:48 2020
Saving to database...
Done
The ISS is currently at Latitude: -16.3244 and Longitude: 148.7790 Timestamp: Mon Jan 6 03:03:53 2020
Saving to database...
Done
The ISS is currently at Latitude: -16.0776 and Longitude: 148.9756 Timestamp: Mon Jan 6 03:03:58 2020
Saving to database...
Done
The ISS is currently at Latitude: -15.8306 and Longitude: 149.1716 Timestamp: Mon Jan 6 03:04:03 2020
Saving to database...
Done
The ISS is currently at Latitude: -15.5834 and Longitude: 149.3671 Timestamp: Mon Jan 6 03:04:08 2020
Saving to database...
Done
```

passover.py

```
Location saved to database
The next time the ISS will pass over your location, in a 7 hour period, is...
2020-01-06 07:54:07
2020-01-06 09:31:00
2020-01-06 11:09:49
2020-01-06 12:48:06
What would you like to do next?
1. Clear the database and save a new location
2. Check another location (Without saving to the dabase)
3. Exit the program
```
