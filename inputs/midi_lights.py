import queue

# library for processing midi inputs
from rtmidi import midiutil

# libraries for controlling lights
import board
import neopixel

class LightsFromMidi:
    DOWN = 144

    def __init__(self, num_lights, color_on, color_off):
        # state of the lights
        self.num_lights = num_lights
        self.on = colorOn
        self.off = colorOff
        self.next_light = 0
        self.prev_light = 0

        # initialize the lights array, turn all lights off
        self.pixels = neopixel.NeoPixel(board.D18, numLights, brightness=1, pixel_order=pixelOrder)
        self.pixels.fill((0,0,0))

        # state of the midi signals
        self.event_q = queue.Queue(1024)
        self.terminate = True

        # initialize midi processing
        midiin, port_name = midiutil.open_midiinput(1)
        midiin.set_callback(self)

    def __call__(self, event, data=None):
        self.event_q.put(event)

    def run(self, lights_controller):
        self.terminate = False
        while not self.terminate:
            event = self.event_q.get()
            message, deltatime = event
            key = message[1]
            state = message[0]
            print(message, deltatime)
            if (state == DOWN):
               self.pixels[self.next_light % self.num_lights] = self.on
               self.next_light+=1
            else:
               self.pixels[self.prev_light % self.num_lights] = self.off
               self.prev_light+=1

    def stop(self):
        self.terminate = True
