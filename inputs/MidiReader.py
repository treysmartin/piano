import rtmidi.midiutil as midiutil
import queue

class PianoReader:
    def __init__(self):
        self.eventQ = queue.Queue(1024)
        print("Starting reading from piano")
        midiin, port_name = midiutil.open_midiinput(1)
        midiin.set_callback(self)

    def __call__(self, event, data=None):
        self.eventQ.put(event);

    def getEventQueue(self):
        return self.eventQ
