from deletingState import DeletingState
# from selectingFileDeletingState import SelectingFileDeletingState
import waitingDeletingState


class ActivelyDeletingState(DeletingState):
    def enter_state(self):
        super(ActivelyDeletingState, self).enter_state()
        session = self._state_machine.session_to_delete
        if session:
            self.dharmacorder._recording_collection.delete_recording_session(session)
            self.dharmacorder.update_display()
        self.transition_to_state_class(waitingDeletingState.WaitingDeletingState)
