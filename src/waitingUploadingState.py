from uploadingState import UploadingState
from selectingFileUploadingState import SelectingFileUploadingState


class WaitingUploadingState(UploadingState):
    def upload_button_pressed(self):
        super(WaitingUploadingState, self).upload_button_pressed()
        self.transition_to_state_class(SelectingFileUploadingState)
