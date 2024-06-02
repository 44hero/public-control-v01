# -*- coding: utf-8 -*-

u"""
YO_parentConstraintByMatrix5.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -4.0-
:Date: 2023/10/27

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PyMel version: 1.2.0

概要(overview):
    matrix を使用した、parent constraint, scale constraint を手動で作成していくツールです。
詳細(details):
    新規に、parentConstraint, scaleConstraint と同等な拘束処理を matrix 操作で実現します。

    具体的には、
        multMatrix の matrixIn[0] への setAttr 及び .matrixIn[1] への connectAttr
            から始まり、最後まで完了させており、
                また、multMatrix node -->> decomposeMatrix node のコネクションに至るまで、全ての必要な
                    工程を行っています。

    因みに、target が transform node の時と joint node の時とで、
        作成される node 数と connection 方法に若干の違いがあります。

        具体的には、
            target が joint node の時には、
            target の jointOrient も考慮しています。

    類似した python module ファイル
        YO_parentConstraintByMatrix62.py ツール (自動接続用)
            が存在しますが、
                基本的には当手動接続用ツールを推奨します。

使用法(usage):
    ::

      # -*- coding: utf-8 -*-

      path = r'C:/Users/username/....'  # e.g.):左記のように所定の位置までパスを通してから。。
      if path not in sys.path:
          print(u'now, add a path.....{}'.format(path))
          sys.path.append(path)
      else:
          print(u'already, added a path.....{}'.format(path))

      from imp import reload

      # import <パッケージ名>.<モジュール名>
      import YO_utilityTools.YO_parentConstraintByMatrix5
      YO_utilityTools.YO_parentConstraintByMatrix5.UI.showUI()

注意(note):
    ・ 他に必須な独自モジュール
        ::

          from YO_utilityTools.renameTool.YO_renameTool5_Modl import RT_Modl
          from YO_utilityTools.message import message
          from YO_utilityTools.message_warning import message_warning
          from YO_utilityTools.commonCheckSelection import commonCheckSelection  # :return: string

<UI 説明>
    ・ source : 制御する側
        コントローラです。 set 入力してください。
    ・ target : 制御される側
        コントロールされる方です。 拘束を必要とする方です。 set 入力してください。

-リマインダ-
    done: 2023//10/27
        汎用箇所を、モジュールとして読み込みに変更

        version = '-4.0-'

    done: 2023/05/24
        - 変更1
            - DG命名を見直す

        version = '-3.0-'

    done: 2023/05/11~2023/05/17
        - 役割で、クラス分けを実施
        - 中身を整理
            - initial attr の追加
            - optionVariable への対応

        version = '-2.0-'

    done: バグ修正 2021/10/01   YO_parentConstraintByMatrix42.py -3.0- 2021/09/30 に準じています。
        親リスト数の不一致時

        version = '-1.1-'

    done: 整理整頓 2021/09/26~09/30
        version = '-1.1-'

    done: コマンドバージョン作成を考慮した、
        当ツールよりも簡潔で自動接続を前提とした別ツールも作成しておきたい。
        YO_parentConstraintByMatrix42.py
        一旦完成 2019/10/23

    done: 一旦完成 2019/10/21
        version = '-1.0-'

    done: source側階層、target側階層を、全てたどり終え、必要な工程を全て完結。2019/10/18

    done: class版として、着手 2019/09/26
"""

import maya.cmds as cmds
# import maya.mel as mel
import maya.OpenMaya as om
# Maya Python API 2.0, OpenMaya モジュールのインポートとローカル名 om2 への変更
from maya.api import OpenMaya as om2
from maya.common.ui import LayoutManager

import re

# 汎用ライブラリー の使用 ################################################################ start
from YO_utilityTools.lib.message import message
from YO_utilityTools.lib.message_warning import message_warning
# from YO_utilityTools.lib.commonCheckJoint import commonCheckJoint  # :return: bool
from YO_utilityTools.lib.commonCheckSelection import commonCheckSelection  # :return: string

# optionVar_command_library(optionVarを操作するライブラリー)
from YO_utilityTools.lib.YO_optionVar import setOptionVarCmd  # オプション変数を設定する関数
from YO_utilityTools.lib.YO_optionVar import getOptionVarCmd  # オプション変数を取得する関数
# from YO_utilityTools.YO_optionVar import upDateOptionVarsDictCmd  # オプション変数をdict操作し、更新をかける関数
# from YO_utilityTools.YO_optionVar import upDateOptionVarCmd  # オプション変数に更新をかける関数
# 汎用ライブラリー の使用 ################################################################## end

from YO_utilityTools.renameTool.YO_renameTool5_Modl import RT_Modl

title = 'YO_parentConstraintByMatrix5'  # Long Name
space = ' '
version = '-4.0- <py 3.7.7 確認済, ui:cmds>'
underScore = '_'


