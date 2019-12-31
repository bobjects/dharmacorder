from deletingState import DeletingState
# from waitingDeletingState import WaitingDeletingState
from activelyDeletingState import ActivelyDeletingState
from threading import Thread
from time import sleep


class IndicatingDeletingState(DeletingState):
    def enter_state(self):
        super(IndicatingDeletingState, self).enter_state()
        IndicatingThread(self)


class IndicatingThread(Thread):
    __slots__ = '_state'

    def __init__(self, a_state):
        self._state = a_state
        super(IndicatingThread, self).__init__()
        self.start()

    def run(self):
        self.turn_on_led()
        sleep(1)
        self.turn_off_led()
        self.transition_away()

    def turn_on_led(self):
        self._state.dharmacorder._front_panel.delete_led_value = True

    def turn_off_led(self):
        self._state.dharmacorder._front_panel.delete_led_value = False

    def transition_away(self):
        self._state.transition_to_state_class(ActivelyDeletingState)
