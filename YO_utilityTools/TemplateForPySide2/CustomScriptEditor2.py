# -*- coding: utf-8 -*-

u"""
CustomScriptEditor2.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -2.5-
:Date: 2024/05/24

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PySide2 version: 5.15.2

概要(overview):
    CustomScriptEditor2.py シングルトン ScriptEditor2 です。
        - 通称: CustomScriptEditor2
        -
詳細(details):
    - シングルトンパターン とは
        シングルトンパターンは、ソフトウェア設計パターンの一つで、
            特定のクラスのインスタンスが常に一つだけ存在することを保証する方法です。
                このパターンは、アプリケーション内で特定のリソースに対する
                    一意のアクセスポイントを提供する必要がある場合に特に便利です。

        シングルトンパターンを実装するには、通常、以下の要素が含まれます：

        - プライベートなコンストラクタ:
            クラスのインスタンス化を制限し、外部から新しいインスタンスを生成できないようにします。
        - 静的なメンバ変数:
            唯一のインスタンスを保持するための静的なメンバ変数がクラス内に定義されます。
        - 静的なメソッド:
            唯一のインスタンスにアクセスするための静的なメソッドが提供されます。
                このメソッドは常に同じインスタンスを返します。

        Pythonでは、シングルトンを実装する方法がいくつかありますが、
            最も一般的な方法はクラス変数やデコレータを使う方法です。

        例えば、以下のように実装します。
        ::


            class Singleton:
                _instance = None

                def __new__(cls):
                    if cls._instance is None:
                        cls._instance = super().__new__(cls)
                    return cls._instance

            # 以下はテストコード
            s1 = Singleton()
            s2 = Singleton()

            print(s1 is s2)  # True

    - @Slot()デコレータ とは
        また、当モジュールの使用先の close を持つメソッド に、
            @Slot()デコレータで装飾します。
                これは、CustomScriptEditor2クラス の closedシグナル が発生したとき
                    （つまり、ウィンドウが閉じられたとき）に
                        呼び出されることを意味します。
        @Slot()デコレータがなくても、関数は通常通りに動作します。
            しかし、@Slot()デコレータを使用すると、Qtのシグナルとスロットメカニズムが最適化され、
                パフォーマンスが向上する可能性があります。
            したがって、シグナルとスロットを頻繁に使用する場合や、パフォーマンスが重要な場合には、
                @Slot()デコレータを使用することをお勧めします。
            ただし、この最適化は通常、大規模なアプリケーションでのみ顕著になります。
                小規模なアプリケーションでは、@Slot()デコレータの有無がパフォーマンスに
                    大きな影響を与えることは少ないでしょう。
        したがって、@Slot()デコレータを削除しても、
            当モジュールの使用先の on_scriptEditor2_closedメソッド は引き続き
                closedシグナルに応答します。
                    ただし、パフォーマンスの最適化が失われる可能性があります。
                        それが許容範囲であれば、@Slot()デコレータを削除することも可能です。
            ただし、一般的には、シグナルとスロットメカニズムを使用する場合、
                関連するメソッドに@Slot()デコレータを適用することが推奨されます。

使用法(usage):
    ::

        # -*- coding: utf-8 -*-
        from .CustomScriptEditor2 import CustomScriptEditor2

        # e.g.):
        _title = 'test'
        _infoDetail = 'test'
        custom_scriptEditor2_instance = CustomScriptEditor2(title = _title,
                                                            infoDetail = _infoDetail
                                                            )

注意(note):
    ・ 他に必須な独自モジュール
        ::

            # ローカルで作成したモジュール ######################################################
            from ..lib.message import message
            # shiboken2 独自モジュール
            from ..TemplateForPySide2.qt import getMayaWindow  # 利用時は、getMayaWindow()

-リマインダ-
    done: 2024/05/21~2024/05/24
        - 修正2 追加2 新規2
            - 概要: 文字列の検索機能に必要な要素を付加
            - 詳細:
                ::

                    class SearchDialog(QDialog):
                        ...
                    +   def accept(self):
                            ...

                    class CustomScriptEditor2(QMainWindow):
                        ...
                    +   def __init__(self
                                         , title = None
                                         , infoDetail = None
                                         , parent = None, flags = Qt.WindowFlags()
                                         ):
                            ...
                            # 追加2
                            self.last_search_text = ''  # 前回の検索文字列を保持
                            ...
                            # 追加2
                            self.search_results = []  # 検索結果の位置を保持するリスト
                            self.current_search_index = -1  # 現在の検索結果のインデックス
                            self.search_dialog = None  # 検索ダイアログのインスタンスを保持
                            self.installEventFilter(self)  # イベントフィルターをインストール
                            ...

                    +   def _setupShortcuts(self):
                            ...
                            self.search_action.triggered.connect(self.copySelectedTextToSearchField)
                            ...

                    +   def searchText(self):
                            ...

                    +   def highlightSearchText(self, search_text, highlight_color):
                            ...

                    +   def resetHighlights(self):
                            ...

                    +   def moveToSearchResult(self, index):
                            ...

                    +   def copySelectedTextToSearchField(self):
                            ...

                    +   def eventFilter(self, source, event):
                            ...

                    +   def mouseReleaseEvent(self, event):
                            ...
        version = '-2.5-'

    done: 2024/05/20
        - 修正1
            - 概要: 文字列の検索機能を設置
        version = '-2.0-'

    done: 2024/05/10~2024/05/17
        新規作成

        version = '-1.0-'
"""

