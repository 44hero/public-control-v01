# -*- coding: utf-8 -*-

u"""
yoSkinWeightsExpImpTool_View.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -2.0-
:Date: 2024/05/09

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PySide2 version: 5.15.2

-リマインダ-
    done: 2024/05/08~2024/05/09
        追加と変更と新規1
            - 概要: outPut 専用 script_editor ウィジェット の挙動修正
            - 詳細: メインとなるUIとのセットで出現することを想定しているのだが、
                個別にUIを誤って閉じてしまった場合等、エラー回避を主な目的とした、ｺｰﾄﾞ修正と追加
                ::

                    +   # UIの起動 関数
                        def createUI(self):
                            ...
                            # 追加と変更と新規1
                            print('新規に outPut 専用 script_editor ウィジェット も作成します')
                            self.create_script_editor_and_show()
                            print(self.script_editor)

                    +   # 追加と変更と新規1
                        def create_script_editor_and_show(self):
                            ...

                    +   # print(self.statusCurrent_scriptEditor)
                        if self.statusCurrent_scriptEditor == 'closed':
                            self.create_script_editor_and_show()
                            # print(self.statusCurrent_scriptEditor)
                        self.script_editor.append_warning(***)

                        # あらゆる箇所で、利用されている、
                        # self.script_editor.append_warning(***)
                        # の前に、
                        # # print(self.statusCurrent_scriptEditor)
                        # if self.statusCurrent_scriptEditor == 'closed':
                        #     self.create_script_editor_and_show()
                        #     # print(self.statusCurrent_scriptEditor)
                        を追記し、エラー回避
        version = '-2.0-'

    done: 2024/04/21~2024/04/25
        新規
        version = '-1.0-'
"""

# 標準ライブラリ #################################################################
import os
from functools import partial
from pprint import pprint
from typing import Any, Tuple, List, AnyStr
from collections import OrderedDict

# サードパーティライブラリ #########################################################
from maya import OpenMayaUI, cmds
from PySide2.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
                               QFileDialog, QGridLayout, QLineEdit, QMainWindow,
                               QMenu, QTabWidget, QTextEdit, QWidget,
                               QHBoxLayout, QVBoxLayout, QPushButton, QAction,
                               QFrame, QLabel, QSpacerItem, QSizePolicy,
                               )
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtCore import Qt, Slot

# ローカルで作成したモジュール ######################################################
import YO_utilityTools.skinWeightsExpImpTool.config as docstring
from YO_utilityTools.lib.commonCheckSelection import commonCheckSelection
# basic_configuration(基本構成)
from .config import SPACE, TITLE, VERSION

from .yoSkinWeightsExpImpTool_Modl import SkinWeightExpImp_Modl
from .yoSkinWeightsExpImpTool_Ctlr import SkinWeightExpImp_Ctlr

# shiboken2 独自モジュール
from ..TemplateForPySide2.qt import getMayaWindow  # 利用時は、getMayaWindow()

from ..TemplateForPySide2.pyside2IniFileSetting import IniFileSetting
from ..TemplateForPySide2.Container import Container
from ..TemplateForPySide2.MyTabWidget import MyTabWidget
from ..TemplateForPySide2.CustomScriptEditor import CustomScriptEditor

from ..TemplateForPySide2.type1.templateForPySide2_type1_View import Tpl4PySide2_Type1_View
# 汎用ライブラリー の使用 #################################################### start
from ..lib.message import message
from ..lib.message_warning import message_warning
from ..lib.yoGetAttributeFromModule import GetAttrFrmMod
from ..lib.commonCheckCurve import commonCheckCurve
from ..lib.commonCheckMesh import commonCheckMesh
from ..lib.commonCheckSurface import commonCheckSurface
from ..lib.commonCheckShape import commonCheckShape
from ..lib.commonCheckSkinCluster import commonCheckSkinCluster
# 汎用ライブラリー の使用 #################################################### end


class CustomPopup(QDialog):
    def __init__(self
                 , titleName: str
                 , infoSummary: str, infoDetail: str
                 , parent = None):
        super(CustomPopup, self).__init__(parent)
        self.win = titleName + '_' + 'ui'
        # UIの window name (objectName) 設定
        # set window name
        self.setObjectName(self.win)  # <- window へobjectName 設定
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)  # windowの右上にx印(close)のみ
        # PySideで作ったGUIは何もしてないと close しても delete はされません。
        # windowオブジェクト に `setAttribute` することで close 時に delete されるようになります。
        self.setAttribute(Qt.WA_DeleteOnClose)  # <- close 時に delete 設定

        self.setWindowTitle(titleName)

        # 独自で色を設定1
        # {QLabel}.setStyleSheet(self.tooltip_style) した時だけ 独自色を設定できます
        self.tooltip_style = """
            QLabel {
                background-color: mediumpurple;
                color: black;
            }
            QToolTip {
                background-color: lemonchiffon;
                color: black;
                border: 1px solid black;
            }
        """

        layout = QVBoxLayout()
        message_label1 = QLabel(infoSummary)
        message_label1.setAlignment(Qt.AlignCenter)  # Align the text to the center
        layout.addWidget(message_label1)

        message_label2 = QLabel('note:')
        message_label2.setAlignment(Qt.AlignCenter)  # Align the text to the center
        # ラベルウィジェット2 を装飾
        # 設定を施す ###################################
        message_label2.setStatusTip(infoDetail)
        message_label2.setToolTip(infoDetail)
        # ラベルウィジェット2 を装飾
        # 設定を施す ###################################
        message_label2.setStyleSheet(self.tooltip_style)  # 独自で色を設定
        layout.addWidget(message_label2)

        btnWid = QWidget()
        gLay = QGridLayout(btnWid)
        self.ok_button: QPushButton = QPushButton('OK')
        self.ok_button.clicked.connect(self.accept)
        self.cls_button: QPushButton = QPushButton('Close')
        self.cls_button.clicked.connect(self.close)
        gLay.addWidget(self.ok_button, 0, 0)
        gLay.addWidget(self.cls_button, 0, 1)

        # ボタン間のスペースを均等に分配
        gLay.setSpacing(3)
        # OKボタンの幅が5倍、Closeボタンの幅が1倍になるように伸縮性を設定
        gLay.setColumnStretch(0, 5)
        gLay.setColumnStretch(1, 1)

        layout.addWidget(btnWid)

        self.setLayout(layout)

        self.result = None  # 結果を保持する変数

    # オーバーライド
    # closeEvent メソッド 組み込み関数
    def closeEvent(self, event):
        # ウィンドウが閉じられたときの処理
        self.result = False  # ウィンドウが閉じられたときはFalseを設定
        event.accept()

    def accept(self):
        # OKボタンが押されたときの処理
        self.result = True  # OKボタンが押されたときはTrueを設定
        self.done(1)


