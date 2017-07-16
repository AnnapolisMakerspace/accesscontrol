
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

    parser.add_argument("--relay_controller", type=str)

    parser.add_argument("--door_scanner", type=str)

    parser.add_argument("--door_button", type=str)

    # this "user data file" should NOT be passed in here.
    # the system_controller module should be
    # requesting/querying the user_data_service for user
    # information.  This works for now because we only have
    # a single dimension identifying users (ie, the UUID of
    # an rfid tag)
    parser.add_argument("--user_data_file", type=str)
                        
    args = parser.parse_args()

    ctx = zmq.Context()
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info("starting up...")

    #  Socket to talk to server
    logger.info("setting up sockets...\n\n")
    relay_sock = ctx.socket(zmq.REQ)
    relay_sock.connect(args.relay_controller)

    scanner_sock = ctx.socket(zmq.SUB)
    scanner_sock.setsockopt_string(zmq.SUBSCRIBE, "")
    scanner_sock.setsockopt(zmq.RCVHWM, 0)
    scanner_sock.connect(args.door_scanner)

    button_sock = ctx.socket(zmq.SUB)
    button_sock.setsockopt_string(zmq.SUBSCRIBE, "")
    button_sock.setsockopt(zmq.RCVHWM, 0)
    button_sock.connect(args.door_button)


    # this should be req/rep from the user_data service:
    # (due to time constraints we're doing it this way for now)
    user_rfids = []
    logger.info("using file: {}".format(args.user_data_file))
    with open(args.user_data_file) as f:
        for l in f:
            line = json.loads(l)
            if line.get("rfid"):
                user_rfids.append(line["rfid"])
                
    logger.info("user rfids: {}".format(user_rfids))
    
    while True:

        raw_mess = scanner_sock.recv().decode()
        logger.info("received scan: {}".format(raw_mess))
        
        mess = json.loads(raw_mess)
        
        if mess.get("rfid") in user_rfids:

            logger.info("rfid: {} in users, activating relay"
                        .format(mess.get("rfid")))
            
            ################################
            # close relay for 2 seconds:
            # (TODO: use ~button~ here)
            request = {"seconds": 2}
            serial_request = json.dumps(request)
            logger.info("sending REQ to door relay: {0}"
                        .format(serial_request))
            relay_sock.send(serial_request.encode())
            raw_message = relay_sock.recv().decode()
            logger.info("received REP from door relay: {0}"
                        .format(raw_message))


        
        
