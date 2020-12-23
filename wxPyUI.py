import wx.adv
import wx
from os import getcwd
import json

TRAY_TOOLTIP = 'LogScraper'
TRAY_ICON = 'cloudy.png'


def create_menu_item(menu, label, function, sub_menu):
    item = wx.MenuItem(parentMenu=menu, id=wx.ID_ANY, text=label, subMenu=sub_menu)
    menu.Bind(wx.EVT_MENU, function, id=item.GetId())
    menu.Append(item)
    return item


def show_about(e):
    """
    Shows the 'About' window that provides information about the application and author
    :param e: event variable
    :return: Nothing
    """
    # Window size
    width = 550
    height = 810

    # Window creation
    frame2 = wx.Frame(None, -1, title='About LogScraper', style=wx.CAPTION)
    frame2.SetIcon(wx.Icon('cloudy.png'))
    frame2.SetSize(0, 0, width, height)
    frame2.Centre()

    # Main panel to hold all widgets
    panel = wx.Panel(frame2)
    panel.SetBackgroundColour(wx.WHITE)
    box = wx.BoxSizer(wx.VERTICAL)

    # panel that holds the main image
    img_panel = wx.Panel(panel)
    img_panel.SetBackgroundColour(wx.WHITE)
    image = 'cloudy.png'
    ready = wx.Image(image, wx.BITMAP_TYPE_PNG)
    wx.StaticBitmap(img_panel, -1, wx.Bitmap(ready))

    # Title Text panel and text
    title = wx.Panel(panel)
    title.SetBackgroundColour(wx.WHITE)
    text = wx.StaticText(title, label='Thanks for using LogScraper!\n')
    font = text.GetFont()
    font = font.Bold()
    font.PointSize = 16
    text.SetFont(font)

    # Attribution and info panel
    attribution_panel = wx.Panel(panel)
    attribution_panel.SetBackgroundColour(wx.WHITE)
    info = wx.StaticText(attribution_panel, label='\n\nIcons made by Freepik \n'
                                                  '(https://www.flaticon.com/authors/freepik)\n'
                                                  'from https://www.flaticon.com/\n\n'
                                                  'LogScraper author - Justin Cagle\n'
                                                  '(https://github.com/jcagle2001/LogScraper)\n'
                                                  'Email: Jcagle2001@msn.com\n\n')

    # Close window button
    button = wx.Button(panel, label='Close')
    button.Bind(wx.EVT_BUTTON, handler=lambda ev: frame2.Close(True), source=button)

    # Add widgets to sizer
    box.Add(title, 0, wx.CENTER)
    box.Add(img_panel, 0, wx.CENTER)
    box.Add(attribution_panel, 0, wx.CENTER)
    box.Add(button, 0, wx.CENTER)
    panel.SetSizer(box)

    # display the window
    frame2.Show()


def show_input_dialogue():
    # Create a frame to hold the dialogue
    dialogue = wx.Frame(None, -1, 'Enter Custom Interval')
    dialogue.SetSize(0, 0, 200, 50)
    dialogue.Centre()

    # create a file input dialogue
    form = wx.TextEntryDialog(dialogue, "Interval (in whole minutes):", 'Enter Custom Interval')
    form.SetValue('')

    # if the user enters a new value and clicks OK, return that value
    if form.ShowModal() == wx.ID_OK:
        value = form.GetValue()
        try:
            value = int(value) * 60
        except ValueError:
            wx.MessageBox('Input must be a whole number value!'
                          '\n\nPlease enter a new value.', 'Error',
                          wx.OK | wx.ICON_ERROR)
            return show_input_dialogue()
    else:
        value = None

    form.Destroy()
    return value


def get_new_path():
    frame = wx.Frame(None, -1, 'Choose Directory')
    dialogue = wx.DirDialog(frame, 'Choose new Directory Path')
    if dialogue.ShowModal() == wx.ID_OK:
        new_path = dialogue.GetPath()
    else:
        new_path = None

    dialogue.Destroy()

    return new_path


