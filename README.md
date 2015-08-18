# IoT Apps
Connecting a Raspberry Pi 2 with Grove sensors to a Google Sheet through Temboo

Google Sheet with dashboard and sensor data: https://docs.google.com/spreadsheets/d/11WF-G47xkEBf5lIw16d9nWxNcBcUJdirGU-gg56f5Eo/edit?usp=sharing 

## How it was done

0. Prepare the SD card with Raspbian:
https://learn.adafruit.com/adafruit-raspberry-pi-lesson-1-preparing-and-sd-card-for-your-raspberry-pi  I used the command:
sudo ./install 2015-05-05-raspbian-wheezy.img 

0. Configure the Pi:
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-2-first-time-configuration?view=all

0. Set up the network:
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-3-network-setup?view=all

0. Optionally, use a console cable:
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-5-using-a-console-cable?view=all

0. Set up SSH:
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-6-using-ssh?view=all

0. Set up VNC:
https://learn.adafruit.com/adafruit-raspberry-pi-lesson-7-remote-control-with-vnc?view=all

0. Set up GrovePi: 
http://www.dexterindustries.com/GrovePi/get-started-with-the-grovepi/setting-software/

0. Connect the sensors/actuators to the following ports:
```
A0: Light sensor
A1: Temperature sensor
A2: Loudness sensor
D3: Button
D4: LED
D8: Buzzer
I2C-1: RGB LCD Backlight

Edit cd ~/GrovePi/Software/Python/grove_temperature_sensor.py
Change “sensor = 0” to “sensor = 1"

Edit cd ~/GrovePi/Software/Python/grove_loudness_sensor.py
Change "loudness_sensor = 0” to "loudness_sensor = 2"
Change "led = 5" to "led = 4"

Check that the sensors and actuators are working:

cd ~/GrovePi/Software/Python
python grove_led_blink.py 
python grove_buzzer.py
python grove_button.py 
python grove_light_sensor.py 
python grove_temperature_sensor.py 
python grove_sound_sensor.py 

cd ~/GrovePi/Software/Python/grove_rgb_lcd
python example.py 
python example2.py 
```
0. Create a Temboo account and install the Python SDK:
http://support.temboo.com/entries/21388458-Using-the-Python-SDK

0. Create a Google App account and get the credentials:
https://temboo.com/library/Library/Google/Spreadsheets/

0. Create a new profile for adding new rows to the above Google Sheet:
https://temboo.com/library/Library/Google/Spreadsheets/AddListRows/

0. Run send_loop.sh, which calls send_sensor_data.py to get the sensor data and send to Google Sheets via Temboo

TODO: Control the actuators remotely via a local Python web server and ngrok:

http://www.instructables.com/id/Python-Web-Server-for-your-Raspberry-Pi/?ALLSTEPS

https://learn.adafruit.com/monitor-your-home-with-the-raspberry-pi-b-plus?view=all

https://ngrok.com/docs#expose
