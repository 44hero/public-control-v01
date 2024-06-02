# -*- coding: utf-8 -*-

u"""
CustomScriptEditor.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -2.0-
:Date: 2024/05/09

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PySide2 version: 5.15.2

概要(overview):
    - 通称: カスタムスクリプトエディタ(CustomScriptEditor)
    - 型: Union[QMainWindow, TypeOfSubclass]
        QMainWindowクラス または、 その派生クラス(サブクラス) という意味です
詳細(details):
    PySide2.QtWidgets.QMainWindow の、独自規格クラス です。
使用法(usage):
    ::

        # ローカルで作成したモジュール
        import CustomScriptEditor
        reload(CustomScriptEditor)
        from CustomScriptEditor import CustomScriptEditor

        # 以下 e.g.):
        ############################################################
        # カスタムで、専用の スクリプトエディタ を初期化
        self.script_editor = None
        self.statusCurrent_scriptEditor = 'open'

        self.script_editor = CustomScriptEditor(title = 'テストUI',
                                            infoDetail = '伝えたい情報'
                                            )
        self.script_editor.closed.connect(self.on_script_editor_closed)
        self.script_editor.show()


        @Slot()
        def on_script_editor_closed(self):
            message_warning("Script editor was hided. Not closed !!")
            self.statusCurrent_scriptEditor = 'closed'
            return self.statusCurrent_scriptEditor
        ##############################

注意(note):
    ・ 他に必須な独自モジュール
        ::

            # ローカルで作成したモジュール ######################################################
            # shiboken2 独自モジュール
            from YO_utilityTools.TemplateForPySide2.qt import getMayaWindow  # 利用時は、getMayaWindow()

-リマインダ-
    done: 2024/05/08~2024/05/09
        追加と変更と新規1
            - 概要: 引数の追加
            - 詳細:
                ::

                    +   def __init__(self
                                     , title = None
                                     , infoDetail = None
                                     , parent = None, flags = Qt.WindowFlags()
                                     ):
                            ...
                            # 追加と変更と新規1
                            self.infoDetail = infoDetail
                            ...

            - 概要: central_widget に 装飾 を追加
            - 詳細:
                ::

                    +   def _setupUI(self):
                            ...
                            # 追加と変更と新規1
                            # central_widget に 装飾 を追加
                            central_widget.setStatusTip(self.infoDetail)
                            central_widget.setToolTip(self.infoDetail)
                            ...

            - 概要: 基となる closeEvent メソッド 組み込み関数 へのオーバーライド記述 への追加記述
            - 詳細: メインとなるUIとのセットで出現することを想定しているのだが、
                個別にUIを誤って閉じてしまった場合等、エラー回避を主な目的とした、ｺｰﾄﾞ修正と追加
                ::

                    +   def closeEvent(self, event):
                            ...
                            # 追加と変更と新規1
                            # ウィンドウを非表示にする
                            self.hide()

                            # 追加と変更と新規1
                            event.ignore()
        version = '-2.0-'

    done: 2024/04/28
        新規作成

        version = '-1.0-'
"""

# 標準ライブラリ #################################################################

# サードパーティライブラリ #########################################################
from PySide2.QtWidgets import (QAction, QApplication, QMainWindow,
                               QMenu, QTextEdit, QWidget,
                               QVBoxLayout,
                               )
from PySide2.QtCore import Qt, Signal

# ローカルで作成したモジュール ######################################################
# shiboken2 独自モジュール
from ..TemplateForPySide2.qt import getMayaWindow  # 利用時は、getMayaWindow()


