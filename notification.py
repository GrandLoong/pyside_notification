import sys
import os
from os.path import join as pathjoin
from PySide import QtCore, QtGui
import time
from ui_elements.loadui import loadUiType, loadStyleSheet

uiFile = pathjoin(os.path.dirname(__file__), 'resources/not.ui')
ui_form, ui_base = loadUiType(uiFile)


class Notification(ui_form, ui_base):
    closed = QtCore.Signal()
    
    def __init__(self, mssg=''):
        super(Notification, self).__init__()
        MSSG = mssg
        self.desktop = QtGui.QDesktopWidget()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.SubWindow)
        self.setupUi(self)
        
        self.createNotification(MSSG)
    
    def closeEvent(self, event):
        self.close.emit()
    
    def createNotification(self, mssg):
        self.x = self.desktop.availableGeometry().width()
        
        # Set the opacity
        self.f = 1.0
        
        # Set the message
        self.lbl_mssg.setText(mssg)
        
        # Start Worker
        self.workThread = WorkThread()
        self.connect(self.workThread, QtCore.SIGNAL("update(QString)"), self.animate)
        self.connect(self.workThread, QtCore.SIGNAL("vanish(QString)"), self.disappear)
        self.connect(self.workThread, QtCore.SIGNAL("finished()"), self.done)
        
        self.workThread.start()
        return
    
    # Quit when done
    def done(self):
        self.hide()
        return
    
    # Reduce opacity of the window
    def disappear(self):
        self.f -= 0.02
        self.setWindowOpacity(self.f)
        return
    
    # Move in animation
    def animate(self):
        self.move(self.x,
                  self.desktop.availableGeometry().height() - self.height())
        self.x -= 1
        return


# The Worker
class WorkThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
    
    def run(self):
        # Bring em in :D
        for i in range(336):
            time.sleep(0.0001)
            self.emit(QtCore.SIGNAL('update(QString)'), "ping")
        # Hide u bitch :P
        for j in range(50):
            time.sleep(0.1)
            self.emit(QtCore.SIGNAL('vanish(QString)'), "ping")
        return


def Notify(msg):
    app = QtGui.QApplication(sys.argv)
    myapp = Notification(msg)
    myapp.show()
    sys.exit(app.exec_())