class UICmd(object):
    u"""< 親クラス: Widget command class です >

    ::

      コマンド群クラスです
      当クラス内の内訳は大別すると以下となります

    ######

        - 1. UI-1. メニュー コマンド群

        追加
        - 4. UI-4. OptionVar を利用したパラメータ管理 コマンド群

        - 2. UI-2. 追加オプション コマンド群

        - その他 アルゴリズムとなる コマンド群

            - 命名規則のコントロール

        - 「main となる コマンド群」

            - main 1
                新規のノード作成や、接続の準備
            - main 2
                階層をたどり、新規作成された multMatrix との接続の有無まで

        追加
        - 独自規格 attribute 操作一連群

    ######
    """

    # A function to instantiate the UI window
    # UIウィンドウ をインスタンス化する関数
    @classmethod
    def showUI(cls):  # 子クラスに同じ名前のメソッドがあり、本来の目的はそちらです
        u"""< UIウィンドウ をインスタンス化する関数 です >

        ::

          子クラスに同じ名前のメソッドがあり、本来の目的はそちらです

          本来の目的である、UiBase_PyMel.showUI() を実現するために、
          ここでは、実行は無効にしています。
          つまり、
          後の子クラスに、当親クラスと同じ名前のメソッドを実装することで、
          当親クラスのメソッドを上書きすることができます。

          本来、当記述は不要ですが、呼び出している事を明らかにしたいので、あえて明記しています
        """
        pass

    def __init__(self):
        self.params = None
        self.size = (200, 55)
        self.win = title + '_ui'

        self.bgc = [0.5, 0.5, 0.5]  # list of float
        self.bgc2 = [0.27, 0.27, 0.27]  # list of float
        self.bgcRed = [0.5, 0.3, 0.3]  # list of float
        self.bgcBlue = [0.3, 0.3, 0.5]  # list of float
        self.bgcBlue2 = [0.5, 0.5, 0.9]  # list of float
        self.bgcBlue3 = [0.0, 0.7, 1.0]  # list of float

        self.NODES_A1 = ''
        self.NODES_A2 = ''
        self.text_A3_32_source = u'source\n: 階層側'
        self.text_A3_32_target = u'target\n: 階層側'
        self.newNodesAll = []

        self.OUTPUT_A = ''
        self.INPUT_A = ''
        self.OUTPUT_A32 = ''
        self.INPUT_A32 = ''
        self.src = ''
        self.tgt = ''
        self.srcP = ''
        self.mM = ''
        self.dM = ''
        self.followHierarchy_isConnected_ToF = False  # multMatrix の matrixIn[2] をトリガーとしています
        self.notYetConnected_counterStart = 2  # multMatrix の matrixIn で未接続の一番若い数字を記録1
        self.notYetConnected_counterEnd = 10  # multMatrix の matrixIn で未接続の一番若い数字を記録2
        self.INPUT_R_GETATTR = [0, 0, 0]
        self.INPUT_T_GETATTR = [0, 0, 0]
        self.INPUT_S_GETATTR = [1, 1, 1]
        self.INPUT_Sh_GETATTR = [0, 0, 0]

        # 特定ボタンの on/off 判定に使用
        # UI button である、
        # R:                     'cBtn_A3_oP2iP_connectTgl'
        # at once(T,S,Sher):     'cBtn_A32_atOnce_oP2iP_connectTgl'
        # at once(matrix index): 'cBtn_A3_32_1_3_atOnce_oP2iP_connectTgl'
        # 以上、特定な3つのボタンステイタスに利用
        self.ui_cBtn_specific_state = [0, 0, 0]  # 特定な3つのボタンステイタス list of bool

        # 追加
        # optionVar関連 ########################################################
        # DATA naming #####################################
        # dict  # range is 2
        # key:   [type(str), type(str)]  # range is 2
        # value: [type(str), type(str)]  # range is 2
        self.opVar_dictVal_dflt_list = ['', '']  # range is 2
        # range is 2
        self.optionVar01_tFld_key = title + underScore + 'txtFldSrc_text'  # type: str
        self.optionVar02_tFld_key = title + underScore + 'txtFldTgt_text'  # type: str

        # 追加
        # optionVar の初期実行 ############################
        # tFld_key Src
        self.cTxtFld_A_source = None
        if getOptionVarCmd(self.optionVar01_tFld_key) is None:  # set default
            setOptionVarCmd(self.optionVar01_tFld_key, self.opVar_dictVal_dflt_list[0])

        # tFld_key Tgt
        self.cTxtFld_A_target = None
        if getOptionVarCmd(self.optionVar02_tFld_key) is None:  # set default
            setOptionVarCmd(self.optionVar02_tFld_key, self.opVar_dictVal_dflt_list[1])

    # 1. UI-1. メニュー コマンド群 ###################################################### start
    # 追加
    # Save Settings 実行 関数
    def cM_editMenuSaveCmd(self, *args):
        u""" <SaveSetting 実行 関数>

        ::

          追加
        """
        # tFld_key Src
        getTxt_fromTxtFldSrc = cmds.textField(self.cTxtFld_A_source, q = True, text = True)
        setOptionVarCmd(self.optionVar01_tFld_key, getTxt_fromTxtFldSrc)

        # tFld_key Tgt
        getTxt_fromTxtFldTgt = cmds.textField(self.cTxtFld_A_target, q = True, text = True)
        setOptionVarCmd(self.optionVar02_tFld_key, getTxt_fromTxtFldTgt)

        message('Save Settings')
        print(getTxt_fromTxtFldSrc, getTxt_fromTxtFldTgt)

    # Reload 実行 関数
    def cM_editMenuReloadCmd(self, *args):
        u""" <Reload 実行 関数>
        """
        # 追加
        self.set_default_value_toOptionVar()  # UI-4. optionVar の value を default に戻す操作

        cmds.evalDeferred(lambda *args: self.showUI())  # refresh UI <---- ここ重要!!
        message('reload UI done')

    # Close 実行 関数
    def cM_editMenuCloseCmd(self, *args):
        u""" <close menu>
        """
        message('close UI done')
        self.cM_editMenuSaveCmd()  # 追加
        cmds.evalDeferred(lambda *args: cmds.deleteUI(self.win))

    # Help 実行 関数
    def cM_helpMenuCmd(self, *args):
        u""" <help menu>
        """
        help(__name__)
        message('see your script editor, detail information....')
    # 1. UI-1. メニュー コマンド群 ######################################################## end

    # 4. UI-4. OptionVar を利用したパラメータ管理 コマンド群 ############################## start
    # 追加
    # UI-4. optionVar からの値の復元 実行 関数
    def restoreOptionVarCmd(self, *args):
        u""" < UI-4. optionVar からの値の復元 実行 関数 です >

        ::

          追加
        """
        # tFld_key_Src
        # self.cmnTxtFld_A1.setText(self.options[self.optionVar01_tFld_key])
        tFld_key_Src = getOptionVarCmd(self.optionVar01_tFld_key)  # type: str
        cmds.textField(self.cTxtFld_A_source, edit = True, text = tFld_key_Src)
        # button のステータスも加味
        if len(tFld_key_Src):
            # UI 更新
            cmds.button('cBtn_A1_sourceSet', e = True, enable = False)
            cmds.button('cBtn_A1_selectSet', e = True, enable = True)
            cmds.button("cBtn_A1_clearSet", e = True, enable = True)

        # tFld_key_Tgt
        # self.cmnTxtFld_B1.setText(self.options[self.optionVar02_tFld_key])
        tFld_key_Tgt = getOptionVarCmd(self.optionVar02_tFld_key)  # type: str
        cmds.textField(self.cTxtFld_A_target, edit = True, text = tFld_key_Tgt)
        # button のステータスも加味
        if len(tFld_key_Tgt):
            # UI 更新
            cmds.button('cBtn_A2_targetSet', e = True, enable = False)
            cmds.button('cBtn_A2_selectSet', e = True,  enable = True)
            cmds.button("cBtn_A2_clearSet", e = True, enable = True)

        message(args[0])  # message output
        print(tFld_key_Src, tFld_key_Tgt)

    # 追加
    # UI-4. optionVar の value を default に戻す操作 関数
    def set_default_value_toOptionVar(self):
        u""" < UI-4. optionVar の value を default に戻す操作 関数 です >

        ::

          追加
          self.opVar_dictVal_dflt_list = ['', '']  # list of str range2
        """
        setOptionVarCmd(self.optionVar01_tFld_key, self.opVar_dictVal_dflt_list[0])  # ''
        setOptionVarCmd(self.optionVar02_tFld_key, self.opVar_dictVal_dflt_list[1])  # ''
    # 4. UI-4. OptionVar を利用したパラメータ管理 コマンド群 ################################ end

    # 2. UI-2. 追加オプション コマンド群 ################################################# start
    # source ############################################################# start
    # UI A option -set source-
    def ui_cBtn_A1_setSource_exe(self, *args):
        u""" <UI A option -set source->
        """
        selNodes = commonCheckSelection()
        if len(selNodes):
            # UI 更新
            cmds.button('cBtn_A1_sourceSet', e = True, enable = False)
            cmds.button("cBtn_A1_clearSet", e = True, enable = True)
            selNode = selNodes[0]
            cmds.textField('cTxtFld_A_source', e = True, tx = selNode)
            cmds.button('cBtn_A1_selectSet', e = True,  enable = True)
            cmds.button('cBtn_A3_32_source', e = True, l = u'{}\n: 階層側'.format(selNode))

    # UI A option -selectSet source-
    def ui_cBtn_A1_selectSet_exe(self, *args):
        u""" <UI A option -selectSet source->
        """
        text = cmds.textField('cTxtFld_A_source', q = True, tx = True)
        if text:
            cmds.select(text, r = True)

    # UI A option -setClear -
    def ui_cBtn_A1_setSourceClear_exe(self, *args):
        u""" <UI A option -setClear ->
        """
        # UI 更新
        cmds.button('cBtn_A1_sourceSet', e = True, enable = True)
        cmds.button("cBtn_A1_clearSet", e = True, enable = False)
        cmds.textField('cTxtFld_A_source', e = True, tx = self.NODES_A1)
        cmds.button('cBtn_A3_32_source', e = True, l = self.text_A3_32_source)
    # source ############################################################### end

    # target ############################################################# start
    # UI A option -set target-
    def ui_cBtn_A2_setTarget_exe(self, *args):
        u""" <UI A option -set target->
        """
        selNodes = commonCheckSelection()
        if len(selNodes):
            # UI 更新
            cmds.button('cBtn_A2_targetSet', e = True, enable = False)
            cmds.button("cBtn_A2_clearSet", e = True, enable = True)
            selNode = selNodes[0]
            cmds.textField('cTxtFld_A_target', e = True, tx = selNode)
            cmds.button('cBtn_A2_selectSet', e = True,  enable = True)
            cmds.button('cBtn_A3_32_target', e = True, l = u'{}\n: 階層側'.format(selNode))

    # UI A option -selectSet target-
    def ui_cBtn_A2_selectSet_exe(self, *args):
        u""" <UI A option -selectSet target->
        """
        text = cmds.textField('cTxtFld_A_target', q = True, tx = True)
        if text:
            cmds.select(text, r = True)

    # UI A option -setClear target-
    def ui_cBtn_A2_setTargetClear_exe(self, *args):
        u""" <UI A option -setClear target->
        """
        # UI 更新
        cmds.button('cBtn_A2_targetSet', e = True, enable = True)
        cmds.button("cBtn_A2_clearSet", e = True, enable = False)
        cmds.textField('cTxtFld_A_target', e = True, tx = self.NODES_A2)
        cmds.button('cBtn_A3_32_target', e = True, l = self.text_A3_32_target)
    # target ############################################################### end

    # 一時的に ui A3_1 inPutNode の rx ry rz の初期値を出力しておく関数
    def ui_A3_inPutNode_init_para_outPut_exe(self, *args):
        u""" < 一時的に ui A3_1 inPutNode の rx ry rz の初期値を出力しておく関数 です。>
        #######################

        #.
            :return parameters_R:
            :rtype: list of string

        #######################
        """
        inPutNode = cmds.button('cBtn_A3_inPutNode', q = True, l = True)
        parameters_R = []
        for ax in list('XYZ'):
            param = cmds.getAttr(inPutNode, '{}.rotate{}'.format(inPutNode, ax))
            parameters_R.append(param)
        return parameters_R

    # UI A3_1 option -最終の outPut node の選択-
    def ui_cBtn_A3_outPutNode_select_exe(self, *args):
        u""" <UI A3_1 option -最終の outPut node の選択->
        """
        outPutNode = cmds.button('cBtn_A3_outPutNode', q = True, l = True)
        cmds.select(outPutNode, r = True)
        self.OUTPUT_A = outPutNode

    # UI A3_1 option -最終の inPut node の選択-
    def ui_cBtn_A3_inPutNode_select_exe(self, *args):
        u""" <UI A3_1 option -最終の inPut node の選択->
        """
        inPutNode = cmds.button('cBtn_A3_inPutNode', q = True, l = True)
        cmds.select(inPutNode, r = True)
        self.INPUT_A = inPutNode

    # ui A3_1 新規作成された outPutNode と inPutNode のコネクションのトグルを行う
    # (rotate 限定)
    # 特定な3つのボタンステイタスに利用
    def ui_cBtn_A3_oP2iP_cnctTgl_exe(self, *args):
        u""" <特定な3つのボタンステイタスに利用>

        ::

          ui A3_1 新規作成された outPutNode と inPutNode のコネクションのトグルを行います
          (rotate 限定)
        """
        outPutNode = cmds.button('cBtn_A3_outPutNode', q = True, l = True)
        inPutNode = cmds.button('cBtn_A3_inPutNode', q = True, l = True)
        chkSorcRotPlugs = []
        for ax in list('XYZ'):
            # inPutNode 自分自身へ入力されてくる、ソース元をリストする(rot のみ！)
            plug = cmds.listConnections('{}.rotate{}'.format(inPutNode, ax)
                                        , c = False
                                        , s = True, d = False, p = True
                                        )
            chkSorcRotPlugs.append(plug)
        # print(chkSorcRotPlugs)

        om.MGlobal.displayWarning(u'新規で作成されたノードである以下、'
                                  u'\n\t{}\n'
                                  u'は未だ残ったままです。ご注意ください。'.format(self.newNodesAll)
                                  )

        if chkSorcRotPlugs == [None, None, None]:
            # UI 更新
            cmds.button('cBtn_A3_oP2iP_connectTgl'
                        , e = True
                        , l = 'connect\n-->>'
                        , bgc = self.bgcRed
                        )
            cmds.connectAttr("{}.outputRotateX".format(outPutNode)
                             , "{}.rotateX".format(inPutNode)
                             , f = True
                             )
            cmds.connectAttr("{}.outputRotateY".format(outPutNode)
                             , "{}.rotateY".format(inPutNode)
                             , f = True
                             )
            cmds.connectAttr("{}.outputRotateZ".format(outPutNode)
                             , "{}.rotateZ".format(inPutNode)
                             , f = True
                             )
            self.ui_cBtn_specific_state[0] = 1  # 特定な3つのボタンステイタス list of bool [1, *, *] へ更新
            om.MGlobal.displayInfo(u'確認: R only, connect を確認しています。')
        elif len(chkSorcRotPlugs):
            # UI 更新
            cmds.button('cBtn_A3_oP2iP_connectTgl', e = True, l = 'undo\ndisconnect'
                        , bgc = self.bgcBlue
                        )
            # print(self.INPUT_R_GETATTR)
            cmds.disconnectAttr("{}.outputRotateX".format(outPutNode)
                                , "{}.rotateX".format(inPutNode)
                                )
            cmds.setAttr("{}.rotateX".format(inPutNode), self.INPUT_R_GETATTR[0])
            cmds.disconnectAttr("{}.outputRotateY".format(outPutNode)
                                , "{}.rotateY".format(inPutNode)
                                )
            cmds.setAttr("{}.rotateY".format(inPutNode), self.INPUT_R_GETATTR[1])
            cmds.disconnectAttr("{}.outputRotateZ".format(outPutNode)
                                , "{}.rotateZ".format(inPutNode)
                                )
            cmds.setAttr("{}.rotateZ".format(inPutNode), self.INPUT_R_GETATTR[2])
            self.ui_cBtn_specific_state[0] = 0  # 特定な3つのボタンステイタス list of bool [0, *, *] へ更新
            om.MGlobal.displayInfo(u'確認: R only, disConnect を確認しています。')
        # print(self.ui_cBtn_specific_state)
        self.ui_cBtn_specific_state_check()  # 特定な3つのボタンステイタスをチェックする関数 実行

    # 一時的に ui A3_2 inPutNode の
    # tx ty tz, sx sy sz, shxy shxz shyz の初期値を出力しておく関数
    def ui_A3_2_inPutNode_init_para_outPut_exe(self, *args):
        u""" <一時的に ui A3_1 inPutNode の rx ry rz の初期値を出力しておく関数 です>

        #############

        #.
            :return: parameters_T, parameters_S, parameters_Sh
            :rtype: tuple[list[str], list[str], list[str]]
                          [Translate], [Scale], [Shear]
                          tx ty tz,    sx sy sz, shxy shxz shyz

        #############

        """
        A3_2_inPutNode = cmds.button('cBtn_A323_inPutNode', q = True, l = True)
        parameters_T = []
        for ax in list('XYZ'):
            param = cmds.getAttr(A3_2_inPutNode
                                 , '{}.translate{}'.format(A3_2_inPutNode, ax)
                                 )
            parameters_T.append(param)
        parameters_S = []
        for ax in list('XYZ'):
            param = cmds.getAttr(A3_2_inPutNode
                                 , '{}.scale{}'.format(A3_2_inPutNode, ax)
                                 )
            parameters_S.append(param)
        parameters_Sh = []
        for ax in ['XY', 'XZ', 'YZ']:
            param = cmds.getAttr(A3_2_inPutNode
                                 , '{}.shear{}'.format(A3_2_inPutNode, ax)
                                 )
            parameters_Sh.append(param)
        return parameters_T, parameters_S, parameters_Sh

    # UI A3_2 option -最終の outPut node の選択-
    def ui_cBtn_A321_outPutNode_select_exe(self, *args):
        u""" <UI A3_2 option -最終の outPut node の選択->
        """
        A3_2_outPutNode = cmds.button('cBtn_A321_outPutNode', q = True, l = True)
        cmds.select(A3_2_outPutNode, r = True)
        self.OUTPUT_A32 = A3_2_outPutNode

    # UI A3_2 option -最終の inPut node の選択-
    def ui_cBtn_A323_inPutNode_select_exe(self, *args):
        u""" <UI A3_2 option -最終の inPut node の選択->
        """
        A3_2_inPutNode = cmds.button('cBtn_A323_inPutNode', q = True, l = True)
        cmds.select(A3_2_inPutNode, r = True)
        self.INPUT_A32 = A3_2_inPutNode

    # ui A3_2 新規作成された outPutNode と inPutNode のコネクションのトグルを行う
    # (Translate, Scale, Shear 限定)
    # 特定な3つのボタンステイタスに利用
    def ui_cBtn_A32_atOnce_oP2iP_connectTgl_exe(self, *args):
        u""" <特定な3つのボタンステイタスに利用>

        ::

          ui A3_2 新規作成された outPutNode と inPutNode のコネクションのトグルを行います
          (Translate, Scale, Shear 限定)
        """
        outPutNode = cmds.button('cBtn_A321_outPutNode', q = True, l = True)
        inPutNode = cmds.button('cBtn_A323_inPutNode', q = True, l = True)
        chkSorcTSShPlugs = []
        for ax in list('XYZ'):
            # inPutNode 自分自身へ入力されてくる、ソース元をリストする(trans のみ！)
            plug = cmds.listConnections('{}.translate{}'.format(inPutNode, ax)
                                        , c = False
                                        , s = True, d = False, p = True
                                        )
            chkSorcTSShPlugs.append(plug)
        for ax in list('XYZ'):
            # inPutNode 自分自身へ入力されてくる、ソース元をリストする(scale のみ！)
            plug = cmds.listConnections('{}.scale{}'.format(inPutNode, ax)
                                        , c = False
                                        , s = True, d = False, p = True
                                        )
            chkSorcTSShPlugs.append(plug)
        for ax in ['XY', 'XZ', 'YZ']:
            # inPutNode 自分自身へ入力されてくる、ソース元をリストする(shear のみ！)
            plug = cmds.listConnections('{}.shear{}'.format(inPutNode, ax)
                                        , c = False
                                        , s = True, d = False, p = True
                                        )
            chkSorcTSShPlugs.append(plug)
        # print(chkSorcTSShPlugs)

        om.MGlobal.displayWarning(u'新規で作成されたノードである以下、'
                                  u'\n\t{}\n'
                                  u'は未だ残ったままです。ご注意ください。'.format(self.newNodesAll)
                                  )

        if chkSorcTSShPlugs == [None, None, None, None, None, None, None, None, None]:
            cmds.button('cBtn_A32_atOnce_oP2iP_connectTgl', e = True, l = 'connect\n-->>'
                        , bgc = self.bgcRed
                        )
            for ax in list('XYZ'):
                cmds.connectAttr("{}.outputTranslate{}".format(outPutNode, ax)
                                 , "{}.translate{}".format(inPutNode, ax)
                                 , f = True
                                 )
            for ax in list('XYZ'):
                cmds.connectAttr("{}.outputScale{}".format(outPutNode, ax)
                                 , "{}.scale{}".format(inPutNode, ax)
                                 , f = True
                                 )
            for ax1, ax2 in zip(['X', 'Y', 'Z'], ['XY', 'XZ', 'YZ']):
                cmds.connectAttr("{}.outputShear{}".format(outPutNode, ax1)
                                 , "{}.shear{}".format(inPutNode, ax2)
                                 , f = True
                                 )
            self.ui_cBtn_specific_state[1] = 1  # 特定な3つのボタンステイタス list of bool [*, 1, *] へ更新
            om.MGlobal.displayInfo(u'確認: T, S, Shear only, connect を確認しています。')
        elif len(chkSorcTSShPlugs):
            cmds.button('cBtn_A32_atOnce_oP2iP_connectTgl', e = True, l = 'undo\ndisconnect'
                        , bgc = self.bgcBlue
                        )
            # print(self.INPUT_T_GETATTR)
            # print(self.INPUT_S_GETATTR)
            # print(self.INPUT_Sh_GETATTR)
            for ax, count in zip(list('XYZ'), self.INPUT_T_GETATTR):
                # print(ax, num)
                cmds.disconnectAttr("{}.outputTranslate{}".format(outPutNode, ax)
                                    , "{}.translate{}".format(inPutNode, ax)
                                    )
                cmds.setAttr("{}.translate{}".format(inPutNode, ax), count)
            for ax, count in zip(list('XYZ'), self.INPUT_S_GETATTR):
                # print(ax, num)
                cmds.disconnectAttr("{}.outputScale{}".format(outPutNode, ax)
                                    , "{}.scale{}".format(inPutNode, ax)
                                    )
                cmds.setAttr("{}.scale{}".format(inPutNode, ax), count)
            for ax1, ax2, count in zip(['X', 'Y', 'Z'], ['XY', 'XZ', 'YZ'], self.INPUT_Sh_GETATTR):
                # print(ax, num)
                cmds.disconnectAttr("{}.outputShear{}".format(outPutNode, ax1)
                                    , "{}.shear{}".format(inPutNode, ax2)
                                    )
                cmds.setAttr("{}.shear{}".format(inPutNode, ax2), count)
            self.ui_cBtn_specific_state[1] = 0  # 特定な3つのボタンステイタス list of bool [*, 0, *] へ更新
            om.MGlobal.displayInfo(u'確認: T, S, Shear only, disConnect を確認しています。')
        # print(self.ui_cBtn_specific_state)
        self.ui_cBtn_specific_state_check()  # 特定な3つのボタンステイタスをチェックする関数 実行

    # UI A3_33 option -新規作成された multMatrix node の選択-
    def ui_cBtn_A3_33_mM_select_exe(self, *args):
        u""" <UI A3_33 option -新規作成された multMatrix node の選択->
        """
        cmds.select(self.mM, r = True)

    def check_attribute_isConnected(self, node, attr):
        connections = cmds.listConnections(node + '.' + attr
                                           , source = True, destination = True
                                           , plugs = True
                                           )
        connections_list = []

        if connections:
            # print("Connections found for {}.{}:".format(node, attr))
            for connection in connections:
                connections_list.append(connection)
        else:
            # print("No connections found for {}.{}.".format(node, attr))
            pass

        count = len(connections_list)
        if count == 2:
            return True
        else:
            return False

    # UI A3_3 source, target 階層側 と multMatrix のコネクションのトグルを行う
    # (matrix 限定)at once 版
    # 特定な3つのボタンステイタスに利用
    def ui_cBtn_A3_32_1_3_atOnce_oP2iP_connectTgl_exe(self, *args):
        u""" <特定な3つのボタンステイタスに利用>

        ::

          source, target 階層側 と multMatrix のコネクションのトグルを行います
          (matrix 限定)at once 版
        """
        src = self.src
        tgt = self.tgt
        mM = self.mM
        self.srcP = cmds.listRelatives(src, p = True)[0]
        srcP = self.srcP
        self.followHierarchy_isConnected_ToF = cmds.isConnected('{}.matrix'.format(srcP)
                                                                , '{}.matrixIn[2]'.format(mM)
                                                                )
        # multMatrix の matrixIn[2] をトリガーとしています
        ToF = self.followHierarchy_isConnected_ToF
        # print(ToF)

        attribute_channel_list = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz'
            , 'shxy', 'shxz', 'shyz']
        isConnected_list = []
        for axis in attribute_channel_list:
            isConnected = self.check_attribute_isConnected(tgt, axis)
            isConnected_list.append(isConnected)
        # print(isConnected_list)
        isConnected = True in isConnected_list
        # print(isConnected)

        # 追加
        # R 確認ボタンと、TSShear 確認ボタン のカレント状態をチェックすることがトリガーとなります
        # from range 3 [0, 0, 0] to range 2 [0, 0]
        ui_cBtn_specific_state_tmp = self.ui_cBtn_specific_state[:-1]
        # print(1 in ui_cBtn_specific_state_tmp)

        if ToF:
            # 追加
            if True in ui_cBtn_specific_state_tmp:  # 確認ボタンが1つでも実行中ならばストップ
                om.MGlobal.displayWarning(u'R, T, S, Shear が接続されたままです。切断はキャンセルしました。'
                                          u'ご確認ください。'
                                          )
                om.MGlobal.displayWarning(u'新規で作成されたノードである以下、'
                                          u'\n\t{}\n'
                                          u'は未だ残ったままです。ご注意ください。'.format(self.newNodesAll)
                                          )
                pass
            else:
                print(u'change at once: disconnected')
                cmds.text('cTxt_A3_31_3_text', e = True, bgc = self.bgcBlue)
                cmds.button('cBtn_A3_32_1_3_atOnce_oP2iP_connectTgl', e = True
                            , l = 'undo\ndisconnect', bgc = self.bgcBlue
                            )
                cmds.button('cBtn_A3_32_source', e = True, bgc = self.bgcBlue)
                cmds.button('cBtn_A3_32_target', e = True, bgc = self.bgcBlue)
                # cmds.disconnectAttr('{}.matrix'.format(srcP), '{}.matrixIn[2]'.format(self.mM))
                self.ui_cBtn_specific_state[2] = 0  # 特定な3つのボタンステイタス list of bool [*, *, 0] へ更新

                cmds.select(src, tgt, r = True)
                # print('mode = 0')
                self.main_followTheHierarchyAndTglConnection_exe()  # 階層をたどり、接続の有無まで行う、main 関数
                # print(self.ui_cBtn_specific_state)
                om.MGlobal.displayWarning(u'新規で作成されたノードである以下、'
                                          u'\n\t{}\n'
                                          u'は未だ残ったままです。ご注意ください。'.format(self.newNodesAll)
                                          )
                om.MGlobal.displayInfo(u'確認: matrix, disConnectを確認しています。')
        else:
            print(u'change at once: connected')
            cmds.text('cTxt_A3_31_3_text', e = True, bgc = self.bgcRed)
            cmds.button('cBtn_A3_32_1_3_atOnce_oP2iP_connectTgl', e = True
                        , l = 'connect\n-->>', bgc = self.bgcRed
                        )
            cmds.button('cBtn_A3_32_source', e = True, bgc = self.bgcRed)
            cmds.button('cBtn_A3_32_target', e = True, bgc = self.bgcRed)
            # cmds.connectAttr('{}.matrix'.format(srcP), '{}.matrixIn[2]'.format(mM), f = True)
            self.ui_cBtn_specific_state[2] = 1  # 特定な3つのボタンステイタス list of bool [*, *, 1] へ更新

            cmds.select(src, tgt, r = True)
            # print('mode = 0')
            self.main_followTheHierarchyAndTglConnection_exe()  # 階層をたどり、接続の有無まで行う、main 関数
            # print(self.ui_cBtn_specific_state)
            om.MGlobal.displayWarning(u'新規で作成されたノードである以下、'
                                      u'\n\t{}\n'
                                      u'は未だ残ったままです。ご注意ください。'.format(self.newNodesAll)
                                      )
            om.MGlobal.displayInfo(u'確認: matrix, connect を確認しています。')
        self.ui_cBtn_specific_state_check()  # 特定な3つのボタンステイタスをチェックする関数 実行

    # UI A option -selects all new nodes-
    def ui_cBtn_A_selAllNwNds_exe(self, *args):
        u""" <UI A option -selects all new nodes->
        """
        cmds.select(self.newNodesAll, r = True)
        om.MGlobal.displayInfo(u'現在選択されているノードは、全て新規で作成されたノードです。'
                               u'ご確認ください。'
                               )

    # UI A option -inputs memory clear all-
    def ui_cBtn_A_allClear_exe(self, *args):
        u""" <UI A option -inputs memory clear all->
        """
        # UI 更新
        cmds.textField('cTxtFld_A_source', e = True, tx = self.NODES_A1)
        cmds.textField('cTxtFld_A_target', e = True, tx = self.NODES_A2)

        cmds.button('cBtn_A1_sourceSet', e = True, enable = True)
        cmds.button('cBtn_A1_clearSet', e = True, enable = False)
        cmds.button('cBtn_A1_selectSet', e = True, enable = False)
        cmds.button('cBtn_A2_targetSet', e = True, enable = True)
        cmds.button('cBtn_A2_clearSet', e = True, enable = False)
        cmds.button('cBtn_A2_selectSet', e = True, enable = False)

        cmds.button('cBtn_A_exe', e = True, enable = True)

        cmds.frameLayout('cFrmLyut_A3', e = True, enable = False)

        cmds.button('cBtn_A3_oP2iP_connectTgl', e = True, l = 'R', bgc = self.bgc)
        cmds.button('cBtn_A32_T_oP2iP_connectTgl', e = True, l = 'T', bgc = self.bgc)
        cmds.button('cBtn_A32_S_oP2iP_connectTgl', e = True, l = 'S', bgc = self.bgc)
        cmds.button('cBtn_A32_Sh_oP2iP_connectTgl', e = True, l = 'Shear', bgc = self.bgc)
        cmds.button('cBtn_A32_atOnce_oP2iP_connectTgl', e = True, l = 'at once', bgc = self.bgc)

        cmds.text('cTxt_A3_31_3_text', e = True, bgc = self.bgc2)

        cmds.button('cBtn_A3_32_source', e = True, l = self.text_A3_32_source, bgc = self.bgc)
        cmds.button('cBtn_A3_32_target', e = True, l = self.text_A3_32_target, bgc = self.bgc)
        cmds.button('cBtn_A3_32_1_3_atOnce_oP2iP_connectTgl', e = True, l = 'at once', bgc = self.bgc)

        cmds.button('cBtn_A_selAllNwNds', e = True, bgc = self.bgc)
        cmds.button('cBtn_A_allClear', e = True, bgc = self.bgc)

        # print(self.newNodesAll)
        cmds.delete(self.newNodesAll)

        om.MGlobal.displayInfo(u'必要とされていた以下のノード'
                               u'\n\t{}\n'
                               u'も完全に削除済です。'.format(self.newNodesAll)
                               )

        # 追加
        # self.tgt に追加登録済である initAttr の完全な削除
        self.delInitAttr(self.tgt)

        self.__init__()  # すべて、元の初期値に戻す
        om.MGlobal.displayInfo(u'メモリーをすべてクリアーしました。')
        # print(self.INPUT_R_GETATTR)
        # print(self.INPUT_T_GETATTR)
        # print(self.INPUT_S_GETATTR)
        # print(self.INPUT_Sh_GETATTR)

    # 特定ボタンの on/off 判定に使用
    # UI button である、
    # R, at once(T,S,Sher), at once(matrix index)
    # 以上、3つのボタンステイタスをチェックする関数
    def ui_cBtn_specific_state_check(self):
        u""" <特定な3つのボタンステイタスをチェックする関数 です>

        ::

          特定ボタンの on/off 判定に使用
          UI button である、
            R:                     'cBtn_A3_oP2iP_connectTgl'
            at once(T,S,Sher):     'cBtn_A32_atOnce_oP2iP_connectTgl'
            at once(matrix index): 'cBtn_A3_32_1_3_atOnce_oP2iP_connectTgl'
          以上、
            常に特定な3つのボタンステイタスをチェックして、
                button('cBtn_A_allDone') をコントロールします。
        """
        if self.ui_cBtn_specific_state == [1, 1, 1]:  # 特定な3つのボタンステイタス list of bool
            cmds.button('cBtn_A_allDone', e = True, enable = True, bgc = self.bgcBlue3)
        else:
            cmds.button('cBtn_A_allDone', e = True, enable = False, bgc = self.bgc)

    # UI A option -all done and inputs memory clear-
    def ui_cBtn_A_allDone_exe(self, *args):
        u""" <UI A option -all done and inputs memory clear->
        """
        # UI 更新
        cmds.textField('cTxtFld_A_source', e = True, tx = self.NODES_A1)
        cmds.textField('cTxtFld_A_target', e = True, tx = self.NODES_A2)

        cmds.button('cBtn_A1_sourceSet', e = True, enable = True)
        cmds.button('cBtn_A1_clearSet', e = True, enable = False)
        cmds.button('cBtn_A1_selectSet', e = True, enable = False)
        cmds.button('cBtn_A2_targetSet', e = True, enable = True)
        cmds.button('cBtn_A2_clearSet', e = True, enable = False)
        cmds.button('cBtn_A2_selectSet', e = True, enable = False)

        cmds.button('cBtn_A_exe', e = True, enable = True)

        cmds.frameLayout('cFrmLyut_A3', e = True, enable = False)

        cmds.button('cBtn_A3_oP2iP_connectTgl', e = True, l = 'R', bgc = self.bgc)
        cmds.button('cBtn_A32_T_oP2iP_connectTgl', e = True, l = 'T', bgc = self.bgc)
        cmds.button('cBtn_A32_S_oP2iP_connectTgl', e = True, l = 'S', bgc = self.bgc)
        cmds.button('cBtn_A32_Sh_oP2iP_connectTgl', e = True, l = 'Shear',
                    bgc = self.bgc)
        cmds.button('cBtn_A32_atOnce_oP2iP_connectTgl', e = True, l = 'at once',
                    bgc = self.bgc)

        cmds.text('cTxt_A3_31_3_text', e = True, bgc = self.bgc2)

        cmds.button('cBtn_A3_32_source', e = True, l = self.text_A3_32_source,
                    bgc = self.bgc)
        cmds.button('cBtn_A3_32_target', e = True, l = self.text_A3_32_target,
                    bgc = self.bgc)
        cmds.button('cBtn_A3_32_1_3_atOnce_oP2iP_connectTgl', e = True, l = 'at once',
                    bgc = self.bgc)

        cmds.button('cBtn_A_selAllNwNds', e = True, bgc = self.bgc)
        cmds.button('cBtn_A_allClear', e = True, bgc = self.bgc)
        cmds.button('cBtn_A_allDone', e = True, bgc = self.bgc)

        # print(self.newNodesAll)
        # cmds.delete(self.newNodesAll)

        self.__init__()  # すべて、元の初期値に戻す
        om.MGlobal.displayInfo(u'メモリーをすべてクリアーしました。')
        print(self.INPUT_R_GETATTR)
        print(self.INPUT_T_GETATTR)
        print(self.INPUT_S_GETATTR)
        print(self.INPUT_Sh_GETATTR)
    # 2. UI-2. 追加オプション コマンド群 ################################################### end

    # その他 アルゴリズムとなる コマンド群 ################################################# start
    # 命名規則のコントロール ################################################ start
    # under bar 3 or 2 version
    def nodeName_decomp_exeB(self, nodes):
        u""" <under bar 3 or 2 version>

        #############

        #.
            :param str nodes:

        #.
            :return: strsCompLists
            :rtype: list[str]

        #############
        """
        patternB = re.compile(
            r'(?P<match1>.*)_(?P<match2>.*)_(?P<match3>.*)|(?P<match4>.*)_(?P<match5>.*)')
        iterator = patternB.finditer(nodes)
        for itr in iterator:
            # パターンヒットを辞書として出力
            ptnB_dict = itr.groupdict()
            # print(ptnB_dict)
            for ptnBNumber_keys, ptnBFindStrs_values in ptnB_dict.items():
                # print(ptnBNumber_keys, ptnBFindStrs_values)
                if ptnBFindStrs_values is None:
                    # value が None の keys のみを辞書から削除
                    ptnB_dict.pop(ptnBNumber_keys)
            # print(ptnB_dict)
            # 余計なものを省いた最終辞書を, ちゃんと綺麗にソートしたいが,
            # 辞書はソートできないので keys でソートする。するとタプルになってしまう。
            ptnB_tuple = sorted(ptnB_dict.items())
            # print(ptnB_tuple)
            strsCompLists = []
            for ptnB in ptnB_tuple:
                # タプルの各要素の内,欲しいのは index[1] なので,
                # 新規リストへ index[1] のみを順次格納する。
                # print(ptn[1])
                strsCompLists.append(ptnB[1])
            return strsCompLists

    # no under bar version
    def nodeName_decomp_exeC(self, nodes):
        u""" < no under bar version >

        #############

        #.
            :param str nodes:

        #.
            :return: strsCompLists
            :rtype: list[str]

        #############
        """
        patternC = re.compile(r'(?P<match6>.*)')
        iterator = patternC.finditer(nodes)
        for itr in iterator:
            # パターンヒットを辞書として出力
            ptnC_dict = itr.groupdict()
            # print(ptnC_dict)
            for ptnCNumber_keys, ptnCFindStrs_values in ptnC_dict.items():
                # print(ptnCNumber_keys, ptnCFindStrs_values)
                if ptnCFindStrs_values is None:
                    # value が None の keys のみを辞書から削除
                    ptnC_dict.pop(ptnCNumber_keys)
            # print(ptnC_dict)
            # 余計なものを省いた最終辞書を, ちゃんと綺麗にソートしたいが,
            # 辞書はソートできないので keys でソートする。するとタプルになってしまう。
            ptnC_tuple = sorted(ptnC_dict.items())
            # print(ptnC_tuple)
            strsCompLists = []
            for ptnC in ptnC_tuple:
                # タプルの各要素の内,欲しいのは index[1] なので,
                # 新規リストへ index[1] のみを順次格納する。
                # print(ptn[1])
                strsCompLists.append(ptnC[1])
            return strsCompLists

    # strCompLists のカウント数に応じたネーミングの振り分け
    def strCompLists_count_caseDividing_exe(self, strsCompLists = None
                                            , utilNodeShortNameSet = '***'
                                            ):
        u""" < strCompLists のカウント数に応じたネーミングの振り分け>

        #############

        #.
            :param list of str strsCompLists: ['', '', '']

        #.
            :param list of str utilNodeShortNameSet: '***'

        #############
        """
        if strsCompLists is None:
            strsCompLists = ['', '', '']

        if len(strsCompLists) == 3:
            # 変更1 大文字整形の復活
            utilNodeShortNameSet = utilNodeShortNameSet.title()  # 大文字整形
            utilNodeShortName = utilNodeShortNameSet.replace(' ', '')  # space削除
            # renameTool 発動
            # 変更1
            # DG命名を見直す
            # print('3')
            RT_Modl().exe(mode = 0
                          , n = [u'{}'.format(strsCompLists[0])
                    , u'{}{}@'.format(strsCompLists[1], utilNodeShortName)
                    , u''  # 変更 memo): old - > u'~'
                    , u''
                    , u'{}'.format(strsCompLists[2])
                                 ]
                          )
        elif len(strsCompLists) == 2:
            # print(strsCompLists)  # [u'spineA', u'L']
            # utilNodeShortNameSet = utilNodeShortNameSet.title()  # 大文字整形
            utilNodeShortName = utilNodeShortNameSet.replace(' ', '')  # space削除
            # print(utilNodeShortName)  # e.g.): u'multMtrx'
            # renameTool 発動
            # 変更1
            # DG命名を見直す
            # print('2')
            RT_Modl().exe(mode = 0
                          , n = [u'{}'.format(strsCompLists[0])
                    , u'{}@'.format(utilNodeShortName)
                                 # test 変更 memo): old - > u'{}{}@'.format(strsCompLists[1], utilNodeShortName
                    , u''  # test 変更 memo): old - > u'~'
                    , u''
                    , u'{}'.format(strsCompLists[1])
                                 ]
                          )
        elif len(strsCompLists) == 1:
            # 小文字整形(そのまま) + space削除のみ
            utilNodeShortName = utilNodeShortNameSet.replace(' ', '')
            # renameTool 発動
            # 変更1
            # DG命名を見直す
            # print('1')
            RT_Modl().exe(mode = 0
                          , n = [u'{}'.format(strsCompLists[0])
                    , u'{}@'.format(utilNodeShortName)
                    , u''  # 変更 memo): old - > u'~'
                    , u''
                    , u''
                                 ]
                          )

    # 命名規則のコントロール ################################################## end
    # その他 アルゴリズムとなる コマンド群 ################################################### end

    # 「main となる コマンド群」 ######################################################### start
    # main 1:
    # children A exe -新規のノード作成や、接続の準備を行う-
    def ui_Execute_A(self, *args):
        u""" <main 1:>

        ::

          children A exe
          -新規のノード作成や、接続の準備を行う-
        """
        self.src = cmds.textField('cTxtFld_A_source', q = True, tx = True)
        self.tgt = cmds.textField('cTxtFld_A_target', q = True, tx = True)
        src = self.src
        tgt = self.tgt
        print(src, tgt)
        # print(len(src), len(tgt))
        if len(src) and len(tgt):  # src, tgt 共に入力セッティングされていれば、実行
            print(u'source, target 共に set 入力されているため、継続実行しています。')
            strsCompLists = self.nodeName_decomp_exeB(src)  # under bar 3 or 2 version
            print('[exeB]' + 'strsCompLists: {}'.format(strsCompLists))

            if strsCompLists is None:
                strsCompLists = self.nodeName_decomp_exeC(src)  # no under bar version
                print('[exeC]' + 'strsCompLists: {}'.format(strsCompLists))

            print('[final]' + 'strsCompLists: {}'.format(strsCompLists))

            cmds.createNode('multMatrix')
            utilNodeShortNameSet = 'mult Mtrx'
            self.strCompLists_count_caseDividing_exe(strsCompLists
                                                     , utilNodeShortNameSet
                                                     )  # naming
            self.mM = cmds.ls(sl = True)[0]
            mM = self.mM

            cmds.createNode('decomposeMatrix')
            utilNodeShortNameSet = 'dcmp Mtrx'
            self.strCompLists_count_caseDividing_exe(strsCompLists
                                                     , utilNodeShortNameSet
                                                     )  # naming
            self.dM = cmds.ls(sl = True)[0]
            dM = self.dM

            nodeAll = [mM, dM]

            # 先ず接続
            cmds.connectAttr('{}.matrixSum'.format(mM), '{}.inputMatrix'.format(dM), force = True)

            # UI 更新
            cmds.button('cBtn_A1_clearSet', e = True, enable = False)
            cmds.button('cBtn_A2_clearSet', e = True, enable = False)
            cmds.button('cBtn_A_exe', e = True, enable = False)

            cmds.frameLayout('cFrmLyut_A3', e = True, enable = True)

            cmds.button('cBtn_A3_oP2iP_connectTgl', e = True, bgc = self.bgcBlue3)
            cmds.button('cBtn_A32_T_oP2iP_connectTgl', e = True, bgc = self.bgcBlue3)
            cmds.button('cBtn_A32_S_oP2iP_connectTgl', e = True, bgc = self.bgcBlue3)
            cmds.button('cBtn_A32_Sh_oP2iP_connectTgl', e = True, bgc = self.bgcBlue3)
            cmds.button('cBtn_A32_atOnce_oP2iP_connectTgl', e = True, bgc = self.bgcBlue3)

            cmds.button('cBtn_A3_32_1_3_atOnce_oP2iP_connectTgl', e = True, bgc = self.bgcBlue3)

            cmds.button('cBtn_A3_33_mM', e = True, l = mM)

            cmds.button('cBtn_A_selAllNwNds', e = True, bgc = self.bgcBlue3)
            cmds.button('cBtn_A_allClear', e = True, bgc = self.bgcBlue3)

            print(u'target の node type は {} で実行中。。\n'.format(cmds.nodeType(tgt)))

            if cmds.nodeType(tgt) == 'joint':  # tgt が joint の場合
                # 先ず, quatNodes系 plug-in の check
                # checkQuatNodePlugIn()

                # matrix を利用した parentConstraint を可能とするメイン関数
                dupTgt, newNodes = self.commonCommand(src, tgt, nodeAll)

                # print(dupTgt)

                cmds.createNode('eulerToQuat')
                utilNodeShortNameSet = 'elerTo Quat'
                self.strCompLists_count_caseDividing_exe(strsCompLists
                                                         , utilNodeShortNameSet
                                                         )  # naming
                eTQt = cmds.ls(sl = True)[0]
                cmds.connectAttr("{}.jointOrient".format(tgt)
                                 , "{}.inputRotate".format(eTQt)
                                 , f = True
                                 )
                newNodes.append(eTQt)

                cmds.createNode("quatInvert")
                utilNodeShortNameSet = 'quat Invt'
                self.strCompLists_count_caseDividing_exe(strsCompLists
                                                         , utilNodeShortNameSet
                                                         )  # naming
                qInv = cmds.ls(sl = True)[0]
                cmds.connectAttr("{}.outputQuat".format(eTQt)
                                 , "{}.inputQuat".format(qInv)
                                 , f = True
                                 )
                newNodes.append(qInv)

                cmds.createNode("quatProd")
                utilNodeShortNameSet = 'quat Prod'
                self.strCompLists_count_caseDividing_exe(strsCompLists
                                                         , utilNodeShortNameSet
                                                         )  # naming
                qPrd = cmds.ls(sl = True)[0]
                cmds.connectAttr("{}.outputQuat".format(qInv)
                                 , "{}.input2Quat".format(qPrd)
                                 , f = True
                                 )
                newNodes.append(qPrd)

                cmds.createNode("quatToEuler")
                utilNodeShortNameSet = 'quatTo Eler'
                self.strCompLists_count_caseDividing_exe(strsCompLists
                                                         , utilNodeShortNameSet
                                                         )  # naming
                qTEr = cmds.ls(sl = True)[0]
                cmds.connectAttr("{}.outputQuat".format(qPrd)
                                 , "{}.inputQuat".format(qTEr)
                                 , f = True
                                 )
                newNodes.append(qTEr)

                cmds.connectAttr("{}.outputQuat".format(dM)
                                 , "{}.input1Quat".format(qPrd)
                                 , f = True
                                 )

                # A3_1 outPut inPut button # UI 更新
                cmds.button('cBtn_A3_outPutNode', e = True, l = qTEr)
                cmds.button('cBtn_A3_inPutNode', e = True, l = tgt)

                # cmds.connectAttr("{}.outputRotateX".format(qTEr), "{}.rotateX".format(tgt), f = True)
                # cmds.connectAttr("{}.outputRotateY".format(qTEr), "{}.rotateY".format(tgt), f = True)
                # cmds.connectAttr("{}.outputRotateZ".format(qTEr), "{}.rotateZ".format(tgt), f = True)

                # A3_2 outPut inPut button # UI 更新
                cmds.button('cBtn_A321_outPutNode', e = True, l = dM, enable = True)
                cmds.button('cBtn_A323_inPutNode', e = True, l = tgt)

                # A3_1 A3_2 の input 側が同じノードなので、混乱を避ける目的で、表示を不可にしておく
                # cmds.button('cBtn_A321_outPutNode', e = True, enable = True)
                cmds.button('cBtn_A323_inPutNode', e = True, enable = False)

                cmds.setAttr('{}.visibility'.format(dupTgt), 0)
                # cmds.select(cl = True)
                # 複製しておいた dupTgt は余計なので削除
                cmds.delete(dupTgt)
                newNodes.remove(dupTgt)  # リストからも削除する

                # 全部選択
                print(u'\n新規で作成されたノードは以下、'
                      u'\n\t{}\n'
                      u'です。'.format(newNodes)
                      )
                cmds.select(newNodes, r = True)

                self.newNodesAll = newNodes

            else:  # tgt が joint 以外の場合
                # matrix を利用した parentConstraint を可能とするメイン関数
                dupTgt, nodeAll = self.commonCommand(src, tgt, nodeAll)

                # print(dupTgt)

                # A3_1 outPut inPut button # UI 更新
                cmds.button('cBtn_A3_outPutNode', e = True, l = dM)
                cmds.button('cBtn_A3_inPutNode', e = True, l = tgt)

                # cmds.connectAttr("{}.outputRotateX".format(dM), "{}.rotateX".format(tgt), f = True)
                # cmds.connectAttr("{}.outputRotateY".format(dM), "{}.rotateY".format(tgt), f = True)
                # cmds.connectAttr("{}.outputRotateZ".format(dM), "{}.rotateZ".format(tgt), f = True)

                # A3_2 outPut inPut button # UI 更新
                cmds.button('cBtn_A321_outPutNode', e = True, l = dM)
                cmds.button('cBtn_A323_inPutNode', e = True, l = tgt)

                # A3_1 A3_2 が其々同じノードなので、混乱を避ける目的で、表示を不可にしておく
                cmds.button('cBtn_A321_outPutNode', e = True, enable = False)
                cmds.button('cBtn_A323_inPutNode', e = True, enable = False)

                cmds.setAttr('{}.visibility'.format(dupTgt), 0)
                # cmds.select(cl = True)
                # 複製しておいた dupTgt は余計なので削除
                cmds.delete(dupTgt)
                nodeAll.remove(dupTgt)  # リストからも削除する

                # 全部選択
                print(u'新規で作成されたノードは {} です。'.format(nodeAll))
                cmds.select(nodeAll, r = True)

                self.newNodesAll = nodeAll

            om.MGlobal.displayInfo(u'現在、新規で作成されたノードは、全て選択された状態です。'
                                   u'尚、現状は未だ準備段階です。ご注意願います。')

            # print('***' * 5)
            # print('{} has those initial parameters....'.format(tgt))
            # 一時的に ui A3 inPutNode の rx ry rz の初期値の出力関数 を利用して、
            # のちに再利用するため保存しておく。
            paras_R = self.ui_A3_inPutNode_init_para_outPut_exe()
            self.INPUT_R_GETATTR = paras_R
            # print('Rotate are    {}'.format(self.INPUT_R_GETATTR))
            # 一時的に ui A3 inPutNode の tx ty tz, sx sy sz, shxy shxz shyz
            # の初期値の出力関数 を利用して、
            # のちに再利用するため保存しておく。
            paras_T, paras_S, paras_Sh = self.ui_A3_2_inPutNode_init_para_outPut_exe()
            self.INPUT_T_GETATTR = paras_T
            # print('Translate are {}'.format(self.INPUT_T_GETATTR))
            # self.INPUT_S_GETATTR = paras_S
            # print('Scale are     {}'.format(self.INPUT_S_GETATTR))
            # self.INPUT_Sh_GETATTR = paras_Sh
            # print('Shear are     {}'.format(self.INPUT_Sh_GETATTR))
            # print('***' * 5)
        else:  # src, tgt 共に入力セッティングされていなければ、何もしない
            message_warning(u'source, target 共に set 入力されていないため、継続実行を中止しました。')
            pass

    # 新規作成された outPutNode と inPutNode コネクションに使用される関数 ####### start
    # matrix を利用した parentConstraint を可能とするメイン関数
    def commonCommand(self, src, tgt, nodeAll):
        u""" < matrix を利用した parentConstraint を可能とするメイン関数 です >

        ::

          新規作成された outPutNode と inPutNode コネクションに使用される関数

        #############

        #.
            :param str src:

        #.
            :param str tgt:

        #.
            :param list[str] nodeAll:

        #.
            :return: dupTgt, nodeAll
            :rtype: tuple[str, list[str]]

        #############
        """
        mM, dM = nodeAll
        # 福本氏のわかりやすい手法を参考にした。以下、手順。
        # ①ターゲットとなる、コントロールされる方を、一時的に複製し、コントローラへ子付けする。
        # ②先ず、複製したそのノードの matrix を、新規作成する multMatrix の
        # .matrixIn[0] へ setAttr する。
        # ③次に、本来のコントローラとなる、src matrix を、新規作成した multMatrix の
        # .matrixIn[1] へ connectAttr する。
        # note:②③を一気に行っておかないと、後工程がうまくいかない！！！
        # memo:.matrixIn[0] を setAttr して、何も接続せず、空けておくことがミソ！！
        # memo:複製した dupTgt は、用を成したので、最後は捨てても構わない！！

        # ①ターゲットとなる、コントロールされる方を、一時的に複製し、コントローラへ子付けする。
        dupTgt = cmds.duplicate(tgt)[0]
        cmds.parent(dupTgt, src)
        nodeAll.append(dupTgt)

        # ②先ず、複製したそのノードの matrix を、新規作成する multMatrix の
        # .matrixIn[0] へ setAttr する。
        srcMat = cmds.getAttr('{}.matrix'.format(dupTgt))
        # print(srcMat)
        cmds.setAttr('{}.matrixIn[0]'.format(mM), srcMat, type = 'matrix')

        # ③次に、本来のコントローラとなる、src matrix を、新規作成した multMatrix の
        # .matrixIn[1] へ connectAttr する。
        cmds.connectAttr('{}.matrix'.format(src), '{}.matrixIn[1]'.format(mM), force = True)

        return dupTgt, nodeAll
    # 新規作成された outPutNode と inPutNode コネクションに使用される関数 ######### end

    # main 2:
    # 階層をたどり、新規作成された multMatrix との接続の有無まで行う
    def main_followTheHierarchyAndTglConnection_exe(self):
        u""" <main 2:>

        ::

          階層をたどり、新規作成された multMatrix との接続の有無まで行う
        """
        # 階層をたどる
        selList = []
        selList = commonCheckSelection()
        print(selList)  # type : list of 'unicode'
        # print('\n')
        cmds.select(cl = True)
        pathList = []  # 一旦、お互いのパスをまとめる
        print('***' * 30 + u'調査の開始')
        if len(selList) == 0 or len(selList) == 1 or len(selList) >= 3:
            print(u'オブジェクトが2つ選択されていないか、もしくは3つ以上同時に選択されています。')
            print('***' * 20 + u'調査の中止！\n')
            pass
        elif len(selList) == 2:
            for sel in selList:
                print('***' * 20)
                print(sel)
                # print(type(sel))  # sel : <type 'unicode'>
                # print(type(DAGPath(sel)))  # DAGPath(sel) : <type 'OpenMaya.MDagPath'>
                parents = self.get_parents(self.DAGPath(sel))
                # print(type(parents))  # parents : <type 'list'>
                # print(parents)
                A = [c.fullPathName() for c in parents]

                # print(A)  # type : list of 'unicode'

                pathList.append(A)
                if len(A) > 0:
                    print(u'親は..')
                    print(A[-1])
                    print('***' * 20 + u'調査、完了\n')  # cmds.select(A[-1], r = True)
                elif len(A) == 0:
                    print(u'親が見当たりません。')
                    print('***' * 20 + u'調査、完了\n')

            # 互いのまとまったパスを比較する`
            # print(pathList)
            srcList = pathList[0]
            tgtList = pathList[1]

            # print('srcList :\n\t{}'.format(srcList))
            # print('tgtList :\n\t{}'.format(tgtList))

            srcList_copy = srcList

            # print(srcList_copy)

            tgtList_copy = tgtList

            # print(tgtList_copy)

            counter = 1
            print('\n' + '***' * 20)
            # popの繰り返しにより、どちらかのリスト要素が先に空になる可能性がある
            # つまり、階層構造が類似していない時を考慮して。。
            while srcList_copy != [] and tgtList_copy != []:  # どちらも空で無い限り繰り返す
                if srcList_copy[-1] == tgtList_copy[-1]:  # 最後のリスト要素 [-1] を比較

                    # print('***' * 5)
                    # print(u'{}巡目'.format(counter))
                    # print(u'{} \n\tと \n{} \n\tは、'.format(srcList_copy, tgtList_copy))
                    # print(u'最後のリスト要素 [-1] が一致しているため、当ツールでは互いの親が'
                    #       u'共通であると認識し、skip の対象と判断し、互いのリストから削除しました。'
                    #       )

                    print(u'次を調べます。')
                    srcList_copy.pop()
                    tgtList_copy.pop()
                    counter += 1
                    print('***' * 5 + '\n')
                else:

                    # print('***' * 5)
                    # print(u'{}巡目'.format(counter))
                    # print(u'{} \n\tと \n{} \n\tは、'.format(srcList_copy, tgtList_copy))
                    # print(u'最後のリスト要素 [-1] が一致していないので、当ツールでは互いの親が'
                    #       u'共通で無いと認識し、skip の対象と判断しました。'
                    #       )

                    print(u'調査を終了しました。A')
                    print('***' * 5)
                    break
            else:  # どちらかが空になったら抜ける

                # print('***' * 5)
                # print(u'{}巡目'.format(counter))
                # print(u'{} \n\tと \n{} \n\tは、'.format(srcList_copy, tgtList_copy))
                # print(u'最後のリスト要素 [-1] が一致していないので、当ツールでは互いの親が'
                #       u'共通で無いと認識し、skip の対象と判断しました。'
                #       )

                print(u'調査を終了しました。B')
                print('***' * 5)
            print('***' * 20)

            srcList_temp = srcList_copy
            tgtList_copy.reverse()
            tgtList_temp = tgtList_copy

            # print(srcList_temp)
            # print(tgtList_temp)

            # mM = cmds.createNode('multMatrix')
            mM = self.mM

            connected_counter = []

            # 階層をたどり終え、既に接続されているかの真偽で区別
            if self.followHierarchy_isConnected_ToF == 0:  # 未だ接続されていないので、接続
                # srcList_temp を階層下から順に接続
                for i, src in enumerate(srcList_temp, start = 2):
                    # .matrixIn[0] は必ず setAttr, .matrixIn[1] は必ず src と接続されている事
                    # を考慮して、start = 2.

                    # print(i, src)

                    ToF = cmds.connectionInfo('{}.matrixIn[{}]'.format(mM, i)
                                              , isDestination = True
                                              )  # .matrixIn[2] 番目から接続されているかどうか調べる
                    # print(ToF)
                    if ToF:
                        pass
                    else:
                        cmds.connectAttr('{}.matrix'.format(src)
                                         , '{}.matrixIn[{}]'.format(mM, i)
                                         , force = True
                                         )
                        connected_counter.append(i)
                # print(connected_counter)
                # print(connected_counter[-1])
                self.notYetConnected_counterStart = connected_counter[-1] + 1
                # print(self.notYetConnected_counterStart)

                # tgtList_temp を階層上から順に接続
                for i, tgt in enumerate(tgtList_temp
                        , start = self.notYetConnected_counterStart):
                    # src connect からの続き。 start = notYetConnected_counterStart からスタート。

                    # print(i, tgt)

                    ToF = cmds.connectionInfo('{}.matrixIn[{}]'.format(mM, i)
                                              , isDestination = True
                                              )
                    # .matrixIn[i] 番目から接続されているかどうか調べる
                    # print(ToF)
                    if ToF:
                        pass
                    else:
                        cmds.connectAttr('{}.inverseMatrix'.format(tgt)
                                         , '{}.matrixIn[{}]'.format(mM, i)
                                         , force = True
                                         )
                        connected_counter.append(i)
                # print(connected_counter)
                # print(connected_counter[-1])
                self.notYetConnected_counterEnd = connected_counter[-1] + 1
                # print(self.notYetConnected_counterEnd)
                print(u'connected all  !!!')

                # ######################################################################################
                # 追加 ###################################### start
                # print(self.tgt)
                tgt = self.tgt
                # cmds.select(tgt)
                self.params = self.getInitAttr(tgt)
                print('\n' + '***' * 15)
                print('add attribute, user defined init attr')
                self.createInitAttr(tgt)  # add user defined attr
                print('***' * 15 + '\n')
                print('***' * 15)
                print('store attribute, user defined init attr')
                self.setInitAttr(tgt)
                print('***' * 15 + '\n')
                # self.delInitAttr(tgt)  # delete user defined attr
                # 追加 ######################################## end
                # ######################################################################################
            else:  # 既に接続されているので、接続の解除
                listAll = cmds.listConnections(mM, c = True, s = True, d = False, p = True)
                # print(listAll)
                # print(len(listAll))
                # 必ず偶数の対になることを利用して。。
                mM_connect_List = listAll[2::2]  # listAll の 2番目から最後までを2飛ばしでスライス
                # listAll[2:-1:2] でも良い
                # print(mM_connect_List)
                src_connect_List = listAll[3::2]  # listAll の 3番目から最後までを2飛ばしでスライス
                # print(src_connect_List)
                # print(len(src_connect_List))
                # print(len(mM_connect_List))
                for s, m in zip(src_connect_List, mM_connect_List):
                    # print(s, m)
                    cmds.disconnectAttr(s, m)
                print(u'not connected...')

                # ######################################################################################
                # 追加 ###################################### start
                tgt = self.tgt
                self.breakAndReset(tgt)
                # 追加 ######################################## end
                # ######################################################################################
        print('***' * 30 + u'調査の終了\n')

    # break and reset オペレーション
    def breakAndReset(self, tgt):
        u""" <break and reset オペレーション です。>
        """
        # 共通
        initT, initR, initS, initSH = [], [], [], []
        exist_initT = cmds.listAttr(tgt, st = 'initT') or []
        if exist_initT:
            initT = cmds.getAttr('{}.initT'.format(tgt))[0]
        exist_initR = cmds.listAttr(tgt, st = 'initR') or []
        if exist_initR:
            initR = cmds.getAttr('{}.initR'.format(tgt))[0]
        exist_initS = cmds.listAttr(tgt, st = 'initS') or []
        if exist_initS:
            initS = cmds.getAttr('{}.initS'.format(tgt))[0]
        exist_initSH = cmds.listAttr(tgt, st = 'initSH') or []
        if exist_initSH:
            initSH = cmds.getAttr('{}.initSH'.format(tgt))[0]
        if not exist_initT and not exist_initR and not exist_initS and not exist_initSH:
            pass
            message_warning(u'decomposeMatrix 等のコネクションは見当たるのですが、'
                            u'reset を実行するための、独自 attribute である、'
                            u'user defined init attr 群が見当たりません。'
                            u'当ツールを利用した ペアレントコンストレイン を実行していない'
                            u'可能性が'
                            u'充分考えられます。'
                            u'先ず初めに、'
                            u'当ツールを利用した ペアレントコンストレイン を実行している'
                            u'必要があります。'
                            )
        else:
            # break connection and delete all nodes
            print('***' * 15)
            print('common job, \n'
                  '\tbreak connection and delete all nodes..done'
                  )
            print('***' * 15 + '\n')

            # reset attr, from user defined attr
            print('***' * 15)
            print('reset job, \n'
                  '\treset attr, from user defined attr..done'
                  )
            for axis, para in zip(list('xyz'), initT):
                cmds.setAttr('{}.t{}'.format(tgt, axis), para)
            for axis, para in zip(list('xyz'), initR):
                cmds.setAttr('{}.r{}'.format(tgt, axis), para)
            for axis, para in zip(list('xyz'), initS):
                cmds.setAttr('{}.s{}'.format(tgt, axis), para)
            for axis, para in zip(['xy', 'xz', 'yz'], initSH):
                cmds.setAttr('{}.sh{}'.format(tgt, axis), para)
            print('***' * 15 + '\n')

            # delete user defined attr
            print('***' * 15)
            print('delete job, \n'
                  '\tdelete user defined attr..done'
                  )
            self.delInitAttr(tgt)
            print('***' * 15)

            message(u'connection は全て切断しました。')
            print(u'また、当ツールを使用した、\n'
                  u'parentConstraintByMatrix を実行する前の、ローカル数値への'
                  u'リセットも行いました。\n'
                  u'ご確認ください。\n'
                  u'但し、\n'
                  u'必要とされていた以下のノード\n\t'
                  u'{}\n'
                  u'は、未だ残ったままです。'
                  u'それらも、同時にご確認ください。\n'
                  u'確認方法は、\n'
                  u'newNodes all selection ボタン押下でも確認できます。'.format(self.newNodesAll)
                  )

    # 階層をたどる(Follow the hierarchy)アルゴリズム ######################### start
    # main 2 に利用 ①
    # ノード名(name)から、MDagPath オブジェクトを生成する関数
    def DAGPath(self, name):
        u""" < ノード名(name)から、MDagPath オブジェクト を生成する関数 です >

        ::

          階層をたどる(Follow the hierarchy)アルゴリズム
          main 2 に利用 ①
          MDagPath とは、
            DAGノードの階層パスを持つ MObject ラッパーのこと

        #######################

        #.
            :param list[str] name: ノード名

        #.
            :return: selList.getDagPath(0)
                MDagPath オブジェクト
            :rtype: 'OpenMaya.MDagPath'

        #######################
        """
        selList = om2.MGlobal.getSelectionListByName(name)
        # print(type(selList))  # selList : <type 'OpenMaya.MSelectionList'>
        # print(type(selList.getDagPath(0)))  # selList.getDagPath(0) : <type 'OpenMaya.MDagPath'>
        print(u'ノード名(name)から MDagPath オブジェクト を生成. '
              u'MDagPath オブジェクト: {}'.format(selList.getDagPath(0))
              )
        # print(selList.getDagPath(0))
        return selList.getDagPath(0)

    # main 2 に利用 ②
    # MDagPath オブジェクト(dagpath)から、末端を除外しながら、親をたどる関数
    def get_parents(self, dagpath):
        u""" < MDagPath オブジェクト(dagpath)から、末端を除外しながら、親をたどる関数 です >

        ::

          階層をたどる(Follow the hierarchy)アルゴリズム
          main 2 に利用 ②

        #######################

        #.
            :param dagpath: MDagPath オブジェクト
            :type dagpath: 'OpenMaya.MDagPath'

        #.
            :return parents:
            :rtype parents: list of str

        #######################
        """
        # print(type(dagpath))  # dagpath : <type 'OpenMaya.MDagPath'>
        dagpath_copy = dagpath.getPath()  # OpenMaya.MDagPath.getPath() と同義
        # getPath() : OpenMaya.MDagPath Class の関数 です。MDagPath を返します。とのこと。
        # Returns the specified sub-path of this path. 翻訳: このパスの指定されたサブパスを返します。とのこと。
        # MDagPath : Path to a DAG node from the top of the DAG. 翻訳: DAGの上部からDAGノードへのパス。とのこと。
        # print(type(dagpath_copy))  # dagpath_copy : <type 'OpenMaya.MDagPath'>
        print(u'MDagPath オブジェクト(dagpath) から フルパスを生成. '
              u'フルパス MDagPath オブジェクト: {}'.format(dagpath_copy)
              )
        print(u'\tもしも長ーい名前が返ってきたら、scene 内で名前がダブっている可能性が高いです！！')
        # print(dagpath_copy)
        parents = []
        # print(dagpath.length())  # OpenMaya.MDagPath.length() と同義. length() : OpenMaya.MDagPath Class の関数 です。int を返します。とのこと。
        for i in range(1, dagpath.length()):
            # ex : group3|group2|group1|edfv なら、['group3','group2','group1','edfv']と同義。
            dagpath_copy.pop()  # フルパスに対して、後ろ(階層の下)から、'|' を境にして、1つずつ除外していく。
            # print(dagpath_copy)
            # print(type(dagpath_copy))  # dagpath_copy : <type 'OpenMaya.MDagPath'>
            parents.append(dagpath_copy.getPath())
        # print(type(parents))
        # print(parents)  # parents : list of string
        return parents
    # 階層をたどる(Follow the hierarchy)アルゴリズム ########################### end
    # 「main となる コマンド群」 ############################################################ end

    # 独自規格 attribute 操作一連群 ################################################### start
    # 追加
    # get initial attribute
    def getInitAttr(self, tgt, *args):
        u""" < get initial attribute >

        ::

          追加

        #########################

            :return: params
                : T, R, S, SH
            :rtype: list of float
                : T, R, S, SH

        #########################
        """
        params = []
        for ch in list('trs'):
            for axis in list('xyz'):
                param = cmds.getAttr('{}.{}{}'.format(tgt, ch, axis))
                # print (param)
                params.append(param)
        for axis in {'xy', 'xz', 'yz'}:
            param = cmds.getAttr('{}.sh{}'.format(tgt, axis))
            params.append(param)
        return params

    # 追加
    # add attribute, user defined initial attribute
    def createInitAttr(self, tgt, *args):
        u""" < add attribute, user defined initial attribute >

        ::

          追加
        """
        # print (tgt)
        # create init TRS
        for ch in list('TRS'):
            cmds.addAttr(tgt, ln = "init{}".format(ch), at = 'double3')
            for axis in list('xyz'):
                cmds.addAttr(tgt, ln = "init{}{}".format(ch, axis)
                             , p = 'init{}'.format(ch), at = 'double'
                             )
            cmds.setAttr("{}.init{}".format(tgt, ch), 0, 0, 0, type = 'double3')
        # create init Shear
        cmds.addAttr(tgt, ln = "initSH", at = 'double3')
        for axis in ['xy', 'xz', 'yz']:
            cmds.addAttr(tgt, ln = "initSH{}".format(axis)
                         , p = 'initSH', at = 'double'
                         )

    # 追加
    # store attribute, to user defined initial attribute
    def setInitAttr(self, tgt, *args):
        u""" < store attribute, to user defined initial attribute >

        ::

          追加
        """
        exist_initT = cmds.listAttr(tgt, st = 'initT') or []
        exist_initR = cmds.listAttr(tgt, st = 'initR') or []
        exist_initS = cmds.listAttr(tgt, st = 'initS') or []
        exist_initSH = cmds.listAttr(tgt, st = 'initSH') or []
        if not exist_initT and not exist_initR and not exist_initS and not exist_initSH:
            pass
        else:
            # print (self.params)
            paraT, paraR , paraS = self.params[0:3], self.params[3:6], self.params[6:9]
            paraSH = self.params[9:12]
            # print (paraT, paraR , paraS, paraSH)
            for axis, para in zip(list('xyz'), paraT):
                cmds.setAttr('{}.initT{}'.format(tgt, axis), para)
            for axis, para in zip(list('xyz'), paraR):
                cmds.setAttr('{}.initR{}'.format(tgt, axis), para)
            for axis, para in zip(list('xyz'), paraS):
                cmds.setAttr('{}.initS{}'.format(tgt, axis), para)
            for axis, para in zip(['xy', 'xz', 'yz'], paraSH):
                cmds.setAttr('{}.initSH{}'.format(tgt, axis), para)

    # 追加
    # remove attribute, to user defined initial attribute
    def delInitAttr(self, tgt, *args):
        u""" < remove attribute, to user defined initial attribute >

        ::

          追加
        """
        exist_initT = cmds.listAttr(tgt, st = 'initT') or []
        exist_initR = cmds.listAttr(tgt, st = 'initR') or []
        exist_initS = cmds.listAttr(tgt, st = 'initS') or []
        exist_initSH = cmds.listAttr(tgt, st = 'initSH') or []
        if not exist_initT and not exist_initR and not exist_initS and not exist_initSH:
            pass
        else:
            # delete init TRS
            for ch in list('TRS'):
                cmds.deleteAttr(tgt, at = "init{}".format(ch))
            # delete init Shear
            cmds.deleteAttr(tgt, at = "initSH")
    # 独自規格 attribute 操作一連群 ###################################################### end