class CustomScriptEditor(QMainWindow):
    closed = Signal()  # ウィンドウが閉じられたときにシグナルを送信する設定

    def __init__(self
                 , title = None
                 , infoDetail = None
                 , parent = None, flags = Qt.WindowFlags()
                 ):
        if parent is None:
            parent = getMayaWindow()

        # super(CustomScriptEditor, self).__init__(parent, flags)
        super().__init__(parent, flags)

        self.size = (100, 900, 800, 200)  # 100, 100, 800, 600
        self.title = title
        self.win = self.title + '_ui'
        # 追加と変更と新規1
        self.infoDetail = infoDetail

        self._windowBasicSettings()
        self._setupUI()
        self._createContextMenu()

    def _duplicateWindowAvoidFunction(self, winName):
        widgets = QApplication.allWidgets()
        for w in widgets:
            if w.objectName() == winName:
                w.deleteLater()

    def _windowBasicSettings(self):
        self.setWindowTitle(self.title)
        if not self.isVisible():
            self.setGeometry(*self.size)
        self._duplicateWindowAvoidFunction(self.win)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setObjectName(self.win)

    def _setupUI(self):
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)  # 読み取り専用に設定

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)

        central_widget = QWidget()
        # 追加と変更と新規1
        # central_widget に 装飾 を追加
        central_widget.setStatusTip(self.infoDetail)
        central_widget.setToolTip(self.infoDetail)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 本来ならば、self.show() は必要ですが、
        # 読み込まれている先で、
        # self.script_editor.show() 等と記述するので、ここでは不要にしています。
        # self.show()

    def _createContextMenu(self):
        self.text_edit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text_edit.customContextMenuRequested.connect(self.showContextMenu)
        self.context_menu = QMenu(self)

        self.select_all_action = QAction("Select All", self)
        self.select_all_action.triggered.connect(self.selectAll)
        self.context_menu.addAction(self.select_all_action)

        self.copy_action = QAction("Copy", self)
        self.copy_action.triggered.connect(self.copyText)
        self.context_menu.addAction(self.copy_action)

        self.clear_action = QAction("Clear Output", self)
        self.clear_action.triggered.connect(self.clearOutput)
        self.context_menu.addAction(self.clear_action)

    def showContextMenu(self, pos):
        self.context_menu.exec_(self.text_edit.mapToGlobal(pos))

    def selectAll(self):
        self.text_edit.selectAll()

    def copyText(self):
        cursor = self.text_edit.textCursor()
        selected_text = cursor.selectedText()
        clipboard = QApplication.clipboard()
        clipboard.setText(selected_text)

    def clearOutput(self):
        self.text_edit.clear()

    # メソッド
    # テキストを追加する
    def append_text(self, text):
        self.text_edit.append(text)

    def append_warning(self, text):
        self.append_with_color(text, 'yellow')

    def append_error(self, text):
        self.append_with_color(text, 'red')

    def append_default(self, text):
        self.append_with_color(text, 'lime')

    def append_default2(self, text):
        self.append_text(text)

    def append_with_color(self, text, color):
        self.text_edit.append(f"<font color='{color}'>{text}</font>")

    # オーバーライド
    # closeEvent メソッド 組み込み関数
    def closeEvent(self, event):
        u""" < (オーバーライド) closeEvent メソッド 組み込み関数 です >

        オーバーライド

        .. note::
            当該 closeEvent メソッド は、基は組み込み関数であり、 イベントハンドラー です
                閉じる要求を受信したときにトップレベル ウィンドウに対してのみ呼び出されます
            self.close でも発動します
        """
        # ウィンドウが閉じられたときにシグナルを送信
        self.closed.emit()
        # super(CustomScriptEditor, self).closeEvent(event)

        # 追加と変更と新規1
        # ウィンドウを非表示にする
        self.hide()

        # 追加と変更と新規1
        # イベントを無視してウィンドウを閉じないようにする
        # イベントがまだ完全には処理されていないことを示します。
        # これは、例えばウィジェットがクリックイベントを部分的にしか処理しない場合や、イベントを無視して親ウィジェットに伝播させたい場合に使用
        event.ignore()

        # イベントを無視してウィンドウを閉じないようにする
        # イベントが適切に処理され、それ以上の処理は必要ないことを示します。
        # これは、例えばウィジェットがクリックイベントを処理し、それ以上の処理（例えば親ウィジェットへのイベントの伝播）は必要ない場合に使用
        # event.accept()


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
    # cse = CustomScriptEditor(title = 'test', infoDetail = 'test')
    # cse.show()
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
