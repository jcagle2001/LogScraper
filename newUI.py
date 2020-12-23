from trayapp import TrayApp

class Tray:

    def __init__(self):
        with TrayApp(name= 'Log Scraper', icon_or_path='cloudy.png') as tray:
            tray.add_button('About', action=)
