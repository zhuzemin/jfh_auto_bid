import sqlite3
import time
from PyQt5.QtCore import pyqtSignal, QThread


class iMacrosThread(QThread):
    progress_update = pyqtSignal(object)  # 信号类型
    Pause = False
    Headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}
    iMacros = None
    Threads = []
    extractList = []
    threadAttrObj={}
    progressObject={}

    def debug(self, s):
        if self.threadAttrObj['DEBUG']:
            print(s)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        self.DoWork()

    def DoWork(self):
        self.progressObject={
            'type':'iMacrosThread',
            'fxProfileName':self.threadAttrObj['fxProfileName']
        }
        ret=1
        while ret==1:
            #self.iMacros.iimPlay(self.threadAttrObj['iMacrosScriptPath'] + 'test.js')
            ret=self.iimToListPlay(self.threadAttrObj['iMacrosScriptPath'] + "getCountdown.iim")
            if ret==0:
                ret=self.iMacros.iimPlay(self.threadAttrObj['iMacrosScriptPath'] + "submit.js")
                #ret=self.iimToListPlay(self.threadAttrObj['iMacrosScriptPath'] + "submit.iim")
                break
            self.debug("self.extractList[0]: "+self.extractList[0])
            self.progressObject['status']='runing'
            self.progressObject['otherValue']={
                'countdown':self.extractList[0]
            }
            self.progress_update.emit(self.progressObject)
        '''result = self.extractList[1]
        conn = sqlite3.connect(self.threadAttrObj['DatabasePath'])  # 建立数据库连接
        cu = conn.cursor()
        cu.execute('INSERT OR IGNORE INTO jfh (url,result) VALUES (?,?)',
        (self.threadAttrObj['threadInitUrl'], result))
        conn.commit()  # 提交更改
        conn.close()  # 关闭数据库连接'''
        if ret==1:
            self.progressObject['status']='finish'
        elif ret==0:
            self.progressObject['status']='error'
        self.progress_update.emit(self.progressObject)

    def PauseSubThread(self):
        for thread in self.Threads:
            thread.Pause = self.Pause

    '''def setProgressVal(self, val):
        debug("self.ProgressBarCurrent: " + str(self.ProgressBarCurrent))

        val['CurrentKeywordIndex'] = self.CurrentKeywordIndex
        val['ProgressBarMax'] = self.ProgressBarMax
        self.ProgressBarCurrent = self.ProgressBarCurrent + 1
        val['ProgressBarCurrent'] = self.ProgressBarCurrent
        self.progress_update.emit(val)'''

    def TerminateSubThread(self):
        for thread in self.Threads:
            thread.terminate()

    def iimToListPlay(self,iimPath,iimValueObjectList=None):
        with open(iimPath, 'r') as f:
            iimList = f.readlines()
        self.extractList.clear()
        for line in iimList:
            if self.Pause:
                self.progressObject['status']: 'pause'
                self.progress_update.emit(self.progressObject)
                while self.Pause: time.sleep(1)
            if(iimValueObjectList is not None):
                for iimValueObject in iimValueObjectList:
                    for key, value in iimValueObject.items():
                        self.iMacros.iimSet(key,value)
            line='SET !TIMEOUT_STEP 1\n'+line
            ret=self.iMacros.iimPlayCode(line)
            if ret != 1:
                self.progressObject['status'] ='error'
                self.progress_update.emit(self.progressObject)
                return 0
            if self.iMacros.iimGetExtract(1) != 'NODATA':
                self.debug('self.iMacros.iimGetExtract(1): '+self.iMacros.iimGetExtract(1))
                self.extractList.append(self.iMacros.iimGetExtract(1))
            if self.threadAttrObj['DEBUG']:
                time.sleep(int(self.threadAttrObj['stepInterval']))
        return 1
