from uploadingState import UploadingState
# from selectingFileUploadingState import SelectingFileUploadingState
import selectingFileUploadingState
import os


class DeletingUploadedFileUploadingState(UploadingState):
    def enter_state(self):
        super(DeletingUploadedFileUploadingState, self).enter_state()
        # os.remove(self.session_to_upload.file_name)
        self.dharmacorder._recording_collection.delete_recording_session(self.session_to_upload)
        self.dharmacorder.update_display()
        self.transition_to_state_class(selectingFileUploadingState.SelectingFileUploadingState)
