import configparser as cp
import pathlib 
import sys
from os import path, mkdir


class Config(cp.ConfigParser):
    def __init__(self, program_name, default_template):
        super().__init__(self)
        if getattr(sys, 'frozen', False):
            exec_path = path.dirname(path.abspath(str(sys.executable)))
        else:
            exec_path = ".\\"
        self.program_name = program_name
        self.path = str(pathlib.Path.home()) + f"\\.config\\{program_name}\\config.ini"
        if not path.isdir(str(pathlib.Path.home()) + "\\.config\\"):
            mkdir(str(pathlib.Path.home()) + "\\.config\\")
        if not path.isdir(str(pathlib.Path.home()) + f"\\.config\\{program_name}\\"):
            mkdir(str(pathlib.Path.home()) + f"\\.config\\{program_name}\\")
        if not path.exists(str(pathlib.Path.home()) + f"\\.config\\{program_name}\\config.ini"):
            self._generate_default_config_file(default_template)
        self.read(self.path)

    def _generate_default_config_file(self, default_template):
        self['DEFAULT'] = {
            "Program": self.program_name}
        self.update(default_template)
        with open(self.path, 'w') as configfile:
            self.write(configfile)

    def save(self):
        with open(self.path, 'w') as configfile:
            self.write(configfile)
