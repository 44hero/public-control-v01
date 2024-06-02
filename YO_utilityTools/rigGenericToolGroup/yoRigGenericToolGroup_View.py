# -*- coding: utf-8 -*-

u"""
yoRigGenericToolGroup_View.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -5.5-
:Date: 2024/05/17

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PySide2 version: 5.15.2

-リマインダ-
    done: 2024/05/17
        - 追加6 と 変更6 と 新規6
            - 概要: ***_View モジュール の tabB の
                IHIツールの Hide, Show の呼び出し の改善
            - 詳細:
                ::

                    +   def constructorChunk9_buttonContext(self):
                            ...
                            # 変更6 ######################### start
                            # 追加4
                            hide_: str = 'Hide'
                            show_: str = 'Show'
                            button_toggle_: str = 'のトグル(押下非押下)'
                            button_rightClick_: str = '上 右クリック'
                            self.commonMessageShowHide = (f'ボタン{button_toggle_} で \n'
                                                          f'★{hide_}\n'
                                                          f'★{show_}\n'
                                                          f'を 呼び出し します。\n'
                                                          u'Script Editor をご覧ください。')
                            # 変更6 ######################### end

                    +   def displayOptions_gpB(self):
                            ...
                            # caseB3
                            ...
                            # 追加6 ######################################### start
                            ihi_btnC_pbtnWid.setCheckable(True)  # トグルボタンに設定
                            ihi_btnC_pbtnWid.toggled.connect(partial(self.on_button_toggled,
                                                                     pushButtonName = ihi_btnC_pbtnWid,
                                                                     caseIndex_ = caseIndex,
                                                                     toolName = isHisInt)
                                                             )  # ボタンのトグルアクションを接続
                            # 追加6 ######################################### end
                            ...
                            # 変更6 ######################################### start
                            # # ボタン コンテキスト menu 右クリック アクション の追加 #######################
                            # ihi_btnC_menuWid: QMenu = QMenu()
                            # # hide 呼び出し ################## 定義
                            # ...
                            # # show 呼び出し ################## 定義
                            # ...
                            # # シグナルとスロットを接続 (menu の ポジション 設定)
                            # ...
                            # # hide 呼び出し ################## アクション
                            # ...
                            # # show 呼び出し ################## アクション
                            # ...
                            # # シグナルとスロットを接続 (menu の 実際のアクション 設定)
                            # ...
                            # 変更6 ######################################### end
                            ...

                    +   # 新規6
                        # タブB IHI 用(toggle button control)
                        def on_button_toggled(self, checked: Any,
                                              pushButtonName: QPushButton,
                                              caseIndex_: str,
                                              toolName: str,
                                              ):
                            ...
    version = '-5.5-'

    done: 2024/05/08
        追加と変更と新規5
            - 概要: ***_View モジュール へ 新規tabF の 追加
            - 詳細:
                ::

                    +   def constructorChunk2_iniFileParam(self):
                            ...
                            self.iniFileParam_contWid = {
                                ...
                                    # 追加と変更と新規5
                                    'gpF_contWid_expStat_iFP': 'gpF_contWid_isExpand',  # [9]
                                    }
                                ...

                    +   def constructorChunk9_buttonContext(self):
                            ...
                            # 追加と変更と新規5
                                    self.commonMessage2 = (f'ボタン上 右クリック で \n'
                                                           f'★{self.help_}\n'
                                                           # f'★{self.cmmd_}\n'
                                                           f'を 呼び出し表示 します。\n'
                                                           u'Script Editor をご覧ください。'
                                                           )
                    +   def createUI(self):
                            ...
                            tabCount__ = 6 ###################################################  # 追加と変更と新規5
                            ...

                    +   def displayOptions(self, main_layout, tabCount_: int):
                            ...
                            # 追加と変更と新規5
                            # groupF ############################################################### タブE
                            gdLayName = self._frame_gdLays_list[5]
                            # print(gdLayName)

                            gpF_contWid: Container = self.displayOptions_gpF()
                            self.frame_vbxLay.addWidget(gpF_contWid)

                            gdLayName.addWidget(gpF_contWid)  # gdLayName に widName を追加
                            spacer: QSpacerItem = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
                            gdLayName.addItem(spacer)

                    +   # 追加と変更と新規5
                        # タブF 用
                        def displayOptions_gpF(self) -> Container:
                            ...
    version = '-5.1-'

    done: 2024/05/01
        追加4
            - 概要: ***_View モジュール の tabB へ
                IHIツールの Hide, Show の呼び出し 追加
            - 詳細:
                ::

                    +   # 追加4
                        # 作成された gpB PushButton ウィジェット 関連をリスト登録 ####################
                        self.pbtnGpB_wid_list: List[QPushButton] = []

                    +   # 追加4
                        # show用 アイコンを設定
                        self.showIcon = None
                        self.showIcon = self.showIcon if self.showIcon is not None else ':/menuIconShow.png'  # maya icon を使用しています
                        # hide用 アイコンを設定
                        self.hideIcon = None
                        self.hideIcon = self.hideIcon if self.hideIcon is not None else ':/QR_hide.png'  # maya icon を使用しています

                    +   # 追加4
                        self.hide_: str = 'Hide'
                        self.show_: str = 'Show'
                        self.commonMessageShowHide = (f'ボタン上 右クリック で \n'
                                                      f'★{self.hide_}\n'
                                                      f'★{self.show_}\n'
                                                      f'を 呼び出し表示 します。\n'
                                                      u'Script Editor をご覧ください。')
                    +   def displayOptions_gpB(self) -> Container:
                            ...
                            # 追加4
                            # caseB3 ######################################################### start
                            # isHistoricallyInteresting: yoIsHistoricallyInteresting
                            caseIndex = 'caseB3'
                            isHisInt = 'isHistoricallyInteresting '
                            ihi_btnC_pbtnWid = QPushButton("IHI")
                            ...
                            # caseB3 ######################################################### end
                            # 中身 ######################################################################## end

                            # 追加4
                            # PushButton の視認性を上げるために色替え e.g.): [0, 3, 4, 7, 8, 11, 12, ...] だけ色変え
                            count = len(self.pbtnGpB_wid_list)
                            if self.pbtnGpB_wid_list:
                                ...
        version = '-5.0-'

    done: 2024/04/11~2024/04/17
        追加3
            - 概要: ***_View モジュール の tabA,D の 各ツールの
                Help の呼び出し 追加
                コマンド実行する記述例 の呼び出し 追加
                に伴う、
                当 ***_View モジュール への関連を 追加
            - 詳細:
                ::

                    +   # 追加3
                        # コンストラクタのまとまり9_コンテキストメニュー 設定
                        def constructorChunk9_buttonContext(self):
                            ...

                    +   # caseA1
                        # rename tool 5: YO_renameTool5_main
                        ...
                        # 追加3
                        # ボタン コンテキスト menu 右クリック アクション の追加 ################## start
                        ...
                        # ボタン コンテキスト menu 右クリック アクション の追加 ################## end

                        # caseA2
                        # createSpaceNode 3: YO_createSpaceNode3_main
                        ...
                        # 追加3
                        # ボタン コンテキスト menu 右クリック アクション の追加 ################## start
                        ...
                        # ボタン コンテキスト menu 右クリック アクション の追加 ################## end

                        # caseD1
                        # pointConstraintByMatrix 1: YO_pointConstraintByMatrix1_main
                        ...
                        # 追加3
                        # ボタン コンテキスト menu 右クリック アクション の追加 ################## start
                        ...
                        # ボタン コンテキスト menu 右クリック アクション の追加 ################## end

                        # caseD2
                        # orientConstraintByMatrix 1: YO_orientConstraintByMatrix1_main
                        ...
                        # 追加3
                        # ボタン コンテキスト menu 右クリック アクション の追加 ################## start
                        ...
                        # ボタン コンテキスト menu 右クリック アクション の追加 ################## end

                        # caseD3
                        # scaleConstraintByMatrix 1: YO_scaleConstraintByMatrix1_main
                        ...
                        # 追加3
                        # ボタン コンテキスト menu 右クリック アクション の追加 ################## start
                        ...
                        # ボタン コンテキスト menu 右クリック アクション の追加 ################## end

                        # caseD4
                        # shearConstraintByMatrix 1: YO_shearConstraintByMatrix1_main
                        ...
                        # 追加3
                        # ボタン コンテキスト menu 右クリック アクション の追加 ################## start
                        ...
                        # ボタン コンテキスト menu 右クリック アクション の追加 ################## end

                    +   # 追加3
                        # ボタン コンテキスト menu の ポジション 設定 関数
                        def show_contextMenu(self, button: QPushButton, menu: QMenu, point: Any):
                            ...

        version = '-4.0-'

    done: 2024/04/11
        追加2
            - 概要: tabB へ YO_constraintToGeometry2 UI の呼び出し を追加
            - 詳細:
                ::

                    +   # 追加2
                        # caseB2
                        # constraintToGeometry: YO_constraintToGeometry2
                        caseIndex = 'caseB2'
                        ...
                        c2g_btnBB_pbtnWid.clicked.connect(partial(self.controller.toolUIBootBtn,
                                                                  f'v: pBtn, {c2g_btnBB_pbtnWid}',
                                                                  caseIndex
                                                                  )
                                                          )  # ツールの呼び出し
        version = '-3.1-'

    done: 2024/04/09
        追加1
            - 概要: tabE へ Node current view として reference の on/off 表示切り替え を追加
            - 詳細:
                ::

                    +   # 追加1
                        self.referenceIcon = None
                        self.referenceIcon = self.referenceIcon if self.referenceIcon is not None else':/reference.png'  # maya icon を使用しています

                    +   'gpE22_contWid_expStat_iFP': 'gpE22_contWid_isExpand',  # [5-2]

                    +   # 追加1
                        # contE2-2 ############################################################### Node 四段目
                        gpE22_contWid: Container = Container("Node")
                        ...
                        self.chunkContent_gpE3(contWid_contentWidget_ = gpE22_contWid.contentWidget)
                        # ################################################################## 三段目 中身 end

                    +   # 追加1
                        # タブE container22 Node 用(current view 表示)
                        def chunkContent_gpE22(self, contWid_contentWidget_):...

                    +   def toggle_checkBox(self
                                            , caseIndex_: str, cBxWid_: QCheckBox
                                            , longName_: str, state: int
                                            ):
                                            ...
                            ...
                            # 追加1
                            # Node: current view 表示 用
                            isNodeV = True if caseIndex_.endswith('nv') else False
                            if isNodeV:
                                self.controller.ui_checkBox_nv(f'v: cBx_nv'
                                                               , caseIndex_, cBxWid_
                                                               , longName_, state
                                                               )
                            ...

                    +   # 追加1
                        # Node: current view 表示 用
                        def currentState_checkBox_nv(self
                                                     , currentState_: str , cBxWid_: QCheckBox
                                                     ):...

        version = '-3.0-'

    done: 2024/03/17~
        新規
        version = '-2.0-'

    done: 2024/01/26~2024/03/03
        新規
        version = '-1.0-'
"""

# 標準ライブラリ #################################################################
from functools import partial
from pprint import pprint
from typing import Any, Tuple, List
from collections import OrderedDict

# サードパーティライブラリ #########################################################
# from maya import OpenMayaUI, cmds
from PySide2.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
                               QMainWindow, QMenu, QTabWidget, QWidget,
                               QHBoxLayout, QVBoxLayout, QPushButton, QAction,
                               QFrame, QLabel, QSpacerItem, QSizePolicy,
                               )
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtCore import Qt

# ローカルで作成したモジュール ######################################################
import YO_utilityTools.rigGenericToolGroup.config as docstring
# basic_configuration(基本構成)
from .config import SPACE, TITLE, VERSION

from .yoRigGenericToolGroup_Modl import RigGenTlGp_Modl
from .yoRigGenericToolGroup_Ctlr import RigGenTlGp_Ctlr

# shiboken2 独自モジュール
from ..TemplateForPySide2.qt import getMayaWindow  # 利用時は、getMayaWindow()

from ..TemplateForPySide2.pyside2IniFileSetting import IniFileSetting
from ..TemplateForPySide2.Container import Container
from ..TemplateForPySide2.MyTabWidget import MyTabWidget

from ..TemplateForPySide2.type2.templateForPySide2_type2_View import Tpl4PySide2_Type2_View
# 汎用ライブラリー の使用 #################################################### start
from ..lib.message import message
from ..lib.message_warning import message_warning
from ..lib.yoGetAttributeFromModule import GetAttrFrmMod
# 汎用ライブラリー の使用 #################################################### end


# 便宜上、
# タブ(tab) のインデックス は、グループ(gp | group) のインデックス と同義
# としています
# また、
# UIをできうる限りコンパクトにしたい故、mayaでいう アノテーション で説明補足しています


