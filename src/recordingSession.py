from dharmacorderSettings import DharmacorderSettings
from recordingStateMachine import RecordingStateMachine
import datetime
import os.path
import os


class RecordingSession(object):
    __slots__ = '_dharmacorder', 'file_name', '_state_machine'

    def __init__(self, a_dharmacorder, existing_file_name_or_none=None):
        self._dharmacorder = a_dharmacorder
        self.file_name = existing_file_name_or_none
        if not existing_file_name_or_none:
            self.reset_file_name()
        self._state_machine = RecordingStateMachine(self._dharmacorder, self)

    def delete_file(self):
        try:
            os.remove(self.file_name)
        except OSError:
            pass

    def new_file_name(self, added_seconds=0):
        # The added_seconds thing is here to allow for switch bounce or other conditions that
        # result in more than one recording to start per second.
        answer = DharmacorderSettings.instance.recording_directory + "/" + DharmacorderSettings.instance.recording_file_prefix + self.current_timestamp_string(added_seconds) + ".wav"
        if os.path.isfile(answer):
            return self.new_file_name(added_seconds=added_seconds + 1)
        else:
            return answer

    def current_timestamp_string(self, added_seconds=0):
        return (datetime.datetime.today() + datetime.timedelta(seconds=added_seconds)).strftime('%Y_%m_%d_%H_%M_%S')

    @property
    def file_already_exists(self):
        return os.path.isfile(self.file_name)

    @property
    def is_in_progress(self):
        return self._state_machine.is_in_progress

    @property
    def is_complete(self):
        return self._state_machine.is_complete

    def reset_file_name(self):
        self.file_name = self.new_file_name()

    def __eq__(self, other):
        return self.file_name == other.file_name

    def __lt__(self, other):
        return self.file_name < other.file_name
