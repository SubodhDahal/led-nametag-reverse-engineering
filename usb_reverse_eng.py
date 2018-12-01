import argparse

import usb.core
import usb

import char_to_pixels

dev = usb.core.find(idVendor=0x0416, idProduct=0x5020)

if dev is None:
    raise ValueError('Device not found')

if dev.is_kernel_driver_active(0):
    reattach = True
    dev.detach_kernel_driver(0)

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

# get the BULK OUT descriptor
epo = usb.util.find_descriptor(
    intf,
    # match our first out endpoint
    custom_match= \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_OUT)

assert epo is not None

def initialize_device (mode='left', speed=3, text_length=1, flash=0, lamp=0):
    speeds = {
        1: 0x00,
        2: 0x10,
        3: 0x20,
        4: 0x30,
        5: 0x40,
        6: 0x50,
        7: 0x60,
        8: 0x70,
    }

    modes = {
        'left': 0x00,
        'right': 0x01,
        'up': 0x02,
        'down': 0x03,
        'centered': 0x04,
        'animate': 0x05,
        'piling': 0x06,
        'split': 0x07,
        'laser': 0x08
    }

    speed_and_mode = speeds[speed] | modes[mode]
    text_length = text_length

    initialization_code = [0x77, 0x61, 0x6e, 0x67, 0x00, 0x00, flash, lamp, speed_and_mode, 0x30, 0x36, 0x30, 0x30, 0x30, 0x35, 0x30, 0x00, text_length, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x14, 0x0c, 0x01, 0x0c, 0x17, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

    epo.write(initialization_code)

def write_text (text, mode, speed, flash, lamp):
    text_length = len(text)

    initialize_device(mode, speed, text_length=text_length, flash=flash, lamp=lamp)

    data = char_to_pixels.get_block_values(text)

    epo.write(data)

    print('Wrote text to LEDs')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Write text to LED nametag')

    parser.add_argument("text")
    parser.add_argument("--mode")
    parser.add_argument("--speed")
    parser.add_argument("--flash")
    parser.add_argument("--lamp")
    args = parser.parse_args()

    mode = args.mode or 'centered'
    speed = int(args.speed) if args.speed else 4
    flash = int(args.flash) if args.flash else 0x00
    lamp = int(args.lamp) if args.lamp else 0x00

    write_text(args.text, mode=mode, speed=speed, flash=flash, lamp=lamp)
