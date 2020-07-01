import os
import shutil

from PyQt5.QtCore import pyqtSignal, QThread
import win32com.client

DEBUG = True


def debug(s):
    if DEBUG:
        print(s)


class FirefoxThread(QThread):
    progress_update = pyqtSignal(object)  # 信号类型 homedir = os.path.expanduser("~")
    iMacros = win32com.client.Dispatch("imacros")
    threadAttrObj={}

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        self.DoWork()

    def DoWork(self):
        if os.path.exists('profiles.ini'):
            if os.path.exists(self.threadAttrObj['fxProfile_iniPath']) and os.path.exists(self.threadAttrObj['fxProfile_iniPath']+'_bak') is not True:
                os.rename(self.threadAttrObj['fxProfile_iniPath'], self.threadAttrObj['fxProfile_iniPath']+'_bak')
            shutil.copyfile('profiles.ini',self.threadAttrObj['fxProfile_iniPath'])
        self.iMacros.iimInit('-fx -fxPath "Firefox\\firefox.exe" -fxProfile "'+self.threadAttrObj['fxProfileName']+'"', True)
        progressObject={
            'type':'iMacrosThread',
            'status':'ready',
            'fxProfileName':self.threadAttrObj['fxProfileName']
        }
        self.progress_update.emit(progressObject)
        #if os.path.exists(self.fxProfile_iniPath+'_bak'):
        #    os.remove(self.fxProfile_iniPath)
        #    os.rename(self.fxProfile_iniPath+'_bak', self.fxProfile_iniPath)
        self.iMacros.iimSet('url',self.threadAttrObj['threadInitUrl'])
        self.iMacros.iimPlay(self.threadAttrObj['iMacrosScriptPath'] + 'login.iim')
