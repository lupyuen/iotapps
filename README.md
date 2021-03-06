# IoT Apps
## Connecting a Raspberry Pi 2 with Grove sensors and actuators to a Google Sheet through Temboo

I programmed a Raspberry Pi 2 with Temperature, Light, Sound and Button Sensors to update a Google Sheet spreadsheet with the sensor data every minute.  I also programmed the Raspberry Pi 2 to allow remote control of the LED, Buzzer and LCD Screen from a web browser over the internet.

The Google Sheet includes a realtime dashboard for visualising the sensor data in real time.  The spreadsheet contains rules for triggering alerts (i.e. temperature too high).  I will be notified of the alerts via SMS or an automated voice call using the Hoiio telephony service.

I used Grove sensors and actuators, connected to the GrovePi+ shield on a Raspberry Pi 2.

Here's the Google Sheet with dashboard (see tab "Dashboard") and sensor data (see tab "Data"): https://docs.google.com/spreadsheets/d/11WF-G47xkEBf5lIw16d9nWxNcBcUJdirGU-gg56f5Eo/edit?usp=sharing 

Photo of the Raspberry Pi 2 with Grove sensors and actuators: https://github.com/lupyuen/iotapps/blob/master/raspberry_pi_setup.jpg

## How it was done

0. You'll need the following items:
    - http://www.seeedstudio.com/depot/Raspberry-Pi-2-Model-B-w-ARMv7-Quad-Core-1GB-RAM-p-2289.html
    - http://www.seeedstudio.com/depot/Quick-Starter-Kit-for-Raspberry-Pi-2-Model-B-p-2364.html
    - http://www.seeedstudio.com/depot/GrovePi-p-2241.html
    - http://www.seeedstudio.com/depot/Grove-Starter-Kit-for-Arduino-p-1855.html

0. Prepare the SD card with Raspbian:
https://learn.adafruit.com/adafruit-raspberry-pi-lesson-1-preparing-and-sd-card-for-your-raspberry-pi  

    I used the command: sudo ./install 2015-05-05-raspbian-wheezy.img 

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

0. Copy /home/pi/GrovePi/Software/Python/grove_rgb_lcd/grove_rgb_lcd.py to /home/pi/GrovePi/Software/Python/

0. Download the Linux/ARM version of ngrok from https://ngrok.com/download and copy to /home/pi/GrovePi/Software/Python/

0. Grant execute access to ngrok:
    ```
    chmod +x /home/pi/GrovePi/Software/Python/ngrok
    ```
    
0. Download the following files to /home/pi/GrovePi/Software/Python/:
    - https://github.com/lupyuen/iotapps/blob/master/send_loop.sh
    - https://github.com/lupyuen/iotapps/blob/master/send_button_data.py
    - https://github.com/lupyuen/iotapps/blob/master/send_sensor_data.py
    - https://github.com/lupyuen/iotapps/blob/master/server.py

