from recordingState import RecordingState


class FailedRecordingState(RecordingState):
    def enter_state(self):
        super(FailedRecordingState, self).enter_state()
        self.dharmacorder.update_display()
        self.dharmacorder._recording_collection.create_ready_recording_session()

