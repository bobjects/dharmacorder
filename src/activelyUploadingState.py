from uploadingState import UploadingState
from deletingUploadedFileUploadingState import DeletingUploadedFileUploadingState
# from selectingFileUploadingState import SelectingFileUploadingState
import selectingFileUploadingState
import waitingUploadingState
from dharmacorderSettings import DharmacorderSettings
import subprocess


class ActivelyUploadingState(UploadingState):
    def enter_state(self):
        super(ActivelyUploadingState, self).enter_state()
        self.dharmacorder._front_panel.upload_led_value = 'fastblink'
        print self._rsync_command_and_args_list
        try:
            subprocess.check_call(self._rsync_command_and_args_list)
        except subprocess.CalledProcessError:
            print "upload failed."
            # self.transition_to_state_class(selectingFileUploadingState.SelectingFileUploadingState)
            self.dharmacorder._front_panel.upload_led_value = False
            self.transition_to_state_class(waitingUploadingState.WaitingUploadingState)
        else:
            print "GOT HERE"
            self.dharmacorder._front_panel.upload_led_value = False
            self.transition_to_state_class(DeletingUploadedFileUploadingState)

    @property
    def _rsync_command_and_args_list(self):
        return [
            'rsync',
            # '-e ssh',
            # 'ssh',
            # '-times',
            '--partial',
            '-e ""/usr/bin/ssh -p {0}""'.format(DharmacorderSettings.instance.upload_server_port),
            # '-e',
            # '""/usr/bin/ssh',
            # '-p',
            # '{0}""'.format(DharmacorderSettings.instance.upload_server_port),
            self.session_to_upload.file_name,
            DharmacorderSettings.instance.upload_server_user_name + "@" + DharmacorderSettings.instance.upload_server_address + ":" + DharmacorderSettings.instance.upload_server_directory
        ]
