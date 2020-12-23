"""
    Main loop
"""
from timer import Timer
from wxPyUI import WxUI
import wx
from wx.adv import TaskBarIcon

app = wx.App()
tray = WxUI(wx.adv.TaskBarIcon)
sw = Timer()
sw.start_timer()
app.MainLoop()

while not tray.is_ready_to_exit():
    pass

SystemExit(0)
