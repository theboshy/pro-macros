from win32gui import GetWindowText, GetForegroundWindow, GetWindowOrgEx


print(GetWindowText(GetForegroundWindow()))
