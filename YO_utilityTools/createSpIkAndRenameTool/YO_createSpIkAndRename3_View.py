# -*- coding: utf-8 -*-

u"""
YO_createSpIkAndRename3_View.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -3.1-
:Date: 2023//12/22

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PyMel version: 1.2.0

-リマインダ-
    done: 2023/12/22
        - 変換箇所5
            - 概要: 絶対パス から 相対パス へ記述変更
            - 詳細:
                ::

                  -     from YO_utilityTools.createSpIkAndRenameTool.[...] import ...
                  +     from .[...] import ...

                  -     from YO_utilityTools.lib.[...] import ...
                  +     from ..lib.[...] import ...

                  -     from YO_utilityTools.renameTool.YO_renameTool5_View import RT_View
                  +     from ..renameTool.YO_renameTool5_View import RT_View

        version = '-3.1-'

    done: 2023//10/25
        汎用箇所を、モジュールとして読み込みに変更

        version = '-3.0-'

    done: 2023/04/12~2023/04/13
        新規

        version = '-1.0-'
"""
# 標準ライブラリ
from functools import partial  # partial 利用時は、最後の引数に、*args 要時あり

# サードパーティライブラリ
import maya.cmds as cmds
import maya.OpenMaya as om
from pymel import core as pm
from pymel.core import uitypes as ui

# ローカルで作成したモジュール
import YO_utilityTools.createSpIkAndRenameTool.config as docstring
# basic_configuration_for_derivation(派生用の基本構成)
from .config import SPACE, TITLE, VERSION

# 汎用ライブラリー の使用 ################################################################ start
from ..lib.message import message
# 汎用ライブラリー の使用 ################################################################## end

# mvc_model_module_that_become_derived_basis(派生基となるMVCモデルモジュール)
from ..renameTool.YO_renameTool5_View import RT_View


