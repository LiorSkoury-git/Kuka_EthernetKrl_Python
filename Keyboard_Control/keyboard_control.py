import sys
import os

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
sys.path.append(parent)

from pynput.keyboard import Listener
from client import EkiClient,constructXMLTEXT,constructWaitXML


def on_press(key):  # The function that's called when a key is pressed
    #print ("Key pressed: {0}".format(key))
    pass

def on_release(key):  # The function that's called when a key is released
    
    global keys
    global eki_client

    if hasattr(key, 'char'):  # Write the character pressed if available
        if key.char.upper() in keys: # Check if the pressed key is in the keys list
            d = {"Action":0,"Key":key.char.upper()}
            action = constructXMLTEXT(d) # construct the action xml message
            res = eki_client.send_data(action) # send the action xml message and get a response
            print (res) 
            wait = constructWaitXML() #construct a wait xml message 
            res = eki_client.send_data(wait) #send a wait xml message and wait for a 'done' feedback
            print (res) # print the result of the action

        if key.char.upper() == "I": #if the input is i you can insert xyzabc coordinates
            frame = input("coords of your frame: (x,y,z,a,b,c)")
            frame = [float(x) for x in frame.split(',')]
            frameDict= {'X':frame[0], 'Y':frame[1], 'Z':frame[2], 'A':frame[3],'B':frame[4], 'C':frame[5]}
            action = constructXMLTEXT({"Action":1})
            action = constructXMLTEXT({"Frame":frameDict},type="tag",root=action)
            #res = eki_client.send_data(action) # send the action xml message and get a response
            #print (res) 
            #wait = constructWaitXML() #construct a wait xml message 
            #res = eki_client.send_data(wait) #send a wait xml message and wait for a 'done' feedback
            #print (res) # print the result of the action
            print (action.printXML())

    if str(key) == "Key.esc":
        # Stop listener
        return False

if __name__ == "__main__":

    # create the eki_client
    ip = '192.168.2.1'
    port = 54600
    eki_client = EkiClient(ip, port)

    #connect to the eki_client
    eki_client.connect()

    #define the keys to read for actionsaADWXJUQ
    keys = ['A','D','W','X','U','J','Q']

    #create a keyboard listener that will trigger the eki_client send method
    with Listener(on_press=on_press, on_release=on_release) as listener:  # Create an instance of Listener
        listener.join()  # Join the listener thread to the main thread to keep waiting for keys
    
    eki_client.close()
