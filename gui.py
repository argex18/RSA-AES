# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(676, 479)
        MainWindow.setAnimated(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labels = QtWidgets.QGroupBox(self.centralwidget)
        self.labels.setObjectName("labels")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.labels)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pbk_label = QtWidgets.QLabel(self.labels)
        self.pbk_label.setObjectName("pbk_label")
        self.horizontalLayout_2.addWidget(self.pbk_label)
        self.prk_label = QtWidgets.QLabel(self.labels)
        self.prk_label.setObjectName("prk_label")
        self.horizontalLayout_2.addWidget(self.prk_label)
        self.verticalLayout.addWidget(self.labels)
        self.inputs = QtWidgets.QGroupBox(self.centralwidget)
        self.inputs.setObjectName("inputs")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.inputs)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pbk = QtWidgets.QTextEdit(self.inputs)
        self.pbk.setObjectName("pbk")
        self.horizontalLayout.addWidget(self.pbk)
        self.prk = QtWidgets.QTextEdit(self.inputs)
        self.prk.setObjectName("prk")
        self.horizontalLayout.addWidget(self.prk)
        self.verticalLayout.addWidget(self.inputs)
        self.buttons = QtWidgets.QGroupBox(self.centralwidget)
        self.buttons.setObjectName("buttons")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.buttons)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.mode_button = QtWidgets.QComboBox(self.buttons)
        self.mode_button.setEditable(False)
        self.mode_button.setMaxVisibleItems(2)
        self.mode_button.setObjectName("mode_button")
        self.mode_button.addItem("")
        self.mode_button.addItem("")
        self.horizontalLayout_3.addWidget(self.mode_button)
        self.confirm_button = QtWidgets.QPushButton(self.buttons)
        self.confirm_button.setObjectName("confirm_button")
        self.horizontalLayout_3.addWidget(self.confirm_button)
        self.generate_button = QtWidgets.QPushButton(self.buttons)
        self.generate_button.setObjectName("generate_button")
        self.horizontalLayout_3.addWidget(self.generate_button)
        self.clear_button = QtWidgets.QPushButton(self.buttons)
        self.clear_button.setObjectName("clear_button")
        self.horizontalLayout_3.addWidget(self.clear_button)
        self.verticalLayout.addWidget(self.buttons)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionFile = QtWidgets.QAction(MainWindow)
        self.actionFile.setObjectName("actionFile")

        self.retranslateUi(MainWindow)
        self.mode_button.setCurrentIndex(0)
        self.clear_button.clicked.connect(self.pbk.clear)
        self.clear_button.clicked.connect(self.prk.clear)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Maturita2020"))
        self.labels.setTitle(_translate("MainWindow", "labels"))
        self.pbk_label.setText(_translate("MainWindow", "Public Key"))
        self.prk_label.setText(_translate("MainWindow", "Private Key"))
        self.inputs.setTitle(_translate("MainWindow", "inputs"))
        self.buttons.setTitle(_translate("MainWindow", "buttons"))
        self.mode_button.setCurrentText(_translate("MainWindow", "Encryption"))
        self.mode_button.setItemText(0, _translate("MainWindow", "Encryption"))
        self.mode_button.setItemText(1, _translate("MainWindow", "Decryption"))
        self.confirm_button.setText(_translate("MainWindow", "Confirm"))
        self.generate_button.setText(_translate("MainWindow", "Generate"))
        self.clear_button.setText(_translate("MainWindow", "Clear"))
        self.actionFile.setText(_translate("MainWindow", "File"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
