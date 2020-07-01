import time

import shutil
from checkCopyProgressThread import *
from threading import Thread

DEBUG = True


def debug(s):
    if DEBUG:
        print(s)


class copyFxProfileThread(QThread):
    progress_update = pyqtSignal(object)  # 信号类型 homedir = os.path.expanduser("~")
    fxProfilePath=os.path.dirname(os.path.abspath(__file__)) + '\\Firefox\\Profiles'
    homedir = os.path.expanduser("~")
    fxProfile_iniPath = homedir + '\\AppData\\Roaming\\Mozilla\\Firefox\\profiles.ini'
    fxProfileName=None

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        self.DoWork()

    def DoWork(self):
        fxProfile_iniStr=None
        if os.path.exists(self.fxProfile_iniPath):
            if os.path.exists(self.fxProfile_iniPath + '_bak'):
                os.remove(self.fxProfile_iniPath + '_bak')
            os.rename(self.fxProfile_iniPath, self.fxProfile_iniPath + '_bak')
        fxProfile_iniStr = '''[General]
StartWithLastProfile=0

[Profile0]
Name=iMacros
IsRelative=0
Path=''' + os.path.dirname(os.path.abspath(__file__)) + '''\\Firefox\\Profiles\\iMacros
            '''
        imProfileCount=0
        for dir in os.listdir(self.fxProfilePath):  # loop through the folder
            if 'iMacros' in dir:
                imProfileCount=imProfileCount+1
                debug('imProfileCount: '+str(imProfileCount))
        self.fxProfileName=os.path.dirname(os.path.abspath(__file__)) + '\\Firefox\\Profiles\\iMacros'+str(imProfileCount)
        shutilThread = Thread(target=shutil.copytree, args=(os.path.dirname(os.path.abspath(__file__)) + '\\Firefox\\Profiles\\iMacros',self.fxProfileName,))
        #shutilThread.start()
        time.sleep(1)
        checkFolderSize=checkFolderSizeThread(self)
        checkFolderSize.srcPath=os.path.dirname(os.path.abspath(__file__)) + '\\Firefox\\Profiles\\iMacros'
        checkFolderSize.dstPath=os.path.dirname(os.path.abspath(__file__)) + '\\Firefox\\Profiles\\iMacros'+str(imProfileCount)
        checkFolderSize.progress_update.connect(self.HandleProgress)
        checkFolderSize.start()
        fxProfile_iniStr=fxProfile_iniStr+'''
[Profile''' + str(imProfileCount) + ''']
Name=iMacros''' + str(imProfileCount) + '''
IsRelative=0
Path=''' + os.path.dirname(os.path.abspath(__file__)) + '''\\Firefox\\Profiles\\iMacros''' + str(imProfileCount) + '''
                        '''
        #os.remove(self.fxProfile_iniPath)
        debug('os.path.dirname(os.path.abspath(__file__)): ' + os.path.dirname(os.path.abspath(__file__)))
        fileHandle = open(self.fxProfile_iniPath, 'w')
        fileHandle.write(fxProfile_iniStr)
        fileHandle.close()
        os.remove('profiles.ini')
        shutil.copyfile(self.fxProfile_iniPath, os.getcwd())
        debug(fxProfile_iniStr)
        #if os.path.exists(self.fxProfile_iniPath+'_bak'):
        #    os.remove(self.fxProfile_iniPath)
        #    os.rename(self.fxProfile_iniPath+'_bak', self.fxProfile_iniPath)

    def HandleProgress(self,progressObject):
        #debug("copyThread_progressObject: "+str(progressObject))
        self.progress_update.emit(progressObject)
