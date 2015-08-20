#!/bin/bash
##  Change to the directory containing our scripts.
cd /home/pi/GrovePi/Software/Python/

##  Start the TCP tunnel for SSH.
./ngrok tcp --log "stdout" -config=/home/pi/.ngrok2/ngrok.yml --remote-addr=???.tcp.ngrok.io:??? 22 &

##  Start the Python web server.
sudo python server.py &

##  Wait a while for the web server to start up before starting the HTTP tunnel.
sleep 10

##  Start the HTTP tunnel for remote web access to our web server.
./ngrok http --log "stdout" -config=/home/pi/.ngrok2/ngrok.yml --subdomain=??? 80 &

##  Loop forever, sending sensor data.
for (( ; ; ))
do
	##  Send sensor data.
	python send_sensor_data.py
	##  Wait 1 minute and send sensor data again.
	sleep 60
done
