# -*- coding: utf-8 -*-

u"""
YO_createSpaceNode3_View.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -4.0-
:Date: 2024/05/15

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PyMel version: 1.2.0
    - PySide2 version: 5.15.2

-リマインダ-
    done: 2024/05/13~2024/05/15
        - 変更6 と 追加6
            - 概要: maya default の Script Editor へのログ出力 を、
                YO_logProcess.action('ERROR'...)
                YO_logProcess.action('WARNING'...)
                    で行っていた箇所を、
                カスタムの Script Editor2 (PySide2作成UI) で置き換え
                    における、エラーの影響を回避
            - 詳細: カスタムの Script Editor2 (PySide2作成UI) で置き換える為には、
                実際には、
                    from ..TemplateForPySide2.CustomScriptEditor2SPIModule import custom_scriptEditor2_instance
                    モジュールを必要としますが、
                        当モジュール自体が、
                            親クラスである、
                                from ..renameTool.YO_renameTool5_View import RT_View
                            を既に import 済であり、
                        その YO_renameTool5_View モジュールに、
                            custom_scriptEditor2_instance
                        は、既に含まれています
                よって、以下のとおり、
                    改めて、新規に、
                        あらかじめ カスタムの Script Editor2 モジュール
                            を定義したり、読み込む必要は無く、
                    コメントアウトしております

                忘備禄用途です

                以下コメントアウト化しているので、実際には使用していませんが、
                    クラス継承している為、しっかりと、使用されています
                クラス継承基は、YO_renameTool5_View(RT_View) です
                つまり、YO_renameTool5_View(RT_View) から再利用しているため、
                    ここでは不必要なだけであり。
                        実際には、YO_renameTool5_View(RT_View) から読み込まれており、
                            しっかりと、使用されています。
                ::

                    +   def __init__(self, _model):
                            ...
                            # 追加6 ########################################################### start
                            # クラス継承元 YO_renameTool5_View(RT_View) のメソッドを 再利用しているので、ここでは不必要 です
                            # self.scriptEditor2_chunk1()
                            # クラス継承元 YO_renameTool5_View(RT_View) のメソッドを 再利用しているので、ここでは不必要 です
                            # self.scriptEditor2_chunk2()
                            # 追加6 ########################################################### end

                    +   # 追加6 ########################################################### start
                        # クラス継承元 YO_renameTool5_View(RT_View) のメソッドを 再利用しているので、ここでは不必要 です
                        # def scriptEditor2_chunk1(self):
                        #     pass

                        # クラス継承元 YO_renameTool5_View(RT_View) のメソッドを 再利用しているので、ここでは不必要 です
                        # def scriptEditor2_chunk2(self):
                        #     pass

                        # クラス継承元 YO_renameTool5_View(RT_View) のメソッドを 再利用しているので、ここでは不必要 です
                        # def create_scriptEditor2_and_show(self):
                        #     pass

                        # クラス継承元 YO_renameTool5_View(RT_View) のメソッドを 再利用しているので、ここでは不必要 です
                        # @Slot()
                        # def on_scriptEditor2_closed(self):
                        #     pass
                        # 追加6 ########################################################### end

                    +   # 追加6 ########################################################### start
                        # クラス継承元 YO_renameTool5_View(RT_View) のメソッドを 再利用しているので、ここでは不必要 です
                        # Close 実行 関数
                        # def editMenuCloseCmd(self, *args):
                        #     pass
                        # 追加6 ########################################################### end
        version = '-4.0-'

    done: 2023/12/21
        - 変換箇所5
            - 概要: 絶対パス から 相対パス へ記述変更
            - 詳細:
                ::

                  -     from YO_utilityTools.createSpaceNode.[...] import ...
                  +     from .[...] import ...

                  -     from YO_utilityTools.lib.[...] import ...
                  +     from ..lib.[...] import ...

                  -     from YO_utilityTools.renameTool.YO_renameTool5_View import RT_View
                  +     from ..renameTool.YO_renameTool5_View import RT_View

        version = '-3.1-'

    done: 2023//10/25
        汎用箇所を、モジュールとして読み込みに変更

        version = '-3.0-'

    done: 2023/04/17~2023/05/08
        新規

        version = '-1.0-'
"""

# 標準ライブラリ #################################################################
# from functools import partial  # partial 利用時は、最後の引数に、*args 要時あり

# サードパーティライブラリ #########################################################
import maya.cmds as cmds
# import maya.OpenMaya as om
from pymel import core as pm
from pymel.core import uitypes as ui

