import time

import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
_ = socket.bind("tcp://*:8081")


while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    socket.send(b"World")
