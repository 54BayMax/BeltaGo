# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui
from PyQt4 import *
from Ui_abc import Ui_MainWindow
import sys
import webbrowser
import time

from Ui_info import Ui_Dialog

class Dialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
    
    @pyqtSignature("")
    def on_toolButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        input, ok=QInputDialog.getText(self, u'String', u'请输入', QLineEdit.Normal, u'信息')
        print u'%s'%input
    
    @pyqtSignature("")
    def on_toolButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        input, ok=QInputDialog.getInteger(self, u'String', u'请输入', QLineEdit.Normal, 0, 100)
        print unicode(input)
    
    @pyqtSignature("")
    def on_toolButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        input, ok=QInputDialog.getInteger(self, u'String', u'请输入', QLineEdit.Normal, 0, 100)
        print unicode(input)
    
    @pyqtSignature("")
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        print "ok"
        self.close()
    
    @pyqtSignature("")
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        print "cancel"

    
    @pyqtSignature("")
    def on_pushButton_11_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSignature("")
    def on_pushButton_12_clicked(self):
        """
        Slot documentation goes here.
        """
        
        # TODO: not implemented yet
        pass

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.graphicsView.mousePressEvent=self.my_click
    
    def my_click(self, e):
        webbrowser.open('www.baidu.com')
        
    @pyqtSignature("")
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        txt1=self.lineEdit.text()
        self.lineEdit.setObjectName(txt1)
        txt2=self.textBrowser.toPlainText()
        print u'%s'%txt1, '\n',unicode(txt2)
        # TODO: not implemented yet
       
    @pyqtSignature("")
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        self.textBrowser.append(self.lineEdit.text())
        # TODO: not implemented yet
        
        
    
    @pyqtSignature("int")
    def on_dial_valueChanged(self, value):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.lcdNumber.display(value)


    
    @pyqtSignature("int")
    def on_horizontalSlider_valueChanged(self, value):
        """
        Slot documentation goes here.
        """
        self.lcdNumber.display(value)
    
    @pyqtSignature("int")
    def on_verticalSlider_valueChanged(self, value):
        """
        Slot documentation goes here.
        """
        self.lcdNumber.display(value)
       
            
    @pyqtSignature("")
    def on_pushButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        QMessageBox.information(self, u'提醒', u'这是帅哥')
    
    @pyqtSignature("")
    def on_pushButton_4_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        QMessageBox.question(self, u'这是一个询问', 'OK', 'Cancel')
    
    @pyqtSignature("")
    def on_pushButton_5_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        QMessageBox.critical(self, u'这是一个警告', u'lll')
    
    @pyqtSignature("")
    def on_pushButton_6_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        QMessageBox.about(self, u'这是一个关于', u'lllzzz')
    
    @pyqtSignature("")
    def on_pushButton_7_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        QMessageBox.aboutQt(self, u'关于Qt')
        

    
    @pyqtSignature("")
    def on_pushButton_8_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        input, ok=QInputDialog.getText(self, u'String', u'请输入', QLineEdit.Normal, u'信息')
        print u'%s'%input
    
    @pyqtSignature("")
    def on_pushButton_9_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        
        input, ok=QInputDialog.getInteger(self, u'String', u'请输入', QLineEdit.Normal, 0, 100)
        print unicode(input)
    
    @pyqtSignature("")
    def on_pushButton_10_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        my_list=QStringList()
        my_list.append(u'苹果')
        my_list.append(u'香蕉')
        input, ok=QInputDialog.getItem(self, u'String', u'请输入', my_list)
        print unicode(input)
        
    @pyqtSignature("")
    def on_pushButton_11_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        myinfo=Dialog()
        myinfo.exec_()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    splash=QSplashScreen(QPixmap("qq.jpg"))
    splash.show()
    splash.showMessage(u'正在启动资源...',Qt.AlignCenter,Qt.red)
    time.sleep(2)
    splash.showMessage(u'正在加载音频资源...',Qt.AlignCenter,Qt.red)
    time.sleep(2)
    app.processEvents()
    ui = MainWindow()
    ui.show()
    splash.finish(ui)
    sys.exit(app.exec_())
