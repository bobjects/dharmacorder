#!/usr/bin/env python
import inspect
from eventSourceMixin import EventSourceMixin
from state import State


class StateMachine(EventSourceMixin):
    __slots__ = 'current_state'

    def __init__(self):
        super(StateMachine, self).__init__()
        self.current_state = None
        self.transition_to_state_class(self.initial_state_class)

    @property
    def initial_state_class(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    def transition_to_state_class(self, a_class):
        self.trigger_event("request_state_transition", a_class)
        if self.current_state:
            self.current_state.exit_state()
            # TODO - Need to exit contours for current state.
        self.current_state = a_class(state_machine=self)
        # TODO - enter contours of the new current state
        self.current_state.enter_state()
