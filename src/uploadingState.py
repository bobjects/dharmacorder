from dharmacorderState import DharmacorderState


class UploadingState(DharmacorderState):
    @property
    def session_to_upload(self):
        return self._state_machine.session_to_upload
