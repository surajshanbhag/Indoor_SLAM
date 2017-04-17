from __future__ import division
import logging
import time
import math


# Registers/etc:
PCA9685_ADDRESS    = 0x40
MODE1              = 0x00
MODE2              = 0x01
SUBADR1            = 0x02
SUBADR2            = 0x03
SUBADR3            = 0x04
PRESCALE           = 0xFE
LED0_ON_L          = 0x06
LED0_ON_H          = 0x07
LED0_OFF_L         = 0x08
LED0_OFF_H         = 0x09
ALL_LED_ON_L       = 0xFA
ALL_LED_ON_H       = 0xFB
ALL_LED_OFF_L      = 0xFC
ALL_LED_OFF_H      = 0xFD

# Bits:
RESTART            = 0x80
SLEEP              = 0x10
ALLCALL            = 0x01
INVRT              = 0x10
OUTDRV             = 0x04


logger = logging.getLogger(__name__)


class PCA9685(object):
    """PCA9685 PWM LED/servo controller."""

    def __init__(self, address=PCA9685_ADDRESS, i2c=None, **kwargs):
        """Initialize the PCA9685."""
        # Setup I2C interface for the device.
        if i2c is None:
            import I2C as I2C
            i2c = I2C
        self._device = i2c.get_i2c_device(address, **kwargs)
        self.set_all_pwm(0, 0)
        self._device.write8(MODE2, OUTDRV)
        self._device.write8(MODE1, ALLCALL)
        time.sleep(0.005)  # wait for oscillator
        mode1 = self._device.readU8(MODE1)
        mode1 = mode1 & ~SLEEP  # wake up (reset sleep)
        self._device.write8(MODE1, mode1)
        time.sleep(0.005)  # wait for oscillator

    def set_pwm_freq(self, freq_hz):
        """Set the PWM frequency to the provided value in hertz."""
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq_hz)
        prescaleval -= 1.0
        logger.debug('Setting PWM frequency to {0} Hz'.format(freq_hz))
        logger.debug('Estimated pre-scale: {0}'.format(prescaleval))
        prescale = int(math.floor(prescaleval + 0.5))
        logger.debug('Final pre-scale: {0}'.format(prescale))
        oldmode = self._device.readU8(MODE1);
        newmode = (oldmode & 0x7F) | 0x10    # sleep
        self._device.write8(MODE1, newmode)  # go to sleep
        self._device.write8(PRESCALE, prescale)
        self._device.write8(MODE1, oldmode)
        time.sleep(0.005)
        self._device.write8(MODE1, oldmode | 0x80)

    def set_pwm(self, channel, on, off):
        """Sets a single PWM channel."""
        self._device.write8(LED0_ON_L+4*channel, on & 0xFF)
        self._device.write8(LED0_ON_H+4*channel, on >> 8)
        self._device.write8(LED0_OFF_L+4*channel, off & 0xFF)
        self._device.write8(LED0_OFF_H+4*channel, off >> 8)

    def set_all_pwm(self, on, off):
        """Sets all PWM channels."""
        self._device.write8(ALL_LED_ON_L, on & 0xFF)
        self._device.write8(ALL_LED_ON_H, on >> 8)
        self._device.write8(ALL_LED_OFF_L, off & 0xFF)
        self._device.write8(ALL_LED_OFF_H, off >> 8)
