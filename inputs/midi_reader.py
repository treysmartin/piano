import rtmidi.midiutil as midiutil
import queue

class midi_reader:
    def __init__(self):
        self.eventQ = queue.Queue(1024)
        self.terminate = True;
        midiin, port_name = midiutil.open_midiinput(1)
        midiin.set_callback(self)

    def __call__(self, event, data=None):
        self.eventQ.put(event);

    def run(self, lightsController):
        self.terminate = False
        while not self.terminate:
            event = self.eventQ.get()
            lightsController.processEvent(event)

    def stop(self):
        self.terminate = True

