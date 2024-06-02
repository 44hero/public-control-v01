# -*- coding: utf-8 -*-

u"""
templateForPySide2_type1_View.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -2.0-
:Date: 2024/02/29

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PySide2 version: 5.15.2

-リマインダ-
    done: 2024/02/22~2024/02/29
        - 更新
            - 概要: 新しいことをインプットしたので、それを反映したひな形を更新
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

        version = '-2.0-'
    done: 2023/11/23~2024/01/26
        新規

        version = '-1.0-'
"""

# 標準ライブラリ #################################################################
from functools import partial
from pprint import pprint
from typing import Tuple, List

# サードパーティライブラリ #########################################################
# from maya import OpenMayaUI, cmds
from PySide2.QtWidgets import (QApplication, QComboBox, QGridLayout,
                               QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                               QPushButton, QAction, QFrame, QLabel,
                               QSpacerItem, QSizePolicy,
                               )
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt

# ローカルで作成したモジュール ######################################################
import YO_utilityTools.TemplateForPySide2.type1.config as docstring
from .templateForPySide2_type1_Ctlr import Tpl4PySide2_Type1_Ctlr
from .templateForPySide2_type1_Modl import Tpl4PySide2_Type1_Modl
# basic_configuration(基本構成)
from .config import SPACE, TITLE, VERSION

# shiboken2 独自モジュール
from ..qt import getMayaWindow  # 利用時は、getMayaWindow()

from ..pyside2IniFileSetting import IniFileSetting
from ..Container import Container
# 汎用ライブラリー の使用 #################################################### start
from ...lib.message import message
# from ...lib.message_warning import message_warning
# 汎用ライブラリー の使用 #################################################### end