0. Connect the sensors/actuators to the following ports ([photo here](https://github.com/lupyuen/iotapps/blob/master/raspberry_pi_setup.jpg)):
    - A0: Light sensor
    - A1: Temperature sensor
    - A2: Loudness sensor
    - D3: Button
    - D4: LED
    - D8: Buzzer
    - I2C-1: RGB LCD Backlight

0. Edit /home/pi/GrovePi/Software/Python/grove_temperature_sensor.py
    - Change “sensor = 0” to “sensor = 1"
    
0. Edit /home/pi/GrovePi/Software/Python/grove_loudness_sensor.py
    - Change "loudness_sensor = 0” to "loudness_sensor = 2"
    - Change "led = 5" to "led = 4"
    
0. Check that the sensors and actuators are working:
    ```
    cd /home/pi/GrovePi/Software/Python
    python grove_led_blink.py 
    python grove_buzzer.py
    python grove_button.py 
    python grove_light_sensor.py 
    python grove_temperature_sensor.py 
    python grove_sound_sensor.py 
    
    cd /home/pi/GrovePi/Software/Python/grove_rgb_lcd
    python example.py 
    python example2.py 
    ```
0. Create a Temboo account and download the Python SDK into /home/pi/GrovePi/Software/Python/temboo:
http://support.temboo.com/entries/21388458-Using-the-Python-SDK

0. Create a Google App account and get the credentials (Client ID, Client Secret, Refresh Token, Access Token):
https://temboo.com/library/Library/Google/Spreadsheets/

0. Create a new Temboo profile for adding new rows to the above Google Sheet, specifying the Google credentials (Client ID, Client Secret, Refresh Token, Access Token), spreadsheet key, worksheet ID:
https://temboo.com/library/Library/Google/Spreadsheets/AddListRows/

0. Edit [send_loop.sh](https://github.com/lupyuen/iotapps/blob/master/send_loop.sh),  [send_sensor_data.py](https://github.com/lupyuen/iotapps/blob/master/send_sensor_data.py), [send_button_data.py](https://github.com/lupyuen/iotapps/blob/master/send_button_data.py) and update the ngrok and Temboo settings accordingly

0. Run [send_loop.sh](https://github.com/lupyuen/iotapps/blob/master/send_loop.sh), which calls [send_sensor_data.py](https://github.com/lupyuen/iotapps/blob/master/send_sensor_data.py) to get the sensor data and send to Google Sheets via Temboo

0. [send_loop.sh](https://github.com/lupyuen/iotapps/blob/master/send_loop.sh) calls [send_button_data.py](https://github.com/lupyuen/iotapps/blob/master/send_button_data.py) to poll the button state repeatedly and update Google Sheets when the button is pressed or released

0. [send_loop.sh](https://github.com/lupyuen/iotapps/blob/master/send_loop.sh) also starts [server.py](https://github.com/lupyuen/iotapps/blob/master/server.py), a local Python web server that controls actuators: LED, LCD screen, buzzer

0. To control the actuators remotely via a web browser, [send_loop.sh](https://github.com/lupyuen/iotapps/blob/master/send_loop.sh) uses ngrok to redirect internet requests to the local Python web server ([server.py](https://github.com/lupyuen/iotapps/blob/master/server.py)):
    ```
    ./ngrok http --log "stdout" -config=/home/pi/.ngrok2/ngrok.yml --subdomain=YOURSUBDOMAIN 80 &
    ```
0. The actuators may be controlled remotely as follows:
    - Switch on LED:	http://luppypi.ngrok.io/led_on
    - Switch off LED:	http://luppypi.ngrok.io/led_off
    - Buzz the buzzer:	http://luppypi.ngrok.io/buzz
    - Show a message on the LCD screen:	http://luppypi.ngrok.io/lcd/hello%20from%20github

0. [send_loop.sh](https://github.com/lupyuen/iotapps/blob/master/send_loop.sh) uses ngrok to expose the Raspberry Pi's SSH port to the internet:
    ```
    ./ngrok tcp --log "stdout" -config=/home/pi/.ngrok2/ngrok.yml --remote-addr=YOURHOST.tcp.ngrok.io:YOURPORT 22 &
    ```
    So to connect to the Raspberry Pi via SSH from anywhere in the internet, you only need to use:
    ```
    ssh YOURHOST.tcp.ngrok.io -p YOURPORT -l pi
    ```
0. To start send_loop.sh automatically upon reboot, run
    ```
    sudo crontab -e
    ```
    and append the line
    ```
    @reboot /home/pi/GrovePi/Software/Python/send_loop.sh > /home/pi/send_loop.log &
    ```

0. To enable the crontab log, see http://raspberrypi.stackexchange.com/questions/3741/where-do-cron-error-message-go

0. For info, warning and error messages by send_loop.sh, see /home/pi/send_loop.log

0. Disable the graphical desktop shell to save power: http://ask.xmodulo.com/disable-desktop-gui-raspberry-pi.html

0. Remember to backup your Raspberry Pi SD card: http://computers.tutsplus.com/articles/how-to-clone-raspberry-pi-sd-cards-using-the-command-line-in-os-x--mac-59911

0. Alerts: I implemented Alerts using simple Google Sheet formulas.  If you click on the “Alert” heading in Column G, you’ll see a formula that checks whether the temperature is too hot (above 31 degrees) and if so, shows the message “Warning: Too hot!”.  The “Alerts” tab shows all rows with alerts.

0. Notifications: In the “Alerts” tab you can see that when there is an alert generated, the system will make an automated voice call (or SMS).  This is done with a Google App Script connected to Hoiio, the SMS and Voice Telephony service.  Pressing the button sensor also triggers a voice call or SMS. Hoiio offers a free trial with limited messages.
