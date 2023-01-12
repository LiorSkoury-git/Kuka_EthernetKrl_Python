from pynput.keyboard import Listener
from client import EkiClient,constructXML,constructWaitXML

def on_press(key):  # The function that's called when a key is pressed
    #print ("Key pressed: {0}".format(key))
    pass

def on_release(key):  # The function that's called when a key is released
    
    global keys
    global eki_client

    print (key)
    if hasattr(key, 'char'):  # Write the character pressed if available
        if key.char.upper() in keys: # Check if the pressed key is in the keys list
            action = constructXML(key.char.upper()) # construct the action xml message
            res = eki_client.send_data(action) # send the action xml message and get a response
            print (res) 
            wait = constructWaitXML() #construct a wait xml message 
            res = eki_client.send_data(wait) #send a wait xml message and wait for a 'done' feedback
            print (res) # print the result of the action

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

    #define the keys to read for actions
    keys = ['A','D','W','X','U','J','Q']

    #create a keyboard listener that will trigger the eki_client send method
    with Listener(on_press=on_press, on_release=on_release) as listener:  # Create an instance of Listener
        listener.join()  # Join the listener thread to the main thread to keep waiting for keys
    
    eki_client.close()
