from dharmacorderState import DharmacorderState


class DeletingState(DharmacorderState):
    @property
    def session_to_delete(self):
        return self._state_machine.session_to_delete
