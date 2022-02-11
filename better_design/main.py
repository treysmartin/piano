import simple_controller
import piano_lights

lights_controller = SimpleController(5, (244,0,0), (0,0,255))
piano_input = LightsFromPiano(50, (244,0,0),(0,0,255))
piano_input.run()

