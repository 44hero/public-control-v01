# -*- coding: utf-8 -*-

u"""
templateForPySide2_type2_View.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -1.0-
:Date: 2024/03/07

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PySide2 version: 5.15.2

-リマインダ-
    done: 2024/03/07
        新規
            - 概要:
            - 詳細:

                #.
                    従来の、
                        UIのサイズを保存する、
                            `windowPrefs.mel`
                        Maya のさまざまな呼び出しに存在する変数を設定および照会できる、プリファレンスの一部である、
                            maya独自規格｛optionVar」
                    以上２つの Maya専用の 保存参照規格 からの、代替え案として、
                        PySide2 規格 の .iniファイル
                    を使用したやり方です。

                    ::

                        ファイルの保存先には、運用ルールが必要です。。。
                        ここでは、「マイドキュメント/maya/versionNumber」に
                            フォルダ「f'{prefix}_{commonName}'」を作り、
                                設定ファイルが保存されていくようにしています。
                        ファイル名はクラス変数にして、継承したクラスで変更できるようにします

                    基本となるUI構成で不可欠となる要素 8つ は以下です
                        - <UI要素 1>. UIを、Maya window 画面の前面にする
                        - <UI要素 2>. UIの title設定 と、新規での ポジションとサイズ設定
                        - <UI要素 3>. UI設定の 保存 と 復元 の機能を 何らかで実現する
                        - <UI要素 4>. UI設定の 保存 と 復元 の機能
                            Note): オリジナルメソッド ｛saveSettings」, 「restore」 で実現
                        - <UI要素 5>. UIの 重複表示の回避
                        - <UI要素 6>. UIの 見た目の統一
                        - <UI要素 7>. -Pyside2特有事項- UI の close 時に delete されるようにする
                        - <UI要素 8>. UIの window name (objectName) 設定

                #.
                    UIのリセット描画も再考

                    現行では、完全な新規インスタンス 作成による 新規UI描画 に成功してはいるものの、
                        場合によっては、
                    コメントアウト行の泥臭い手法に変更せざるを得ないかも知れません。

                    ::

                        def resetSettings(self, central_wid_):
                            ...

        version = '-1.0-'
"""
# 標準ライブラリ #################################################################
from functools import partial
from pprint import pprint
from typing import Tuple, List
from collections import OrderedDict
import inspect

# サードパーティライブラリ #########################################################
# from maya import OpenMayaUI, cmds
from PySide2.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout,
                               QMainWindow, QRadioButton, QTabWidget, QWidget,
                               QHBoxLayout, QVBoxLayout, QPushButton, QAction,
                               QFrame, QLabel, QSpacerItem, QSizePolicy,
                               QMessageBox
                               )
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt, Slot

# ローカルで作成したモジュール ######################################################
import YO_utilityTools.TemplateForPySide2.type2.config as docstring
from .templateForPySide2_type2_Ctlr import Tpl4PySide2_Type2_Ctlr
from .templateForPySide2_type2_Modl import Tpl4PySide2_Type2_Modl
# basic_configuration(基本構成)
from .config import SPACE, TITLE, VERSION

# shiboken2 独自モジュール
from ..qt import getMayaWindow  # 利用時は、getMayaWindow()

from ..pyside2IniFileSetting import IniFileSetting
from ..MyTabWidget import MyTabWidget
from ..Container import Container
# 汎用ライブラリー の使用 #################################################### start
from ...lib.message import message
from ...lib.message_warning import message_warning
from ...lib.yoGetAttributeFromModule import GetAttrFrmMod
# 汎用ライブラリー の使用 #################################################### end


class CustomPopup(QDialog):
    def __init__(self
                 , titleName: str
                 , infoSummary: str, infoDetail: str
                 , parent = None):
        super().__init__(parent)
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
        ok_button = QPushButton('OK')
        ok_button.clicked.connect(self.accept)
        cls_button = QPushButton('Close')
        cls_button.clicked.connect(self.close)
        gLay.addWidget(ok_button, 0, 0)
        gLay.addWidget(cls_button, 0, 1)

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


