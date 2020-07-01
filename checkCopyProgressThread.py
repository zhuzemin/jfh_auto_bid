import os
from PyQt5.QtCore import pyqtSignal, QThread

DEBUG = True


def debug(s):
    if DEBUG:
        print(s)


class checkFolderSizeThread(QThread):
    progress_update = pyqtSignal(object)  # 信号类型 homedir = os.path.expanduser("~")
    srcPath=None
    dstPath=None

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        self.DoWork()

    def DoWork(self):
        currentSize=0
        totalSize=self.get_fileNumber(self.srcPath)
        progressObject={
            'type':'checkCopyProgressThread',
            'totalFileNumber':totalSize,
        }
        while currentSize!=totalSize:
            currentSize=self.get_fileNumber(self.dstPath)
            progressObject['currentSize']=currentSize
            #debug("checkThread_progressObject: "+str(progressObject))
            self.progress_update.emit(progressObject)
        progressObject['currentSize']=self.get_size(self.dstPath)
        self.progress_update.emit(progressObject)

    def get_size(self, start_path='.'):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)

        return total_size

    def get_fileNumber(self, start_path='.'):
        path, dirs, files = next(os.walk(start_path))
        return len(files)