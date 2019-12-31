from recordingState import RecordingState
from completeRecordingState import CompleteRecordingState


class StoppingRecordingState(RecordingState):
    def enter_state(self):
        super(StoppingRecordingState, self).enter_state()
        self._state_machine.wavefile.close()
        self.dharmacorder._front_panel.record_led_value = False
        self.dharmacorder._recording_collection.create_ready_recording_session()
        self.transition_to_state_class(CompleteRecordingState)
