# -*- coding: utf-8 -*-

u"""
YO_renameTool5_View.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -5.0-
:Date: 2024/05/15

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PyMel version: 1.2.0
    - PySide2 version: 5.15.2

-リマインダ-
    done: 2024/05/13~2024/05/15
        - 変更7 と 追加7
            - 概要: maya default の Script Editor へのログ出力 を、
                YO_logProcess.action('ERROR'...)
                YO_logProcess.action('WARNING'...)
                    で行っていた箇所を、
                カスタムの Script Editor2 (PySide2作成UI) で置き換え
                    における、エラーの影響を回避
            - 詳細: カスタムの Script Editor2 (PySide2作成UI) で置き換える為には、
                from ..TemplateForPySide2.CustomScriptEditor2SPIModule import custom_scriptEditor2_instance
                モジュールを必要とします
                また、
                    YO_renameTool5_Modl モジュール での記述を主とするのですが、
                        当モジュール YO_renameTool5_View へもエラーの影響が及びます
                そのエラーの影響を回避する目的として、
                    以下のように、あらかじめ カスタムの Script Editor2 モジュール
                        を定義しています
                ::

                    +   # 追加7
                        from PySide2.QtCore import Slot

                    +   # 追加7
                        from ..TemplateForPySide2.CustomScriptEditor2SPIModule import custom_scriptEditor2_instance

                    +   def __init__(self, _model):
                            ...
                            # 追加7 ########################################################### start
                            self.scriptEditor2_chunk1()
                            self.scriptEditor2_chunk2()
                            # 追加7 ########################################################### end

                    +   # 追加7 ########################################################### start
                        def scriptEditor2_chunk1(self):
                            ...

                        def scriptEditor2_chunk2(self):
                            ...

                        def create_scriptEditor2_and_show(self):
                            ...

                        @Slot()
                        def on_scriptEditor2_closed(self):
                            ...
                        # 追加7 ########################################################### end

                    +   def editMenuCloseCmd(self, *args):
                            ...
                            # 追加7 ########################################################### start
                            # カスタムの専用 スクリプトエディタ2 を同時に閉じます
                            if self.statusCurrent_scriptEditor2 == 'closed':
                                pass
                            else:
                                # スクリプトエディタ は 完全に閉じず 隠れます
                                self.scriptEditor2.close()

                                ...
                            # 追加7 ########################################################### end
        version = '-5.0-'

    done: 2023/12/21
        - 変換箇所6
            - 概要: 絶対パス から 相対パス へ記述変更
            - 詳細:
                ::

                    -     from YO_utilityTools.renameTool.[...] import ...
                    +     from .[...] import ...

                    -     from YO_utilityTools.lib.[...] import ...
                    +     from ..lib.[...] import ...
        version = '-4.2-'

    done: 2023//10/25
        汎用箇所を、モジュールとして読み込みに変更

        version = '-4.0-'

    done: 2023/09/08~2023/09/20
        python2系 -> python3系 変換
            - YO_renameTools5_main.py 変換記述あり
            - YO_renameTools5_Modl.py 変換記述あり
            詳細はそれ自身のリマインダに記述...

        version = '-3.0-'

    done: 2023/03/13~2022/04/10
        派生ファイル作成を考慮してコードの見直し

        version = '-2.0-'

    done: 2023/02/22~2022/02/23
        新規

        version = '-1.0-'
"""

# 標準ライブラリ #################################################################
from functools import partial  # partial 利用時は、最後の引数に、*args 要時あり

# サードパーティライブラリ #########################################################
import maya.cmds as cmds
# import maya.OpenMaya as om
from pymel import core as pm
from pymel.core import uitypes as ui
# 追加7
from PySide2.QtCore import Slot

# ローカルで作成したモジュール ######################################################
import YO_utilityTools.renameTool.config as docstring
# basic_configuration(基本構成)
from .config import SPACE, TITLE, VERSION
# 汎用ライブラリー の使用 ################################################################ start
from ..lib.message import message
from ..lib.message_warning import message_warning
# 汎用ライブラリー の使用 ################################################################## end
# 追加7
from ..TemplateForPySide2.CustomScriptEditor2SPIModule import custom_scriptEditor2_instance