# ローカルで作成したモジュール ######################################################
import YO_utilityTools.createSpaceNode.config as docstring
# basic_configuration_for_derivation(派生用の基本構成)
from .config import SPACE, TITLE, VERSION
# 汎用ライブラリー の使用 ################################################################ start
from ..lib.message import message
# from ..lib.message_warning import message_warning
# 汎用ライブラリー の使用 ################################################################## end
# from ..TemplateForPySide2.CustomScriptEditor2SPIModule import custom_scriptEditor2_instance

# mvc_model_module_that_become_derived_basis(派生基となるMVCモデルモジュール)
from ..renameTool.YO_renameTool5_View import RT_View


class CSpaceNode_View(RT_View):
    u""" < GUIウィンドウを作成するための Viewクラス です >

    ::

      UIを作成するためのメソッドや、UIの更新を行うためのメソッドを実装します。

      GUIウィンドウを作成するための PyMel コードが含まれます。
        Viewクラスのコンストラクターは、Modelオブジェクト への参照を受け取ります。
            View クラスは GUIウィンドウ を作成し、そのウィンドウ内の要素を更新するためのメソッドを提供します。

    ######

        基本となる要素は以下の 6つ
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
    def __init__(self, _model):
        super(CSpaceNode_View, self).__init__(_model)
        self.model = _model

        self.title = TITLE
        self.space = SPACE
        self.version = VERSION

        self.win = TITLE + '_ui'

        self.size = (316, 312)

        self.infoSummary = (u'独自の space 作成用リネームツールツール\n'
                            u'の バージョン3(PyMel版) です。'
                            )
        self.infoDetail = (u'親 space を作りたいノードを選択し実行しますする事で、\n'
                           u'選択ノードの階層の一つ上階層の'
                           u'親に 親 space が、命名規則に則って1つ作成されます。\n'
                           u'親 space には、locator， null， joint の何れかで作成'
                           u'されるよう設計されています。\n'
                           u'独自規格の命名規則については、\n'
                           u'\trenameTool package の help をご覧ください。'
                           )
        self.disableTemporaryFunctionInfo = (u'独自規格の命名規則に基づくため、\n'
                                             u'\t第1単語 + 第2単語 + 第3単語 の入力エリア'
                                             u'は、\n'
                                             u'\t\t現在はユーザーによる入力は不可で'
                                             u'構成しています。'
                                             )

        self.bgcBlue2 = [0.0, 0.7, 1.0]  # list of float
        self.bgcBlue = [0.5, 0.5, 0.9]  # list of float

        # 追加6 ########################################################### start
        # クラス継承元 YO_renameTool5_View(RT_View) のメソッドを 再利用しているので、ここでは不必要 です
        # self.scriptEditor2_chunk1()
        # クラス継承元 YO_renameTool5_View(RT_View) のメソッドを 再利用しているので、ここでは不必要 です
        # self.scriptEditor2_chunk2()
        # 追加6 ########################################################### end

    # 追加6 ########################################################### start
    # クラス継承元 YO_renameTool5_View(RT_View) のメソッドを 再利用しているので、ここでは不必要 です
    # def scriptEditor2_chunk1(self):
    #     pass

    # クラス継承元 YO_renameTool5_View(RT_View) のメソッドを 再利用しているので、ここでは不必要 です
    # def scriptEditor2_chunk2(self):
    #     pass

    # クラス継承元 YO_renameTool5_View(RT_View) のメソッドを 再利用しているので、ここでは不必要 です
    # def create_scriptEditor2_and_show(self):
    #     pass

    # クラス継承元 YO_renameTool5_View(RT_View) のメソッドを 再利用しているので、ここでは不必要 です
    # @Slot()
    # def on_scriptEditor2_closed(self):
    #     pass
    # 追加6 ########################################################### end

    def create(self):
        # UI-0. 重複しないウインドウ
        try:
            pm.deleteUI(self.win, window = True)
        except:
            pass

        self.controller = self.model.controller  # 和えて明示しています。無くてもこのケースでは実行可。

        with pm.window(self.win
                , title = self.title[3:] + self.space + self.version
                , widthHeight = self.size
                , menuBar = True
                , sizeable = True
                , maximizeButton = False, minimizeButton = False
                       ):
            # UI-1. メニュー
            self.commonMenu()  # 最上段の UI common menu の作成  # base からの継承で再利用...

            # UI-2. メインLayout + 情報 + 追加オプション
            with ui.AutoLayout(ratios = [4, 1]):  # before: [3.5, 1]
                with pm.tabLayout(scrollable = True  # 境界線のちらつき防止
                        , tabsVisible = False, h = 1
                        , childResizable = True
                                  ):  # tab 追加を可能とする時は、tabsVisible = True
                    with pm.columnLayout(adj = True):
                        # UI-2. 情報
                        self.commonInformation()  # base からの継承 override 変更 (独自に定義しなおして上書き)

                        pm.separator(height = 10, style = 'out')

                        # UI-2. 追加オプションのまとまり
                        self.displayOptions()  # base からの継承 override 変更 (独自に定義しなおして上書き)

                # UI-3. ボタンLayout + 底面ボタン3つ
                with ui.AutoLayout(orientation = "horizontal"
                        , spacing = 3
                                   ) as commonBtns_layout:
                    # UI-3. 底面ボタン3つ
                    self.commonButtons()  # base からの継承で再利用...
                    commonBtns_layout.redistribute(2, 1, 1)  # ボタン幅比率の矯正補正

        # # UI-4. optionVar による値の復元
        restoreOptionVar = 'Restore Option Variables'
        # self.restoreOptionVarCmd(restoreOptionVar)
        self.controller.restoreOptionVar(restoreOptionVar)
        # # partial(self.restoreOptionVarCmd, restoreOptionVar)

        cmds.evalDeferred(lambda *args: pm.showWindow(self.win))

    # UIディテール 作成 ################################################################ start
    # base からの継承で再利用...
    # UI-1. commonメニュー
    # def commonMenu(self):
    #     pass

    # base からの継承で再利用...
    # UI-3. common底面ボタン3つ
    # def commonButtons(self):
    #     pass

    # base からの継承 override 変更 (独自に定義しなおして上書き)
    # UI-2. common情報
    def commonInformation(self):
        u""" < UI-2. common情報 の作成 >

        ::

          base から継承 override 変更 (独自に定義しなおして上書き)
        """
        pm.text(l = self.infoSummary)
        pm.text(l = u'note:'
                , annotation = (self.infoDetail
                                +
                                '\n'
                                +
                                self.disableTemporaryFunctionInfo
                                )
                , bgc = self.bgcBlue
                )

    # base から継承 override 変更 (独自に定義しなおして上書き)
    # UI-2. 追加オプションのまとまり
    def displayOptions(self):
        u""" < UI-2. 追加オプションのまとまり の作成 >

        ::

          base から継承 override 変更 (独自に定義しなおして上書き)
        """
        # base から継承 override 変更 (独自に定義しなおして上書き)
        self.displayOptions_mode()  # UI-21. mode オプション の作成
        # base から継承 override 変更 (独自に定義しなおして上書き)
        self.displayOptions_textField()  # UI-22. TextField オプション の作成

        # 完全に新規
        self.nodeType()

    # base から継承 override 変更 (独自に定義しなおして上書き)
    # UI-2. 追加オプション
    # UI-21. mode オプション の作成
    def displayOptions_mode(self):
        u""" < UI-2. 追加オプション  UI-21. mode オプション の作成 >

        ::

          base から継承 override 変更 (独自に定義しなおして上書き)
        """
        with pm.rowColumnLayout(numberOfRows = 1
                , columnSpacing = (1, 10)
                                ) as dispOpt_mode_layout:
            pm.text(l = 'rename mode  ')
            # radioCollection #######################################
            # type: pm.radioCollection
            self.model.cmnModeRdBtnClcton = pm.radioCollection()

            # 初期状態を固定（このツール用に状態を編集し固定）
            pm.radioButton(self.model.mode_handleNameLists[0]
                           , en = False
                , select = False
                , label = u'強制的'
                           )
            pm.radioButton(self.model.mode_handleNameLists[1]
                           , en = False
                , select = True
                , label = u'構成要素をキープ'
                           )
            # dispOpt_mode_layout.redistribute(1.2, 1, 6)  # ボタン幅比率の矯正補正

    # base から継承 override 変更 (独自に定義しなおして上書き)
    # UI-2. 追加オプション
    # UI-22. TextField オプション の作成
    def displayOptions_textField(self):
        u""" < UI-2. 追加オプション  UI-22. TextField オプション の作成 >

        ::

          base から継承 override 変更 (独自に定義しなおして上書き)
        """
        with pm.horizontalLayout() as dispOpt_txtFld_layout:
            ######################################################
            # cmnLyutA ###########################################
            with pm.columnLayout(
                    adj = True
                    # , w = 33
            ) as self.cmnLyutA:
                # textField A1 #######################################
                # type: pm.textField
                self.model.cmnTxtFld_A1 = pm.textField(
                    height = 26
                    # , w = 50
                    , tx = u'~'
                    , bgc = self.model.textFieldBgc_A1
                    , editable = False
                )
                # textField A1 の popUp A1  #############
                # self.model.cmnPUpMnu_A1 = pm.popupMenu(b = 3)

            ######################################################
            # cmnLyutB ###########################################
            with pm.columnLayout(
                    adj = True
                    # , w = 33
            ) as self.cmnLyutB:
                # textField B1 #######################################
                # type: pm.textField
                self.model.cmnTxtFld_B1 = pm.textField(
                    height = 26
                    # , w = 50
                    , tx = u'~[Space]'
                    , bgc = self.model.textFieldBgc_B1
                    , editable = False
                    , font = self.model.tempFont
                )
                # textField B1 の popUp B1  #############
                # self.model.cmnPUpMnu_B1 = pm.popupMenu(b = 3)

            ######################################################
            # cmnLyutC ###########################################
            with pm.rowLayout(numberOfColumns = 4
                              # , w = 33
                    , ad4 = 4  # 前回は、 ad4 = 2
                              ) as self.cmnLyutC:
                # textField C1 #######################################
                # type: pm.textField
                self.model.cmnTxtFld_C1 = pm.textField(
                    ed = False
                    , height = 26
                    , w = 27
                    , tx = u'~'
                    , bgc = self.model.textFieldBgc_C
                )
                # textField C1 の popUp C1  ##############
                # self.model.cmnPUpMnu_C1 = pm.popupMenu(b = 3)

                # textField C2 #######################################
                # type: pm.textField
                self.model.cmnTxtFld_C2 = pm.textField(
                    ed = False
                    , height = 26
                    , w = 35  # 前回は w = 27
                    , bgc = self.model.textFieldBgc_C
                )
                # textField C2 の popUp C2  ##############
                self.model.cmnPUpMnu_C2 = pm.popupMenu(b = 3)

                # textField C3 #######################################
                # type: pm.textField
                self.model.cmnTxtFld_C3 = pm.textField(
                    ed = False
                    , height = 26
                    , w = 27  # 前回は、 w = 20
                    , bgc = self.model.textFieldBgc_C
                )
                # textField C3 の popUp C3  ##############
                self.model.cmnPUpMnu_C3 = pm.popupMenu(b = 3)

                # button D ####################################################################
                self.model.cmnBtnD = pm.button(height = 26, w = 20, l = u'>>', en = False)
                # button D の popUp D  ##############
                self.model.cmnPUpMnu_D = pm.popupMenu(b = 3)
                pm.menuItem(label = u'##### '
                                    u'sample string set (サンプル文字列セット)'
                                    u' #####'
                            )
                pm.menuItem(divider = True)
                # self.cmnLyutC.columnWidth(1, 1, 1, 2)
            # dispOpt_txtFld_layout.redistribute(1, 1, 1)  # ボタン幅比率の矯正補正

    # 完全に新規
    # 2. UI 追加オプション
    # 23. nodeTypeを選択するUI の作成
    def nodeType(self):
        u""" <2. 追加オプション  23. nodeTypeを選択UI の作成 です >

        ::

          完全に新規
        """
        ################################################
        # node type 選択ボタン フィールド まとまり # cCmnLayout_nodeType
        ################################################
        # cCmnLayout_nodeType..start
        with pm.columnLayout(
                # bgc = self.bgcGra
        ) as cCmnLayout_nodeType:
            # pm.checkBox #######################################
            self.model.cOpMnu_nodeType = pm.optionMenu(
                label = 'node type', w = 150
                , bgc = self.model.bgcGray
                , enableBackground = False
            )
            pm.menuItem('cMuItm_loc', l = 'locator')
            pm.menuItem('cMuItm_nul', l = 'null')
            pm.menuItem('cMuItm_jot', l = 'joint')
    # UIディテール 作成 ################################################################## end

    # 1. UI-1. メニュー コマンド群 ###################################################### start
    # Save Settings 実行による optionVar の保存 関数
    # Model へ移動...

    # base からの継承で再利用...
    # Reload 実行 関数
    # def editMenuReloadCmd(self, *args):
    #     pass

    # base から継承で、同じ内容だが新規扱い(override)
    # Help 実行 関数
    def helpMenuCmd(self, *args):
        u""" < Help 実行 関数 です > """
        # cmds.launch(web = 'http://help.autodesk.com/cloudhelp/2016/'
        #                   'JPN/Maya-Tech-Docs/CommandsPython/index.html'
        #             )
        help(docstring)
        message('For more information, see Script Editor')

    # 追加6 ########################################################### start
    # クラス継承元 YO_renameTool5_View(RT_View) のメソッドを 再利用しているので、ここでは不必要 です
    # Close 実行 関数
    # def editMenuCloseCmd(self, *args):
    #     pass
    # 追加6 ########################################################### end
    # 1. UI-1. メニュー コマンド群 ######################################################## end

if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
