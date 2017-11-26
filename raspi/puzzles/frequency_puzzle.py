from raspi.puzzles.puzzle import BOCSPuzzle
from raspi.arduino_comm import ArduinoCommEventType as EventType
from raspi.available_io import *
from random import *


class FrequencyPuzzle(BOCSPuzzle):

    PUZZLE_ID = 'frequency_puzzle'  # A unique ID (can be anything) to use when reporting puzzle stats to the server

    is_solved = False  # Set this to True when you want the BOCS to progress to the next puzzle

    def __init__(self, stat_server, update_io_state, register_callback):
        """
        Runs once, when the puzzle is first started.
        :param update_io_statke: a callback function to update the state of an I/O device
        :param register_callback: a callback function to register the function that should be called anytime a BOCS
            user input event occurs
        """
        # Perform some standard initialization defined by the BOCSPuzzle base class
        BOCSPuzzle.__init__(self, stat_server, update_io_state)

        # Register our `event_received` function to be called whenever there is a BOCS input event (e.g. key press)
        register_callback(self.user_input_event_received)

        # Let’s display the image bocs-start.png on the e-ink display
        self.eink.set_image('frequency_puzzle.png') #Does not exist yet

        #TODO Deploy Piano

        #Variable Setup
        self.code = '341532' #Assuming inputs are int increments from left to right
        self.code_state = 0  #Current input to look for in code

    def user_input_event_received(self, event):
        """
        This function is called whenever the user triggers an input event on the BOCS. The majority of your puzzle logic
        should probably be here (or be in another function called from here), as this will run every time the user does
        something to the box.
        :param event: an object with attributes `id` (which event happened), `data` (what was the primary data
        associated with the event, e.g. which key/number) and `options` (extra data, usually empty)
        """

        if event.data == int(self.code[self.code_state]):     #if input is = to relevant code input
            self.code_state += 1                         #yes - increment code input
            if code_state == 2:                      #check whether to play audio
                #TODO play correct2 audio clip      #yes - Play audio
            elif self.code_state == 4:
                #TODO play correct4 audio clip
        else:                                       #no - reset code input
            self.code_state = 0
            if random() >= 0.5:     #check whether to play audio (random)
                #TODO play random incorrect audio clip

        if self.code_state == 6:                         #if code is complete
            #TODO play finished audio clip          #yes - puzzle is finished, play audio, change screen
            self.eink.set_image('frequency_puzzle_solved.png')  # Does not exist yet
            self.is_solved = True
            #no - do nothing
