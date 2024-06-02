# -*- coding: utf-8 -*-

from maya import OpenMayaUI, cmds
from PySide2 import QtWidgets
from PySide2 import QtCore
from shiboken2 import wrapInstance


class ToolWidget(QtWidgets.QWidget):
    applied = QtCore.Signal()
    closed = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super(ToolWidget, self).__init__(*args, **kwargs)
        mainLayout = QtWidgets.QGridLayout(self)
        self.setLayout(mainLayout)

        self.__scrollWidget = QtWidgets.QScrollArea(self)
        self.__scrollWidget.setWidgetResizable(True)
        self.__scrollWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.__scrollWidget.setMinimumHeight(1)
        mainLayout.addWidget(self.__scrollWidget, 0, 0, 1, 3)

        self.__actionBtn = QtWidgets.QPushButton(self)
        self.__actionBtn.setText('Apply and Close')
        self.__actionBtn.clicked.connect(self.action)
        mainLayout.addWidget(self.__actionBtn, 1, 0)

        applyBtn = QtWidgets.QPushButton(self)
        applyBtn.setText('Apply')
        applyBtn.clicked.connect(self.apply)
        mainLayout.addWidget(applyBtn, 1, 1)

        closeBtn = QtWidgets.QPushButton(self)
        closeBtn.setText('Close')
        closeBtn.clicked.connect(self.close)
        mainLayout.addWidget(closeBtn, 1, 2)

    def action(self):
        self.apply()
        self.close()

    def apply(self):
        self.applied.emit()

    def close(self):
        self.closed.emit()

    def setActionName(self, name):
        self.__actionBtn.setText(name)

    def setOptionWidget(self, widget):
        self.__scrollWidget.setWidget(widget)


class Callback(object):
    def __init__(self, func, *args, **kwargs):
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs

    def __call__(self):
        cmds.undoInfo(openChunk = True)
        try:
            return self.__func(*self.__args, **self.__kwargs)

        except:
            raise

        finally:
            cmds.undoInfo(closeChunk = True)


# OpenMayaUIに、Qtに関する補助機能が用意されています。これはPythonからでも利用できますが、「C++」の
# 「ポインタ※」という機能がPython には無いため、そのままでは使用できません。そこで、C++ で作られた機能
# をPythonから使えるようにしてくれる、PySide付属のモジュール「shiboken」を使用して対応していきます。
# 「shiboken」の中には、「wrapInstance」という機能があり、C++ のポインタの情報をPython で扱えるデータ
# に変換してくれます。コレを使ってポインタからQWidget に変換したデータを、呼び出された場所に「return」を
# 使用して返します。
# 「ポインタ」とは、データがメモリのどこに保存されているか、住所を表すものです。
def getMayaWindow():  # Maya のウィンドウを取得する関数です
    """
    Get the main Maya window as a QtGui.QMainWindow instance
    @return: QtWidgets.QMainWindow instance of the top level Maya windows
    """
    main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
    if main_window_ptr is not None:
        return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)
