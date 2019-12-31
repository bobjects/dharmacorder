#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ledDisplayTM1637 import LEDDisplayTM1637
from frontPanel import FrontPanel
from recordingCollection import RecordingCollection
from recordingStateMachine import RecordingStateMachine
from uploadingStateMachine import UploadingStateMachine
from deletingStateMachine import DeletingStateMachine
from dharmacorderSettings import DharmacorderSettings
import sys
import os
import time
import datetime
from time import sleep
# import RPi.GPIO as IO
from gpiozero import DigitalOutputDevice
from gpiozero import LED
from gpiozero import Button
from time import sleep
import socket
import re


class Dharmacorder(object):
    __slots__ = '_front_panel', '_recording_collection', '_uploading_state_machine', '_deleting_state_machine'

    def __init__(self):
        self._front_panel = FrontPanel()
        self.display_initial_messages()
        self._recording_collection = RecordingCollection(self)
        self._recording_collection.populate_with_existing_recordings()
        self._recording_collection.create_ready_recording_session()
        self._uploading_state_machine = UploadingStateMachine(self)
        self._deleting_state_machine = DeletingStateMachine(self)
        self._front_panel.when_event_do("recordButtonPressed", self.record_button_pressed)
        self._front_panel.when_event_do("uploadButtonPressed", self.upload_button_pressed)
        self._front_panel.when_event_do("deleteButtonPressed", self.delete_button_pressed)
        self._front_panel.when_event_do("deleteButtonHeld", self.delete_button_held)
        self.update_display()

    @property
    def _state_machines(self):
        return [self._uploading_state_machine, self._deleting_state_machine] + self._recording_collection.state_machines

    def record_button_pressed(self):
        for state_machine in self._state_machines:
            state_machine.record_button_pressed()

    def upload_button_pressed(self):
        for state_machine in self._state_machines:
            state_machine.upload_button_pressed()

    def delete_button_pressed(self):
        for state_machine in self._state_machines:
            state_machine.delete_button_pressed()

    def delete_button_held(self):
        for state_machine in self._state_machines:
            state_machine.delete_button_held()

    def display_initial_messages(self):
        self._front_panel.display_value = " 1P "
        sleep(1)
        # TODO: display the last octet of the IPv4 address.
        last_octet = ""
        try:
            address = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if
                         not ip.startswith("127.")] or [
                            [(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in
                             [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
            last_octet = str(re.search('\d*$', address).group(0))
        except:
            pass
        self._front_panel.display_value = last_octet
        sleep(2)
        self._front_panel.display_value = ""

    def update_display(self):
        number_complete = len(self._recording_collection.complete_recording_sessions)
        if number_complete:
            self._front_panel.display_value = number_complete
        else:
            self._front_panel.display_value = "    "


def main():
    import termcolor
    print termcolor.COLORS
    dharmacorder = Dharmacorder()
    # recordLED = LED(24)
    # uploadLED = LED(25)
    # deleteLED = LED(12)
    # recordButton = Button(16)
    # uploadButton = Button(20)
    # deleteButton = Button(21)
    #
    # def record_button_payload():
    #     recordLED.toggle()
    #
    # def upload_button_payload():
    #     uploadLED.toggle()
    #
    # def delete_button_payload():
    #     deleteLED.toggle()
    #
    # recordButton.when_pressed = record_button_payload
    # uploadButton.when_pressed = upload_button_payload
    # deleteButton.when_pressed = delete_button_payload

    # Just act like a clock for now.  :)
    # use_24_hour_format = True
    # colon_is_on = True
    # dharmacorder._front_panel._display.clear()
    # while True:
    #     now = datetime.datetime.now()
    #     hour = now.hour
    #     minute = now.minute
    #     if not use_24_hour_format:
    #         hour = (hour - 1) % 12 + 1
    #     digits = [hour / 10, hour % 10, minute / 10, minute % 10]
    #     if not hour / 10:
    #         digits[0] = None
    #     dharmacorder._front_panel.display_value = digits
    #     dharmacorder._front_panel._display.colon = colon_is_on
    #     colon_is_on = not colon_is_on
    #     sleep(0.5)
    while True:
            sleep(1000)


if __name__ == '__main__':
    main()