class Tpl4PySide2_Type2_View(QMainWindow):
    u""" < GUIウィンドウを作成するための Viewクラス です >

    ::

      UIを作成するためのメソッドや、UIの更新を行うためのメソッドを実装します。

      GUIウィンドウを作成するための PySide2 コードが含まれます。
        Viewクラスのコンストラクターは、Modelオブジェクト への参照を受け取ります。
            View クラスは GUIウィンドウ を作成し、そのウィンドウ内の要素を更新するためのメソッドを提供します。

    .. note::
        従来の、
            UIのサイズを保存する、
                `windowPrefs.mel`
            Maya のさまざまな呼び出しに存在する変数を設定および照会できる、プリファレンスの一部である、
                maya独自規格｛optionVar」
        以上２つの Maya専用の 保存参照規格 からの、代替え案として、
            PySide2 規格 の .iniファイル
        を使用したやり方です。

    ::

        ファイルの保存先には、運用ルールが必要です。。。
        ここでは、「マイドキュメント/maya/versionNumber」に
            フォルダ「f'{prefix}_{commonName}'」を作り、
                設定ファイルが保存されていくようにしています。
        ファイル名はクラス変数にして、継承したクラスで変更できるようにします

    基本となるUI構成で不可欠となる要素 8つ は以下です
        - <UI要素 1>. UIを、Maya window 画面の前面にする
        - <UI要素 2>. UIの title設定 と、新規での ポジションとサイズ設定
        - <UI要素 3>. UI設定の 保存 と 復元 の機能を 何らかで実現する
        - <UI要素 4>. UI設定の 保存 と 復元 の機能
            Note): オリジナルメソッド ｛saveSettings」, 「restore」 で実現
        - <UI要素 5>. UIの 重複表示の回避
        - <UI要素 6>. UIの 見た目の統一
        - <UI要素 7>. -Pyside2特有事項- UI の close 時に delete されるようにする
        - <UI要素 8>. UIの window name (objectName) 設定
    ######

        基本となるUI要素は以下の 6つ
            - UI-0. 重複しないウインドウ

            - UI-1. commonメニュー

            - UI-2. メインLayout + common情報 + 追加オプション

            - UI-3. ボタンLayout + common底面ボタン3つ

            - UI-4. OptionVar を利用したパラメータ管理

            - (5. スクリプトベースコマンド入力への対応)

        構成要素である以下の1群のみ一部ここ View へ移動
            - 1. UI-1. メニュー コマンド群

    ######
    """
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

        super(Tpl4PySide2_Type2_View, self).__init__(parent, flags)

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
        self.infoSummary = (u'XXXのツール\n'
                            u'の バージョンYYY(ZZZ版) です。')
        self.infoDetail = u'AAAのBBBをCCCしました。'
        # ######################################################################

        # <UI要素 3>.
        # コンストラクタのまとまり1_.iniファイル 設定
        self.constructorChunk1_iniFileSetting()

        # コンストラクタのまとまり2_.iniファイルのパラメーター 設定
        self.constructorChunk2_iniFileParam()
        # コンストラクタのまとまり3_色とアイコン 設定
        self.constructorChunk3_colorAndIcon()
        # コンストラクタのまとまり4_その他A 設定
        self.constructorChunk4_otherA()

        # コンストラクタのまとまり5_その他B タブ及びタブのフレーム関連 設定
        self.constructorChunk5_otherB()

    # コンストラクタのまとまり1_.iniファイル 設定
    def constructorChunk1_iniFileSetting(self):
        u""" < コンストラクタのまとまり1_.iniファイル 設定 >

        ######################
        """
        # .iniファイルの設定 ########################################################### start
        self.iniFS = IniFileSetting(self.title)  # pyside2IniFileSetting モジュール
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
                             'tab_wid_selection_iFP': 'tab_wid_selection',
                             'contA_wid_expStat_iFP': 'contA_wid_expStat',
                             'contB_wid_expStat_iFP': 'contB_wid_expStat',
                             'contC_wid_expStat_iFP': 'contC_wid_expStat',
                             'contD_wid_expStat_iFP': 'contD_wid_expStat',
                             'cBrbtnB_wid_isChecked_iFP': 'cBrbtnB_wid_isChecked',
                             'cDrbtnD_wid_isChecked_iFP': 'cDrbtnD_wid_isChecked',
                             }
        self.iFP_oDict = OrderedDict(self.iniFileParam)  # 順序付き辞書 定義
        # .iniファイルのパラメーター設定 ##################################### end

    # コンストラクタのまとまり3_色とアイコン 設定
    def constructorChunk3_colorAndIcon(self):
        u""" < コンストラクタのまとまり3_色とアイコン 設定 >

        ######################
        """
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
        # 独自で色を設定2
        self.bgcBlue3 = "background-color:deepskyblue; color: black"
        self.bgcWhite = "background-color: white;"

        # アイコンを設定
        self.saveSettingsIcon = None
        self.saveSettingsIcon = self.saveSettingsIcon if self.saveSettingsIcon is not None else ':/save.png'  # maya icon を使用しています
        self.resetSettingsIcon = None
        self.resetSettingsIcon = self.resetSettingsIcon if self.resetSettingsIcon is not None else ':/RS_refresh_layer.png'  # maya icon を使用しています
        self.closeIcon = None
        self.closeIcon = self.closeIcon if self.closeIcon is not None else ':/restoreClosedTab.png'  # maya icon を使用しています
        self.helpIcon = None
        self.helpIcon = self.helpIcon if self.helpIcon is not None else ':/help.png'  # maya icon を使用しています

    # コンストラクタのまとまり4_その他A 設定
    def constructorChunk4_otherA(self):
        u""" < コンストラクタのまとまり4_その他A 設定 >

        ######################
        """
        # container1用 ボタンの情報のリスト まとめ
        self.button_info: List[str] = ['buttonA', 'buttonB', 'buttonC']

        self.doResetStat = False  # reset ボタン 及び reset メニュー の選択状況の 記録

        # コンテナ 情報のリスト まとめ
        self.cont_heights_dict = {}  # tab毎 で作成されている コンテナ の高さを 辞書登録
        self.cont_wid_list = []  # 作成されている 全てのコンテナ の高さの リスト
        self.cont_total_height = 0  # tab毎 で作成されている コンテナ の高さの 合計
        self.contExist_tab_dict = {}  # コンテナが存在するtabの有無 辞書
        self.contExist_tab_oDict = None  # コンテナが存在するtabの有無 辞書 順序付き辞書 定義

        # RadioButton 情報のリスト まとめ
        self.rbtn_wid_list = []  # 作成されている 全てのコンテナ の高さの リスト

    # コンストラクタのまとまり5_その他B タブ及びタブのフレーム関連 設定
    def constructorChunk5_otherB(self):
        u""" < コンストラクタのまとまり5_その他B タブ及びタブのフレーム関連 設定>

        .. note::
            self.tabs の数
                と
            self._frame_gdLays_list  の数
                は
            常に一致します
        """
        # 作成された tabウィジェット 関連をリスト登録 ################################
        # tab widget
        self.tab_wid_: QTabWidget = None  # createUI()で一度作成実行された MyTabWidget(tabCount = ***) を登録
        # 子tab widget リスト 定義
        self.tabs: List[QTabWidget] = []  # BTW): 子tab widget の数と tabCount は必ず一致します
        # 子tab widget の 子frame widget リスト 定義
        self.frames: List[QFrame] = []
        # 子tab widget の 子frame widget の 子grid layout リスト 定義
        self._frame_gdLays_list: List[QGridLayout] = []  # BTW): frame grid layout の数と tabCount は必ず一致します
        # 暫定 子tabラベル名 のリスト 定義
        self.tabLabelName_list_old: List[str] = []
        # 新規 子tabラベル名 の辞書 定義
        self.tabLabelName_dict_new = {'A': 'test です',
                                      'B': 'test2 です',
                                      'C': 'test3 です'
                                      }  # note): 数は、tabCount と等数がベスト
        # 新規 子tabラベル名 の順序付き辞書として 定義
        self.tabLabelName_oDict_new = OrderedDict(self.tabLabelName_dict_new)
        # タブの数 保存 定義
        self.tabCount__ = 0
        # クリックされたタブのインデックスを保存するための属性を追加します。
        self.clicked_tab_index = None

        # 作成された RadioButton ウィジェット 関連をリスト登録 #######################
        self.rbtn_wid_list = []

    # オリジナルメソッド
    # 重複ウィンドウの回避関数
    def _duplicateWindowAvoidFunction(self, winName: str):
        u""" < 重複ウィンドウの回避関数 です >

        オリジナルメソッド

        :param str winName: self.win # window ui name に相当します
        """
        widgets = QApplication.allWidgets()
        for w in widgets:
            if w.objectName() == winName:
                # w.close()
                w.deleteLater()

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
        self.setWindowTitle(self.title + self.space + self.version)  # <- window の title名 設定
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
        # # type2
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

        .. note::
            以下のコード行の引数にて、tab数を指定してください
            ::

                self.displayOptions(main_layout = ***, tabCount_ = 4)

            の引数 tabCount_
        """
        self._windowBasicSettings()  # Window基本設定

        self.controller = self.model.controller  # 和えて明示しています。無くてもこのケースでは実行可。

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
        # self.frame_frWid.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # # まとまりA
        # # 大フレーム群 に収まっているものです ######################################## start
        # # UI-2. common情報
        # # 設定を施す ###################################
        self.commonInformation(main_layout = self.frame_vbxLay)  # ############################ UI-2. common情報
        tabCount__ = 4
        # # UI-2. 追加オプションのまとまり
        # # 設定を施す ###################################
        self.displayOptions(main_layout = self.frame_vbxLay, tabCount_ = tabCount__)  # #################### UI-2. 追加オプションのまとまり

        # # 大フレーム群 に収まっているものです ######################################## end

        # 3.2): 底面ボタン群 -Layout- ###################################$##### -Layout- start
        # セントラルウィジェット 内に 水平レイアウト(底面ボタン用)
        # を 直接 作成 追加 ###################################### 一遍に行えます
        self.button_hbxLay = QHBoxLayout(self.central_wid)  # レイアウト(底面ボタン用)

        # まとまりB
        # 底面ボタン群 です ####################################################### start
        # UI-3. common底面ボタン3つ
        # 設定を施す ###################################
        self.commonButtons(button_layout = self.button_hbxLay)  # ######################## UI-3. common底面ボタン3

        # 底面ボタン群 です ####################################################### end

        # レイアウト(底面ボタン用) を メインレイアウト
        # に追加 ###################################### 追加して初めて表示されます     -表示-
        main_vbxLay.addLayout(self.button_hbxLay)

        # 3.2): 底面ボタン群 -Layout- ###################################$##### -Layout- end
        # 3):###############################################################################

        # print('###' * 3 + 'koko A')
        # pprint(self.iniFileParam)

        # # 自動で、self.iniFileParam['tab_wid_selection_iFP'] を作成する方法
        # if tabCount__ >= 1:
        #     self.iniFileParam['tab_wid_selection_iFP'] = 'tab_wid_selection'
        # self.tabCount__ = tabCount__
        # print('###' * 3 + 'koko B')
        # print(self.iniFileParam)

        self.show()  # 最終的にUIを作成
        # window の高さ編集をしてアップデートしてあげる
        self.cal_alwaysHeight_window()

        # GetAttrFrmMod(moduleName = Container)

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
                メインとなるレイアウト(底面ボタン用)
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
        # executeプッシュボタンウィジェット
        # を作成 ###################################### 作成しただけでは表示されません -Widget-
        execute = 'Execute'
        exeBtn_pbtnWid = QPushButton(execute)  # プッシュボタンウィジェット(execute用)
        # ボタンウィジェット(execute用) を レイアウト(底面ボタン用)
        # に追加 ###################################### 追加して初めて表示されます     -表示-
        button_layout.addWidget(exeBtn_pbtnWid, 2)  # 追加 # 比率も考慮

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
        exeBtn_pbtnWid.setStyleSheet(self.bgcBlue3)  # 独自で色を設定

        # シグナル/スロット
        exeBtn_pbtnWid.clicked.connect(
            partial(self.controller.executeBtn, f'v: button, {execute}')
            )
        rstBtn_pbtnWid.clicked.connect(
            partial(self.controller.menuReset, f'v: button, {reset}')
            )
        clsBtn_pbtnWid.clicked.connect(
            partial(self.controller.menuClose, f'v: button, {close_}')
            )

    # UI-2. common情報
    def commonInformation(self, main_layout):
        u""" < UI-2. common情報 の作成 >

        .. note:: 以下 は必須です！！

            - **main_vbxLay**
                メインレイアウト
                    に、
                以下の、情報
                    がぶら下がります

        ######################

        - ラベルウィジェット1
        - ラベルウィジェット2
        - セパレータウィジェット
        を一気に作成し、レイアウトまで行っています

        ######################

        :param main_layout: メインとなるレイアウト
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
        main_layout.addWidget(txt1_lblWid)  # メインレイアウト に ラベルウィジェット1 を追加
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
        main_layout.addWidget(txt2_lblWid)  # メインレイアウト に ラベルウィジェット2 を追加
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
        main_layout.addWidget(separator_frWid)  # メインレイアウト に フレームウィジェット(セパレータ用) を追加
        # QFrame -Widget- ################################################### -Widget- end

        # 常に、レイアウト(大フレーム用) のトップに配置されるようにするため、垂直スペーサーを追加して間隔を制御します
        # spacer = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.frame_vbxLay.addItem(spacer)

    # UI-2. 追加オプションのまとまり
    def displayOptions(self, main_layout, tabCount_: int):
        u""" < UI-2. 追加オプションのまとまり >

        .. note:: 以下 は必須です！！

            - **main_vbxLay**
                メインレイアウト
                    に、
                以下の、情報
                    がぶら下がります
            - tabCount_ 数は、
                新規となる 子tabラベル名 の辞書
                    self.tabLabelName_dict_new
                と等数がベスト

        ######################

        - タブウィジェット
        を一気に作成し、レイアウトまで行っています

        ######################

        :param main_layout: メインとなるレイアウト
        :param int tabCount_: tab数の指定入力
        """
        self.tabCount__ = tabCount_
        tab_wid_: QTabWidget = MyTabWidget(tabCount = tabCount_)  # note): tabCount_は、子tab widget リスト と等数がベスト
        main_layout.addWidget(tab_wid_)  # メインレイアウト に タブウィジェット を追加

        # # add tab selection to the iniFileParam
        # # tab数が1以上である限り、
        # # 毎時、新規で self.iniFileParam に
        # # f'tab_wid_selection_iFP' 辞書登録をする、サンプルです
        # # 自動で、self.iniFileParam['tab_wid_selection_iFP'] を作成する方法
        # if tabCount_ > 0:
        #     # create 独自naming の定義
        #     tab_wid_sel_key = f'tab_wid_selection_iFP'
        #     tab_wid_sel_val = f'tab_wid_selection'
        #     print('###' * 3 + 'koko E')
        #     print(tab_wid_sel_key, tab_wid_sel_val)
        #     self.iFP_oDict[tab_wid_sel_key] = tab_wid_sel_val

        self.tab_wid_ = tab_wid_

        # タブのアップデート関数
        self.update_tab_names(tab_wid = tab_wid_)  # 子tabラベル名 等を更新

        # PySide2.QtWidgets.QTabWidget 組み込み関数 を使用した
        # 初期 タブインデックス 選択番号 設定
        tab_wid_.setCurrentIndex(1)  # note): 数は、tabCount 数以内 がベスト

        # PySide2.QtWidgets.QTabWidget 組み込み関数 を使用した
        # tab クリックで、コンテナ のある フレーム の高さを再計算するシグナル の埋め込み
        # note): クリックされたタブのインデックスが tabBarClicked シグナル によって
        #   提供されるため、tabClicked メソッドに 引数は不要
        tab_wid_.tabBarClicked.connect(self.tabClicked)

        # 子tab widget の 子frame widget の 子grid layout それぞれに対して、以下を実行
        self._frame_gdLays_list = tab_wid_.getAllChildrenGridLayout_fromMainTabWidget()
        # pprint(self._frame_gdLays_list)

        # this is sample code
        # tabCount_数に応じた、サンプルボタンをタブへ格納する、サンプルです
        for index in range(tabCount_):
            # QGridLayout 独自naming  # note): fr1_gdLay, fr2_gdLay...に相当
            # gdLayName: f'fr{index}_gdLay'
            # QWidget 独自naming  # note): btGp1_wid, btGp2_wid...に相当
            # widName: f'btGp{index}_wid'
            # QVBoxLayout 独自naming  # note): btGp1_vbxLay, btGp2_vbxLay...に相当
            # vbxLayName: f'btGp{index}_vbxLay'
            if index % 2 == 0:
                self.contExist_tab_dict[index] = False
                # print(f'{index} = 偶数')
                # 偶数番号のtab・偶数番号のframe ###################################
                gdLayName = self._frame_gdLays_list[index]
                # ラジオボタンの作成
                gdLayName.addWidget(QPushButton('ボタン1'), 0, 0)  # gdLayName に 'ボタン3' を追加
                gdLayName.addWidget(QPushButton('ボタン2'), 0, 1)  # gdLayName に 'ボタン4' を追加
            else:
                # コンテナが存在するtabの リスト として登録
                self.contExist_tab_dict[index] = True

                # print(f'{index} = 奇数')
                # 奇数番号のtab・奇数番号のframe ###################################
                gdLayName = self._frame_gdLays_list[index]

                widName = QWidget()
                vbxLayName = QVBoxLayout(widName)
                pBtnX_pbtnWid = QPushButton('ボタンX')
                vbxLayName.addWidget(pBtnX_pbtnWid)
                rBtnY_rbtnWid = QRadioButton(f'this is ボタンY')
                rBtnY_rbtnWid.setChecked(False)
                vbxLayName.addWidget(rBtnY_rbtnWid)

                gdLayName.addWidget(widName)  # gdLayName に widName を追加

                ################################################################
                contAll_wid = QWidget()
                contAll_vbxLay = QVBoxLayout(contAll_wid)
                ############################################################
                contA_wid = Container("GroupA")
                contAll_vbxLay.addWidget(contA_wid)

                self.cont_wid_list.append(contA_wid)  # コンテナ の リスト として登録

                # コンテナA ヘッダー シグナルとスロットを接続
                contA_clickableHeaderWid = contA_wid.contentHeader.clickableHeaderWidget
                contA_clickableHeaderWid.clicked.connect(partial(self.cal_alwaysHeight_containerAll, contA_wid)
                                                         )

                content_layout = QGridLayout(contA_wid.contentWidget)
                pBtnC_pbtnWid = QPushButton('ボタンA')
                content_layout.addWidget(pBtnC_pbtnWid)
                rbtnB_rbtnWid = QRadioButton(f'this is ボタンB')
                rbtnB_rbtnWid.setChecked(False)
                content_layout.addWidget(rbtnB_rbtnWid)

                self.rbtn_wid_list.append(rbtnB_rbtnWid)  # RadioButton の リスト として登録

                contA_wid.collapse()

                ############################################################
                contB_wid = Container("GroupB")
                contAll_vbxLay.addWidget(contB_wid)

                self.cont_wid_list.append(contB_wid)  # コンテナ の リスト として登録

                # コンテナB ヘッダー シグナルとスロットを接続
                contB_clickableHeaderWid = contB_wid.contentHeader.clickableHeaderWidget
                contB_clickableHeaderWid.clicked.connect(partial(self.cal_alwaysHeight_containerAll, contB_wid)
                                                         )

                content_layout = QGridLayout(contB_wid.contentWidget)
                pBtnC_pbtnWid = QPushButton('ボタンC')
                content_layout.addWidget(pBtnC_pbtnWid)

                contB_wid.collapse()
                ############################################################

                gdLayName.addWidget(contAll_wid)  # gdLayName に widName を追加

                spacer = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
                gdLayName.addItem(spacer)
        # # # tab1, frame1 #########################################################
        # fr1_gdLay = self._frame_gdLays_list[0]
        # btGp1A_wid = QWidget()
        # btGp1A_vbxLay = QVBoxLayout(btGp1A_wid)
        # btGp1A_vbxLay.addWidget(QPushButton('ボタン1'))
        # btGp1A_vbxLay.addWidget(QPushButton('ボタン2'))
        # fr1_gdLay.addWidget(btGp1A_wid)  # fr1_gdLay に btGp1A_wid を追加
        # # # tab2, frame2 #########################################################
        # fr2_gdLay = self._frame_gdLays_list[1]
        # fr2_gdLay.addWidget(QPushButton('ボタン3'), 0, 0)  # fr2_gdLay に 'ボタン3' を追加
        # fr2_gdLay.addWidget(QPushButton('ボタン4'), 0, 1)  # fr2_gdLay に 'ボタン4' を追加
        # # # tab3, frame3 #########################################################
        # fr3_gdLay = self._frame_gdLays_list[2]
        # btGp3A_wid = QWidget()
        # btGp3A_vbxLay = QVBoxLayout(btGp3A_wid)
        # btGp3A_vbxLay.addWidget(QPushButton('ボタン1'))
        # btGp3A_vbxLay.addWidget(QPushButton('ボタン2'))
        # fr3_gdLay.addWidget(btGp3A_wid)  # fr3_gdLay に btGp3A_wid を追加

        # # 毎時、新規で self.iniFileParam に辞書登録する、サンプルです
        # # 自動で、self.iniFileParam['tab{index}_rbt{i}_wid_stat_iFP'] を作成する方法
        # for index, tab in enumerate(self.tabs):
        #     isExist_rbnt_wid = tab.findChildren(QRadioButton)
        #     # print(isExist_rbnt_wid)
        #     count_ = len(isExist_rbnt_wid)
        #     # print(count_)
        #     if isExist_rbnt_wid:
        #         i = 0
        #         while i < count_:
        #             # create 独自naming の定義
        #             tabIdx_rbtIdx_wid_stat_key = f'tab{index}_rbt{i}_wid_stat_iFP'
        #             tabIdx_rbtIdx_wid_stat_val = f'tab{index}_rbt{i}_wid_stat'
        #             print('###' * 3 + 'koko D')
        #             print(tabIdx_rbtIdx_wid_stat_key, tabIdx_rbtIdx_wid_stat_val)
        #             # 既存の.iniファイルのパラメーター設定に、順序付き辞書に追加
        #             self.iFP_oDict[tabIdx_rbtIdx_wid_stat_key] = tabIdx_rbtIdx_wid_stat_val
        #             i += 1
        # print('###' * 3 + 'koko X')
        # pprint(self.iFP_oDict)

        # spacer = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # main_layout.addItem(spacer)

        # print(self.contExist_tab_dict)
        # # コンテナが存在するtabの有無 辞書 順序付き辞書 定義
        # self.contExist_tab_oDict = OrderedDict(self.contExist_tab_dict)  # 順序付き辞書 定義
        # print(self.contExist_tab_oDict)

    # tab クリックで、コンテナ のある フレーム の高さを再計算する関数
    def tabClicked(self, index):
        u""" < tab クリックで、コンテナ のある フレーム の高さを再計算する関数 です>

        関数がシグナルのスロットとして使用される場合、
            その関数の引数はシグナルによって提供される情報を受け取るために使用されます。
                しかし、引数を持たない関数をシグナルのスロットとして使用することも可能です。
        当メソッドは 組み込み関数 tabBarClicked シグナルのスロットとして設定されています。
            このシグナルはタブバーでタブがクリックされたときに発生し、
                クリックされたタブのインデックスがそのシグナルによって提供されます。
        したがって、tabClicked メソッドが引数を受け取らなくても、
            PySide2がシグナルによって提供される情報（ここではクリックされたタブのインデックス）
                を適切に処理することができます。
                    そのため、引数 index がなくても問題ありません。
        """
        # self.cont_heights_dict.clear()
        # print(f'cont_heights_dict: ')
        # pprint(self.cont_heights_dict)
        print(f'Tab clicked: {index}\n')
        self.clicked_tab_index = index
        # print(self.clicked_tab_index)
        # name = self.tab_wid_.getCurrentTabName(index)
        # print(name, type(name))
        child = self.tab_wid_.currentWidget()
        # print(child, type(child))
        cont_wid_all = child.findChildren(Container)
        # print('koko')
        # pprint(cont_wid_all)
        # print(f'{self.cont_heights_dict}\n')
        if not cont_wid_all:
            pass
        else:
            # self.cont_heights_dict.clear()
            # print(f'cont_heights_dict: ')
            # pprint(self.cont_heights_dict)
            for cont_wid in cont_wid_all:
                # print(containerIndex, type(cont_wid))
                self.cal_alwaysHeight_containerAll(cont_wid)
            # print(f'cont_heights_dict: ')
            # pprint(self.cont_heights_dict)
            # print(f'cont_total_height: {self.cont_total_height}\n')

    # def printClickedTabIndex(self):
    #     current_tab_index = self.tab_wid_.currentIndex()
    #     print(f'Current tab index: {current_tab_index}')

    # タブのアップデート関数
    def update_tab_names(self, tab_wid):
        u""" < タブのアップデート関数 です>

        .. note:: 以下 は必須です！！

            - **tab_wid**
                タブウィジェット
                    に、
                以下の、情報
                    がぶら下がります

        ######################

        - タブウィジェット
        を一気に更新します

        ######################

        :param tab_wid: タブウィジェット
        """
        self.tabs: List[QTabWidget] = tab_wid.getAllChildrenTabWidget_fromMainTabWidget()
        # print('koko')
        # pprint(self.tabs)
        self.tabLabelName_list_old: List[str] = tab_wid.getAllChildrenTabLabelName_fromMainTabWidget()
        # print('koko')
        # pprint(self.tabLabelName_list_old)
        for index, tab in enumerate(self.tabs):
            tab_wid.addTab(tab, self.tabLabelName_list_old[index])
        for index, (new_name_key, new_name_value) in enumerate(self.tabLabelName_oDict_new.items()):
            tab_wid.setTabText(index, new_name_key)
            tab_wid.setTabToolTip(index, new_name_value)
    # UIディテール 作成 ################################################################ end

    # オーバーライド
    # show メソッド 組み込み関数
    def show(self):
        u""" < (オーバーライド) show メソッド 組み込み関数 です >

        オーバーライド

        .. note::
            当該 show メソッド は、基は組み込み関数です

        実行の手順
            #. 復元用のオリジナルメソッド「restore」を実行し、表示する前に設定を復元します
            #. 次に、メソッド「show」をオーバーライドし、表示する
        """
        # print('###' * 3 + 'koko D')
        # pprint(self.iniFileParam)
        if not self.doResetStat:
            # print('###' * 3 + 'koko E')
            self.restore()  # 復元用のオリジナルメソッド
        # self.restore()  # 復元用のオリジナルメソッド

        super().show()  # super(Tpl4PySide2_Type2_View, self).show() でも可

    # 1. UI-1. メニュー コマンド群 ###################################################### start
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

        # # 自動で、self.iniFileParam['tab_wid_selection_iFP'] を要素として作成する方法
        # print(self.tabCount__)
        # if self.tabCount__ >= 1:
        #     # tabウィジェット の情報を 保存
        #     getTabCurrentIndex = self.tab_wid_.currentIndex()
        #     print(getTabCurrentIndex)
        #     self._settings.setValue(self.iniFileParam['tab_wid_selection_iFP']
        #                             , getTabCurrentIndex
        #                             )

        # tabウィジェット の情報を 保存
        getTabCurrentIndex = self.tab_wid_.currentIndex()
        # print(getTabCurrentIndex)
        self._settings.setValue(self.iniFileParam['tab_wid_selection_iFP']
                                , getTabCurrentIndex
                                )

        # Container の情報を 保存 #############################################
        # tab1contA wid : self.cont_wid_list[0]
        contA_wid_isExpand, _ = self.cont_wid_list[0].contentHeader.getStatus_contentWidget()
        # print(contA_wid_isExpand)
        self._settings.setValue(
            self.iniFileParam['contA_wid_expStat_iFP'], contA_wid_isExpand
            )

        # tab1contB wid : self.cont_wid_list[1]
        contB_wid_isExpand, _ = self.cont_wid_list[1].contentHeader.getStatus_contentWidget()
        # print(contB_wid_isExpand)
        self._settings.setValue(
            self.iniFileParam['contB_wid_expStat_iFP'], contB_wid_isExpand
            )

        # tab3contA wid : self.cont_wid_list[2]
        contC_wid_isExpand, _ = self.cont_wid_list[2].contentHeader.getStatus_contentWidget()
        # print(contC_wid_isExpand)
        self._settings.setValue(
            self.iniFileParam['contC_wid_expStat_iFP'], contC_wid_isExpand
            )

        # tab3contB wid : self.cont_wid_list[3]
        contD_wid_isExpand, _ = self.cont_wid_list[3].contentHeader.getStatus_contentWidget()
        # print(contD_wid_isExpand)
        self._settings.setValue(
            self.iniFileParam['contD_wid_expStat_iFP'], contD_wid_isExpand
            )

        # contB の RadioButton B wid : self.rbtn_wid_list[0]
        cBrbtnB_wid_isChecked = self.rbtn_wid_list[0].isChecked()  # ウィジェットラジオボタン から isCheckedメソッド 使用で bool を 取得
        # print(cBrbtnB_wid_isChecked)
        self._settings.setValue(
            self.iniFileParam['cBrbtnB_wid_isChecked_iFP'], cBrbtnB_wid_isChecked
            )

        # contD の RadioButton D wid : self.rbtn_wid_list[1]
        cDrbtnD_wid_isChecked = self.rbtn_wid_list[1].isChecked()  # ウィジェットラジオボタン から isCheckedメソッド 使用で bool を 取得
        # print(cDrbtnD_wid_isChecked)
        self._settings.setValue(
            self.iniFileParam['cDrbtnD_wid_isChecked_iFP'], cDrbtnD_wid_isChecked
            )

        print('saveSettings')
        print(f'\tSave a .INI file, at \n\t\t{self.filename}')

    def saveSettings_geoOnly(self):
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

        print('saveSettings_geoOnly')
        print(f'\tSave a .INI file, at \n\t\t{self.filename}')

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
        print('###' * 10)
        print(f'\nReset all input value...')

        titleName_ = 'ResetExecutionHeadsUp'
        infoSummary_ = ('ユーザーは、リセットを実行しようとしています。\n'
                        'OK / close どちらかを押下願います。')
        infoDetail_ = ('UIの設定が全てリセットされてしまいます。\n'
                       'よろしければ、OK ボタンを\n'
                       '拒否の場合は、close ボタンを\n'
                       '押下願います。')
        popup = CustomPopup(titleName = titleName_
                            , infoSummary = infoSummary_
                            , infoDetail = infoDetail_
                            )
        popup.exec_()

        # ポップアップの結果に応じて分岐
        if not popup.result:
            message_warning('リセットはキャンセルされました。')
            # ウィンドウが閉じられた場合の処理
            pass
        else:
            message('リセットは実行されました。')
            # OKボタンが押された場合の処理

            # .iniファイル の 内容を クリア します
            self.iniFS.clear_ini_file()
            # まずは一旦保存
            self.saveSettings_geoOnly()  # UI設定のみ の保存用 関数 実行
            print(u'一旦saveGeometry..のみ実行')

            # 入力フィールドを持つ子供Widgetのみのカレントの情報一括クリアー 関数 実行
            # self.clearAllValue_toAllWidget(central_wid_)

            # self.clearAllValue_toAllWidget(central_wid_) の代替え案 ########## start
            model_ = Tpl4PySide2_Type2_Modl()
            view_ = Tpl4PySide2_Type2_View(model_)
            Tpl4PySide2_Type2_Ctlr(view_, model_)
            # self.clearAllValue_toAllWidget(central_wid_) の代替え案 ########## end

            # self.saveSettings()  # UI設定の保存用 関数 実行

    # 当ひな形のtype2では未使用
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
                self.clearAllValue_toAllWidget(central_wid_ = child)
            # 3. その他の場合はクリアー対象の処理
            else:
                if hasattr(child, 'clear') and callable(getattr(child, 'clear')):
                    child.clear()
                if hasattr(child, 'setChecked') and callable(getattr(child, 'setChecked')):
                    child.setChecked(False)
                if isinstance(child, QComboBox):
                    child.setCurrentIndex(-1)
                self.clearAllValue_toAllWidget(central_wid_ = child)

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
    # メモ: (PyMel版)Model: editMenuSaveSettingsCmd に相当
    # メモ: (PyMel版)View: editMenuCloseCmd に相当
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
        # print('###' * 3 + 'koko close event')
        # pprint(self.iniFileParam)
        # pprint(self.iFP_oDict)
        self.saveSettings()  # UI設定の保存用オリジナルメソッド
        # super(Tpl4PySide2_View, self).closeEvent(event)  # ここは無くても上手く発動するようです
    # 1. UI-1. メニュー コマンド群 ######################################################## end

    # 4. UI-4. OptionVar を利用したパラメータ管理 コマンド群 ############################### start
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
        # print('###' * 3 + 'koko R')
        # pprint(self.iniFileParam)
        # サイズの情報を 復元
        self.restoreGeometry(self._settings.value(self.iniFileParam['geo_iFP']))  # iniFile から 可変byte配列 を ゲット し、サイズの情報 を 復元操作
        print(f'\tRestore a \n\t\t'
              f'{self.iniFileParam["geo_iFP"]} \n\t\t\t'
              f'param: {...}'
              )

        # # 自動で、self.iniFileParam['tab_wid_selection_iFP'] を要素として取得する方法
        # print(self.tabCount__)
        # if self.tabCount__ >= 1:
        #     # tabウィジェット の情報を 復元
        #     tab_wid_selection = self._settings.value(self.iniFileParam['tab_wid_selection_iFP'])
        #     print(tab_wid_selection)
        #     if tab_wid_selection:
        #         self.tab_wid_.setCurrentIndex(int(tab_wid_selection))

        # tabウィジェット の情報を 復元
        tab_wid_selection = self._settings.value(self.iniFileParam['tab_wid_selection_iFP'])
        # print(tab_wid_selection)
        if tab_wid_selection is not None:
            self.tab_wid_.setCurrentIndex(int(tab_wid_selection))

        # print(self.cont_wid_list)

        # Container の情報を 復元 #############################################
        # tab1contA wid: self.cont_wid_list[0] の情報を 復元
        tab1contA_wid_isExpand: str = self._settings.value(
            self.iniFileParam['contA_wid_expStat_iFP']
            )  # iniFile から isChecked を ゲット
        if tab1contA_wid_isExpand is True:
            self.cont_wid_list[0].expand()
        else:
            self.cont_wid_list[0].collapse()

        # tab1contB wid: self.cont_wid_list[1] の情報を 復元
        contB_wid_isExpand: str = self._settings.value(
            self.iniFileParam['contB_wid_expStat_iFP']
            )  # iniFile から isChecked を ゲット
        if contB_wid_isExpand is True:
            self.cont_wid_list[1].expand()
        else:
            self.cont_wid_list[1].collapse()

        # tab3contA wid: self.cont_wid_list[2] の情報を 復元
        contC_wid_isExpand: str = self._settings.value(
            self.iniFileParam['contC_wid_expStat_iFP']
            )  # iniFile から isChecked を ゲット
        if contC_wid_isExpand is True:
            self.cont_wid_list[2].expand()
        else:
            self.cont_wid_list[2].collapse()

        # tab3contB wid: self.cont_wid_list[3] の情報を 復元
        contD_wid_isExpand: str = self._settings.value(
            self.iniFileParam['contD_wid_expStat_iFP']
            )  # iniFile から isChecked を ゲット
        if contD_wid_isExpand is True:
            self.cont_wid_list[3].expand()
        else:
            self.cont_wid_list[3].collapse()

        # contB の RadioButton B wid: self.rbtn_wid_list[0] の情報を 復元
        cBrbtnB_wid_isChecked: str = self._settings.value(
            self.iniFileParam['cBrbtnB_wid_isChecked_iFP']
            )  # iniFile から isChecked を ゲット
        if cBrbtnB_wid_isChecked:
            self.rbtn_wid_list[0].setChecked(bool(cBrbtnB_wid_isChecked))
            # ウィジェットラジオボタン へ setCheckedメソッド 使用で bool を 復元操作

        # contD の RadioButton D wid: self.rbtn_wid_list[1] の情報を 復元
        cDrbtnD_wid_isChecked: str = self._settings.value(
            self.iniFileParam['cDrbtnD_wid_isChecked_iFP']
            )  # iniFile から isChecked を ゲット
        if cDrbtnD_wid_isChecked:
            self.rbtn_wid_list[1].setChecked(bool(cDrbtnD_wid_isChecked))
            # ウィジェットラジオボタン へ setCheckedメソッド 使用で bool を 復元操作

        print(f'\tRestore a .INI file, from \n\t\t{self.filename}')
    # 4. UI-4. OptionVar を利用したパラメータ管理 コマンド群 ############################### end

    def check_type(self, object_):
        type_ = type(object_)
        pprint(f'{object_} は {type_} という型です。', compact = True)

    def cal_alwaysHeight_containerAll(self, container_widget_name):
        # x, y, width, height: Tuple[int, int, int, int]

        # # check
        # # current： container_widget_name のサイズ
        # print(f'I am \n\t{container_widget_name}')
        # print(f'type is \n\t{type(container_widget_name)}')
        currentSize_frame_list = list(container_widget_name.geometry().getRect())  # タプルをリストに変換
        currentHeight_frame_ = currentSize_frame_list[3]  # List[int, int, int, int]
        # print(f'currentFrame_currentHeight: {currentHeight_frame_}')

        # Save the new height of the frame
        self.cont_heights_dict[container_widget_name] = currentHeight_frame_
        # print(f'cont_heights_dict: ')
        # pprint(self.cont_heights_dict)

        # Calculate the total height of all frames
        self.cont_total_height = sum(self.cont_heights_dict.values())
        # print(f'cont_total_height: {self.cont_total_height}\n')

        # temp
        # Get the current width size of the window
        current_width = self.geometry().width()
        # Set the new height
        temp_height = self.cont_total_height
        # Resize the window, keeping the current width and changing the height
        self.resize(current_width, temp_height)

        # final
        # 一旦フィットさせる。但し、全体的にフィットしてしまうので、ここで終わりにはしない！
        self.adjustSize()
        # Get the final height size of the window
        final_height = self.geometry().height()
        adjust = 20
        self.resize(current_width, final_height - adjust)

    def cal_alwaysHeight_window(self):
        # x, y, width, height: Tuple[int, int, int, int]
        # 初期： QMainWindow のサイズ
        start_size = list(self.geometry().getRect())  # タプルをリストに変換

        # 縦のみの合計サイズを抽出
        # Calculate the total height of all containers
        total_height = sum(self.cont_heights_dict.values())
        # Set the new height
        start_size[3] = total_height
        # アップデート： 全ての コンテナー が解放されている時、ぴったりと QMainWindow の最低限必要なサイズにフィットさせるサイズ
        upDate_size = tuple(start_size)  # リストをタプルに変換
        self.setGeometry(*upDate_size)
    # 2. UI-2. 追加オプション コマンド群 ################################################# start

    def uiOptBtn_changeColorCmd(self, index, optBtn_pbtnWid):
        print(index)
        # self.check_type(index)
        # self.check_type(optBtn_pbtnWid)
        if index == 'buttonA':
            optBtn_pbtnWid.setStyleSheet("background-color: black;")
        elif index == 'buttonB':
            optBtn_pbtnWid.setStyleSheet("background-color: pink;")
        elif index == 'buttonC':
            optBtn_pbtnWid.setStyleSheet("background-color: white;"
                                         )
    # 2. UI-2. 追加オプション コマンド群 ################################################# end


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
