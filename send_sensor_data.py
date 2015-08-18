#!/usr/bin/env python
#
# GrovePi Example for using the Grove Temperature Sensor (http://www.seeedstudio.com/wiki/Grove_-_Temperature_Sensor)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2015  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
# NOTE:
#   The sensor uses a thermistor to detect ambient temperature.
#   The resistance of a thermistor will increase when the ambient temperature decreases.
#
#   There are 3 revisions 1.0, 1.1 and 1.2, each using a different model thermistor.
#   Each thermistor datasheet specifies a unique Nominal B-Constant which is used in the calculation forumla.
#
#   The second argument in the grovepi.temp() method defines which board version you have connected.
#   Defaults to '1.0'. eg.
#       temp = grovepi.temp(sensor)        # B value = 3975
#       temp = grovepi.temp(sensor,'1.1')  # B value = 4250
#       temp = grovepi.temp(sensor,'1.2')  # B value = 4250

import time
import grovepi
import datetime
from temboo.Library.Google.Spreadsheets import AddListRows
from temboo.core.session import TembooSession

# Connect the Grove Light Sensor to analog port A0
# SIG,NC,VCC,GND
light_sensor = 0
grovepi.pinMode(light_sensor, "INPUT")

# Connect the Grove Temperature Sensor to analog port A1
# SIG,NC,VCC,GND
temp_sensor = 1

# Connect the Grove Sound Sensor to analog port A2
# SIG,NC,VCC,GND
sound_sensor = 2

while True:
    try:
        # Get the current timestamp.
        now = datetime.datetime.now()
        timestamp = str(now)

        # Get sensor values.
        lightLevel = grovepi.analogRead(light_sensor)
        temp = grovepi.temp(temp_sensor, '1.1')
        soundLevel = grovepi.analogRead(sound_sensor)
        # TODO: Get this from a humidity sensor.
        humidity = "75"

        # Show the sensor values for debugging.
        print ("timestamp=", timestamp)
        print ("lightLevel=", lightLevel)
        print ("temp=", temp)
        print ("soundLevel=", soundLevel)

        # Send the sensor data to the Google Spreadsheet through Temboo.
        # Create a session with your Temboo account details
        session = TembooSession(“USERID”, “APPNAME”, “APPKEY”)

        # Instantiate the Choreo
        addListRowsChoreo = AddListRows(session)

        # Get an InputSet object for the Choreo
        addListRowsInputs = addListRowsChoreo.new_input_set()

        # Set credential to use for execution
        addListRowsInputs.set_credential('SensorData')

        # Set the data to be added
        addListRowsInputs.set_RowsetXML("""
        <rowset>
        <row>
        <Timestamp>{0}</Timestamp>
        <Temperature>{1}</Temperature>
        <Humidity>{2}</Humidity>
        <LightLevel>{3}</LightLevel>
        <SoundLevel>{4}</SoundLevel>
        </row>
        </rowset>
        """.format(timestamp, temp, humidity, lightLevel, soundLevel))

        # Execute the Choreo
        addListRowsResults = addListRowsChoreo.execute_with_results(addListRowsInputs)

        # Print the Choreo outputs
        print("Response: " + addListRowsResults.get_Response())
        print("NewAccessToken: " + addListRowsResults.get_NewAccessToken())

        # TODO: Delay and continue
        break

        time.sleep(.5)

    except KeyboardInterrupt:
        break
    except IOError:
        print ("Error")
