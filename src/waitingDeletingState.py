from deletingState import DeletingState
from selectingFileDeletingState import SelectingFileDeletingState


class WaitingDeletingState(DeletingState):
    def delete_button_held(self):
        super(WaitingDeletingState, self).delete_button_held()
        self.transition_to_state_class(SelectingFileDeletingState)
