from recordingState import RecordingState
from completeRecordingState import CompleteRecordingState
from readyRecordingState import ReadyRecordingState


class InitialRecordingState(RecordingState):
    def enter_state(self):
        super(InitialRecordingState, self).enter_state()
        if self.file_already_exists:
            self.transition_to_state_class(CompleteRecordingState)
        else:
            self.transition_to_state_class(ReadyRecordingState)
