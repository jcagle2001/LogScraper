from infi.systray import SysTrayIcon
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory
import json


def do_nothing():
    pass


class TrayUI:
    tray = None
    menu_options = None
    directory = os.getcwd()
    scrape_time = 60
    version = 'v0.1'
    is_ready = False

    def __init__(self):
        self.menu_options = (('About', "cloudyIcon.ico", do_nothing),
                             ('Time Interval', None, (('1 minute', None, do_nothing),
                                                      ('5 minutes', None, do_nothing),
                                                      ('10 minutes', None, do_nothing),
                                                      (None, None, do_nothing),
                                                      ('Custom Interval', None, do_nothing))),
                             ('File Directory', None, ((self.directory, None, do_nothing),
                                                       (None, None, do_nothing),
                                                       ('Change Directory', None,
                                                        self.get_new_file_directory))),
                             (None, None, do_nothing)
                             )
        self.tray = SysTrayIcon(icon="cloudyIcon.ico",
                                hover_text="LogScraper",
                                menu_options=self.menu_options,
                                on_quit=self.on_clicked_exit)
        self.tray.start()

    def get_new_file_directory(self):
        Tk().withdraw()
        self.directory = askdirectory()
        self.dump_current_config()
        self.tray.update()

    def get_scrape_time(self):
        """Get the interval time (in seconds) to compare against stopwatch"""
        return self.scrape_time

    def check_config(self):
        """
            Load config parameters from the config file, if it exists.
            If not, create the file and populate it with the default parameters
        """
        try:
            with open("config/config.ini", "r") as config_file:
                json_dict = json.load(config_file)
                self.version = json_dict['version']
                self.scrape_time = json_dict['time']
                self.directory = json_dict['path']
        except FileNotFoundError:
            self.dump_current_config()

    def dump_current_config(self):
        """
        Dump the current parameters to the config file
        """
        with open("config/config.ini", "w+") as config_file:
            json_dict = {'version': self.version,
                         'time': self.scrape_time,
                         'path': self.directory}
            json.dump(json_dict, config_file)

    def on_clicked_exit(self):
        """
        Prime the app for shutdown and stop the icon instance
        """
        self.is_ready = True
        self.tray.shutdown()

    def user_clicked_exit(self):
        """
        Get the running status of the app
        :return: boolean indicating the readiness of the app to exit
        """
        return self.is_ready
