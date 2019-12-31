from recordingState import RecordingState


class CancelledRecordingState(RecordingState):
    def enter_state(self):
        super(CancelledRecordingState, self).enter_state()
        self.dharmacorder._front_panel.record_led_value = False
        self.dharmacorder._recording_collection.delete_recording_session(self.recording_session)
        self.dharmacorder.update_display()
        self.dharmacorder._recording_collection.create_ready_recording_session()

