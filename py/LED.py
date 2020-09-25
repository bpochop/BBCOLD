'''
# import RPi.GPIO as GPIO
# from rpi_ws281x import *
import argparse

# LED strip configuration:
LED_COUNT      = 93      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 5     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
args = parser.parse_args()

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()


class LED():
    def __init__(self):
        self.LEDdone = True

    def mainLoop(self, strip):
        pass
        done = True
        while done:
            self.colorWipe(strip, Color(0, 0, 0), 10)  # This will slowsly turn off all LED...
            # i.e. the crosshair, before it starts animation
            self.colorWipe(strip, Color(127, 0, 0))  # Red wipe
            self.checkIfDone()
            self.colorWipe(strip, Color(127, 127, 127))  # White wipe
            self.checkIfDone()
            self.colorWipe(strip, Color(000, 000, 127))  # Blue wipe
            self.checkIfDone()
            self.theaterChase(strip, Color(0, 0, 127))  # Blue theater chase
            self.checkIfDone()
            self.theaterChase(strip, Color(127, 127, 127))  # White theater chase
            self.checkIfDone()
            self.theaterChase(strip, Color(127, 0, 0))  # Red theater chase
            self.checkIfDone()
            self.rainbow(strip)
            self.checkIfDone()
            self.rainbowCycle(strip)
            self.checkIfDone()
            self.theaterChaseRainbow(strip)
            self.checkIfDone()
            done = False

    #             if LEDdone = False:
    #                 break

    def checkIfDone(self):
        return done, self.LEDdone

    def LEDISDONE(self):
        done = False
        self.LEDdone = False
        return done, self.LEDdone

    def colorCupPlacement(self, strip):
        for i in range(72, 84):
            strip.setPixelColor(i, Color(255, 0, 0))
            strip.show()
        for i in range(84, 93):
            strip.setPixelColor(i, Color(255, 255, 255))
            strip.show()

        strip.setPixelColor(24, Color(255, 0, 0))
        strip.setPixelColor(50, Color(255, 0, 0))
        strip.setPixelColor(68, Color(255, 0, 0))
        strip.setPixelColor(8, Color(255, 0, 0))
        strip.setPixelColor(38, Color(255, 0, 0))
        strip.setPixelColor(60, Color(255, 0, 0))
        strip.setPixelColor(0, Color(255, 0, 0))
        strip.setPixelColor(32, Color(255, 0, 0))
        strip.setPixelColor(56, Color(255, 0, 0))
        strip.setPixelColor(16, Color(255, 0, 0))
        strip.setPixelColor(44, Color(255, 0, 0))
        strip.setPixelColor(64, Color(255, 0, 0))
        strip.show()

    def colorWipe(self, strip, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(int(LED_COUNT)):
            strip.setPixelColor(i, color)
            strip.show()
            t.sleep(wait_ms / 2000.0)

    def theaterChase(self, strip, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, int(LED_COUNT), 3):
                    strip.setPixelColor(i + q, color)
                strip.show()
                t.sleep(wait_ms / 1000.0)
                for i in range(0, int(LED_COUNT), 3):
                    strip.setPixelColor(i + q, 0)

    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def rainbow(self, strip, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256 * iterations):
            for i in range(int(LED_COUNT)):
                strip.setPixelColor(i, self.wheel((i + j) & 255))
            strip.show()
            t.sleep(wait_ms / 1000.0)

    def rainbowCycle(self, strip, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256 * iterations):
            for i in range(int(LED_COUNT)):
                strip.setPixelColor(i, self.wheel((int(i * 256 / int(LED_COUNT)) + j) & 255))
            strip.show()
            t.sleep(wait_ms / 1000.0)

    def theaterChaseRainbow(self, strip, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, int(LED_COUNT), 3):
                    strip.setPixelColor(i + q, self.wheel((i + j) % 255))
                strip.show()
                t.sleep(wait_ms / 2000.0)
                for i in range(0, int(LED_COUNT), 3):
                    strip.setPixelColor(i + q, 0)

    def checkIfDone(self):
        return '''
