import platform
import re
from device import Device


# Platform identification constants.
UNKNOWN          = 0
RASPBERRY_PI     = 1
BEAGLEBONE_BLACK = 2
MINNOWBOARD      = 3


def get_i2c_device(address, busnum=None, i2c_interface=None, **kwargs):
    """Return an I2C device for the specified address and on the specified bus.
    If busnum isn't specified, the default I2C bus for the platform will attempt
    to be detected.
    """
    if busnum is None:
        busnum = get_default_bus()
    return Device(address, busnum, i2c_interface, **kwargs)


def get_default_bus():
    """Return the default bus number based on the device platform.  For a
    Raspberry Pi either bus 0 or 1 (based on the Pi revision) will be returned.
    For a Beaglebone Black the first user accessible bus, 1, will be returned.
    """
    plat = platform_detect()
    if plat == RASPBERRY_PI:
        if pi_revision() == 1:
            # Revision 1 Pi uses I2C bus 0.
            return 0
        else:
            # Revision 2 Pi uses I2C bus 1.
            return 1
    elif plat == BEAGLEBONE_BLACK:
        # Beaglebone Black has multiple I2C buses, default to 1 (P9_19 and P9_20).
        return 1
    else:
        raise RuntimeError('Could not determine default I2C bus for platform.')

def platform_detect():
    """Detect if running on the Raspberry Pi or Beaglebone Black and return the
    platform type.  Will return RASPBERRY_PI, BEAGLEBONE_BLACK, or UNKNOWN."""
    # Handle Raspberry Pi
    pi = pi_version()
    if pi is not None:
        return RASPBERRY_PI

    # Handle Beaglebone Black
    # TODO: Check the Beaglebone Black /proc/cpuinfo value instead of reading
    # the platform.
    plat = platform.platform()
    if plat.lower().find('armv7l-with-debian') > -1:
        return BEAGLEBONE_BLACK
    elif plat.lower().find('armv7l-with-ubuntu') > -1:
        return BEAGLEBONE_BLACK
    elif plat.lower().find('armv7l-with-glibc2.4') > -1:
        return BEAGLEBONE_BLACK
        
    # Handle Minnowboard
    # Assumption is that mraa is installed
    try: 
        import mraa 
        if mraa.getPlatformName()=='MinnowBoard MAX':
            return MINNOWBOARD
    except ImportError:
        pass
    
    # Couldn't figure out the platform, just return unknown.
    return UNKNOWN

def pi_version():
    """Detect the version of the Raspberry Pi.  Returns either 1, 2 or
    None depending on if it's a Raspberry Pi 1 (model A, B, A+, B+),
    Raspberry Pi 2 (model B+), or not a Raspberry Pi.
    """
    # Check /proc/cpuinfo for the Hardware field value.
    # 2708 is pi 1
    # 2709 is pi 2
    # Anything else is not a pi.
    with open('/proc/cpuinfo', 'r') as infile:
        cpuinfo = infile.read()
    # Match a line like 'Hardware   : BCM2709'
    match = re.search('^Hardware\s+:\s+(\w+)$', cpuinfo,
                      flags=re.MULTILINE | re.IGNORECASE)
    if not match:
        # Couldn't find the hardware, assume it isn't a pi.
        return None
    if match.group(1) == 'BCM2708':
        # Pi 1
        return 1
    elif match.group(1) == 'BCM2709':
        # Pi 2
        return 2
    else:
        # Something else, not a pi.
        return None

def pi_revision():
    """Detect the revision number of a Raspberry Pi, useful for changing
    functionality like default I2C bus based on revision."""
    # Revision list available at: http://elinux.org/RPi_HardwareHistory#Board_Revision_History
    with open('/proc/cpuinfo', 'r') as infile:
        for line in infile:
            # Match a line of the form "Revision : 0002" while ignoring extra
            # info in front of the revsion (like 1000 when the Pi was over-volted).
            match = re.match('Revision\s+:\s+.*(\w{4})$', line, flags=re.IGNORECASE)
            if match and match.group(1) in ['0000', '0002', '0003']:
                # Return revision 1 if revision ends with 0000, 0002 or 0003.
                return 1
            elif match:
                # Assume revision 2 if revision ends with any other 4 chars.
                return 2
        # Couldn't find the revision, throw an exception.
        raise RuntimeError('Could not determine Raspberry Pi revision.')

