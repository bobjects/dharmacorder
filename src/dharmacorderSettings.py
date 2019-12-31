from classproperty import classproperty
from validate import Validator
from configobj import ConfigObj


class DharmacorderSettings(object):
    __slots__ = '_configobj'
    Instance = None

    @classproperty
    @classmethod
    def instance(cls):
        if cls.Instance is None:  # IGNORE:E0203
            cls.Instance = cls()  # IGNORE:W0201
        return cls.Instance

    def __init__(self):
        print("Instantiating DharmacorderSettings singleton")
        self._configobj = None
        self.create_sample_config()
        self.read_config_file()

    @property
    def display_brightness_1_to_7(self):
        return self._configobj['display_brightness_1_to_7']

    @property
    def recording_directory(self):
        return self._configobj['recording_directory']

    @property
    def recording_file_prefix(self):
        return self._configobj['recording_file_prefix']

    @property
    def led_brightness_1_to_10(self):
        return self._configobj['led_brightness_1_to_10']

    @property
    def upload_server_address(self):
        return self._configobj['upload_server_address']

    @property
    def upload_server_port(self):
        return self._configobj['upload_server_port']

    @property
    def upload_server_user_name(self):
        return self._configobj['upload_server_user_name']

    @property
    def upload_server_directory(self):
        return self._configobj['upload_server_directory']

    @property
    def led_display_data_pin(self):
        return self._configobj['led_display_data_pin']

    @property
    def led_display_clock_pin(self):
        return self._configobj['led_display_clock_pin']

    @property
    def record_led_pin(self):
        return self._configobj['record_led_pin']

    @property
    def upload_led_pin(self):
        return self._configobj['upload_led_pin']

    @property
    def delete_led_pin(self):
        return self._configobj['delete_led_pin']

    @property
    def record_button_pin(self):
        return self._configobj['record_button_pin']

    @property
    def upload_button_pin(self):
        return self._configobj['upload_button_pin']

    @property
    def delete_button_pin(self):
        return self._configobj['delete_button_pin']

    @property
    def maximum_record_seconds(self):
        return self._configobj['maximum_record_seconds']

    @property
    def button_hold_qualification_seconds(self):
        return self._configobj['button_hold_qualification_seconds']

    @property
    def recording_gain_0_to_100(self):
        return self._configobj['recording_gain_0_to_100']

    @property
    def recording_device_number(self):
        return self._configobj['recording_device_number']

    def read_config_file(self):
        self._configobj = ConfigObj(self.ini_file_name, configspec=self.configspec_file_name)
        self._configobj.validate(Validator(), copy=True)
        # Write, just in case there are missing values in the conf file.
        self._configobj.write()

    def create_sample_config(self):
        # TODO:  any way to do this without creating a physical configspec file?
        # It seems weird that you have to do that.
        with open(self.configspec_file_name, 'w') as f:
            f.write('''
            recording_directory = string(default='/home/pi/recordings')
            recording_file_prefix = string(default='raw_recording_')
            display_brightness_1_to_7 = integer(1, 7, default=1)
            led_brightness_1_to_10 = integer(1, 10, default=1)
            upload_server_address = string(default='bobjectsinc.com')
            upload_server_port = integer(0, 65535, default=22)
            upload_server_user_name = string(default='dharmacorder')
            upload_server_directory = string(default='~/uploads')
            led_display_data_pin = integer(1, 27, default=18)
            led_display_clock_pin = integer(1, 27, default=23)
            record_led_pin = integer(1, 27, default=24)
            upload_led_pin = integer(1, 27, default=25)
            delete_led_pin = integer(1, 27, default=12)
            record_button_pin = integer(1, 27, default=16)
            upload_button_pin = integer(1, 27, default=20)
            delete_button_pin = integer(1, 27, default=21)
            maximum_record_seconds = integer(10, 14400, default=7200)
            button_hold_qualification_seconds = integer(1, 60, default=2)
            recording_gain_0_to_100 = integer(0, 100, default=100)
            recording_device_number = integer(1, 10, default=1)
            ''')
        spec = ConfigObj(self.configspec_file_name, list_values=False)
        example_conf = ConfigObj(configspec=spec)
        assert example_conf.validate(Validator())
        copy = ConfigObj(example_conf.copy())
        with open(self.sample_ini_file_name, 'w') as f:
            copy.write(f)

    @property
    def ini_file_name(self):
        return "dharmacorder.conf"

    @property
    def configspec_file_name(self):
        return "configspec.conf"

    @property
    def sample_ini_file_name(self):
        return "dharmacorder.conf.sample"

