from stateMachine import StateMachine
from termcolor import colored


class DharmacorderStateMachine(StateMachine):
    def __init__(self, a_dharmacorder):
        self.dharmacorder = a_dharmacorder
        super(DharmacorderStateMachine, self).__init__()

    def record_button_pressed(self):
        self.current_state.record_button_pressed()

    def upload_button_pressed(self):
        self.current_state.upload_button_pressed()

    def delete_button_pressed(self):
        self.current_state.delete_button_pressed()

    def delete_button_held(self):
        self.current_state.delete_button_held()

    def print_in_color(self, a_string):
        print colored(a_string, self.print_color)

    @property
    def print_color(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])