class RigGenTlGp_View(Tpl4PySide2_Type2_View):
    def __init__(self, _model, parent = None, flags = Qt.WindowFlags()):
        # <UI要素 1>.
        # 当該window を Maya window 画面の前面に ######################################## start
        if parent is None:
            parent = getMayaWindow()
        # 当該window を Maya window 画面の前面に ######################################## end

        super(RigGenTlGp_View, self).__init__(_model, parent, flags)

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
        self.infoSummary = (u'rig作業高汎用ツール\n'
                            u'の PySide2版 です。'
                            )
        self.infoDetail = (u'rig 作業時の汎用性の高いツールをまとめました。'
                           )
        # ######################################################################

        # <UI要素 3>.
        # コンストラクタのまとまり1_.iniファイル 設定
        self.constructorChunk1_iniFileSetting()  # オーバーライド

        # コンストラクタのまとまり2_.iniファイルのパラメーター 設定
        self.constructorChunk2_iniFileParam()  # オーバーライド
        # コンストラクタのまとまり3_色とアイコン 設定
        self.constructorChunk3_colorAndIcon()  # note): オリジナルから引用し再利用
        # コンストラクタのまとまり4_その他A 設定
        self.constructorChunk4_otherA()  # オーバーライド
        # コンストラクタのまとまり5_その他B タブ及びタブのフレーム関連 設定
        self.constructorChunk5_otherB()  # オーバーライド

        # コンストラクタのまとまり6_色 設定
        self.constructorChunk6_color()  # 新規

        # コンストラクタのまとまり7_アイコン 設定
        self.constructorChunk7_icon()  # 新規
        # コンストラクタのまとまり8_アイコン 設定
        self.constructorChunk8_icon()  # 新規

        # コンストラクタのまとまり9_コンテキストメニュー 設定
        self.constructorChunk9_buttonContext()  # 新規

    # オーバーライド
    # コンストラクタのまとまり1_.iniファイル 設定
    def constructorChunk1_iniFileSetting(self):
        u""" < コンストラクタのまとまり1_.iniファイル 設定 >

        ######################
        """
        # .iniファイルの設定 ########################################################### start
        # 変更箇所
        self.iniFS = IniFileSetting(self.title[2:])  # pyside2IniFileSetting モジュール
        filename, _settings = self.iniFS.iniFileSetting()  # .iniファイルの設定 メソッド
        self.filename = filename
        self._settings = _settings
        # .iniファイルの設定 ########################################################### end

    # オーバーライド
    # コンストラクタのまとまり2_.iniファイルのパラメーター 設定
    def constructorChunk2_iniFileParam(self):
        u""" < コンストラクタのまとまり2_.iniファイルのパラメーター 設定 >

        ######################
        """
        # .iniファイルのパラメーター設定 ##################################### start
        self.iniFileParam = {'geo_iFP': 'geometry',  # [0]
                             'tab_wid_selection_iFP': 'tab_wid_selection',  # [1]
                             }
        self.iniFileParam_contWid = {
            'gpA_contWid_expStat_iFP': 'gpA_contWid_isExpand',  # [0]

            'gpB_contWid_expStat_iFP': 'gpB_contWid_isExpand',  # [1]

            'gpC_contWid_expStat_iFP': 'gpC_contWid_isExpand',  # [2]

            'gpD_contWid_expStat_iFP': 'gpD_contWid_isExpand',  # [3]

            'gpE1_contWid_expStat_iFP': 'gpE1_contWid_isExpand',  # [4]
            'gpE2_contWid_expStat_iFP': 'gpE2_contWid_isExpand',  # [5]
            'gpE3_contWid_expStat_iFP': 'gpE3_contWid_isExpand',  # [6]

            # 追加1
            'gpE22_contWid_expStat_iFP': 'gpE22_contWid_isExpand',  # [5-2]

            'gpE4_contWid_expStat_iFP': 'gpE4_contWid_isExpand',  # [7]
            'gpE5_contWid_expStat_iFP': 'gpE5_contWid_isExpand',  # [8]

            # 追加と変更5
            'gpF_contWid_expStat_iFP': 'gpF_contWid_isExpand',  # [9]
            }
        self.od = OrderedDict(self.iniFileParam_contWid)  # 順序付き辞書 定義
        # .iniファイルのパラメーター設定 ##################################### end

    # オーバーライド
    # コンストラクタのまとまり4_その他A 設定
    def constructorChunk4_otherA(self):
        u""" < コンストラクタのまとまり4_その他A 設定 >

        ######################
        """
        self.doResetStat = False
        # 作成された コンテナウィジェット の高さを辞書登録
        self.container_heights = {}
        # 作成された コンテナウィジェット をリスト登録
        self.containers = []

    # オーバーライド
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
        self.tabLabelName_dict_new = {'A': 'Rename', 'B': 'Utility',
                                      'C': 'ｸﾗｽﾀ,SpIK', 'D': 'Constraint',
                                      'E': 'ﾁｬﾝﾈﾙﾎﾞｯｸｽ / current view',
                                      'F': 'Skinning',                            #追加と変更5
                                      }  # note): 数は、tabCount と等数がベスト
        # 新規 子tabラベル名 の順序付き辞書として 定義
        self.tabLabelName_oDict_new = OrderedDict(self.tabLabelName_dict_new)
        # タブの数 保存 定義
        self.tabCount__ = 0
        # クリックされたタブのインデックスを保存するための属性を追加します。
        self.clicked_tab_index = None

        # 作成された RadioButton ウィジェット 関連をリスト登録 #######################
        # self.rbtn_wid_list = []

        # 追加4
        # 作成された gpB PushButton ウィジェット 関連をリスト登録 ####################
        self.pbtnGpB_wid_list: List[QPushButton] = []

        # 作成された gpD PushButton ウィジェット 関連をリスト登録 ####################
        self.pbtnGpD_wid_list: List[QPushButton] = []

        # 作成された gpE 各コンテンツ ウィジェット 関連をリスト登録 ####################
        self.gpE_contents_wid_list: List[QWidget] = []

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

    # 新規
    # コンストラクタのまとまり7_アイコン 設定
    def constructorChunk7_icon(self):
        u""" < コンストラクタのまとまり7_アイコン 設定 >

        ######################
        """
        # # 独自で色を設定1
        # # {QLabel}.setStyleSheet(self.tooltip_style) した時だけ 独自色を設定できます
        # self.tooltip_style = """
        #     QLabel {
        #         background-color: mediumpurple;
        #         color: black;
        #     }
        #     QToolTip {
        #         background-color: lemonchiffon;
        #         color: black;
        #         border: 1px solid black;
        #     }
        # """
        # # 独自で色を設定2
        # self.bgcBlue3 = "background-color:deepskyblue; color: black"
        # self.bgcWhite = "background-color: white;"

        # アイコンを設定
        self.rotateOrderIcon = None
        self.rotateOrderIcon = self.rotateOrderIcon if self.rotateOrderIcon is not None else ':/rotate_M.png'  # maya icon を使用しています
        self.segmentScaleCompensateIcon = None
        self.segmentScaleCompensateIcon = self.segmentScaleCompensateIcon if self.segmentScaleCompensateIcon is not None else ':/kinReroot.png'  # maya icon を使用しています
        self.drawStyleIcon = None
        self.drawStyleIcon = self.drawStyleIcon if self.drawStyleIcon is not None else ':/Knife.png'  # maya icon を使用しています
        self.radiusIcon = None
        self.radiusIcon = self.radiusIcon if self.radiusIcon is not None else ':/radiusDim.png'  # maya icon を使用しています
        self.shearIcon = None
        self.shearIcon = self.shearIcon if self.shearIcon is not None else ':/smearUVTool.png'  # maya icon を使用しています

        # 追加1
        self.referenceIcon = None
        self.referenceIcon = self.referenceIcon if self.referenceIcon is not None else':/reference.png'  # maya icon を使用しています

        self.displayLocalAxisIcon = None
        self.displayLocalAxisIcon = self.displayLocalAxisIcon if self.displayLocalAxisIcon is not None else ':/locator.png'  # maya icon を使用しています
        self.backfaceCullingIcon = None
        self.backfaceCullingIcon = self.backfaceCullingIcon if self.backfaceCullingIcon is not None else ':/faces_NEX.png'  # maya icon を使用しています
        self.lineWidthIcon = None
        self.lineWidthIcon = self.lineWidthIcon if self.lineWidthIcon is not None else ':/curveAddPt.png'  # maya icon を使用しています

    # 新規
    # コンストラクタのまとまり7_アイコン 設定
    def constructorChunk8_icon(self):
        u""" < コンストラクタのまとまり8_アイコン 設定 >

        ######################
        """
        # コマンド用 アイコンを設定
        self.commandIcon = None
        self.commandIcon = self.commandIcon if self.commandIcon is not None else ':/commandButton.png'  # maya icon を使用しています
        # 追加4
        # show用 アイコンを設定
        self.showIcon = None
        self.showIcon = self.showIcon if self.showIcon is not None else ':/menuIconShow.png'  # maya icon を使用しています
        # hide用 アイコンを設定
        self.hideIcon = None
        self.hideIcon = self.hideIcon if self.hideIcon is not None else ':/QR_hide.png'  # maya icon を使用しています

    # 追加3
    # コンストラクタのまとまり9_コンテキストメニュー 設定
    def constructorChunk9_buttonContext(self):
        self.help_: str = 'Help'
        self.cmmd_: str = 'Command 例'
        self.commonMessage = (f'ボタン上 右クリック で \n'
                              f'★{self.help_}\n'
                              f'★{self.cmmd_}\n'
                              f'を 呼び出し表示 します。\n'
                              u'Script Editor をご覧ください。'
                              )
        # 追加と変更5
        self.commonMessage2 = (f'ボタン上 右クリック で \n'
                               f'★{self.help_}\n'
                               # f'★{self.cmmd_}\n'
                               f'を 呼び出し表示 します。\n'
                               u'Script Editor をご覧ください。'
                               )
        # 変更6 ######################### start
        # 追加4
        hide_: str = 'Hide'
        show_: str = 'Show'
        button_toggle_: str = 'のトグル(押下非押下)'
        button_rightClick_: str = '上 右クリック'
        self.commonMessageShowHide = (f'ボタン{button_toggle_} で \n'
                                      f'★{hide_}\n'
                                      f'★{show_}\n'
                                      f'を 呼び出し します。\n'
                                      u'Script Editor をご覧ください。')
        # 変更6 ######################### end

    # オーバーライド
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
        # 変更箇所
        self.setWindowTitle(self.title[2:] + self.space + self.version)  # <- window の title名 設定
        # self.setWindowTitle(self.title + self.space + self.version)  # <- window の title名 設定
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
        self._duplicateWindowAvoidFunction(self.win)  # 重複ウィンドウの回避関数 # note): オリジナルから引用し再利用
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

    # オーバーライド
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
        # self.frame_frWid.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # # まとまりA
        # # 大フレーム群 に収まっているものです ######################################## start
        # # UI-2. common情報
        # # 設定を施す ###################################
        self.commonInformation(main_layout = self.frame_vbxLay)  # ############################ UI-2. common情報
        tabCount__ = 6 ###################################################  # 追加と変更と新規5
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
        # self.commonButtons(button_layout = self.button_hbxLay)  # ######################## UI-3. common底面ボタン3

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

    # オーバーライド
    # UI-2. 追加オプションのまとまり
    def displayOptions(self, main_layout, tabCount_: int):
        u""" < UI-2. 追加オプションのまとまり >

        .. note:: 以下 は必須です！！

            - **self.frame_layout**
                レイアウト(大フレーム用)
                    に、
                以下の、コンテナー groupA, groupB, groupC...
                    とぶら下がります

        ::

            - groupA
                ├   rename tool 5
                └   createSpaceNode tool 3
            - groupB
                ├   nodeCreateToWorldSpace tool
                └   ...
            - groupC
                ├   createClusterAndRename tool 6
                └   createSpIkAndRename tool 3

        を一気に作成しています

        #########

        :param main_layout: self.frame_layout レイアウト(大フレーム用)
        :type main_layout:
        :param int tabCount_:
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

        self.tab_wid_: QTabWidget = tab_wid_

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

        # 各タブの定義 ################################################################# start
        # groupA ############################################################### タブA
        gdLayName = self._frame_gdLays_list[0]

        gpA_contWid: Container = self.displayOptions_gpA()
        self.frame_vbxLay.addWidget(gpA_contWid)

        gdLayName.addWidget(gpA_contWid)  # gdLayName に widName を追加
        spacer: QSpacerItem = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gdLayName.addItem(spacer)

        # groupB ############################################################### タブB
        gdLayName = self._frame_gdLays_list[1]

        gpB_contWid: Container = self.displayOptions_gpB()
        self.frame_vbxLay.addWidget(gpB_contWid)

        gdLayName.addWidget(gpB_contWid)  # gdLayName に widName を追加
        spacer: QSpacerItem = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gdLayName.addItem(spacer)

        # groupC ############################################################### タブC
        gdLayName = self._frame_gdLays_list[2]

        gpC_contWid: Container = self.displayOptions_gpC()
        self.frame_vbxLay.addWidget(gpC_contWid)

        gdLayName.addWidget(gpC_contWid)  # gdLayName に widName を追加
        spacer: QSpacerItem = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gdLayName.addItem(spacer)

        # groupD ############################################################### タブD
        gdLayName = self._frame_gdLays_list[3]

        gpD_contWid: Container = self.displayOptions_gpD()
        self.frame_vbxLay.addWidget(gpD_contWid)

        gdLayName.addWidget(gpD_contWid)  # gdLayName に widName を追加
        spacer: QSpacerItem = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gdLayName.addItem(spacer)

        # groupE ############################################################### タブE
        gdLayName = self._frame_gdLays_list[4]
        # print(gdLayName)

        # tabE のみ Container を複数ぶら下げるため QWidget です
        gpE_contWid: QWidget = self.displayOptions_gpE()
        self.frame_vbxLay.addWidget(gpE_contWid)

        gdLayName.addWidget(gpE_contWid)  # gdLayName に widName を追加
        spacer: QSpacerItem = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gdLayName.addItem(spacer)

        # 追加と変更5
        # groupF ############################################################### タブE
        gdLayName = self._frame_gdLays_list[5]
        # print(gdLayName)

        gpF_contWid: Container = self.displayOptions_gpF()
        self.frame_vbxLay.addWidget(gpF_contWid)

        gdLayName.addWidget(gpF_contWid)  # gdLayName に widName を追加
        spacer: QSpacerItem = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gdLayName.addItem(spacer)
        # 各タブの定義 ################################################################# end

        # Container の視認性を上げるために色替え
        if self.containers:
            for index, cont_index in enumerate(self.containers):
                header = cont_index.contentHeader.background_header  # header の取得
                headerContent = cont_index.contentHeader.content  # headerContent の取得
                if index % 2 == 0:
                    header.setStyleSheet(self.bgcGray)  # Set background color to gray or slategray
                    # headerContent.setStyleSheet(self.bgcGray)  # Set background color to gray or slategray
                else:
                    header.setStyleSheet(self.bgcGray2)  # Set background color to gray or slategray
                    # headerContent.setStyleSheet(self.bgcGray2)  # Set background color to gray or slategray

    # 新規
    # タブA 用
    def displayOptions_gpA(self) -> Container:
        u"""

        :return: gpA_contWid
        :rtype: Container
        """
        gpA_contWid: Container = Container("Rename")
        self.containers.append(gpA_contWid)
        gpA_contWid.setStatusTip('リネーム系ツール群')
        gpA_contWid.setToolTip('命名規則に基づいた、\n'
                               'リネームに関するツールをまとめています')
        gpA_contWid.collapse()  # 強制的に閉じる からスタート
        # clickableHeader のシグナルとスロットを接続
        gpA_clickableHeaderWid = gpA_contWid.contentHeader.clickableHeaderWidget
        gpA_clickableHeaderWid.clicked.connect(partial(self.cal_alwaysHeight_containerAll
                                                       , gpA_contWid
                                                       )
                                               )

        # 中身 ############################################################ start
        cont_gpA_gdLay = QGridLayout(gpA_contWid.contentWidget)

        # caseA1
        # rename tool 5: YO_renameTool5_main
        caseIndex = 'caseA1'
        rt = 'renameTool'
        rt_btnA_pbtnWid = QPushButton("RT")
        rt_btnA_pbtnWid.setStatusTip(rt)
        rt_btnA_pbtnWid.setToolTip(rt + ' ' + 'バージョン5(PyMel版)')
        rt_btnA_pbtnWid.setStyleSheet(self.tooltip_style)  # アノテーションカラー設定
        cont_gpA_gdLay.addWidget(rt_btnA_pbtnWid, 0, 0)
        # シグナルとスロットを接続
        rt_btnA_pbtnWid.clicked.connect(partial(self.controller.toolUIBootBtn,
                                                f'v: pBtn, {rt}',
                                                caseIndex
                                                )
                                        )  # ツールの呼び出し
        # 追加3
        # ボタン コンテキスト menu 右クリック アクション の追加 ################## start
        rt_btnA_menuWid: QMenu = QMenu()

        # help 呼び出し ################## 定義
        rt_btnA_actWid_help: QAction = QAction(
            QIcon(self.helpIcon),
            # note): self.helpIcon は、継承元 templateForPySide2_type2_View の
            #   __init__ から 読み込んでいます。
            self.help_,
            rt_btnA_menuWid
            )
        rt_btnA_menuWid.addAction(rt_btnA_actWid_help)

        # command 呼び出し ################## 定義
        rt_btnA_actWid_cmmd: QAction = QAction(
            QIcon(self.commandIcon),
            self.cmmd_,
            rt_btnA_menuWid
            )
        rt_btnA_menuWid.addAction(rt_btnA_actWid_cmmd)

        rt_btnA_pbtnWid.setContextMenuPolicy(Qt.CustomContextMenu)
        # シグナルとスロットを接続 (menu の ポジション 設定)
        rt_btnA_pbtnWid.customContextMenuRequested.connect(
            partial(self.show_contextMenu,
                    rt_btnA_pbtnWid,
                    rt_btnA_menuWid
                    )  # ボタン コンテキスト menu の ポジション 設定 関数 を利用
            )

        # help 呼び出し ################## アクション
        # シグナルとスロットを接続 (menu の 実際のアクション 設定)
        rt_btnA_actWid_help.triggered.connect(
            partial(self.controller.ui_buttonRightClick_help,
                    f'v: pBtn, {rt} help',
                    caseIndex
                    )  # 各ツールのHelp起動の呼び出し 関数 をコントロールする 関数 を利用
            )

        # command 呼び出し ################## アクション
        # シグナルとスロットを接続 (menu の 実際のアクション 設定)
        rt_btnA_actWid_cmmd.triggered.connect(
            partial(self.controller.ui_buttonRightClick_commandExample,
                    f'v: pBtn, {rt} command 例',
                    caseIndex
                    )  # 各ツールのHelp起動の呼び出し 関数 をコントロールする 関数 を利用
            )
        # ボタン コンテキスト menu 右クリック アクション の追加 ################## end

        # caseA2
        # createSpaceNode 3: YO_createSpaceNode3_main
        caseIndex = 'caseA2'
        sn = 'createSpaceNode'
        sn_btnB_pbtnWid = QPushButton("SN")
        sn_btnB_pbtnWid.setStatusTip(sn)
        sn_btnB_pbtnWid.setToolTip(sn + ' ' + 'バージョン3(PyMel版)')
        sn_btnB_pbtnWid.setStyleSheet(self.tooltip_style)  # アノテーションカラー設定
        cont_gpA_gdLay.addWidget(sn_btnB_pbtnWid, 0, 1)
        # シグナルとスロットを接続
        sn_btnB_pbtnWid.clicked.connect(partial(self.controller.toolUIBootBtn,
                                                f'v: pBtn, {sn}',
                                                caseIndex
                                                )
                                        )  # ツールの呼び出し
        # 追加3
        # ボタン コンテキスト menu 右クリック アクション の追加 ################## start
        sn_btnB_menuWid: QMenu = QMenu()

        # help 呼び出し ################## 定義
        sn_btnB_actWid_help: QAction = QAction(
            QIcon(self.helpIcon),
            # note): self.helpIcon は、継承元 templateForPySide2_type2_View の
            #   __init__ から 読み込んでいます。
            self.help_,
            sn_btnB_menuWid
            )
        sn_btnB_menuWid.addAction(sn_btnB_actWid_help)

        # command 呼び出し ################## 定義
        sn_btnB_actWid_cmmd: QAction = QAction(
            QIcon(self.commandIcon),
            self.cmmd_,
            sn_btnB_menuWid
            )
        sn_btnB_menuWid.addAction(sn_btnB_actWid_cmmd)

        sn_btnB_pbtnWid.setContextMenuPolicy(Qt.CustomContextMenu)
        # シグナルとスロットを接続 (menu の ポジション 設定)
        sn_btnB_pbtnWid.customContextMenuRequested.connect(
            partial(self.show_contextMenu,
                    sn_btnB_pbtnWid,
                    sn_btnB_menuWid
                    )  # ボタン コンテキスト menu の ポジション 設定 関数 を利用
            )

        # help 呼び出し ################## アクション
        # シグナルとスロットを接続 (menu の 実際のアクション 設定)
        sn_btnB_actWid_help.triggered.connect(
            partial(self.controller.ui_buttonRightClick_help,
                    f'v: pBtn, {sn} help',
                    caseIndex
                    )  # 各ツールのHelp起動の呼び出し 関数 をコントロールする 関数 を利用
            )

        # command 呼び出し ################## アクション
        # シグナルとスロットを接続 (menu の 実際のアクション 設定)
        sn_btnB_actWid_cmmd.triggered.connect(
            partial(self.controller.ui_buttonRightClick_commandExample,
                    f'v: pBtn, {sn} command 例',
                    caseIndex
                    )  # 各ツールのHelp起動の呼び出し 関数 をコントロールする 関数 を利用
            )
        # ボタン コンテキスト menu 右クリック アクション の追加 ################## end
        # 中身 ############################################################ end

        return gpA_contWid

    # 新規
    # タブB 用
    def displayOptions_gpB(self) -> Container:
        u"""

        :return: gpB_contWid
        :rtype: Container
        """
        gpB_contWid: Container = Container("Utility")
        self.containers.append(gpB_contWid)
        gpB_contWid.setStatusTip('汎用ツール群')
        gpB_contWid.setToolTip('汎用性のあるツールをまとめています')
        gpB_contWid.collapse()  # 強制的に閉じる からスタート
        # clickableHeader のシグナルとスロットを接続
        gpB_clickableHeaderWid = gpB_contWid.contentHeader.clickableHeaderWidget
        gpB_clickableHeaderWid.clicked.connect(partial(self.cal_alwaysHeight_containerAll
                                                       , gpB_contWid
                                                       )
                                               )
        # 中身 ######################################################################## start
        cont_gpB_gdLay = QGridLayout(gpB_contWid.contentWidget)

        # caseB1 ######################################################### start
        # nodeCreateToWorldSpace: YO_nodeCreateToWorldSpace
        caseIndex = 'caseB1'
        nodeCreateToWorldSpace = 'nodeCreateToWorldSpace'
        nc2ws_btnA_pbtnWid = QPushButton("NC2WS")
        nc2ws_btnA_pbtnWid.setStatusTip(nodeCreateToWorldSpace)
        nc2ws_btnA_pbtnWid.setToolTip(nodeCreateToWorldSpace + ' ' + 'バージョン??(?版)')
        nc2ws_btnA_pbtnWid.setStyleSheet(self.tooltip_style)  # アノテーションカラー設定
        cont_gpB_gdLay.addWidget(nc2ws_btnA_pbtnWid, 0, 0)
        # シグナルとスロットを接続
        nc2ws_btnA_pbtnWid.clicked.connect(partial(self.controller.toolUIBootBtn,
                                                   f'v: pBtn, {nodeCreateToWorldSpace}',
                                                   caseIndex
                                                   )
                                           )  # ツールの呼び出し
        self.pbtnGpB_wid_list.append(nc2ws_btnA_pbtnWid)
        # caseB1 ######################################################### end

        # 追加2
        # caseB2 ######################################################### start
        # constraintToGeometry: YO_constraintToGeometry2
        caseIndex = 'caseB2'
        constraintToGeometry = 'constraintToGeometry'
        c2g_btnBB_pbtnWid = QPushButton("C2G")
        c2g_btnBB_pbtnWid.setStatusTip(constraintToGeometry)
        c2g_btnBB_pbtnWid.setToolTip(constraintToGeometry + ' ' + 'バージョン??(?版)')
        c2g_btnBB_pbtnWid.setStyleSheet(self.tooltip_style)  # アノテーションカラー設定
        cont_gpB_gdLay.addWidget(c2g_btnBB_pbtnWid, 0, 1)
        # シグナルとスロットを接続
        c2g_btnBB_pbtnWid.clicked.connect(partial(self.controller.toolUIBootBtn,
                                                  f'v: pBtn, {constraintToGeometry}',
                                                  caseIndex
                                                  )
                                          )  # ツールの呼び出し
        self.pbtnGpB_wid_list.append(c2g_btnBB_pbtnWid)
        # caseB2 ######################################################### end

        # 追加4
        # caseB3 ######################################################### start
        # isHistoricallyInteresting: yoIsHistoricallyInteresting
        caseIndex = 'caseB3'
        isHisInt = 'isHistoricallyInteresting '
        ihi_btnC_pbtnWid = QPushButton("IHI")

        # 追加6 ######################################### start
        ihi_btnC_pbtnWid.setCheckable(True)  # トグルボタンに設定
        ihi_btnC_pbtnWid.toggled.connect(partial(self.on_button_toggled,
                                                 pushButtonName = ihi_btnC_pbtnWid,
                                                 caseIndex_ = caseIndex,
                                                 toolName = isHisInt)
                                         )  # ボタンのトグルアクションを接続
        # 追加6 ######################################### end

        # ihi_btnC_pbtnWid.setFlat(True)
        # ihi_btnC_pbtnWid.setStyleSheet("border: 1px solid white;")
        ihi_btnC_pbtnWid.setStatusTip(isHisInt)
        ihi_btnC_pbtnWid.setToolTip(isHisInt
                                    + '\n\n'
                                    + self.commonMessageShowHide
                                    )
        ihi_btnC_pbtnWid.setStyleSheet(self.tooltip_style)  # アノテーションカラー設定
        cont_gpB_gdLay.addWidget(ihi_btnC_pbtnWid, 1, 0)

        # 変更6 ######################################### start
        # # ボタン コンテキスト menu 右クリック アクション の追加 #######################
        # ihi_btnC_menuWid: QMenu = QMenu()
        # # hide 呼び出し ################## 定義
        # ihi_btnC_actWid_hide: QAction = QAction(
        #     QIcon(self.hideIcon),
        #     # note): self.helpIcon は、継承元 templateForPySide2_type2_View の
        #     #   __init__ から 読み込んでいます。
        #     self.hide_,
        #     ihi_btnC_menuWid
        #     )
        # ihi_btnC_menuWid.addAction(ihi_btnC_actWid_hide)
        # # show 呼び出し ################## 定義
        # ihi_btnC_actWid_show: QAction = QAction(
        #     QIcon(self.showIcon),
        #     self.show_,
        #     ihi_btnC_menuWid
        #     )
        # ihi_btnC_menuWid.addAction(ihi_btnC_actWid_show)
        #
        # ihi_btnC_pbtnWid.setContextMenuPolicy(Qt.CustomContextMenu)
        # # シグナルとスロットを接続 (menu の ポジション 設定)
        # ihi_btnC_pbtnWid.customContextMenuRequested.connect(
        #     partial(self.show_contextMenu,
        #             ihi_btnC_pbtnWid,
        #             ihi_btnC_menuWid
        #             )  # ボタン コンテキスト menu の ポジション 設定 関数 を利用
        #     )
        #
        # # hide 呼び出し ################## アクション
        # caseIndexOption = 'hide'
        # # シグナルとスロットを接続 (menu の 実際のアクション 設定)
        # ihi_btnC_actWid_hide.triggered.connect(
        #     partial(self.controller.ui_buttonRightClick_command,
        #             f'v: pBtn, {isHisInt} hide',
        #             caseIndex + caseIndexOption
        #             )  # 各ツールのHelp起動の呼び出し 関数 をコントロールする 関数 を利用
        #     )
        # # show 呼び出し ################## アクション
        # caseIndexOption = 'show'
        # # シグナルとスロットを接続 (menu の 実際のアクション 設定)
        # ihi_btnC_actWid_show.triggered.connect(
        #     partial(self.controller.ui_buttonRightClick_command,
        #             f'v: pBtn, {isHisInt} show',
        #             caseIndex + caseIndexOption
        #             )  # 各ツールのHelp起動の呼び出し 関数 をコントロールする 関数 を利用
        #     )
        # 変更6 ######################################### end
        self.pbtnGpB_wid_list.append(ihi_btnC_pbtnWid)
        # caseB3 ######################################################### end
        # 中身 ######################################################################## end

        # 追加4
        # PushButton の視認性を上げるために色替え e.g.): [0, 3, 4, 7, 8, 11, 12, ...] だけ色変え
        count = len(self.pbtnGpB_wid_list)
        if self.pbtnGpB_wid_list:
            # 条件に合う要素を選択して最終的なリストを作成する
            unChangeCol_pbtnWid_list: List[QPushButton] = []
            # インデックスが 0, 4, 8 の要素 選択
            for i in range(0, count, 4):
                unChangeCol_pbtnWid_list.append(self.pbtnGpB_wid_list[i])
            # インデックスが 3, 7, 11 の要素 選択
            for i in range(3, count, 4):
                unChangeCol_pbtnWid_list.append(self.pbtnGpB_wid_list[i])
            # unChangeCol_pbtnWid_list を除外したリストを changeCol_pbtnWid_list として別定義
            changeCol_pbtnWid_list: List[QPushButton] = [x for x in self.pbtnGpB_wid_list
                                                         if x not in unChangeCol_pbtnWid_list
                                                         ]
            for index in unChangeCol_pbtnWid_list:
                index.setStyleSheet(self.pBtn_tooltip_style1)  # Set background color to gray or slategray
            for index in changeCol_pbtnWid_list:
                index.setStyleSheet(self.pBtn_tooltip_style2)  # Set background color to gray or slategray

        return gpB_contWid

    # 新規
    # タブC 用
    def displayOptions_gpC(self) -> Container:
        u"""

        :return: gpC_contWid
        :rtype: Container
        """
        gpC_contWid: Container = Container("ｸﾗｽﾀ,SpIK")
        self.containers.append(gpC_contWid)
        gpC_contWid.setStatusTip('Cluster&SplineIK群')
        gpC_contWid.setToolTip('命名規則に基づいた、\n'
                               'クラスタ・SpIK作成するツールをまとめています')
        gpC_contWid.collapse()  # 強制的に閉じる からスタート
        # clickableHeader のシグナルとスロットを接続
        gpC_clickableHeaderWid = gpC_contWid.contentHeader.clickableHeaderWidget
        gpC_clickableHeaderWid.clicked.connect(partial(self.cal_alwaysHeight_containerAll
                                                       , gpC_contWid
                                                       )
                                               )
        # 中身 #############################################
        cont_gpC_gdLay = QGridLayout(gpC_contWid.contentWidget)

        # caseC1
        # createClusterAndRename 6: YO_createClusterAndRename6_main
        caseIndex = 'caseC1'
        createClusterAndRename = 'createClusterAndRename'
        cl_btnA_pbtnWid = QPushButton("CL")
        cl_btnA_pbtnWid.setStatusTip(createClusterAndRename)
        cl_btnA_pbtnWid.setToolTip(createClusterAndRename + ' ' + 'バージョン6(PyMel版)')
        cl_btnA_pbtnWid.setStyleSheet(self.tooltip_style)  # アノテーションカラー設定
        cont_gpC_gdLay.addWidget(cl_btnA_pbtnWid, 0, 0)
        # シグナルとスロットを接続
        cl_btnA_pbtnWid.clicked.connect(partial(self.controller.toolUIBootBtn,
                                                f'v: pBtn, {createClusterAndRename}',
                                                caseIndex
                                                )
                                        )  # ツールの呼び出し

        # caseC2
        # createSpIkAndRename 3: YO_createSpIkAndRename3_main
        caseIndex = 'caseC2'
        createSpIkAndRename = 'createSpIkAndRename'
        sik_btnB_pbtnWid = QPushButton("SIK")
        sik_btnB_pbtnWid.setStatusTip(createSpIkAndRename)
        sik_btnB_pbtnWid.setToolTip(createSpIkAndRename + ' ' + 'バージョン3(PyMel版)')
        sik_btnB_pbtnWid.setStyleSheet(self.tooltip_style)  # アノテーションカラー設定
        cont_gpC_gdLay.addWidget(sik_btnB_pbtnWid, 0, 1)
        # シグナルとスロットを接続
        sik_btnB_pbtnWid.clicked.connect(partial(self.controller.toolUIBootBtn,
                                                 f'v: pBtn, {createSpIkAndRename}',
                                                 caseIndex
                                                 )
                                         )  # ツールの呼び出し

        return gpC_contWid

    # 新規
    # タブD 用
    def displayOptions_gpD(self) -> Container:
        u"""

        :return: gpD_contWid
        :rtype: Container
        """
        gpD_contWid: Container = Container("Constraint")
        self.containers.append(gpD_contWid)
        gpD_contWid.setStatusTip('コンストレインツール群')
        gpD_contWid.setToolTip('個別チャンネル\n'
                               '(Translate/Point,Rotate/Orient,Scale,Shear)毎に、\n'
                               'コンストレインをマトリックスを使用して実現するツール、\n'
                               'としてまとめています')
        gpD_contWid.collapse()  # 強制的に閉じる からスタート
        # clickableHeader のシグナルとスロットを接続
        gpD_clickableHeaderWid = gpD_contWid.contentHeader.clickableHeaderWidget
        gpD_clickableHeaderWid.clicked.connect(partial(self.cal_alwaysHeight_containerAll
                                                       , gpD_contWid
                                                       )
                                               )

        # 中身 ############################################################ start
        cont_gpD_gdLay = QGridLayout(gpD_contWid.contentWidget)
        # cont_gpD_gdLay.setSpacing(5)  # ボタン間の間隔を設定

        # caseD1
        # pointConstraintByMatrix 1: YO_pointConstraintByMatrix1_main
        caseIndex: str = 'caseD1'
        pConByMat: str = 'pointConstraintByMatrix'
        pConByMat_btnA_pbtnWid: QPushButton = QPushButton("p")
        pConByMat_btnA_pbtnWid.setStatusTip(pConByMat)
        pConByMat_btnA_pbtnWid.setToolTip(pConByMat
                                          + ' ' + 'バージョン1(PyMel版)' + '\n\n'
                                          + self.commonMessage
                                          )
        # pConByMat_btnA_pbtnWid.setStyleSheet(self.pBtn_tooltip_style)  # アノテーションカラー設定
        cont_gpD_gdLay.addWidget(pConByMat_btnA_pbtnWid, 0, 0)
        # シグナルとスロットを接続
        pConByMat_btnA_pbtnWid.clicked.connect(
            partial(self.controller.toolUIBootBtn,
                    f'v: pBtn, {pConByMat}',
                    caseIndex
                    )
            )  # ツールの呼び出し
        self.pbtnGpD_wid_list.append(pConByMat_btnA_pbtnWid)
        # 追加3
        # ボタン コンテキスト menu 右クリック アクション の追加 ################## start
        pConByMat_btnA_menuWid: QMenu = QMenu()

        # help 呼び出し ################## 定義
        pConByMat_btnA_actWid_help: QAction = QAction(
            QIcon(self.helpIcon),
            # note): self.helpIcon は、継承元 templateForPySide2_type2_View の
            #   __init__ から 読み込んでいます。
            self.help_,
            pConByMat_btnA_menuWid
            )
        pConByMat_btnA_menuWid.addAction(pConByMat_btnA_actWid_help)

        # command 呼び出し ################## 定義
        pConByMat_btnA_actWid_cmmd: QAction = QAction(
            QIcon(self.commandIcon),
            self.cmmd_,
            pConByMat_btnA_menuWid
            )
        pConByMat_btnA_menuWid.addAction(pConByMat_btnA_actWid_cmmd)

        pConByMat_btnA_pbtnWid.setContextMenuPolicy(Qt.CustomContextMenu)
        # シグナルとスロットを接続 (menu の ポジション 設定)
        pConByMat_btnA_pbtnWid.customContextMenuRequested.connect(
            partial(self.show_contextMenu,
                    pConByMat_btnA_pbtnWid,
                    pConByMat_btnA_menuWid
                    )  # ボタン コンテキスト menu の ポジション 設定 関数 を利用
            )

        # help 呼び出し ################## アクション
        # シグナルとスロットを接続 (menu の 実際のアクション 設定)
        pConByMat_btnA_actWid_help.triggered.connect(
            partial(self.controller.ui_buttonRightClick_help,
                    f'v: pBtn, {pConByMat} help',
                    caseIndex
                    )  # 各ツールのHelp起動の呼び出し 関数 をコントロールする 関数 を利用
            )

        # command 呼び出し ################## アクション
        # シグナルとスロットを接続 (menu の 実際のアクション 設定)
        pConByMat_btnA_actWid_cmmd.triggered.connect(
            partial(self.controller.ui_buttonRightClick_commandExample,
                    f'v: pBtn, {pConByMat} command 例',
                    caseIndex
                    )  # 各ツールのHelp起動の呼び出し 関数 をコントロールする 関数 を利用
            )
        # ボタン コンテキスト menu 右クリック アクション の追加 ################## end

        # caseD2
        # orientConstraintByMatrix 1: YO_orientConstraintByMatrix1_main
        caseIndex: str = 'caseD2'
        oConByMat: str = 'orientConstraintByMatrix'
        oConByMat_btnA_pbtnWid: QPushButton = QPushButton("o")
        oConByMat_btnA_pbtnWid.setStatusTip(oConByMat)
        oConByMat_btnA_pbtnWid.setToolTip(oConByMat
                                          + ' ' + 'バージョン1(PyMel版)' + '\n\n'
                                          + self.commonMessage
                                          )
        # oConByMat_btnA_pbtnWid.setStyleSheet(self.tooltip_style)  # アノテーションカラー設定
        cont_gpD_gdLay.addWidget(oConByMat_btnA_pbtnWid, 0, 1)
        # シグナルとスロットを接続
        oConByMat_btnA_pbtnWid.clicked.connect(
            partial(self.controller.toolUIBootBtn,
                    f'v: pBtn, {oConByMat}',
                    caseIndex
                    )
            )  # ツールの呼び出し
        self.pbtnGpD_wid_list.append(oConByMat_btnA_pbtnWid)
        # 追加3
        # ボタン コンテキスト menu 右クリック アクション の追加 ################## start
        oConByMat_btnA_menuWid: QMenu = QMenu()

        # help 呼び出し ################## 定義
        oConByMat_btnA_actWid_help: QAction = QAction(
            QIcon(self.helpIcon),
            # note): self.helpIcon は、継承元 templateForPySide2_type2_View の
            #   __init__ から 読み込んでいます。
            self.help_,
            oConByMat_btnA_menuWid
            )
        oConByMat_btnA_menuWid.addAction(oConByMat_btnA_actWid_help)

        # command 呼び出し ################## 定義
        oConByMat_btnA_actWid_cmmd: QAction = QAction(
            QIcon(self.commandIcon),
            self.cmmd_,
            oConByMat_btnA_menuWid
            )
        oConByMat_btnA_menuWid.addAction(oConByMat_btnA_actWid_cmmd)

        oConByMat_btnA_pbtnWid.setContextMenuPolicy(Qt.CustomContextMenu)
        # シグナルとスロットを接続 (menu の ポジション 設定)
        oConByMat_btnA_pbtnWid.customContextMenuRequested.connect(
            partial(self.show_contextMenu,
                    oConByMat_btnA_pbtnWid,
                    oConByMat_btnA_menuWid
                    )  # ボタン コンテキスト menu の ポジション 設定 関数 を利用
            )

        # help 呼び出し ################## アクション
        # シグナルとスロットを接続 (menu の 実際のアクション 設定)
        oConByMat_btnA_actWid_help.triggered.connect(
            partial(self.controller.ui_buttonRightClick_help,
                    f'v: pBtn, {oConByMat} help',
                    caseIndex
                    )  # 各ツールのHelp起動の呼び出し 関数 をコントロールする 関数 を利用
            )

        # command 呼び出し ################## アクション
        # シグナルとスロットを接続 (menu の 実際のアクション 設定)
        oConByMat_btnA_actWid_cmmd.triggered.connect(
            partial(self.controller.ui_buttonRightClick_commandExample,
                    f'v: pBtn, {oConByMat} command 例',
                    caseIndex
                    )  # 各ツールのHelp起動の呼び出し 関数 をコントロールする 関数 を利用
            )
        # ボタン コンテキスト menu 右クリック アクション の追加 ################## end

        # caseD3
        # scaleConstraintByMatrix 1: YO_scaleConstraintByMatrix1_main
        caseIndex: str = 'caseD3'
        scConByMat: str = 'scaleConstraintByMatrix'
        scConByMat_btnA_pbtnWid: QPushButton = QPushButton("sc")
        scConByMat_btnA_pbtnWid.setStatusTip(scConByMat)
        scConByMat_btnA_pbtnWid.setToolTip(scConByMat
                                           + ' ' + 'バージョン1(PyMel版)' + '\n\n'
                                           + self.commonMessage
                                           )
        # scConByMat_btnA_pbtnWid.setStyleSheet(self.tooltip_style)  # アノテーションカラー設定
        cont_gpD_gdLay.addWidget(scConByMat_btnA_pbtnWid, 1, 0)
        # シグナルとスロットを接続
        scConByMat_btnA_pbtnWid.clicked.connect(
            partial(self.controller.toolUIBootBtn,
                    f'v: pBtn, {scConByMat}',
                    caseIndex
                    )
            )  # ツールの呼び出し
        self.pbtnGpD_wid_list.append(scConByMat_btnA_pbtnWid)
        # 追加3
        # ボタン コンテキスト menu 右クリック アクション の追加 ################## start
        scConByMat_btnA_menuWid: QMenu = QMenu()

        # help 呼び出し ################## 定義
        scConByMat_btnA_actWid_help: QAction = QAction(
            QIcon(self.helpIcon),
            # note): self.helpIcon は、継承元 templateForPySide2_type2_View の
            #   __init__ から 読み込んでいます。
            self.help_,
            scConByMat_btnA_menuWid
            )
        scConByMat_btnA_menuWid.addAction(scConByMat_btnA_actWid_help)

        # command 呼び出し ################## 定義
        scConByMat_btnA_actWid_cmmd: QAction = QAction(
            QIcon(self.commandIcon),
            self.cmmd_,
            scConByMat_btnA_menuWid
            )
        scConByMat_btnA_menuWid.addAction(scConByMat_btnA_actWid_cmmd)

        scConByMat_btnA_pbtnWid.setContextMenuPolicy(Qt.CustomContextMenu)
        # シグナルとスロットを接続 (menu の ポジション 設定)
        scConByMat_btnA_pbtnWid.customContextMenuRequested.connect(
            partial(self.show_contextMenu,
                    scConByMat_btnA_pbtnWid,
                    scConByMat_btnA_menuWid
                    )  # ボタン コンテキスト menu の ポジション 設定 関数 を利用
            )

        # help 呼び出し ################## アクション
        # シグナルとスロットを接続 (menu の 実際のアクション 設定)
        scConByMat_btnA_actWid_help.triggered.connect(
            partial(self.controller.ui_buttonRightClick_help,
                    f'v: pBtn, {scConByMat} help',
                    caseIndex
                    )  # 各ツールのHelp起動の呼び出し 関数 をコントロールする 関数 を利用
            )

        # command 呼び出し ################## アクション
        # シグナルとスロットを接続 (menu の 実際のアクション 設定)
        scConByMat_btnA_actWid_cmmd.triggered.connect(
            partial(self.controller.ui_buttonRightClick_commandExample,
                    f'v: pBtn, {scConByMat} command 例',
                    caseIndex
                    )  # 各ツールのHelp起動の呼び出し 関数 をコントロールする 関数 を利用
            )
        # ボタン コンテキスト menu 右クリック アクション の追加 ################## end

        # caseD4
        # shearConstraintByMatrix 1: YO_shearConstraintByMatrix1_main
        caseIndex: str = 'caseD4'
        shConByMat: str = 'shearConstraintByMatrix'
        shConByMat_btnA_pbtnWid: QPushButton = QPushButton("sh")
        shConByMat_btnA_pbtnWid.setStatusTip(shConByMat)
        shConByMat_btnA_pbtnWid.setToolTip(shConByMat
                                           + ' ' + 'バージョン1(PyMel版)' + '\n\n'
                                           + self.commonMessage
                                           )
        # shConByMat_btnA_pbtnWid.setStyleSheet(self.tooltip_style)  # アノテーションカラー設定
        cont_gpD_gdLay.addWidget(shConByMat_btnA_pbtnWid, 1, 1)
        # シグナルとスロットを接続
        shConByMat_btnA_pbtnWid.clicked.connect(
            partial(self.controller.toolUIBootBtn,
                    f'v: pBtn, {shConByMat}',
                    caseIndex
                    )
            )  # ツールの呼び出し
        self.pbtnGpD_wid_list.append(shConByMat_btnA_pbtnWid)
        # 追加3
        # ボタン コンテキスト menu 右クリック アクション の追加 ################## start
        shConByMat_btnA_menuWid: QMenu = QMenu()

        # help 呼び出し ################## 定義
        shConByMat_btnA_actWid_help: QAction = QAction(
            QIcon(self.helpIcon),
            # note): self.helpIcon は、継承元 templateForPySide2_type2_View の
            #   __init__ から 読み込んでいます。
            self.help_,
            shConByMat_btnA_menuWid
            )
        shConByMat_btnA_menuWid.addAction(shConByMat_btnA_actWid_help)

        # command 呼び出し ################## 定義
        shConByMat_btnA_actWid_cmmd: QAction = QAction(
            QIcon(self.commandIcon),
            self.cmmd_,
            shConByMat_btnA_menuWid
            )
        shConByMat_btnA_menuWid.addAction(shConByMat_btnA_actWid_cmmd)

        shConByMat_btnA_pbtnWid.setContextMenuPolicy(Qt.CustomContextMenu)
        # シグナルとスロットを接続 (menu の ポジション 設定)
        shConByMat_btnA_pbtnWid.customContextMenuRequested.connect(
            partial(self.show_contextMenu,
                    shConByMat_btnA_pbtnWid,
                    shConByMat_btnA_menuWid
                    )  # ボタン コンテキスト menu の ポジション 設定 関数 を利用
            )

        # help 呼び出し ################## アクション
        # シグナルとスロットを接続 (menu の 実際のアクション 設定)
        shConByMat_btnA_actWid_help.triggered.connect(
            partial(self.controller.ui_buttonRightClick_help,
                    f'v: pBtn, {shConByMat} help',
                    caseIndex
                    )  # 各ツールのHelp起動の呼び出し 関数 をコントロールする 関数 を利用
            )

        # command 呼び出し ################## アクション
        # シグナルとスロットを接続 (menu の 実際のアクション 設定)
        shConByMat_btnA_actWid_cmmd.triggered.connect(
            partial(self.controller.ui_buttonRightClick_commandExample,
                    f'v: pBtn, {shConByMat} command 例',
                    caseIndex
                    )  # 各ツールのHelp起動の呼び出し 関数 をコントロールする 関数 を利用
            )
        # ボタン コンテキスト menu 右クリック アクション の追加 ################## end

        # caseD5
        # parentConstraintByMatrix5: YO_parentConstraintByMatrix5
        caseIndex: str = 'caseD5'
        prConByMat5: str = 'parentConstraintByMatrix5'
        prConByMat_btnA_pbtnWid: QPushButton = QPushButton("pr5")
        prConByMat_btnA_pbtnWid.setStatusTip(prConByMat5 + '(手動)')
        prConByMat_btnA_pbtnWid.setToolTip(prConByMat5
                                           + '(手動)' + ' '
                                           + 'バージョン4(cmds版)'
                                           )
        # prConByMat_btnA_pbtnWid.setStyleSheet(self.tooltip_style)  # アノテーションカラー設定
        cont_gpD_gdLay.addWidget(prConByMat_btnA_pbtnWid, 2, 0)
        # シグナルとスロットを接続
        prConByMat_btnA_pbtnWid.clicked.connect(
            partial(self.controller.toolUIBootBtn,
                    f'v: pBtn, {prConByMat5}',
                    caseIndex
                    )
            )  # ツールの呼び出し
        self.pbtnGpD_wid_list.append(prConByMat_btnA_pbtnWid)

        # caseD6
        # parentConstraintByMatrix62: YO_parentConstraintByMatrix62
        caseIndex: str = 'caseD6'
        prConByMat62: str = 'parentConstraintByMatrix62'
        prConByMat_btnB_pbtnWid: QPushButton = QPushButton("pr62")
        prConByMat_btnB_pbtnWid.setStatusTip(prConByMat62 + '(自動)')
        prConByMat_btnB_pbtnWid.setToolTip(prConByMat62
                                           + '(自動)' + ' '
                                           + 'バージョン8(cmds版)'
                                           )
        # prConByMat_btnB_pbtnWid.setStyleSheet(self.tooltip_style)  # アノテーションカラー設定
        cont_gpD_gdLay.addWidget(prConByMat_btnB_pbtnWid, 2, 1)
        # シグナルとスロットを接続
        prConByMat_btnB_pbtnWid.clicked.connect(
            partial(self.controller.toolUIBootBtn,
                    f'v: pBtn, {prConByMat62}',
                    caseIndex
                    )
            )  # ツールの呼び出し
        self.pbtnGpD_wid_list.append(prConByMat_btnB_pbtnWid)
        # 中身 ############################################################ end

        # PushButton の視認性を上げるために色替え e.g.): [0, 3, 4, 7, 8, 11, 12, ...] だけ色変え
        count = len(self.pbtnGpD_wid_list)
        if self.pbtnGpD_wid_list:
            # 条件に合う要素を選択して最終的なリストを作成する
            unChangeCol_pbtnWid_list: List[QPushButton] = []
            # インデックスが 0, 4, 8 の要素 選択
            for i in range(0, count, 4):
                unChangeCol_pbtnWid_list.append(self.pbtnGpD_wid_list[i])
            # インデックスが 3, 7, 11 の要素 選択
            for i in range(3, count, 4):
                unChangeCol_pbtnWid_list.append(self.pbtnGpD_wid_list[i])
            # unChangeCol_pbtnWid_list を除外したリストを changeCol_pbtnWid_list として別定義
            changeCol_pbtnWid_list: List[QPushButton] = [x for x in self.pbtnGpD_wid_list
                                                         if x not in unChangeCol_pbtnWid_list
                                                         ]
            for index in unChangeCol_pbtnWid_list:
                index.setStyleSheet(self.pBtn_tooltip_style1)  # Set background color to gray or slategray
            for index in changeCol_pbtnWid_list:
                index.setStyleSheet(self.pBtn_tooltip_style2)  # Set background color to gray or slategray
        return gpD_contWid

    # 追加3
    # ボタン コンテキスト menu の ポジション 設定 関数
    def show_contextMenu(self, button: QPushButton, menu: QMenu, point: Any):
        u""" < ボタン コンテキスト menu の ポジション 設定 関数 です >

        :param QPushButton button: QPushButtonウィジェット名
        :param QMenu menu: QMenuウィジェット名
        :param Any point:
        :return : None
        """
        globalPos = button.mapToGlobal(point)
        globalPos.setX(globalPos.x())  # start: globalPos.x() + button.width() でした。
        menu.exec_(globalPos)

    # 新規
    # タブE 用
    def displayOptions_gpE(self) -> QWidget:
        u"""

        :return: wid
            Containerを複数持つ為、それらをまとめる目的の QWidget です
        :rtype: QWidget
        """
        wid: QWidget = QWidget()
        layout: QVBoxLayout = QVBoxLayout(wid)  # Container 用 縦レイアウト

        # contE1 ############################################################### Joint 一段目
        gpE1_contWid: Container = Container("Joint")
        self.containers.append(gpE1_contWid)
        gpE1_contWid.setStatusTip('Joint (channel box) 群')
        gpE1_contWid.setToolTip(u'<Joint (channel box) 群>\n\n'
                                u'rig作業で大切だと思われるアトリビュートに対して、\n'
                                u'主に、joint のチャネルボックスへの show/hide '
                                u'を容易にする目的で、\n'
                                u'ツール化。')
        gpE1_contWid.collapse()  # 強制的に閉じる からスタート
        # clickableHeader のシグナルとスロットを接続
        gpE1_clickableHeaderWid = gpE1_contWid.contentHeader.clickableHeaderWidget
        gpE1_clickableHeaderWid.clicked.connect(partial(self.cal_alwaysHeight_containerAll
                                                        , gpE1_contWid
                                                        )
                                                )
        layout.addWidget(gpE1_contWid)
        # ################################################################## 一段目 中身 start
        self.chunkContent_gpE1(contWid_contentWidget_ = gpE1_contWid.contentWidget)
        # ################################################################## 一段目 中身 end

        # contE2 ################################################################ Node 二段目
        gpE2_contWid: Container = Container("Node")
        self.containers.append(gpE2_contWid)
        gpE2_contWid.setStatusTip('Node (channel box) 群')
        gpE2_contWid.setToolTip(u'<Node (channel box) 群>\n\n'
                                u'rig作業で大切だと思われるアトリビュートに対して、\n'
                                u'node のチャネルボックスへの show/hide '
                                u'を容易にする目的で、\n'
                                u'ツール化。')
        gpE2_contWid.collapse()  # 強制的に閉じる からスタート
        # clickableHeader のシグナルとスロットを接続
        gpE2_clickableHeaderWid = gpE2_contWid.contentHeader.clickableHeaderWidget
        gpE2_clickableHeaderWid.clicked.connect(partial(self.cal_alwaysHeight_containerAll
                                                        , gpE2_contWid
                                                        )
                                                )
        layout.addWidget(gpE2_contWid)
        # ################################################################## 二段目 中身 start
        self.chunkContent_gpE2(contWid_contentWidget_ = gpE2_contWid.contentWidget)
        # ################################################################## 二段目 中身 end

        # contE3 ############################################################### Joint 三段目
        gpE3_contWid: Container = Container("Joint")
        self.containers.append(gpE3_contWid)
        gpE3_contWid.setStatusTip('Joint (current view) 群')
        gpE3_contWid.setToolTip(u'<Joint (current view) 群>\n\n'
                                u'rig作業で大切だと思われるアトリビュートに対して、\n'
                                u'主に、joint への その他のアトリビュートへのアクセス '
                                u'を容易にする目的で、\n'
                                u'ツール化。')
        gpE3_contWid.collapse()  # 強制的に閉じる からスタート
        # clickableHeader のシグナルとスロットを接続
        gpE3_clickableHeaderWid = gpE3_contWid.contentHeader.clickableHeaderWidget
        gpE3_clickableHeaderWid.clicked.connect(partial(self.cal_alwaysHeight_containerAll
                                                        , gpE3_contWid
                                                        )
                                                )
        layout.addWidget(gpE3_contWid)
        # ################################################################## 三段目 中身 start
        self.chunkContent_gpE3(contWid_contentWidget_ = gpE3_contWid.contentWidget)
        # ################################################################## 三段目 中身 end

        # 追加1
        # contE2-2 ############################################################### Node 四段目
        gpE22_contWid: Container = Container("Node")
        self.containers.append(gpE22_contWid)
        gpE22_contWid.setStatusTip('Node (current view) 群')
        gpE22_contWid.setToolTip(u'<Node (current view) 群>\n\n'
                                 u'rig作業で大切だと思われるアトリビュートに対して、\n'
                                 u'主に、Node への その他のアトリビュートへのアクセス '
                                 u'を容易にする目的で、\n'
                                 u'ツール化。')
        gpE22_contWid.collapse()  # 強制的に閉じる からスタート
        # clickableHeader のシグナルとスロットを接続
        gpE3_clickableHeaderWid = gpE22_contWid.contentHeader.clickableHeaderWidget
        gpE3_clickableHeaderWid.clicked.connect(partial(self.cal_alwaysHeight_containerAll
                                                        , gpE22_contWid
                                                        )
                                                )
        layout.addWidget(gpE22_contWid)
        # ################################################################## 三段目 中身 start
        self.chunkContent_gpE22(contWid_contentWidget_ = gpE22_contWid.contentWidget)
        # ################################################################## 三段目 中身 end

        # contE4 ################################################################ Mesh 四段目
        gpE4_contWid: Container = Container("Mesh")
        self.containers.append(gpE4_contWid)
        gpE4_contWid.setStatusTip('Mesh (current view) 群')
        gpE4_contWid.setToolTip(u'<Mesh (current view) 群>\n\n'
                                u'rig作業で大切だと思われるアトリビュートに対して、\n'
                                u'主に、mesh コンポーネントへのアクセス '
                                u'を容易にする目的で、\n'
                                u'ツール化。')
        gpE4_contWid.collapse()  # 強制的に閉じる からスタート
        # clickableHeader のシグナルとスロットを接続
        gpE4_clickableHeaderWid = gpE4_contWid.contentHeader.clickableHeaderWidget
        gpE4_clickableHeaderWid.clicked.connect(partial(self.cal_alwaysHeight_containerAll
                                                        , gpE4_contWid
                                                        )
                                                )
        layout.addWidget(gpE4_contWid)
        # ################################################################## 四段目 中身 start
        self.chunkContent_gpE4(contWid_contentWidget_ = gpE4_contWid.contentWidget)
        # ################################################################## 四段目 中身 end

        # contE5 ############################################################### Curve 五段目
        gpE5_contWid: Container = Container("Curve")
        self.containers.append(gpE5_contWid)
        gpE5_contWid.setStatusTip('Curve (channel box) 群')
        gpE5_contWid.setToolTip(u'<Curve (channel box) 群>\n\n'
                                u'rig作業で大切だと思われるアトリビュートに対して、\n'
                                u'主に、curve コンポーネントへのアクセス '
                                u'を容易にする目的で、\n'
                                u'ツール化。')
        gpE5_contWid.collapse()  # 強制的に閉じる からスタート
        # clickableHeader のシグナルとスロットを接続
        gpE5_clickableHeaderWid = gpE5_contWid.contentHeader.clickableHeaderWidget
        gpE5_clickableHeaderWid.clicked.connect(partial(self.cal_alwaysHeight_containerAll
                                                        , gpE5_contWid
                                                        )
                                                )
        layout.addWidget(gpE5_contWid)
        # ################################################################## 五段目 中身 start
        self.chunkContent_gpE5(contWid_contentWidget_ = gpE5_contWid.contentWidget)
        # ################################################################## 五段目 中身 end

        # contents_wid の視認性を上げるために色替え
        for index, contentsIndex in enumerate(self.gpE_contents_wid_list):
            if index % 2 == 0:
                contentsIndex.setStyleSheet(self.wid_tooltip_style1)  # Set background color to gray or slategray
            else:
                contentsIndex.setStyleSheet(self.wid_tooltip_style2)  # Set background color to gray or slategray
        return wid

    # 新規
    # タブE container1 Joint 用(channel box 表示)
    def chunkContent_gpE1(self, contWid_contentWidget_):
        contentE1_layout: QGridLayout = QGridLayout(contWid_contentWidget_)

        # rotateOrder(ro) <caseE1_1j> ########################################## start
        caseIndex = 'caseE1_1j'
        longName = 'rotateOrder'
        shortName = 'ro'
        hBxWid_ro = QWidget()
        # 水平レイアウトの作成
        hBxLay_ro = QHBoxLayout(hBxWid_ro)
        hBxWid_ro.setToolTip(f'{longName}({shortName}):\n\n'
                             u'カレントの選択ノード joint のチャンネルボックスへの、\n'
                             f'{longName}({shortName}) アトリビュート の show/hide を'
                             u'コントロールします。\n'
                             u'複数選択でも実行可。')
        self.gpE_contents_wid_list.append(hBxWid_ro)  # gpE 各コンテンツ 登録

        # iconラベル の作成
        iconLabel_ro = QLabel()
        # iconラベル を 中央揃え にする
        # iconLabel_ro.setAlignment(Qt.AlignCenter)
        # icon を 設定
        pixmap_ro = QPixmap(self.rotateOrderIcon)
        iconLabel_ro.setPixmap(pixmap_ro)
        # iconラベル を 水平レイアウト に追加
        hBxLay_ro.addWidget(iconLabel_ro)

        # iconラベル の 右隣に表示する label を作成
        label_ro = QLabel(shortName)  # 任意の説明テキスト
        # label を 中央揃え にする
        label_ro.setAlignment(Qt.AlignCenter)
        # label を 水平レイアウト に追加
        hBxLay_ro.addWidget(label_ro)

        # CheckBox を作成
        cBxWid_ro: QCheckBox = QCheckBox('show\n/hide', self)
        cBxWid_ro.stateChanged.connect(partial(self.toggle_checkBox
                                               , caseIndex
                                               , cBxWid_ro
                                               , longName
                                               )  # note): 引数に state は不要です
                                       )
        hBxLay_ro.addWidget(cBxWid_ro)

        # 水平レイアウト を 垂直レイアウト に追加
        contentE1_layout.addWidget(hBxWid_ro, 0, 0)
        # rotateOrder(ro) <caseE1_1j> ########################################## end

        # segmentScaleCompensate(ssc) <caseE1_2j> ############################## start
        caseIndex = 'caseE1_2j'
        longName = 'segmentScaleCompensate'
        shortName = 'ssc'
        hBxWid_ssc = QWidget()
        # 水平レイアウトの作成
        hBxLay_ssc = QHBoxLayout(hBxWid_ssc)
        hBxWid_ssc.setToolTip(f'{longName}({shortName}):\n\n'
                              u'カレントの選択ノード joint のチャンネルボックスへの、\n'
                              f'{longName}({shortName}) アトリビュート の show/hide を'
                              u'コントロールします。\n'
                              u'複数選択でも実行可。')
        self.gpE_contents_wid_list.append(hBxWid_ssc)  # gpE 各コンテンツ 登録

        # iconラベル の作成
        iconLabel_ssc = QLabel()
        # iconラベル を 中央揃え にする
        # iconLabel_ssc.setAlignment(Qt.AlignCenter)
        # icon を 設定
        pixmap_ssc = QPixmap(self.segmentScaleCompensateIcon)
        iconLabel_ssc.setPixmap(pixmap_ssc)
        # iconラベル を 水平レイアウト に追加
        hBxLay_ssc.addWidget(iconLabel_ssc)

        # iconラベル の 右隣に表示する label を作成
        label_ssc = QLabel(shortName)  # 任意の説明テキスト
        # label を 中央揃え にする
        label_ssc.setAlignment(Qt.AlignCenter)
        # label を 水平レイアウト に追加
        hBxLay_ssc.addWidget(label_ssc)

        # CheckBox を作成
        cBxWid_ssc: QCheckBox = QCheckBox('show\n/hide', self)
        cBxWid_ssc.stateChanged.connect(partial(self.toggle_checkBox
                                                , caseIndex
                                                , cBxWid_ssc
                                                , longName
                                                )  # note): 引数に state は不要です
                                        )
        hBxLay_ssc.addWidget(cBxWid_ssc)

        # 水平レイアウト を 垂直レイアウト に追加
        contentE1_layout.addWidget(hBxWid_ssc, 1, 0)
        # segmentScaleCompensate(ssc) <caseE1_2j> ############################## end

        # drawStyle(ds) <caseE1_3j> ############################################ start
        caseIndex = 'caseE1_3j'
        longName = 'drawStyle'
        shortName = 'ds'

        mainWid_ds = QWidget()  # 2つの QHBoxLayout() をまとめます
        # 垂直レイアウト の作成
        mainLay_ds = QVBoxLayout(mainWid_ds)
        mainWid_ds.setToolTip(f'{longName}({shortName}):\n\n'
                              u'カレントの選択ノード joint のチャンネルボックスへの、\n'
                              f'{longName}({shortName}) アトリビュート の show/hide を'
                              u'コントロールします。\n'
                              u'複数選択でも実行可。')
        self.gpE_contents_wid_list.append(mainWid_ds)  # gpE 各コンテンツ 登録

        # #####################################################################
        # QHBoxLayout を２つ作成
        hbxLay1 = QHBoxLayout()  # 要素1, 要素2, 要素3
        hbxLay2 = QHBoxLayout()  # 要素4 のみ
        # ##################################################################
        # 要素1 ######################################## add_to_hbxLay1
        # iconラベル の作成
        iconLabel_ds = QLabel()
        # iconラベル を 中央揃え にする
        # iconLabel_ssc.setAlignment(Qt.AlignCenter)
        # icon を 設定
        pixmap_ds = QPixmap(self.drawStyleIcon)
        iconLabel_ds.setPixmap(pixmap_ds)
        # iconラベル を 水平レイアウト に追加
        hbxLay1.addWidget(iconLabel_ds)
        # 要素2 ######################################## add_to_hbxLay1
        # iconラベル の 右隣に表示する label を作成
        label_ds = QLabel(shortName)  # 任意の説明テキスト
        # label を 中央揃え にする
        label_ds.setAlignment(Qt.AlignCenter)
        # label を 水平レイアウト に追加
        hbxLay1.addWidget(label_ds)
        # 要素3 ######################################## add_to_hbxLay1
        # CheckBox を作成
        cBxWid_ds: QCheckBox = QCheckBox('show\n/hide', self)
        cBxWid_ds.stateChanged.connect(partial(self.toggle_checkBox
                                               , caseIndex
                                               , cBxWid_ds
                                               , longName
                                               )  # note): 引数に state は不要です
                                       )
        hbxLay1.addWidget(cBxWid_ds)
        # 要素4 ######################################## add_to_hbxLay2
        btn1_ds = QPushButton('UI')
        btn1_ds.setStyleSheet(self.pBtn_tooltip_style3)
        btn1_ds.setFixedWidth(25)
        hbxLay2.addWidget(btn1_ds)
        # シグナルとスロットを接続
        jointDrawStyle_change = 'jointDrawStyle_change'
        btn1_ds.clicked.connect(partial(self.controller.toolUIBootBtn,
                                        f'v: pBtn, {jointDrawStyle_change}',
                                        caseIndex
                                        )
                                )  # ツールの呼び出し
        # ##################################################################
        # 垂直レイアウト へ 水平レイアウト x 2 を追加
        mainLay_ds.addLayout(hbxLay1)
        mainLay_ds.addLayout(hbxLay2)
        # #####################################################################
        # 水平レイアウト を 垂直レイアウト に追加
        contentE1_layout.addWidget(mainWid_ds, 2, 0)
        # drawStyle(ds) <caseE1_3j> ############################################ end

        # radius(radi) <caseE1_4j> ############################################# start
        caseIndex = 'caseE1_4j'
        longName = 'radius'
        shortName = 'radi'

        mainWid_radi = QWidget()  # 2つの QHBoxLayout() をまとめます
        # 垂直レイアウト の作成
        mainLay_radi = QVBoxLayout(mainWid_radi)
        mainWid_radi.setToolTip(f'{longName}({shortName}):\n\n'
                                u'カレントの選択ノード joint のチャンネルボックスへの、\n'
                                f'{longName}({shortName}) アトリビュート の show/hide を'
                                u'コントロールします。\n'
                                u'複数選択でも実行可。')
        self.gpE_contents_wid_list.append(mainWid_radi)  # gpE 各コンテンツ 登録

        # #####################################################################
        # QHBoxLayout を２つ作成
        hbxLay1 = QHBoxLayout()  # 要素1, 要素2, 要素3
        hbxLay2 = QHBoxLayout()  # 要素4 のみ
        # ##################################################################
        # 要素1 ######################################## add_to_hbxLay1
        # iconラベル の作成
        iconLabel_radi = QLabel()
        # iconラベル を 中央揃え にする
        # iconLabel_radi.setAlignment(Qt.AlignCenter)
        # icon を 設定
        pixmap_radi = QPixmap(self.radiusIcon)
        iconLabel_radi.setPixmap(pixmap_radi)
        # iconラベル を 水平レイアウト に追加
        hbxLay1.addWidget(iconLabel_radi)
        # 要素2 ######################################## add_to_hbxLay1
        # iconラベル の 右隣に表示する label を作成
        label_radi = QLabel(shortName)  # 任意の説明テキスト
        # label を 中央揃え にする
        label_radi.setAlignment(Qt.AlignCenter)
        # label を 水平レイアウト に追加
        hbxLay1.addWidget(label_radi)
        # 要素3 ######################################## add_to_hbxLay1
        # CheckBox を作成
        cBx_radi: QCheckBox = QCheckBox('show\n/hide', self)
        cBx_radi.stateChanged.connect(partial(self.toggle_checkBox
                                              , caseIndex
                                              , cBx_radi
                                              , longName
                                              )  # note): 引数に state は不要です
                                      )
        hbxLay1.addWidget(cBx_radi)
        # 要素4 ######################################## add_to_hbxLay2
        btn1_radi = QPushButton('UI')
        btn1_radi.setStyleSheet(self.pBtn_tooltip_style3)
        btn1_radi.setFixedWidth(25)
        hbxLay2.addWidget(btn1_radi)
        # シグナルとスロットを接続
        jointRadiusSlider = 'jointRadiusSlider'
        btn1_radi.clicked.connect(partial(self.controller.toolUIBootBtn,
                                          f'v: pBtn, {jointRadiusSlider}',
                                          caseIndex
                                          )
                                  )  # ツールの呼び出し
        # ##################################################################
        # 垂直レイアウト へ 水平レイアウト x 2 を追加
        mainLay_radi.addLayout(hbxLay1)
        mainLay_radi.addLayout(hbxLay2)
        # #####################################################################
        # 水平レイアウト を 垂直レイアウト に追加
        contentE1_layout.addWidget(mainWid_radi, 3, 0)
        # radius(radi) <caseE1_4j> ############################################# end

    # 新規
    # タブE container2 Node 用(channel box 表示)
    def chunkContent_gpE2(self, contWid_contentWidget_):
        contentE2_layout: QGridLayout = QGridLayout(contWid_contentWidget_)

        # shear(sh) <caseE2_1n> ################################################ start
        caseIndex = 'caseE2_1n'
        longName = 'shear'
        shortName = 'sh'
        hBxWid_sh = QWidget()
        # 水平レイアウトの作成
        hBxLay_sh = QHBoxLayout(hBxWid_sh)
        hBxWid_sh.setToolTip(f'{longName}({shortName}):\n\n'
                             u'カレントの選択ノードのチャンネルボックスへの、\n'
                             f'{longName}({shortName}) アトリビュート の show/hide を'
                             u'コントロールします。\n'
                             u'複数選択でも実行可。')
        self.gpE_contents_wid_list.append(hBxWid_sh)  # gpE 各コンテンツ 登録

        # iconラベル の作成
        iconLabel_sh = QLabel()
        # iconラベル を 中央揃え にする
        # iconLabel_sh.setAlignment(Qt.AlignCenter)
        # icon を 設定
        pixmap_sh = QPixmap(self.shearIcon)
        iconLabel_sh.setPixmap(pixmap_sh)
        # iconラベル を 水平レイアウト に追加
        hBxLay_sh.addWidget(iconLabel_sh)

        # iconラベル の 右隣に表示する label を作成
        label_sh = QLabel(shortName)  # 任意の説明テキスト
        # label を 中央揃え にする
        label_sh.setAlignment(Qt.AlignCenter)
        # label を 水平レイアウト に追加
        hBxLay_sh.addWidget(label_sh)

        # CheckBox を作成
        cBxWid_sh: QCheckBox = QCheckBox('show\n/hide', self)
        cBxWid_sh.stateChanged.connect(partial(self.toggle_checkBox
                                               , caseIndex
                                               , cBxWid_sh
                                               , longName
                                               )  # note): 引数に state は不要です
                                       )
        hBxLay_sh.addWidget(cBxWid_sh)

        # 水平レイアウト を 垂直レイアウト に追加
        contentE2_layout.addWidget(hBxWid_sh, 0, 0)
        # shear(sh) <caseE2_1n> ################################################ end

    # 新規
    # タブE container3 Joint 用(current view 表示)
    def chunkContent_gpE3(self, contWid_contentWidget_):
        contentE3_layout: QGridLayout = QGridLayout(contWid_contentWidget_)

        # displayLocalAxis(dla) <caseE3_1jv> ################################### start
        caseIndex = 'caseE3_1jv'
        longName = 'displayLocalAxis'
        shortName = 'dla'
        hBxWid_dla = QWidget()
        # 水平レイアウトの作成
        hBxLay_dla = QHBoxLayout(hBxWid_dla)
        hBxWid_dla.setToolTip(f'{longName}({shortName}):\n\n'
                              u'カレントの選択ノード joint への、\n'
                              u'current view上での表示 の show/hide を'
                              u'コントロールします。\n'
                              u'複数選択でも実行可。')
        self.gpE_contents_wid_list.append(hBxWid_dla)  # gpE 各コンテンツ 登録

        # iconラベル の作成
        iconLabel_dla = QLabel()
        # iconラベル を 中央揃え にする
        # iconLabel_dla.setAlignment(Qt.AlignCenter)
        # icon を 設定
        pixmap_dla = QPixmap(self.displayLocalAxisIcon)
        iconLabel_dla.setPixmap(pixmap_dla)
        # iconラベル を 水平レイアウト に追加
        hBxLay_dla.addWidget(iconLabel_dla)

        # iconラベル の 右隣に表示する label を作成
        label_dla = QLabel(shortName)  # 任意の説明テキスト
        # label を 中央揃え にする
        label_dla.setAlignment(Qt.AlignCenter)
        # label を 水平レイアウト に追加
        hBxLay_dla.addWidget(label_dla)

        # CheckBox を作成
        cBxWid_dla: QCheckBox = QCheckBox('show\n/hide', self)
        cBxWid_dla.stateChanged.connect(partial(self.toggle_checkBox
                                                , caseIndex
                                                , cBxWid_dla
                                                , longName
                                                )  # note): 引数に state は不要です
                                        )
        hBxLay_dla.addWidget(cBxWid_dla)

        # 水平レイアウト を 垂直レイアウト に追加
        contentE3_layout.addWidget(hBxWid_dla, 0, 0)

    # 追加1
    # タブE container22 Node 用(current view 表示)
    def chunkContent_gpE22(self, contWid_contentWidget_):
        contentE3_layout: QGridLayout = QGridLayout(contWid_contentWidget_)

        # reference(ref) <caseE22_1nv> ################################### start
        caseIndex = 'caseE22_1nv'
        longName = 'reference'
        shortName = 'ref'
        hBxWid_ref = QWidget()
        # 水平レイアウトの作成
        hBxLay_ref = QHBoxLayout(hBxWid_ref)
        hBxWid_ref.setToolTip(f'{longName}({shortName}):\n\n'
                              u'カレントの選択ノード node への、\n'
                              u'current view上での表示 の normal/reference を'
                              u'コントロールします。\n'
                              u'複数選択でも実行可。')
        self.gpE_contents_wid_list.append(hBxWid_ref)  # gpE 各コンテンツ 登録

        # iconラベル の作成
        iconLabel_ref = QLabel()
        # iconラベル を 中央揃え にする
        # iconLabel_ref.setAlignment(Qt.AlignCenter)
        # icon を 設定
        pixmap_ref = QPixmap(self.referenceIcon)
        iconLabel_ref.setPixmap(pixmap_ref)
        # iconラベル を 水平レイアウト に追加
        hBxLay_ref.addWidget(iconLabel_ref)

        # iconラベル の 右隣に表示する label を作成
        label_ref = QLabel(shortName)  # 任意の説明テキスト
        # label を 中央揃え にする
        label_ref.setAlignment(Qt.AlignCenter)
        # label を 水平レイアウト に追加
        hBxLay_ref.addWidget(label_ref)

        # CheckBox を作成
        cBxWid_ref: QCheckBox = QCheckBox('normal\n/reference', self)
        cBxWid_ref.stateChanged.connect(partial(self.toggle_checkBox
                                                , caseIndex
                                                , cBxWid_ref
                                                , longName
                                                )  # note): 引数に state は不要です
                                        )
        hBxLay_ref.addWidget(cBxWid_ref)

        # 水平レイアウト を 垂直レイアウト に追加
        contentE3_layout.addWidget(hBxWid_ref, 0, 0)

    # 新規
    # タブE container4 Mesh 用(current view 表示)
    def chunkContent_gpE4(self, contWid_contentWidget_):
        contentE4_layout: QGridLayout = QGridLayout(contWid_contentWidget_)

        # backfaceCulling(bck) <caseE4_1mv> #################################### start
        caseIndex = 'caseE4_1mv'
        longName = 'backfaceCulling'
        shortName = 'bck'
        hBxWid_bck = QWidget()
        # 水平レイアウトの作成
        hBxLay_bck = QHBoxLayout(hBxWid_bck)
        hBxWid_bck.setToolTip(f'{longName}({shortName}):\n\n'
                              u'カレントの選択ノード mesh への、\n'
                              u'current view上での表示 の on/off を'
                              u'コントロールします。\n'
                              u'複数選択でも実行可。')
        self.gpE_contents_wid_list.append(hBxWid_bck)  # gpE 各コンテンツ 登録

        # iconラベル の作成
        iconLabel_bck = QLabel()
        # iconラベル を 中央揃え にする
        # iconLabel_bck.setAlignment(Qt.AlignCenter)
        # icon を 設定
        pixmap_bck = QPixmap(self.backfaceCullingIcon)
        iconLabel_bck.setPixmap(pixmap_bck)
        # iconラベル を 水平レイアウト に追加
        hBxLay_bck.addWidget(iconLabel_bck)

        # iconラベル の 右隣に表示する label を作成
        label_bck = QLabel(shortName)  # 任意の説明テキスト
        # label を 中央揃え にする
        label_bck.setAlignment(Qt.AlignCenter)
        # label を 水平レイアウト に追加
        hBxLay_bck.addWidget(label_bck)

        # CheckBox を作成
        cBxWid_bck: QCheckBox = QCheckBox('on\n/off', self)
        cBxWid_bck.stateChanged.connect(partial(self.toggle_checkBox
                                                , caseIndex
                                                , cBxWid_bck
                                                , longName
                                                )  # note): 引数に state は不要です
                                        )
        hBxLay_bck.addWidget(cBxWid_bck)

        # 水平レイアウト を 垂直レイアウト に追加
        contentE4_layout.addWidget(hBxWid_bck, 0, 0)

    # 新規
    # タブE container5 Curve 用(channel box 表示)
    def chunkContent_gpE5(self, contWid_contentWidget_):
        contentE5_layout = QGridLayout(contWid_contentWidget_)

        # lineWidth(ls) <caseE5_1c> ########################################## start
        caseIndex = 'caseE5_1c'
        longName = 'lineWidth'
        shortName = 'ls'
        hBxWid_ls = QWidget()
        # 水平レイアウトの作成
        hBxLay_ls = QHBoxLayout(hBxWid_ls)
        hBxWid_ls.setToolTip(f'{longName}({shortName}):\n\n'
                             u'カレントの選択ノード curve のチャンネルボックスへの、\n'
                             f'{longName}({shortName}) アトリビュート の show/hide を'
                             u'コントロールします。\n'
                             u'複数選択でも実行可。')
        self.gpE_contents_wid_list.append(hBxWid_ls)  # gpE 各コンテンツ 登録

        # iconラベル の作成
        iconLabel_ls = QLabel()
        # iconラベル を 中央揃え にする
        # iconLabel_ls.setAlignment(Qt.AlignCenter)
        # icon を 設定
        pixmap_ls = QPixmap(self.lineWidthIcon)
        iconLabel_ls.setPixmap(pixmap_ls)
        # iconラベル を 水平レイアウト に追加
        hBxLay_ls.addWidget(iconLabel_ls)

        # iconラベル の 右隣に表示する label を作成
        label_ls = QLabel(shortName)  # 任意の説明テキスト
        # label を 中央揃え にする
        label_ls.setAlignment(Qt.AlignCenter)
        # label を 水平レイアウト に追加
        hBxLay_ls.addWidget(label_ls)

        # CheckBox を作成
        cBxWid_ls: QCheckBox = QCheckBox('show\n/hide', self)
        cBxWid_ls.stateChanged.connect(partial(self.toggle_checkBox
                                               , caseIndex
                                               , cBxWid_ls
                                               , longName
                                               )  # note): 引数に state は不要です
                                       )
        hBxLay_ls.addWidget(cBxWid_ls)

        # 水平レイアウト を 垂直レイアウト に追加
        contentE5_layout.addWidget(hBxWid_ls, 0, 0)
        # rotateOrder(ro) <caseE1_1j> ########################################## end

    # 新規6
    # タブB IHI 用(toggle button control)
    def on_button_toggled(self, checked: Any,
                          pushButtonName: QPushButton,
                          caseIndex_: str,
                          toolName: str,
                          ):
        u""" < タブB IHI 用(toggle button control)関数 です >

        :param bool checked: True or False
            引数 checked はスロット関数で必要です。
            シグナル toggled はボタンのチェック状態が変わるときに呼び出され、
            その際に新しいチェック状態（True または False）を引数として渡します。
            この引数を受け取るために、スロット関数で引数を定義する必要があります。
            e.g.):
                ihi_btnC_pbtnWid.toggled.connect(partial(self.on_button_toggled,
                                                 pushButtonName = ihi_btnC_pbtnWid,
                                                 caseIndex_ = caseIndex,
                                                 name = isHisInt)
                                         )  # ボタンのトグルアクションを接続
                のように、self.on_button_toggled(...) を使用する際は、
                checked 引数 は不要です。
        :param QPushButton pushButtonName: QPushButton インスタンス名です
        :param str caseIndex_: 後のコマンド実行時の、独自判別識別子です
        :param str toolName: tool の名前です
        """
        # print(pushButtonName, caseIndex_, name)
        if checked:
            # print('hide')
            caseIndexOption = 'hide'
            pushButtonName.setText("IHI: Hide")
        else:
            # print('show')
            caseIndexOption = 'show'
            pushButtonName.setText("IHI: Show")
        # 誤りです ########################### start
        # b/c):
        #   toggled シグナルが発生するたびに新しい clicked シグナルとスロットの接続が追加されるため、
        #   累積していくことによって起きています。
        #   これを防ぐためには、ボタンの clicked シグナルとスロットの接続を一度だけ行うようにする必要があります。
        # # シグナルとスロットを接続
        # pushButtonName.clicked.connect(
        #     partial(self.controller.toolUIBootBtn,
        #             f'v: pBtn, {toolName} {caseIndexOption}', caseIndex_ + caseIndexOption
        #             )
        #     )  # ツールの呼び出し
        # 誤りです ########################### end
        self.controller.toolUIBootBtn(f'v: pBtn, {toolName} {caseIndexOption}',
                                      caseIndex_ + caseIndexOption
                                      )

    # 追加と変更と新規5
    # タブF 用
    def displayOptions_gpF(self) -> Container:
        u"""

        :return: gpF_contWid
        :rtype: Container
        """
        gpF_contWid: Container = Container("Skinning")
        self.containers.append(gpF_contWid)
        gpF_contWid.setStatusTip('Skinning系支援ツール群')
        gpF_contWid.setToolTip('Skinning作業に関する、\n'
                               '支援ツールをまとめています')
        gpF_contWid.collapse()  # 強制的に閉じる からスタート
        # clickableHeader のシグナルとスロットを接続
        gpF_clickableHeaderWid = gpF_contWid.contentHeader.clickableHeaderWidget
        gpF_clickableHeaderWid.clicked.connect(partial(self.cal_alwaysHeight_containerAll
                                                       , gpF_contWid
                                                       )
                                               )

        # 中身 ############################################################ start
        cont_gpF_gdLay = QGridLayout(gpF_contWid.contentWidget)

        # caseF1
        # skin Weights ExpImp Tool: skinWeightsExpImpTool
        caseIndex = 'caseF1'
        skExpImp = 'skinWeightsExpImpTool'
        skExpImp_btnA_pbtnWid = QPushButton("ExpImp")
        skExpImp_btnA_pbtnWid.setStatusTip(skExpImp)
        skExpImp_btnA_pbtnWid.setToolTip(skExpImp + ' ' + 'ui:PySide2'
                                         + '\n\n'
                                         + self.commonMessage2
                                         )
        skExpImp_btnA_pbtnWid.setStyleSheet(self.tooltip_style)  # アノテーションカラー設定
        cont_gpF_gdLay.addWidget(skExpImp_btnA_pbtnWid, 0, 0)
        # シグナルとスロットを接続
        skExpImp_btnA_pbtnWid.clicked.connect(partial(self.controller.toolUIBootBtn,
                                                      f'v: pBtn, {skExpImp}',
                                                      caseIndex
                                                      )
                                              )  # ツールの呼び出し
        # ボタン コンテキスト menu 右クリック アクション の追加 ################## start
        skExpImp_btnA_menuWid: QMenu = QMenu()

        # help 呼び出し ################## 定義
        skExpImp_btnA_actWid_help: QAction = QAction(
            QIcon(self.helpIcon),
            # note): self.helpIcon は、継承元 templateForPySide2_type2_View の
            #   __init__ から 読み込んでいます。
            self.help_,
            skExpImp_btnA_menuWid
            )
        skExpImp_btnA_menuWid.addAction(skExpImp_btnA_actWid_help)

        # command 呼び出し ################## 定義
        skExpImp_btnA_actWid_cmmd: QAction = QAction(
            QIcon(self.commandIcon),
            self.cmmd_,
            skExpImp_btnA_menuWid
            )
        skExpImp_btnA_actWid_cmmd.setDisabled(True)
        skExpImp_btnA_menuWid.addAction(skExpImp_btnA_actWid_cmmd)

        skExpImp_btnA_pbtnWid.setContextMenuPolicy(Qt.CustomContextMenu)
        # シグナルとスロットを接続 (menu の ポジション 設定)
        skExpImp_btnA_pbtnWid.customContextMenuRequested.connect(
            partial(self.show_contextMenu,
                    skExpImp_btnA_pbtnWid,
                    skExpImp_btnA_menuWid
                    )  # ボタン コンテキスト menu の ポジション 設定 関数 を利用
            )

        # help 呼び出し ################## アクション
        # シグナルとスロットを接続 (menu の 実際のアクション 設定)
        skExpImp_btnA_actWid_help.triggered.connect(
            partial(self.controller.ui_buttonRightClick_help,
                    f'v: pBtn, {skExpImp} help', caseIndex
                    )  # 各ツールのHelp起動の呼び出し 関数 をコントロールする 関数 を利用
            )

        # command 呼び出し ################## アクション
        # シグナルとスロットを接続 (menu の 実際のアクション 設定)
        skExpImp_btnA_actWid_cmmd.triggered.connect(
            partial(self.controller.ui_buttonRightClick_commandExample,
                    f'v: pBtn, {skExpImp} command 例', caseIndex
                    )  # 各ツールのHelp起動の呼び出し 関数 をコントロールする 関数 を利用
            )
        # ボタン コンテキスト menu 右クリック アクション の追加 ################## end
        # 中身 ############################################################ end

        return gpF_contWid
    # UIディテール 作成 ################################################################ end

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

        # tabウィジェット の情報を 保存
        getTabCurrentIndex = self.tab_wid_.currentIndex()
        # print(getTabCurrentIndex)
        self._settings.setValue(self.iniFileParam['tab_wid_selection_iFP']
                                , getTabCurrentIndex
                                )

        # # ウィジェット(コンテナA用) の情報を 保存
        # contA_wid_isExpand, _ = gpA_contWid.contentHeader.outPut_content_status()
        # self._settings.setValue(self.iniFileParam['gpA_contWid_expStat_iFP'], contA_wid_isExpand)

        # コンテナー群 のみに特化したループ処理 # self.iniFileParam_contWid [0]番目 から開始
        for count, gpIndex_contWid in enumerate(self.containers, 0):
            # print(count, gpIndex_contWid)
            # print(gpIndex_contWid)
            gpIndex_contWid_isExpand, _ = gpIndex_contWid.contentHeader.getStatus_contentWidget()
            # print(list(self.od.items())[count])
            # # print(list(self.od.items())[count][0])
            # # print(list(self.od.values())[count])
            # print(gpIndex_contWid_isExpand)
            # print(type(gpIndex_contWid_isExpand))
            self._settings.setValue(list(self.od.values())[count]
                                    , gpIndex_contWid_isExpand
                                    )

        print(f'\tSave a .INI file, at \n\t\t{self.filename}')

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
        model_ = RigGenTlGp_Modl()
        view_ = RigGenTlGp_View(model_)
        RigGenTlGp_Ctlr(view_, model_)
        # self.clearAllValue_toAllWidget(central_wid_) の代替え案 ########## end

        # self.saveSettings()  # UI設定の保存用 関数 実行

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

        # tabウィジェット の情報を 復元
        tab_wid_selection = self._settings.value(self.iniFileParam['tab_wid_selection_iFP'])
        if tab_wid_selection is not None:
            self.tab_wid_.setCurrentIndex(int(tab_wid_selection))

        # # ウィジェット(コンテナA用) の情報を 復元
        # contA_wid_isExpand: str = self._settings.value(self.iniFileParam['contA_wid_expStat_iFP'])  # iniFile から isChecked を ゲット
        # if contA_wid_isExpand is True:
        #     self.contA_wid.expand()
        # else:
        #     self.contA_wid.collapse()

        # コンテナー群 のみに特化したループ処理 # self.iniFileParam_contWid [0]番目から開始
        for count, gpIndex_contWid in enumerate(self.containers, 0):
            # ウィジェット(コンテナ用) の情報を 復元
            gpIndex_contWid_isExpand: str = self._settings.value(list(self.od.values())[count])  # iniFile から isChecked を ゲット
            # print(gpIndex_contWid_isExpand)
            # print(type(gpIndex_contWid_isExpand))
            if gpIndex_contWid_isExpand is True:
                gpIndex_contWid.expand()
            else:
                gpIndex_contWid.collapse()

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

    def toggle_checkBox(self
                        , caseIndex_: str, cBxWid_: QCheckBox
                        , longName_: str, state: int
                        ):
        """

        :param str caseIndex_: 参照となる印
        :param QCheckBox cBxWid_: QCheckBox widget 名
        :param str longName_: アトリビュート ロング名
        :param int state: QCheckBox widget の check の状態を
            int:
                onClick: result 2 / offClick: result 0
                    で表す
        """
        # print(caseIndex_)
        # print(cBxWid_)
        # print(longName_)
        # print(state)

        # Joint: channel box 表示 用
        isJoint = True if caseIndex_[-1] == 'j' else False
        if isJoint:
            self.controller.ui_checkBox_j(f'v: cBx_j'
                                          , caseIndex_, cBxWid_
                                          , longName_, state
                                          )
        # Node: channel box 表示 用
        isNode = True if caseIndex_[-1] == 'n' else False
        if isNode:
            self.controller.ui_checkBox_n(f'v: cBx_n'
                                          , caseIndex_, cBxWid_
                                          , longName_, state
                                          )
        # Joint: current view 表示 用
        isJointV = True if caseIndex_.endswith('jv') else False
        if isJointV:
            self.controller.ui_checkBox_jv(f'v: cBx_jv'
                                           , caseIndex_, cBxWid_
                                           , longName_, state
                                           )

        # 追加1
        # Node: current view 表示 用
        isNodeV = True if caseIndex_.endswith('nv') else False
        if isNodeV:
            self.controller.ui_checkBox_nv(f'v: cBx_nv'
                                           , caseIndex_, cBxWid_
                                           , longName_, state
                                           )

        # Mesh: current view 表示 用
        isMeshV = True if caseIndex_.endswith('mv') else False
        if isMeshV:
            self.controller.ui_checkBox_mv(f'v: cBx_mv'
                                           , caseIndex_, cBxWid_
                                           , longName_, state
                                           )
        # Curve: channel box 表示 用
        isCurve = True if caseIndex_[-1] == 'c' else False
        if isCurve:
            self.controller.ui_checkBox_c(f'v: cBx_c'
                                          , caseIndex_, cBxWid_
                                          , longName_, state
                                          )

    # Joint: channel box 表示 用
    def currentState_checkBox_j(self
                                , currentState_: str , cBxWid_: QCheckBox
                                ):
        u""" < Joint: channel box 表示 用 >

        :param str currentState_: 'show' | 'hide' | None
        :param QCheckBox cBxWid_: QCheckBox widget 名
        """
        # message(f'v: cBx_j')
        # print(currentState, cBxWid_name)
        if not currentState_:
            cBxWid_.setText('???')
            # message_warning(u'選択したノードの中で、joint で無いオブジェクトが'
            #                 u'含まれている様です！！ joint にのみ 実行は一応行っております。'
            #                 u'ご確認ください。')
        else:
            cBxWid_.setText(currentState_)
            if currentState_ == 'hide':
                cBxWid_.setStyleSheet(self.bgcRed)
            else:
                cBxWid_.setStyleSheet(self.bgcGreen)

    # Node: channel box 表示 用
    def currentState_checkBox_n(self
                                , currentState_: str , cBxWid_: QCheckBox
                                ):
        u""" < Node: channel box 表示 用 >

        :param str currentState_: 'show' | 'hide' | None
        :param QCheckBox cBxWid_: QCheckBox widget 名
        """
        # message(f'v: cBx_n')
        # print(currentState, cBxWid_name)
        if not currentState_:
            cBxWid_.setText('???')
            # message_warning(u'選択したノードの中で、node で無いオブジェクトが'
            #                 u'含まれている様です！！ node にのみ 実行は一応行っております。'
            #                 u'ご確認ください。')
        else:
            cBxWid_.setText(currentState_)
            if currentState_ == 'hide':
                cBxWid_.setStyleSheet(self.bgcRed)
            else:
                cBxWid_.setStyleSheet(self.bgcGreen)

    # Joint: current view 表示 用
    def currentState_checkBox_jv(self
                                 , currentState_: str , cBxWid_: QCheckBox
                                 ):
        u""" < Joint: current view 表示 用 >

        :param str currentState_: 'show' | 'hide' | None
        :param QCheckBox cBxWid_: QCheckBox widget 名
        """
        # message(f'v: cBx_jv')
        # print(currentState, cBxWid_name)
        if not currentState_:
            cBxWid_.setText('???')
            # message_warning(u'選択したノードの中で、joint で無いオブジェクトが'
            #                 u'含まれている様です！！ joint にのみ 実行は一応行っております。'
            #                 u'ご確認ください。')
        else:
            cBxWid_.setText(currentState_)
            if currentState_ == 'hide':
                cBxWid_.setStyleSheet(self.bgcRed)
            else:
                cBxWid_.setStyleSheet(self.bgcGreen)

    # 追加1
    # Node: current view 表示 用
    def currentState_checkBox_nv(self
                                 , currentState_: str , cBxWid_: QCheckBox
                                 ):
        u""" < Node: current view 表示 用 >

        :param str currentState_: 'normal' | 'reference' | None
        :param QCheckBox cBxWid_: QCheckBox widget 名
        """
        # message(f'v: cBx_jv')
        # print(currentState, cBxWid_name)
        if not currentState_:
            cBxWid_.setText('???')
            # message_warning(u'選択したノードの中で、joint で無いオブジェクトが'
            #                 u'含まれている様です！！ joint にのみ 実行は一応行っております。'
            #                 u'ご確認ください。')
        else:
            cBxWid_.setText(currentState_)
            if currentState_ == 'reference':
                cBxWid_.setStyleSheet(self.bgcRed)
            else:
                cBxWid_.setStyleSheet(self.bgcGreen)

    # Mesh: current view 表示 用
    def currentState_checkBox_mv(self
                                 , currentState_: str , cBxWid_: QCheckBox
                                 ):
        u""" < Mesh: current view 表示 用 >

        :param str currentState_: 'on' | 'off' | None
        :param QCheckBox cBxWid_: QCheckBox widget 名
        """
        # message(f'v: cBx_mv')
        # print(currentState, cBxWid_name)
        if not currentState_:
            cBxWid_.setText('???')
            # message_warning(u'選択したノードの中で、mesh で無いオブジェクトが'
            #                 u'含まれている様です！！ mesh にのみ 実行は一応行っております。'
            #                 u'ご確認ください。')
        else:
            cBxWid_.setText(currentState_)
            if currentState_ == 'off':
                cBxWid_.setStyleSheet(self.bgcRed)
            else:
                cBxWid_.setStyleSheet(self.bgcGreen)

    # Curve: channel box 表示 用
    def currentState_checkBox_c(self
                                , currentState_: str , cBxWid_: QCheckBox
                                ):
        u""" < Curve: channel box 表示 用 >

        :param str currentState_: 'show' | 'hide' | None
        :param QCheckBox cBxWid_: QCheckBox widget 名
        """
        # message(f'v: cBx_c')
        # print(currentState, cBxWid_name)
        if not currentState_:
            cBxWid_.setText('???')
            # message_warning(u'選択したノードの中で、curve で無いオブジェクトが'
            #                 u'含まれている様です！！ curve にのみ 実行は一応行っております。'
            #                 u'ご確認ください。')
        else:
            cBxWid_.setText(currentState_)
            if currentState_ == 'hide':
                cBxWid_.setStyleSheet(self.bgcRed)
            else:
                cBxWid_.setStyleSheet(self.bgcGreen)

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
