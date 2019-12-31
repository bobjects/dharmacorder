

class State(object):
    __slots__ = '_state_machine'

    def __init__(self, state_machine):
        self._state_machine = state_machine

    def enter_state(self):
        pass

    def exit_state(self):
        pass

    def transition_to_state_class(self, a_class):
        self._state_machine.transition_to_state_class(a_class)