# 標準ライブラリ #################################################################
from typing import Any

# サードパーティライブラリ #########################################################
from PySide2.QtWidgets import (QAction, QApplication, QColorDialog, QDialog,
                               QLabel, QLineEdit, QMainWindow, QMenu,
                               QPushButton, QTextEdit, QWidget, QVBoxLayout,
                               )
from PySide2.QtCore import QEvent, Qt, Signal
from PySide2.QtGui import QBrush, QColor, QFont, QTextCharFormat, QTextCursor

# ローカルで作成したモジュール ######################################################
from ..lib.message import message
# from ..lib.message_warning import message_warning
# shiboken2 独自モジュール
from ..TemplateForPySide2.qt import getMayaWindow  # 利用時は、getMayaWindow()


# 検索ダイアログの作成
class SearchDialog(QDialog):
    def __init__(self, parent = None
                 , initial_text = '', initial_color = Qt.yellow
                 ):
        super().__init__(parent)

        self.setWindowTitle("Search")
        self.setFixedSize(300, 150)

        self.search_label = QLabel("Enter text to search:")
        self.search_input = QLineEdit()
        self.search_input.setText(initial_text)

        self.search_text = initial_text

        # self.color_label = QLabel("Select highlight color:")
        # self.color_button = QPushButton("Choose Color")
        # self.color_button.clicked.connect(self.chooseColor)
        self.highlight_color = initial_color

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.search_label)
        layout.addWidget(self.search_input)
        # layout.addWidget(self.color_label)
        # layout.addWidget(self.color_button)
        layout.addWidget(self.search_button)
        self.setLayout(layout)

        # Enterキーが押されたときにacceptメソッドを呼び出す
        self.search_input.returnPressed.connect(self.accept)

    # def chooseColor(self):
    #     color = QColorDialog.getColor(initial = self.highlight_color)
    #     if color.isValid():
    #         self.highlight_color = color

    def get_search_text(self):
        return self.search_input.text()

    def get_highlight_color(self):
        return self.highlight_color

    def setInitialText(self, text):
        self.search_text = text
        # テキストも更新するようにしました。
        # これにより、ダイアログが再表示されたときに初期テキストが適切に反映されます。
        self.search_input.setText(text)

    # def exec_(self):
    #     return super().exec_()

    # 新規2
    # acceptメソッドが呼び出されたとき
    # （つまり、検索ボタンがクリックされたときやEnterキーが押されたとき）
    # に、検索フィールドのテキストをハイライトするようにすることができます。
    def accept(self):
        search_text = self.get_search_text()
        self.parent().highlightSearchText(search_text, self.get_highlight_color())
        super().accept()


