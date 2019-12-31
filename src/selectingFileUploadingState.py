from uploadingState import UploadingState
# from waitingUploadingState import WaitingUploadingState
import waitingUploadingState
from activelyUploadingState import ActivelyUploadingState


class SelectingFileUploadingState(UploadingState):
    def enter_state(self):
        super(SelectingFileUploadingState, self).enter_state()
        session = self.dharmacorder._recording_collection.oldest_complete_session
        print session
        self._state_machine.session_to_upload = session
        if session:
            self.transition_to_state_class(ActivelyUploadingState)
        else:
            self.transition_to_state_class(waitingUploadingState.WaitingUploadingState)
