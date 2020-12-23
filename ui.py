from pystray import Icon, Menu, MenuItem
from PIL import Image
from tkinter import Tk, PhotoImage, Text, END
from tkinter.filedialog import askdirectory
import json
import os


class Tray:
    icon = None
    icon_file = None
    menu = None
    time_sub = None
    path_sub = None
    is_ready = False
    directory = os.getcwd()
    version = 'v0.1'
    scrape_time = 60
    min1_state = False
    min5_state = False
    min10_state = False
    custom_state = False

    def __init__(self):
        # init app to not ready to exit
        self.is_ready = False

        # load the saved configuration from the config file
        self.check_config()

        # Set the time interval state based on the saved config
        self.set_state()

        # instantiate the Icon class and save a handle
        self.icon = Icon(name='LogScraper')

        # set the icon image from a local file
        self.icon_file = Image.open('cloudy.png')

        # tell the instance to use that image
        self.icon.icon = self.icon_file

        # populate the time interval sub-menu
        self.time_sub = Menu(MenuItem('1 minute',
                                      action=self.m1_on_clicked,
                                      checked=lambda item: self.min1_state),
                             MenuItem('5 minutes',
                                      action=self.m5_on_clicked,
                                      checked=lambda item: self.min5_state),
                             MenuItem('10 minutes',
                                      action=self.m10_on_clicked,
                                      checked=lambda item: self.min10_state),
                             Menu.SEPARATOR,
                             MenuItem('Custom Time',
                                      action=self.custom_on_clicked,
                                      checked=lambda item: self.custom_state))

        # populate the directory submenu
        self.path_sub = Menu(MenuItem(self.directory, None, enabled=False),
                             Menu.SEPARATOR,
                             MenuItem('Change Directory', action=self.get_new_file_directory),
                             MenuItem('(Note: Change will not be visible without restart,',
                                      None, enabled=False),
                             MenuItem('however a restart is NOT required!)', None, enabled=False))

        # populate the main menu
        self.menu = (MenuItem('About', None),
                     MenuItem('Time Interval', self.time_sub),
                     MenuItem('Change File Directory', self.path_sub),
                     Menu.SEPARATOR,
                     MenuItem('Exit', action=self.on_clicked_exit))

        # pass the menu structure to the icon instance
        self.icon.menu = self.menu

        # config is done. Run it.
        self.icon.run()

    def on_clicked_exit(self):
        """
        Prime the app for shutdown and stop the icon instance
        """
        self.is_ready = True
        self.icon.stop()

    def m1_on_clicked(self):
        """
        Passed to event callback to handle 1 minute interval event
        :return: no return
        """
        if not self.min1_state:
            self.min1_state = not self.min1_state
            self.min5_state = False
            self.min10_state = False
            self.custom_state = False

        self.scrape_time = 60
        self.dump_current_config()

    def m5_on_clicked(self):
        """
        Passed to event callback to handle 5 minute interval event
        :return: no return
        """
        if not self.min5_state:
            self.min1_state = False
            self.min5_state = not self.min5_state
            self.min10_state = False
            self.custom_state = False

        self.scrape_time = 300
        self.dump_current_config()

    def m10_on_clicked(self):
        """
        Passed to event callback to handle 10 minute interval event
        :return: no return
        """
        if not self.min10_state:
            self.min1_state = False
            self.min5_state = False
            self.min10_state = not self.min10_state
            self.custom_state = False

        self.scrape_time = 600
        self.dump_current_config()

    def custom_on_clicked(self):
        """
        Passed to event callback to handle custom time interval event
        :return: no return
        """
        if not self.custom_state:
            self.min1_state = False
            self.min5_state = False
            self.min10_state = False
            self.custom_state = not self.custom_state

        # TODO: Add popup window to input custom time
        self.dump_current_config()

    def user_clicked_exit(self):
        """
        Get the running status of the app
        :return: boolean indicating the readiness of the app to exit
        """
        return self.is_ready

    def dump_current_config(self):
        """Dump the current parameters to the config file"""
        with open("config/config.ini", "w+") as config_file:
            json_dict = {'version': self.version,
                         'time': self.scrape_time,
                         'path': self.directory}
            json.dump(json_dict, config_file)

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

    def set_state(self):
        """Set the appropriate state for the scrape time"""
        if self.scrape_time == 60:
            self.min1_state = True
        elif self.scrape_time == 300:
            self.min5_state = True
        elif self.scrape_time == 600:
            self.min10_state = True
        else:
            self.custom_state = True

    def get_scrape_time(self):
        """Get the interval time (in seconds) to compare against stopwatch"""
        return self.scrape_time

    def get_new_file_directory(self):
        Tk().withdraw()
        self.directory = askdirectory()
        self.dump_current_config()
