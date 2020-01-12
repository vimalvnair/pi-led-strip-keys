from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from sys import argv
import time
from rpi_ws281x import PixelStrip, Color
import argparse
import random

# LED strip configuration:
LED_COUNT = 50        # Number of LED pixels.
LED_PIN = 10        # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

led_strip = None

class handler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        global led_strip

        if self.path.endswith('favicon.ico'):
            return
        #print(self.path)
        #led_strip.setPixelColor(random.randrange(0, 50, 1), Color(random.randrange(0, 255, 10) ,random.randrange(0, 255, 10),random.randrange(0, 255, 10)))
        #led_strip.show()

        query = parse_qs(urlparse(self.path).query)
        code = int(query.get('code', ['-1'])[0])
        print(code)
        self._led_effect_for(code)

        self._set_response()

    def _led_effect_for(self, key_code):
        global led_strip

        if key_code <= 50:
            for i in range(key_code + 1):
                led_strip.setPixelColor(i, Color(0, 0, 255))

            for i in range(key_code + 1, LED_COUNT):
                led_strip.setPixelColor(i, Color(0, 255, 0))
        else:
            key_code = key_code % 50

            for i in range(key_code + 1):
                led_strip.setPixelColor(i, Color(0, 255, 255))

            for i in range(key_code + 1, LED_COUNT):
                led_strip.setPixelColor(i, Color(255, 0, 0))

        led_strip.show()
        
    def log_message(self, format, *args):
        return

def initialize_led_strip():
    global led_strip

    led_strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    led_strip.begin()
    
def run(server_class=HTTPServer, handler_class=handler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...\n')
    try:
        initialize_led_strip()
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Stopping httpd...\n')

if __name__ == '__main__':
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
