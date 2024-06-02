# -*- coding: utf-8 -*-

from maya import OpenMayaUI, cmds
from PySide2 import QtWidgets, QtCore, QtGui
import shiboken2

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
    @return: QtGui.QMainWindow instance of the top level Maya windows
    """
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    if ptr is not None:
        widget = shiboken2.wrapInstance(long(ptr), QtWidgets.QMainWindow)
        return widget
