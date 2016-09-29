# Developer Info

## Project structure

### main.py

This is where the program is started from. It handles reading the configuration, Slack I/O, and the main loop. 
It loads project global types and functions from common.py, then imports from weather.py, then launches the Slack client.

### common.py

This is where global types (those used by main.py and weather.py) are defined, including the Command class and its parser.
This is also where the locations  are defined, and various variables for looking up dates, months, etc.

### weather.py

This is where the interface with OpenWeatherMap is. It defines functions for processing weather and time-related data,
as well as a function that takes a Command and handles all of the appropriate behaviour, returning a string with 
the correct message.

### chart.py

This is where the process for loading Clear Sky Forecast charts will be.

### setup.py

This is the initial setup script that creates `config.xml`, and checks that the program functions correctly.
This must be run before the program is run.

### tests.py

This is where unit testing will go.

## Adding to the functionality

### Adding locations

The locations are defined in common.py. Valid location codes are in `locations`.
Location codes are strings with the name of the location. They must be a single word,
due to the limitations of the Command parser. Their coordinates are stored in the dict
`location_ref`, so that `location_ref[location]` will return the coordinates as a comma
separated pair of ints in a string. Alternate names for each location are stored in
`location_short`.

