ITECH EthernetKrl comunication workshop
=======================================

This repo was created for an ITECH workshop about the KUKA robot's communication using EthernetKrl.
The EthernetKrl version used for this workshop is 3.2 for KSS 8.7

To run the code, first follow the steps:

1 - create a virtual environment in your desired location

2 - install python and the requirements libraries with "pip install -r requirements.txt"

3 - Make sure the EthernetKrl package is available in your robot

4 - place the file Config -> ITECH.xml in this folder on your robot controller:
        C:\KRC\ROBOTER\Config\User\Common\EthernetKRL

5 - place both files (.dat and .src) from the KRL folder on your program folder on your controller:
        ...\Repositories\YourRobotName\KRC\R1\Program

6 - select the 'ethernetkrl_workshop.src' program and start running it until you get the message "waiting for flag[1]."

7 - run the virtual environment

8 - run app.py 

9 - open rhino and load the Example.gh file

10 - create the client using the createClient hops function

11 - connect to the server using the Connect hops function

12 - you can start controlling the robot by using the sendKey and sendFrame hops functions