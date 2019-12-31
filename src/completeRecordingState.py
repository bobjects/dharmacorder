from recordingState import RecordingState


class CompleteRecordingState(RecordingState):
    def enter_state(self):
        super(CompleteRecordingState, self).enter_state()
        self.dharmacorder.update_display()

    @property
    def is_complete(self):
        return True
