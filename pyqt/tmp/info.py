# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""

from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature

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
        print "tool3"
    
    @pyqtSignature("")
    def on_toolButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        print "ok"
    
    @pyqtSignature("")
    def on_toolButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        print "cancel"
    
    @pyqtSignature("")
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSignature("")
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
