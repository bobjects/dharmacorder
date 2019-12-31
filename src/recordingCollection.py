import glob
from recordingSession import RecordingSession
from dharmacorderSettings import DharmacorderSettings


class RecordingCollection(object):
    __slots__ = '_dharmacorder', '_recording_sessions'

    def __init__(self, a_dharmacorder):
        self._dharmacorder = a_dharmacorder
        self._recording_sessions = []

    def populate_with_existing_recordings(self):
        for wav_file_path_name in sorted(glob.iglob(DharmacorderSettings.instance.recording_directory + '/*.wav')):
            self._recording_sessions.append(RecordingSession(self._dharmacorder, wav_file_path_name))

    def create_ready_recording_session(self):
        self._recording_sessions.append(RecordingSession(self._dharmacorder))

    def delete_recording_session(self, a_recording_session):
        if a_recording_session in self._recording_sessions:
            self._recording_sessions.remove(a_recording_session)
            a_recording_session.delete_file()

    @property
    def complete_recording_sessions(self):
        return [sess for sess in self._recording_sessions if sess.is_complete]

    @property
    def oldest_complete_session(self):
        return next((sess for sess in sorted(self._recording_sessions) if sess.is_complete), None)

    @property
    def newest_complete_session(self):
        return next((sess for sess in sorted(self._recording_sessions, reverse=True) if sess.is_complete), None)

    @property
    def in_progress_session(self):
        return next((sess for sess in self._recording_sessions if sess.is_in_progress), None)

    @property
    def state_machines(self):
        return [sess._state_machine for sess in self._recording_sessions]

