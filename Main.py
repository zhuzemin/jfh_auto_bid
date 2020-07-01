import glob
import json
import sys

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QFileDialog, QAction, QAbstractItemView
from PyQt5 import QtWidgets
from MainWindow import Ui_MainWindow
from iMacrosThread import *
from FirefoxThread import *
from tkinter import Tk
from tkinter.filedialog import askdirectory
from copyFxProfileThread import *

class Main(QtWidgets.QMainWindow):
    ConfigPath = 'config.ini'
    DatabasePath = 'log.db'
    iMacrosThreadList = {}
    tableView_threadListModel = QStandardItemModel()
    iMacrosScriptPath = os.path.dirname(os.path.abspath(__file__)) + '\\iMacrosScript\\'
    firefoxThreadList = {}
    threadInitUrl=None
    fxProfileName=None
    homedir = os.path.expanduser("~")
    fxProfile_iniPath = homedir + '\\AppData\\Roaming\\Mozilla\\Firefox\\profiles.ini'
    threadAttrObj={}

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_launchFirefox.clicked.connect(self.launchFirefox)
        self.ui.pushButton_addProfile.clicked.connect(self.copyFxProfile)
        self.ui.pushButton_Start.clicked.connect(lambda: self.ThreadControl("Start"))
        self.ui.pushButton_Pause.clicked.connect(self.thread_pause_resume)
        self.ui.pushButton_Cancel.clicked.connect(lambda: self.ThreadControl("Terminate"))
        self.ui.progressBar.setValue(0)
        self.ui.groupBox_iMacros.setEnabled(False)
        self.tableView_threadListModel.setHorizontalHeaderLabels(['url', 'countdown', 'status', 'fxProfileName'])
        self.ui.tableView_threadList.setModel(self.tableView_threadListModel)
        self.ui.tableView_threadList.selectionModel().selectionChanged.connect(self.tableViewSelectChange)
        self.ui.tableView_threadList.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.ui.actionLoad_Profile.triggered.connect(self.MakeopenFileNameDialog("ProfileLoad"))
        # self.ui.actionSave_Profile.triggered.connect(lambda:self.saveFileDialog("ProfileSave"))
        if len(sys.argv) > 1:
            if sys.argv[1] == '-c' and os.path.exists(sys.argv[2]):
                self.ConfigPath = sys.argv[2]
        if os.path.exists(self.ConfigPath):
            self.loadConfig(self.ConfigPath)
        QAction("Quit", self).triggered.connect(self.closeEvent)
        self.createDB(self.DatabasePath)

    def launchFirefox(self):
        self.threadAttrObj = {
            'DEBUG': self.ui.checkBox_debugEnable.isChecked(),
            'fxProfile_iniPath': self.fxProfile_iniPath,
            'stepInterval': self.ui.lineEdit_stepInterval.text(),
            'iMacrosScriptPath': self.iMacrosScriptPath,
            'DatabasePath': self.DatabasePath,
            #'ProxyEnable': self.ui.checkBox_ProxyEnable.isChecked(),
            #'Proxy': self.ui.lineEdit_Proxy.text(),
            'fxProfileName': self.fxProfileName,
            'threadInitUrl': self.threadInitUrl
        }
        thread = FirefoxThread(self)  # 创建一个线程
        thread.progress_update.connect(self.HandleProgress)
        thread.threadAttrObj = self.threadAttrObj
        thread.start()
        self.firefoxThreadList[self.fxProfileName]=thread
        self.ui.pushButton_launchFirefox.setEnabled(False)
        self.ui.groupBox_iMacros.setEnabled(True)

    def tableViewSelectChange(self):
        for index in sorted(self.ui.tableView_threadList.selectionModel().selectedRows()):
            self.threadInitUrl = self.ui.tableView_threadList.model().data(self.ui.tableView_threadList.model().index(index.row(),0))
            self.fxProfileName=self.ui.tableView_threadList.model().data(self.ui.tableView_threadList.model().index(index.row(),3))
            status=self.ui.tableView_threadList.model().data(self.ui.tableView_threadList.model().index(index.row(),2))
            debug('status: '+status)
            debug('self.threadInitUrl: '+self.threadInitUrl)
            debug('self.fxProfileName: '+self.fxProfileName)
            if status =='firefoxNotOpen':
                self.ui.pushButton_launchFirefox.setEnabled(True)
                self.ui.groupBox_iMacros.setEnabled(False)
            elif status == "ready":
                self.ui.pushButton_launchFirefox.setEnabled(False)
                self.ui.groupBox_iMacros.setEnabled(True)
                self.ui.pushButton_Start.setEnabled(True)
            elif status == "error" or status =='finish':
                self.ui.pushButton_launchFirefox.setEnabled(False)
                self.ui.groupBox_iMacros.setEnabled(True)
                self.ui.pushButton_Start.setEnabled(True)
            elif status == "runing":
                self.ui.pushButton_launchFirefox.setEnabled(False)
                self.ui.groupBox_iMacros.setEnabled(True)
                self.ui.pushButton_Start.setEnabled(False)

            self.ui.pushButton_addProfile.setText('Edit')
        if len(self.ui.tableView_threadList.selectionModel().selectedRows())==0:
            self.ui.pushButton_launchFirefox.setEnabled(False)
            self.ui.groupBox_iMacros.setEnabled(False)
            self.ui.pushButton_addProfile.setText('Add')

    def copyFxProfile(self):
        if self.ui.pushButton_addProfile.text()=='Add':
            #self.Firefox.iMacros.iimClose()
            #self.Firefox.terminate()
            copyFxProfile=copyFxProfileThread(self)
            copyFxProfile.progress_update.connect(self.HandleProgress)
            copyFxProfile.start()
            url = QStandardItem(self.ui.lineEdit_url.text())
            countdown=QStandardItem('##: ##: ##')
            status=QStandardItem('firefoxNotOpen')
            fxProfileName=QStandardItem(copyFxProfile.fxProfileName)
            self.tableView_threadListModel.appendRow([url,countdown,status,fxProfileName])
        elif self.ui.pushButton_addProfile.text()=='Edit':
            self.threadInitUrl=self.ui.lineEdit_url.text()
            for index in sorted(self.ui.tableView_threadList.selectionModel().selectedRows()):
                self.tableView_threadListModel.setData(self.ui.tableView_threadList.model().index(index.row(),0), self.threadInitUrl)

    def createDB(self, DatabasePath):
        conn = sqlite3.connect(DatabasePath)  # 建立数据库连接
        cu = conn.cursor()
        cu.execute("""
        CREATE TABLE IF NOT EXISTS jfh (
        logtime TIMESTAMP default (datetime('now', 'localtime')), 
        url string, 
        result string             
        );
        """)
        conn.commit()  # 提交更改
        conn.close()  # 关闭数据库连接

    def closeEvent(self, event):
        self.setWindowTitle(self.windowTitle()+' ---- Closing...')
        if len(self.iMacrosThreadList)!=0:
            for thread in self.iMacrosThreadList.values():
                thread.iMacros.iimClose()
                #thread().terminate()
        if len(self.firefoxThreadList)!=0:
            for thread in self.firefoxThreadList.values():
                thread.iMacros.iimClose()
                #thread().terminate()
        if os.path.exists(self.fxProfile_iniPath+'_bak'):
            os.remove(self.fxProfile_iniPath)
            os.rename(self.fxProfile_iniPath+'_bak', self.fxProfile_iniPath)
        self.saveConfig(self.ConfigPath)

    def saveFileDialog(self, flag):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "Support Files (*.txt);;All Files (*)", options=options)
        # if fileName:
        #    if flag=="ProfileSave":
        #        self.saveConfig(fileName)

    def saveConfig(self, filePath):
        debug("saveConfig")
        config = {}
        '''config["Proxy"] = self.ui.lineEdit_Proxy.text()
        config["ProxyEnable"] = self.ui.checkBox_ProxyEnable.isChecked()
        if self.ui.radioButton_ProxyTypeHttp.isChecked():
            config["ProxyType"] = "http"
        elif self.ui.radioButton_ProxyTypeSocks5.isChecked():
            config["ProxyType"] = "socks5"
        else:
            config["ProxyType"] = None'''
        model=self.tableView_threadListModel
        config['tableView_threadListModel']=[]
        for row in range(model.rowCount()):
            rowList=[]
            for column in range(model.columnCount()):
                if column == 1:
                    itemStr='##: ##: ##'
                elif column == 2:
                    itemStr='firefoxNotOpen'
                else:
                    itemObj=model.item(row, column)
                    itemStr=itemObj.text()
                rowList.append(itemStr)
            config['tableView_threadListModel'].append(rowList)
        debug("config['tableView_threadListModel']: "+str(config['tableView_threadListModel']))
        config["DatabasePath"] = self.DatabasePath
        config['debugEnable'] = self.ui.checkBox_debugEnable.isChecked()
        config['stepInterval'] = self.ui.lineEdit_stepInterval.text()
        with open(filePath, 'w') as outfile:
            json.dump(config, outfile)

    def loadConfig(self, filePath):
        with open(filePath, 'r') as f:
            config = json.loads(f.read())
        for row in config['tableView_threadListModel']:
            rowObj=[]
            for rowStr in row:
                rowObj.append(QStandardItem(rowStr))
            self.tableView_threadListModel.appendRow(rowObj)
        '''self.ui.lineEdit_Proxy.setText(config["Proxy"])
        self.ui.checkBox_ProxyEnable.setChecked(config["ProxyEnable"])
        if config["ProxyType"].lower() == "http":
            self.ui.radioButton_ProxyTypeHttp.setChecked(True)
        elif config["ProxyType"].lower() == "socks5":
            self.ui.radioButton_ProxyTypeSocks5.setChecked(True)'''
        self.DatabasePath = config["DatabasePath"]
        self.ui.checkBox_debugEnable.setChecked(config['debugEnable'])
        self.ui.lineEdit_stepInterval.setText(config['stepInterval'])

    def FindLastModifiedFile(self, Directory, FileType):
        list_of_files = glob.glob(Directory + FileType)  # * means all if need specific format then *.csv
        try:
            latest_file = max(list_of_files, key=os.path.getctime)
        except:
            return None
        return latest_file

    # def radioButton_clicked(self,flag):
    #    self.thread.ProxyType=flag

    # def checkBox_isChecked(self):
    #    if self.ui.checkBox_UseProxie.isChecked():
    #        self.ui.groupBox_Proxies.setEnabled(True)
    #    else:
    #        self.ui.groupBox_Proxies.setEnabled(False)

    def thread_pause_resume(self):
        thread = self.iMacrosThreadList[self.fxProfileName]
        if self.ui.pushButton_Pause.text() == "Pause":
            thread.Pause = True
            #self.thread.PauseSubThread()
            self.ui.pushButton_Pause.setText("Resume")
        else:
            thread.Pause = False
            #self.thread.PauseSubThread()
            self.ui.pushButton_Pause.setText("Pause")

    def ThreadControl(self, Trriger):
        if Trriger == "Start":
            thread = iMacrosThread(self)  # 创建一个线程
            thread.threadAttrObj=self.threadAttrObj
            thread.iMacros = self.firefoxThreadList[self.fxProfileName].iMacros
            thread.progress_update.connect(self.HandleProgress)
            thread.start()
            self.iMacrosThreadList[self.fxProfileName]=thread
            self.ui.pushButton_Start.setEnabled(False)
        elif Trriger == "Terminate":
            thread=self.iMacrosThreadList[self.fxProfileName]
            #thread.TerminateSubThread()# terminate SearchResultThread
            thread.iMacros.iimClose()
            thread.terminate()
            #self.ui.progressBar.setValue(0)
            self.ui.pushButton_Start.setEnabled(True)
            self.ui.pushButton_launchFirefox.setEnabled(True)
            for index in sorted(self.ui.tableView_threadList.selectionModel().selectedRows()):
                fxProfileName = self.ui.tableView_threadList.model().data(
                    self.ui.tableView_threadList.model().index(index.row(), 3))
                if fxProfileName==self.fxProfileName:
                    self.tableView_threadListModel.setData(self.ui.tableView_threadList.model().index(index.row(),2), 'firefoxNotOpen')

    def HandleProgress(self, val):
        #debug("val['totalFileNumber']: "+str(val['totalFileNumber']))
        #debug("val['currentSize']: "+str(val['currentSize']))
        if val['type']=='checkCopyProgressThread':
            self.ui.progressBar.setMaximum(val['totalFileNumber'])
            self.ui.progressBar.setValue(val['currentSize'])
        elif val['type']=='iMacrosThread':
            for row in range(self.tableView_threadListModel.rowCount(self.ui.tableView_threadList.rootIndex())):
                fxProfileName = self.ui.tableView_threadList.model().data(self.ui.tableView_threadList.model().index(row, 3))
                if fxProfileName==val['fxProfileName']:
                    self.tableView_threadListModel.setData(self.ui.tableView_threadList.model().index(row,2), val['status'])
                    if val['status']=='runing':
                        self.tableView_threadListModel.setData(self.ui.tableView_threadList.model().index(row, 1),val['otherValue']['countdown'])
                    elif val['status']=='error':
                        self.ui.pushButton_Start.setEnabled(True)

    def LoadFileByLine(self, fileName):
        if os.path.exists(fileName):
            with open(fileName, "r") as f:
                array = f.readlines()
            return array

    def checkBox_isChecked(self):
        if self.ui.checkBox_ProxyEnable.isChecked():
            self.ui.groupBox_Proxy.setEnabled(True)
        else:
            self.ui.groupBox_Proxy.setEnabled(False)

    def openFileNameDialog(self, flag):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Support Files (*.txt *.json);;All Files (*);;Python Files (*.py)",
                                                  options=options)
        if fileName:
            if flag == "KeywordListPath":
                self.MakelistViewLoad(fileName, flag)

    def selectFolderDialog(self, flag):
        root = Tk()
        root.withdraw()  # hide root
        self.queueRulePath = askdirectory(parent=root, initialdir=os.path.dirname(os.path.abspath(__file__)),title='Select Folder') # shows dialog box and return the path
        if flag == 'queueRulePath':
            self.ui.lineEdit_queueRulePath.setText(self.queueRulePath)

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
