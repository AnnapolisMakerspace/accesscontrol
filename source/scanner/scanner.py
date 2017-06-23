

import signal
import time

import zmq.green as zmq
#import zmq

from pirc522 import RFID


rdr = RFID()
util = rdr.util()


#util.debug = True
util.debug = False


print("starting up, entering main loop...")


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
                print("ACCESS REQUEST: {}  --  (raw UID: {})"
                      .format("".join(map(str, uid)), uid))

                # stop crypto:
                util.deauth()
                
                #input("\n(press enter to continue.)\n\n")
                time.sleep(0.5)
                

except KeyboardInterrupt as e:
    print("cleaning up GPIO...")
    rdr.cleanup()
    print("done.")
    exit(0)
