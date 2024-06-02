# -*- coding: utf-8 -*-

u"""
YO_pointConstraintByMatrix1_View.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -5.0-
:Date: 2024/05/16

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PyMel version: 1.2.0
    - PySide2 version: 5.15.2

-リマインダ-
    done: 2024/05/16
        - 変更11 追加11 新規11
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

                    +   # 追加11
                        from PySide2.QtCore import Slot

                    +   # 追加11
                        from ..TemplateForPySide2.CustomScriptEditor2SPIModule import custom_scriptEditor2_instance

                    +   def __init__(self, _model):
                            ...
                            # 追加11 ########################################################### start
                            self.scriptEditor2_chunk1()
                            self.scriptEditor2_chunk2()
                            # 追加11 ########################################################### end

                    +   # 追加11 ########################################################### start
                        def scriptEditor2_chunk1(self):
                            ...

                        def scriptEditor2_chunk2(self):
                            ...

                        def create_scriptEditor2_and_show(self):
                            ...

                        @Slot()
                        def on_scriptEditor2_closed(self):
                            ...
                        # 追加11 ########################################################### end

                    +   def editMenuCloseCmd(self, *args):
                            ...
                            # 追加11 ########################################################### start
                            # カスタムの専用 スクリプトエディタ2 を同時に閉じます
                            if self.statusCurrent_scriptEditor2 == 'closed':
                                pass
                            else:
                                # スクリプトエディタ は 完全に閉じず 隠れます
                                self.scriptEditor2.close()

                                ...
                            # 追加11 ########################################################### end
        version = '-5.0-'

    done: 2024/01/04
        - 変換箇所8
            - 概要: 絶対パス から 相対パス へ記述変更
            - 詳細:
                ::

                  -     from YO_utilityTools.pointConstraintByMatrix.[...] import ...
                  +     from .[...] import ...

                  -     from YO_utilityTools.lib.[...] import ...
                  +     from ..lib.[...] import ...

                  -     from YO_utilityTools.renameTool.YO_renameTool5_Ctlr import RT_Ctlr
                  +     from ..renameTool.YO_renameTool5_Ctlr import RT_Ctlr
        version = '-4.3-'

    done: 2023//10/26
        汎用箇所を、モジュールとして読み込みに変更

        version = '-2.0-'

    done: 2023/10/16
        - 変更箇所1
            - 概要: 登録・確認用ボタンの、1関数実行実現のため、
                引数付き1関数を新規定義したので(***_Modl.py)、
                    これに伴います。
                引数付き実行のpartialを利用。
            - 詳細箇所:
                ::

                    ...
                  partial(self.model.ui_tFldA_allBtnCmd, 'set')
                    ...
                  partial(self.model.ui_tFldA_allBtnCmd, 'sel')
                    ...
                  partial(self.model.ui_tFldA_allBtnCmd, 'clr')
                    ...
                  partial(self.model.ui_tFldB_allBtnCmd, 'set')
                    ...
                  partial(self.model.ui_tFldB_allBtnCmd, 'sel')
                    ...
                  partial(self.model.ui_tFldB_allBtnCmd, 'clr')
                    ...

        version = '-1.1-'

    done: 2023/10/12~2023/10/16
        - 新規

        version = '-1.0-'
"""

# 標準ライブラリ #################################################################
from functools import partial  # partial 利用時は、最後の引数に、*args 要時あり

# サードパーティライブラリ #########################################################
import maya.cmds as cmds
import maya.OpenMaya as om
from pymel import core as pm
from pymel.core import uitypes as ui
# 追加11
from PySide2.QtCore import Slot

# ローカルで作成したモジュール ######################################################
import YO_utilityTools.pointConstraintByMatrix.config as docstring
# basic_configuration_for_derivation(派生用の基本構成)
from .config import SPACE, TITLE, VERSION
# 汎用ライブラリー の使用 ################################################################ start
from ..lib.message import message
# 汎用ライブラリー の使用 ################################################################## end
# 追加11
from ..TemplateForPySide2.CustomScriptEditor2SPIModule import custom_scriptEditor2_instance


