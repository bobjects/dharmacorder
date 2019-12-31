import sys
import os
import time
import datetime
from time import sleep
from RPi import GPIO


class LEDDisplayTM1637(object):
    __slots__ = '_clock_pin', '_data_pin', '_brightness', '_value', '_colon', '_characters_and_encoded_bytes', '_last_written_encoded_bytes', '_last_written_brightness', '_last_written_string'

    def __init__(self, clock_pin=23, data_pin=18, brightness_0_to_7=2):
        self._clock_pin = clock_pin
        self._data_pin = data_pin
        self._brightness = brightness_0_to_7
        self._value = None
        self._colon = False
        self._characters_and_encoded_bytes = None
        self._last_written_encoded_bytes = None
        self._last_written_brightness = None
        self._last_written_string = "    "
        self._initialize_characters_and_encoded_bytes()
        self._initialize_pins()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, a_string_integer_or_list):
        self._value = a_string_integer_or_list
        self.show(a_string_integer_or_list)

    @property
    def colon(self):
        return self._colon

    @colon.setter
    def colon(self, a_boolean):
        self._colon = a_boolean
        self.show_string(self._last_written_string)

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, brightness_0_to_7):
        self._brightness = min(max(brightness_0_to_7, 0), 7)
        self.show_string(self._last_written_string)

    def clear(self):
        self.colon = False
        self.show_string("    ")

    def show(self, a_string_integer_or_list):
        if isinstance(a_string_integer_or_list, basestring):
            self.show_string(a_string_integer_or_list)
        elif isinstance(a_string_integer_or_list, int):
            self.show_integer(a_string_integer_or_list)
        elif isinstance(a_string_integer_or_list, (list, tuple)):
            self.show_list(a_string_integer_or_list)
        else:
            raise ValueError("Argument to show() must be a string, int, list, or tuple.")

    def show_integer(self, an_integer, zero_padded=False):
        integer_to_show = min(an_integer, 9999)
        if zero_padded:
            string_to_show = '{0:04d}'.format(integer_to_show)
        else:
            string_to_show = '{:4}'.format(integer_to_show)
        self.show_string(string_to_show)

    def show_string(self, a_string):
        trimmed_padded_string = '{a_string: <{width}}'.format(a_string=a_string, width=4)[:4]
        self._last_written_string = trimmed_padded_string
        encoded_bytes = (
            self._encoded_byte_for_character(trimmed_padded_string[0]),
            self._encoded_byte_for_character(trimmed_padded_string[1]),
            self._encoded_byte_for_character(trimmed_padded_string[2]),
            self._encoded_byte_for_character(trimmed_padded_string[3])
        )
        self._write_encoded_bytes_to_display(encoded_bytes)

    def show_list(self, a_list_of_integers):
        string_to_show = ""
        if len(a_list_of_integers) is not 4:
            raise ValueError("show_list() requires a 4-element list or tuple")
        for element in a_list_of_integers:
            if isinstance(element, int):
                string_to_show += str(max(min(element, 9), 0))
            elif element is None:
                string_to_show += " "
            else:
                raise ValueError("show_tuple() requires a list or tuple of only integers or None")
        self.show_string(string_to_show)

    def _write_encoded_bytes_to_display(self, a_list_of_ints):
        if (self._last_written_encoded_bytes is not a_list_of_ints) or (self._last_written_brightness is not self._brightness):
            self._last_written_encoded_bytes = a_list_of_ints
            self._start_display_write_cycle()
            self._write_raw_byte_to_display(0x40)  # Auto addressing mode
            self._finish_display_write_cycle()
            self._start_display_write_cycle()
            self._write_raw_byte_to_display(0xC0)  # Start address
            for encoded_byte in a_list_of_ints:
                self._write_raw_byte_to_display(encoded_byte)
            self._finish_display_write_cycle()
            self._start_display_write_cycle()
            self._write_raw_byte_to_display(0x88 + self._brightness)
            self._finish_display_write_cycle()

    def _start_display_write_cycle(self):
        GPIO.output(self._clock_pin, GPIO.HIGH)
        GPIO.output(self._data_pin, GPIO.HIGH)
        GPIO.output(self._data_pin, GPIO.LOW)
        GPIO.output(self._clock_pin, GPIO.LOW)

    def _finish_display_write_cycle(self):
        GPIO.output(self._clock_pin, GPIO.LOW)
        GPIO.output(self._data_pin, GPIO.LOW)
        GPIO.output(self._clock_pin, GPIO.HIGH)
        GPIO.output(self._data_pin, GPIO.HIGH)

    def _write_raw_byte_to_display(self, byte_integer):
        bits = byte_integer
        for _ in range(0, 8):
            GPIO.output(self._clock_pin, GPIO.LOW)
            if bits & 1:
                GPIO.output(self._data_pin, GPIO.HIGH)
            else:
                GPIO.output(self._data_pin, GPIO.LOW)
            bits = bits >> 1
            GPIO.output(self._clock_pin, GPIO.HIGH)

        # wait for ACK
        GPIO.output(self._clock_pin, GPIO.LOW)
        GPIO.output(self._data_pin, GPIO.HIGH)
        GPIO.output(self._clock_pin, GPIO.HIGH)
        GPIO.setup(self._data_pin, GPIO.IN)

        while GPIO.input(self._data_pin):
            time.sleep(0.001)
            if GPIO.input(self._data_pin):
                GPIO.setup(self._data_pin, GPIO.OUT)
                GPIO.output(self._data_pin, GPIO.LOW)
                GPIO.setup(self._data_pin, GPIO.IN)
        GPIO.setup(self._data_pin, GPIO.OUT)

    def _encoded_byte_for_character(self, a_character):
        answer = self._characters_and_encoded_bytes[a_character]
        if self._colon:
            answer += 0x80
        return answer

    def _initialize_pins(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._clock_pin, GPIO.OUT)
        GPIO.setup(self._data_pin, GPIO.OUT)

    def _initialize_characters_and_encoded_bytes(self):
        self._characters_and_encoded_bytes = {
            # Most-significant segment to least:
            # center, upper-left, lower-left, bottom, lower-right, upper-right, top.
            '0': 0b00111111,
            '1': 0b00000110,
            '2': 0b01011011,
            '3': 0b01001111,
            '4': 0b01100110,
            '5': 0b01101101,
            '6': 0b01111101,
            '7': 0b00000111,
            '8': 0b01111111,
            '9': 0b01101111,
            '': 0b00000000,
            ' ': 0b00000000,
            'a': 0b01110111,
            'b': 0b01111100,
            'c': 0b00111001,
            'd': 0b01011110,
            'e': 0b01111001,
            'f': 0b01110001,
            'g': 0b00111100,
            'h': 0b01110110,
            'i': 0b00000100,
            'j': 0b00011110,
            'k': 0b01110110,  # ambiguous - try not to use this character
            'l': 0b00111000,
            'm': 0b00110111,  # ambiguous - try not to use this character
            'n': 0b01010100,
            'o': 0b01011100,
            'p': 0b01110011,
            'q': 0b01100111,  # ambiguous - try not to use this character
            'r': 0b01010000,
            's': 0b01101101,  # ambiguous - try not to use this character
            't': 0b01111000,
            'u': 0b00011100,
            'v': 0b00111110,  # ambiguous - try not to use this character
            'w': 0b01111110,  # ambiguous - try not to use this character
            'x': 0b01110110,  # ambiguous - try not to use this character
            'y': 0b01101110,
            'z': 0b01011011,  # ambiguous - try not to use this character
            'A': 0b01110111,
            'B': 0b01111100,
            'C': 0b00111001,
            'D': 0b01011110,
            'E': 0b01111001,
            'F': 0b01110001,
            'G': 0b00111100,
            'H': 0b01110110,
            'I': 0b00000100,
            'J': 0b00011110,
            'K': 0b01110110,  # ambiguous - try not to use this character
            'L': 0b00111000,
            'M': 0b00110111,  # ambiguous - try not to use this character
            'N': 0b01010100,
            'O': 0b01011100,
            'P': 0b01110011,
            'Q': 0b01100111,  # ambiguous - try not to use this character
            'R': 0b01010000,
            'S': 0b01101101,  # ambiguous - try not to use this character
            'T': 0b01111000,
            'U': 0b00011100,
            'V': 0b00111110,  # ambiguous - try not to use this character
            'W': 0b01111110,  # ambiguous - try not to use this character
            'X': 0b01110110,  # ambiguous - try not to use this character
            'Y': 0b01101110,
            'Z': 0b01011011  # ambiguous - try not to use this character
        }


if __name__ == '__main__':
    display = LEDDisplayTM1637(brightness_0_to_7=0)
    display.clear()
