from recordingState import RecordingState
from startingRecordingState import StartingRecordingState


class ReadyRecordingState(RecordingState):
    def record_button_pressed(self):
        super(ReadyRecordingState, self).record_button_pressed()
        self.transition_to_state_class(StartingRecordingState)
