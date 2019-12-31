from dharmacorderSettings import DharmacorderSettings
from eventSourceMixin import EventSourceMixin
from ledDisplayTM1637 import LEDDisplayTM1637
from gpiozero import LED
from gpiozero import PWMLED
from gpiozero import Button


class FrontPanel(EventSourceMixin):
    __slots__ = '_record_led', '_upload_led', '_delete_led', '_record_button', '_upload_button', '_delete_button'

    def __init__(self):
        super(FrontPanel, self).__init__()
        # TODO: adjust brightness with DharmacorderSettings.instance.led_brightness_1_to_10
        self._display = LEDDisplayTM1637(brightness_0_to_7=DharmacorderSettings.instance.display_brightness_1_to_7, data_pin=DharmacorderSettings.instance.led_display_data_pin, clock_pin=DharmacorderSettings.instance.led_display_clock_pin)
        # self._record_led = LED(DharmacorderSettings.instance.record_led_pin)
        # self._upload_led = LED(DharmacorderSettings.instance.upload_led_pin)
        # self._delete_led = LED(DharmacorderSettings.instance.delete_led_pin)
        self._record_led = PWMLED(DharmacorderSettings.instance.record_led_pin)
        self._upload_led = PWMLED(DharmacorderSettings.instance.upload_led_pin)
        self._delete_led = PWMLED(DharmacorderSettings.instance.delete_led_pin)
        # Don't attempt to use bounce_time - it's broken.  Grrr......
        self._record_button = Button(DharmacorderSettings.instance.record_button_pin, hold_time=0.25)
        self._upload_button = Button(DharmacorderSettings.instance.upload_button_pin, hold_time=0.25)
        # self._record_button = Button(DharmacorderSettings.instance.record_button_pin)
        # self._upload_button = Button(DharmacorderSettings.instance.upload_button_pin)
        self._delete_button = Button(DharmacorderSettings.instance.delete_button_pin, hold_time=DharmacorderSettings.instance.button_hold_qualification_seconds)
        self._delete_button.when_pressed = self._delete_button_pressed_payload
        self._record_button.when_held = self._record_button_held_payload
        self._upload_button.when_held = self._upload_button_held_payload
        self._delete_button.when_held = self._delete_button_held_payload

    @property
    def record_led_value(self):
        return self._record_led.is_lit

    @record_led_value.setter
    def record_led_value(self, a_boolean_or_string):
        if a_boolean_or_string == 'blink' or a_boolean_or_string == 'slowblink':
            self._record_led.blink(on_time=1, off_time=0.5, fade_in_time=0.5, fade_out_time=0.5)
        elif a_boolean_or_string == 'fastblink':
            self._record_led.blink(on_time=0.25, off_time=0.25, fade_in_time=0, fade_out_time=0)
        elif a_boolean_or_string is True:
            self._record_led.on()
        else:
            self._record_led.off()

    @property
    def upload_led_value(self):
        return self._upload_led.is_lit

    @upload_led_value.setter
    def upload_led_value(self, a_boolean_or_string):
        if a_boolean_or_string == 'blink' or a_boolean_or_string == 'slowblink':
            self._upload_led.blink(on_time=1, off_time=0.5, fade_in_time=0.5, fade_out_time=0.5)
        elif a_boolean_or_string == 'fastblink':
            self._upload_led.blink(on_time=0.25, off_time=0.25, fade_in_time=0, fade_out_time=0)
        elif a_boolean_or_string is True:
            self._upload_led.on()
        else:
            self._upload_led.off()

    @property
    def delete_led_value(self):
        return self._delete_led.is_lit

    @delete_led_value.setter
    def delete_led_value(self, a_boolean_or_string):
        if a_boolean_or_string == 'blink' or a_boolean_or_string == 'slowblink':
            self._delete_led.blink(on_time=1, off_time=0.5, fade_in_time=0.5, fade_out_time=0.5)
        elif a_boolean_or_string == 'fastblink':
            self._delete_led.blink(on_time=0.25, off_time=0.25, fade_in_time=0, fade_out_time=0)
        elif a_boolean_or_string is True:
            self._delete_led.on()
        else:
            self._delete_led.off()

    @property
    def display_value(self):
        return self._display.value

    @display_value.setter
    def display_value(self, an_object):
        self._display.value = an_object

    def _record_button_held_payload(self):
        self.trigger_event("recordButtonPressed")

    def _upload_button_held_payload(self):
        self.trigger_event("uploadButtonPressed")

    def _delete_button_pressed_payload(self):
        self.trigger_event("deleteButtonPressed")

    def _delete_button_held_payload(self):
        self.trigger_event("deleteButtonHeld")
