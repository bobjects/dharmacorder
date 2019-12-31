from uploadingState import UploadingState
from waitingUploadingState import WaitingUploadingState


class InitialUploadingState(UploadingState):
    def enter_state(self):
        super(InitialUploadingState, self).enter_state()
        self.transition_to_state_class(WaitingUploadingState)
