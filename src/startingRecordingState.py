import os
import wave
from inProgressRecordingState import InProgressRecordingState
from activelyRecordingState import ActivelyRecordingState
from dharmacorderSettings import DharmacorderSettings


class StartingRecordingState(InProgressRecordingState):
    def enter_state(self):
        super(StartingRecordingState, self).enter_state()
        # self.dharmacorder._front_panel.record_led_value = True
        self.dharmacorder._front_panel.record_led_value = 'slowblink'
        self.reset_file_name()
        self.create_directory_if_needed()
        self.start_recording()
        self.transition_to_state_class(ActivelyRecordingState)

    def reset_file_name(self):
        self._state_machine.recording_session.reset_file_name()

    def create_directory_if_needed(self):
        dirname = DharmacorderSettings.instance.recording_directory
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def start_recording(self):
        print self.file_name
        self._state_machine.wavefile = wave.open(self.file_name, 'w')
        self._state_machine.wavefile.setnchannels(2)
        self._state_machine.wavefile.setsampwidth(2)
        self._state_machine.wavefile.setframerate(48000)
