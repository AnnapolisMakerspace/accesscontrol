

import signal
import time

#import zmq.green as zmq
#import zmq
from pirc522 import RFID


def octet_to_string(ot):
    return "0"*(3 - len(str(ot))) + str(ot)

rdr = RFID()
util = rdr.util()

# Set util debug to true - it will print what's going on
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
            (error, uid) = rdr.anticoll()

            if not error:
                # Print UID
                print("ACCESS REQUEST: {}  --  (raw UID: {})"
                      .format("".join(map(octet_to_string, uid)), uid))

                # Let's see what do we have in whole tag
                #print("setting tag in util...")
                #util.set_tag(uid)
                
                #print("calling auth()...")
                #util.auth(rdr.auth_b, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
                
                # Save authorization info (key B) to util.
                # It doesn't call RFID.card_auth(), that's called when needed
                #util.auth(rdr.auth_b, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])

                # Print contents of block 4 in format
                # "S1B0: [contents in decimal]".
                # RFID.card_auth() will be called now
                #util.read_out(4)

                # Print it again - now auth won't be called,
                # because it doesn't have to be
                #util.read_out(4)

                # Print contents of different block - S1B2 - RFID.card_auth()
                # will be called again
                #util.read_out(6)

                # We can change authorization info if you
                # have different key in other sector
                #util.auth(rdr.auth_a, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])

                # If you want to use methods from RFID itself,
                # you can use this for authorization
                # This will authorize for block 1 of sector 2 -> block 9
                # This is once more called only if it's not already
                # authorized for this block
                #util.do_auth(util.block_addr(2, 1))

                # Now we can do some "lower-level" stuff with block 9
                # rdr.write(9, [
                #     0x01, 0x23, 0x45, 0x67, 0x89, 0x98, 0x76, 0x54, 0x32, 0x10,
                #     0x69, 0x27, 0x46, 0x66, 0x66, 0x64
                # ])

                # We can rewrite specific bytes in block using this method.
                # None means "don't change this byte"
                # Note that this won't do authorization, because we've
                # already called do_auth for block 9
                #util.rewrite(9, [None, None, 0xAB, 0xCD, 0xEF])

                # This will write S2B1:
                # [0x01, 0x23, 0xAB, 0xCD, 0xEF, 0x98, 0x76......]
                # because we've rewritten third, fourth and fifth byte
                #util.read_out(9)

                # Let's see what do we have in whole tag
                #util.dump()

                # We must stop crypto
                util.deauth()
                
                #input("\n(press enter to continue.)\n\n")
                time.sleep(0.5)
                

except KeyboardInterrupt as e:
    print("cleaning up GPIO...")
    rdr.cleanup()
    print("done.")
    exit(0)