class CSpIkAndRT_View(RT_View):
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
        super(CSpIkAndRT_View, self).__init__(_model)
        self.model = _model

        self.title = TITLE
        self.space = SPACE
        self.version = VERSION

        self.win = TITLE + '_ui'

        self.size = (316, 312)

        self.infoSummary = (u'既定の命名規則に基づいた Spline IK Handle と Curve を作成するツール\n'
                            u'の バージョン3(PyMel版) です。'
                            )
        self.infoDetail = (u'現状の命名規則に基づいた、'
                           u'Spline IK Handle ・ Curve 共に同時作成し、'
                           u'ネーミングの統一も行います。\n'
                           u'独自規格の命名規則については、\n'
                           u'\trenameTool package の help をご覧ください。'
                           )

        self.bgcBlue2 = [0.0, 0.7, 1.0]  # list of float
        self.bgcBlue = [0.5, 0.5, 0.9]  # list of float

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
            with ui.AutoLayout(ratios = [16, 1]):  # before: [3.5, 1]
                with pm.tabLayout(scrollable = True  # 境界線のちらつき防止
                        , tabsVisible = False, h = 1
                        , childResizable = True
                                  ):  # tab 追加を可能とする時は、tabsVisible = True
                    with pm.columnLayout(adj = True):
                        # UI-2. 情報
                        self.commonInformation()  # base からの継承で再利用...

                        pm.separator(height = 10, style = 'out')

                        # UI-2. 追加オプションのまとまり
                        self.displayOptions()  # base から継承 override 変更 (独自に定義しなおして上書き)

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

    # base からの継承で再利用...
    # UI-2. common情報
    # def commonInformation(self):
    #     pass

    # base から継承 override 変更 (独自に定義しなおして上書き)
    # UI-2. 追加オプションのまとまり
    def displayOptions(self):
        u""" < UI-2. 追加オプションのまとまり の作成>

        ::

          base から継承 override 変更 (独自に定義しなおして上書き)
        """
        # 完全に新規
        self.setJointField()  # UI-20. start joint, end joint setting オプション の作成

        # base から継承で再利用
        self.displayOptions_mode()  # UI-21. mode オプション の作成
        # base から継承 override 変更 (独自に定義しなおして上書き)
        self.displayOptions_textField()  # UI-22. TextField オプション の作成

        # 完全に新規
        self.automaticNumbering()  # UI-23.  自動でナンバリングするための識別子
        # 完全に新規
        self.iKSplineHandleSetting()  # UI-24. IK Spline Handle Setting
        # cmds.separator(height = 10, style = 'in')
        # 完全に新規
        self.finalNaming()  # UI-25. 名前をcheck

    # 完全に新規
    # UI-2. UI 追加オプション
    # UI-20. start joint, end joint setting オプション の作成
    def setJointField(self):
        u""" < UI-20. start joint, end joint setting オプション の作成 >

        ::

          新規
        """
        with pm.columnLayout(adjustableColumn = True):
            #####################
            # start joint
            with pm.rowLayout(
                    numberOfColumns = 5
                    # , bgc = self.bgcBlue2
                    , adjustableColumn = 2
            ):
                common_text_staJt = u'Spline IK の start joint となるジョイントを登録します'
                pm.text(l = 'start joint'
                            +
                            ' '
                            +
                            ':'
                            + '  ' * 2
                        , annotation = common_text_staJt
                        )
                self.model.setJtFld_staJt_txtFld = pm.textField(tx = '...', annotation = common_text_staJt)
                self.model.setJtFld_staJt_setBtn = pm.button(
                    w = 20
                    , label = 'Set'
                    , ann = u'Set ボタンです'
                    , c = partial(self.model.setJtFld_staJt_btnCmd, 'set')
                    , enable = True
                )
                self.model.setJtFld_staJt_selBtn = pm.button(
                    w = 20
                    , label = 'sel'
                    , ann = u'選択 ボタンです'
                    , c = partial(self.model.setJtFld_staJt_btnCmd, 'sel')
                    , enable = False
                )
                self.model.setJtFld_staJt_clrBtn = pm.button(
                    w = 20
                    , label = 'C'
                    , ann = u'登録解除 ボタンです'
                    , c = partial(self.model.setJtFld_staJt_btnCmd, 'clr')
                    , enable = False
                )

            #####################
            # end joint
            with pm.rowLayout(
                    numberOfColumns = 5
                    # , bgc = self.bgcBlue2
                    , adjustableColumn = 2
            ):
                common_text_endJt = u'Spline IK の end joint となるジョイントを登録します'
                pm.text(l = 'end joint'
                            +
                            ' ' * 2
                            +
                            ':'
                            +
                            '  ' * 2
                        , annotation = common_text_endJt
                        )
                self.model.setJtFld_endJt_txtFld = pm.textField(tx = '...', annotation = common_text_endJt)
                self.model.setJtFld_endJt_setBtn = pm.button(
                    w = 20
                    , label = 'Set'
                    , ann = u'Set ボタンです'
                    , c = partial(self.model.setJtFld_endJt_btnCmd, 'set')
                    , enable = True
                )
                self.model.setJtFld_endJt_selBtn = pm.button(
                    w = 20, label = 'sel'
                    , ann = u'選択 ボタンです'
                    , c = partial(self.model.setJtFld_endJt_btnCmd, 'sel')
                    , enable = False
                )
                self.model.setJtFld_endJt_clrBtn = pm.button(
                    w = 20, label = 'C'
                    , ann = u'登録解除 ボタンです'
                    , c = partial(self.model.setJtFld_endJt_btnCmd, 'clr')
                    , enable = False
                )

    # UI-2. 追加オプション
    # UI-21. mode オプション の作成
    # def displayOptions_mode(self):
    #     pass

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
                    insertionPosition = 0
                    , height = 26
                    # , w = 50
                    , tx = self.model.currentTxt_A1
                    , bgc = self.model.textFieldBgc_A1
                    , ann = u'第1単語:主に一般的な命名入力領域です。\n'
                            u'右ボタンで補足できます。\n'
                            u'補足: @,~ 識別子は'
                            u'このフィールド内では'
                            u'規定文字として入力を許可しています。'
                    , cc = partial(self.model.limitedTypingInputCmd, u'cmnTxtFld_A1')
                    , pht = 'sample', font = self.model.tempFont
                )
                # textField A1 の popUp A1  #############
                self.model.cmnPUpMnu_A1 = pm.popupMenu(b = 3)
                # 許可している文字列
                pm.menuItem(label = u'##### '
                                    u'Allowed strings (許可している文字列)'
                                    u' #####'
                            , divider = True
                            )
                pm.menuItem(label = u'at sign --> @'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆ナンバリング用識別子を追加◆◆'
                            , c = partial(self.model.textFieldPupMnuCmd, u'cmnPUpMnu_A1', u'@')
                            , ann = u'ナンバリング用識別子を追加します。'
                            , enable = False  # original 流用から変更
                            )
                pm.menuItem(label = u'tilde --> ~'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆そのままの文字列を利用◆◆'
                            , c = partial(self.model.textFieldPupMnuCmd, u'cmnPUpMnu_A1', u'~')
                            , ann = u'そのままの文字列を利用します。'
                            , enable = False  # original 流用から変更
                            )
                # クリアー用文字列
                pm.menuItem(label = u'##### '
                                    u'strings clear (クリアー用文字列)'
                                    u' #####'
                            , divider = True
                            )
                pm.menuItem(label = u'blank -- > '
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆文字列をクリアー◆◆'
                            , c = partial(self.model.textFieldPupMnuCmd, u'cmnPUpMnu_A1', u'')
                            , ann = u'文字列をクリアーします。'
                            )
                # プリセット
                pm.menuItem(label = u'##### '
                                    u'preset (プリセット)'
                                    u' #####'
                            , divider = True
                            )
                pm.menuItem(label = u'SpIk'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆spline IK curve cv 其々への、'
                                    u'spline IK 用クラスターとしての命名を付加◆◆'
                            , c = partial(self.model.textFieldPupMnuCmd, u'cmnPUpMnu_A1', u'SpIk')
                            , ann = u'プリセット名'
                            , enable = True  # original 流用から変更
                            )
            # self.cmnLyutA .. end

            ######################################################
            # cmnLyutB ###########################################
            with pm.columnLayout(
                    adj = True
                    # , w = 33
            ) as self.cmnLyutB:
                # textField B1 #######################################
                # type: pm.textField
                self.model.cmnTxtFld_B1 = pm.textField(
                    insertionPosition = 0
                    , editable = False
                    , height = 26
                    # , w = 50
                    , tx = self.model.currentTxt_B1
                    , bgc = self.model.textFieldBgc_B1
                    , insertText = 'spIKHndle'
                    , ann = u'第2単語:主に役割等を表す入力領域です。\n'
                            u'右ボタンで補足できます。\n'
                            u'e.g.): "spIK"`\n'
                            u'補足:@ 識別子は'
                            u'このフィールド内では'
                            u'規定文字として入力を許可しています。'
                    , cc = partial(self.model.limitedTypingInputCmd, u'cmnTxtFld_B1')
                )
                # textField B1 の popUp B1  #############
                self.model.cmnPUpMnu_B1 = pm.popupMenu(b = 3)
                # 許可している文字列
                pm.menuItem(label = u'##### '
                                    u'Allowed strings (許可している文字列)'
                                    u' #####'
                            , divider = True
                            )
                pm.menuItem(label = u'square brackets --> []'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆挿入用文字列識別子を追加◆◆'
                            , c = partial(self.model.textFieldPupMnuCmd, u'cmnPUpMnu_B1', u'[Space]')
                            , ann = u'挿入用文字列識別子を追加します。 e.g.)サンプル[Space]'
                            , enable = False  # original 流用から変更
                            )
                pm.menuItem(label = u'at sign --> @'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆ナンバリング用識別子を追加◆◆'
                            , c = partial(self.model.textFieldPupMnuCmd, u'cmnPUpMnu_B1', u'@')
                            , ann = u'ナンバリング用識別子を追加します。'
                            , enable = False  # original 流用から変更
                            )
                pm.menuItem(label = u'tilde --> ~'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆そのままの文字列を利用◆◆'
                            , c = partial(self.model.textFieldPupMnuCmd, u'cmnPUpMnu_B1', u'~')
                            , ann = u'そのままの文字列を利用します。'
                            , enable = False  # original 流用から変更
                            )
                # クリアー用文字列
                pm.menuItem(label = u'##### '
                                    u'strings clear (クリアー用文字列)'
                                    u' #####'
                            , divider = True
                            )
                pm.menuItem(label = u'blank -- > '
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆文字列をクリアー◆◆'
                            , c = partial(self.model.textFieldPupMnuCmd, u'cmnPUpMnu_B1', u'')
                            , ann = u'文字をクリアーします。'
                            , enable = False  # original 流用から変更
                            )
                # プリセット
                pm.menuItem(label = u'##### '
                                    u'preset (プリセット)'
                                    u' #####'
                            , divider = True
                            )
                pm.menuItem(label = u'spIKHndle'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆spline IK Handle としての命名の付加 ver01◆◆'
                            , c = partial(self.model.textFieldPupMnuCmd, u'cmnPUpMnu_B1', u'spIKHndle')
                            , ann = u'プリセット名'
                            )
                pm.menuItem(label = u'splineIKHandle'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆spline IK Handle としての命名の付加 ver02◆◆'
                            , c = partial(self.model.textFieldPupMnuCmd, u'cmnPUpMnu_B1', u'splineIKHandle')
                            , ann = u'プリセット名'
                            )

            ######################################################
            # cmnLyutC ###########################################
            with pm.rowLayout(
                    numberOfColumns = 4
                    # , w = 33
                    , ad4 = 4  # 前回は、 ad4 = 2
            ) as self.cmnLyutC:
                # textField C1 #######################################
                # type: pm.textField
                self.model.cmnTxtFld_C1 = pm.textField(
                    insertionPosition = 0
                    , ed = False
                    , height = 26
                    , w = 27
                    , tx = self.model.currentTxt_C1
                    , bgc = self.model.textFieldBgc_C
                    , ann = u'第3単語-要素1:識別子領域です。\n'
                            u'右ボタンで補足できます。\n'
                            u'e.g.): "@"'
                )
                # textField C1 の popUp C1  ##############
                self.model.cmnPUpMnu_C1 = pm.popupMenu(b = 3)
                # 許可している文字列
                pm.menuItem(label = u'##### '
                                    u'Allowed strings (許可している文字列)'
                                    u' #####'
                            , divider = True
                            )
                pm.menuItem(label = u'at sign --> @'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆ナンバリング用識別子を利用◆◆'
                            , c = partial(self.model.textFieldPupMnuCmd, u'cmnPUpMnu_C1', u'@')
                            , ann = u'ナンバリング用識別子を利用します。'
                            , enable = False  # original 流用から変更
                            )
                pm.menuItem(label = u'tilde --> ~'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆そのままの文字列を利用◆◆'
                            , c = partial(self.model.textFieldPupMnuCmd, u'cmnPUpMnu_C1', u'~')
                            , ann = u'そのままの文字列を利用します。'
                            , enable = False  # original 流用から変更
                            )
                # クリアー用文字列
                pm.menuItem(label = u'##### '
                                    u'strings clear (クリアー用文字列)'
                                    u' #####'
                            , divider = True
                            )
                pm.menuItem(label = u'blank -- > '
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆文字列をクリアー◆◆'
                            , c = partial(self.model.textFieldPupMnuCmd, u'cmnPUpMnu_C1', u'')
                            , ann = u'文字列をクリアーします。'
                            , enable = False  # original 流用から変更
                            )

                # textField C2 #######################################
                # type: pm.textField
                self.model.cmnTxtFld_C2 = pm.textField(
                    insertionPosition = 0
                    , ed = False
                    , height = 26
                    , w = 35  # 前回は w = 27
                    , tx = self.model.currentTxt_C2
                    , bgc = self.model.textFieldBgc_C
                    , ann = u'第3単語-要素2:識別子領域です。\n'
                            u'右ボタンで補足できます。\n'
                            u'e.g.): "Gp"'
                )
                # textField C2 の popUp C2  ##############
                self.model.cmnPUpMnu_C2 = pm.popupMenu(b = 3)
                # プリセット
                pm.menuItem(label = u'##### '
                                    u'preset (プリセット)'
                                    u' #####'
                            , divider = True
                            )
                pm.menuItem(label = u'group -- > Gp'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆文字列 Gp 識別子を利用◆◆'
                            , c = partial(self.model.textFieldPupMnuCmd, u'cmnPUpMnu_C2', u'Gp')
                            , ann = u'プリセット名'
                            , enable = False  # original 流用から変更
                            )
                # クリアー用文字列
                pm.menuItem(label = u'##### '
                                    u'strings clear (クリアー用文字列)'
                                    u' #####'
                            , divider = True)
                pm.menuItem(label = u'blank -- > '
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆文字列をクリアー◆◆'
                            , c = partial(self.model.textFieldPupMnuCmd, u'cmnPUpMnu_C2', u'')
                            , ann = u'文字列をクリアーします。'
                            , enable = False  # original 流用から変更
                            )

                # textField C3 #######################################
                # type: pm.textField
                self.model.cmnTxtFld_C3 = pm.textField(
                    insertionPosition = 0
                    , ed = False
                    , height = 26
                    , w = 27  # 前回は、 w = 20
                    , tx = self.model.currentTxt_C3
                    , bgc = self.model.textFieldBgc_C
                    , ann = u'第3単語-要素3:識別子領域です。\n'
                            u'右ボタンで補足できます。\n'
                            u'e.g.): "L", "R"'
                    , pht = 'L', font = self.model.tempFont
                )
                # textField C3 の popUp C3  ##############
                self.cmnPUpMnu_C3 = pm.popupMenu(b = 3)
                # プリセット
                pm.menuItem(label = u'##### '
                                    u'preset (プリセット)'
                                    u' #####'
                            , divider = True)

                pm.menuItem(label = u'left -- > L'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆文字列 L 識別子を利用◆◆'
                            , c = partial(self.model.textFieldPupMnuCmd, u'cmnPUpMnu_C3', u'L')
                            , ann = u'プリセット名'
                            )
                pm.menuItem(label = u'right -- > R'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆文字列 R 識別子を利用◆◆'
                            , c = partial(self.model.textFieldPupMnuCmd, u'cmnPUpMnu_C3', u'R')
                            , ann = u'プリセット名'
                            )
                pm.menuItem(label = u'center -- > C'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆文字列 C 識別子を利用◆◆'
                            , c = partial(self.model.textFieldPupMnuCmd, u'cmnPUpMnu_C3', u'C')
                            , ann = u'プリセット名'
                            )
                pm.menuItem(label = u'middle -- > M'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆文字列 M 識別子を利用◆◆'
                            , c = partial(self.model.textFieldPupMnuCmd, u'cmnPUpMnu_C3', u'M')
                            , ann = u'プリセット名'
                            )
                # クリアー用文字列
                pm.menuItem(label = u'##### '
                                    u'strings clear (クリアー用文字列)'
                                    u' #####'
                            , divider = True
                            )
                pm.menuItem(label = u'blank -- > '
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆文字列をクリアー◆◆'
                            , c = partial(self.model.textFieldPupMnuCmd, u'cmnPUpMnu_C3', u'')
                            , ann = u'文字列をクリアーします。'
                            )

                # button D ####################################################################
                self.model.cmnBtnD = pm.button(height = 26, w = 20, l = u'>>', en = False)
                # button D の popUp D  ##############
                self.model.cmnPUpMnu_D = pm.popupMenu(b = 3)
                pm.menuItem(label = u'##### '
                                    u'sample string set (サンプル文字列セット)'
                                    u' #####'
                            )
                pm.menuItem(divider = True)  # self.cmnLyutC .. end

    # 完全に新規
    # UI-2. 追加オプション
    # UI-23. 自動でナンバリングするための識別子を付与するUI の作成
    def automaticNumbering(self):
        u""" < UI-2. 追加オプション  UI-23. 自動でナンバリングするための識別子を付与するUI の作成 です >

        ::

          完全に新規
        """
        # clmLyut_autoNumbering
        with pm.columnLayout(
                # bgc = self.bgcGray
        ) as self.clmLyut_autoNumbering:
            self.model.autoNumbering_ckBx = pm.checkBox(
                label = 'Use identifiers for automatic numbering'
                , value = False
                , onCommand = partial(self.model.doAutoNumbering_ckBx_tgl_command, 'on')
                , offCommand = partial(self.model.doAutoNumbering_ckBx_tgl_command, 'off')
                , annotation = u'自動でナンバリングするための識別子を使用します'
            )

    # 完全に新規
    # UI-2. UI 追加オプション
    # UI-24. IK Spline Handle Setting
    def iKSplineHandleSetting(self):
        u""" <  >

        ::

          2. 追加オプション
          23. 自動でナンバリングするための識別子を使用する関数 です

          新規
        """
        # ikHandle -solver "ikSplineSolver"
        # -roc false -parentCurve true -startJoint "spineA_spIKjt" -endEffector "spineTip_spIKjt";
        # // Result: ikHandle1 effector1 curve1 //
        # 基本、Auto parent curve(-parentCurve true)で子付けされる個所に最終的なコントローラも置いていけば良さそう

        # clmLyut_iKSpHndleSetting
        with pm.columnLayout(
                adjustableColumn = True
                # , bgc = self.bgcGray
        ) as self.clmLyut_iKSpHndleSetting:
            # separator
            pm.separator(style = 'shelf'
                         # , w = 10
                         , height = 10
                         )

            pm.text(label = 'Required parts of\n'
                            u'▼ maya default: IK SplineHandle Settings'
                    , ann = u'maya default: IK SplineHandle Settings の必要箇所'
                            u'を抜粋します'
                    )
            # ###########################################################################
            #####################
            # rootOnCurve(roc)
            self.model.ikSpHdleSetting_rootOnCurve_ckBx = pm.checkBox(
                label = 'Root on curve'  # roc(roc)  bool
                , value = False
                , annotation = u'ルートを ikSplineHandle のカーブにロックするかどうかを指定します\n'
                               u'\t'
                               u'my setting default: False\n'
                               u'\t'
                               u'maya setting default: True'
            )

            #####################
            # parentCurve(pcv)
            with pm.rowLayout(
                    numberOfColumns = 5
                    # , w = 50
                    , adjustableColumn = 2
            ) as self.clmLyut_parentCurve:
                self.model.ikSpHdleSetting_parentCurve_ckBx = pm.checkBox(
                    label = 'Auto parent curve'  # parentCurve(pcv)  bool
                    , value = False
                    , annotation = u'ikSplineHandle により影響を受ける最初のジョイントの親が、'
                                   u'自動的にカーブの親となるかどうかを指定します\n'
                                   u'\t'
                                   u'my setting default: False\n'
                                   u'\t'
                                   u'maya setting default: True'
                )
                self.model.ikSpHdleSetting_pcv_txtFld = pm.textField(
                    enable = True
                    , editable = False
                    , tx = '...'
                    , bgc = self.model.bgcGray2
                    , ann = u'spline IK curve の parent 先を検索し、表示します'
                )
                pm.button(enable = False, w = 20, label = 'Set', ann = u'Set ボタンです')
                pm.button(enable = False, w = 20, label = 'sel', ann = u'選択 ボタンです')
                pm.button(enable = False, w = 20, label = 'C', ann = u'登録解除 ボタンです')

            #####################
            # createCurve(ccv)
            self.model.ikSpHdleSetting_createCurve_ckBx = pm.checkBox(
                label = 'Auto create curve'  # createCurve(ccv)  bool
                , value = True, enable = False
                , annotation = u'ikSplineHandle に対してカーブを自動的に作成するかどうかを指定します\n'
                               u'\t'
                               u'my setting default: True\n'
                               u'\t'
                               u'maya setting default: True'
            )

            #####################
            # simplifyCurve(scv)
            self.model.ikSpHdleSetting_simplifyCurve_ckBx = pm.checkBox(
                label = 'Auto simplify curve'  # simplifyCurve(scv)  bool
                , value = True
                , annotation = u'ikSplineHandle カーブを単純化するかどうかを指定します\n'
                               u'\t'
                               u'my setting default: True\n'
                               u'\t'
                               u'maya setting default: True'
            )

            # Reset ボタン
            with pm.rowLayout(
                    numberOfColumns = 2
                    , adjustableColumn = 2
                                              ) as AA:
                pm.text(' ' * 110)
                pm.button(h = 20, label = 'Reset'
                          , c = partial(self.model.reset_iKSplineHandleSetting)
                          , annotation = u'Reset these setting, only'
                          )
            # ###########################################################################
            # separator
            pm.separator(style = 'shelf'
                         , w = 10
                         , height = 10
                         )

            #####################
            # auto grouping
            self.model.ikSpHdleSetting_grouping_ckBx = pm.checkBox(
                label = 'Grouping'  # simplifyCurve(scv)  bool
                , value = True
                , annotation = u'適切に Grouping するかを指定します（独自規格）\n'
                               u'\t'
                               u'my setting default: True'
            )

    # 完全に新規
    # UI-2. 追加オプション
    # UI-25. 名前をcheckするUI の作成
    def finalNaming(self):
        u""" < UI-2. UI 追加オプション  UI-25. 名前をcheckするUI の作成 です >

        ::

          完全に新規
        """
        # clmLyut_finalNaming
        with pm.verticalLayout(
                # adjustableColumn = True
                # , bgc = self.bgcGray
                # ,
                spacing = 5
        ) as clmLyut_finalNaming:
            pm.separator(style = 'in'
                         # , w = 10
                         , height = 10
                         )

            # C: naming check
            with pm.rowLayout(
                    numberOfColumns = 4
                    , adjustableColumn = 2
            ) as C:
                pm.text(label = ' ' * 25)
                pm.button(label = u'↓↓ naming check ! ↓↓'
                          , w = 10
                          , bgc = self.model.bgcGray
                          , c = partial(self.model.check_naming_command)
                          , annotation = u'押下により、作成時のネーミングの'
                                         u'確認が行えます。\n'
                                         u'上部 textField の入力に基づきます。'
                          )
                pm.text(label = ' ' * 25)

            # D: final naming
            with pm.rowLayout(
                    numberOfColumns = 2
                    , adjustableColumn = 2
            ) as D:
                pm.text(label = ' ' * 10)
                pm.text(label = 'final naming')

            # E: 1. Spline IK Handle name
            with pm.rowLayout(
                    numberOfColumns = 2
                    , adjustableColumn = 2
                    # , height = 20
            ) as E:
                pm.text(label = '1. Spline IK Handle name (DAG): '
                                +
                                ' '
                        )
                self.model.cTxt_spIKHndle_ckName = pm.text(
                    label = ''
                    , bgc = self.model.bgcGray2
                )

            # F: 2. Spline IK Curve name
            with pm.rowLayout(
                    numberOfColumns = 2
                    , adjustableColumn = 2
                    # , height = 20
            ) as F:
                pm.text(label = '2. Spline IK Curve name (DAG): '
                                +
                                ' ' * 3
                        )
                self.model.cTxt_spIKCrv_ckName = pm.text(
                    label = ''
                    , bgc = self.model.bgcGray2
                )
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

    # base からの継承で再利用...
    # Close 実行 関数
    # def editMenuCloseCmd(self, *args):
    #     pass
    # 1. UI-1. メニュー コマンド群 ######################################################## end

if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
