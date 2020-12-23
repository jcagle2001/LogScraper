import wx.adv
import wx
from os import getcwd

TRAY_TOOLTIP = 'LogScraper'
TRAY_ICON = 'cloudy.png'


def create_menu_item(menu, label, function, sub_menu):
    item = wx.MenuItem(parentMenu=menu, id=wx.ID_ANY, text=label, subMenu=sub_menu)
    menu.Bind(wx.EVT_MENU, function, id=item.GetId())
    menu.Append(item)
    return item


class WxUI(wx.adv.TaskBarIcon):
    directory = getcwd()
    scrape_interval = None
    one = None
    five = None
    ten = None
    custom = None
    status_1min = True
    status_5min = False
    status_10min = False
    status_custom = False
    about = None

    def __init__(self, frame):
        self.frame = frame
        super(WxUI, self).__init__()
        self.SetIcon(wx.Icon(TRAY_ICON), TRAY_TOOLTIP)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, None, None)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        int_sub = wx.Menu()
        dir_sub = wx.Menu()

        # Create interval submenu
        self.one = int_sub.AppendRadioItem(100, "1 minute")
        self.one.Check(self.status_1min)
        self.five = int_sub.AppendRadioItem(500, "5 minutes")
        self.five.Check(self.status_5min)
        self.ten = int_sub.AppendRadioItem(1000, "10 minutes")
        self.ten.Check(self.status_10min)
        self.custom = int_sub.AppendRadioItem(999, "Custom Interval")
        self.custom.Check(self.status_custom)
        int_sub.AppendSeparator()
        create_menu_item(int_sub, "Set Custom Interval", None, None)
        self.Bind(wx.EVT_MENU, self.toggle_one, self.one)
        self.Bind(wx.EVT_MENU, self.toggle_five, self.five)
        self.Bind(wx.EVT_MENU, self.toggle_ten, self.ten)
        self.Bind(wx.EVT_MENU, None, None, 999)

        # Create directory submenu
        create_menu_item(dir_sub, self.directory, None, None).Enable(False)
        dir_sub.AppendSeparator()
        create_menu_item(dir_sub, "Change Directory", None, None)

        # Create main popup menu
        self.about = create_menu_item(menu, "About", None, None)
        menu.Bind(wx.EVT_MENU, self.show_about, self.about)
        create_menu_item(menu, "Scrape Interval", None, int_sub)
        create_menu_item(menu, "Directory", None, dir_sub)
        menu.AppendSeparator()
        create_menu_item(menu, "Exit", None, None)

        return menu

    def toggle_one(self, e):
        if not self.status_1min:
            self.one.Check(not self.status_1min)
            self.scrape_interval = 60
            self.status_1min = True
            self.status_5min = False
            self.status_10min = False
            self.status_custom = False

    def toggle_five(self, e):
        if not self.status_5min:
            self.five.Check(not self.status_5min)
            self.scrape_interval = 300
            self.status_1min = False
            self.status_5min = True
            self.status_10min = False
            self.status_custom = False

    def toggle_ten(self, e):
        if not self.status_10min:
            self.ten.Check(not self.status_10min)
            self.scrape_interval = 6000
            self.status_1min = False
            self.status_5min = False
            self.status_10min = True
            self.status_custom = False

    def show_about(self, e):
        display_width, display_height = wx.DisplaySize()
        width = 400
        height = 500
        frame2 = wx.Frame(None, -1, title='About LogScraper')
        frame2.SetIcon(wx.Icon('cloudy.png'))
        frame2.SetSize((display_width / 2) - (width / 2),
                       (display_height / 2) - (height / 2),
                       width,
                       height)
        panel = wx.Panel(frame2)
        frame2.Show()
