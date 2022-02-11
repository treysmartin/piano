import queue

# library for processing midi inputs
from rtmidi import midiutil

# libraries for controlling lights
import board
import neopixel

class LightsFromPiano:
    DOWN = 144

    def __init__(self, num_lights, color_on, color_off):
        # state of the lights
        self.num_lights = num_lights
        self.color_on = color_on
        self.color_off = color_off
        self.next_light = 0
        self.prev_light = 0

        # initialize the lights array, turn all lights off
        self.pixels = neopixel.NeoPixel(board.D18,
                                        self.num_lights,
                                        brightness=1,
                                        pixel_order=neopixel.RGB)
        self.pixels.fill((0,0,0))

        # state of the midi signals
        self.event_q = queue.Queue(1024)
        self.terminate = True

        # initialize midi processing
        midiin = midiutil.open_midiinput(1)[0]
        midiin.set_callback(self)

    # function that gets called when midi signal is detected
    def __call__(self, event, data=None):
        self.event_q.put(event)

    # read from the events queue and control the lights
    def run(self):
        self.terminate = False
        while not self.terminate:
            event = self.event_q.get()
            message, deltatime = event
            state = message[0]
            print(message, deltatime)
            if state == LightsFromPiano.DOWN:
                self.pixels[self.next_light % self.num_lights] = self.color_on
                self.next_light+=1
            else:
                self.pixels[self.prev_light % self.num_lights] = self.color_off
                self.prev_light+=1

    def stop(self):
        self.terminate = True

if __name__=='__main__':
    lights_controller = LightsFromPiano(50, (244,0,0),(0,0,255))
    lights_controller.run()
