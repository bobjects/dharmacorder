from dharmacorderState import DharmacorderState


class RecordingState(DharmacorderState):
    @property
    def file_name(self):
        return self._state_machine.file_name

    @property
    def file_already_exists(self):
        return self._state_machine.file_already_exists

    @property
    def is_in_progress(self):
        return False

    @property
    def is_complete(self):
        return False

    @property
    def recording_session(self):
        return self._state_machine.recording_session
