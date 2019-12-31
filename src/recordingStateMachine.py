from dharmacorderStateMachine import DharmacorderStateMachine
from initialRecordingState import InitialRecordingState


class RecordingStateMachine(DharmacorderStateMachine):
    __slots__ = 'recording_session'

    def __init__(self, a_dharmacorder, a_recording_session):
        self.recording_session = a_recording_session
        super(RecordingStateMachine, self).__init__(a_dharmacorder)

    @property
    def initial_state_class(self):
        return InitialRecordingState

    @property
    def print_color(self):
        return 'red'

    @property
    def file_name(self):
        return self.recording_session.file_name

    @property
    def file_already_exists(self):
        return self.recording_session.file_already_exists

    @property
    def is_in_progress(self):
        return self.current_state.is_in_progress

    @property
    def is_complete(self):
        return self.current_state.is_complete