class Tpl4PySide2_Type1_View(QMainWindow):
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
                             }
        # self.od = OrderedDict(self.iniFileParam)  # 順序付き辞書 定義
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
        self.doResetStat = False

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

        self.show()  # 最終的にUIを作成

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
        container1_hbxLay = QHBoxLayout(container1_wid)  # レイアウト(コンテナ1用)
        # ウィジェット(コンテナ1用) を装飾
        # 設定を施す ###################################
        container1_wid.setStyleSheet("background-color: gray;"
                                     )  # Set background color to gray
        # レイアウト(コンテナ1用) を装飾
        # 設定を施す ###################################
        # container1_hbxLay.setSpacing(6)  # Adjust the value (e.g., 5) as per your preference

        # ボタン作成 関数 を繰り返します
        for index in self.button_info:
            _, optBtn_wid_ = self.create_optBtn(index)  # ボタン作成 関数
            # 各々のボタンウィジェット を レイアウト(コンテナ1用)
            # に追加 ###################################### 追加して初めて表示されます     -表示-
            container1_hbxLay.addWidget(optBtn_wid_)

        # レイアウト(コンテナ1用) を装飾
        # 設定を施す ###################################
        container1_hbxLay.setAlignment(Qt.AlignCenter)  # Center-align

        # ウィジェット(コンテナ1用) を レイアウト(大フレーム用)
        # に追加 ###################################### 追加して初めて表示されます     -表示-
        frame_layout.addWidget(container1_wid)
        # QWidget -Widget- ################################################## -Widget- end

        # QWidget -Widget- ################################################## -Widget- start
        # container2
        # を作成 ###################################### 作成しただけでは表示されません -Widget-
        container2_wid = QWidget(self)  # ウィジェット(コンテナ2用)
        # ウィジェット(コンテナ2用) 内に 水平のレイアウト(コンテナ2用)
        # を作成し そのウィジェット へ set ############### 作成しただけでは表示されません -Layout-
        container2_vbxLay = QVBoxLayout(container2_wid)  # レイアウト(コンテナ2用)
        # ウィジェット(コンテナ2用) を装飾
        # 設定を施す ###################################
        container2_wid.setStyleSheet("background-color: gray;"
                                     )  # Set background color to white

        # ウィジェット(コンテナ2用) を レイアウト(コンテナ2用)
        # に追加 ###################################### 追加して初めて表示されます     -表示-
        another_lblWid = QLabel("Another Widget")  # ラベルウィジェット(コンテナ2用)
        container2_vbxLay.addWidget(another_lblWid)

        # ウィジェット(コンテナ2用) を レイアウト(大フレーム用)
        # に追加 ###################################### 追加して初めて表示されます     -表示-
        frame_layout.addWidget(container2_wid)
        # レイアウト(コンテナ2用) を装飾
        # 設定を施す ###################################
        container2_vbxLay.setAlignment(Qt.AlignCenter)  # Center-align
        # QWidget -Widget- ################################################## -Widget- end

        # 常に、レイアウト(大フレーム用) のトップに配置されるようにするため、垂直スペーサーを追加して間隔を制御します
        # spacer = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # frame_layout.addItem(spacer)

        layout = QVBoxLayout()

        # groupA ################################################
        gpA_container = Container("Group A")
        gpA_container.collapse()
        layout.addWidget(gpA_container)
        content_layout = QGridLayout(gpA_container.contentWidget)
        content_layout.addWidget(QPushButton("Button"))

        frame_layout.addWidget(gpA_container)

        # groupB ################################################
        gpB_container = Container("Group B")
        gpB_container.collapse()
        layout.addWidget(gpB_container)
        content_layout = QGridLayout(gpB_container.contentWidget)
        # 中身
        btnB_pbtnWid = QPushButton("ButtonB")
        content_layout.addWidget(btnB_pbtnWid, 0, 0)  # 1
        btnC_pbtnWid = QPushButton("ButtonC")
        content_layout.addWidget(btnC_pbtnWid, 0, 1)  # 2

        frame_layout.addWidget(gpB_container)

    # UI-2. 追加オプションのまとまり 内の
    # container1用 ボタン作成 関数
    def create_optBtn(self, index_: str):
        """ < UI-2. 追加オプションのまとまり 内の container1用 ボタン作成 関数 です>

        :param str index_: container1用 ボタン名
        :return: index_, optBtn_pbtnWid（container1用 ボタン名, QPushButton名 のタプル）
        :rtype: tuple[str, QPushButton]
        """
        # container1 内に ボタンウィジェット
        # を作成 ###################################### 作成しただけでは表示されません -Widget-
        optBtn_pbtnWid = QPushButton(index_)  # ボタンウィジェット(container1用)
        # # optBtn_pbtnWid を container1_hbxLay
        # # に追加 ###################################### 追加して初めて表示されます     -表示-
        # container1_hbxLay.addWidget(optBtn_pbtnWid)
        # ボタンウィジェット(container1用) を装飾
        # 設定を施す ###################################
        optBtn_pbtnWid.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed
                                     )  # Set button自身にフィット
        # シグナル/スロット
        optBtn_pbtnWid.clicked.connect(
            partial(self.controller.selfColorChangeExeBtn, index_,
                    optBtn_pbtnWid
                    )
            )
        # # container1 内に ボタンウィジェット
        # # を作成 ###################################### 作成しただけでは表示されません -Widget-
        # btnA = 'buttonA'
        # self.btnA_pbtnWid = QPushButton(btnA)
        # # btnA_pbtnWid を container1_hbxLay
        # # に追加 ###################################### 追加して初めて表示されます     -表示-
        # container1_hbxLay.addWidget(self.btnA_pbtnWid)
        # # Set button自身にフィット
        # # 設定を施す ###################################
        # self.btnA_pbtnWid.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # シグナル/スロット
        # self.btnA_pbtnWid.clicked.connect(partial(self.controller.selfColorChangeExeBtn, btnA))
        #
        # btnB = 'buttonB'
        # self.btnB_pbtnWid = QPushButton(btnB)
        # # btnB_pbtnWid を container1_hbxLay
        # # に追加 ###################################### 追加して初めて表示されます     -表示-
        # container1_hbxLay.addWidget(self.btnB_pbtnWid)
        # # Set button自身にフィット
        # # 設定を施す ###################################
        # self.btnB_pbtnWid.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # シグナル/スロット
        # self.btnB_pbtnWid.clicked.connect(partial(self.controller.selfColorChangeExeBtn, btnB))
        #
        # btnC = 'buttonC'
        # self.btnC_pbtnWid = QPushButton(btnC)
        # # btnC_pbtnWid を container1_hbxLay
        # # に追加 ###################################### 追加して初めて表示されます     -表示-
        # container1_hbxLay.addWidget(self.btnC_pbtnWid)
        # # Set button自身にフィット
        # # 設定を施す ###################################
        # self.btnC_pbtnWid.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # シグナル/スロット
        # self.btnC_pbtnWid.clicked.connect(partial(self.controller.selfColorChangeExeBtn, btnC))
        return index_, optBtn_pbtnWid
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
        # print('--- def show(self): ...')
        # print(f'do reset?: {self.doResetStatYesOrNo_byString(self.doResetStat)}')
        if not self.doResetStat:
            self.restore()  # 復元用のオリジナルメソッド
        # self.restore()  # 復元用のオリジナルメソッド

        super().show()  # super(Tpl4PySide2_View, self).show() でも可

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
        # print('--- def resetSettings(self): ...')
        # print(f'do reset?: {self.doResetStatYesOrNo_byString(self.doResetStat)}')
        print('###' * 10)
        print(f'\nReset all input value...')

        # まずは一旦保存
        self.saveSettings()  # UI設定の保存用 関数 実行
        print(u'一旦save..')

        # 入力フィールドを持つ子供Widgetのみのカレントの情報一括クリアー 関数 実行
        # self.clearAllValue_toAllWidget(central_wid_)

        # self.clearAllValue_toAllWidget(central_wid_) の代替え案 ########## start
        model_ = Tpl4PySide2_Type1_Modl()
        view_ = Tpl4PySide2_Type1_View(model_)
        Tpl4PySide2_Type1_Ctlr(view_, model_)
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
        # サイズの情報を 復元
        self.restoreGeometry(self._settings.value(self.iniFileParam['geo_iFP']))  # iniFile から 可変byte配列 を ゲット し、サイズの情報 を 復元操作
        # print(f'\tRestore a \n\t\t'
        #       f'{self.iniFileParam["geo_iFP"]} \n\t\t\t'
        #       f'param: {...}'
        #       )

        print(f'\tRestore a .INI file, from \n\t\t{self.filename}')
    # 4. UI-4. OptionVar を利用したパラメータ管理 コマンド群 ############################### end

    def check_type(self, object_):
        type_ = type(object_)
        pprint(f'{object_} は {type_} という型です。', compact = True)

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