class UI(UICmd):
    u"""< Widget class: 子クラス です >

    ::

      UIクラスです
      基本となる要素は以下の 6つ

    ######

        - UI-0. 重複しないウインドウ

        - UI-1. commonメニュー

        - UI-2. メインLayout + common情報 + 追加オプション

        - UI-3. ボタンLayout + common底面ボタン1つ

        - UI-4. OptionVar を利用したパラメータ管理

        - plug-in check

    ######
    """

    # A function to instantiate the UI window
    # UIウィンドウ をインスタンス化する関数
    @classmethod
    def showUI(cls):
        u"""A function to instantiate the YO makeSelection you chosen UI window
        :return win:
        :rtype win: string
        """
        win = cls()
        win.createUI()
        return win

    # class Name を Output します
    def classNameOutput(self):
        u""" <class Name を Output します>
        :return self.__class__.__name__:
        :rtype self.__class__.__name__: string
        """
        return self.__class__.__name__

    def __init__(self):
        u"""Initialize data attributes"""
        super(UI, self).__init__()  # python3系の記述: super().__init__()
        self.helpMenuItem = None
        self.helpMenu = None
        self.editMenuClose = None
        self.editMenuReload = None
        self.editMenuSave = None
        self.editMenu = None
        self.cClmnLyut = None
        self.optionBorder = None
        self.mainForm = None
        self.closeBtn = None

    def createUI(self):
        # if cmds.window(self.win, ex = True):
        #     print('***' * 10)
        #     print('once, close win job')
        #     cmds.deleteUI(self.win)
        #     print('***' * 10 + '\n')
        # print('***' * 10)
        # print('create win job')

        # UI-0. 重複しないウインドウ
        try:
            print('***' * 10)
            print('once, close win job')
            cmds.deleteUI(self.win, window = True)
            print('***' * 10 + '\n')
        except:
            pass
        print('***' * 10)
        print('create win job')

        cmds.window(self.win, title = title[3:] + space + version
                    , widthHeight = self.size
                    , menuBar = True, sizeable = True
                    , maximizeButton = False, minimizeButton = False
                    )

        # UI 大枠の定義
        self.mainForm = cmds.formLayout(nd = 100)  # UI-2. メインLayout + common情報 + 追加オプション
        self.cM_commonMenu()  # UI-1. commonメニュー
        self.cB_commonButtons()  # UI-3. ボタンLayout + common底面ボタン3つ
        self.optionBorder = cmds.tabLayout(scrollable = True, tabsVisible = False, h = 1
                                           , childResizable = True
                                           )
        cmds.formLayout(self.mainForm, e = True
                        , attachForm = ([self.optionBorder, 'top', 5]
                                        , [self.optionBorder, 'left', 5]
                                        , [self.optionBorder, 'right', 5]
                                        )
                        , attachControl = [self.optionBorder, 'bottom', 5, self.closeBtn]
                        )

        # plug-in check
        print('check plug-in job')
        self.checkMatNodePlugIn()
        self.checkQuatNodePlugIn()
        print('***' * 10 + '\n')

        # UI-2. common情報
        self.cClmnLyut = cmds.columnLayout(adjustableColumn = True
                                           , w = 100
                                           )
        cmds.text(l = u'parent constraint, scale constraint byMatrix ツール')
        cmds.text(l = u'note:'
                  , annotation = u'matrix を使用した、\n'
                                 u'parent constraint, scale constraint'
                                 u'を手動で作成していくツールです。'
                  , bgc = self.bgcBlue2
                  )
        cmds.setParent(self.cClmnLyut)  # ui_mainA は cClmnLyut の子供

        cmds.separator(height = 5)

        # UI-2. 追加オプション mainA
        self.ui_mainA()

        cmds.setParent(self.cClmnLyut)  # ui_mainA は cClmnLyut の子供

        cmds.separator(height = 5)

        # UI-2. 追加オプション mainB
        self.ui_mainB()

        cmds.setParent(self.cClmnLyut)  # ui_mainB は cClmnLyut の子供

        # cmds.separator(height = 5)
        cmds.setParent('..')  # 以上は self.win の子供

        # UI-4. OptionVar を利用したパラメータ管理
        restoreOptionVar = 'Restore Option Variables'
        self.restoreOptionVarCmd(restoreOptionVar)

        cmds.evalDeferred(lambda *args: cmds.showWindow(self.win))
        print('***' * 10 + '\n')

    # UIディテール 作成 ################################################################ start
    # UI-1. commonメニュー
    def cM_commonMenu(self):
        u""" < UI-1. commonメニュー の作成 >
        """
        self.editMenu = cmds.menu(l = 'Edit', tearOff = False)
        self.editMenuSave = cmds.menuItem(l = 'Save Settings'
                                          , en = True
                                          , c = self.cM_editMenuSaveCmd
                                          )
        self.editMenuReload = cmds.menuItem(l = 'Reset Settings'
                                            , en = True
                                            , c = self.cM_editMenuReloadCmd
                                            )
        self.editMenuClose = cmds.menuItem(l = 'Close This UI'
                                           , en = True
                                           , c = self.cM_editMenuCloseCmd
                                           )
        self.helpMenu = cmds.menu(l = 'Help')
        self.helpMenuItem = cmds.menuItem(l = 'Help on {}'.format(title)
                                          , c = self.cM_helpMenuCmd
                                          )

    # UI-3. ボタンLayout + common底面ボタン1つ
    def cB_commonButtons(self, *args):
        u""" < UI-3. ボタンLayout + common底面ボタン1つ 作成 >
        """
        self.closeBtn = cmds.button(l = 'Close'
                                    , enable = True
                                    , h = 30
                                    , c = self.cM_editMenuCloseCmd
                                    , vis = True
                                    )
        cmds.formLayout(self.mainForm, e = True
                        , attachForm = ([self.closeBtn, 'bottom', 5]
                                        , [self.closeBtn, 'right', 5]
                                        )
                        , attachPosition = [self.closeBtn, 'left', 2, 0]
                        , attachNone =[self.closeBtn, 'top']
                        )

    # UI-2. 追加オプション mainA
    def ui_mainA(self):
        u""" < UI-2. 追加オプション mainA 作成 >
        """
        A = cmds.frameLayout(label = 'A', collapsable = True
                             , annotation = u"新規に、parentConstraint を matrix "
                                            u"操作で作成します。\n"
                                            u"具体的には、multMatrix の"
                                            u" .matrixIn[0] への setAttr "
                                            u"及び"
                                            u" .matrixIn[1] への connectAttr "
                                            u"までは必ず行っています。\n"
                                            u"また、multMatrix node -->> decomposeMatrix node "
                                            u"のコネクションも行っています。\n"
                                            u"因みに、"
                                            u"target が transform node と joint node の"
                                            u"どちらかで、作成される node 数と connection "
                                            u"方法に若干の違いがあります。\n"
                                            u"具体的には、joint node の時には、jointOrient も"
                                            u"考慮しています。"
                             , collapse = False
                             )

        # 親A に 子A1, A2, A3 をぶら下げる ################################################### start

        # 子A1 #############################################################################
        # textField
        with LayoutManager(cmds.rowColumnLayout(
                numberOfColumns = 5
                , adjustableColumn = 2
                , columnWidth = ([1, 120], [2, 150])  # old: [1, 50], [2, 150]
                , columnSpacing = ([3, 2], [4, 2])
                                                )
                           ) as A1:
            # source
            cmds.text(l = u'コントローラ側(source):', annotation = u"制御する側です")
            self.cTxtFld_A_source = cmds.textField(
                'cTxtFld_A_source', text = ''
                , w = 200
                , annotation = u"制御する側\n"
                               u"コントローラです。 set 入力してください。"
            )
            cmds.button('cBtn_A1_sourceSet', l = "<< set", c = self.ui_cBtn_A1_setSource_exe)
            cmds.button('cBtn_A1_selectSet', l = "Sel", annotation = u"set select"
                        , c = self.ui_cBtn_A1_selectSet_exe
                        , enable = False
                        )
            cmds.button('cBtn_A1_clearSet', l = "C", annotation = u"set clear"
                        , c = self.ui_cBtn_A1_setSourceClear_exe
                        , enable = False
                        )
            # target
            cmds.text(l = u'コントロールされる側(target):', annotation = u"制御される側です")
            self.cTxtFld_A_target = cmds.textField(
                'cTxtFld_A_target', text = ''
                , w = 200
                , annotation = u"制御される側\n"
                               u"コントロールされる方です。 拘束を必要とする方です。 set 入力してください。"
            )
            cmds.button('cBtn_A2_targetSet', l = "<< set"
                        , c = self.ui_cBtn_A2_setTarget_exe
                        )
            cmds.button('cBtn_A2_selectSet', l = "Sel", annotation = u"set select"
                        , c = self.ui_cBtn_A2_selectSet_exe
                        , enable = False
                        )
            cmds.button('cBtn_A2_clearSet', l = "C", annotation = u"set clear"
                        , c = self.ui_cBtn_A2_setTargetClear_exe
                        , enable = False
                        )
            # cmds.setParent(A1)
            # 以上は A1 の子供
        cmds.setParent(A)  # A1 は A の子供

        # 子A2 #############################################################################
        # Execute
        with LayoutManager(cmds.rowLayout(
                numberOfColumns = 1
                , adjustableColumn = 1
                # , columnAttach = [1, 'both', 10]
                                          )
                           ) as A2:
            cBtn_A_exe = cmds.button('cBtn_A_exe', l = 'Execute'
                                     , c = self.ui_Execute_A
                                     , annotation = u'関連する新規ノード作成を行いますが、\n'
                                                    u'完全な実行は未だ行いません。'
                                     , bgc = self.bgcBlue3
                                     )
            # cmds.setParent(A2)
            # 以上は A2 の子供
        cmds.setParent(A)  # A2 は A の子供

        cmds.separator(style = 'in')

        # manual connection area
        # 子A3(cFrmLyut_A3) ################################################################
        with LayoutManager(cmds.frameLayout('cFrmLyut_A3'
                , l = 'manual connection area'
                , labelVisible = True
                , collapsable = False
                , enable = False
                , annotation = u'其々を、ユーザーが手動でコネクションし'
                               u'確認するエリアです。'
                                            )
                           ) as cFrmLyut_A3:
            # R
            # 孫 A3_1 のまとまり #########################################################
            with LayoutManager(cmds.columnLayout(
                    adjustableColumn = True
                    , height = 35
                                                 )
                               ) as cClmnLyut_A3_1:
                mainForm_A3_1 = cmds.formLayout(nd = 100, visible = True)
                A31 = cmds.button('cBtn_A3_outPutNode', l = ''
                                  , height = 30
                                  , c = self.ui_cBtn_A3_outPutNode_select_exe
                                  )
                A32 = cmds.button('cBtn_A3_oP2iP_connectTgl', l = 'R', width = 10
                                  , height = 30
                                  , bgc = self.bgc
                                  , c = self.ui_cBtn_A3_oP2iP_cnctTgl_exe
                                  , annotation = u'<Rotate>のみ\n'
                                                 u'コネクションをトグルできます。'
                                  )
                A33 = cmds.button('cBtn_A3_inPutNode', l = ''
                                  , height = 30
                                  , c = self.ui_cBtn_A3_inPutNode_select_exe
                                  )
                cmds.setParent(mainForm_A3_1)  # 以上は mainForm_A3_1 の子供
                A34 = cmds.formLayout(mainForm_A3_1, e = True
                                      # フォームの境界にボタンのどのエッジを固定するかの指定。
                                      # オフセット値を5としている。
                                      , attachForm = ([A31, 'left', 5], [A31, 'top', 5]
                                                      , [A32, 'top', 5]
                                                      , [A33, 'top', 5], [A33, 'right', 5]
                                                      )
                                      # ボタンをフォームのどの位置に固定するかの指定。
                                      # A31の右辺を40%の位置に、A33の左辺を60%の位置に。
                                      , attachPosition = ([A31, 'right', 2, 40], [A33, 'left', 2, 60])
                                      # 真ん中のボタンA32が左右のボタンの隣接する辺に固定のための設定。
                                      , attachControl = ([A32, 'left', 4, A31], [A32, 'right', 4, A33])
                                      # すべてのボタンの上辺は固定しない。
                                      # , attachNone = ([A31, 'top'], [A32, 'top'], [A33, 'top'])
                                      )
                cmds.setParent(mainForm_A3_1)  # A34 は mainForm_A3_1 の子供
                # cmds.setParent(cClmnLyut_A3_1)
            # mainForm_A3_1 は cClmnLyut_A3_1 の子供
            # cmds.setParent(cFrmLyut_A3)
            # 以上は cFrmLyut_A3 の子供

        # 孫 A3_2 のまとまり  #########################################################
        cClmnLyut_A3_2 = cmds.columnLayout(adjustableColumn = True
                                           , height = 60
                                           )

        mainForm_A3_2 = cmds.formLayout(nd = 100, visible = True)

        # ひ孫 A3_21 ################################################
        A3_21 = cmds.button('cBtn_A321_outPutNode', l = '', height = 30
                            , c = self.ui_cBtn_A321_outPutNode_select_exe
                            )
        cmds.setParent(mainForm_A3_2)  # A3_21 は mainForm_A3_2 の子供

        # ひ孫 A3_22 ################################################
        A3_22 = cmds.columnLayout(adjustableColumn = True, width = 10
                                  # , height = 45
                                  )

        cmds.separator(style = 'in')

        # T, S, Shear
        # ひひ孫 A3_22_1 #############################
        with LayoutManager(cmds.rowLayout(
                numberOfColumns = 3
                , adjustableColumn = 3
                , height = 20
                , columnWidth3 = [15, 15, 15]
                , columnAttach = ([1, 'both', 0], [2, 'both', 0], [3, 'both', 0])
                , annotation = 'AAA'
                                          )
                           ) as A3_22_1:
            cmds.button('cBtn_A32_T_oP2iP_connectTgl', l = 'T', annotation = 'translate'
                        , bgc = self.bgc
                        , enable = False
                        )
            cmds.button('cBtn_A32_S_oP2iP_connectTgl', l = 'S', annotation = 'scale'
                        , bgc = self.bgc
                        , enable = False
                        )
            cmds.button('cBtn_A32_Sh_oP2iP_connectTgl', l = 'Shear', annotation = 'shear'
                        , bgc = self.bgc
                        , enable = False
                        )
            # cmds.setParent(A3_22_1)
            # 以上は A3_22_1 の子供

        cmds.setParent(A3_22)  # A3_22_1 は A3_22 の子供

        cmds.separator(style = 'in')

        # ひひ孫 A3_22_2 #############################
        A3_22_2 = cmds.columnLayout(adjustableColumn = True, width = 10
                                    # , height = 40
                                    )
        # at once T, S, Shear
        cmds.button('cBtn_A32_atOnce_oP2iP_connectTgl', l = 'at once'
                    , height = 30
                    , bgc = self.bgc
                    , c = self.ui_cBtn_A32_atOnce_oP2iP_connectTgl_exe
                    , annotation = u'<Translate, Scale, Shear>を\n'
                                   u'一遍に コネクション トグルできます。'
                    )  # 残りをいっぺんに接続
        cmds.setParent(A3_22_2)  # 以上は A3_22_2 の子供
        cmds.setParent(A3_22)  # A3_22_2 は A3_22 の子供
        cmds.setParent(mainForm_A3_2)  # A3_22 は mainForm_A3_2 の子供

        # ひ孫 A3_23 ################################################
        A3_23 = cmds.button('cBtn_A323_inPutNode', l = '', height = 30
                            , c = self.ui_cBtn_A323_inPutNode_select_exe
                            )
        cmds.setParent(mainForm_A3_2)  # A3_23 は mainForm_A3_2 の子供

        # ひ孫 A3_21 A3_22 A3_23 のレイアウト #############################
        A3_24 = cmds.formLayout(mainForm_A3_2, e = True
                                # フォームの境界にボタンのどのエッジを固定するかの指定。
                                # オフセット値を5としている。
                                , attachForm = ([A3_21, 'left', 5], [A3_21, 'bottom', 15]
                                                , [A3_22, 'bottom', 0]
                                                , [A3_23, 'bottom', 15], [A3_23, 'right', 5]
                                                )
                                # ボタンをフォームのどの位置に固定するかの指定。
                                # A31の右辺を40%の位置に、A33の左辺を60%の位置に。
                                , attachPosition = ([A3_21, 'right', 2, 40]
                                                    , [A3_23, 'left', 2, 60]
                                                    )
                                # 真ん中のボタンA32が左右のボタンの隣接する辺に固定のための設定。
                                , attachControl = ([A3_22, 'left', 4, A3_21]
                                                   , [A3_22, 'right', 4, A3_23]
                                                   )
                                # すべてのボタンの下辺は固定しない。
                                # , attachNone = ([A3_21, 'bottom'], [A3_22, 'bottom']
                                #                 , [A3_23, 'bottom']
                                #                 )
                                )
        cmds.setParent(mainForm_A3_2)  # A3_24 は mainForm_A3_2 の子供
        cmds.setParent(cClmnLyut_A3_2)  # mainForm_A3_2 は cClmnLyut_A3_2 の子供
        cmds.setParent(cFrmLyut_A3)  # cClmnLyut_A3_2 は cFrmLyut_A3 の子供

        # 孫 A3_3 のまとまり  #########################################################
        cClmnLyut_A3_3 = cmds.columnLayout(adjustableColumn = True
                                           , height = 170
                                           )

        cmds.separator(style = 'in', width = 200)

        mainForm_A3_31 = cmds.formLayout(nd = 100, visible = True)

        # image
        # ひ孫 A3_31 ################################################
        with LayoutManager(cmds.columnLayout(
                adjustableColumn = True
                # , columnAlign = 'center'
                # , columnAttach = ['right', 155]
                , columnOffset = ['left', -30]
                                             )
                           ) as A3_31:
            A3_31_1 = cmds.text(l = u'image:           ')
            A3_31_2 = cmds.text(l = u'group\n'
                                    u'│'
                                , bgc = [0, 0, 0], enableBackground = False
                                )
            A3_31_3 = cmds.text('cTxt_A3_31_3_text', l = u'          ├ group\n'
                                                         u'                  │    └ source\n'
                                                         u'│\n'
                                                         u'│\n'
                                                         u'│\n'
                                                         u'          ├ group\n'
                                                         u'                 │    └ target'
                                , bgc = self.bgc2
                                )
            A3_31_4 = cmds.text(l = u'│\n'
                                    u'│'
                                , bgc = [0, 0, 0], enableBackground = False
                                )
            # cmds.setParent('..')

        # ひ孫 A3_32 ################################################
        A3_32 = cmds.columnLayout(adjustableColumn = True)
        with LayoutManager(cmds.rowColumnLayout(
                numberOfColumns = 2
                # , columnWidth=[(1, 30), (2, 10)]
                , adjustableColumn = 1
                                                )
                           ) as A3_32_1:
            A3_32_1_1 = cmds.button('cBtn_A3_32_source', l = self.text_A3_32_source
                                    , bgc = self.bgc, enable = False
                                    , width = 20, height = 20
                                    , annotation = u'source 階層側各ノードの'
                                                   u'<.matrix>と\n'
                                                   u'multMatrix側の'
                                                   u'<.matrixIn[2]~>とを\n'
                                                   u'一遍に コネクション トグルできます。'
                                    )
            A3_32_1_2 = cmds.text('cTxt_A3_32_1_2', l = u'各ノードの\n'
                                                        u'.matrix\n'
                                                        u'attribute')
            # at once matrix
            A3_32_1_3 = cmds.button('cBtn_A3_32_1_3_atOnce_oP2iP_connectTgl', l = u'at once', height = 30
                                    , bgc = self.bgc
                                    , annotation = u'各ノードの'
                                                   u'<.matrix, .inverseMatrix>\nと\n'
                                                   u'multMatrix側の'
                                                   u'<.matrixIn[*]>\nとを'
                                                   u'一遍に コネクション トグルできます。'
                                    , c = self.ui_cBtn_A3_32_1_3_atOnce_oP2iP_connectTgl_exe
                                    )
            A3_32_1_4 = cmds.text('cTxt_A3_32_1_4', l = u'')
            A3_32_1_5 = cmds.button('cBtn_A3_32_target', l = self.text_A3_32_target
                                    , bgc = self.bgc, enable = False
                                    , width = 20, height = 20
                                    , annotation = u'target 階層側各ノードの'
                                                   u'<.inverseMatrix>と\n'
                                                   u'multMatrix側の'
                                                   u'<~.matrixIn[*]>とを\n'
                                                   u'一遍に コネクション トグルできます。'
                                    )
            A3_32_1_6 = cmds.text('cTxt_A3_32_1_6', l = u'各ノードの\n'
                                                        u'.inverse\nMatrix\n'
                                                        u'attribute'
                                  )
            # cmds.setParent(A3_32_1)
        cmds.setParent(A3_32)
        cmds.setParent('..')

        # ひ孫 A3_33 ################################################
        A3_33 = cmds.columnLayout(adjustableColumn = True)
        with LayoutManager(cmds.rowLayout(
                numberOfColumns = 2
                , adjustableColumn = 2
                                          )
                           ) as A3_33_1:
            A3_33_1_1 = cmds.text('cTxt_A3_33_1_1', l = u'multMatrix\n'
                                                        u'.matrixIn[2~]\nattribute\n'
                                                        u'------------>'
                                                        u'\n\n\n\n'
                                                        u'------------>\n'
                                                        u'multMatrix\n'
                                                        u'.matrixIn[~*]\nattribute\n'
                                                        u''
                                  )
            A3_33_1_2 = cmds.button('cBtn_A3_33_mM', l = u'', height = 100
                                    , c = self.ui_cBtn_A3_33_mM_select_exe
                                    )
            # cmds.setParent(A3_33_1)
        cmds.setParent('..')

        # ひ孫 A3_31 A3_32 A3_33 のレイアウト #############################
        A3_34 = cmds.formLayout(mainForm_A3_31, e = True
                                # フォームの境界にボタンのどのエッジを固定するかの指定。
                                # オフセット値を5としている。
                                , attachForm = ([A3_31, 'left', 5], [A3_31, 'bottom', 5]
                                                , [A3_32, 'top', 30]
                                                , [A3_33, 'top', 10], [A3_33, 'right', 5]
                                                )
                                # ボタンをフォームのどの位置に固定するかの指定。
                                # A31の右辺を40%の位置に、A33の左辺を60%の位置に。
                                , attachPosition = ([A3_31, 'right', 2, 30]
                                                    , [A3_32, 'left', 2, 30]
                                                    , [A3_32, 'right', 2, 60]
                                                    , [A3_33, 'left', 2, 60]
                                                    )
                                # 真ん中のボタンA32が左右のボタンの隣接する辺に固定のための設定。
                                , attachControl = ([A3_32, 'left', 2, A3_31], [A3_32,
                                                                               'right',
                                                                               2, A3_33])
                                # すべてのボタンの上辺は固定しない。
                                , attachNone = ([A3_31, 'bottom'], [A3_32, 'bottom'],
                                                [A3_33, 'bottom'])
                                )

        cmds.setParent(mainForm_A3_31)  # A34 は mainForm_A3_31 の子供

        cmds.setParent(cClmnLyut_A3_3)  # mainForm_A3_31 は cClmnLyut_A3_3 の子供

        cmds.setParent(cFrmLyut_A3)  # 以上は cFrmLyut_A3 の子供

        # 親A に 子A1, A2, A3 をぶら下げる ###################################################### end

        cmds.button('cBtn_A_selAllNwNds'
                    , l = 'newNodes all selection'
                    , c = self.ui_cBtn_A_selAllNwNds_exe
                    , annotation = u'新規作成された、全てのノードを'
                                   u'一遍に選択します。'
                    )
        with LayoutManager(cmds.rowColumnLayout(adjustableColumn = 1
                , numberOfColumns = 2
                , columnWidth = ([1, 150], [2, 50])
                                                )
                           ):
            cmds.button('cBtn_A_allClear'
                        , l = 'all memory clear and delete newNodes'
                        , c = self.ui_cBtn_A_allClear_exe
                        , annotation = u'登録しておいた、全ての内容を'
                                       u'一斉に解除します。\n'
                                       u'また、新規作成された、全てのノードも'
                                       u'一遍に削除します。'
                        )  # Cancel registrations all at once
            cmds.button('cBtn_A_allDone', enable = False
                        , l = 'all done'
                        , c = self.ui_cBtn_A_allDone_exe
                        , annotation = u'実行を全て完了させます。\n'
                                       u'また、UIを初期状態にします。')
        cmds.setParent(A)  # cFrmLyut_A3 は A の子供

    # UI-2. 追加オプション mainB
    def ui_mainB(self):
        u""" < UI-2. 追加オプション mainB 作成 >
        """
        cmds.frameLayout(label = 'B', collapsable = True
                         , annotation = u"`任意の multMatrix の matrixIn[0] へ "
                                        u"setAttr するためのメニューです。"
                         , collapse = True
                         )

        # 親B に 子B1, B2 をぶら下げる
        B1 = cmds.rowColumnLayout(adjustableColumn = 2, numberOfColumns = 3
                                  , columnWidth = ([1, 50], [2, 150])
                                  )
        cmds.text(l = 'source', annotation = u"元となるソース")
        cmds.textField(w = 150
                       , annotation = u"matrix attribute を出力したい node "
                                      u"を set 入力してください。"
                       )
        cmds.button(l = "<< set", c = '{}.ui_cBtn_setSource_B_exe()'.format(__name__))
        cmds.setParent('..')  # B1 は B の子供

        B3 = cmds.rowLayout(adjustableColumn = 2, numberOfColumns = 4
                            , columnWidth = ([1, 130], [2, 150])
                            )
        cmds.text(l = 'y r choice multMatrix node', annotation = u"multMatrix")
        cmds.textField(
                       # , w = 150
                       h = 30, font = 'fixedWidthFont', bgc = [0.7, 0.7, 0.7]
                       , annotation = u"multMatrix を set 入力してください。"
                       )
        cmds.button(l = "<< set"
                    , c = '{}.ui_cBtn_setMultMat_B_exe()'.format(__name__)
                    )
        cmds.button(l = "set\nclear", enable = False
                    , c = '{}.ui_cBtn_clear_B_exe()'.format(__name__)
                    )
        cmds.setParent('..')  # B1 は B の子供

        B2 = cmds.columnLayout(adjustableColumn = 1, columnAttach = ['both', 10])
        cmds.button(l = 'Execute', c = ('{}.ui_Execute_B()'.format(__name__)))
        cmds.setParent('..')  # B2 は B の子供
    # UIディテール 作成 ################################################################## end

    # plug-in check ################################################################## start
    # matrixNodes系 plug-in の checkTool
    def checkMatNodePlugIn(self):
        u""" < matrixNodes(decomposeMatrix)系 plug-inのロード >
        """
        matNodePlugin = "matrixNodes"
        ToF = cmds.pluginInfo(matNodePlugin, q = True, l = True)
        if not ToF:
            cmds.loadPlugin(matNodePlugin)
            message(u"## check ##\n"
                    u"{} プラグインをロードしました。"
                    .format(matNodePlugin)
                    )
        else:
            pass
            message_warning(u'## check ##\n'
                            u'{} プラグインは、既にロードされています。'
                            .format(matNodePlugin)
                            )

    # quatNodes系 plug-in の checkTool
    def checkQuatNodePlugIn(self):
        u""" < quatNodes系 plug-inのロード >
        """
        quatNodePlugin = "quatNodes"
        ToF = cmds.pluginInfo(quatNodePlugin, q = True, l = True)
        if not ToF:
            cmds.loadPlugin(quatNodePlugin)
            message(u"## check ##\n"
                    u"{} プラグインをロードしました。"
                    .format(quatNodePlugin)
                    )
        else:
            pass
            message_warning(u'## check ##\n'
                            u'{} プラグインは、既にロードされています。'
                            .format(quatNodePlugin)
                            )
    # plug-in check #################################################################### end


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
    UI.showUI()  # open UI
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
