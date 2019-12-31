from recordingState import RecordingState


class InProgressRecordingState(RecordingState):
    @property
    def is_in_progress(self):
        return True
