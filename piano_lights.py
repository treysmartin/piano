import queue

# library for processing midi inputs
from rtmidi import midiutil

class LightsFromPiano:

    def __init__(self):
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
    def run(self, lights_controller):
        self.terminate = False
        while not self.terminate:
            event = self.event_q.get()
            lights_controller.process_event(event)

    def stop(self):
        self.terminate = True
