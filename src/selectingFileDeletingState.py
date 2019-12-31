from deletingState import DeletingState
# from waitingDeletingState import WaitingDeletingState
import waitingDeletingState
from indicatingDeletingState import IndicatingDeletingState


class SelectingFileDeletingState(DeletingState):
    def enter_state(self):
        super(SelectingFileDeletingState, self).enter_state()
        print self.dharmacorder._recording_collection.in_progress_session
        if self.dharmacorder._recording_collection.in_progress_session:
            # If there is an in-progress recording session, then that session will cancel itself if the user holds the delete button.
            # So we do nothing here.
            self.transition_to_state_class(waitingDeletingState.WaitingDeletingState)
        else:
            session = self.dharmacorder._recording_collection.newest_complete_session
            self._state_machine.session_to_delete = session
            if session:
                self.transition_to_state_class(IndicatingDeletingState)
            else:
                self.transition_to_state_class(waitingDeletingState.WaitingDeletingState)
