# -- coding: utf-8 --

import os

from ..data import icon


def notify(title, message, icon=icon.ico, **kwargs):
    """
    Optional parameters:
        * ``icon`` - path to an ICO file to display instead of the ntfy icon
    """

    import win32api
    import win32con
    import win32gui

    class WindowsBalloonTip:
        def __init__(self, title, msg):
            message_map = {win32con.WM_DESTROY: self.OnDestroy, }
            # Register the Window class.
            wc = win32gui.WNDCLASS()
            hinst = wc.hInstance = win32api.GetModuleHandle(None)
            wc.lpszClassName = "PythonTaskbar"
            wc.lpfnWndProc = message_map  # could also specify a wndproc.
            classAtom = win32gui.RegisterClass(wc)
            # Create the Window.
            style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
            self.hwnd = win32gui.CreateWindow(
                classAtom, "Taskbar", style, 0, 0, win32con.CW_USEDEFAULT,
                win32con.CW_USEDEFAULT, 0, 0, hinst, None)
            win32gui.UpdateWindow(self.hwnd)
            iconPathName = os.path.abspath(icon)
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            try:
                hicon = win32gui.LoadImage(hinst, iconPathName,
                                           win32con.IMAGE_ICON, 0, 0,
                                           icon_flags)
            except:
                hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
            flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
            nid = (self.hwnd, 0, flags, win32con.WM_USER + 20, hicon,
                   "tooltip")
            win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
            win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY,
                                      (self.hwnd, 0, win32gui.NIF_INFO,
                                       win32con.WM_USER + 20, hicon,
                                       "Balloon tooltip", title, 200, msg))
            win32gui.DestroyWindow(self.hwnd)

        def OnDestroy(self, hwnd, msg, wparam, lparam):
            win32api.PostQuitMessage(0)  # Terminate the app.

    WindowsBalloonTip(message, title)