class WxUI(wx.adv.TaskBarIcon):
    directory = getcwd()
    version = 'v.0.1'
    scrape_interval = 60
    one = None
    five = None
    ten = None
    custom = None
    status_1min = True
    status_5min = False
    status_10min = False
    status_custom = False
    about = None
    is_ready = False

    def __init__(self, frame):
        """
        Initialize the GUI
        :param frame: main GUI window
        """
        self.frame = frame
        super(WxUI, self).__init__()
        self.SetIcon(wx.Icon(TRAY_ICON), TRAY_TOOLTIP)
        self.check_config()
        self.set_state()

    def CreatePopupMenu(self):
        """
        Creates the right-click popup menu
        :return: Menu
        """
        menu = wx.Menu()
        int_sub = wx.Menu()
        dir_sub = wx.Menu()

        # Create interval submenu
        create_menu_item(int_sub, str(int(self.scrape_interval / 60)) + ' minute(s)',
                         None, None).Enable(False)
        int_sub.AppendSeparator()
        self.one = int_sub.AppendRadioItem(100, "1 minute")
        self.one.Check(self.status_1min)
        self.five = int_sub.AppendRadioItem(500, "5 minutes")
        self.five.Check(self.status_5min)
        self.ten = int_sub.AppendRadioItem(1000, "10 minutes")
        self.ten.Check(self.status_10min)
        self.custom = int_sub.AppendRadioItem(999, "Custom Interval")
        self.custom.Check(self.status_custom)
        int_sub.AppendSeparator()
        create_menu_item(int_sub, "Set Custom Interval", self.toggle_custom, None)

        # Event handlers for each interval that is clickable.
        self.Bind(wx.EVT_MENU, self.toggle_one, self.one)
        self.Bind(wx.EVT_MENU, self.toggle_five, self.five)
        self.Bind(wx.EVT_MENU, self.toggle_ten, self.ten)

        # Create directory submenu
        create_menu_item(dir_sub, self.directory, None, None).Enable(False)
        dir_sub.AppendSeparator()
        create_menu_item(dir_sub, "Change Directory", self.change_path, None)

        # Create main popup menu
        self.about = create_menu_item(menu, "About", None, None)
        menu.Bind(wx.EVT_MENU, show_about, self.about)
        create_menu_item(menu, "Scrape Interval", None, int_sub)
        create_menu_item(menu, "Directory", None, dir_sub)
        menu.AppendSeparator()
        create_menu_item(menu, "Exit", self.on_exit, None)

        return menu

    def on_exit(self, e):
        """
        Handles GUI shutdown request
        :param e: event
        :return: none
        """
        self.dump_current_config()
        wx.CallAfter(self.Destroy)
        self.is_ready = True

    def is_ready_to_exit(self):
        """
        Indicates that the GUI has received a shutdown request.
        :return: bool
        """
        return self.is_ready

    def toggle_one(self, e):
        """
        Toggle the '1 minute' Interval item
        :param e: event
        :return: none
        """
        if not self.status_1min:
            self.one.Check(not self.status_1min)
            self.scrape_interval = 60
            self.status_1min = True
            self.status_5min = False
            self.status_10min = False
            self.status_custom = False
            self.dump_current_config()

    def toggle_five(self, e):
        """
        Toggle the '5 minutes' Interval item
        :param e: event
        :return: none
        """
        if not self.status_5min:
            self.five.Check(not self.status_5min)
            self.scrape_interval = 300
            self.status_1min = False
            self.status_5min = True
            self.status_10min = False
            self.status_custom = False
            self.dump_current_config()

    def toggle_ten(self, e):
        """
        Toggle the '10 minutes' Interval item
        :param e: event
        :return: none
        """
        if not self.status_10min:
            self.ten.Check(not self.status_10min)
            self.scrape_interval = 600
            self.status_1min = False
            self.status_5min = False
            self.status_10min = True
            self.status_custom = False
            self.dump_current_config()

    def toggle_custom(self, e):
        """
        Toggle the 'Custom Interval' Interval item when a custom value is entered
        :param e: event
        :return: none
        """
        if not self.custom:
            self.custom.Check(not self.status_custom)
        value = show_input_dialogue()
        if value is not None:
            self.scrape_interval = value
            self.status_1min = False
            self.status_5min = False
            self.status_10min = False
            self.status_custom = True
            self.dump_current_config()

    def change_path(self, e):
        """
        Handles user path change
        :param e: event
        :return: none
        """
        new_path = get_new_path()

        if new_path is not None:
            self.directory = new_path
            self.dump_current_config()
        else:
            return

    def provide_path(self):
        """
        Indicates the desired user path to look for a log file
        :return: directory path
        """
        return self.directory

    def dump_current_config(self):
        """Dump the current parameters to the config file"""
        with open("config/config.ini", "w+") as config_file:
            json_dict = {'version': self.version,
                         'time': self.scrape_interval,
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
                self.scrape_interval = json_dict['time']
                self.directory = json_dict['path']
        except FileNotFoundError:
            self.dump_current_config()

    def set_state(self):
        """Set the appropriate state for the scrape time"""
        if self.scrape_interval == 60:
            self.status_1min = True
        elif self.scrape_interval == 300:
            self.status_5min = True
        elif self.scrape_interval == 600:
            self.status_10min = True
        else:
            self.status_custom = True
