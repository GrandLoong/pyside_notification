import sys
import os
import time
from os.path import join as pathjoin
import error

try:
    from PySide import QtCore, QtGui
except ImportError:
    raise error.PysideNotFoundError()
from ui_elements.loadui import loadUiType, loadStyleSheet

uiFile = pathjoin(os.path.dirname(__file__), 'ui_elements/notification.ui')
css_file = pathjoin(os.path.dirname(__file__), 'ui_elements/notification.css')
ui_form, ui_base = loadUiType(uiFile)


# The Worker
class WorkThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
    
    def run(self):
        # Bring em in :D
        for i in range(336):
            time.sleep(0.001)
            self.emit(QtCore.SIGNAL('update(QString)'), "ping")
        # Hide u bitch :P
        for j in range(200):
            time.sleep(0.1)
            self.emit(QtCore.SIGNAL('vanish(QString)'), "ping")
        return


class Notification(ui_form, ui_base):
    closed = QtCore.Signal()
    
    def __init__(self, mssg=''):
        super(Notification, self).__init__()
        MSSG = mssg
        self.desktop = QtGui.QDesktopWidget()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.SubWindow)
        self.setupUi(self)
        self.app_dir = os.path.dirname(__file__)
        self.f = 1.0
        self.x = self.desktop.availableGeometry().width()
        self.workThread = WorkThread()
        self.set_transparency(True)
        self.label_icon.setIcon(QtGui.QIcon(self.add_icon('push-notification.png')))
        self.createNotification(MSSG)
    
    
    def add_icon(self, icon_name):
        return pathjoin(self.app_dir, 'ui_elements', icon_name)
    
    def createNotification(self, msg):
        self.lbl_mssg.setText(msg)
        
        # Start Worker
        self.connect(self.workThread, QtCore.SIGNAL("update(QString)"), self.animate)
        self.connect(self.workThread, QtCore.SIGNAL("vanish(QString)"), self.disappear)
        self.connect(self.workThread, QtCore.SIGNAL("finished()"), self.done)
        
        self.workThread.start()
        return
    
    def set_transparency(self, enabled):
        if enabled:
            self.setAutoFillBackground(False)
        else:
            self.setAttribute(QtCore.Qt.WA_NoSystemBackground, False)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, enabled)
        self.repaint()
    
    # Quit when done
    @staticmethod
    def done():
        sys.exit()
    
    # Reduce opacity of the window
    def disappear(self):
        self.f -= 0.005
        self.setWindowOpacity(self.f)
        return
    
    # Move in animation
    def animate(self):
        self.move(self.x,
                  self.desktop.availableGeometry().height() - self.height())
        self.x -= 1
        return


def Notify(msg):
    app = QtGui.QApplication(sys.argv)
    gui = Notification(msg)
    gui.setStyleSheet(loadStyleSheet(css_file))
    gui.show()
    sys.exit(app.exec_())
