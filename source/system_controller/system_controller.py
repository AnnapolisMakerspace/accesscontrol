
import logging
import json
import time
import argparse
import json
import zmq


def base_send_command(command, pub_socket):
    command = {"command": command}
    serial_command = json.dumps(command)
    logger.info("publishing command: {0}".format(serial_command))    
    pub_socket.send(serial_command.encode())
    



if __name__ == '__main__':
    description = "testing req/rep"
    
    parser = argparse.ArgumentParser(usage=None, description=description)

    parser.add_argument("--relay_controller", type=str,
                        default="tcp://127.0.0.1:5555")

    parser.add_argument("--door_scanner", type=str,
                        default="tcp://127.0.0.1:5556")

    parser.add_argument("--door_button", type=str,
                        default="tcp://127.0.0.1:5557")

    parser.add_argument("--user_data_file", type=str)
                        
    
    
    args = parser.parse_args()

    context = zmq.Context()
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info("starting up...")

    #  Socket to talk to server
    logger.info("setting up sockets...\n\n")
    relay_sock = context.socket(zmq.REQ)
    relay_sock.connect(args.relay_controller)

    scanner_sock = context.socket(zmq.SUB)
    scanner_sock.setsockopt_string(zmq.SUBSCRIBE, "")
    scanner_sock.connect(args.door_scanner)

    button_sock = context.socket(zmq.SUB)
    button_sock.setsockopt_string(zmq.SUBSCRIBE, "")
    button_sock.connect(args.door_button)

    user_rfids = []
    logger.info("using file: {}".format(args.user_data_file))
    with open(args.user_data_file) as f:
        for l in f:
            line = json.loads(l)
            if line.get("rfid"):
                user_rfids.append(line["rfid"])
                
    #logger.info("user rfids: {}".format(user_rfids))
    
    while True:

        raw_mess = scanner_sock.recv().decode()
        logger.info("received scan: {}".format(raw_mess))
        
        mess = json.loads(raw_mess)
        
        if mess.get("rfid") in user_rfids:
            ################################
            # close relay:
            request = {"seconds": 1}
            serial_request = json.dumps(request)
            logger.info("sending REQ: {0}".format(serial_request))
            relay_sock.send(serial_request.encode())
            raw_message = relay_sock.recv().decode()
            logger.info("\nReceived REP: {0}".format(raw_message))


        
        
