import usb.core
import usb

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

print(intf)

# get the BULK OUT descriptor
epo = usb.util.find_descriptor(
    intf,
    # match our first out endpoint
    custom_match= \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_OUT)

assert epo is not None

# get the BULK IN descriptor
epi = usb.util.find_descriptor(
    intf,
    # match our first out endpoint
    custom_match= \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_IN)

assert epi is not None

def initialize_device (mode='rtl'):
    if mode == 'rtl':
        initialization_code = b'\x77\x61\x6e\x67\x00\x00\x00\x40\x30\x30\x36\x30\x30\x30\x35\x30\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x14\x0c\x01\x09\x35\x12\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    elif mode == 'animate':
        initialization_code = b'\x77\x61\x6e\x67\x00\x00\x00\x40\x35\x30\x36\x30\x30\x30\x35\x30\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x14\x0c\x01\x0c\x17\x20\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    epo.write(initialization_code)

initialize_device('animate')

data = b'\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

epo.write(data)
