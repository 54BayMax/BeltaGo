# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\snake\pyqt\abc.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(843, 600)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.textBrowser = QtGui.QTextBrowser(self.centralWidget)
        self.textBrowser.setGeometry(QtCore.QRect(240, 260, 256, 192))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.label = QtGui.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(240, 230, 54, 12))
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEdit = QtGui.QLineEdit(self.centralWidget)
        self.lineEdit.setGeometry(QtCore.QRect(302, 230, 181, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.pushButton = QtGui.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(250, 470, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.centralWidget)
        self.pushButton_2.setGeometry(QtCore.QRect(400, 470, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(self.centralWidget)
        self.pushButton_3.setGeometry(QtCore.QRect(100, 270, 75, 23))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QtGui.QPushButton(self.centralWidget)
        self.pushButton_4.setGeometry(QtCore.QRect(100, 310, 75, 23))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_5 = QtGui.QPushButton(self.centralWidget)
        self.pushButton_5.setGeometry(QtCore.QRect(100, 350, 75, 23))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_6 = QtGui.QPushButton(self.centralWidget)
        self.pushButton_6.setGeometry(QtCore.QRect(100, 390, 75, 23))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.pushButton_7 = QtGui.QPushButton(self.centralWidget)
        self.pushButton_7.setGeometry(QtCore.QRect(100, 430, 75, 23))
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
        self.pushButton_8 = QtGui.QPushButton(self.centralWidget)
        self.pushButton_8.setGeometry(QtCore.QRect(100, 100, 75, 23))
        self.pushButton_8.setObjectName(_fromUtf8("pushButton_8"))
        self.pushButton_9 = QtGui.QPushButton(self.centralWidget)
        self.pushButton_9.setGeometry(QtCore.QRect(190, 100, 75, 23))
        self.pushButton_9.setObjectName(_fromUtf8("pushButton_9"))
        self.pushButton_10 = QtGui.QPushButton(self.centralWidget)
        self.pushButton_10.setGeometry(QtCore.QRect(270, 100, 75, 23))
        self.pushButton_10.setObjectName(_fromUtf8("pushButton_10"))
        self.pushButton_11 = QtGui.QPushButton(self.centralWidget)
        self.pushButton_11.setGeometry(QtCore.QRect(570, 400, 75, 23))
        self.pushButton_11.setObjectName(_fromUtf8("pushButton_11"))
        self.graphicsView = QtGui.QGraphicsView(self.centralWidget)
        self.graphicsView.setGeometry(QtCore.QRect(520, 50, 256, 192))
        self.graphicsView.setStyleSheet(_fromUtf8("border-image: url(:/test/out.jpg);"))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">abcd</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label.setText(_translate("MainWindow", "name", None))
        self.pushButton.setText(_translate("MainWindow", "yes", None))
        self.pushButton_2.setText(_translate("MainWindow", "print", None))
        self.pushButton_3.setText(_translate("MainWindow", "info", None))
        self.pushButton_4.setText(_translate("MainWindow", "question", None))
        self.pushButton_5.setText(_translate("MainWindow", "critical", None))
        self.pushButton_6.setText(_translate("MainWindow", "about", None))
        self.pushButton_7.setText(_translate("MainWindow", "aboutqt", None))
        self.pushButton_8.setText(_translate("MainWindow", "string", None))
        self.pushButton_9.setText(_translate("MainWindow", "interger", None))
        self.pushButton_10.setText(_translate("MainWindow", "Item", None))
        self.pushButton_11.setText(_translate("MainWindow", "PushButton", None))

import image_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

