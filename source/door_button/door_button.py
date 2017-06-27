

import logging
import json
import time
import argparse
from functools import partial

import RPi.GPIO as gpio
import zmq


def setup_gpio(gpio_bcm_pin_number):
    gpio.setmode(gpio.BCM)
    gpio.setup(gpio_bcm_pin_number, gpio.IN, pull_up_down=gpio.PUD_UP)


def base_publish_event(event, pub_socket):
    event = {"event": event}
    serial_event = json.dumps(event)
    logger.info("publishing event: {0}".format(serial_event))    
    pub_socket.send(serial_event.encode())
    

if __name__ == '__main__':
    description = ""
    
    parser = argparse.ArgumentParser(usage=None, description=description)
    parser.add_argument("--pub_endpoint", type=str,
                        default="tcp://127.0.0.1:5557",
                        help=("end point this module will bind to, and "
                              "publish/announce button presses"))

    parser.add_argument("--button_gpio_pin", type=int,
                        default=18,
                        help=("GPIO pin to be driven by "
                              "module (BCM pin numbering scheme)"))

    args = parser.parse_args()
    
    # Bind to the service endpoint:
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind(args.pub_endpoint)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info("starting up.  using GPIO pio: {}"
                .format(args.button_gpio_pin))
    publish_event = partial(base_publish_event,
                            pub_socket=socket)
    while True:
        logger.debug('setting up GPIO on pin: {}...'
                     .format(args.button_gpio_pin))
        setup_gpio(args.button_gpio_pin)
        try:

            current_state = True
            
            while True:
                input_state = gpio.input(args.button_gpio_pin)
                
                if input_state == current_state:
                    time.sleep(0.05)
                    continue
                
                elif input_state == True:
                    logger.info('Button Up')
                    current_state = input_state
                    publish_event("ButtonUp")
                    continue
                    
                elif input_state == False:
                    logger.info('Button Down')                    
                    current_state = input_state
                    publish_event("ButtonDown")
                    continue                    
                

        # need to handle graceful shutdown in here.                
        # except <Graceful Shutdown Event/Exception> as e:
        #     gpio.cleanup()
        #     break
        except KeyboardInterrupt:
            logger.info("shutting down...")
            gpio.cleanup()
            break
        
        except Exception as e:
            logger.error("error encountered while handling request")
            logger.error(e)
            gpio.cleanup()
            socket.send_string(json.dumps({
                "status": "ERROR",
            }))

