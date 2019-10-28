import logging
import os
import sys
import time
import shutil
import pathlib

from datetime import datetime
from watchdog.events import FileSystemEventHandler, LoggingEventHandler
from watchdog.observers import Observer


def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')


def makedir(path):
    if(not os.path.exists(path)):
        os.mkdir(path)
        print("Directory ", path,
              path,  " Created ")
    else:
        print("Directory ", path,  " already exists")


def categorized_filetype(file_extension):
    types = {
        "Audio": ['.mid', '.aif', '.cda', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.wpl'],
        "Compressed": ['.7z', '.arj', '.deb', '.pkg', '.rar', '.rpm', '.tar', '.z', '.zip', ],
        "Image": ['.jpg', '.tif', '.ai', '.bmp', '.gif', '.ico', '.jpeg', '.png', '.ps', '.psd', '.svg', '.tif'],
        "Media": ['.bin',  '.dmg',  '.iso', '.toast',  '.vcd'],
        "Data": ['.dbf', '.csv', '.dat', '.db', '.log', '.mdb', '.sav', '.sql', '.tar', '.xml'],
        "Executable ": ['.pl', '.apk', '.bat', '.bin', '.cgi', '.com', '.exe', '.gadget', '.jar', '.py', '.wsf'],
        "Font": ['.fnt', '.fon', '.otf', '.ttf'],
        "Internet": ['.aspx', '.pl', '.html', '.asp', '.cer', '.cfm', '.cgi', '.css', '.htm', '.js', '.jsp', '.part', '.php', '.py', '.rss', '.xhtml'],
        "Presentation": ['.odp', '.pps', '.ppt', '.pptx'],
        "Programming": ['.c', '.class', '.cpp', '.cs', '.h', '.java', '.sh', '.swift', '.vb'],
        "Spreadsheet": ['.ods', '.xlr', '.xls', '.xlsx'],
        "System": ['.bak', '.cab', '.cfg', '.cpl', '.cur', '.dll', '.dmp', '.drv', '.icns', '.ico', '.ini', '.lnk', '.msi', '.sys', '.tmp'],
        "Video": ['.mpeg', '.3g2', '.3gp', '.avi', '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.rm', '.swf', '.vob', '.wmv'],
        "Word": ['.docx', '.wps', '.doc', '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wks', '.wpd'],
    }
    for type in types:
        if(file_extension in types[type]):
            return type
    return "Default"


def move_file(src, des):
    # if(not pathlib.Path(des).exists()):
    return os.rename(src, des)


class my_event_handler(LoggingEventHandler):
    def __init__(self, filename):
        self.filename = filename

    def on_created(self, event):
        # super(my_event_handler, self).on_created(event)
        dirName = datetime.today().strftime('%Y-%m-%d')
        create_current_date_dir = os.path.join(get_download_path(), dirName)
        file = os.path.splitext(event.src_path)
        base_file_name = os.path.basename(event.src_path)
        file_extension = file[1]
        if(not event.is_directory):
            file_dir = categorized_filetype(file_extension)
            extension_dir = os.path.join(
                create_current_date_dir, file_dir)
            # makedir(create_current_date_dir)
            # makedir(extension_dir)
            print(event.src_path, os.path.join(
                extension_dir, base_file_name))
            os.rename(event.src_path, os.path.join(
                extension_dir, base_file_name))


if __name__ == "__main__":
    download_path = get_download_path()
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    observer = Observer()
    event_handler1 = my_event_handler("s")
    observer.schedule(event_handler1, download_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
