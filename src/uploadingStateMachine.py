from dharmacorderStateMachine import DharmacorderStateMachine
from initialUploadingState import InitialUploadingState


class UploadingStateMachine(DharmacorderStateMachine):
    def __init__(self, a_dharmacorder):
        super(UploadingStateMachine, self).__init__(a_dharmacorder)
        self.session_to_upload = None

    @property
    def initial_state_class(self):
        return InitialUploadingState

    @property
    def print_color(self):
        return 'blue'
