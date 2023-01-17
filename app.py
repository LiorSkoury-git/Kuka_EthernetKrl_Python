from flask import Flask
import ghhops_server as hs
from client import EkiClient,constructXMLTEXT,constructWaitXML


# register hops app as middleware
app = Flask(__name__)
hops: hs.HopsFlask = hs.Hops(app)
sticky = None

#-- Point At component --#
@hops.component(
    "/sum",
    name="Sum",
    description="sum of numbers",
    inputs=[
        hs.HopsNumber("A", "A", "First Number"),
        hs.HopsNumber("B", "B", "Second Number")
    ],
    outputs=[
        hs.HopsNumber("Sum", "Sum", "Sum of the numbers")
    ]
)
def sum(a : float=0, b: float=0):
    return a+b

@hops.component(
    "/createClient",
    name="CreateClient",
    description="Create EKI Client",
    inputs=[
        hs.HopsString("IP","IP","IP of the EKI client"),
        hs.HopsString("PORT","PORT","Port of the EKI client")
    ],
    outputs=[
        hs.HopsString("Created","Created","Indicate if the client was created")
    ]
)
def createClient(ip: str, port: str):
    global sticky
    client = EkiClient(ip,int(port))
    sticky = client
    return sticky.ip


@hops.component(
    "/connectClient",
    name="connectClient",
    description="connect EKI Client to the EKI server",
    inputs=[
        hs.HopsBoolean("Connect","Connect","True to connect")
    ],
    outputs=[
        hs.HopsBoolean("Connected","Connected","Connected the EKI client to the EKI server")
    ]
)
def connectClient(connect:bool):
    global sticky
    if connect:
        connected = sticky.connect()
        return connected

    return False


@hops.component(
    "/sendKey",
    name="sendKey",
    description="sendKey to EKI Client",
    inputs=[
        hs.HopsString("Key","Key","Keyboard key to send to the robot")
    ],
    outputs=[
        hs.HopsString("XML","XML","XML structure of the key as string")
    ]
)
def sendKey(key:str):
    global sticky
    d = {"Action":0,"Key":key.upper()}
    action = constructXMLTEXT(d) # construct the action xml message
    #return str(action.serialize())
    res = sticky.send_data(action)
    wait = constructWaitXML() #construct a wait xml message 
    res = sticky.send_data(wait) #send a wait xml message and wait for a 'done' feedback
    #print (res) # print the result of the action

    return str(res)


@hops.component(
    "/sendFrame",
    name="sendFrame",
    description="sendFrame to EKI Client",
    inputs=[
        hs.HopsPoint("XYZ","XYZ","XYZ location of the frame"),
        hs.HopsVector("ABC","ABC","ABC Orientation of the frame"),
    ],
    outputs=[
        hs.HopsString("XML","XML","XML structure of the frame as string")
    ]
)
def sendFrame(xyz,abc):
    global sticky
    action = constructXMLTEXT({"Action":1})
    frameDict= {'X':xyz.X, 'Y':xyz.Y, 'Z':xyz.Z, 'A':abc.X,'B':abc.Y, 'C':abc.Z}
    action = constructXMLTEXT({"Frame":frameDict},type="tag",root=action)
    #return str(action.serialize())
    res = sticky.send_data(action)
    wait = constructWaitXML() #construct a wait xml message 
    res = sticky.send_data(wait) #send a wait xml message and wait for a 'done' feedback
    #print (res) # print the result of the action

    return str(res)


if __name__ == '__main__':
    # set debug=True
    app.run(debug=True)