class RT_View(object):
    u""" < GUIウィンドウを作成するための Viewクラス です >

    ::

      UIを作成するためのメソッドや、UIの更新を行うためのメソッドを実装します。

      GUIウィンドウを作成するための PyMel コードが含まれます。
        Viewクラスのコンストラクターは、Modelオブジェクト への参照を受け取ります。
            View クラスは GUIウィンドウ を作成し、そのウィンドウ内の要素を更新するためのメソッドを提供します。

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
    def __init__(self, _model):
        self.model = _model

        self.title = TITLE
        self.space = SPACE
        self.version = VERSION
        
        self.win = TITLE + '_ui'

        self.size = (316, 312)

        self.infoSummary = (u'独自規格の命名規則に基づいた rename ツール\n'
                            u'の バージョン5(PyMel版) です。'
                            )
        self.infoDetail = (u'●独自規格の命名規則とは、\n'
                           u'1. 第1単語 + 第2単語 + 第3単語 で基本的に構成\n'
                           u'2. 命名には、多くても 2つの  _(アンダーバー) で必ず構成する\n'
                           u'\te.g.): lip_jtA_GpL\n'
                           u'\te.g.): lip_jtA\n'
                           u'\te.g.): lip_geo, lip_rigGeo\n'
                           u'3. 第1単語, 第2単語は 必ず小文字で始まる、'
                           u'ローワーキャメルケース記述 を基本とする\n'
                           u'\te.g.): lip_jt\n'
                           u'\te.g.): lip_geo, lip_rigGeo, lip_jtA_GpL\n'
                           u'4. 第3単語は 必ず大文字で始まる、アッパーキャメルケース記述 を基本とする\n'
                           u'\te.g.): lip_jtA_GpL, lip_jt_AL, lip_jtA_L\n'
                           u'5. 識別子は、 必ず大文字で始まる\n'
                           u'\t識別子とは、\n'
                           u'\t\ta. ナンバリング用識別子\n'
                           u'\t\tb. 文字列 Gp 識別子（グループの意）\n'
                           u'\t\tc. サイド用識別子\n'
                           u'\t\t\tを想定しています\n'
                           u'\te.g.): "A", "B", "L", "R", "Gp" ....\n'
                           u'6. 命名には、ナンバリング用識別子は 2個以上 存在してはいけない\n'
                           u'\t以下は NG です\n'
                           u'\tNG. ): lip_jtA_AL\n\n'
                           u'●text ベースのコマンド 出力を搭載\n'
                           u'UI操作実行後、 maya script editor の一行目には必ず、'
                           u'text ベースのコマンド を出力も致します。\n'
                           u'繰り返し作業や、スクリプトベースの作業を補足するためです。\n'
                           u'詳細は、 \n'
                           u'\t当ツール の help をご覧ください。'
                           )

        self.bgcBlue2 = [0.0, 0.7, 1.0]  # list of float
        self.bgcBlue = [0.5, 0.5, 0.9]  # list of float

        # 追加7 ########################################################### start
        self.scriptEditor2_chunk1()
        self.scriptEditor2_chunk2()
        # 追加7 ########################################################### end

    # common コマンド群 ################################################################ start
    # print message メソッド
    # from ..lib.message import message へ移動...

    # print warning message メソッド
    # from ..lib.message_warning import message_warning へ移動...

    # selection 共通関数 v3 -flatten込み
    # from ..lib.commonCheckSelection import commonCheckSelection へ移動...
    # common コマンド群 ################################################################## end

    # 追加7 ########################################################### start
    # ここで、CustomScriptEditor2 の closedシグナル を購読しています
    def scriptEditor2_chunk1(self):
        # note): custom_scriptEditor2_instance 本モジュール基で、
        #   CustomScriptEditor2(title, infoDetail)
        #   引数: title, 引数: infoDetail
        #   を定義しています
        self.scriptEditor2 = custom_scriptEditor2_instance

        # ここで、CustomScriptEditor2 の closedシグナル を購読しています
        self.scriptEditor2.closed.connect(self.on_scriptEditor2_closed)

        # カスタムで、専用の スクリプトエディタ を初期化
        # self.scriptEditor2 = None
        self.statusCurrent_scriptEditor2 = 'open'

    def scriptEditor2_chunk2(self):
        # print('--------- ' + f'{self.__class__}' + ' ---------')
        # print('outPut 専用 scriptEditor2 ウィジェット を 紐づき で作成します')
        self.create_scriptEditor2_and_show()
        # print(self.scriptEditor2)
        # print('--------- ' + f'{self.__class__}' + ' ---------' * 3 + 'end\n')

    def create_scriptEditor2_and_show(self):
        # CustomScriptEditor2 ﾓｼﾞｭｰﾙ先では、あえて、show() せず、ここで show() しています。
        self.scriptEditor2.show()  # note): これは必須です。
        self.statusCurrent_scriptEditor2 = 'open'

    # CustomScriptEditor2 クラスの closedシグナル が発行されると 当メソッド が呼び出されます
    @Slot()
    def on_scriptEditor2_closed(self):
        # commonMessage = "Script editor was hided. Not closed !!"
        # message_warning(commonMessage + f'{self.__class__}')

        self.statusCurrent_scriptEditor2 = 'closed'
        # # QTextEdit の内容を保存
        # self.script_editor_content = self.scriptEditor2.text_edit.toPlainText()
        # print(self.script_editor_content)
        return self.statusCurrent_scriptEditor2
    # 追加7 ########################################################### end

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
            self.commonMenu()  # 最上段の UI common menu の作成

            # UI-2. メインLayout + 情報 + 追加オプション
            with ui.AutoLayout(ratios = [3.5, 1]):
                with pm.tabLayout(scrollable = True  # 境界線のちらつき防止
                        , tabsVisible = False, h = 1
                        , childResizable = True
                                  ):  # tab 追加を可能とする時は、tabsVisible = True
                    with pm.columnLayout(adj = True):
                        # UI-2. 情報
                        self.commonInformation()

                        pm.separator(height = 10, style = 'out')

                        # UI-2. 追加オプションのまとまり
                        self.displayOptions()

                # UI-3. ボタンLayout + 底面ボタン3つ
                with ui.AutoLayout(orientation = "horizontal"
                        , spacing = 3
                                   ) as commonBtns_layout:
                    # UI-3. 底面ボタン3つ
                    self.commonButtons()
                    commonBtns_layout.redistribute(2, 1, 1)  # ボタン幅比率の矯正補正

        # # UI-4. optionVar による値の復元
        restoreOptionVar = 'Restore Option Variables'
        # self.restoreOptionVarCmd(restoreOptionVar)
        self.controller.restoreOptionVar(restoreOptionVar)
        # # partial(self.restoreOptionVarCmd, restoreOptionVar)

        cmds.evalDeferred(lambda *args: pm.showWindow(self.win))

    # UIディテール 作成 ################################################################ start
    # UI-1. commonメニュー
    def commonMenu(self):
        u""" < UI-1. commonメニュー の作成 > """
        # Edit menu ##############################################
        pm.menu(l = 'Edit')
        saveSettings = 'Save Settings'
        pm.menuItem(l = saveSettings
                    , c = partial(self.controller.menuSave, 'menu, ' + saveSettings)
                    )
        resetSettings = 'Reset Settings'
        pm.menuItem(l = resetSettings
                    , c = partial(self.controller.menuReload, 'menu, ' + resetSettings)
                    )

        pm.menuItem(divider = True)

        closeThisUi = 'Close This UI'
        pm.menuItem(l = closeThisUi
                    , c = partial(self.controller.menuClose, 'menu, ' + closeThisUi)
                    )

        # Help menu ##############################################
        pm.menu(l = 'Help')
        help = 'Help'
        pm.menuItem(l = 'Help on {}'.format(self.model.title)
                    , c = partial(self.controller.menuHelp, help)
                    )

    # UI-3. common底面ボタン3つ
    def commonButtons(self):
        u""" < UI-3. common底面ボタン3つの作成 > """
        execute = 'Execute'
        pm.button(l = execute, bgc = self.bgcBlue2
                  , c = partial(self.controller.executeBtn, 'button, ' + execute)
                  )
        reset = 'Reset'
        pm.button(l = reset
                  , c = partial(self.controller.menuReload, 'button, ' + reset)
                  )
        close = 'Close'
        pm.button(l = close
                  , c = partial(self.controller.menuClose, 'button, ' + close)
                  )

    # UI-2. common情報
    def commonInformation(self):
        u""" < UI-2. common情報 の作成 > """
        pm.text(l = self.infoSummary)
        pm.text(l = u'note:'
                , annotation = self.infoDetail
                , bgc = self.bgcBlue
                )

    # UI-2. 追加オプションのまとまり
    def displayOptions(self):
        u""" < UI-2. 追加オプションのまとまり の作成 > """
        self.displayOptions_mode()  # UI-21. mode オプション の作成
        self.displayOptions_textField()  # UI-22. TextField オプション の作成

    # UI-2. 追加オプション
    # UI-21. mode オプション の作成
    def displayOptions_mode(self):
        u""" < UI-2. 追加オプション  UI-21. mode オプション の作成 > """
        with pm.rowColumnLayout(numberOfRows = 1, columnSpacing = (1, 10)
                                ) as dispOpt_mode_layout:
            pm.text(l = 'rename mode  ')
            # radioCollection #######################################
            # type: pm.radioCollection
            self.model.cmnModeRdBtnClcton = pm.radioCollection()
            pm.radioButton(self.model.mode_handleNameLists[0]
                , select = True
                , label = u'強制的'
                , onCommand = partial(self.controller.currentMode, 'mode0')
                           )
            pm.radioButton(self.model.mode_handleNameLists[1]
                , select = False
                , label = u'構成要素をキープ'
                , onCommand = partial(self.controller.currentMode, 'mode1')
                # , bgc = self.bgcBlue
                           )
            # dispOpt_mode_layout.redistribute(1.2, 1, 6)  # ボタン幅比率の矯正補正

    # UI-2. 追加オプション
    # UI-22. TextField オプション の作成
    def displayOptions_textField(self):
        u""" < UI-2. 追加オプション  UI-22. TextField オプション の作成 > """
        with pm.horizontalLayout() as dispOpt_txtFld_layout:
            ######################################################
            # cmnLyutA ###########################################
            with pm.columnLayout(adj = True
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
                    , cc = partial(self.controller.limitedTypingInput
                                   , u'cmnTxtFld_A1'
                                   )
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
                            , c = partial(self.controller.textFieldPupMnu
                                          , u'cmnPUpMnu_A1', u'@'
                                          )
                            , ann = u'ナンバリング用識別子を追加します。'
                            )
                pm.menuItem(label = u'tilde --> ~'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆そのままの文字列を利用◆◆'
                            , c = partial(self.controller.textFieldPupMnu
                                          , u'cmnPUpMnu_A1', u'~'
                                          )
                            , ann = u'そのままの文字列を利用します。'
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
                            , c = partial(self.controller.textFieldPupMnu
                                          , u'cmnPUpMnu_A1', u''
                                          )
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
                            , c = partial(self.controller.textFieldPupMnu
                                          , u'cmnPUpMnu_A1', u'SpIk'
                                          )
                            , ann = u'プリセット名'
                            )

            ######################################################
            # cmnLyutB ###########################################
            with pm.columnLayout(adj = True
                                 ) as self.cmnLyutB:
                # textField B1 #######################################
                # type: pm.textField
                self.model.cmnTxtFld_B1 = pm.textField(
                    insertionPosition = 0
                    , height = 26
                    # , w = 50
                    , tx = self.model.currentTxt_B1
                    , bgc = self.model.textFieldBgc_B1
                    , ann = u'第2単語:主に役割等を表す入力領域です。\n'
                            u'右ボタンで補足できます。\n'
                            u'e.g.): "jt", "if", "geo", "rigGeo", "ctrl"`\n'
                            u'補足:[],@,~ 識別子は'
                            u'このフィールド内では'
                            u'規定文字として入力を許可しています。'
                    , cc = partial(self.controller.limitedTypingInput
                                   , u'cmnTxtFld_B1'
                                   )
                    , pht = 'jt', font = self.model.tempFont
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
                            , c = partial(self.controller.textFieldPupMnu
                                          , u'cmnPUpMnu_B1', u'[Space]'
                                          )
                            , ann = u'挿入用文字列識別子を追加します。 e.g.)サンプル[Space]'
                            )
                pm.menuItem(label = u'at sign --> @'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆ナンバリング用識別子を追加◆◆'
                            , c = partial(self.controller.textFieldPupMnu
                                          , u'cmnPUpMnu_B1', u'@'
                                          )
                            , ann = u'ナンバリング用識別子を追加します。'
                            )
                pm.menuItem(label = u'tilde --> ~'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆そのままの文字列を利用◆◆'
                            , c = partial(self.controller.textFieldPupMnu
                                          , u'cmnPUpMnu_B1', u'~'
                                          )
                            , ann = u'そのままの文字列を利用します。'
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
                            , c = partial(self.controller.textFieldPupMnu
                                          , u'cmnPUpMnu_B1', u''
                                          )
                            , ann = u'文字列をクリアーします。'
                            )
                # プリセット
                pm.menuItem(label = u'##### '
                                    u'preset (プリセット)'
                                    u' #####'
                            , divider = True
                            )
                pm.menuItem(label = u'geo'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆geometry としての命名の付加◆◆'
                            , c = partial(self.controller.textFieldPupMnu
                                          , u'cmnPUpMnu_B1', u'geo'
                                          )
                            , ann = u'プリセット名'
                            )
                pm.menuItem(label = u'bindGeo'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆skinning geometry としての命名の付加◆◆'
                            , c = partial(self.controller.textFieldPupMnu
                                          , u'cmnPUpMnu_B1', u'bindGeo'
                                          )
                            , ann = u'プリセット名'
                            )
                pm.menuItem(label = u'--' * 20)
                pm.menuItem(label = u'spIKjt'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆spline IK joint としての命名の付加◆◆'
                            , c = partial(self.controller.textFieldPupMnu
                                          , u'cmnPUpMnu_B1', u'spIKjt'
                                          )
                            , ann = u'プリセット名'
                            )
                pm.menuItem(label = u'jt'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆joint としての命名の付加◆◆'
                            , c = partial(self.controller.textFieldPupMnu
                                          , u'cmnPUpMnu_B1', u'jt'
                                          )
                            , ann = u'プリセット名'
                            )
                pm.menuItem(label = u'if'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆influence joint としての命名の付加◆◆'
                            , c = partial(self.controller.textFieldPupMnu
                                          , u'cmnPUpMnu_B1', u'if'
                                          )
                            , ann = u'プリセット名'
                            )
                pm.menuItem(label = u'jtPxy'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆joint proxy としての命名の付加◆◆'
                            , c = partial(self.controller.textFieldPupMnu
                                          , u'cmnPUpMnu_B1', u'jtPxy'
                                          )
                            , ann = u'プリセット名。'
                            )
                pm.menuItem(label = u'ctrl'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆controller としての命名の付加◆◆'
                            , c = partial(self.controller.textFieldPupMnu
                                          , u'cmnPUpMnu_B1', u'ctrl'
                                          )
                            , ann = u'プリセット名。'
                            )

            ######################################################
            # cmnLyutC ###########################################
            with pm.rowLayout(numberOfColumns = 4
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
                    , pht = '@', font = self.model.tempFont
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
                            , c = partial(self.controller.textFieldPupMnu
                                          , u'cmnPUpMnu_C1', u'@'
                                          )
                            , ann = u'ナンバリング用識別子を利用します。'
                            )
                pm.menuItem(label = u'tilde --> ~'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆そのままの文字列を利用◆◆'
                            , c = partial(self.controller.textFieldPupMnu
                                          , u'cmnPUpMnu_C1', u'~'
                                          )
                            , ann = u'そのままの文字列を利用します。'
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
                            , c = partial(self.controller.textFieldPupMnu
                                          , u'cmnPUpMnu_C1', u''
                                          )
                            , ann = u'文字列をクリアーします。'
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
                    , pht = 'Gp', font = self.model.tempFont
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
                            , c = partial(self.controller.textFieldPupMnu
                                          , u'cmnPUpMnu_C2', u'Gp'
                                          )
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
                            , c = partial(self.controller.textFieldPupMnu
                                          , u'cmnPUpMnu_C2', u''
                                          )
                            , ann = u'文字列をクリアーします。'
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
                self.model.cmnPUpMnu_C3 = pm.popupMenu(b = 3)
                # プリセット
                pm.menuItem(label = u'##### '
                                    u'preset (プリセット)'
                                    u' #####'
                            , divider = True
                            )
                pm.menuItem(label = u'left -- > L'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆文字列 L 識別子を利用◆◆'
                            , c = partial(self.controller.textFieldPupMnu
                                          , u'cmnPUpMnu_C3', u'L'
                                          )
                            , ann = u'プリセット名'
                            )
                pm.menuItem(label = u'right -- > R'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆文字列 R 識別子を利用◆◆'
                            , c = partial(self.controller.textFieldPupMnu
                                          , u'cmnPUpMnu_C3', u'R'
                                          )
                            , ann = u'プリセット名'
                            )
                pm.menuItem(label = u'center -- > C'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆文字列 C 識別子を利用◆◆'
                            , c = partial(self.controller.textFieldPupMnu
                                          , u'cmnPUpMnu_C3', u'C'
                                          )
                            , ann = u'プリセット名'
                            )
                pm.menuItem(label = u'middle -- > M'
                                    +
                                    self.space * 4
                                    +
                                    u'◆◆文字列 M 識別子を利用◆◆'
                            , c = partial(self.controller.textFieldPupMnu
                                          , u'cmnPUpMnu_C3', u'M'
                                          )
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
                            , c = partial(self.controller.textFieldPupMnu
                                          , u'cmnPUpMnu_C3', u''
                                          )
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
                pm.menuItem(divider = True)
            dispOpt_txtFld_layout.redistribute(1, 1, 1)  # ボタン幅比率の矯正補正
    # UIディテール 作成 ################################################################## end

    # 1. UI-1. メニュー コマンド群 ###################################################### start
    # Save Settings 実行による optionVar の保存 関数
    # Model へ移動...

    # Reload 実行 関数
    def editMenuReloadCmd(self, *args):
        u""" < Reload 実行 関数 です > """
        # print(args)
        # self.__init__()  # すべて、元の初期値に戻す
        # self.set_default_value_toOptionVar()  # optionVar の value を default に戻す操作

        pm.evalDeferred(lambda *args: self.create())  # refresh UI <---- ここ重要!!

        # message(args[0])

    # Help 実行 関数
    def helpMenuCmd(self, *args):
        u""" < Help 実行 関数 です > """
        # cmds.launch(web = 'http://help.autodesk.com/cloudhelp/2016/'
        #                   'JPN/Maya-Tech-Docs/CommandsPython/index.html'
        #             )
        help(docstring)
        message('For more information, see Script Editor')

    # Close 実行 関数
    def editMenuCloseCmd(self, *args):
        u""" < Close 実行 関数 です > """
        # self.editMenuSaveSettingsCmd('Save Settings')  # UI で閉じると、自動で Save Settings を実行します

        pm.evalDeferred(lambda *args: pm.deleteUI(self.win))

        # message(args[0])  # cmds.deleteUI(self.win)

        # 追加7 ########################################################### start
        # カスタムの専用 スクリプトエディタ2 を同時に閉じます
        if self.statusCurrent_scriptEditor2 == 'closed':
            pass
        else:
            # スクリプトエディタ は 完全に閉じず 隠れます
            self.scriptEditor2.close()

            # # スクリプトエディタを完全に閉じる
            # message("Script editor also completely closed and exited at the same time.")
            # # CustomScriptEditorのインスタンスはQtのイベントループが次に実行されるときに遅延削除されます。
            # # これにより、CustomScriptEditorのウィジェットが閉じられ、
            # # その後のコードがそのウィジェットを参照しないことを保証できる。
            # # CustomScriptEditorのインスタンスは完全に削除されるため、
            # # その状態（例えばQTextEditの内容）は保持されない。
            # # その状態を保持するためには、何らかの形でその状態を保存し、
            # # 新しいCustomScriptEditorのインスタンスが作成されるときにその状態を復元する必要がある
            # self.scriptEditor2.deleteLater()
        # 追加7 ########################################################### end

    # 1. UI-1. メニュー コマンド群 ######################################################## end


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
