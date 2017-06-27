
import logging
import signal
import time
import argparse

#import zmq.green as zmq
import zmq

from pirc522 import RFID


rdr = RFID()
util = rdr.util()


#util.debug = True
util.debug = False


if __name__ == '__main__':

    description = "Access Control Door Scanner"    
    parser = argparse.ArgumentParser(usage=None, description=description)

    parser.add_argument("--pub_endpoint", type=str,
                        default="tcp://127.0.0.1:5556")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)    
    logger.info("parsed args, starting up...")
    
    context = zmq.Context()

    #  Socket to talk to server
    logger.info("setting up PUB socket on : {}".format(args.pub_endpoint))
    socket = context.socket(zmq.PUB)
    socket.bind(args.pub_endpoint)

    try:    
        while True:
            #print("\n\nstarted, waiting for tag...")
            # Wait for tag
            rdr.wait_for_tag()

            #print("read tag, checking for error...")
            # Request tag
            (error, data) = rdr.request()

            if error:
                #print("e", sep="", end="")
                continue

            elif not error:
                #print("")
                #print("\nDetected!")

                #print("running anti-collision...")
                (collision_error, uid) = rdr.anticoll()

                if not collision_error:
                    # Print UID
                    logger.info("ACCESS REQUEST: {}  --  (raw UID: {})"
                                .format("".join(map(str, uid)), uid))

                    # stop crypto:
                    util.deauth()

                    #input("\n(press enter to continue.)\n\n")
                    time.sleep(0.5)


    except Exception as e:
        logger.error(e)
        logger.error("cleaning up GPIO...")
        rdr.cleanup()
        raise
