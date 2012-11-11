#!/usr/bin/env python

import sys,os
from PyQt4 import QtGui, QtCore

class Main(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        # Default values: self.brightness = 65535 and self.gamma = 1.0
        self.settings = QtCore.QSettings("www.michielovertoom.com", "qtbrightness")
        self.brightness, _ = self.settings.value("brightness", 65535).toInt()
        self.brightness = max(self.brightness, 10000) # Not too dark.
        self.gamma, _ = self.settings.value("gamma", 1000).toInt()
        if self.gamma == 0:
            self.gamma = 1000
        self.gamma = max(self.gamma, 100)
        self.gammafloat =  float(self.gamma)/1000.0
        self.changed = True

        self.grid=QtGui.QGridLayout(self)

        self.brilabel=QtGui.QLabel(self)
        self.brilabel.setText("brightness")
        self.grid.addWidget(self.brilabel, 0, 0)

        self.brivaluelabel=QtGui.QLabel(self)
        self.brivaluelabel.setText(str(self.brightness))
        self.grid.addWidget(self.brivaluelabel, 0, 4)

        self.gamlabel=QtGui.QLabel(self)
        self.gamlabel.setText("gamma")
        self.grid.addWidget(self.gamlabel, 1, 0)

        self.gamvaluelabel=QtGui.QLabel(self)
        self.gamvaluelabel.setText("%.2f" % self.gammafloat)
        self.grid.addWidget(self.gamvaluelabel, 1, 4)

        self.grid.setColumnMinimumWidth(1,12)
        self.grid.setColumnMinimumWidth(3,12)

        self.brislider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.grid.addWidget(self.brislider, 0,2)
        # self.brislider.setFocusPolicy(QtCore.Qt.NoFocus) # Prettier, but loses keyboard control.
        self.brislider.setRange(0, 65535)
        self.brislider.setValue(self.brightness)
        self.brislider.setSingleStep(8192)
        self.brislider.setPageStep(8192)
        self.connect(self.brislider, QtCore.SIGNAL("valueChanged(int)"), self.change_brightness)

        self.gamslider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.grid.addWidget(self.gamslider, 1,2)
        # self.gamslider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.gamslider.setRange(0, 10000)
        self.gamslider.setValue(self.gamma)
        self.gamslider.setSingleStep(100)
        self.gamslider.setPageStep(100)
        self.connect(self.gamslider, QtCore.SIGNAL("valueChanged(int)"), self.change_gamma)

        self.timer = QtCore.QBasicTimer()
        self.timer.start(1000, self)
        self.timerEvent(None)

        self.setWindowTitle("Brightness and gamma")
        self.setGeometry(100, 100, 400, 150)

    def change_brightness(self, event):
        self.brightness = self.brislider.value()
        self.settings.setValue("brightness", self.brightness);
        self.brivaluelabel.setText("%.5d" % self.brightness)
        self.changed = True

    def change_gamma(self, event):
        self.gamma = self.gamslider.value()
        self.gammafloat = float(self.gamma)/1000.0
        self.settings.setValue("gamma", self.gamma);
        self.gamvaluelabel.setText("%.2f" % self.gammafloat)
        self.changed = True

    def timerEvent(self, event):
        if self.changed:
            self.changed = False
            os.system("xbrightness %d %f" % (self.brightness, self.gammafloat))

app = QtGui.QApplication(sys.argv)
main = Main()
main.show()
app.exec_()
