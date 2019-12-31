import alsaaudio
from dharmacorderSettings import DharmacorderSettings
from inProgressRecordingState import InProgressRecordingState
from stoppingRecordingState import StoppingRecordingState
from canceledRecordingState import CancelledRecordingState
from failedRecordingState import FailedRecordingState
from threading import Thread
from Queue import Queue
import datetime
import time


class ActivelyRecordingState(InProgressRecordingState):
    __slots__ = 'still_recording', 'was_canceled'

    def __init__(self, state_machine):
        self.still_recording = True
        self.was_canceled = False
        super(ActivelyRecordingState, self).__init__(state_machine)

    def enter_state(self):
        super(ActivelyRecordingState, self).enter_state()
        RecordingThread(self)

    def record_button_pressed(self):
        super(ActivelyRecordingState, self).record_button_pressed()
        self.still_recording = False

    def delete_button_held(self):
        print "Actively recording delete button held."
        self.was_canceled = True
        self.still_recording = False


class RecordingThread(Thread):
    __slots__ = '_initial_epoch_seconds', '_state'

    def __init__(self, a_state):
        super(RecordingThread, self).__init__()
        self._initial_epoch_seconds = self._current_epoch_seconds
        self._state = a_state
        self.start()

    def run(self):
        # try:
            card_index = DharmacorderSettings.instance.recording_device_number
            mixer_control = "Mic"
            volume_level = DharmacorderSettings.instance.recording_gain_0_to_100

            mixer = alsaaudio.Mixer(control=mixer_control, cardindex=card_index)
            mixer.setvolume(volume_level, 0, 'capture')
            # pcm = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, str(card_index))
            pcm = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, str(card_index))
            pcm.setchannels(2)
            pcm.setrate(48000)

            # warning:  setperiodsize is ineffective.  It's always 1024.
            # for n in range(1, 16385):
            #     if pcm.setperiodsize(n) == n:
            #         print n

            pcm.setformat(alsaaudio.PCM_FORMAT_S16_LE)
            pcm.setperiodsize(1024)
            while self._state.still_recording and not self.maximum_record_seconds_reached:
                l, data = pcm.read()
                # print l
                if l < 0:
                    print "Overrun!  Skipping this read"
                else:
                    self._state._state_machine.wavefile.writeframes(data)
            self.transition_away()
        # except:
        #     self._state.transition_to_state_class(FailedRecordingState)

    def transition_away(self):
        if self._state.was_canceled:
            self._state.transition_to_state_class(CancelledRecordingState)
        else:
            self._state.transition_to_state_class(StoppingRecordingState)

    @property
    def maximum_record_seconds_reached(self):
        return (self._current_epoch_seconds - self._initial_epoch_seconds) > DharmacorderSettings.instance.maximum_record_seconds

    @property
    def _current_epoch_seconds(self):
        # Holy crap, that's ugly.
        return time.mktime(datetime.datetime.today().timetuple())
