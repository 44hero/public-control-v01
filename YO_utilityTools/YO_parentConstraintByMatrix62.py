# -*- coding: utf-8 -*-

u"""
YO_parentConstraintByMatrix62.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -8.0-
:Date: 2023/10/27

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PyMel version: 1.2.0

概要(overview):
    matrix を使用した、parent constraint, scale constraint を自動作成するツールです。
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
        YO_parentConstraintByMatrix5.py ツール (手動接続用)
            をベースに、当ツールを作成しました。
                よって、上記の手動接続用ツールを推奨します。

    当ツールは、
        その、自動作成バージョンにあたり、簡潔な、コード記述実行を目的としています。

    ・ text ベースのコマンド 出力を搭載
        UI操作実行後、 maya script editor のには必ず、text ベースのコマンド を出力も致します。
            繰り返し作業や、スクリプトベースの作業を補足するためです。
                詳細は、 maya script editor をご覧ください。
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

      # UI立ち上げるには
      # import <パッケージ名>.<モジュール名>
      import YO_utilityTools.YO_parentConstraintByMatrix62
      reload(YO_utilityTools.YO_parentConstraintByMatrix62)
      # <パッケージ名>.<モジュール名>.<□□:機能名>()
      YO_utilityTools.YO_parentConstraintByMatrix62.UI.showUI()

      # UI立ち上げずに、コマンドで実行するには
      # 以下 e.g.):
      # import <パッケージ名>.<モジュール名>
      import YO_utilityTools.YO_parentConstraintByMatrix62
      # reload(YO_utilityTools.YO_parentConstraintByMatrix62)
      # <パッケージ名>.<モジュール名>.<□□:機能名>()
      YO_utilityTools.YO_parentConstraintByMatrix62.UI().command(connect = True
                , source = 'jawA_ctrl_L', target = 'jawA_jt_L')

注意(note):
    ・ 他に必須な独自モジュール
        ::

          from YO_utilityTools.renameTool.YO_renameTool5_Modl import RT_Modl
          from YO_utilityTools.message import message
          from YO_utilityTools.message_warning import message_warning
          from YO_utilityTools.commonCheckJoint import commonCheckJoint  # :return: bool
          from YO_utilityTools.commonCheckSelection import commonCheckSelection  # :return: string

<UI 説明>
    ・ source : 制御する側
        コントローラです。 set 入力してください。
    ・ target : 制御される側
        コントロールされる方です。 拘束を必要とする方です。 set 入力してください。

-UIを立ち上げずにコマンドで実行する方法-
    補足(supplementary explanation):
        「接続の有無」,「制御する」側,「制御される」側 さえ明確ならば、UIを立ち上げずにコマンドで実行も出来ます。
    <接続編>
        使用法(usage):
            <各コマンド 説明>
                connect, ct:  「接続の有無」 :bool:
                    e.g.)True
                source, src: 「制御する」側 名 :string:
                    e.g.)'jawA_ctrl_L'
                target, tgt: 「制御される」側 名 :string:
                    e.g.)'jawA_jt_L'

            <longName>:
                ::

                  YO_parentConstraintByMatrix62.UI().command(connect = True
                  , source = 'jawA_ctrl_L', target = 'jawA_jt_L'
                  )
            <shortName>:
                ::

                  YO_parentConstraintByMatrix62.UI().command(ct = True
                  , src = 'jawA_ctrl_L', tgt = 'jawA_jt_L'
                  )
    <切断編>
        使用法(usage):
            <各コマンド 説明>
                target, tgt: 「切断したい、制御されているノード」側 名 :string:
                    e.g.)'pCube1'

            <longName>:
                ::

                  YO_parentConstraintByMatrix62.UICmd().brkAndRest_command(target = 'pCube1')
            <shortName>:
                ::

                  YO_parentConstraintByMatrix62.UICmd().brkAndRest_command(tgt = 'pCube1')

-リマインダ-
    done: 2023//10/27
        汎用箇所を、モジュールとして読み込みに変更

        version = '-8.0-'

    done: 2023/10/11
        - python2系 -> python3系 変換
            - 変換箇所1
                - 概要: dict関連
                - 詳細: 以下参照
                ::

                  -        for ptnBNumber_keys, ptnBFindStrs_values in ptnB_dict.items():
                                ...
                  +        for ptnBNumber_keys, ptnBFindStrs_values in list(ptnB_dict.items()):
                                ...
            - 変換箇所2
                - 概要: dict関連
                - 詳細: 以下参照
                ::

                  -        for ptnCNumber_keys, ptnCFindStrs_values in ptnC_dict.items():
                                ...
                  +        for ptnCNumber_keys, ptnCFindStrs_values in list(ptnC_dict.items()):
                                ...
            - 変換箇所3
                - 概要: dict関連
                - 詳細: 以下参照
                ::

                  -        key0 = kwargs.keys()[0]
                  +        key0 = list(kwargs.keys())[0]
            - 変換箇所4
                - 概要: dict関連
                - 詳細: 以下参照
                ::

                  -        key1 = kwargs.keys()[1]
                  +        key1 = list(kwargs.keys())[1]
            - 変換箇所5
                - 概要: dict関連
                - 詳細: 以下参照
                ::

                  -        key2 = kwargs.keys()[2]
                  +        key2 = list(kwargs.keys())[2]
            - 変換箇所6
                - 概要: dict関連
                - 詳細: 以下参照
                ::

                  -        key0 = kwargs.keys()[0]
                  +        key0 = list(kwargs.keys())[0]

      version = '-7.0-'

    done: 2023/05/24
        - 変更1
            - DG命名を見直す

        version = '-6.0-'

    done: 2023/05/17
        - 中身を整理
        - 追加
            - optionVariable への対応

        version = '-5.0-'

    done: 2023/05/11~2023/05/12
        - 役割で、クラス分けの見直しを実施
        - 中身を整理

        version = '-4.0-'

    done: バグ修正 2021/09/30
        - 親リスト数の不一致時

        version = '-3.0-'

    done: 追加 2021/05/26
        - break connections と reset 用の、コマンドバージョンも作成

        version = '-2.5-'

    done: 追加 2021/05/20~26
        - target node に、
            - initial attr の追加及び、
            - いつでも呼び出せるよう break connections と reset も追加

        version = '-2.0-'

    done: 整理 2021/05/20
        version = '-1.0-'

    done: 2019/10/23
        - class集約の特性を利用して、UI class と コマンド class で役割を分けた。
    done: 2019/10/21-23
        - コマンドバージョン作成。
            - 手動接続用よりも簡潔で自動接続を前提としたい。
            - バージョン名を変更し、別ツールとした。
    done: 2019/10/18
        - source側階層、target側階層を、全てたどり終え、必要な工程を全て完結。
    done: 2019/09/26
        - class版として、着手
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
from YO_utilityTools.lib.commonCheckJoint import commonCheckJoint  # :return: bool
from YO_utilityTools.lib.commonCheckSelection import commonCheckSelection  # :return: string

# optionVar_command_library(optionVarを操作するライブラリー)
from YO_utilityTools.lib.YO_optionVar import setOptionVarCmd  # オプション変数を設定する関数
from YO_utilityTools.lib.YO_optionVar import getOptionVarCmd  # オプション変数を取得する関数
# from YO_utilityTools.YO_optionVar import upDateOptionVarsDictCmd  # オプション変数をdict操作し、更新をかける関数
# from YO_utilityTools.YO_optionVar import upDateOptionVarCmd  # オプション変数に更新をかける関数
# 汎用ライブラリー の使用 ################################################################## end

from YO_utilityTools.renameTool.YO_renameTool5_Modl import RT_Modl

title = 'YO_parentConstraintByMatrix62'  # Long Name
space = ' '
version = '-8.0- <py 3.7.7 確認済, ui:cmds, TRS一括処理版>'
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
            - 新規作成された outPutNode と inPutNode コネクションに使用される関数
            - 階層をたどる(Follow the hierarchy)アルゴリズム

        - 3. UI-3. common ボタン コマンド群

                - 接続編 <UI用>
                    - 接続 proc1.
                        UI Execute ボタン押下 実行 関数
                            execute
                - 切断編 <UI用>
                    - 切断 proc2.
                        UI Break and reset ボタン押下 実行 関数
                            breakAndReset

        - 5. スクリプトベースコマンド入力への対応

                - 接続編 <スクリプトベース用>
                    - 接続 proc1.5.
                        新規のノード作成及び、source target の Rotate, Translate, Scale, Shear との接続
                            command
                    - 接続 proc2.
                        source, target 階層側 と multMatrix のコネクションを行う(matrix 限定)
                            cnctSrcHircyTgtHircy2MltMat_exe
                    - 接続実行文を生成する関数
                - 切断編 <スクリプトベース用>
                    - 切断 proc1.
                        brkAndRest_command
                    - 切断実行文を生成する関数

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
        self.tFldB_set_tgt = None
        self.tFldA_set_src = None

        self.size = (200, 153)
        self.win = title + '_ui'

        self.bgcBlue = [0.5, 0.5, 0.9]  # list of float
        self.bgcBlue2 = [0.0, 0.7, 1.0]  # list of float

        self.message = message
        self.message_warning = message_warning
        self.commonCheckSelection = commonCheckSelection  # :return: string

        self.src = ''
        self.tgt = ''
        self.srcP = ''
        self.cnctAll_value = True
        self.mM = ''
        self.dM = ''
        self.outPutNode = ''
        self.inPutNode = ''
        self.outPutNode2 = ''
        self.newNodesAll = []
        self.followHierarchy_isConnected_ToF = False  # multMatrix の matrixIn[2] をトリガーとしています
        self.notYetConnected_counterStart = 2  # multMatrix の matrixIn で未接続の一番若い数字を記録1
        self.notYetConnected_counterEnd = 10  # multMatrix の matrixIn で未接続の一番若い数字を記録2

        self.params = []  # list of float, count 12, T, R, S, SH

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

    def classNameOutput(self):
        """
        :rtype: str
        :return: self.__class__.__name__
        """
        return self.__class__.__name__

    # 1. UI-1. メニュー コマンド群 ###################################################### start
    # 追加
    # Save Settings 実行 関数
    def editMenuSaveCmd(self, *args):
        u""" <SaveSetting 実行 関数>

        ::

          追加
        """
        # tFld_key Src
        getTxt_fromTxtFldSrc = cmds.textField(self.tFldA_set_src, q = True, text = True)
        setOptionVarCmd(self.optionVar01_tFld_key, getTxt_fromTxtFldSrc)

        # tFld_key Tgt
        getTxt_fromTxtFldTgt = cmds.textField(self.tFldB_set_tgt, q = True, text = True)
        setOptionVarCmd(self.optionVar02_tFld_key, getTxt_fromTxtFldTgt)

        self.message('Save Settings')
        print(getTxt_fromTxtFldSrc, getTxt_fromTxtFldTgt)

    # UI Reset 実行 関数
    def editMenuReloadCmd(self, *args):
        u""" <UI Reset 実行 関数 です>
        """
        # UI.showUI()

        # 追加
        self.set_default_value_toOptionVar()  # UI-4. optionVar の value を default に戻す操作

        cmds.evalDeferred(lambda *args: UI.showUI())  # refresh UI <---- ここ重要!!
        self.message('reset UI, done')

    # UI Close 実行 関数
    def editMenuCloseCmd(self, *args):
        u""" <UI Close 実行 関数 です>
        """
        self.editMenuSaveCmd()  # 追加
        cmds.evalDeferred(lambda *args: cmds.deleteUI(self.win))
        self.message('close done')

    # Help 実行 関数
    def helpMenuCmd(self, *args):
        u""" <help menu>
        """
        help(__name__)
        self.message('see your script editor, detail information....')
    # common command ################################################################### end

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
        cmds.textField(self.tFldA_set_src, edit = True, text = tFld_key_Src)
        # button のステータスも加味
        if len(tFld_key_Src):
            # UI 更新
            cmds.button('tBtnA_set_src', e = True, enable = False)
            cmds.button('tBtnA_sel_src', e = True, enable = True)
            cmds.button("tBtnA_clr_src", e = True, enable = True)

        # tFld_key_Tgt
        # self.cmnTxtFld_B1.setText(self.options[self.optionVar02_tFld_key])
        tFld_key_Tgt = getOptionVarCmd(self.optionVar02_tFld_key)  # type: str
        cmds.textField(self.tFldB_set_tgt, edit = True, text = tFld_key_Tgt)
        if len(tFld_key_Tgt):
            # UI 更新
            cmds.button('tBtnB_set_tgt', e = True, enable = False)
            cmds.button('tBtnB_sel_tgt', e = True,  enable = True)
            cmds.button("tBtnB_clr_tgt", e = True, enable = True)

        self.message(args[0])  # message output
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
    # UI button A -set- source
    def ui_tBtnA_set_src_exe(self, *args):
        u""" <UI button A -set- source>
        """
        sel = self.commonCheckSelection()  # selection 共通関数
        if sel:
            selGeo = cmds.ls(sl = True)[0]
            # print(checkSC)
            om.MGlobal.displayInfo(u'Set 完了')
            cmds.textField('tFldA_set_src', e = True, text = selGeo)
            cmds.button('tBtnA_set_src', e = True, enable = False)
            cmds.button('tBtnA_sel_src', e = True, enable = True)
            cmds.button('tBtnA_clr_src', e = True, enable = True)

    # UI button A -selectSet- source
    def ui_tBtnA_selSet_src_exe(self, *args):
        u""" <UI button A -selectSet- source>
        """
        setGeo = cmds.textField('tFldA_set_src', q = True, text = True)
        cmds.select(setGeo, r = True)

    # UI button A -setClear- source
    def ui_tBtnA_clrSet_src_exe(self, *args):
        u""" <UI button A -setClear- source>
        """
        cmds.textField('tFldA_set_src', e = True, text = '')
        cmds.button('tBtnA_set_src', e = True, enable = True)
        cmds.button('tBtnA_sel_src', e = True, enable = False)
        cmds.button('tBtnA_clr_src', e = True, enable = False)

    # UI button B -set- target
    def ui_tBtnB_set_tgt_exe(self, *args):
        u""" <UI button B -set- target>
        """
        sel = self.commonCheckSelection()  # selection 共通関数
        if sel:
            selGeo = cmds.ls(sl = True)[0]
            # print(checkSC)
            om.MGlobal.displayInfo(u'Set 完了')
            cmds.textField('tFldB_set_tgt', e = True, text = selGeo)
            cmds.button('tBtnB_set_tgt', e = True, enable = False)
            cmds.button('tBtnB_sel_tgt', e = True, enable = True)
            cmds.button('tBtnB_clr_tgt', e = True, enable = True)

    # UI button B -selectSet- target
    def ui_tBtnB_selSet_tgt_exe(self, *args):
        u""" < UI button B -selectSet- target >
        """
        setGeo = cmds.textField('tFldB_set_tgt', q = True, text = True)
        cmds.select(setGeo, r = True)

    # UI button B -setClear- target
    def ui_tBtnB_clrSet_tgt_exe(self, *args):
        u""" < UI button B -setClear- target >
        """
        cmds.textField('tFldB_set_tgt', e = True, text = '')
        cmds.button('tBtnB_set_tgt', e = True, enable = True)
        cmds.button('tBtnB_sel_tgt', e = True, enable = False)
        cmds.button('tBtnB_clr_tgt', e = True, enable = False)
    # 2. UI-2. 追加オプション コマンド群 ################################################### end

    # その他 アルゴリズムとなる コマンド群 ################################################# start
    # 命名規則のコントロール ################################################ start
    # under bar 3 or 2 version
    def nodeName_decomp_exeB(self, nodes):
        u""" < under bar 3 or 2 version >

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
            for ptnBNumber_keys, ptnBFindStrs_values in list(ptnB_dict.items()):  # 変換箇所1
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
            for ptnCNumber_keys, ptnCFindStrs_values in list(ptnC_dict.items()):  # 変換箇所2
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
        u""" < strCompLists のカウント数に応じたネーミングの振り分け >

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
                    , u''  # 変更 memo): old - > u'~'
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

    # 命名規則のコントロール  ################################################# end

    # 新規作成された outPutNode と inPutNode コネクションに使用される関数 ###### start
    # matrix を利用した parentConstraint を可能とするメイン関数
    def commonCommand(self, src, tgt, nodeAll):
        u""" <matrix を利用した parentConstraint を可能とするメイン関数>

        :param src:
        :type src: string
        :param tgt:
        :type tgt: string
        :param nodeAll:
        :type nodeAll: list of string
        :return dupTgt, nodeAll:
        :rtype dupTgt, nodeAll: string, list of string
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

    # 新規作成された outPutNode と inPutNode のコネクションを行う
    # (rotate 限定)
    def oP2iP_cnctR_exe(self, outPutNode, inPutNode):
        u""" <新規作成された outPutNode と inPutNode のコネクションを行う
        (rotate 限定)
        >
        """
        chkSorcRotPlugs = []
        for ax in list('XYZ'):
            # inPutNode 自分自身へ入力されてくる、ソース元をリストする(rot のみ！)
            plug = cmds.listConnections('{}.rotate{}'.format(inPutNode, ax)
                                        , c = False
                                        , s = True, d = False, p = True
                                        )
            chkSorcRotPlugs.append(plug)
        # print(chkSorcRotPlugs)
        if chkSorcRotPlugs == [None, None, None]:
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

    # 新規作成された outPutNode と inPutNode のコネクションを行う
    # (Translate, Scale, Shear 限定)
    def oP2iP_cnctTSSh_exe(self, outPutNode, inPutNode):
        u""" <新規作成された outPutNode と inPutNode のコネクションを行う
        (Translate, Scale, Shear 限定)
        >
        """
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
        if chkSorcTSShPlugs == [None, None, None, None, None, None, None, None, None]:
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
    # 新規作成された outPutNode と inPutNode コネクションに使用される関数 ######## end

    # 階層をたどる(Follow the hierarchy)アルゴリズム ######################### start
    # sub main 関数:
    # 最終接続 となり、
    # 階層をたどり、新規作成された multMatrix との接続まで行う。
    def main_followTheHierarchyAndConnection_exe(self):
        u""" <sub main 関数:
        最終接続 となり、
        階層をたどり、新規作成された multMatrix との接続まで行う。
        >
        """
        # 階層をたどる
        selList = []
        selList = self.commonCheckSelection()
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
        print('***' * 30 + u'調査の終了\n')

    # sub main 関数 に利用 1:
    # ノード名(name)から、MDagPath オブジェクトを生成する関数
    # MDagPath とは、DAGノードの階層パスを持つ MObject ラッパーのこと。
    def DAGPath(self, name):
        u""" <sub main 関数に利用 1:
        ノード名(name)から、MDagPath オブジェクト を生成する関数。
        >
        :param name: ノード名
        :type name: list of string
        :return selList.getDagPath(0): MDagPath オブジェクト
        :rtype selList.getDagPath(0): 'OpenMaya.MDagPath'
        """
        selList = om2.MGlobal.getSelectionListByName(name)
        # print(type(selList))  # selList : <type 'OpenMaya.MSelectionList'>
        # print(type(selList.getDagPath(0)))  # selList.getDagPath(0) : <type 'OpenMaya.MDagPath'>
        print(u'ノード名(name)から MDagPath オブジェクト を生成. '
              u'MDagPath オブジェクト: {}'.format(selList.getDagPath(0))
              )
        # print(selList.getDagPath(0))
        return selList.getDagPath(0)

    # sub main 関数に利用 2:
    # MDagPath オブジェクト(dagpath)から、末端を除外しながら、親をたどる関数
    def get_parents(self, dagpath):
        u""" <sub main 関数に利用 2:
        MDagPath オブジェクト(dagpath)から、末端を除外しながら、親をたどる関数。
        >

        :param dagpath: MDagPath オブジェクト
        :type dagpath: オブジェクト
        :return parents:
        :rtype parents: list of string
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
    # その他 アルゴリズムとなる コマンド群 ################################################### end

    # 3. UI-3. common ボタン コマンド群 ################################################# start
    # 接続編 <UI用> ####################################################### start
    ##########################################
    # プロセスの大枠 #######
    #######################
    # 接続 proc1. UI Execute ボタン押下 実行 関数
    #   def execute(self, ..):..
    # <共通>
    #   接続 proc1.5.
    #       def command(self, ..):..
    # <共通>
    #   接続 proc2.
    #       def cnctSrcHircyTgtHircy2MltMat_exe(self, ..):..
    ##########################################

    # 接続編 <UI用>
    # 接続 proc1. #
    # UI Execute ボタン押下 実行 関数
    # proc1.5. へ渡ります
    def execute(self, *args):
        u""" < proc1. UI Execute ボタン押下 実行 関数です >

        ::

          proc1.5. へ渡ります
        """
        self.src = cmds.textField('tFldA_set_src', q = True, text = True)
        self.tgt = cmds.textField('tFldB_set_tgt', q = True, text = True)
        self.cnctAll_value = cmds.checkBox('cBox_cnctAll', q = True, v = True)
        # print(sorcSkGeo, destSkGeo)
        src = self.src
        tgt = self.tgt
        cnctAllValue = self.cnctAll_value
        # コマンドベース
        self.command(connect = cnctAllValue, source = src, target = tgt)  # proc1.5. へ渡る
    # 接続編 <UI用> ######################################################### end

    # 切断編 <UI用> ####################################################### start
    ##########################################
    # プロセスの大枠 #######
    #######################
    # 切断 proc2. UI Break and reset ボタン押下 実行 関数
    #   def breakAndReset(self, ..):..
    ##########################################

    # 切断編 <UI用>
    # 切断 proc2. #
    # UI Break and reset ボタン押下 実行 関数
    # <スクリプトベース用> にも再利用しています
    def breakAndReset(self, *args):
        u""" < UI Break and reset ボタン押下 実行 関数です。 >
        """
        sels = self.commonCheckSelection()
        if not sels:
            self.message_warning(u'何も選択されていないため、継続実行を中止しました。'
                                 u'reset したいノードを一つ選択し再度実行してください。'
                                 u'connection を切断し、基から有った、ローカル数値にリセットいたします。'
                                 )
        else:
            dCMtx = cmds.listConnections(sels[0], t = 'decomposeMatrix') or []
            # print (dCMtx)
            isJoint = commonCheckJoint(sels[0])  # joint かどうか、return bool

            # joint の時、特殊
            if isJoint:
                qTElr = cmds.listConnections(sels[0], t = 'quatToEuler') or []
                # print (qTElr)
                if not qTElr:
                    pass
                    self.message_warning(u'quatToEuler 等のコネクションが見当たりません。'
                                         u'matrix を利用した ペアレントコンストレイン でない可能性が'
                                         u'充分考えられます。'
                                         )
                else:
                    # break connection and delete all nodes
                    print('***' * 15)
                    print('joint only job, \n'
                          '\tbreak connection and delete some nodes..done'
                          )
                    cmds.delete(qTElr[0])
                    print('***' * 15 + '\n')
            # 継続して。。
            # 共通
            if not dCMtx:
                pass
                self.message_warning(u'decomposeMatrix 等のコネクションが見当たりません。'
                                     u'matrix を利用した ペアレントコンストレイン でない可能性が'
                                     u'充分考えられます。'
                                     )
            else:
                initT, initR, initS, initSH = [], [], [], []
                exist_initT = cmds.listAttr(sels[0], st = 'initT') or []
                if exist_initT:
                    initT = cmds.getAttr('{}.initT'.format(sels[0]))[0]
                exist_initR = cmds.listAttr(sels[0], st = 'initR') or []
                if exist_initR:
                    initR = cmds.getAttr('{}.initR'.format(sels[0]))[0]
                exist_initS = cmds.listAttr(sels[0], st = 'initS') or []
                if exist_initS:
                    initS = cmds.getAttr('{}.initS'.format(sels[0]))[0]
                exist_initSH = cmds.listAttr(sels[0], st = 'initSH') or []
                if exist_initSH:
                    initSH = cmds.getAttr('{}.initSH'.format(sels[0]))[0]
                if not exist_initT and not exist_initR and not exist_initS and not exist_initSH:
                    pass
                    self.message_warning(u'decomposeMatrix 等のコネクションは見当たるのですが、'
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
                    cmds.delete(dCMtx)
                    print('***' * 15 + '\n')

                    # reset attr, from user defined attr
                    print('***' * 15)
                    print('reset job, \n'
                          '\treset attr, from user defined attr..done'
                          )
                    for axis, para in zip(list('xyz'), initT):
                        cmds.setAttr('{}.t{}'.format(sels[0], axis), para)
                    for axis, para in zip(list('xyz'), initR):
                        cmds.setAttr('{}.r{}'.format(sels[0], axis), para)
                    for axis, para in zip(list('xyz'), initS):
                        cmds.setAttr('{}.s{}'.format(sels[0], axis), para)
                    for axis, para in zip(['xy', 'xz', 'yz'], initSH):
                        cmds.setAttr('{}.sh{}'.format(sels[0], axis), para)
                    print('***' * 15 + '\n')

                    # delete user defined attr
                    print('***' * 15)
                    print('delete job, \n'
                          '\tdelete user defined attr..done'
                          )
                    self.delInitAttr(sels[0])
                    print('***' * 15)

                    # 追加
                    tgt = sels[0]
                    self.commonResultPrintOut_brkAndRest_version(tgt)  # スクリプトベース 切断実行文を生成する関数
                    self.message(u'connection を全て削除しました。'
                                 u'また、当ツールを使用した、'
                                 u'parentConstraintByMatrix を実行する前の、ローカル数値への'
                                 u'リセットも行いました。'
                                 u'ご確認ください。'
                                 )
    # 切断編 <UI用> ######################################################### end
    # 3. UI-3. common ボタン コマンド群 ################################################### end

    # 5. スクリプトベースコマンド入力への対応 ############################################# start
    # 接続編 <スクリプトベース用> ########################################### start
    ##########################################
    # プロセスの大枠 #######
    #######################
    # <共通>
    #   接続 proc1.5.
    #       def command(self, ..):..
    # <共通>
    #   接続 proc2.
    #       def cnctSrcHircyTgtHircy2MltMat_exe(self, ..):..
    ##########################################

    # 接続編 <共通>
    # 接続 proc1.5. #
    # 新規のノード作成及び、source target の Rotate, Translate, Scale, Shear との接続を行う。
    # また、jointについては、jointOrient との接続もしている。
    # 辞書型引数を複数持つ、当関数 command を必ず経由します
    def command(self, *args, **kwargs):
        u""" < proc1.5.>

        ::

          新規のノード作成及び、source target の Rotate, Translate, Scale, Shear との接続を行う。
          < スクリプトベース用 > 接続編
            また、joint については、jointOrient との接続もしている。
                辞書型引数を複数持つ、当関数 command を必ず経由します。
                    proc2. へ渡る。

        #######################

        :param kwargs:
        - longName
            connect = bool, source = string, target = string
        - shortName
            ct = bool, src = string, tgt = string
        :type kwargs: dict

        ######################
        """
        print('\n' + '***' * 20)
        print('kwargs : {}'.format(kwargs))

        # connect
        key0 = list(kwargs.keys())[0]  # 変換箇所3
        val0 = kwargs.get(key0)
        # source
        key1 = list(kwargs.keys())[1]  # 変換箇所4
        val1 = kwargs.get(key1)
        # target
        key2 = list(kwargs.keys())[2]  # 変換箇所5
        val2 = kwargs.get(key2)

        connectAll = kwargs.get('connect', kwargs.get('ct', val0))  # longName shortName を考慮
        print('connect : {}'.format(connectAll))

        src = kwargs.get('source', kwargs.get('src', val1))  # longName shortName を考慮
        print('source : {}'.format(src))

        tgt = kwargs.get('target', kwargs.get('tgt', val2))  # longName shortName を考慮
        print('target : {}'.format(tgt))

        print('***' * 20 + '\n')

        self.cnctAll_value = connectAll
        self.src = src
        self.tgt = tgt
        self.outPutNode = ''
        self.inPutNode = ''

        if len(src) and len(tgt):  # src, tgt 共に入力セッティングされていれば、実行
            if connectAll:  # 全ての接続を実行
                print(u'source, target 共に set 入力されているため、継続実行しています。')
                strsCompLists = self.nodeName_decomp_exeB(src)  # under bar 3 or 2 version
                if strsCompLists is None:
                    strsCompLists = self.nodeName_decomp_exeC(src)  # no under bar version
                # print(strsCompLists)

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
                cmds.connectAttr('{}.matrixSum'.format(mM)
                                 , '{}.inputMatrix'.format(dM)
                                 , force = True
                                 )

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

                    # cmds.connectAttr("%s.outputRotateX" % qTEr, "%s.rotateX" % tgt, f = True)
                    # cmds.connectAttr("%s.outputRotateY" % qTEr, "%s.rotateY" % tgt, f = True)
                    # cmds.connectAttr("%s.outputRotateZ" % qTEr, "%s.rotateZ" % tgt, f = True)

                    self.outPutNode = qTEr
                    self.inPutNode = tgt
                    self.outPutNode2 = dM

                    print('***' * 15)
                    print('outPutNode : {}, inPutNode : {}'.format(qTEr, tgt))
                    print(self.outPutNode, self.inPutNode)
                    print('***' * 15)
                    print('Rotate connected..')
                    self.oP2iP_cnctR_exe(self.outPutNode, self.inPutNode)

                    print('outPutNode2 : {}, inPutNode : {}'.format(dM, tgt))
                    print(self.outPutNode2, self.inPutNode)
                    print('***' * 15)
                    print('Translate, Scale, Shear connected..')
                    self.oP2iP_cnctTSSh_exe(self.outPutNode2, self.inPutNode)

                    cmds.setAttr('{}.visibility'.format(dupTgt), 0)
                    # cmds.select(cl = True)
                    # 複製しておいた dupTgt は余計なので削除
                    cmds.delete(dupTgt)
                    newNodes.remove(dupTgt)  # リストからも削除する

                    # 全部選択
                    # print(u'新規で作成されたノードは %s です。' % newNodes)
                    cmds.select(newNodes, r = True)

                    self.newNodesAll = newNodes

                else:  # tgt が joint 以外の場合
                    # matrix を利用した parentConstraint を可能とするメイン関数
                    dupTgt, nodeAll = self.commonCommand(src, tgt, nodeAll)

                    # print(dupTgt)

                    # cmds.connectAttr("%s.outputRotateX" % dM, "%s.rotateX" % tgt, f = True)
                    # cmds.connectAttr("%s.outputRotateY" % dM, "%s.rotateY" % tgt, f = True)
                    # cmds.connectAttr("%s.outputRotateZ" % dM, "%s.rotateZ" % tgt, f = True)

                    self.outPutNode = dM
                    self.inPutNode = tgt

                    print('***' * 15)
                    print('outPutNode : {}, inPutNode : {}'.format(dM, tgt))
                    print(self.outPutNode, self.inPutNode)
                    print('***' * 15)
                    print('Rotate connected..')
                    self.oP2iP_cnctR_exe(self.outPutNode, self.inPutNode)

                    print('outPutNode : {}, inPutNode : {}'.format(dM, tgt))
                    print(self.outPutNode, self.inPutNode)
                    print('***' * 15)
                    print('Translate, Scale, Shear connected..')
                    self.oP2iP_cnctTSSh_exe(self.outPutNode, self.inPutNode)

                    cmds.setAttr('{}.visibility'.format(dupTgt), 0)
                    # cmds.select(cl = True)
                    # 複製しておいた dupTgt は余計なので削除
                    cmds.delete(dupTgt)
                    nodeAll.remove(dupTgt)  # リストからも削除する

                    # 全部選択
                    # print(u'新規で作成されたノードは %s です。' % nodeAll)
                    cmds.select(nodeAll, r = True)

                    self.newNodesAll = nodeAll
                # print(u'現在、新規で作成されたノードは、全て選択された状態です。')

                print('***' * 15)
                print(u'Rotate connected..done')
                print('***' * 15)
                print(u'Translate, Scale, Shear connected..done')
                print('***' * 15 + '\n')

                # proc2. へ渡る
                self.cnctSrcHircyTgtHircy2MltMat_exe()  # proc2. へ渡る
                print('***' * 15)
                print(u'Source Hierarchy, Target Hierarchy, to MultMatrix. connected..done')
                print('***' * 15 + '\n')

                # ######################################################################################
                # 追加 ###################################### start
                cmds.select(tgt)
                self.params = self.getInitAttr(tgt)
                print('***' * 15)
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

                self.commonResultPrintOut(connectAll, src, tgt)  # コマンドベースの実行文を生成する関数
                self.message(u'parentConstraint を'
                             u'matrix で実現'
                             u'完了しました。'
                             )
                self.__init__()  # すべて、元の初期値に戻す
            else:  # 継続実行中止
                pass
                self.commonResultPrintOut(connectAll, src, tgt)  # コマンドベースの実行文を生成する関数
                self.message_warning(u'create new nodes and connect all : check'
                                     u'ボタンが on されていないか、'
                                     u'もしくは、コマンド connect = True 記述がなさられていないため、'
                                     u'継続実行を中止しました。'
                                     )
        else:  # src, tgt 共に入力セッティングされていなければ、何もしない
            pass
            self.commonResultPrintOut(connectAll, src, tgt)  # コマンドベースの実行文を生成する関数
            self.message_warning(u'source, target 共に set 入力されていないため、'
                                 u'継続実行を中止しました。'
                                 )

    # 接続 proc2. #
    # source, target 階層側 と multMatrix のコネクションを行う(matrix 限定)
    def cnctSrcHircyTgtHircy2MltMat_exe(self, *args, **kwargs):
        u""" <proc2.>

        ::

          コマンドベース 接続編
            source, target 階層側 と multMatrix のコネクションを行う(matrix 限定)
                proc1.5 を経ています。
        """
        src = self.src
        tgt = self.tgt
        mM = self.mM
        self.srcP = cmds.listRelatives(src, p = True)[0]
        srcP = self.srcP
        self.followHierarchy_isConnected_ToF = cmds.isConnected('{}.matrix'.format(srcP)
                                                                ,
                                                                '{}.matrixIn[2]'.format(mM)
                                                                )
        # multMatrix の matrixIn[2] をトリガーとしています
        ToF = self.followHierarchy_isConnected_ToF
        # print(ToF)
        if not ToF:
            # cmds.connectAttr('%s.matrix' % srcP, '%s.matrixIn[2]' % mM, f = True)
            cmds.select(src, tgt, r = True)
            # print('mode = 0')
            self.main_followTheHierarchyAndConnection_exe()
            # 階層をたどり、接続の有無まで行う、最終接続 sub main 関数

    # スクリプトベース 接続実行文を生成する関数
    def commonResultPrintOut(self, connectValue, srcNode, tgtNode):
        u""" < コマンドベース 接続実行文を生成する関数 >

        #######################

        :param bool connectValue: 0 or 1
        :param string srcNode: コントローラ側
        :param string tgtNode: コントロールされる側

        #######################
        """
        moduleName = __name__
        # print(moduleName)
        className = self.classNameOutput()
        # print(className)
        # print(moduleName, className, connect, src, tgt)
        print(u'\n'
              u'// Result: {}.{}().command(connect = {}'
              u', source = \'{}\''
              u', target = \'{}\''
              u')'
              .format(moduleName, className
                      , connectValue, srcNode, tgtNode
                      )
              )  # longName を考慮
        print(u'\n'
              u'// Result: {}.{}().command(ct = {}'
              u', src = \'{}\''
              u', tgt = \'{}\''
              u')'
              .format(moduleName, className
                      , connectValue, srcNode, tgtNode
                      )
              )  # shortName を考慮
        print('')  # 改行の意
    # 接続編 ################################################################ end

    # 切断編 <スクリプトベース用> ############################################ start
    ##########################################
    # プロセスの大枠 #######
    #######################
    # 切断 proc1. break connections と reset 用
    #   def brkAndRest_command(self, ..):..
    # <共通>
    #   切断 proc2. UI Break and reset ボタン押下 実行 関数 を再利用
    #       def breakAndReset(self, ..):..
    ##########################################

    # 切断編 <スクリプトベース用>
    # 切断 proc1. #
    # break connections と reset 用
    def brkAndRest_command(self, *args, **kwargs):
        u""" <コマンドベース 切断編
        break connections と reset 用
        >
        """
        print('\n' + '***' * 20)
        print('kwargs : {}'.format(kwargs))
        # target
        key0 = list(kwargs.keys())[0]  # 変換箇所6
        val0 = kwargs.get(key0)

        tgt = kwargs.get('target', kwargs.get('tgt', val0))  # longName shortName を考慮
        print('target : {}'.format(tgt))

        print('***' * 20 + '\n')

        if len(tgt):  # tgt に入力セッティングされていれば、実行
            cmds.select(tgt)
            self.breakAndReset()
            self.__init__()  # すべて、元の初期値に戻す
        else:  # tgt に入力セッティングされていなければ、何もしない
            pass
            self.message_warning(u'target に set 入力されていないため、'
                                 u'継続実行を中止しました。')
        self.commonResultPrintOut_brkAndRest_version(tgt)  # コマンドベースの実行文を生成する関数

    # スクリプトベース 切断実行文を生成する関数
    def commonResultPrintOut_brkAndRest_version(self, tgtNode):
        u""" < コマンドベース 切断実行文を生成する関数 >

        #######################

        :param tgtNode:
        :type tgtNode: string

        #######################
        """
        moduleName = __name__
        # print(moduleName)
        className = self.classNameOutput()
        print(u'\n'
              u'// Result: {}.{}().brkAndRest_command('
              u'target = \'{}\''
              u')'
              .format(moduleName, className, tgtNode)
              )  # longName を考慮
        print(u'\n'
              u'// Result: {}.{}().brkAndRest_command('
              u'tgt = \'{}\''
              u')'
              .format(moduleName, className, tgtNode)
              )  # shortName を考慮
        print('')  # 改行の意
    # 切断編 ################################################################ end
    # 5. スクリプトベースコマンド入力への対応 ############################################### end

    # 独自規格 attribute 操作一連群 ################################################### start
    # 追加
    # get initial attribute
    def getInitAttr(self, tgt, *args):
        u""" <get initial attribute>

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
        u""" <add attribute, user defined initial attribute>

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
        u""" <store attribute, to user defined initial attribute>

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
        u""" <remove attribute, to user defined initial attribute>

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
    # 独自規格 attribute 操作一連群 ##################################################### end


class UI(UICmd):
    u"""< Widget class: 子クラス です >

    ::

      UIクラスです
      基本となる要素は以下の 6つ

    ######

        - UI-0. 重複しないウインドウ

        - UI-1. commonメニュー

        - UI-2. メインLayout + common情報 + 追加オプション

        - UI-3. ボタンLayout + common底面ボタン2つ

        - UI-4. OptionVar を利用したパラメータ管理

        - plug-in check

    ######
    """

    # A function to instantiate the UI window
    # UIウィンドウ をインスタンス化する関数
    @classmethod
    def showUI(cls):
        """A function to instantiate the YO makeSelection you chosen UI window
        :return: win
        """
        win = cls()
        win.createUI()
        # print(win)
        return win

    def classNameOutput(self):
        """
        :rtype: str
        :return: self.__class__.__name__
        """
        return self.__class__.__name__

    def __init__(self):
        u"""Initialize data attributes"""
        super(UI, self).__init__()  # python3系の記述: super().__init__()
        self.editMenuSave = None
        self.closeBtn = None

    def createUI(self):
        # if cmds.window(self.win, ex = True):
        #     cmds.deleteUI(self.win)

        # UI-0. 重複しないウインドウ
        try:
            cmds.deleteUI(self.win, window = True)
        except:
            pass

        cmds.window(self.win, title = title[3:] + space + version
                    , widthHeight = self.size
                    , menuBar = True, sizeable = True
                    , maximizeButton = False, minimizeButton = False
                    )

        # UI-1. commonメニュー
        # main ####################################################################### start
        editMenu = cmds.menu(l = 'Edit')
        self.editMenuSave = cmds.menuItem(l = 'Save Settings'
                                          , en = True
                                          , c = self.editMenuSaveCmd
                                          )
        editMenuReload = cmds.menuItem(l = 'Reset Settings'
                                       , c = self.editMenuReloadCmd
                                       , enable = True
                                       )
        editMenuClose = cmds.menuItem(l = 'Close This UI'
                                      , c = self.editMenuCloseCmd
                                      , enable = True
                                      )
        helpMenu = cmds.menu(l = 'Help')
        helpMenuItem = cmds.menuItem(l = 'Help on {}'.format(title)
                                     , c = self.helpMenuCmd
                                     )
        # main ######################################################################### end

        # UI-2. メインLayout + common情報 + 追加オプション
        # sub ######################################################################## start
        with LayoutManager(cmds.columnLayout(adjustableColumn = True)
                           ):
            cmds.separator()
            # UI-2. common情報
            cmds.text(l = u'parent constraint, scale constraint byMatrix ツール')
            cmds.text(l = u'note:'
                      , annotation = u'matrix を使用した、\n'
                                     u'parent constraint, scale constraint'
                                     u'を自動作成するツールです。'
                      , bgc = self.bgcBlue
                      )
        # UI-2. 追加オプション
        with LayoutManager(cmds.rowColumnLayout(
                numberOfColumns = 5
                , adjustableColumn = 2)
                           ):
            cmds.text(label = u'コントローラ側(source):', annotation = u"制御する側です")
            self.tFldA_set_src = cmds.textField('tFldA_set_src'
                                                , text = ''
                                                , annotation = u"制御する側\n"
                                                               u"コントローラです。 set 入力してください。"
                                                )
            cmds.button('tBtnA_set_src', l = 'Set'
                        , width = 20
                        , annotation = u'set'
                        , c = self.ui_tBtnA_set_src_exe
                        )
            cmds.button('tBtnA_sel_src', l = 'Sel'
                        , width = 18
                        , annotation = u'select set'
                        , enable = False
                        , c = self.ui_tBtnA_selSet_src_exe
                        )
            cmds.button('tBtnA_clr_src', l = 'C'
                        , width = 15
                        , annotation = u'clear set'
                        , enable = False
                        , c = self.ui_tBtnA_clrSet_src_exe
                        )
            cmds.text(label = u'コントロールされる側(target):', annotation = u"制御される側です")
            self.tFldB_set_tgt = cmds.textField('tFldB_set_tgt'
                                                , text = ''
                                                , annotation = u"制御される側\n"
                                                               u"コントロールされる方です。 拘束を必要とする方です。 set 入力してください。"
                                                )
            cmds.button('tBtnB_set_tgt', l = 'Set'
                        , width = 20
                        , annotation = u'set'
                        , c = self.ui_tBtnB_set_tgt_exe
                        )
            cmds.button('tBtnB_sel_tgt', l = 'Sel'
                        , width = 18
                        , annotation = u'select set'
                        , enable = False
                        , c = self.ui_tBtnB_selSet_tgt_exe
                        )
            cmds.button('tBtnB_clr_tgt', l = 'C'
                        , width = 15
                        , annotation = u'clear set'
                        , enable = False
                        , c = self.ui_tBtnB_clrSet_tgt_exe
                        )
        # UI-2. 追加オプション
        with LayoutManager(cmds.columnLayout(columnAttach = ['left', 30])
                           ):
            cmds.checkBox('cBox_cnctAll'
                          , l = u'create new nodes and connect all'
                          , value = True
                          )
        # UI-3. ボタンLayout + common底面ボタン2つ
        # UI-3. common底面ボタン2つ
        with LayoutManager(cmds.columnLayout(adjustableColumn = True)
                           ):
            cmds.button(l = 'Execute', bgc = self.bgcBlue2
                        , annotation = u'parentConstraint, scaleConstraint と'
                                       u'同等な拘束処理を\n'
                                       u'matrix 操作で実現します。'
                        , c = self.execute
                        )
            # 追加
            self.closeBtn = cmds.button(l = 'Close'
                                        , enable = True
                                        , h = 30
                                        , c = self.editMenuCloseCmd
                                        , vis = True
                                        )

        # break and reset ボタンLayout + ボタン1つ
        with LayoutManager(cmds.columnLayout(
                adjustableColumn = True
                , columnAttach = ['left', 100]
                                             )
                           ):
            cmds.button(l = 'break and reset'
                        , annotation = u'connection を全て削除し、\n'
                                       u'独自規格を利用して、\n実行する前の、ローカル数値にも'
                                       u'リセットいたします。'
                        , c = self.breakAndReset
                        )
        # sub ########################################################################## end

        # plug-in check
        print('\n' + '***' * 10)
        print('check plug-in job')
        self.checkMatNodePlugIn()
        self.checkQuatNodePlugIn()

        print('***' * 10 + '\n')

        # UI-4. OptionVar を利用したパラメータ管理
        restoreOptionVar = 'Restore Option Variables'
        self.restoreOptionVarCmd(restoreOptionVar)

        cmds.evalDeferred(lambda *args: cmds.showWindow(self.win))
        print('***' * 10 + '\n')

    # plug-in check ################################################################## start
    # matrixNodes系 plug-in の checkTool
    def checkMatNodePlugIn(self):
        u""" <matrixNodes(decomposeMatrix)系 plug-inのロード>
        """
        matNodePlugin = "matrixNodes"
        ToF = cmds.pluginInfo(matNodePlugin, q = True, l = True)
        if not ToF:
            cmds.loadPlugin(matNodePlugin)
            self.message(u"## check ##\n"
                         u"{} プラグインをロードしました。"
                         .format(matNodePlugin)
                         )
        else:
            pass
            self.message_warning(u'## check ##\n'
                                 u'{} プラグインは、既にロードされています。'
                                 .format(matNodePlugin)
                                 )

    # quatNodes系 plug-in の checkTool
    def checkQuatNodePlugIn(self):
        u""" <quatNodes系 plug-inのロード>
        """
        quatNodePlugin = "quatNodes"
        ToF = cmds.pluginInfo(quatNodePlugin, q = True, l = True)
        if not ToF:
            cmds.loadPlugin(quatNodePlugin)
            self.message(u"## check ##\n"
                         u"{} プラグインをロードしました。"
                         .format(quatNodePlugin)
                         )
        else:
            pass
            self.message_warning(u'## check ##\n'
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
