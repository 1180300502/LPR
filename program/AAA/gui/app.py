from PyQt5.QtWidgets import QApplication
from AAA.gui.fream import MainForm
import sys
class APP(QApplication):
    def __init__(self):
        super(APP,self).__init__(sys.argv)
        self.dlg=MainForm()
        self.dlg.show()