class PConByMat_View(object):
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
        self.model = _model

        self.title = TITLE
        self.space = SPACE
        self.version = VERSION

        self.win = TITLE + '_ui'

        self.size = (316, 312)

        self.infoSummary = (u'point constraint byMatrix ツール\n'
                            u'の バージョン1(PyMel版) です。'
                            )
        self.infoDetail = (u'matrix を使用した、\n'
                           u'point constraint'
                           u'を自動作成するツールです。'
                           )

        self.bgcBlue2 = [0.0, 0.7, 1.0]  # list of float
        self.bgcBlue = [0.5, 0.5, 0.9]  # list of float

        # 追加11 ########################################################### start
        self.scriptEditor2_chunk1()
        self.scriptEditor2_chunk2()
        # 追加11 ########################################################### end

    # common コマンド群 ################################################################ start
    # print message メソッド
    # from ..lib.message import message へ移動...

    # print warning message メソッド
    # from ..lib.message_warning import message_warning へ移動...

    # selection 共通関数 v3 -flatten込み
    # from ..lib.commonCheckSelection import commonCheckSelection へ移動...
    # common コマンド群 ################################################################## end

    # 追加11 ########################################################### start
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
        # print('outPut 専用 scriptEditor2 ウィジェット を単独で作成します')
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
    # 追加11 ########################################################### end

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
            with ui.AutoLayout(ratios = [4.5, 1]):
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
        self.displayOptions_textField()  # UI-22. TextField オプション の作成
        self.displayOptions_checkBox()  # UI-21. mode オプション の作成
        self.displayOptions_button()  # UI-21. mode オプション の作成

    # UI-2. 追加オプション
    # UI-22. TextField オプション の作成
    def displayOptions_textField(self):
        u""" < UI-2. 追加オプション  UI-22. TextField オプション の作成 > """
        with pm.columnLayout(adjustableColumn = True) as dispOpt_txtFld_layout:
            ######################################################
            # cmnLyutA ###########################################
            with pm.rowLayout(
                    numberOfColumns = 5
                    # , bgc = self.bgcBlue2
                    , adjustableColumn = 2
                    ):
                pm.text(label = u'コントローラ側(source):', annotation = u"制御する側です")
                self.model.tFldA_set_src = pm.textField(
                    text = ''
                    , annotation = u"制御する側\n"
                                   u"コントローラです。 set 入力してください。"
                    )
                self.model.tBtnA_set_src = pm.button(
                    l = 'Set'
                    , width = 20
                    , annotation = u'set'
                    , c = partial(self.model.ui_tFldA_allBtnCmd, 'set')
                    )
                self.model.tBtnA_sel_src = pm.button(
                    l = 'Sel'
                    , width = 18
                    , annotation = u'select set'
                    , enable = False
                    , c = partial(self.model.ui_tFldA_allBtnCmd, 'sel')
                    )
                self.model.tBtnA_clr_src = pm.button(
                    l = 'C'
                    , width = 15
                    , annotation = u'clear set'
                    , enable = False
                    , c = partial(self.model.ui_tFldA_allBtnCmd, 'clr')
                    )
            ######################################################
            # cmnLyutB ###########################################
            with pm.rowLayout(
                    numberOfColumns = 5
                    # , bgc = self.bgcBlue2
                    , adjustableColumn = 2
                    ):
                pm.text(label = u'コントロールされる側(target):', annotation = u"制御される側です")
                self.model.tFldB_set_tgt = pm.textField(
                    text = ''
                    , annotation = u"制御される側\n"
                                   u"コントロールされる方です。 拘束を必要とする方です。 set 入力してください。"
                    )
                self.model.tBtnB_set_tgt = pm.button(
                    l = 'Set'
                    , width = 20
                    , annotation = u'set'
                    , c = partial(self.model.ui_tFldB_allBtnCmd, 'set')
                    )
                self.model.tBtnB_sel_tgt = pm.button(
                    l = 'Sel'
                    , width = 18
                    , annotation = u'select set'
                    , enable = False
                    , c = partial(self.model.ui_tFldB_allBtnCmd, 'sel')
                    )
                self.model.tBtnB_clr_tgt = pm.button(
                    l = 'C'
                    , width = 15
                    , annotation = u'clear set'
                    , enable = False
                    , c = partial(self.model.ui_tFldB_allBtnCmd, 'clr')
                    )
            ######################################################
            # dispOpt_txtFld_layout.redistribute(1, 1, 1)  # ボタン幅比率の矯正補正

    # UI-2. 追加オプション
    # UI-21. checkBox オプション の作成
    def displayOptions_checkBox(self):
        u""" < UI-2. 追加オプション  UI-21. mode オプション の作成 > """
        with pm.columnLayout(adjustableColumn = True
                , columnAttach = ['left', 30]
                             ) as dispOpt_mode_layout:
            # radioCollection #######################################
            # type: pm.radioCollection
            self.model.cBox_cnctAll = pm.checkBox(
                l = u'create new nodes and connect all'
                , value = True
                )
            # dispOpt_mode_layout.redistribute(1.2, 1, 6)  # ボタン幅比率の矯正補正

    def displayOptions_button(self):
        # break and reset ボタンLayout + ボタン1つ
        with pm.columnLayout(
                adjustableColumn = True
                , columnAttach = ['left', 100]
                           ):
            breakAndReset = 'Break And Reset'
            pm.button(l = 'break and reset'
                      , annotation = u'connection を全て削除し、\n'
                                     u'独自規格を利用して、\n実行する前の、ローカル数値にも'
                                     u'リセットいたします。'
                      , c = partial(self.controller.breakAndResetBtn
                                    , 'button, ' + breakAndReset
                                    )
                      )
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
        # pm.launch(web = 'http://help.autodesk.com/cloudhelp/2016/'
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

        # 追加11 ########################################################### start
        # # カスタムの専用 スクリプトエディタ2 を同時に閉じます
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
        # 追加11 ########################################################### end
    # 1. UI-1. メニュー コマンド群 ######################################################## end


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
