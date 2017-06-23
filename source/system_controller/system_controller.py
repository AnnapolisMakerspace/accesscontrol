

import argparse
import json
import zmq


if __name__ == '__main__':
    description = "testing req/rep"
    
    parser = argparse.ArgumentParser(usage=None, description=description)

    parser.add_argument("--relay_controller", type=str,
                        default="tcp://127.0.0.1:5555")

    args = parser.parse_args()

    context = zmq.Context()

    #  Socket to talk to server
    print("Connecting to server...\n\n")
    socket = context.socket(zmq.REQ)
    socket.connect(args.req_endpoint)

    while True:
        raw_seconds = input("send command, activate for seconds: ")

        try:
            seconds = float(raw_seconds)
        except Exception as e:
            print("could not parse input: {}".format(e))
            seconds = None


        request = {"seconds": seconds}
        serial_request = json.dumps(request)
        print("sending REQ: \n{0}".format(serial_request))
               
        socket.send(serial_request.encode())
        raw_message = socket.recv().decode()
        
        print("\nReceived REP: \n{0}\n\n\n"
               .format(raw_message))

        
