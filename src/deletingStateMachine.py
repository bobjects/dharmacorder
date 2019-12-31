from dharmacorderStateMachine import DharmacorderStateMachine
from initialDeletingState import InitialDeletingState


class DeletingStateMachine(DharmacorderStateMachine):
    __slots__ = 'session_to_delete'

    def __init__(self, a_dharmacorder):
        super(DeletingStateMachine, self).__init__(a_dharmacorder)
        self.session_to_delete = None

    @property
    def initial_state_class(self):
        return InitialDeletingState

    @property
    def print_color(self):
        return 'magenta'
