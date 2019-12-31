from state import State


class DharmacorderState(State):
    def record_button_pressed(self):
        pass

    def upload_button_pressed(self):
        pass

    def delete_button_pressed(self):
        pass

    def delete_button_held(self):
        pass

    def enter_state(self):
        self.print_in_color("    entering " + str(type(self).__name__))
        super(DharmacorderState, self).enter_state()

    def exit_state(self):
        self.print_in_color("        exiting " + str(type(self).__name__))
        super(DharmacorderState, self).exit_state()

    def print_in_color(self, a_string):
        self._state_machine.print_in_color(a_string)

    @property
    def dharmacorder(self):
        return self._state_machine.dharmacorder
