import rtmidi.midiutil as midiutil
import queue

class midi_reader:
    def __init__(self):
        self.event_q = queue.Queue(1024)
        self.terminate = True
        midiin, port_name = midiutil.open_midiinput(1)
        midiin.set_callback(self)

    def __call__(self, event, data=None):
        self.event_q.put(event)

    def run(self, lights_controller):
        self.terminate = False
        while not self.terminate:
            event = self.event_q.get()
            lights_controller.process_event(event)

    def stop(self):
        self.terminate = True