class CustomScriptEditor2(QMainWindow):
    closed = Signal()  # ウィンドウが閉じられたときにシグナルを送信する設定
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self
                 , title = None
                 , infoDetail = None
                 , parent = None, flags = Qt.WindowFlags()
                 ):
        if parent is None:
            parent = getMayaWindow()

        # super(CustomScriptEditor2, self).__init__(parent, flags)
        super().__init__(parent, flags)

        self.size = (100, 300, 400, 800)  # 100, 100, 800, 600 / 100, 900, 800, 200
        self.title = title
        self.win = self.title + '_ui'
        # 追加と変更と新規1
        self.infoDetail = infoDetail

        self.default_font_size = 10
        self.setFont(QFont("Arial", self.default_font_size))

        self.colors = ['black', 'darkslategrey', 'dimgrey', 'grey'
            , 'lightslategrey', 'slategrey', 'darkgrey', 'lightgray'
            , 'powderblue'  # total: 9, index: 0-8
                       ]  # 色のリスト
        self.current_color_index = 0
        # self.setStyleSheet(f"background-color: {self.colors[self.current_color_index]};")

        self.ctrl_pressed = False  # Ctrlキーが押されているかどうかを管理する変数
        self.alt_pressed = False  # Altキーが押されているかどうかを管理する変数

        # 追加2
        self.last_search_text = ''  # 前回の検索文字列を保持

        highlightColorList = [
            Qt.black,         # 0
            Qt.white,         # 1
            Qt.red,           # 2
            Qt.green,         # 3
            Qt.blue,          # 4
            Qt.cyan,          # 5
            Qt.magenta,       # 6
            Qt.gray,          # 7
            Qt.darkRed,       # 8
            Qt.darkGreen,     # 9
            Qt.darkBlue,      # 10
            Qt.darkCyan,      # 11
            Qt.darkMagenta,   # 12
            Qt.darkGray,      # 13
            Qt.lightGray,     # 14
            Qt.transparent    # 15
            ]  # Qt モジュールの色リスト
        # start: yellow, gray, darkCyan, darkGray
        self.highlight_color = highlightColorList[12]  # ハイライト色を保持: Qt.darkMagenta

        # 追加2
        self.search_results = []  # 検索結果の位置を保持するリスト
        self.current_search_index = -1  # 現在の検索結果のインデックス
        self.search_dialog = None  # 検索ダイアログのインスタンスを保持
        self.installEventFilter(self)  # イベントフィルターをインストール

        self._windowBasicSettings()
        self._setupUI()
        self._createContextMenu()
        self._setupShortcuts()  # ショートカットの設定

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
        # 追加2 変更2 新規2
        self.text_edit.setStyleSheet(f"background-color: {self.colors[self.current_color_index]};")

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)

        central_widget = QWidget()
        # 追加と変更と新規1
        # central_widget に 装飾 を追加
        central_widget.setStatusTip(self.infoDetail)
        central_widget.setToolTip(self.infoDetail)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # self.show()

    def _createContextMenu(self):
        self.text_edit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text_edit.customContextMenuRequested.connect(self.showContextMenu)
        self.context_menu = QMenu(self)

        self.select_all_action = QAction("Select All", self)
        self.select_all_action.setStatusTip('出力内容を全て選択します')
        self.select_all_action.setToolTip('出力内容を全て選択します')
        self.select_all_action.triggered.connect(self.selectAll)
        self.context_menu.addAction(self.select_all_action)

        self.copy_action = QAction("Copy", self)
        self.copy_action.setStatusTip('出力内容を任意選択でCopyします')
        self.copy_action.setToolTip('出力内容を任意選択でCopyします')
        self.copy_action.triggered.connect(self.copyText)
        self.context_menu.addAction(self.copy_action)

        self.clear_action = QAction("Clear Output", self)
        self.clear_action.setStatusTip('出力内容を全てｸﾘｱｰします')
        self.clear_action.setToolTip('出力内容を全てｸﾘｱｰします')
        self.clear_action.triggered.connect(self.clearOutput)
        self.context_menu.addAction(self.clear_action)

        # セパレータの追加
        self.context_menu.addSeparator()

        # 検索アクションの追加
        self.search_action = QAction("Search", self)
        self.search_action.setStatusTip('検索窓を用いて任意の文字列を検索します')
        self.search_action.setToolTip('検索窓を用いて任意の文字列を検索します')
        self.search_action.triggered.connect(self.searchText)
        self.context_menu.addAction(self.search_action)
        # 検索アクション 次 の追加
        self.next_result_action = QAction("Next", self)
        self.next_result_action.setEnabled(False)
        self.next_result_action.setStatusTip('任意の文字列を順に選択します')
        self.next_result_action.setToolTip('任意の文字列を順に選択します')
        self.next_result_action.triggered.connect(self.nextSearchResult)
        self.context_menu.addAction(self.next_result_action)
        # 検索アクション 前 の追加
        self.prev_result_action = QAction("Prev", self)
        self.prev_result_action.setEnabled(False)
        self.prev_result_action.setStatusTip('任意の文字列を逆順に選択します')
        self.prev_result_action.setToolTip('任意の文字列を逆順に選択します')
        self.prev_result_action.triggered.connect(self.prevSearchResult)
        self.context_menu.addAction(self.prev_result_action)
        # 検索アクション 検索のクリアー の追加
        self.searchClear_action = QAction("Search Clear", self)
        self.searchClear_action.setEnabled(True)
        self.searchClear_action.setStatusTip('中ﾎﾞﾀﾝﾀﾞﾌﾞﾙｸﾘｯｸ で検索をｸﾘｱｰ出来ます')
        self.searchClear_action.setToolTip('中ﾎﾞﾀﾝﾀﾞﾌﾞﾙｸﾘｯｸ で検索をｸﾘｱｰ出来ます')
        # self.searchClear_action.triggered.connect(self.prevSearchResult)
        self.context_menu.addAction(self.searchClear_action)

    def _setupShortcuts(self):
        # ショートカットの設定
        self.search_action.setShortcut("Ctrl+F")
        self.search_action.triggered.connect(self.copySelectedTextToSearchField)
        self.addAction(self.search_action)

        # self.next_result_action = QAction(self)
        self.next_result_action.setShortcut("F3")
        # self.next_result_action.triggered.connect(self.nextSearchResult)
        self.addAction(self.next_result_action)

        # self.prev_result_action = QAction(self)
        self.prev_result_action.setShortcut("Shift+F3")
        # self.prev_result_action.triggered.connect(self.prevSearchResult)
        self.addAction(self.prev_result_action)

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

    def searchText(self):
        # searchText メソッド内で、既存の検索ダイアログが存在するかどうかをチェックし、
        # 存在しない場合は新しい検索ダイアログを作成します
        if self.search_dialog is None:
            self.search_dialog = SearchDialog(self,
                                              initial_text=self.last_search_text,
                                              initial_color=self.highlight_color)
        else:
            self.search_dialog.setInitialText(self.last_search_text)
            self.search_dialog.activateWindow()
        self.search_dialog.show()

    def highlightSearchText(self, search_text, highlight_color):
        self.search_results.clear()
        self.current_search_index = -1

        cursor = self.text_edit.textCursor()
        document = self.text_edit.document()

        cursor.beginEditBlock()

        self.resetHighlights()

        cursor.endEditBlock()

        cursor.beginEditBlock()
        highlight_format = QTextCharFormat()
        highlight_format.setBackground(QBrush(highlight_color))

        pos = 0
        search_length = len(search_text)
        while True:
            pos = self.text_edit.toPlainText().find(search_text, pos)
            if pos == -1:
                break

            cursor.setPosition(pos)
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, search_length)

            current_format = cursor.charFormat()
            current_format.setBackground(QBrush(highlight_color))
            cursor.setCharFormat(current_format)

            self.search_results.append((pos, search_length))  # 検索結果の位置と長さを保存
            pos += search_length

        cursor.endEditBlock()

        # if self.search_results:
        #     self.current_search_index = 0
        #     self.moveToSearchResult(self.current_search_index)

        # 検索結果が存在する場合、NextとPrevのアクションを有効化
        if self.search_results:
            self.current_search_index = 0
            self.moveToSearchResult(self.current_search_index)
            self.next_result_action.setEnabled(True)
            self.prev_result_action.setEnabled(True)
        else:
            self.next_result_action.setEnabled(False)
            self.prev_result_action.setEnabled(False)

    def resetHighlights(self):
        cursor = self.text_edit.textCursor()
        document = self.text_edit.document()

        cursor.setPosition(0)
        while cursor.position() < document.characterCount() - 1:
            cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
            current_format = cursor.charFormat()
            current_format.setBackground(QBrush(Qt.transparent))
            cursor.setCharFormat(current_format)
            cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.MoveAnchor)

    def moveToSearchResult(self, index):
        if 0 <= index < len(self.search_results):
            cursor = self.text_edit.textCursor()
            pos, length = self.search_results[index]
            cursor.setPosition(pos)
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, length)
            self.text_edit.setTextCursor(cursor)
            self.text_edit.ensureCursorVisible()

    def nextSearchResult(self):
        if self.search_results:
            self.current_search_index = (self.current_search_index + 1) % len(self.search_results)
            self.moveToSearchResult(self.current_search_index)

    def prevSearchResult(self):
        if self.search_results:
            self.current_search_index = (self.current_search_index - 1) % len(self.search_results)
            self.moveToSearchResult(self.current_search_index)

    # メソッド
    # テキストを追加する
    # def append_text(self, text: Any):
    #     """
    #
    #     :param Any text: str で無いことに注意
    #     """
    #     self.text_edit.append(text)

    def append_warning(self, text: Any):
        """

        :param Any text: str で無いことに注意
        """
        self.append_with_color(text, 'yellow')

    def append_error(self, text: Any):
        """

        :param Any text: str で無いことに注意
        """
        # 候補: red, orangered, lightcoral, indianred
        self.append_with_color(text, 'lightcoral')

    def append_default(self, text: Any):
        """

        :param Any text: str で無いことに注意
        """
        self.append_with_color(text, 'white')

    def append_default2(self, text: Any):
        """

        :param Any text: str で無いことに注意
        """
        self.append_with_color(text, 'lime')

    # def append_default_test(self, text: Any):
    #     """
    #
    #     :param Any text: str で無いことに注意
    #     """
    #     self.append_text(text)

    def append_with_color(self, text: Any, color: str):
        """

        :param Any text: str で無いことに注意
        :param str color:
        """
        # textが文字列でない場合、文字列に変換
        if not isinstance(text, str):
            text = str(text)

        # 改行とタブの文字列をHTML対応に置き換える
        text = text.replace('\n', '<br>').replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;')
        # self.text_edit.setHtml(f"<font color='{color}'>{text}</font>")  # start

        # 指定された色でテキストをHTML形式で追加
        self.text_edit.append(f"<font color='{color}'>{text}</font>")  # start
        # self.text_edit.append(f"<font color='{color}' size='{4}'>{text}</font>")

    # オーバーライド
    # wheelEvent メソッド 組み込み関数
    def wheelEvent(self, event):
        u""" < (オーバーライド) wheelEvent メソッド 組み込み関数 です >

        オーバーライド

        .. note::
            当該 wheelEvent メソッド は、基は組み込み関数であり、 イベントハンドラー です
                Ctrl + マウスホイールで 呼び出される
                    仕様です
            ウスホイールを上にスクロールすると文字サイズが増え、
                下にスクロールすると文字サイズが減ります。
                    ただし、これはCtrlキーが押されているときだけ有効です。
                        Ctrlキーが押されていない場合、マウスホイールは通常通りに動作します。
        """
        if self.ctrl_pressed:  # Ctrlキーが押されている場合のみ処理を行う
            delta = event.angleDelta().y()
            if delta > 0:
                self.default_font_size += 1
            elif delta < 0 and self.default_font_size > 1:
                self.default_font_size -= 1
            self.setFont(QFont("Arial", self.default_font_size))
        else:
            super().wheelEvent(event)

    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Control:
    #         self.ctrl_pressed = True
    #     elif event.key() == Qt.Key_Alt:
    #         self.alt_pressed = True
    #     elif event.key() == Qt.Key_B and self.alt_pressed:  # Altキーが押されている場合のみ処理を行う
    #         self.current_color_index = (self.current_color_index + 1) % len(self.colors)
    #         self.setStyleSheet(f"background-color: {self.colors[self.current_color_index]};")
    #     super().keyPressEvent(event)
    #
    # def keyReleaseEvent(self, event):
    #     if event.key() == Qt.Key_Control:
    #         self.ctrl_pressed = False
    #     elif event.key() == Qt.Key_Alt:
    #         self.alt_pressed = False
    #     super().keyReleaseEvent(event)

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
        print('\n')
        commonMessage = "Common Script Editor 2 UI was hided. Not closed !!"
        message(commonMessage + f'{self.__class__}')
        # print('CustomScriptEditor2 class UI, hide')
        # ウィンドウが閉じられたときにシグナルを送信
        self.closed.emit()
        # super(CustomScriptEditor2, self).closeEvent(event)

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

    def mouseDoubleClickEvent(self, event):
        """中ボタンダブルクリックイベント"""
        if event.button() == Qt.MiddleButton:
            self.resetHighlights()
            # 検索のクリアーを実行したら、デフォルトのcontextMenuhy表示へ戻す
            self.next_result_action.setEnabled(False)
            self.prev_result_action.setEnabled(False)

    def copySelectedTextToSearchField(self):
        cursor = self.text_edit.textCursor()
        selected_text = cursor.selectedText()
        if selected_text:
            if self.search_dialog is None:
                self.search_dialog = SearchDialog(self,
                                                  initial_text=selected_text,
                                                  initial_color=self.highlight_color)
            else:
                self.search_dialog.setInitialText(selected_text)
                self.search_dialog.activateWindow()
            self.search_dialog.show()

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_F and event.modifiers() == Qt.ControlModifier:
            self.copySelectedTextToSearchField()
            return True
        return super().eventFilter(source, event)

    # CustomScriptEditor2 クラス内の mouseReleaseEvent メソッドを追加します
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            cursor = self.text_edit.textCursor()
            selected_text = cursor.selectedText()
            if selected_text:
                # テキストが選択されている場合は、検索ダイアログのフィールドに反映させます
                if self.search_dialog is None:
                    self.search_dialog = SearchDialog(self,
                                                      initial_text=selected_text,
                                                      initial_color=self.highlight_color)
                else:
                    self.search_dialog.setInitialText(selected_text)
                    self.search_dialog.activateWindow()
                self.search_dialog.show()
        super().mouseReleaseEvent(event)


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
    # cse2 = CustomScriptEditor2(title = 'test', infoDetail = 'test')
    # cse2.show()
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
