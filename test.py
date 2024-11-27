from win32com.client import Dispatch
from sys import executable


def create_shortcut(file_name: str, target: str, work_dir: str, arguments: str = ''):
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(file_name)
    shortcut.TargetPath = target
    # shortcut.Arguments = arguments
    shortcut.WorkingDirectory = work_dir
    # shortcut.save()


create_shortcut("label.url", executable, "/")
