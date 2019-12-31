from deletingState import DeletingState
from waitingDeletingState import WaitingDeletingState


class InitialDeletingState(DeletingState):
    def enter_state(self):
        super(InitialDeletingState, self).enter_state()
        self.transition_to_state_class(WaitingDeletingState)

