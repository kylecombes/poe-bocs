from raspi.io_states.keypad_state import KeypadState
from raspi.puzzles.puzzle import BOCSPuzzle
from raspi.arduino_comm import ArduinoCommEventType as EventType
from raspi.available_io import *


class BirthdayParadoxPuzzle(BOCSPuzzle):

    PUZZLE_ID = 'Birthday Paradox'  # Used by stat server

    PROMPT = "How many people are needed in a room for the probability that 2 have the " \
            "same birthday to be greater than 50%?"
    LINE_2_PREFIX = "Input: "
    guess = ""
    ANSWER = "23"
    is_solved = False

    def __init__(self, init_bundle, register_callback):
        BOCSPuzzle.__init__(self, init_bundle)

        # Set the initial states of the inputs and outputs we'll be using
        self.eink.set_text('{}\n\n{}'.format(self.PROMPT, self.LINE_2_PREFIX))
        self.keypad_state = KeypadState(visible=True)
        self.update_io_state(ARDUINO1, self.keypad_state)

        # Subscribe to input events
        register_callback(self.key_pressed)

    def key_pressed(self, event):
        if event.id == EventType.NUMERIC_KEYPAD_PRESS:
            key = event.data
            if key == '#':  # Submit
                if self.guess == self.ANSWER:
                    self.keypad_state.set_visible(False)
                    self.update_io_state(ARDUINO1, self.keypad_state)
                    self.eink.set_text('Correct!')
                    self.is_solved = True
                    self.report_attempt(self.PUZZLE_ID)
                else:
                    self.eink.set_text("Sorry, that's incorrect")
                    self.report_attempt(self.PUZZLE_ID, self.guess)
                    self.pause(5)
                    self.eink.set_text('{}\n\n{}'.format(self.PROMPT, self.LINE_2_PREFIX))
            else:
                if key == '*':  # Backspace
                    self.guess = self.guess[0:-1]
                else:  # Digit entry
                    self.guess += str(key)

                line2 = self.LINE_2_PREFIX + self.guess

                self.eink.set_text('{}\n\n{}{}'.format(self.PROMPT, self.LINE_2_PREFIX, self.guess))