class SkinWeightExpImp_View(Tpl4PySide2_Type1_View):
    # initialize(初期化関数)コンストラクタです。
    # ここで定義されたインスタンス変数は、他のメソッドで上書き・参照が出来ます。
    # 当該window を Maya window 画面の前面にする設定 も行っています
    def __init__(self, _model, parent = None, flags = Qt.WindowFlags()):
        u""" < initialize(初期化関数)コンストラクタ です >

        ::

          ここで定義されたインスタンス変数は、他のメソッドで上書き・参照が出来ます。

        基本となるUI構成で不可欠となる要素 8つ の内、以下 2つ を実行しています
            - <UI要素 1>. UIを、Maya window 画面の前面にする
            - <UI要素 3>. UI設定の保存と復元 の機能を 何らかで実現する
                .iniファイルを利用した、
                    - windowUIの、ポジションとサイズ、
                    - 他必要箇所となる 入力フィールドの要素、
                の、保存と復元 の機能を有効にする
        """
        # <UI要素 1>.
        # 当該window を Maya window 画面の前面に ######################################## start
        if parent is None:
            parent = getMayaWindow()
        # 当該window を Maya window 画面の前面に ######################################## end

        super(Tpl4PySide2_Type1_View, self).__init__(parent, flags)

        self.model = _model
        self.controller = None

        # ######################################################################
        self.title = TITLE  # <- window の title名
        self.space = SPACE
        self.version = VERSION
        self.underScore = '_'
        self.win = TITLE + '_ui'  # <- window へ objectName
        # 不変要素な、4つ 且つ typeがint であることを明記
        self.size: Tuple[int] = (500, 300, 210, 270)  # x, y, width, height
        self.bgc = "background-color:gray; color: white"
        self.infoSummary = (u'skin weights の export, import ツール\n'
                            u'の バージョン1.0(PySide2版) です。')
        self.infoDetail = u'maya 用の skin weights の export, import ツール です。'
        # ######################################################################

        # <UI要素 3>.
        # コンストラクタのまとまり1_.iniファイル 設定
        self.constructorChunk1_iniFileSetting()

        # コンストラクタのまとまり2_.iniファイルのパラメーター 設定
        self.constructorChunk2_iniFileParam()
        # コンストラクタのまとまり3_色とアイコン 設定
        self.constructorChunk3_colorAndIcon()  # 継承元既存からの再利用
        # コンストラクタのまとまり4_その他A 設定
        self.constructorChunk4_otherA()
        # コンストラクタのまとまり5_そのB 設定
        self.constructorChunk5_otherB()
        # コンストラクタのまとまり6_色 設定
        self.constructorChunk6_color()

        # カスタムで、専用の スクリプトエディタ を初期化
        self.script_editor = None
        self.statusCurrent_scriptEditor = 'open'

    # コンストラクタのまとまり1_.iniファイル 設定
    def constructorChunk1_iniFileSetting(self):
        u""" < コンストラクタのまとまり1_.iniファイル 設定 >

        ######################
        """
        # .iniファイルの設定 ########################################################### start
        self.iniFS = IniFileSetting(self.title[2:])  # pyside2IniFileSetting モジュール
        filename, _settings = self.iniFS.iniFileSetting()  # .iniファイルの設定 メソッド
        self.filename = filename
        self._settings = _settings
        # .iniファイルの設定 ########################################################### end

    # コンストラクタのまとまり2_.iniファイルのパラメーター 設定
    def constructorChunk2_iniFileParam(self):
        u""" < コンストラクタのまとまり2_.iniファイルのパラメーター 設定 >

        ######################
        """
        # .iniファイルのパラメーター設定 ##################################### start
        self.iniFileParam = {'geo_iFP': 'geometry',
                             }
        self.iniFileParam_txtFld_ExpImp = {
            'exp_txtFld_A_iFP': 'exp_txtFld_A',  # [0] self.expFileNameTxtFld_lEdtWid に相当
            'exp_txtFld_B_iFP': 'exp_txtFld_B',  # [1] self.expFilePathTxtFld_lEdtWid に相当
            'imp_txtFld_A_iFP': 'imp_txtFld_A',  # [2] self.impFileNameTxtFld_lEdtWid に相当
            'imp_txtFld_B_iFP': 'imp_txtFld_B',  # [3] self.impFilePathTxtFld_lEdtWid に相当
            }
        # self.od = OrderedDict(self.iniFileParam_txtFld_ExpImp)  # 順序付き辞書 定義
        # .iniファイルのパラメーター設定 ##################################### end

    # コンストラクタのまとまり4_その他A 設定
    def constructorChunk4_otherA(self):
        u""" < コンストラクタのまとまり4_その他A 設定 >

        ######################
        """
        # container1用 ボタンの情報のリスト まとめ
        self.button_info: List[str] = ['buttonA', 'buttonB', 'buttonC']
        self.doResetStat = False

    # コンストラクタのまとまり5_そのB 設定
    def constructorChunk5_otherB(self):
        self.exp_SCname = ''
        self.exp_directory = r''
        self.imp_directory = r''
        self.imp_FileName = ''

    # 新規
    # コンストラクタのまとまり6_色 設定
    def constructorChunk6_color(self):
        u""" < コンストラクタのまとまり6_色 設定 >

        ######################
        """
        # QPushButton 独自で色を設定1
        # {QPushButton}.setStyleSheet(self.pBtn_tooltip_style*) した時だけ 独自色を設定できます
        # style1 bgcGray
        self.pBtn_tooltip_style1 = """
            QPushButton {
                background-color: rgb(93, 93, 93);
                color: white;
            }
            QToolTip {
                background-color: lemonchiffon;
                color: black;
                border: 1px solid black;
            }
        """
        # style2 bgcGray2
        self.pBtn_tooltip_style2 = """
            QPushButton {
                background-color: rgb(113, 113, 113);
                color: white;
            }
            QToolTip {
                background-color: lemonchiffon;
                color: black;
                border: 1px solid black;
            }
        """
        # style2 bgcGray3
        self.pBtn_tooltip_style3 = """
            QPushButton {
                background-color: lightgray;
                color: black;
            }
            QToolTip {
                background-color: lemonchiffon;
                color: black;
                border: 1px solid black;
            }
        """

        # 独自で色を設定2
        self.bgcGray = "background-color: rgb(93, 93, 93)"
        self.bgcGray2 = "background-color: rgb(113, 113, 113);"  # old: gray
        self.bgcGray3 = "background-color: rgb(68, 68, 68);"  # maya default gray color
        self.bgcRed = ("background-color: lightcoral;"
                       "color: black")
        self.bgcGreen = ("background-color: yellowgreen;"
                         "color: black")

        # QWidget 独自で色を設定3
        # {QWidget}.setStyleSheet(self.wid_tooltip_style1*) した時だけ 独自色を設定できます
        # style1 bgcGray
        self.wid_tooltip_style1 = """
            QWidget {
                background-color: rgb(93, 93, 93);
                color: white;
            }
            QToolTip {
                background-color: lemonchiffon;
                color: black;
                border: 1px solid black;
            }
        """
        # style2 bgcGray2
        self.wid_tooltip_style2 = """
            QWidget {
                background-color: rgb(113, 113, 113);
                color: white;
            }
            QToolTip {
                background-color: lemonchiffon;
                color: black;
                border: 1px solid black;
            }
        """

    # オリジナルメソッド
    # Window基本設定
    def _windowBasicSettings(self):
        u""" < 当該window の、基本設定 をいっぺんに行う 関数 です >

        オリジナルメソッド

        .. note::
          - set window title と 新規のポジションとサイズ設定 : <UI要素 2>.
          - set window name : <UI要素 8>.
          はここで行っています
        基本となるUI構成で不可欠となる要素 8つ の内、以下 5つ を実行しています
            - <UI要素 2>. UIの title設定 と、新規での ポジションとサイズ設定
            - <UI要素 5>. UIの重複の回避
            - <UI要素 6>. UIの見た目の統一
            - <UI要素 7>. -Pyside2特有事項- UIのclose時にdeleteされるようにする
            - <UI要素 8>. UI window name (objectName) 設定
        """
        # <UI要素 2>.
        # UI設定の保存と復元 の機能 ###################################################### start
        # self.setWindowTitle(self.title[2:] + self.space + self.version)  # <- window の title名 設定
        self.setWindowTitle(self.title[2:] + self.space + self.version)  # <- window の title名 設定
        # ウィンドウが一度でも作成されているかどうかを確認
        # 純粋に初めてのUI作成時: False # 以下を実行
        # 次回再度ロード時は: True # ここをスキップし、前回の ポジションとサイズ が復元される
        if not self.isVisible():
            self.setGeometry(*self.size)  # 完全に新規にUI作成したときの初期値。アンパック(*)は重要
        # UI設定の保存と復元 の機能 ###################################################### end

        # <UI要素 5>.
        # UIの 重複表示の回避 ########################################################### start
        # old style ############################### start
        # child_list = self.parent().children()
        # for c in child_list:
        #     # 自分と同じ名前のUIのクラスオブジェクトが存在してたらCloseする
        #     if self.__class__.__name__ == c.__class__.__name__:
        #         c.close()
        # old style ############################### end
        self._duplicateWindowAvoidFunction(winName = self.win)  # 重複ウィンドウの回避関数
        # UIの 重複表示の回避 ########################################################### end

        # <UI要素 6>.
        # UIの 見た目の統一 ############################################################# start
        # Windows用 window の見た目の制御を行います
        # # type1
        # # minimize, maximize, close 有り
        # self.setWindowFlags(Qt.Window)
        # # type2
        # # minimize のみ有り
        # self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint)
        # type3
        # close のみ有り
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)  # windowの右上にx印(close)のみ
        # UIの 見た目の統一 ############################################################# end

        # self.setUpdatesEnabled(True)  # デフォルトでTrueです

        # <UI要素 7>.
        # -Pyside2特有事項- UI の close 時に delete されるようにする ###################### start
        # PySideで作ったGUIは何もしてないと close しても delete はされません。
        # windowオブジェクト に `setAttribute` することで close 時に delete されるようになります。
        self.setAttribute(Qt.WA_DeleteOnClose)  # <- close 時に delete 設定
        # -Pyside2特有事項- UI の close 時に delete されるようにする ###################### end

        # <UI要素 8>.
        # UIの window name (objectName) 設定 ########################################## start
        # set window name
        self.setObjectName(self.win)  # <- window へobjectName 設定
        # UIの window name (objectName) 設定 ########################################## end

        # <UI要素 4>.
        # UI設定の保存と復元 の機能 の 一部 ############################################### start
        # different style ######################## start
        # Note: .iniファイルを使用せず、maya独自規格使用時 有効です
        #       但し、UIに入力フィールドとう存在した場合には、それらはここには含まれず、他のアプローチも必要
        # window を close したときのサイズ・位置のみが `windowPrefs.mel` に保存されるようになり、
        # 次回 show 時に復元されるようになります。
        # self.setProperty("saveWindowPref", True)
        # different style ######################## end
        #  UI設定の保存と復元 の機能 の 一部 ############################################### end

    # UIの起動 関数
    def createUI(self):
        u""" < UIの起動 関数 です >

        ::

          -構成は以下-
          0): QMainWindow
          |
          |-- 1): QWidget (central_wid) -Widget-
            |
            |-- 2): QVBoxLayout (main_vbxLay) -Layout-
              |
              |-- 3): 大フレーム群 と 底面ボタン群 とに分けられます
                |
                |-- 大フレーム群 <フレーム に commonInformation と displayOptions がぶら下がります>
                |   3.1): QFrame (self.frame_frWid) -Widget-
                |   |
                |   |-- <self.commonInformation() -まとまり->
                |   |   QVBoxLayout (self.frame_layout) -Layout-
                |   |   |
                |   |   |-- QLabel (txt1_lblWid) -Widget-
                |   |   |-- QLabel (txt2_lblWid) -Widget-
                |   |   |-- QFrame (separator_frWid) -Widget-
                |   |
                |   |-- <self.displayOptions() -まとまり->
                |       QVBoxLayout (self.frame_layout) -Layout-
                |       |
                |       |-- QWidget (container1_wid) -Widget-
                |       |   |
                |       |   |-- QHBoxLayout (container1_hbxLay) -Layout-
                |       |       |
                |       |       |-- QLabel ("New Widget") -Widget-
                |       |
                |       |-- QWidget (container2_wid) -Widget-
                |           |
                |           |-- QVBoxLayout (container2_vbxLay) -Layout-
                |               |
                |               |-- QLabel (another_lblWid "Another Widget") -Widget-
                |
                |-- 底面ボタン群 <self.commonButtons() -まとまり->
                    3.2): QHBoxLayout (self.button_hbxLay) -Layout-
                    |
                    |-- QPushButton ("Execute") -Widget-
                    |-- QPushButton ("Reset") -Widget-
                    |-- QPushButton ("Close") -Widget-

          -概要-
          0): QMainWindow (メインウィンドウ)
          - メインウィンドウ全体を管理するクラスです.

          1): QWidget (central_wid) -Widget-
          - メインウィンドウの中央に配置されるウィジェットです.
          - 垂直に配置されたレイアウト (QVBoxLayout: main_vbxLay) を持っています.

          2): QVBoxLayout (main_vbxLay) -Layout-
          - QWidget (central_wid) 内のメインレイアウトです.

             3): 大フレーム群 と 底面ボタン群
                - `QWidget` 内のコンテンツをさらに2つに分けています.

                3.1): 大フレーム群 -Widget-
                   - `QFrame` (`self.frame_frWid`) を使用して、共通情報 (`commonInformation`) と表示オプション (`displayOptions`) を含む2つのグループに分けています.
                   - それぞれのグループは `QVBoxLayout` (`self.frame_layout`) を持っています.
                      - commonInformation (共通情報)
                      - displayOptions (表示オプション)

                3.2): 底面ボタン群 -Layout-
                   - `QHBoxLayout` (`self.button_hbxLay`) を使用して、以下の3つのボタンを水平に配置しています:
                      - `QPushButton` ("Execute") -Widget-
                      - `QPushButton` ("Reset") -Widget-
                      - `QPushButton` ("Close") -Widget-
                   - これらのボタンは `self.commonButtons()` メソッド内で構築されます.
        """
        self._windowBasicSettings()  # 当該window の設定をいっぺんに行う 関数

        self.controller = self.model.controller  # 和えて明示しています。無くてもこのケースでは実行可。

        # print('--- createUI, koko')
        # print(self.ui)
        #
        # if self.ui is not None:
        #     self.ui.deleteLater()

        # 1):###############################################################################
        # 概要: メインウィンドウ の中央に配置される セントラルウィジェット です
        # 1): QWidget -Widget- ############################################## -Widget- start
        self.central_wid = QWidget(self)  # セントラルウィジェット
        self.setCentralWidget(self.central_wid)  # 中央に配置

        # 1): QWidget -Widget- ############################################## -Widget- end
        # 1):###############################################################################

        # Clear existing menu items
        # self.menuBar().clear()
        # UI-1. commonメニュー
        self.commonMenu()  # ############################### UI-1. commonメニュー

        # 2):###############################################################################
        # 概要: セントラルウィジェット 内の メインレイアウト です
        # 2): QVBoxLayout -Layout- ########################################## -Layout- start
        # セントラルウィジェット に 縦のメインレイアウト
        # を作成し そのウィジェット へ set ############### 作成しただけでは表示されません -Layout-
        main_vbxLay = QVBoxLayout(self.central_wid)  # メインレイアウト
        # レイアウトの余白を調整
        main_vbxLay.setContentsMargins(3, 3, 3, 3)

        # 2): QVBoxLayout -Layout- ########################################## -Layout- end
        # 2):###############################################################################

        # 3):###############################################################################
        # 概要: メインレイアウト 内には、大フレーム群 と 底面ボタン群 が縦に配置されます
        # 3.1): 大フレーム群 -Widget- ######################################### -Widget- start
        # セントラルウィジェット 内に ウィジェット(大フレーム用)
        # を作成 ###################################### 作成しただけでは表示されません -Widget-
        self.frame_frWid = QFrame(self.central_wid)  # フレームウィジェット(大フレーム用)
        # フレームウィジェット(大フレーム用) に 縦のレイアウト(大フレーム用)
        # を作成し そのウィジェット へ set ############### 作成しただけでは表示されません -Layout-
        self.frame_vbxLay = QVBoxLayout(self.frame_frWid)  # レイアウト(大フレーム用)
        # フレームウィジェット(大フレーム用) を メインレイアウト
        # に追加 ###################################### 追加して初めて表示されます     -表示-
        main_vbxLay.addWidget(self.frame_frWid)
        # フレームウィジェット(大フレーム用) を装飾
        # 設定を施す ###################################
        self.frame_frWid.setFrameShape(QFrame.StyledPanel)  # 枠のスタイルを設定

        # まとまりA
        # 大フレーム群 に収まっているものです ######################################## start
        # UI-2. common情報
        # 設定を施す ###################################
        self.commonInformation(frame_layout = self.frame_vbxLay)  # ############################ UI-2. common情報
        # UI-2. 追加オプションのまとまり
        # 設定を施す ###################################
        self.displayOptions(frame_layout = self.frame_vbxLay)  # #################### UI-2. 追加オプションのまとまり

        # 大フレーム群 に収まっているものです ######################################## end

        # 常に、大フレーム のトップ に順番に配置されるようにするため、垂直スペーサーを追加して間隔を制御
        # まとまりA を装飾
        # 設定を施す ###################################
        spacer = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.frame_vbxLay.addItem(spacer)

        # 3.1): 大フレーム群 -Widget- ######################################### -Widget- end

        # 3.2): 底面ボタン群 -Layout- ###################################$##### -Layout- start
        # セントラルウィジェット 内に 水平レイアウト(底面ボタン用)
        # を 直接 作成 追加 ###################################### 一遍に行えます
        self.button_hbxLay = QHBoxLayout(self.central_wid)  # レイアウト(底面ボタン用)

        # まとまりB
        # 底面ボタン群 です ####################################################### start
        # UI-3. common底面ボタン3つ
        # 設定を施す ###################################
        self.commonButtons(self.button_hbxLay)  # ######################## UI-3. common底面ボタン3つ

        # 底面ボタン群 です ####################################################### end

        # レイアウト(底面ボタン用) を メインレイアウト
        # に追加 ###################################### 追加して初めて表示されます     -表示-
        main_vbxLay.addLayout(self.button_hbxLay)

        # 3.2): 底面ボタン群 -Layout- ###################################$##### -Layout- end
        # 3):###############################################################################

        # 最終的にUIを作成
        self.show()   # 継承元の show メソッド 組み込み関数 を再利用 しています

        # 追加と変更と新規1
        print('新規に outPut 専用 script_editor ウィジェット も作成します')
        self.create_script_editor_and_show()
        print(self.script_editor)

    # 追加と変更と新規1
    def create_script_editor_and_show(self):
        # カスタムで、専用の スクリプトエディタ を作成します
        if self.script_editor is None:
            self.script_editor = CustomScriptEditor(
                title = 'resultOutputUI_forHeadsUpSpecialization',
                infoDetail = ('<注意喚起特化用_結果_出力_UI>\n\n'
                              '各ｺｰﾄﾞ実行中に頻繁に出力される結果表示において、\n'
                              '注意喚起の結果出力だけにフォーカスした、\n'
                              '注意喚起特化用UI\n'
                              'です。\n\n'
                              'note): \n'
                              '右ボタン押下でエディタ用途として\n簡単な編集も可能です。')
                )  # 都度各ｺｰﾄﾞ実行内容の結果出力 用 UI です
            self.script_editor.closed.connect(self.on_script_editor_closed)
        else:
            print('ひき続き継続して使用中...')
            pass

        # CustomScriptEditor ﾓｼﾞｭｰﾙ先では、あえて、show() せず、ここで show() しています。
        self.script_editor.show()  # note): これは必須です。

        self.statusCurrent_scriptEditor = 'open'

    # reset ボタン及びメニュー を選択したかどうかを文字列で返す 関数
    def doResetStatYesOrNo_byString(self, value: bool) -> str:
        u""" < reset ボタン及びメニュー を選択したかどうかを文字列で返す 関数 です >

        :param bool value: True/False
        :return: result
            'yes'/'no'
        :rtype: str
        """
        if value:
            result = 'yes'
        else:
            result = 'no'
        return result

    # UIディテール 作成 ################################################################ start
    # UI-1. commonメニュー
    def commonMenu(self):
        u""" < UI-1. commonメニュー の作成 >

        - メニュー
        を一気に作成しています
        """
        # menuBar_ ################################################################### start
        menuBar_ = self.menuBar()
        editMenu = menuBar_.addMenu("Edit")
        helpMenu = menuBar_.addMenu('Help')
        editMenu.setToolTip(f'Edit menu です。')
        helpMenu.setToolTip(f'Help menu です。')

        # Edit menu ##############################################
        saveSettings = 'Save Settings'
        saveAction = QAction(QIcon(self.saveSettingsIcon), saveSettings, self)
        saveAction.setShortcut("Ctrl+S")  # QKeySequence.Save, Qt.CTRL + Qt.Key_S と同等
        saveAction.setStatusTip(f'setting を save します。')

        resetSettings = 'Reset Settings'
        resetAction = QAction(QIcon(self.resetSettingsIcon), resetSettings, self)
        resetAction.setShortcut("Ctrl+Alt+S")  # Qt.CTRL + Qt.ALT + Qt.Key_S と同等
        resetAction.setStatusTip(f'setting を reset します。')

        closeThisUi = 'Close This UI'
        closeAction = QAction(QIcon(self.closeIcon), closeThisUi, self)
        closeAction.setShortcut("Ctrl+X")  # QKeySequence.Close, Qt.CTRL + Qt.Key_X と同等
        closeAction.setStatusTip(f'当UI を close します。')

        # アクション
        editMenu.addAction(saveAction)
        editMenu.addAction(resetAction)
        editMenu.addAction(closeAction)

        # シグナル/スロット
        saveAction.triggered.connect(
            partial(self.controller.menuSave, f'v: menu, {saveSettings}')
            )
        resetAction.triggered.connect(
            partial(self.controller.menuReset, f'v: menu, {resetSettings}')
            )
        closeAction.triggered.connect(
            partial(self.controller.menuClose, f'v: menu, {closeThisUi}')
            )

        # Help menu ##############################################
        help_ = 'Help'
        helpAction = QAction(QIcon(self.helpIcon), f'Help on {self.title[2:]}',
                             self
                             )
        helpAction.setShortcut("Ctrl+H")  # Qt.CTRL + Qt.Key_H と同等
        helpMenu.addAction(helpAction)
        helpMenu.setStatusTip(f'当UI の help です。')

        helpMenu.addAction(helpAction)

        helpAction.triggered.connect(partial(self.controller.menuHelp, help_
                                             )
                                     )
        # menuBar_ ################################################################### end

    # UI-3. common底面ボタン3つ
    def commonButtons(self, button_layout):
        u""" < UI-3. common底面ボタン3つの作成 >

        .. note:: 以下 は必須です！！

            - **button_layout**
                レイアウト(底面ボタン用)
                    に、
                以下の、情報
                    がぶら下がります

        ######################

        - Execute ボタン
        - Reset ボタン
        - Close ボタン
        を一気に作成し、レイアウトまで行っています

        ######################

        :param button_layout: メインとなるレイアウト(底面ボタン用)
        """
        # ボタン を作成 と レイアウト(底面ボタン用) に追加
        # # executeプッシュボタンウィジェット
        # # を作成 ###################################### 作成しただけでは表示されません -Widget-
        # execute = 'Execute'
        # exeBtn_pbtnWid = QPushButton(execute)  # プッシュボタンウィジェット(execute用)
        # # ボタンウィジェット(execute用) を レイアウト(底面ボタン用)
        # # に追加 ###################################### 追加して初めて表示されます     -表示-
        # button_layout.addWidget(exeBtn_pbtnWid, 2)  # 追加 # 比率も考慮

        # resetプッシュボタンウィジェット
        # を作成 ###################################### 作成しただけでは表示されません -Widget-
        reset = 'Reset'
        rstBtn_pbtnWid = QPushButton(reset)  # プッシュボタンウィジェット(reset用)
        # ボタンウィジェット(reset用) を レイアウト(底面ボタン用)
        # に追加 ###################################### 追加して初めて表示されます     -表示-
        button_layout.addWidget(rstBtn_pbtnWid, 1)  # 追加 # 比率も考慮

        # closeプッシュボタンウィジェット
        # を作成 ###################################### 作成しただけでは表示されません -Widget-
        close_ = 'Close'
        clsBtn_pbtnWid = QPushButton(close_)  # ボタンウィジェット(close用)
        # ボタンウィジェット(close用) を レイアウト(底面ボタン用)
        # に追加 ###################################### 追加して初めて表示されます     -表示-
        button_layout.addWidget(clsBtn_pbtnWid, 1)  # 追加 # 比率も考慮

        # レイアウト(底面ボタン用) の調整を装飾
        # 設定を施す ###################################
        button_layout.setSpacing(4)  # それぞれのボタンの間隔を狭くする
        # プッシュボタンウィジェット(execute用) を装飾
        # 設定を施す ###################################
        # exeBtn_pbtnWid.setStyleSheet(self.bgcBlue3)  # 独自で色を設定

        # シグナル/スロット
        # exeBtn_pbtnWid.clicked.connect(
        #     partial(self.controller.executeBtn, f'v: button, {execute}')
        #     )
        rstBtn_pbtnWid.clicked.connect(
            partial(self.controller.menuReset, f'v: button, {reset}')
            )
        clsBtn_pbtnWid.clicked.connect(
            partial(self.controller.menuClose, f'v: button, {close_}')
            )

    # UI-2. common情報
    def commonInformation(self, frame_layout):
        u""" < UI-2. common情報 の作成 >

        .. note:: 以下 は必須です！！

            - **frame_layout**
                メインとなるレイアウト(大フレーム用)
                    に、
                以下の、情報
                    がぶら下がります

        ######################

        - ラベルウィジェット1
        - ラベルウィジェット2
        - セパレータウィジェット
        を一気に作成し、レイアウトまで行っています

        ######################

        :param frame_layout: メインとなるレイアウト(大フレーム用)
        """
        # QLabel -Widget- ################################################### -Widget- start
        # ラベルウィジェット1
        # を作成 ###################################### 作成しただけでは表示されません -Widget-
        txt1_lblWid = QLabel(self.infoSummary)  # ラベルウィジェット1
        # 装飾
        # 設定を施す ###################################
        txt1_lblWid.setAlignment(Qt.AlignCenter)  # Align the text to the center
        # ラベルウィジェット1 を レイアウト(大フレーム用)
        # に追加 ###################################### 追加して初めて表示されます     -表示-
        frame_layout.addWidget(txt1_lblWid)
        # QLabel -Widget- ################################################### -Widget- end

        # QLabel -Widget- ################################################### -Widget- start
        # ラベルウィジェット2
        # を作成 ###################################### 作成しただけでは表示されません -Widget-
        txt2_lblWid = QLabel('note:')  # ラベルウィジェット2
        # ラベルウィジェット2 を装飾
        # 設定を施す ###################################
        txt2_lblWid.setAlignment(Qt.AlignCenter)  # Align the text to the center
        # txt1_lblWid を装飾 ツールヒントを設定
        # QToolTip.setFont(QApplication.font())
        # txt1_lblWid.setStatusTip(self.infoDetail)
        # txt1_lblWid.setToolTip(self.infoDetail)
        # ラベルウィジェット2 を装飾
        # 設定を施す ###################################
        txt2_lblWid.setStatusTip(self.infoDetail)
        txt2_lblWid.setToolTip(self.infoDetail)
        # ラベルウィジェット2 を装飾
        # 設定を施す ###################################
        txt2_lblWid.setStyleSheet(self.tooltip_style)  # 独自で色を設定
        # ラベルウィジェット2 を レイアウト(大フレーム用)
        # に追加 ###################################### 追加して初めて表示されます     -表示-
        frame_layout.addWidget(txt2_lblWid)
        # QLabel -Widget- ################################################### -Widget- end

        # QFrame -Widget- ################################################### -Widget- start
        # セパレータウィジェット
        # を作成 ###################################### 作成しただけでは表示されません -Widget-
        separator_frWid = QFrame(self)  # フレームウィジェット(セパレータ用)
        # フレームウィジェット(セパレータ用) を装飾
        # 設定を施す ###################################
        separator_frWid.setFrameShape(QFrame.HLine)  # Set frame_frWid shape to horizontal line
        separator_frWid.setFrameShadow(QFrame.Raised)
        separator_frWid.setStyleSheet(self.bgcWhite)  # 独自で色を設定
        separator_frWid.setLineWidth(2)  # Set the line width
        # フレームウィジェット(セパレータ用) を レイアウト(大フレーム用)
        # に追加 ###################################### 追加して初めて表示されます     -表示-
        frame_layout.addWidget(separator_frWid)
        # QFrame -Widget- ################################################### -Widget- end

        # 常に、レイアウト(大フレーム用) のトップに配置されるようにするため、垂直スペーサーを追加して間隔を制御します
        # spacer = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # frame_layout.addItem(spacer)

    # UI-2. 追加オプションのまとまり
    def displayOptions(self, frame_layout):
        u""" < UI-2. 追加オプションのまとまり >

        .. note:: 以下 は必須です！！

            - **frame_layout**
                メインとなるレイアウト(大フレーム用)
                    に、
                以下の、情報
                    がぶら下がります

        ######################

        以下は、サンプルです。

        - container1
        - container2
        を一気に作成しています

        ######################

        :param frame_layout: メインとなるレイアウト
        """
        # QWidget -Widget- ################################################## -Widget- start
        # container1
        # を作成 ###################################### 作成しただけでは表示されません -Widget-
        container1_wid = QWidget(self)  # ウィジェット(コンテナ1用)
        # ウィジェット(コンテナ1用) 内に 縦のレイアウト(コンテナ1用)
        # を作成し そのウィジェット へ set ############### 作成しただけでは表示されません -Layout-
        container1_gdLay = QGridLayout(container1_wid)  # レイアウト(コンテナ1用)

        # caseA1 ##################################################################### start
        # export tool: cmds.deformerWeights(f'{ｽｷﾝｸﾗｽﾀｰ名}.xml',
        #                       export = True, path = 'directoryﾊﾟｽ',
        #                       deformer = 'ｽｷﾝｸﾗｽﾀｰ名'
        #                       )
        caseIndex = 'caseA1'
        et = 'exportTool'
        expDefWeitsOptSC_string = 'skinCluster 名\n取得ﾎﾞﾀﾝ:'
        expDefWeitsOpt_lblWid = QLabel(expDefWeitsOptSC_string)
        # ラベルウィジェット を装飾
        expDefWeitsOpt_lblWid.setAlignment(Qt.AlignRight)
        container1_gdLay.addWidget(expDefWeitsOpt_lblWid, 0, 0)

        # get SkinCluster name #################################################
        # container1 内に ボタンウィジェット
        # を作成 ###################################### 作成しただけでは表示されません -Widget-
        expDefWeitsOptUI_string = (u'maya default の Export Deformer Weights Options UI\n'
                                   u'を使用せず、\n'
                                   u'skinCluster のみ、且つ、XMLファイル での出力 に特化した、ファイル書き出し\n'
                                   u'で weight を出力するツールです。\n\n'
                                   u'note):'
                                   u'ｽｷﾝｸﾗｽﾀｰ名 を そのまま XMLファイル名 として出力します。'
                                   u'\n'
                                   u'note):'
                                   u'当ツールは、予め、デフォルトで\n'
                                   u'\t<mel>' + '---' * 15 + '\n'
                                   u'\tdeformerWeights -export \n\t\t-deformer "ｽｷﾝｸﾗｽﾀｰ名" -format "XML" \n\t\t-path "ﾊﾟｽdirectory" "ｽｷﾝｸﾗｽﾀｰ名.xml";\n'
                                   u'\t<cmds>' + '---' * 15 + '\n'
                                   u'\tcmds.deformerWeights(\'ｽｷﾝｸﾗｽﾀｰ名.xml\', \n\t\texport = True, path = \'ﾊﾟｽdirectory\', \n\t\tdeformer = \'ｽｷﾝｸﾗｽﾀｰ名\')\n'
                                   u'で実行される設定です。'
                                   )
        getSC = 'get SkinCluster name'
        getSC_message_string = (f'{getSC}'
                                f'\n\n'
                                '当ボタンを押下することで、ｽｷﾝｸﾗｽﾀｰ名 を取得します。\n'
                                'その ｽｷﾝｸﾗｽﾀｰ名 を ファイル名 として認識し、\n'
                                '下の テキストフィールド へ自動で 入力を完了させます。'
                                )
        exp_btnA_getSC_pbtnWid = QPushButton('get')
        # ボタンウィジェット を装飾
        # 設定を施す ###################################
        exp_btnA_getSC_pbtnWid.setStatusTip(getSC_message_string)
        exp_btnA_getSC_pbtnWid.setToolTip(getSC_message_string)
        # ボタンウィジェット の幅を設定
        # exp_btnA_getSC_pbtnWid.setFixedWidth(100)  # 100は適切な幅に置き換えてください
        container1_gdLay.addWidget(exp_btnA_getSC_pbtnWid, 0, 1)
        # シグナル/スロット
        exp_btnA_getSC_pbtnWid.clicked.connect(partial(self.getSkinClusterBtn_directCheck,
                                                       f'v: pBtn, {getSC}',
                                                       caseIndex
                                                       )
                                               )  # ツールの呼び出し

        # skinned geometry name ################################################
        exp_skinGeoName_string = 'geometry 名:'
        skinGeoName_message_string = 'skinned \ngeometry 名'
        exp_skinGeoNameStr_lblWid: QLabel = QLabel(exp_skinGeoName_string)
        # ラベルウィジェット を装飾
        exp_skinGeoNameStr_lblWid.setStatusTip(skinGeoName_message_string)
        exp_skinGeoNameStr_lblWid.setToolTip(skinGeoName_message_string)
        exp_skinGeoNameStr_lblWid.setAlignment(Qt.AlignRight)
        container1_gdLay.addWidget(exp_skinGeoNameStr_lblWid, 1, 0)
        self.exp_skinGeoName_lblWid: QLabel = QLabel()
        # ラベルウィジェット を装飾
        self.exp_skinGeoName_lblWid.setAlignment(Qt.AlignCenter)
        container1_gdLay.addWidget(self.exp_skinGeoName_lblWid, 1, 1)

        # skinned geometry type ################################################
        exp_skinGeoType_string = 'type名:'
        skinGeoType_message_string = 'skinned \ngeometry type名'
        exp_skinGeoTypeStr_lblWid: QLabel = QLabel(exp_skinGeoType_string)
        # ラベルウィジェット を装飾
        exp_skinGeoTypeStr_lblWid.setStatusTip(skinGeoType_message_string)
        exp_skinGeoTypeStr_lblWid.setToolTip(skinGeoType_message_string)
        exp_skinGeoTypeStr_lblWid.setAlignment(Qt.AlignRight)
        container1_gdLay.addWidget(exp_skinGeoTypeStr_lblWid, 2, 0)
        self.exp_skinGeoType_lblWid: QLabel = QLabel()
        # ラベルウィジェット を装飾
        self.exp_skinGeoType_lblWid.setAlignment(Qt.AlignCenter)
        container1_gdLay.addWidget(self.exp_skinGeoType_lblWid, 2, 1)

        # File name ############################################################
        expFileName_string = 'File name:'
        self.expFileName_lblWid = QLabel(expFileName_string)
        # ラベルウィジェット を装飾
        self.expFileName_lblWid.setAlignment(Qt.AlignRight)
        # ラベルウィジェット を装飾
        # 設定を施す ###################################
        self.expFileName_lblWid.setStatusTip(expDefWeitsOptUI_string)
        self.expFileName_lblWid.setToolTip(expDefWeitsOptUI_string)
        container1_gdLay.addWidget(self.expFileName_lblWid, 3, 0)
        # テキスト入力フィールド（LineEdit）を作成してレイアウトに追加
        self.expFileNameTxtFld_lEdtWid: QLineEdit = QLineEdit()
        # テキスト入力フィールド の幅を設定
        # self.expFileNameTxtFld_lEdtWid.setFixedWidth(150)  # 100は適切な幅に置き換えてください
        # テキスト入力フィールド を装飾
        # 設定を施す ###################################
        self.expFileNameTxtFld_lEdtWid.setStatusTip(expDefWeitsOptUI_string)
        self.expFileNameTxtFld_lEdtWid.setToolTip(expDefWeitsOptUI_string)
        container1_gdLay.addWidget(self.expFileNameTxtFld_lEdtWid, 3, 1)
        expFileType_string = '.xml'
        self.expFileType_lblWid = QLabel(expFileType_string)
        container1_gdLay.addWidget(self.expFileType_lblWid, 3, 2)

        # File path ############################################################
        expFilePath_string = 'File path:'
        self.expFilePath_lblWid = QLabel(expFilePath_string)
        # ラベルウィジェット を装飾
        self.expFilePath_lblWid.setAlignment(Qt.AlignRight)
        # ラベルウィジェット を装飾
        # 設定を施す ###################################
        self.expFilePath_lblWid.setStatusTip(expDefWeitsOptUI_string)
        self.expFilePath_lblWid.setToolTip(expDefWeitsOptUI_string)
        container1_gdLay.addWidget(self.expFilePath_lblWid, 4, 0)  # itの列を2列に広げる
        # テキスト入力フィールド（LineEdit）を作成してレイアウトに追加
        self.expFilePathTxtFld_lEdtWid: QLineEdit = QLineEdit()
        # テキスト入力フィールド を装飾
        # 設定を施す ###################################
        self.expFilePathTxtFld_lEdtWid.setStatusTip(expDefWeitsOptUI_string)
        self.expFilePathTxtFld_lEdtWid.setToolTip(expDefWeitsOptUI_string)
        container1_gdLay.addWidget(self.expFilePathTxtFld_lEdtWid, 4, 1)

        setDir_string = 'Set Directory'
        setDir_message_string = (f'{setDir_string}'
                                 f'\n\n'
                                 '当ボタンを押下することで、'
                                 'ｽｷﾝｸﾗｽﾀｰ名を付与した .xmlﾌｧｲﾙ の出力先ﾃﾞｨﾚｸﾄﾘ を設定します。'
                                 )
        exp_setDir_pbtnWid = QPushButton('Set')
        # ボタンウィジェット を装飾
        # 設定を施す ###################################
        exp_setDir_pbtnWid.setStatusTip(setDir_message_string)
        exp_setDir_pbtnWid.setToolTip(setDir_message_string)
        container1_gdLay.addWidget(exp_setDir_pbtnWid, 4, 2)
        # シグナル/スロット
        exp_setDir_pbtnWid.clicked.connect(self.exp_browse_path)

        # ボタンウィジェット(execute用) ###########################################
        exp_exe = 'Export'
        exp_btnA_exe_pbtnWid = QPushButton(exp_exe)
        # ボタンウィジェット を装飾
        # 設定を施す ###################################
        # 継承元既存からの再利用
        exp_btnA_exe_pbtnWid.setStyleSheet(self.bgcBlue3)  # 独自で色を設定
        # ボタンウィジェット の幅を設定
        # exp_btnA_exe_pbtnWid.setFixedWidth(150)  # 100は適切な幅に置き換えてください
        container1_gdLay.addWidget(exp_btnA_exe_pbtnWid, 5, 0, 1, 3)
        # シグナル/スロット
        exp_btnA_exe_pbtnWid.clicked.connect(partial(self.exp_exeButton_skinClusterWeightFile_outPut,
                                                     f'v: pBtn, {et}',
                                                     caseIndex
                                                     )
                                             )  # ツールの呼び出し
        # caseA1 ##################################################################### end

        # Separatorを作成してレイアウトに追加
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Raised)
        container1_gdLay.addWidget(separator, 6, 0, 1, 3)  #note): addWidget(separator, 行, 列, 行スパン, 列スパン)

        # caseA2 ##################################################################### start
        # import tool: importSkinWeight('directoryﾊﾟｽ', f'{ｽｷﾝｸﾗｽﾀｰ名}.xml')
        caseIndex = 'caseA2'
        it = 'importTool'
        impDefWeitsOptUI_string = (u'maya default の Import Deformer Weights Options UI\n'
                                   u'を使用せず、\n'
                                   u'skinCluster のみ、且つ、XMLファイル のみに特化した、ファイル読み込み\n'
                                   u'で weight を取得するツールです。\n\n'
                                   u'note):'
                                   u'ｽｷﾝｸﾗｽﾀｰ名 を そのまま XMLファイル名 として入力します。\n'
                                   u'note):'
                                   u'ｽｷﾆﾝｸﾞされていなくても構いません。\n'
                                   u'\n'
                                   u'note):'
                                   u'当ツールは、予め、デフォルトで\n'
                                   u'\t<mel>' + '---' * 15 + '\n'
                                   u'\tdeformerWeights -import \n\t\t-method "index" -deformer "ｽｷﾝｸﾗｽﾀｰ名" \n\t\t-path "ﾊﾟｽdirectory" "ｽｷﾝｸﾗｽﾀｰ名.xml";\n'
                                   u'\tskinCluster -e -forceNormalizeWeights "ｽｷﾝｸﾗｽﾀｰ名";\n'
                                   u'\t<cmds>' + '---' * 15 + '\n'
                                   u'\tcmds.deformerWeights(\'ｽｷﾝｸﾗｽﾀｰ名.xml\', \n\t\timport = True, path = \'ﾊﾟｽdirectory\', \n\t\tdeformer = \'ｽｷﾝｸﾗｽﾀｰ名\', method = \'index\')\n'
                                   u'\tcmds.skinCluster(\'ｽｷﾝｸﾗｽﾀｰ名\', e = True, \n\t\tforceNormalizeWeights = True)\n'
                                   u'相当で実行される設定です。')

        openFile_pbtnWid = QPushButton("Open File")
        # ボタンウィジェット を装飾
        # 設定を施す ###################################
        openFile_pbtnWid.setStatusTip(impDefWeitsOptUI_string)
        openFile_pbtnWid.setToolTip(impDefWeitsOptUI_string)
        container1_gdLay.addWidget(openFile_pbtnWid, 7, 1, 1, 1)
        # シグナル/スロット
        openFile_pbtnWid.clicked.connect(self.imp_open_file)

        # File path ############################################################
        impFilePath_string = 'File path:'
        impFilePath_lblWid = QLabel(impFilePath_string)
        # ラベルウィジェット を装飾
        impFilePath_lblWid.setAlignment(Qt.AlignRight)
        impFilePath_lblWid.setStatusTip(impDefWeitsOptUI_string)
        impFilePath_lblWid.setToolTip(impDefWeitsOptUI_string)
        container1_gdLay.addWidget(impFilePath_lblWid, 8, 0)  # itの列を2列に広げる
        # テキスト入力フィールド（LineEdit）を作成してレイアウトに追加
        self.impFilePathTxtFld_lEdtWid: QLineEdit = QLineEdit()
        # テキスト入力フィールド を装飾
        # 設定を施す ###################################
        self.impFilePathTxtFld_lEdtWid.setStatusTip(impDefWeitsOptUI_string)
        self.impFilePathTxtFld_lEdtWid.setToolTip(impDefWeitsOptUI_string)
        container1_gdLay.addWidget(self.impFilePathTxtFld_lEdtWid, 8, 1)

        # File name ############################################################
        impFileName_string = 'File name:'
        impFileName_lblWid = QLabel(impFileName_string)
        # ラベルウィジェット を装飾
        impFileName_lblWid.setAlignment(Qt.AlignRight)
        container1_gdLay.addWidget(impFileName_lblWid, 9, 0)  # itの列を2列に広げる
        # テキスト入力フィールド（LineEdit）を作成してレイアウトに追加
        self.impFileNameTxtFld_lEdtWid: QLineEdit = QLineEdit()
        # テキスト入力フィールド を装飾
        # 設定を施す ###################################
        self.impFileNameTxtFld_lEdtWid.setStatusTip(impDefWeitsOptUI_string)
        self.impFileNameTxtFld_lEdtWid.setToolTip(impDefWeitsOptUI_string)
        container1_gdLay.addWidget(self.impFileNameTxtFld_lEdtWid, 9, 1)

        # ボタンウィジェット(execute用) ###########################################
        imp_exe = 'Import'
        imp_btnA_exe_pbtnWid = QPushButton(imp_exe)
        # ボタンウィジェット を装飾
        # 設定を施す ###################################
        # 継承元既存からの再利用
        imp_btnA_exe_pbtnWid.setStyleSheet(self.bgcBlue3)  # 独自で色を設定
        # ボタンウィジェット の幅を設定
        # imp_btnA_exe_pbtnWid.setFixedWidth(150)  # 100は適切な幅に置き換えてください
        container1_gdLay.addWidget(imp_btnA_exe_pbtnWid, 10, 0, 1, 3)
        # シグナル/スロット
        imp_btnA_exe_pbtnWid.clicked.connect(partial(self.imp_exeButton_skinClusterWeightFile_inPut,
                                                     f'v: pBtn, {it}',
                                                     caseIndex
                                                     )
                                             )  # ツールの呼び出し
        # caseA1 ##################################################################### end

        # レイアウト(コンテナ1用) を装飾
        # 設定を施す ###################################
        container1_gdLay.setAlignment(Qt.AlignCenter)  # Center-align

        # ウィジェット(コンテナ1用) を レイアウト(大フレーム用)
        # に追加 ###################################### 追加して初めて表示されます     -表示-
        frame_layout.addWidget(container1_wid)
        # QWidget -Widget- ################################################## -Widget- end

        # 常に、レイアウト(大フレーム用) のトップに配置されるようにするため、垂直スペーサーを追加して間隔を制御します
        # spacer = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # frame_layout.addItem(spacer)
    # UIディテール 作成 ################################################################ end

    # export 関連 ######################################################### start
    def getSkinClusterBtn_directCheck(self, message_, caseIndex_):
        check_string = 'check'
        message(check_string)

        # 追加と変更と新規1
        # print(self.statusCurrent_scriptEditor)
        if self.statusCurrent_scriptEditor == 'closed':
            self.create_script_editor_and_show()
            # print(self.statusCurrent_scriptEditor)

        self.script_editor.append_default(check_string)

        sels = commonCheckSelection()
        if not sels:
            self.exp_skinnedGeoNameLabel_upDate('nothing selection !! \n'
                                                'please select anything.',
                                                callWarning = 'warning'
                                                )
            self.exp_skinnedGeoTypeLabel_upDate('', callWarning = 'warning')
            meaasge_warning_string = 'get SkinCluster name was not successful !!'
            message_warning(meaasge_warning_string)

            # 追加と変更と新規1
            # print(self.statusCurrent_scriptEditor)
            if self.statusCurrent_scriptEditor == 'closed':
                self.create_script_editor_and_show()
                # print(self.statusCurrent_scriptEditor)

            self.script_editor.append_warning(meaasge_warning_string)
            self.exp_fileNameTxtFld_upDate('')  # name_SC = ''
        else:
            hasShapeList = [commonCheckShape(sel) for sel in sels]

            if not all(hasShapeList):
                self.exp_skinnedGeoTypeLabel_upDate('not skinning geometry.',
                                                         callWarning = 'warning'
                                                         )
            else:
                name_SC = commonCheckSkinCluster()
                if not name_SC:
                    self.exp_skinnedGeoNameLabel_upDate('not skinning geometry.',
                                                             callWarning = 'warning'
                                                             )
                    self.exp_skinnedGeoTypeLabel_upDate(sels[0], callWarning = 'warning')
                else:
                    self.exp_skinnedGeoNameLabel_upDate(sels[0], callWarning = 'default')
                    self.exp_skinnedGeoTypeLabel_upDate(sels[0], callWarning = 'default')
                self.controller.execute_getSkinCluster(f'v: pBtn, {message_}', caseIndex_)
        # # print('ok')
        # self.controller.getSkinClusterBtn(f'v: pBtn, {message_}', caseIndex_)

    def exp_skinnedGeoNameLabel_upDate(self, sel, callWarning: str):
        if callWarning == 'warning':
            # ボタンウィジェット を装飾
            # 設定を施す ###################################
            self.exp_skinGeoName_lblWid.setStyleSheet(self.bgcRed)  # 独自で色を設定
            self.exp_skinGeoName_lblWid.setText(sel)
        else:
            # ボタンウィジェット を装飾
            # 設定を施す ###################################
            self.exp_skinGeoName_lblWid.setStyleSheet(self.bgcGray3)  # 独自で色を設定
            self.exp_skinGeoName_lblWid.setText(sel)

    def exp_skinnedGeoTypeLabel_upDate(self, sel, callWarning: str):
        if callWarning == 'warning':
            # ボタンウィジェット を装飾
            # 設定を施す ###################################
            self.exp_skinGeoType_lblWid.setStyleSheet(self.bgcRed)  # 独自で色を設定
            self.exp_skinGeoType_lblWid.setText('')
        else:
            # ボタンウィジェット を装飾
            # 設定を施す ###################################
            self.exp_skinGeoType_lblWid.setStyleSheet(self.bgcGray3)  # 独自で色を設定
            self.set_label_based_on_type(sel)  # typeを個別に判断し、self.exp_skinGeoType_lblWid.setText(***)へ反映する関数

    # typeを個別に判断し、self.exp_skinGeoType_lblWid.setText(***)へ反映する関数
    def set_label_based_on_type(self, sel):
        isCurve = commonCheckCurve(sel)
        isSurface = commonCheckSurface(sel)
        isMesh = commonCheckMesh(sel)
        if isCurve:
            self.exp_skinGeoType_lblWid.setText("nurbsCurve")
        elif isSurface:
            self.exp_skinGeoType_lblWid.setText("nurbsSurface")
        elif isMesh:
            self.exp_skinGeoType_lblWid.setText("mesh")
        else:
            # どれもTrueではない場合の処理
            pass  # 何もしない場合、または別の処理を追加する

    def exp_fileNameTxtFld_upDate(self, name_SC):
        upDate_string = 'upDate'
        message(upDate_string)

        # 追加と変更と新規1
        # print(self.statusCurrent_scriptEditor)
        if self.statusCurrent_scriptEditor == 'closed':
            self.create_script_editor_and_show()
            # print(self.statusCurrent_scriptEditor)

        self.script_editor.append_default(upDate_string)

        # print(f'-{name_SC}-')
        self.expFileNameTxtFld_lEdtWid.setText(name_SC)
        if not name_SC:
            meaasge_warning_string = 'get SkinCluster name was not successful !!'
            message_warning(meaasge_warning_string)

            # 追加と変更と新規1
            # print(self.statusCurrent_scriptEditor)
            if self.statusCurrent_scriptEditor == 'closed':
                self.create_script_editor_and_show()
                # print(self.statusCurrent_scriptEditor)

            self.script_editor.append_warning(meaasge_warning_string)
            # self.expFileNameTxtFld_lEdtWid
            # 設定を施す ###################################
            # 編集可能コントロール
            self.expFileNameTxtFld_lEdtWid.setReadOnly(False)
        else:
            message('get SkinCluster name was successful !!')
            # self.expFileNameTxtFld_lEdtWid
            # 設定を施す ###################################
            # 編集不可コントロール
            self.expFileNameTxtFld_lEdtWid.setReadOnly(True)

    def exp_browse_path(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if not directory:
            meaasge_warning_string = 'set directory was not successful !!'
            message_warning(meaasge_warning_string)

            # 追加と変更と新規1
            # print(self.statusCurrent_scriptEditor)
            if self.statusCurrent_scriptEditor == 'closed':
                self.create_script_editor_and_show()
                # print(self.statusCurrent_scriptEditor)

            self.script_editor.append_warning(meaasge_warning_string)
        else:
            self.expFilePathTxtFld_lEdtWid.setText(directory)
            self.exp_directory = directory
            message('set directory was successful !!')
            return directory

    def exp_fileNameTxtFld_get(self):
        name_SC = self.expFileNameTxtFld_lEdtWid.text()
        return name_SC

    def exp_filePathTxtFld_get(self):
        directory = self.expFilePathTxtFld_lEdtWid.text()
        return directory

    def exp_exeButton_skinClusterWeightFile_outPut(self, message_, caseIndex_):
        outPut_string = 'outPut'
        message(outPut_string)

        # 追加と変更と新規1
        # print(self.statusCurrent_scriptEditor)
        if self.statusCurrent_scriptEditor == 'closed':
            self.create_script_editor_and_show()
            # print(self.statusCurrent_scriptEditor)

        self.script_editor.append_default(outPut_string)

        # print(f'message_: {message_}')
        # print(f'caseIndex_: {caseIndex_}')

        self.exp_SCname = self.exp_fileNameTxtFld_get()   # 確実に、textField 入力済の 文字列を取得
        # print(f'self.exp_SCname: {self.exp_SCname}')
        self.exp_directory = self.exp_filePathTxtFld_get()   # 確実に、textField 入力済の 文字列を取得
        # print(f'self.exp_directory: {self.exp_directory}')
        sels = commonCheckSelection()
        # print(sels)
        if not sels:
            pass
            meaasge_warning_string = (u'skinCluster weight の export 作業です。'
                                      u'skinning された geometry '
                                      u'を一つ選択して実行してください。')
            message_warning(meaasge_warning_string)

            # 追加と変更と新規1
            # print(self.statusCurrent_scriptEditor)
            if self.statusCurrent_scriptEditor == 'closed':
                self.create_script_editor_and_show()
                # print(self.statusCurrent_scriptEditor)

            self.script_editor.append_warning(meaasge_warning_string)
        else:
            if len(sels) >= 2:
                pass
                meaasge_warning_string = (u'geometry を複数選択して実行してます。\n'
                                          u'一つだけ選択して実行してください。')
                message_warning(meaasge_warning_string)

                # 追加と変更と新規1
                # print(self.statusCurrent_scriptEditor)
                if self.statusCurrent_scriptEditor == 'closed':
                    self.create_script_editor_and_show()
                    # print(self.statusCurrent_scriptEditor)

                self.script_editor.append_warning(meaasge_warning_string)
            else:
                commonMessage_fileName = (u'File name が設定されていません。'
                                          u'上部の \'get SkinCluster name\' ボタンを押下し、'
                                          u'File name text field への設定を確実に行って、'
                                          u'実行を再開願います。 '
                                          )
                commonMessage_filePath = (u'File path が設定されていません。'
                                          u'右側の \'Set Directory\' ボタンを押下し、'
                                          u'File path text field への設定を確実に行って、'
                                          u'実行を再開願います。 '
                                          )
                # xx
                if self.exp_SCname == '' and self.exp_directory == r'':
                    meaasge_warning_string = commonMessage_fileName
                    message_warning(meaasge_warning_string)

                    # 追加と変更と新規1
                    # print(self.statusCurrent_scriptEditor)
                    if self.statusCurrent_scriptEditor == 'closed':
                        self.create_script_editor_and_show()
                        # print(self.statusCurrent_scriptEditor)

                    self.script_editor.append_warning(meaasge_warning_string)
                    meaasge_warning_string = commonMessage_filePath
                    message_warning(meaasge_warning_string)

                    # 追加と変更と新規1
                    # print(self.statusCurrent_scriptEditor)
                    if self.statusCurrent_scriptEditor == 'closed':
                        self.create_script_editor_and_show()
                        # print(self.statusCurrent_scriptEditor)

                    self.script_editor.append_warning(meaasge_warning_string)
                # ox
                elif self.exp_SCname and self.exp_directory == r'':
                    meaasge_warning_string = commonMessage_filePath
                    message_warning(meaasge_warning_string)

                    # 追加と変更と新規1
                    # print(self.statusCurrent_scriptEditor)
                    if self.statusCurrent_scriptEditor == 'closed':
                        self.create_script_editor_and_show()
                        # print(self.statusCurrent_scriptEditor)

                    self.script_editor.append_warning(meaasge_warning_string)
                # xo
                elif self.exp_SCname == '' and self.exp_directory:
                    meaasge_warning_string = commonMessage_fileName
                    message_warning(meaasge_warning_string)

                    # 追加と変更と新規1
                    # print(self.statusCurrent_scriptEditor)
                    if self.statusCurrent_scriptEditor == 'closed':
                        self.create_script_editor_and_show()
                        # print(self.statusCurrent_scriptEditor)

                    self.script_editor.append_warning(meaasge_warning_string)
                # oo
                elif self.exp_SCname and self.exp_directory:
                    # print('ok')
                    self.controller.executeBtn_export(message_, caseIndex_,
                                          self.exp_directory, self.exp_SCname
                                          )

    def exp_isFileExist_popUp_ui(self, caseIndex, directory, scName):
        file_name = f'{scName}.xml'
        isContinue_bool: bool = False

        titleName_ = 'IsFileExistHeadsUp'
        infoSummary_ = ('所定の directory\n'
                        f'{directory}\n'
                        f'へ 既に、{file_name} が存在しているようです。 \n'
                        'そのまま、既存ﾌｧｲﾙ を上書き Export するかどうか、ユーザーは判断願います。\n'
                        'OK / close どちらかを押下願います。'
                        )
        infoDetail_ = ('そのまま、既存ﾌｧｲﾙ に上書き Export されてしまいます。\n'
                       'よろしければ、OK ボタンを\n'
                       '拒否の場合は、close ボタンを\n'
                       '押下願います。'
                       )
        popup = CustomPopup(titleName = titleName_
                            , infoSummary = infoSummary_
                            , infoDetail = infoDetail_
                            )
        popup.ok_button.setStatusTip('既存ﾌｧｲﾙ を上書き Export の意')
        popup.ok_button.setToolTip('既存ﾌｧｲﾙ を上書き Export の意')
        popup.cls_button.setStatusTip('既存ﾌｧｲﾙ を上書き Export せず、一旦キャンセル の意')
        popup.cls_button.setToolTip('既存ﾌｧｲﾙ を上書き Export せず、一旦キャンセル の意')
        popup.exec_()

        # ポップアップの結果に応じて分岐
        if not popup.result:
            meaasge_warning_string = '上書き Export は、一旦キャンセルされました。'
            message_warning(meaasge_warning_string)

            # 追加と変更と新規1
            # print(self.statusCurrent_scriptEditor)
            if self.statusCurrent_scriptEditor == 'closed':
                self.create_script_editor_and_show()
                # print(self.statusCurrent_scriptEditor)

            self.script_editor.append_warning(meaasge_warning_string)
            # ウィンドウが閉じられた場合の処理
            isContinue_bool: bool = False
        else:
            message('上書き Export は、そのまま継続で実行されます。')
            # OKボタンが押された場合の処理
            isContinue_bool: bool = True
        return isContinue_bool
    # export 関連 ######################################################### end

    # import 関連 ######################################################### start
    def imp_open_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self,
                                                   "Open XML File", "",
                                                   "XML Files (*.xml)"
                                                   )
        if not file_path:
            meaasge_warning_string = 'open file was not successful !!'
            message_warning(meaasge_warning_string)

            # 追加と変更と新規1
            # print(self.statusCurrent_scriptEditor)
            if self.statusCurrent_scriptEditor == 'closed':
                self.create_script_editor_and_show()
                # print(self.statusCurrent_scriptEditor)

            self.script_editor.append_warning(meaasge_warning_string)
        else:
            # ファイルパスをディレクトリとファイル名に分割
            directory, file_name = os.path.split(file_path)
            # print("ディレクトリ:", directory)
            # print("ファイル名:", file_name)
            self.impFilePathTxtFld_lEdtWid.setText(directory)
            self.impFileNameTxtFld_lEdtWid.setText(file_name)
            self.imp_directory = directory
            self.imp_FileName = file_name
            message('open file was successful !!')

    def imp_filePathTxtFld_get(self):
        directory = self.impFilePathTxtFld_lEdtWid.text()
        return directory

    def imp_fileNameTxtFld_get(self):
        fileName = self.impFileNameTxtFld_lEdtWid.text()
        return fileName

    def imp_exeButton_skinClusterWeightFile_inPut(self, message_, caseIndex_):
        inPut_string = 'inPut'
        message(inPut_string)

        # 追加と変更と新規1
        # print(self.statusCurrent_scriptEditor)
        if self.statusCurrent_scriptEditor == 'closed':
            self.create_script_editor_and_show()
            # print(self.statusCurrent_scriptEditor)

        self.script_editor.append_default(inPut_string)

        # print(f'message_: {message_}')
        # print(f'caseIndex_: {caseIndex_}')

        self.imp_directory = self.imp_filePathTxtFld_get()   # 確実に、textField 入力済の 文字列を取得
        # print(f'self.imp_directory: {self.imp_directory}')
        self.imp_FileName = self.imp_fileNameTxtFld_get()   # 確実に、textField 入力済の 文字列を取得
        # print(f'self.imp_FileName: {self.imp_FileName}')
        sels = commonCheckSelection()
        # print(sels)
        if not sels:
            pass
            meaasge_warning_string = (u'skinCluster weight の import 作業です。'
                                      u'import weight を施したい skinning 済の geometry 、'
                                      u'もしくは、'
                                      u'これから import weight を施したい skinning していない geometry 、'
                                      u'を一つ選択して実行してください。')
            message_warning(meaasge_warning_string)

            # 追加と変更と新規1
            # print(self.statusCurrent_scriptEditor)
            if self.statusCurrent_scriptEditor == 'closed':
                self.create_script_editor_and_show()
                # print(self.statusCurrent_scriptEditor)

            self.script_editor.append_warning(meaasge_warning_string)
        else:
            if len(sels) >= 2:
                pass
                meaasge_warning_string = (u'geometry を複数選択して実行してます。\n'
                                          u'一つだけ選択して実行してください。'
                                          )
                message_warning(meaasge_warning_string)

                # 追加と変更と新規1
                # print(self.statusCurrent_scriptEditor)
                if self.statusCurrent_scriptEditor == 'closed':
                    self.create_script_editor_and_show()
                    # print(self.statusCurrent_scriptEditor)

                self.script_editor.append_warning(meaasge_warning_string)
            else:
                commonMessage = (u'File name, File path が設定されていません。'
                                 u'上部の \'Open File\' ボタンを押下し、'
                                 u'File name text field, File path text field '
                                 u'への設定を確実に行って、実行を再開願います。 '
                                 )
                if self.imp_directory == r'' or self.imp_FileName == '':
                    meaasge_warning_string = commonMessage
                    message_warning(meaasge_warning_string)

                    # 追加と変更と新規1
                    # print(self.statusCurrent_scriptEditor)
                    if self.statusCurrent_scriptEditor == 'closed':
                        self.create_script_editor_and_show()
                        # print(self.statusCurrent_scriptEditor)

                    self.script_editor.append_warning(meaasge_warning_string)
                elif self.imp_directory and self.imp_FileName:
                    self.controller.executeBtn_import(message_, caseIndex_,
                                                      self.imp_directory,
                                                      self.imp_FileName
                                                      )
    # import 関連 ######################################################### end

    # show メソッド 組み込み関数 は 継承元 Tpl4PySide2_Type1_View から再利用
    # def show(self):
    #     pass

    # CustomScriptEditor クラスの closedシグナル が発行されると 当メソッド が呼び出されます
    @Slot()
    def on_script_editor_closed(self):
        message_warning("Script editor was hided. Not closed !!")
        self.statusCurrent_scriptEditor = 'closed'
        # # QTextEdit の内容を保存
        # self.script_editor_content = self.script_editor.text_edit.toPlainText()
        # print(self.script_editor_content)
        return self.statusCurrent_scriptEditor

    # 1. UI-1. メニュー コマンド群 ###################################################### start
    # オーバーライド
    # Save Settings 関数 #################################
    # メモ: (PyMel版)Model: editMenuSaveSettingsCmd に相当
    # オリジナルメソッド
    # 基本となるUI構成で不可欠となる要素 8つ の内、以下 1つ を実行しています
    # <UI要素 4>. UI設定の 保存 の機能
    # UI設定の保存用 関数
    def saveSettings(self):
        u""" < UI設定の保存用 関数 です >

        オリジナルメソッド

        基本となるUI構成で不可欠となる要素 8つ の内、以下 1つ を実行しています
            <UI要素 4>. UI設定の 保存 の機能
        """
        print('###' * 10)
        print(f'Save...'
              f'\nNote: always overwriting save.. mode'
              )
        # サイズの情報を 保存
        self._settings.setValue(self.iniFileParam['geo_iFP'], self.saveGeometry())  # ウインドウの位置と大きさを 可変byte配列 で 取得 し、iniFile へ 可変byte配列 を セット
        # print(f'\tSave a \n\t\t'
        #       f'{self.iniFileParam["geo_iFP"]} \n\t\t\t'
        #       f'param: {...}'
        #       )

        # expFileNameTxtFld LineEditの情報を 保存
        exp_txtFld_A_text = self.expFileNameTxtFld_lEdtWid.text()  # ウィジェットフィールド から textメソッド 使用で text を 取得
        self._settings.setValue(
            self.iniFileParam_txtFld_ExpImp['exp_txtFld_A_iFP'],
            exp_txtFld_A_text
            )  # iniFile へ text を セット
        # expFilePathTxtFld LineEditの情報を 保存
        exp_txtFld_B_text = self.expFilePathTxtFld_lEdtWid.text()  # ウィジェットフィールド から textメソッド 使用で text を 取得
        self._settings.setValue(
            self.iniFileParam_txtFld_ExpImp['exp_txtFld_B_iFP'],
            exp_txtFld_B_text
            )  # iniFile へ text を セット
        # impFileNameTxtFld LineEditの情報を 保存
        imp_txtFld_A_text = self.impFileNameTxtFld_lEdtWid.text()  # ウィジェットフィールド から textメソッド 使用で text を 取得
        self._settings.setValue(
            self.iniFileParam_txtFld_ExpImp['imp_txtFld_A_iFP'],
            imp_txtFld_A_text
            )  # iniFile へ text を セット
        # impFilePathTxtFld LineEditの情報を 保存
        imp_txtFld_B_text = self.impFilePathTxtFld_lEdtWid.text()  # ウィジェットフィールド から textメソッド 使用で text を 取得
        self._settings.setValue(
            self.iniFileParam_txtFld_ExpImp['imp_txtFld_B_iFP'],
            imp_txtFld_B_text
            )  # iniFile へ text を セット

        print(f'\tSave a .INI file, at \n\t\t{self.filename}')

    # saveSettings_geoOnly メソッド は 継承元 Tpl4PySide2_Type1_View から再利用
    # def show(self):
    #     pass

    # オーバーライド
    # Reset 実行 関数 #####################################
    # メモ: (PyMel版)Model: set_default_value_toOptionVar に相当
    # メモ: (PyMel版)View: editMenuReloadCmd に相当
    # オリジナルメソッド
    # Reset 実行 関数(UIのサイズは保持)
    def resetSettings(self):
        u""" < Reset 実行 関数 です >

        オリジナルメソッド

        .. note::
            UIの入力箇所を全てクリアーします
                見た目がUIの再描画リロードライクにしています
            因みに、UIのサイズは保持します

        :param central_wid_: self.central_wid # セントラルウィジェット に相当します
        """
        # old style ################################################
        # print(args)
        # self.__init__()  # すべて、元の初期値に戻す
        # self.set_default_value_toOptionVar()  # optionVar の value を default に戻す操作
        # pm.evalDeferred(lambda *args: self.create())  # refresh UI <---- ここ重要!!

        # new style ################################################
        self.doResetStat = True
        # print('--- def resetSettings(self): ...')
        # print(f'do reset?: {self.doResetStatYesOrNo_byString(self.doResetStat)}')
        print('###' * 10)
        print(f'\nReset all input value...')

        message('リセットは実行されました。')
        # OKボタンが押された場合の処理

        # .iniファイル の 内容を クリア します
        self.iniFS.clear_ini_file()
        # まずは一旦保存
        self.saveSettings_geoOnly()  # UI設定のみ の保存用 関数 実行 # note): オリジナルから引用し再利用
        print(u'一旦saveGeometry..のみ実行')

        # 入力フィールドを持つ子供Widgetのみのカレントの情報一括クリアー 関数 実行
        # self.clearAllValue_toAllWidget(central_wid_)

        # self.clearAllValue_toAllWidget(central_wid_) の代替え案 ########## start
        model_ = SkinWeightExpImp_Modl()
        view_ = SkinWeightExpImp_View(model_)
        SkinWeightExpImp_Ctlr(view_, model_)
        # print('--- def resetSettings(view_): ...')
        # print(f'do reset?: {view_.doResetStatYesOrNo_byString(view_.doResetStat)}')
        # self.clearAllValue_toAllWidget(central_wid_) の代替え案 ########## end

        # self.saveSettings()  # UI設定の保存用 関数 実行

    # オリジナルメソッド
    # 入力フィールドを持つ子供Widgetのみのカレントの情報一括クリアー 関数
    def clearAllValue_toAllWidget(self, central_wid_):
        u""" < 入力フィールドを持つ子供Widgetのみのカレントの情報一括クリアー 関数 です >

        オリジナルメソッド

        .. note:: 情報一括クリアー には以下の条件を満たす必要があります

            1. QLabel を対象として
                - 全てクリアー対象から除外(暫定。変更大いにあり！)
                    対象: 現状 common情報 群
            2. QPushButton を対象として
                - 特定のボタンはクリアーから除外
                    対象: ['Execute', 'Reset', 'Close']
                - もし child が clear メソッド を持ち、
                    かつそれが呼び出し可能である場合、
                        clear メソッド を呼び出しています。
                - もし child が setChecked メソッド を持ち、
                    かつそれが呼び出し可能である場合、
                        setChecked(False) を呼び出しています。
                - もし child が setStyleSheet メソッド を持ち、
                    かつそれが呼び出し可能である場合、
                        背景色やテキストの設定をクリアして基に戻しています。
                - 再帰的に同じ処理を行います。
            3. その他の場合はクリアー対象の処理
                - もし child が clear メソッド を持ち、
                    かつそれが呼び出し可能である場合、
                        clear メソッド を呼び出しています。
                - もし child が setChecked メソッド を持ち、
                    かつそれが呼び出し可能である場合、
                        setChecked(False) を呼び出しています。
                - もし child が QComboBox の インスタンス である場合、
                    setCurrentIndex(-1) を呼び出しています。
                - 再帰的に同じ処理を行います。

        メインとなる Widget(central_wid_) にぶら下がっている、
            入力フィールドを持つ 子供の Widget のみ、に特化しています
        それらに対して、カレントの情報を一括で クリアー する
            メソッドとなります

        :param central_wid_: self.central_wid # ここでは セントラルウィジェット に相当します
        """
        for child in central_wid_.findChildren(QWidget):
            # 1.
            if isinstance(child, QLabel):
                continue
            # 2.
            elif isinstance(child, QPushButton):
                # 特定のボタンはクリアーから除外
                if child.text() in ['Execute', 'Reset', 'Close']:
                    continue
                # クリアー対象の処理
                if hasattr(child, 'clear') and callable(getattr(child, 'clear')):
                    child.clear()
                if hasattr(child, 'setChecked') and callable(getattr(child, 'setChecked')):
                    child.setChecked(False)
                if hasattr(child, 'setStyleSheet') and callable(getattr(child, 'setStyleSheet')):
                    child.setStyleSheet("")
                self.clearAllValue_toAllWidget(child)
            # 3. その他の場合はクリアー対象の処理
            else:
                if hasattr(child, 'clear') and callable(getattr(child, 'clear')):
                    child.clear()
                if hasattr(child, 'setChecked') and callable(getattr(child, 'setChecked')):
                    child.setChecked(False)
                if isinstance(child, QComboBox):
                    child.setCurrentIndex(-1)
                self.clearAllValue_toAllWidget(child)

    # オーバーライド
    # Help 実行 関数 #####################################
    def helpMenuCmd(self, *args):
        u""" < Help 実行 関数 です > """
        # cmds.launch(web = 'http://help.autodesk.com/cloudhelp/2016/'
        #                   'JPN/Maya-Tech-Docs/CommandsPython/index.html'
        #             )
        help(docstring)
        message(f'v: {args[0]}' + f', For more information, see Script Editor'
                )  # message(args[0])

    # Close 実行 関数 #####################################
    # オーバーライド
    # closeEvent メソッド 組み込み関数
    def closeEvent(self, event):
        u""" < (オーバーライド) closeEvent メソッド 組み込み関数 です >

        オーバーライド

        .. note::
            当該 closeEvent メソッド は、基は組み込み関数であり、 イベントハンドラー です
                閉じる要求を受信したときにトップレベル ウィンドウに対してのみ呼び出されます
            self.close でも発動します

        実行の手順
            #. UI設定の保存用オリジナルメソッド「saveSettings」を実行し、設定を保存します
            #. 次に、閉じる要求を受信したときにトップレベル ウィンドウに対してのみ呼び出されます
        """
        # print(event)
        self.saveSettings()  # UI設定の保存用オリジナルメソッド
        # # super(SkinWeightExpImp_View, self).closeEvent(event)  # ここは無くても上手く発動するようです

        # # カスタムの専用 スクリプトエディタ を同時に閉じます
        if self.statusCurrent_scriptEditor == 'closed':
            pass
        else:
            message("Script editor also completely closed and exited at the same time.")
            # self.script_editor.close()

            # スクリプトエディタを完全に閉じる
            # CustomScriptEditorのインスタンスはQtのイベントループが次に実行されるときに遅延削除されます。
            # これにより、CustomScriptEditorのウィジェットが閉じられ、
            # その後のコードがそのウィジェットを参照しないことを保証できる。
            # CustomScriptEditorのインスタンスは完全に削除されるため、
            # その状態（例えばQTextEditの内容）は保持されない。
            # その状態を保持するためには、何らかの形でその状態を保存し、
            # 新しいCustomScriptEditorのインスタンスが作成されるときにその状態を復元する必要がある
            self.script_editor.deleteLater()
    # 1. UI-1. メニュー コマンド群 ######################################################## end

    # 4. UI-4. OptionVar を利用したパラメータ管理 コマンド群 ############################### start
    # オーバーライド
    # メモ: (PyMel版)Model: restoreOptionVarCmd に相当
    # オリジナルメソッド
    # 基本となるUI構成で不可欠となる要素 8つ の内、以下 1つ を実行しています
    # <UI要素 4>. UI設定の 復元 の機能
    # UI設定の復元用 関数
    def restore(self):
        u""" < UI設定の復元用 関数 です >

        オリジナルメソッド

        基本となるUI構成で不可欠となる要素 8つ の内、以下 1つ を実行しています
            <UI要素 4>. UI設定の 復元 の機能
        .. note::
            - 継承することを前提に考えると、「__init__」で復元するのは好ましくありません
            - self._settings.value から取得するデータは、
                restoreGeometry以外は、型が string です！！
        """
        # restore = 'Restore'
        # print(f'v: direct def restore execute, {restore}')
        # self.controller.restoreExecute(restore)
        print('###' * 10)
        print(f'Restore...')

        # サイズの情報を 復元
        self.restoreGeometry(self._settings.value(self.iniFileParam['geo_iFP']))  # iniFile から 可変byte配列 を ゲット し、サイズの情報 を 復元操作
        # print(f'\tRestore a \n\t\t'
        #       f'{self.iniFileParam["geo_iFP"]} \n\t\t\t'
        #       f'param: {...}'
        #       )

        # expFileNameTxtFld LineEditの情報を 復元
        exp_txtFld_A_text = self._settings.value(
            self.iniFileParam_txtFld_ExpImp['exp_txtFld_A_iFP']
            )  # iniFile から text を ゲット
        if exp_txtFld_A_text:
            self.expFileNameTxtFld_lEdtWid.setText(exp_txtFld_A_text)  # ウィジェットフィールド へ setTextメソッド 使用で text を 復元操作
        # expFilePathTxtFld LineEditの情報を 復元
        exp_txtFld_B_text = self._settings.value(
            self.iniFileParam_txtFld_ExpImp['exp_txtFld_B_iFP']
            )  # iniFile から text を ゲット
        if exp_txtFld_B_text:
            self.expFilePathTxtFld_lEdtWid.setText(exp_txtFld_B_text)  # ウィジェットフィールド へ setTextメソッド 使用で text を 復元操作
        # impFileNameTxtFld LineEditの情報を 復元
        imp_txtFld_A_text = self._settings.value(
            self.iniFileParam_txtFld_ExpImp['imp_txtFld_A_iFP']
            )  # iniFile から text を ゲット
        if imp_txtFld_A_text:
            self.impFileNameTxtFld_lEdtWid.setText(imp_txtFld_A_text)  # ウィジェットフィールド へ setTextメソッド 使用で text を 復元操作
        # impFilePathTxtFld LineEditの情報を 復元
        imp_txtFld_B_text = self._settings.value(
            self.iniFileParam_txtFld_ExpImp['imp_txtFld_B_iFP']
            )  # iniFile から text を ゲット
        if imp_txtFld_B_text:
            self.impFilePathTxtFld_lEdtWid.setText(imp_txtFld_B_text)  # ウィジェットフィールド へ setTextメソッド 使用で text を 復元操作

        print(f'\tRestore a .INI file, from \n\t\t{self.filename}')
    # 4. UI-4. OptionVar を利用したパラメータ管理 コマンド群 ############################### end

    # 新規
    def cal_alwaysHeight_window(self):
        # x, y, width, height: Tuple[int, int, int, int]
        # 初期： QMainWindow のサイズ
        start_size = list(self.geometry().getRect())  # タプルをリストに変換

        # 縦のみの合計サイズを抽出
        # Calculate the total height of all containers
        total_height = sum(self.container_heights.values())
        # Set the new height
        start_size[3] = total_height
        # アップデート： 全ての コンテナー が解放されている時、ぴったりと QMainWindow の最低限必要なサイズにフィットさせるサイズ
        upDate_size = tuple(start_size)  # リストをタプルに変換
        self.setGeometry(*upDate_size)

    # 新規
    def cal_alwaysHeight_containerAll(self, container_geo_name):
        # x, y, width, height: Tuple[int, int, int, int]

        # # check
        # # current： container_geo_name のサイズ
        # print(f'I am \n\t{container_geo_name}')
        # print(f'type is \n\t{type(container_geo_name)}')
        currentSize_frame_list = list(container_geo_name.geometry().getRect())  # タプルをリストに変換
        currentHeight_frame_ = currentSize_frame_list[3]
        # print(f'currentFrame_currentHeight: {currentHeight_frame_}')

        # Save the new height of the frame
        self.container_heights[container_geo_name] = currentHeight_frame_
        # print(self.container_heights)

        # Calculate the total height of all frames
        total_height = sum(self.container_heights.values())
        # print(f'total_height: {total_height}')

        # temp
        # Get the current width size of the window
        current_width = self.geometry().width()
        # Set the new height
        temp_height = total_height
        # Resize the window, keeping the current width and changing the height
        self.resize(current_width, temp_height)
        # temp_size = list(self.geometry().getRect())  # タプルをリストに変換
        # print(f'temp_size: {temp_size}')

        # final
        # 一旦フィットさせる。但し、全体的にフィットしてしまうので、ここで終わりにはしない！
        self.adjustSize()
        # Get the final height size of the window
        final_height = self.geometry().height()
        adjust = 20
        self.resize(current_width, final_height - adjust)
        # final_size = list(self.geometry().getRect())  # タプルをリストに変換
        # print(f'final_size: {final_size}')


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
