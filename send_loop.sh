#!/bin/bash
for (( ; ; ))
do
	##  Send sensor data.
	python send_sensor_data.py
	##  Wait 1 minute and send sensor data again.
	sleep 60
done
