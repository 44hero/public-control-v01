# -*- coding: utf-8 -*-

u"""
YO_createSpIkAndRename3_Modl.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -3.1-
:Date: 2023/12/22

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

                  -     from YO_utilityTools.lib import ...
                  +     from ..lib import ...

                  -     from YO_utilityTools.renameTool.YO_renameTool5_Modl import RT_Modl
                  +     from ..renameTool.YO_renameTool5_Modl import RT_Modl

        version = '-3.1-'

    done: 2023//10/25
        汎用箇所を、モジュールとして読み込みに変更

        version = '-3.0-'

    done: 2023/09/13~2023/09/20
        - python2系 -> python3系 変換
            - 変換箇所
                - 概要: unicode関連
                    - 対象箇所
                        - # 分析2 n ###
                        - # 分析7 sj ###
                        - # 分析8 ee ###
                - 詳細: 以下参照
                ::

                  -
                            def analysis_strs_fromCmd3(self, mode, n, roc, pcv, ccv, scv, sj, ee, grp):
                                ...
                                #############################################
                                # 分析2 n ###
                                ...
                                patternC = re.compile(r'u\'(?P<ptnC>.*?)\'')  # 変更対象箇所
                                ...
                                #############################################
                                # 分析7 sj ###
                                ...
                                patternSj = re.compile(r'u\'(?P<ptnSjStr>.*?)\'')  # 変更対象箇所
                                ...
                                #############################################
                                # 分析8 ee ###
                                ...
                                patternEe = re.compile(r'u\'(?P<ptnEeStr>.*?)\'')  # 変更対象箇所
                                ...

                  +
                            def analysis_strs_fromCmd(self, mode, n):
                                ...
                                #############################################
                                # 分析2 n ###
                                ...
                                patternC = re.compile(r'\'(?P<ptnC>.*?)\'')  # 変更
                                ...
                                #############################################
                                # 分析7 sj ###
                                ...
                                patternSj = re.compile(r'\'(?P<ptnSjStr>.*?)\'')  # 変更
                                ...
                                #############################################
                                # 分析8 ee ###
                                ...
                                patternEe = re.compile(r'\'(?P<ptnEeStr>.*?)\'')  # 変更
                                ...

      version = '-2.0-'

    done: 2023/09/08~2023/09/13
        - 修正4
            - restore UI 時のバグ修正
                def restoreOptionVarCmd(self, *args):...
                ::

                  ...
                  # add start joint
                  ...
                  # 修正4
                  # button のステータスも加味
                  if len(tFld_key_stJt) and tFld_key_stJt != '...':
                      # UI 更新
                      self.setJtFld_staJt_setBtn.setEnable(False)
                      self.setJtFld_staJt_selBtn.setEnable(True)
                      self.setJtFld_staJt_clrBtn.setEnable(True)
                  if tFld_key_stJt == '...':
                      # UI 更新 default
                      self.setJtFld_staJt_setBtn.setEnable(True)
                      self.setJtFld_staJt_selBtn.setEnable(False)
                      self.setJtFld_staJt_clrBtn.setEnable(False)
                  ...
                  # add end joint
                  ...
                  # 修正4
                  # button のステータスも加味
                  if len(tFld_key_edJt) and tFld_key_edJt != '...':
                      # UI 更新
                      self.setJtFld_endJt_setBtn.setEnable(False)
                      self.setJtFld_endJt_selBtn.setEnable(True)
                      self.setJtFld_endJt_clrBtn.setEnable(True)
                  if tFld_key_edJt == '...':
                      self.setJtFld_endJt_setBtn.setEnable(True)
                      self.setJtFld_endJt_selBtn.setEnable(False)
                      self.setJtFld_endJt_clrBtn.setEnable(False)

        version = '-1.5-'

    done: 2023/05/25
        - 修正3
            - コマンド実行時、UI実行時 どちらでも
                splineIk 作成前に、シーン内の重複ノード名を検索判断する仕組みを修正

        version = '-1.2-'

    done: 2023/05/24
        - 追加2
            - restore時のボタンステータスの更新を追加
            - u'SpIk' popUp 入力への制限を追加
            - splineIk 作成前に、シーン内の重複ノード名を検索判断する仕組みを追加

        version = '-1.1-'

    done: 2023/04/12~2022/04/13
        新規

        version = '-1.0-'
"""

# 標準ライブラリ
import re
# from functools import partial  # partial 利用時は、最後の引数に、*args 要時あり
from collections import OrderedDict
from distutils.util import strtobool
# import pprint

# サードパーティライブラリ
import maya.cmds as cmds
# from pymel import core as pm
# import maya.OpenMaya as om

# ローカルで作成したモジュール
# basic_configuration_for_derivation(派生用の基本構成)
from .config import SPACE, TITLE, VERSION

# 汎用ライブラリー の使用 ################################################################ start
from ..lib.message import message
from ..lib.message_warning import message_warning
from ..lib.commonCheckJoint import commonCheckJoint  # :return: bool
from ..lib.commonCheckSelection import commonCheckSelection  # :return: string
# 個別ノードの持つ単独UUID番号、に対する独自操作 モジュール
# from ..lib.YO_uuID import UUID
# yo_uuid = UUID()

# ロギング用モジュール ##################################################### start
from ..lib.YO_logger2 import LogProcess_Output  # ログプロセス出力用クラス
YO_logProcess = LogProcess_Output()
# YO_logProcess.action(....) : 細かな情報出力、として利用しています

from ..lib import YO_logger2
# self.title, YO_logger2.getLineNo() : title名と行番号、を指し示す出力、として利用しています

from ..lib.YO_logger2 import Decorator  # ログデコレーター用クラス
# #############################
# 開発用(development)と、本番用(product) を共存させています
# 本コード内にある、
#   (@)instance.declogger
# がそれに相当します
# 以下のように、行のコメントアウトの有無で、開発用と本番用を区別出来ます
# 開発用:
#   (@)instance.declogger
# 本番用:
#   (#) (@)instance.declogger
# #############################
instance = Decorator()
# ロギング用モジュール ##################################################### end

# optionVar_command_library(optionVarを操作するライブラリー)
from ..lib.YO_optionVar import setOptionVarCmd  # オプション変数を設定する関数
from ..lib.YO_optionVar import getOptionVarCmd  # オプション変数を取得する関数
# from ..lib.YO_optionVar import upDateOptionVarsDictCmd  # オプション変数をdict操作し、更新をかける関数
# from ..lib.YO_optionVar import upDateOptionVarCmd  # オプション変数に更新をかける関数
# 汎用ライブラリー の使用 ################################################################## end


# mvc_model_module_that_become_derived_basis(派生基となるMVCモデルモジュール)
from ..renameTool.YO_renameTool5_Modl import RT_Modl


class CSpIkAndRT_Modl(RT_Modl):
    u""" < アプリケーションのデータモデルを表す Modelクラス です >

    ::

      データの取得や処理を行うためのメソッドを実装します。

      Modelクラスはアプリケーションの状態を表すデータフィールドを持ち、
        アプリケーションのロジックを実装するメソッドを提供します。

    ######

        構成要素は以下の9群
            - common コマンド群

            - コンストラクタのまとまり群

            - 1. UI-1. メニュー コマンド群
                一部ここ Model へ移動

            - 4. UI-4. OptionVar を利用したパラメータ管理 コマンド群

            - 2. UI-2. 追加オプション コマンド群

            - その他 アルゴリズムとなる コマンド群

            - 3. UI-3. common ボタン コマンド群

            - 5. スクリプトベースコマンド入力への対応

            - 「splineIK 作成と、naming の核となる コマンド群」

                - 共通な一連の関数のまとまり

                    - イレギュラー対応用

                - splineIK作成と naming を一遍に操作

    ######
    """
    def __init__(self):
        super(CSpIkAndRT_Modl, self).__init__()  # RT_Modl からの派生宣言

        # base から継承で、同じ内容だが新規扱い(override)
        self.constructor_chunk1()  # コンストラクタのまとまり1 # パッケージ名等の定義
        # base から継承で、同じ内容だが新規扱い(override)
        self.constructor_chunk2()  # コンストラクタのまとまり2 # タイトル等の定義

        # base から継承で再利用しているので不要
        # self.constructor_chunk3()  # コンストラクタのまとまり3 # その他の定義
        # self.constructor_chunk4()  # コンストラクタのまとまり4 # UIコントロールに関わる定義

        # 完全に新規
        self.constructor_chunk5()  # コンストラクタのまとまり5 # UIコントロールに関わる定義の追加
        # 完全に新規
        self.constructor_chunk6()  # コンストラクタのまとまり5 # その他の定義の追加

        # base から継承 override 変更 (独自に定義しなおして上書き)
        self.settingOptionVar()  # コンストラクタのまとまりA # optionVar のセッティング
        # base から継承 override 変更 (独自に定義しなおして上書き)
        self.startOptionVarCmd()  # コンストラクタのまとまりB # optionVar の初期実行コマンド

        # self.options = pm.optionVar  # type: # OptionVarDict
        # self.options = upDateOptionVarsDictCmd()  # type: # dict

    # common コマンド群 ################################################################ start
    # 完全に新規
    # selection が joint かどうか調べる関数
    # rom YO_utilityTools.lib.commonCheckJoint import commonCheckJoint へ移動...
    # common コマンド群 ################################################################## end

    # コンストラクタのまとまり群 ######################################################### start
    # base から継承で、同じ内容だが新規扱い(override)
    # コンストラクタのまとまり1 # パッケージ名等の定義
    def constructor_chunk1(self):
        u""" < コンストラクタのまとまり1 # パッケージ名等の定義 です >

        ::

          base から継承で、同じ内容だが新規扱い(override)

        #######################
        """
        self.pkgName = __package__
        self.id = '_Modl'

    # base から継承で、同じ内容だが新規扱い(override)
    # コンストラクタのまとまり2 # タイトル等の定義
    def constructor_chunk2(self):
        u""" < コンストラクタのまとまり2 # タイトル等の定義 です >

        ::

          base から継承で、同じ内容だが新規扱い(override)

        #######################
        """
        self.title = TITLE
        # self.win = TITLE + '_ui'
        # self.space = SPACE
        # self.version = VERSION
        self.underScore = '_'

    # base から継承で再利用しているので不要
    # コンストラクタのまとまり3 # その他の定義
    # def constructor_chunk3(self):
    #     u""" < コンストラクタのまとまり3 # その他の定義 です > """
    #     pass

    # base から継承で再利用しているので不要
    # コンストラクタのまとまり4 # UIコントロールに関わる定義
    # def constructor_chunk3(self):
    #     u""" < コンストラクタのまとまり3 # UIコントロールに関わる定義 です > """
    #     pass

    # 完全に新規
    # コンストラクタのまとまり5 # UIコントロールに関わる定義の追加
    def constructor_chunk5(self):
        u""" < コンストラクタのまとまり5 # UIコントロールに関わる定義の追加 です >

        ::

          完全に新規

        #######################
        """
        self.bgcGray2 = [0.4, 0.4, 0.4]  # list of float
        self.bgcBlue = [0.5, 0.5, 0.9]  # list of float
        self.bgcGray = [0.7, 0.7, 0.7]  # list of float

        self.spIKHndle_name = ''

        # add
        # start joint, end joint 登録用 各button名
        self.setJtFld_staJt_setBtn = None
        self.setJtFld_staJt_selBtn = None
        self.setJtFld_staJt_clrBtn = None
        self.setJtFld_endJt_setBtn = None
        self.setJtFld_endJt_selBtn = None
        self.setJtFld_endJt_clrBtn = None

        # add textField
        # splineIKのparent先 textFiled名
        self.ikSpHdleSetting_pcv_txtFld = None

        # add textField
        # final naming check 各text名
        self.cTxt_spIKHndle_ckName = None
        self.cTxt_spIKCrv_ckName = None

    # 完全に新規
    # コンストラクタのまとまり6 # その他の定義の追加
    def constructor_chunk6(self):
        u""" < コンストラクタのまとまり6 # その他の定義 の追加です >

        ::

          完全に新規

        #######################
        """
        self.runInUiOrCommand = str  # 'fromCmd' or 'fromUI'

        self.currentCbx_roc = bool
        self.currentCbx_pcv = bool
        self.currentCbx_ccv = bool
        self.currentCbx_scv = bool
        self.getStaNodeName_fromUI = str
        self.getEndNodeName_fromUI = str
        self.currentCbx_grp = bool

        self.roc_fromCmd = bool
        self.pcv_fromCmd = bool
        self.ccv_fromCmd = bool
        self.scv_fromCmd = bool
        self.sj_fromCmd = str
        self.ee_fromCmd = str
        self.grp_fromCmd = bool

        # ikスプラインハンドル設定の各フラグ引数を照会し、辞書化する(順番保持版)
        # Queries each flag argument of the ik spline handle setting and dictionaries
        self.qEhFlgArgDict_ikSpHdlSttng = \
            OrderedDict(roc = False, pcv = False, ccv = True, scv = True, grp = True)

    # base から継承 override 変更 (独自に定義しなおして上書き)
    # コンストラクタのまとまりA # optionVar のセッティング
    def settingOptionVar(self):
        u""" < コンストラクタのまとまりA # optionVar のセッティング です >

        ::

          base から継承 override 変更 (独自に定義しなおして上書き)

        #######################
        """
        # dict  # range is 2 + # range is 6 + # range is 1 + # range is 4 + # range is 1
        # key:   [type(str), type(str)  # range is 2
        # , type(str), type(str), type(str), type(str), type(str)  # range is 6
        # , type(str)  # range is 1
        # , type(str), type(str), type(str), type(str)  # range is 4
        # , type(str)  # range is 1
        # ]
        # value: [type(str), type(str)  # range is 2
        # , type(str), type(str), type(str), type(str), type(str)   + # range is 6
        # , type(bool)  # range is 1
        # , type(bool), type(bool), type(bool), type(bool)  # range is 4
        # , type(bool)  # range is 1
        # ]

        # add start joint, end joint
        # range is 2
        self.opVar_dictVal_def_list_addCSpIkAndR_0 = ['...', '...']  # range is 2
        # value: [type(str), type(str)]  # range is 2

        # range is 6
        self.opVar_dictVal_dflt_list = ['mode0'
            , '', 'spIKHndle', '', '', ''
                                        ]  # range is 6
        # value: [type(str)
        #          , type(str), type(str), type(str), type(str), type(str)
        #         ]  # range is 6

        # add autoNumbering
        # range is 1
        self.opVar_dictVal_def_list_addCSpIkAndR_1 = ['False']  # range is 1
        # value: [type(bool)]  # range is 1

        # add rootOnCurve(roc), parentCurve(pcv), createCurve(ccv), simplifyCurve(scv)
        # range is 4
        self.opVar_dictVal_def_list_addCSpIkAndR_2 = ['False', 'False', 'True', 'True']  # range is 4
        # value: [type(bool) type(bool), type(bool), type(bool)]  # range is 4

        # add grouping
        # range is 1
        self.opVar_dictVal_def_list_addCSpIkAndR_3 = ['True']  # range is 1
        # value: [type(bool)]  # range is 1

        # OptionVar DATA naming ########################################################### start
        # save settings menu により、maya optionVar への 辞書登録を実施する準備です
        # dict  # range is 2 + # range is 6 + # range is 1 + # range is 4 + # range is 1
        # key:   [type(str), type(str)  # range is 2
        # , type(str), type(str), type(str), type(str), type(str)  # range is 6
        # , type(str)  # range is 1
        # , type(str), type(str), type(str), type(str)  # range is 4
        # , type(str)  # range is 1
        # ]
        # value: [type(str), type(str)  # range is 2
        # , type(str), type(str), type(str), type(str), type(str)   + # range is 6
        # , type(bool)  # range is 1
        # , type(bool), type(bool), type(bool), type(bool)  # range is 4
        # , type(bool)  # range is 1
        # ]

        # add start joint, end joint
        # range is 2
        self.optionVar01Jt_tFld_key = self.title + self.underScore + 'txtFld_stJt_text'  # type: str
        self.optionVar02Jt_tFld_key = self.title + self.underScore + 'txtFld_edJt_text'  # type: str

        # range is 6
        self.optionVar01_mode_key = self.title + self.underScore + 'rdBtn_text'  # type: str
        self.optionVar01_tFld_key = self.title + self.underScore + 'txtFldA1_text'  # type: str
        self.optionVar02_tFld_key = self.title + self.underScore + 'txtFldB1_text'  # type: str
        self.optionVar03_tFld_key = self.title + self.underScore + 'txtFldC1_text'  # type: str
        self.optionVar04_tFld_key = self.title + self.underScore + 'txtFldC2_text'  # type: str
        self.optionVar05_tFld_key = self.title + self.underScore + 'txtFldC3_text'  # type: str

        # add autoNumbering
        # range is 1
        self.optionVar01_atNm_key = self.title + self.underScore + 'rdBtnA_bool'  # type: str

        # add rootOnCurve(roc), parentCurve(pcv), createCurve(ccv), simplifyCurve(scv)
        # range is 4
        self.optionVar01IKSttng_roc_key = self.title + self.underScore + 'rdBtnB1_bool'  # type: str
        self.optionVar01IKSttng_pcv_key = self.title + self.underScore + 'rdBtnB2_bool'  # type: str
        self.optionVar01IKSttng_ccv_key = self.title + self.underScore + 'rdBtnB3_bool'  # type: str
        self.optionVar01IKSttng_scv_key = self.title + self.underScore + 'rdBtnB4_bool'  # type: str

        # add grouping
        # range is 1
        self.optionVar01IKSttng_grp_key = self.title + self.underScore + 'rdBtnC1_bool'  # type: str
        # OptionVar DATA naming ########################################################### end

    # base から継承 override 変更 (独自に定義しなおして上書き)
    # コンストラクタのまとまりB # optionVar の初期実行コマンド
    def startOptionVarCmd(self):
        u""" < コンストラクタのまとまりB # optionVar の初期実行コマンド です >

        ::

          base から継承 override 変更 (独自に定義しなおして上書き)

        #######################
        """
        # add start joint
        self.setJtFld_staJt_txtFld = None  # type: pm.textField
        # #######################
        # 補足 #
        # 初めてmayaで実行すると、optionVar は辞書なので
        # 「"YO_createSpIkAndRename2_PyMel_txtFld_stJt_text'"というkeyが初めて実行されてるから無いよ！」
        # というエラーが出るのでそれを回避しています
        # #######################
        if getOptionVarCmd(self.optionVar01Jt_tFld_key) is None:  # set default
            setOptionVarCmd(self.optionVar01Jt_tFld_key, self.opVar_dictVal_def_list_addCSpIkAndR_0[0])
            # self.options[self.optionVar01Jt_tFld_key] = self.opVar_dictVal_def_list_addCSpIkAndR_0[0]  # dict type(value): str

        # add end joint
        self.setJtFld_endJt_txtFld = None  # type: pm.textField
        # #######################
        # 補足 #
        # 初めてmayaで実行すると、optionVar は辞書なので
        # 「"YO_createSpIkAndRename2_PyMel_txtFld_edJt_text'"というkeyが初めて実行されてるから無いよ！」
        # というエラーが出るのでそれを回避しています
        # #######################
        if getOptionVarCmd(self.optionVar02Jt_tFld_key) is None:  # set default
            setOptionVarCmd(self.optionVar02Jt_tFld_key, self.opVar_dictVal_def_list_addCSpIkAndR_0[1])
            # self.options[self.optionVar02Jt_tFld_key] = self.opVar_dictVal_def_list_addCSpIkAndR_0[1]  # dict type(value): str

        # mode_key
        self.cmnModeRdBtnClcton = None  # type: pm.radioCollection
        # #######################
        # 補足 #
        # 初めてmayaで実行すると、optionVar は辞書なので
        # 「"YO_renameTool4_PyMel_rdBtn_text"というkeyが初めて実行されてるから無いよ！」
        # というエラーが出るのでそれを回避しています
        # #######################
        if getOptionVarCmd(self.optionVar01_mode_key) is None:  # set default
            setOptionVarCmd(self.optionVar01_mode_key, self.opVar_dictVal_dflt_list[0])
            # self.options[self.optionVar01_mode_key] = self.opVar_dictVal_def_list[0]  # dict type(value): str

        # tFld_key A1
        self.cmnTxtFld_A1 = None  # type: pm.textField
        # #######################
        # 補足 #
        # 初めてmayaで実行すると、optionVar は辞書なので
        # 「"YO_renameTool4_PyMel_txtFldA1_text"というkeyが初めて実行されてるから無いよ！」
        # というエラーが出るのでそれを回避しています
        # #######################
        if getOptionVarCmd(self.optionVar01_tFld_key) is None:  # set default
            setOptionVarCmd(self.optionVar01_tFld_key, self.opVar_dictVal_dflt_list[1])
            # self.options[self.optionVar01_tFld_key] = self.opVar_dictVal_def_list[1]  # dict type(value): str

        # tFld_key B1
        self.cmnTxtFld_B1 = None  # type: pm.textField
        # #######################
        # 補足 #
        # 初めてmayaで実行すると、optionVar は辞書なので
        # 「"YO_renameTool4_PyMel_txtFldB1_text"というkeyが初めて実行されてるから無いよ！」
        # というエラーが出るのでそれを回避しています
        # #######################
        if getOptionVarCmd(self.optionVar02_tFld_key) is None:  # set default
            setOptionVarCmd(self.optionVar02_tFld_key, self.opVar_dictVal_dflt_list[2])
            # self.options[self.optionVar02_tFld_key] = self.opVar_dictVal_def_list[2]  # dict type(value): str

        # tFld_key C1
        self.cmnTxtFld_C1 = None  # type: pm.textField
        # #######################
        # 補足 #
        # 初めてmayaで実行すると、optionVar は辞書なので
        # 「"YO_renameTool4_PyMel_txtFldC1_text"というkeyが初めて実行されてるから無いよ！」
        # というエラーが出るのでそれを回避しています
        # #######################
        if getOptionVarCmd(self.optionVar03_tFld_key) is None:  # set default
            setOptionVarCmd(self.optionVar03_tFld_key, self.opVar_dictVal_dflt_list[3])
            # self.options[self.optionVar03_tFld_key] = self.opVar_dictVal_def_list[3]  # dict type(value): str

        # tFld_key C2
        self.cmnTxtFld_C2 = None  # type: pm.textField
        # #######################
        # 補足 #
        # 初めてmayaで実行すると、optionVar は辞書なので
        # 「"YO_renameTool4_PyMel_txtFldC2_text"というkeyが初めて実行されてるから無いよ！」
        # というエラーが出るのでそれを回避しています
        # #######################
        if getOptionVarCmd(self.optionVar04_tFld_key) is None:  # set default
            setOptionVarCmd(self.optionVar04_tFld_key, self.opVar_dictVal_dflt_list[4])
            # self.options[self.optionVar04_tFld_key] = self.opVar_dictVal_def_list[4]  # dict type(value): str

        # tFld_key C3
        self.cmnTxtFld_C3 = None  # type: pm.textField
        # #######################
        # 補足 #
        # 初めてmayaで実行すると、optionVar は辞書なので
        # 「"YO_renameTool4_PyMel_txtFldC2_text"というkeyが初めて実行されてるから無いよ！」
        # というエラーが出るのでそれを回避しています
        # #######################
        if getOptionVarCmd(self.optionVar05_tFld_key) is None:  # set default
            setOptionVarCmd(self.optionVar05_tFld_key, self.opVar_dictVal_dflt_list[5])
            # self.options[self.optionVar05_tFld_key] = self.opVar_dictVal_def_list[5]  # dict type(value): str

        # add autoNumbering
        self.autoNumbering_ckBx = None  # type: pm.checkBox
        # #######################
        # 補足 #
        # 初めてmayaで実行すると、optionVar は辞書なので
        # 「"YO_createSpIkAndRename2_PyMel_rdBtnA_bool"というkeyが初めて実行されてるから無いよ！」
        # というエラーが出るのでそれを回避しています
        # #######################
        if getOptionVarCmd(self.optionVar01_atNm_key) is None:  # set default
            setOptionVarCmd(self.optionVar01_atNm_key, self.opVar_dictVal_def_list_addCSpIkAndR_1[0])
            # self.options[self.optionVar01_atNm_key] = self.opVar_dictVal_def_list_addCSpIkAndR_1[0]  # dicttype(value): bool

        # add rootOnCurve(roc)
        self.ikSpHdleSetting_rootOnCurve_ckBx = None  # type: pm.checkBox
        # #######################
        # 補足 #
        # 初めてmayaで実行すると、optionVar は辞書なので
        # 「"YO_createClusterAndRename5_PyMel_rdBtnB1_bool"というkeyが初めて実行されてるから無いよ！」
        # というエラーが出るのでそれを回避しています
        # #######################
        if getOptionVarCmd(self.optionVar01IKSttng_roc_key) is None:  # set default
            setOptionVarCmd(self.optionVar01IKSttng_roc_key, self.opVar_dictVal_def_list_addCSpIkAndR_2[0])
            # self.options[self.optionVar01IKSttng_roc_key] = self.opVar_dictVal_def_list_addCSpIkAndR_2[0]  # dict type(value): bool

        # add parentCurve(pcv)
        self.ikSpHdleSetting_parentCurve_ckBx = None  # type: pm.checkBox
        # #######################
        # 補足 #
        # 初めてmayaで実行すると、optionVar は辞書なので
        # 「"YO_createClusterAndRename5_PyMel_rdBtnB2_bool"というkeyが初めて実行されてるから無いよ！」
        # というエラーが出るのでそれを回避しています
        # #######################
        if getOptionVarCmd(self.optionVar01IKSttng_pcv_key) is None:  # set default
            setOptionVarCmd(self.optionVar01IKSttng_pcv_key, self.opVar_dictVal_def_list_addCSpIkAndR_2[1])
            # self.options[self.optionVar01IKSttng_pcv_key] = self.opVar_dictVal_def_list_addCSpIkAndR_2[1]  # dict type(value): bool

        # add createCurve(ccv)
        self.ikSpHdleSetting_createCurve_ckBx = None  # type: pm.checkBox
        # #######################
        # 補足 #
        # 初めてmayaで実行すると、optionVar は辞書なので
        # 「"YO_createClusterAndRename5_PyMel_rdBtnB3_bool"というkeyが初めて実行されてるから無いよ！」
        # というエラーが出るのでそれを回避しています
        # #######################
        if getOptionVarCmd(self.optionVar01IKSttng_ccv_key) is None:  # set default
            setOptionVarCmd(self.optionVar01IKSttng_ccv_key, self.opVar_dictVal_def_list_addCSpIkAndR_2[2])
            # self.options[self.optionVar01IKSttng_ccv_key] = self.opVar_dictVal_def_list_addCSpIkAndR_2[2]  # dict type(value): bool

        # add simplifyCurve(scv)
        self.ikSpHdleSetting_simplifyCurve_ckBx = None  # type: pm.checkBox
        # #######################
        # 補足 #
        # 初めてmayaで実行すると、optionVar は辞書なので
        # 「"YO_createClusterAndRename5_PyMel_rdBtnB4_bool"というkeyが初めて実行されてるから無いよ！」
        # というエラーが出るのでそれを回避しています
        # #######################
        if getOptionVarCmd(self.optionVar01IKSttng_scv_key) is None:  # set default
            setOptionVarCmd(self.optionVar01IKSttng_scv_key, self.opVar_dictVal_def_list_addCSpIkAndR_2[3])
            # self.options[self.optionVar01IKSttng_scv_key] = self.opVar_dictVal_def_list_addCSpIkAndR_2[3]  # dict type(value): bool

        # add grouping
        self.ikSpHdleSetting_grouping_ckBx = None  # type: pm.checkBox
        # #######################
        # 補足 #
        # 初めてmayaで実行すると、optionVar は辞書なので
        # 「"YO_createClusterAndRename5_PyMel_rdBtnB1_bool"というkeyが初めて実行されてるから無いよ！」
        # というエラーが出るのでそれを回避しています
        # #######################
        if getOptionVarCmd(self.optionVar01IKSttng_grp_key) is None:  # set default
            setOptionVarCmd(self.optionVar01IKSttng_grp_key, self.opVar_dictVal_def_list_addCSpIkAndR_3[0])
            # self.options[self.optionVar01IKSttng_grp_key] = self.opVar_dictVal_def_list_addCSpIkAndR_3[0]  # dict type(value): bool
        # OptionVar DATAの初期化 #################################################### end
    # コンストラクタのまとまり群 ########################################################### end

    # 1. UI-1. メニュー コマンド群 ###################################################### start
    # base から継承 override 変更 (独自に定義しなおして上書き)
    # Save Settings 実行による optionVar の保存 関数
    def editMenuSaveSettingsCmd(self, *args):
        u""" < Save Settings 実行による optionVar の保存 関数 です >

        ::

          base から継承 override 変更 (独自に定義しなおして上書き)

        """
        # add start joint
        # tFld_key stJt
        # self.options へ ["YO_createSpIkAndRename2_PyMel_txtFld_stJt_text"] を保存
        getTxt_fromTxtFld_stJt = self.setJtFld_staJt_txtFld.getText()
        # self.options[self.optionVar01Jt_tFld_key] = getTxt_fromTxtFld_stJt
        setOptionVarCmd(self.optionVar01Jt_tFld_key, getTxt_fromTxtFld_stJt)

        # add end joint
        # tFld_key edJt
        # self.options へ ["YO_createSpIkAndRename2_PyMel_txtFld_edJt_text"] を保存
        getTxt_fromTxtFld_edJt = self.setJtFld_endJt_txtFld.getText()
        # self.options[self.optionVar02Jt_tFld_key] = getTxt_fromTxtFld_edJt
        setOptionVarCmd(self.optionVar02Jt_tFld_key, getTxt_fromTxtFld_edJt)

        # mode_key
        # self.options へ ["YO_createClusterAndRename5_PyMel_rdBtn_text"] を保存
        getSel_fromRdBtn = self.cmnModeRdBtnClcton.getSelect()
        # self.options[self.optionVar01_mode_key] = getSel_fromRdBtn
        setOptionVarCmd(self.optionVar01_mode_key, getSel_fromRdBtn)

        # tFld_key A1
        # self.options へ ["YO_createClusterAndRename5_PyMel_txtFldA1_text"] を保存
        getTxt_fromTxtFldA1 = self.cmnTxtFld_A1.getText()
        # self.options[self.optionVar01_tFld_key] = getTxt_fromTxtFldA1
        setOptionVarCmd(self.optionVar01_tFld_key, getTxt_fromTxtFldA1)

        # tFld_key B1
        # self.options へ ["YO_createClusterAndRename5_PyMel_txtFldB1_text"] を保存
        getTxt_fromTxtFldB1 = self.cmnTxtFld_B1.getText()
        # self.options[self.optionVar02_tFld_key] = getTxt_fromTxtFldB1
        setOptionVarCmd(self.optionVar02_tFld_key, getTxt_fromTxtFldB1)

        # tFld_key C1
        # self.options へ ["YO_createClusterAndRename5_PyMel_txtFldC1_text"] を保存
        getTxt_fromTxtFldC1 = self.cmnTxtFld_C1.getText()
        # self.options[self.optionVar03_tFld_key] = getTxt_fromTxtFldC1
        setOptionVarCmd(self.optionVar03_tFld_key, getTxt_fromTxtFldC1)

        # tFld_key C2
        # self.options へ ["YO_createClusterAndRename5_PyMel_txtFldC2_text"] を保存
        getTxt_fromTxtFldC2 = self.cmnTxtFld_C2.getText()
        # self.options[self.optionVar04_tFld_key] = getTxt_fromTxtFldC2
        setOptionVarCmd(self.optionVar04_tFld_key, getTxt_fromTxtFldC2)

        # tFld_key C3
        # self.options へ ["YO_createClusterAndRename5_PyMel_txtFldC3_text"] を保存
        getTxt_fromTxtFldC3 = self.cmnTxtFld_C3.getText()
        # self.options[self.optionVar05_tFld_key] = getTxt_fromTxtFldC3
        setOptionVarCmd(self.optionVar05_tFld_key, getTxt_fromTxtFldC3)

        # add autoNumbering
        # atNm_key
        # self.options へ ["YO_createSpIkAndRename2_PyMel_rdBtnA_bool"] を保存
        getVal_fromRdBtnA = self.autoNumbering_ckBx.getValue()
        # self.options[self.optionVar01_atNm_key] = getVal_fromRdBtnA
        setOptionVarCmd(self.optionVar01_atNm_key, getVal_fromRdBtnA)

        # add rootOnCurve(roc)
        # roc_key
        # self.options へ ["YO_createSpIkAndRename2_PyMel_rdBtnB1_bool"] を保存
        getVal_fromRdBtnB1 = self.ikSpHdleSetting_rootOnCurve_ckBx.getValue()
        # self.options[self.optionVar01IKSttng_roc_key] = getVal_fromRdBtnB1
        setOptionVarCmd(self.optionVar01IKSttng_roc_key, getVal_fromRdBtnB1)

        # add parentCurve(pcv)
        # pcv_key
        # self.options へ ["YO_createSpIkAndRename2_PyMel_rdBtnB2_bool"] を保存
        getVal_fromRdBtnB2 = self.ikSpHdleSetting_parentCurve_ckBx.getValue()
        # self.options[self.optionVar01IKSttng_pcv_key] = getVal_fromRdBtnB2
        setOptionVarCmd(self.optionVar01IKSttng_pcv_key, getVal_fromRdBtnB2)

        # add createCurve(ccv)
        # ccv_key
        # self.options へ ["YO_createSpIkAndRename2_PyMel_rdBtnB3_bool"] を保存
        getVal_fromRdBtnB3 = self.ikSpHdleSetting_createCurve_ckBx.getValue()
        # self.options[self.optionVar01IKSttng_ccv_key] = getVal_fromRdBtnB3
        setOptionVarCmd(self.optionVar01IKSttng_ccv_key, getVal_fromRdBtnB3)

        # add simplifyCurve(scv)
        # scv_key
        # self.options へ ["YO_createSpIkAndRename2_PyMel_rdBtnB4_bool"] を保存
        getVal_fromRdBtnB4 = self.ikSpHdleSetting_simplifyCurve_ckBx.getValue()
        # self.options[self.optionVar01IKSttng_scv_key] = getVal_fromRdBtnB4
        setOptionVarCmd(self.optionVar01IKSttng_scv_key, getVal_fromRdBtnB4)

        # add grouping
        # grp_key
        # self.options へ ["YO_createSpIkAndRename2_PyMel_rdBtnC1_bool"] を保存
        getVal_fromRdBtnC1 = self.ikSpHdleSetting_grouping_ckBx.getValue()
        # self.options[self.optionVar01IKSttng_grp_key] = getVal_fromRdBtnC1
        setOptionVarCmd(self.optionVar01IKSttng_grp_key, getVal_fromRdBtnC1)

        message(args[0])

        print(getTxt_fromTxtFld_stJt, getTxt_fromTxtFld_edJt
              , getSel_fromRdBtn
              , getTxt_fromTxtFldA1, getTxt_fromTxtFldB1
              , getTxt_fromTxtFldC1, getTxt_fromTxtFldC2, getTxt_fromTxtFldC3
              , getVal_fromRdBtnA
              , getVal_fromRdBtnB1, getVal_fromRdBtnB2
              , getVal_fromRdBtnB3, getVal_fromRdBtnB4
              , getVal_fromRdBtnC1
              )

    # Reload 実行 関数
    # View へ移動...

    # Help 実行 関数
    # View へ移動...

    # Close 実行 関数
    # View へ移動...
    # 1. UI-1. メニュー コマンド群 ######################################################## end

    # 4. UI-4. OptionVar を利用したパラメータ管理 コマンド群 ############################## start
    # base から継承 override 変更 (独自に定義しなおして上書き)
    # optionVar からの値の復元 実行 関数
    def restoreOptionVarCmd(self, *args):
        u""" < optionVar からの値の復元 実行 関数です >

        ::

          base から継承 override 変更 (独自に定義しなおして上書き)

        """
        # add start joint
        # tFld_key_stJt
        tFld_key_stJt = getOptionVarCmd(self.optionVar01Jt_tFld_key)
        # self.setJtFld_staJt_txtFld.setText(self.options[self.optionVar01Jt_tFld_key])
        self.setJtFld_staJt_txtFld.setText(tFld_key_stJt)
        # 修正4
        # button のステータスも加味
        if len(tFld_key_stJt) and tFld_key_stJt != '...':
            # UI 更新
            self.setJtFld_staJt_setBtn.setEnable(False)
            self.setJtFld_staJt_selBtn.setEnable(True)
            self.setJtFld_staJt_clrBtn.setEnable(True)
        if tFld_key_stJt == '...':
            # UI 更新 default
            self.setJtFld_staJt_setBtn.setEnable(True)
            self.setJtFld_staJt_selBtn.setEnable(False)
            self.setJtFld_staJt_clrBtn.setEnable(False)

        # add end joint
        # tFld_key_edJt
        tFld_key_edJt = getOptionVarCmd(self.optionVar02Jt_tFld_key)
        # self.setJtFld_endJt_txtFld.setText(self.options[self.optionVar02Jt_tFld_key])
        self.setJtFld_endJt_txtFld.setText(tFld_key_edJt)
        # 修正4
        # button のステータスも加味
        if len(tFld_key_edJt) and tFld_key_edJt != '...':
            # UI 更新
            self.setJtFld_endJt_setBtn.setEnable(False)
            self.setJtFld_endJt_selBtn.setEnable(True)
            self.setJtFld_endJt_clrBtn.setEnable(True)
        if tFld_key_edJt == '...':
            self.setJtFld_endJt_setBtn.setEnable(True)
            self.setJtFld_endJt_selBtn.setEnable(False)
            self.setJtFld_endJt_clrBtn.setEnable(False)

        # mode_key
        mode_key = getOptionVarCmd(self.optionVar01_mode_key)
        # self.cmnModeRdBtnClcton.setSelect(self.options[self.optionVar01_mode_key])
        self.cmnModeRdBtnClcton.setSelect(mode_key)

        # tFld_key_A1
        tFld_key_A1 = getOptionVarCmd(self.optionVar01_tFld_key)
        # self.cmnTxtFld_A1.setText(self.options[self.optionVar01_tFld_key])
        self.cmnTxtFld_A1.setText(tFld_key_A1)
        # font 変更も加味
        if len(tFld_key_A1):
            self.cmnTxtFld_A1.setFont(self.defaultFont)

        # tFld_key_B1
        tFld_key_B1 = getOptionVarCmd(self.optionVar02_tFld_key)
        # self.cmnTxtFld_B1.setText(self.options[self.optionVar02_tFld_key])
        self.cmnTxtFld_B1.setText(tFld_key_B1)
        # font 変更も加味
        if len(tFld_key_B1):
            self.cmnTxtFld_B1.setFont(self.defaultFont)

        # tFld_key_C1
        tFld_key_C1 = getOptionVarCmd(self.optionVar03_tFld_key)
        # self.cmnTxtFld_C1.setText(self.options[self.optionVar03_tFld_key])
        self.cmnTxtFld_C1.setText(tFld_key_C1)
        # font 変更も加味
        if len(tFld_key_C1):
            self.cmnTxtFld_C1.setFont(self.defaultFont)

        # tFld_key_C2
        tFld_key_C2 = getOptionVarCmd(self.optionVar04_tFld_key)
        # self.cmnTxtFld_C2.setText(self.options[self.optionVar04_tFld_key])
        self.cmnTxtFld_C2.setText(tFld_key_C2)
        # font 変更も加味
        if len(tFld_key_C2):
            self.cmnTxtFld_C2.setFont(self.defaultFont)

        # tFld_key_C3
        tFld_key_C3 = getOptionVarCmd(self.optionVar05_tFld_key)
        # self.cmnTxtFld_C3.setText(self.options[self.optionVar05_tFld_key])
        self.cmnTxtFld_C3.setText(tFld_key_C3)
        # font 変更も加味
        if len(tFld_key_C3):
            self.cmnTxtFld_C3.setFont(self.defaultFont)

        # add autoNumbering
        # atNm_key
        atNm_key = getOptionVarCmd(self.optionVar01_atNm_key)
        # self.autoNumbering_ckBx.setValue(self.options[self.optionVar01_atNm_key])
        self.autoNumbering_ckBx.setValue(atNm_key)

        # add rootOnCurve(roc)
        # roc_key
        roc_key = getOptionVarCmd(self.optionVar01IKSttng_roc_key)
        # self.ikSpHdleSetting_rootOnCurve_ckBx.setValue(self.options[self.optionVar01IKSttng_roc_key])
        self.ikSpHdleSetting_rootOnCurve_ckBx.setValue(roc_key)

        # add parentCurve(pcv)
        # pcv_key
        pcv_key = getOptionVarCmd(self.optionVar01IKSttng_pcv_key)
        # self.ikSpHdleSetting_parentCurve_ckBx.setValue(self.options[self.optionVar01IKSttng_pcv_key])
        self.ikSpHdleSetting_parentCurve_ckBx.setValue(pcv_key)

        # add createCurve(ccv)
        # ccv_key
        ccv_key = getOptionVarCmd(self.optionVar01IKSttng_ccv_key)
        # self.ikSpHdleSetting_createCurve_ckBx.setValue(self.options[self.optionVar01IKSttng_ccv_key])
        self.ikSpHdleSetting_createCurve_ckBx.setValue(ccv_key)

        # add simplifyCurve(scv)
        # scv_key
        scv_key = getOptionVarCmd(self.optionVar01IKSttng_scv_key)
        # self.ikSpHdleSetting_simplifyCurve_ckBx.setValue(self.options[self.optionVar01IKSttng_scv_key])
        self.ikSpHdleSetting_simplifyCurve_ckBx.setValue(scv_key)

        # add simplifyCurve(scv)
        # grp_key
        grp_key = getOptionVarCmd(self.optionVar01IKSttng_grp_key)
        # self.ikSpHdleSetting_grouping_ckBx.setValue(self.options[self.optionVar01IKSttng_grp_key])
        self.ikSpHdleSetting_grouping_ckBx.setValue(grp_key)

        message(args[0])  # message output

        # print(self.options[self.optionVar01Jt_tFld_key], self.options[self.optionVar02Jt_tFld_key]
        #
        #       , self.options[self.optionVar01_mode_key]
        #
        #       , self.options[self.optionVar01_tFld_key]
        #       , self.options[self.optionVar02_tFld_key]
        #       , self.options[self.optionVar03_tFld_key]
        #       , self.options[self.optionVar04_tFld_key]
        #       , self.options[self.optionVar05_tFld_key]
        #
        #       , self.options[self.optionVar01_atNm_key]
        #
        #       , self.options[self.optionVar01IKSttng_roc_key], self.options[self.optionVar01IKSttng_pcv_key]
        #       , self.options[self.optionVar01IKSttng_ccv_key], self.options[self.optionVar01IKSttng_scv_key]
        #
        #       , self.options[self.optionVar01IKSttng_grp_key]
        #       )

        print(tFld_key_stJt, tFld_key_edJt
              , mode_key
              , tFld_key_A1, tFld_key_B1, tFld_key_C1, tFld_key_C2, tFld_key_C3
              , atNm_key
              , roc_key, pcv_key, ccv_key, scv_key
              , grp_key
              )

    # base から継承 override 変更 (独自に定義しなおして上書き)
    # UI-4. optionVar の value を default に戻す操作 関数
    def set_default_value_toOptionVar(self):
        u""" < UI-4. optionVar の value を default に戻す操作 関数 です >

        ::

          base から継承 override 変更 (独自に定義しなおして上書き)
          self.opVar_dictVal_def_list = ['mode0'
            , '', 'clstHndle', '', '', ''
                                       ]  # range is 6
          self.opVar_dictVal_def_list_addCCAndR = [False, False]  # range is 2

        """
        # add start joint
        setOptionVarCmd(self.optionVar01Jt_tFld_key, self.opVar_dictVal_def_list_addCSpIkAndR_0[0])  # ''
        # add end joint
        setOptionVarCmd(self.optionVar02Jt_tFld_key, self.opVar_dictVal_def_list_addCSpIkAndR_0[1])  # ''

        setOptionVarCmd(self.optionVar01_mode_key, self.opVar_dictVal_dflt_list[0])  # 'mode0'
        setOptionVarCmd(self.optionVar01_tFld_key, self.opVar_dictVal_dflt_list[1])  # ''
        setOptionVarCmd(self.optionVar02_tFld_key, self.opVar_dictVal_dflt_list[2])  # 'clstHndle'
        setOptionVarCmd(self.optionVar03_tFld_key, self.opVar_dictVal_dflt_list[3])  # ''
        setOptionVarCmd(self.optionVar04_tFld_key, self.opVar_dictVal_dflt_list[4])  # ''
        setOptionVarCmd(self.optionVar05_tFld_key, self.opVar_dictVal_dflt_list[5])  # ''

        # add autoNumbering
        setOptionVarCmd(self.optionVar01_atNm_key, self.opVar_dictVal_def_list_addCSpIkAndR_1[0])  # bool(0)
        # add rootOnCurve(roc)
        setOptionVarCmd(self.optionVar01IKSttng_roc_key, self.opVar_dictVal_def_list_addCSpIkAndR_2[0])  # bool(0)
        # add parentCurve(pcv)
        setOptionVarCmd(self.optionVar01IKSttng_pcv_key, self.opVar_dictVal_def_list_addCSpIkAndR_2[1])  # bool(0)
        # add createCurve(ccv)
        setOptionVarCmd(self.optionVar01IKSttng_ccv_key, self.opVar_dictVal_def_list_addCSpIkAndR_2[2])  # bool(1)
        # add simplifyCurve(scv)
        setOptionVarCmd(self.optionVar01IKSttng_scv_key, self.opVar_dictVal_def_list_addCSpIkAndR_2[3])  # bool(1)

        # add grouping
        setOptionVarCmd(self.optionVar01IKSttng_grp_key, self.opVar_dictVal_def_list_addCSpIkAndR_3[0])  # bool(1)

        # # add start joint
        # self.options[self.optionVar01Jt_tFld_key] = self.opVar_dictVal_def_list_addCSpIkAndR_0[0]  # ''
        # # add end joint
        # self.options[self.optionVar02Jt_tFld_key] = self.opVar_dictVal_def_list_addCSpIkAndR_0[1]  # ''
        #
        # self.options[self.optionVar01_mode_key] = self.opVar_dictVal_def_list[0]  # 'mode0'
        # self.options[self.optionVar01_tFld_key] = self.opVar_dictVal_def_list[1]  # ''
        # self.options[self.optionVar02_tFld_key] = self.opVar_dictVal_def_list[2]  # 'clstHndle'
        # self.options[self.optionVar03_tFld_key] = self.opVar_dictVal_def_list[3]  # ''
        # self.options[self.optionVar04_tFld_key] = self.opVar_dictVal_def_list[4]  # ''
        # self.options[self.optionVar05_tFld_key] = self.opVar_dictVal_def_list[5]  # ''
        #
        # # add autoNumbering
        # self.options[self.optionVar01_atNm_key] = self.opVar_dictVal_def_list_addCSpIkAndR_1[0]  # bool(0)
        # # add rootOnCurve(roc)
        # self.options[self.optionVar01IKSttng_roc_key] = \
        #     self.opVar_dictVal_def_list_addCSpIkAndR_2[0]  # bool(0)
        # # add parentCurve(pcv)
        # self.options[self.optionVar01IKSttng_pcv_key] = \
        #     self.opVar_dictVal_def_list_addCSpIkAndR_2[1]  # bool(0)
        # # add createCurve(ccv)
        # self.options[self.optionVar01IKSttng_ccv_key] = \
        #     self.opVar_dictVal_def_list_addCSpIkAndR_2[2]  # bool(1)
        # # add simplifyCurve(scv)
        # self.options[self.optionVar01IKSttng_scv_key] = \
        #     self.opVar_dictVal_def_list_addCSpIkAndR_2[3]  # bool(1)
        #
        # # add grouping
        # self.options[self.optionVar01IKSttng_grp_key] = \
        #     self.opVar_dictVal_def_list_addCSpIkAndR_3[0]  # bool(1)
    # 4. UI-4. OptionVar を利用したパラメータ管理 コマンド群 ############################### end

    # 2. UI-2. 追加オプション コマンド群 ###################################################### start
    # base から継承 override 変更 (独自に定義しなおして上書き)
    # pop up menu 用 制限
    # 各 textField 上に出現する pop up menu の 実行コマンド
    def textFieldPupMnuCmd(self, cmnPUpMnu, textStr, *args):
        u""" < pop up menu 用 制限 >

        ::

          各 textField 上に出現する pop up menu の 実行コマンド
          original 継承から変更 override(独自に定義しなおして上書き)

        ##########################

        #.
            :param str cmnPUpMnu:
            :param str textStr:

        ##########################
        """
        print(cmnPUpMnu, textStr)
        if cmnPUpMnu == u'cmnPUpMnu_A1':  # 後ろに追加 or 総入れ替え
            self.currentTxt_A1 = self.get_currentTxt_A1()  # current old
            # print(self.currentTxt_A1)  # current old
            self.cmnTxtFld_A1.setText(u'{}{}'.format(self.currentTxt_A1, textStr))
            self.cmnTxtFld_A1.setInsertionPosition(0)

            if textStr == u'~' or textStr == u'':  # 総入れ替え
                self.cmnTxtFld_A1.setText(textStr)
            elif textStr == u'@':  # 追加
                self.currentTxt_A1 = self.get_currentTxt_A1()  # 一旦現状を get する
                # @ 識別子 の複数入力を検知し、強制的に独自規定で1つに制限するメソッド 実行
                result = self.limitAtSignIdMultipleInputToOneCmd(self.currentTxt_A1, 1)
                self.cmnTxtFld_A1.setText(result)  # 修正
            # 追加2
            # u'SpIk' popUp 入力への制限を追加
            elif textStr == u'SpIk':
                currentTxt_A1_old = self.currentTxt_A1  # 一旦現状を get する
                # print(currentTxt_A1_old)  # current old
                findStr = self.currentTxt_A1.find(u'SpIk')  # 無ければ-1を返します
                # print(findStr)
                if not findStr == -1:  # 有れば-1以外を返します
                    self.cmnTxtFld_A1.setText(currentTxt_A1_old)  # 入れ替え

            self.cmnTxtFld_A1.setFont(self.defaultFont)

        elif cmnPUpMnu == u'cmnPUpMnu_B1':  # 後ろに追加 or 総入れ替え
            self.currentTxt_B1 = self.get_currentTxt_B1()
            self.cmnTxtFld_B1.setText(u'{}{}'.format(self.currentTxt_B1, textStr))
            self.cmnTxtFld_B1.setInsertionPosition(0)

            if textStr == u'~' or textStr == u'':  # 総入れ替え
                self.cmnTxtFld_B1.setText(textStr)
            elif textStr == u'spIKHndle' or textStr == u'splineIKHandle':  # 総入れ替え
                self.cmnTxtFld_B1.setText(textStr)

            self.cmnTxtFld_B1.setFont(self.defaultFont)

        elif cmnPUpMnu == u'cmnPUpMnu_C1':  # 総入れ替え
            self.cmnTxtFld_C1.setText(textStr)
            self.cmnTxtFld_C1.setFont(self.defaultFont)
        elif cmnPUpMnu == u'cmnPUpMnu_C2':  # 総入れ替え
            self.cmnTxtFld_C2.setText(textStr)
            self.cmnTxtFld_C2.setFont(self.defaultFont)
        elif cmnPUpMnu == u'cmnPUpMnu_C3':  # 総入れ替え
            self.cmnTxtFld_C3.setText(textStr)
            self.cmnTxtFld_C3.setFont(self.defaultFont)

            # もしも、self.cmnTxtFld_C3 を blank 実行したときは、
            # 自動で self.cmnTxtFld_C1 も同時に blank 実行する。
            # b/c): 必要でなくなるので
            if textStr == u'':
                self.cmnTxtFld_C1.setText(u'')
                self.cmnTxtFld_C1.setFont(self.defaultFont)

    # 完全に新規
    # ナンバリング識別子の付加の on/off の実行関数
    # self.cmnTxtFld_A1 に付加します
    def doAutoNumbering_ckBx_tgl_command(self, textStr, *args):
        u""" < ナンバリング識別子の付加の on/off の実行関数 です >

        ::

          self.cmnTxtFld_A1 に付加します

        ####################

        #.
            :param str textStr:

        ####################
        """
        # print(textStr)
        if textStr == 'on':
            self.currentTxt_A1 = self.get_currentTxt_A1()
            # print(self.currentTxt_A1)
            is_atMark = self.serchAtMark_fromCurrentTxt(self.currentTxt_A1)
            if is_atMark:  # 追加
                self.cmnTxtFld_A1.setText(self.currentTxt_A1[:-1])  # 一旦除去
                message_warning(u'ナンバリング識別子は既に付加されていました。一旦除去しました')
            else:  # 追加修正
                pass
            self.cmnTxtFld_A1.setInsertionPosition(0)  # ここ大事! 順番も大事！！
            self.cmnTxtFld_A1.insertText('@')  # ここ大事! 順番も大事！！
            message(u'ナンバリング識別子を付加します')
        elif textStr == 'off':
            getTxt = self.cmnTxtFld_A1.getText()
            # print(getTxt)
            # @ (at mark) の有無を調べます。
            is_atMark = self.serchAtMark_fromCurrentTxt(getTxt)
            if is_atMark:
                self.cmnTxtFld_A1.setText(getTxt[:-1])
                message(u'ナンバリング識別子を除去します')

    # base から継承 override 変更 (独自に定義しなおして上書き)
    # textField へのタイピング入力 用 制限
    # 各 textField へのタイピング入力に、一連の制限をかける コマンド
    def limitedTypingInputCmd(self, cmnTxtFld, *args):
        u""" < textField へのタイピング入力 用 制限 >

        ::

          各 textField へのタイピング入力に、一連の制限をかける コマンド
          original 継承から変更 override(独自に定義しなおして上書き)

        ####################

        #.
            :param str cmnTxtFld:

        ####################
        """
        # print(cmnTxtFld)
        if cmnTxtFld == u'cmnTxtFld_A1':
            self.currentTxt_A1 = self.get_currentTxt_A1()
            # print(self.currentTxt_A1)  # current old
            if len(self.currentTxt_A1) > 0:
                if self.currentTxt_A1[0].isupper():  # 先頭が大文字かどうか調べる
                    self.cmnTxtFld_A1.setFont(self.tempFont)
                    self.cmnTxtFld_A1.setInsertionPosition(0)
                    message_text = u'第1単語:アッパーキャメルケース記述で始まっています。' \
                                   u'このままでよろしいですか?' \
                                   u'継続します。'
                    message_warning(message_text)
                else:
                    self.cmnTxtFld_A1.setFont(self.defaultFont)
                    self.cmnTxtFld_A1.setInsertionPosition(0)
                    # print(self.currentTxt_A1.find('SpIk'))  # 'SpIk'文字列を検索し無ければ-1を返します
                    if not self.currentTxt_A1.find('SpIk') == -1:  # 有れば-1以外を返します
                        pass
                    elif self.currentTxt_A1.find('SpIk') == -1:  # 無ければ-1を返します
                        message_text = u'第1単語はユーザー入力後には、必ず "SpIk" 文字列を付加します。' \
                                  u'継続します。'
                        self.cmnTxtFld_A1.setFont(self.defaultFont)
                        self.cmnTxtFld_A1.setInsertionPosition(0)
                        self.cmnTxtFld_A1.setText(self.currentTxt_A1 + 'SpIk')
                        message(message_text)
                # "SpIk" 文字列を付加で更新される可能性があるので、再度 get する
                self.currentTxt_A1 = self.get_currentTxt_A1()
                # print('A')
                # print(self.currentTxt_A1)
                # print('B')
                self.currentTxt_A1 = self.exceptCheck_A1(self.currentTxt_A1)
                # print('D')
                # print(self.currentTxt_A1)
        elif cmnTxtFld == u'cmnTxtFld_B1':
            self.currentTxt_B1 = self.get_currentTxt_B1()
            if len(self.currentTxt_B1) > 0:
                if self.currentTxt_B1[0].isupper():  # 先頭が大文字かどうか調べる
                    self.cmnTxtFld_B1.setFont(self.tempFont)
                    self.cmnTxtFld_B1.setInsertionPosition(0)
                    message_text = u'第2単語:先頭に大文字が見つかりました。' \
                                   u'必ずローワーキャメルケース記述であるよう強制します。'
                    message_warning(message_text)

                    # 先頭を小文字にする
                    self.cmnTxtFld_B1.setText(u'{}{}'
                                   .format(self.currentTxt_B1[0].lower()
                                           , self.currentTxt_B1.split(self.currentTxt_B1[0])[1]
                                           )
                                              )
                    self.cmnTxtFld_B1.setInsertionPosition(0)

                else:
                    self.cmnTxtFld_B1.setFont(self.defaultFont)
                    self.cmnTxtFld_B1.setInsertionPosition(0)
                self.currentTxt_B1 = self.get_currentTxt_B1()
                # print('A')
                # print(self.currentTxt_B1)
                self.currentTxt_B1 = self.exceptCheck_B1(self.currentTxt_B1)
                # print('C')
                # print(self.currentTxt_B1)

    # 完全に新規
    # setJointField start button 其々の押下で実行される関数
    def setJtFld_staJt_btnCmd(self, command = str, *args):
        u"""< setJointField start button 其々の押下で実行される関数 です >

        ::

          完全に新規

        #######################

        #.
            :param str command:
                rename mode: 強制的:0, 構成要素をキープ:1 何れか

        #######################
        """
        selectionLists = commonCheckSelection()
        # print(selectionLists[0])
        if not selectionLists:
            message_warning(u'start joint を選択し、Set ボタンを押下ください')
            pass
        else:
            isJoint = commonCheckJoint(selectionLists[0])
            # print(isJoint)
            if isJoint:
                if command is 'set':
                    self.setJtFld_staJt_txtFld.setText(selectionLists[0])
                    # cmds.textField(self.setJtFld_staJt_txtFld
                    #                , e = True
                    #                , tx = selectionLists[0]
                    #                )
                    self.setJtFld_staJt_setBtn.setEnable(False)
                    # cmds.button(self.setJtFld_staJt_setBtn
                    #             , e = True
                    #             , enable = False
                    #             )
                    self.setJtFld_staJt_selBtn.setEnable(True)
                    # cmds.button(self.setJtFld_staJt_selBtn
                    #             , e = True
                    #             , enable = True
                    #             )
                    self.setJtFld_staJt_clrBtn.setEnable(True)
                    # cmds.button(self.setJtFld_staJt_clrBtn
                    #             , e = True
                    #             , enable = True
                    #             )

                    crv_parent = cmds.pickWalk(selectionLists[0], direction = 'up')
                    self.ikSpHdleSetting_pcv_txtFld.setText(crv_parent[0])
                    # cmds.textField(self.ikSpHdleSetting_pcv_txtFld
                    #                , e = True
                    #                , tx = crv_parent[0]
                    #                )
                    cmds.select(selectionLists[0], r = True)
                    message(u'start joint を登録しました')
            else:
                message_warning(u'joint を選択し、Set ボタンを押下ください')
                pass
        if command is 'sel':
            self.getNode_fromStaJtTxtFld = self.setJtFld_staJt_txtFld.getText()
            # self.getNode_fromStaJtTxtFld = cmds.textField(self.setJtFld_staJt_txtFld
            #                                               , q = True
            #                                               , tx = True
            #                                               )
            cmds.select(self.getNode_fromStaJtTxtFld, r = True)
            message(u'登録 joint を選択します')
        elif command is 'clr':
            self.setJtFld_staJt_txtFld.setText('')
            # cmds.textField(self.setJtFld_staJt_txtFld
            #                , e = True
            #                , tx = ''
            #                )
            self.setJtFld_staJt_setBtn.setEnable(True)
            # cmds.button(self.setJtFld_staJt_setBtn
            #             , e = True
            #             , enable = True
            #             )
            self.setJtFld_staJt_selBtn.setEnable(False)
            # cmds.button(self.setJtFld_staJt_selBtn
            #             , e = True
            #             , enable = False
            #
            self.setJtFld_staJt_clrBtn.setEnable(False)
            # cmds.button(self.setJtFld_staJt_clrBtn
            #             , e = True
            #             , enable = False
            #             )

            self.ikSpHdleSetting_pcv_txtFld.setText('')
            # cmds.textField(self.ikSpHdleSetting_pcv_txtFld
            #                , e = True
            #                , tx = ''
            #                )
            message(u'start joint の登録をクリアーしました')

    # 完全に新規
    # setJointField end button 其々の押下で実行される関数
    def setJtFld_endJt_btnCmd(self, command = str, *args):
        u"""< setJointField end button 其々の押下で実行される関数 です >

        :param command:
        ::

          完全に新規

        #######################

        #.
            :param str command:

        #######################
        """
        selectionLists = commonCheckSelection()
        # print(selectionLists[0])
        if not selectionLists:
            message_warning(u'end joint を選択し、Set ボタンを押下ください')
            pass
        else:
            isJoint = commonCheckJoint(selectionLists[0])
            # print(isJoint)
            if isJoint:
                if command is 'set':
                    self.setJtFld_endJt_txtFld.setText(selectionLists[0])
                    # cmds.textField(self.setJtFld_endJt_txtFld
                    #                , e = True
                    #                , tx = selectionLists[0]
                    #                )
                    self.setJtFld_endJt_setBtn.setEnable(False)
                    # cmds.button(self.setJtFld_endJt_setBtn
                    #             , e = True
                    #             , enable = False
                    #             )
                    self.setJtFld_endJt_selBtn.setEnable(True)
                    # cmds.button(self.setJtFld_endJt_selBtn
                    #             , e = True
                    #             , enable = True
                    #             )
                    self.setJtFld_endJt_clrBtn.setEnable(True)
                    # cmds.button(self.setJtFld_endJt_clrBtn
                    #             , e = True
                    #             , enable = True
                    #             )
                    message(u'end joint を登録しました')
            else:
                message_warning(u'joint を選択し、Set ボタンを押下ください')
                pass
        if command is 'sel':
            self.getNode_fromEndJtTxtFld = self.setJtFld_endJt_txtFld.getText()
            # self.getNode_fromEndJtTxtFld = cmds.textField(self.setJtFld_endJt_txtFld
            #                                               , q = True
            #                                               , tx = True
            #                                               )
            cmds.select(self.getNode_fromEndJtTxtFld, r = True)
            message(u'登録 joint を選択します')
        elif command is 'clr':
            self.setJtFld_endJt_txtFld.setText('')
            # cmds.textField(self.setJtFld_endJt_txtFld
            #                , e = True
            #                , tx = ''
            #                )
            self.setJtFld_endJt_setBtn.setEnable(True)
            # cmds.button(self.setJtFld_endJt_setBtn
            #             , e = True
            #             , enable = True
            #             )
            self.setJtFld_endJt_selBtn.setEnable(False)
            # cmds.button(self.setJtFld_endJt_selBtn
            #             , e = True
            #             , enable = False
            #             )
            self.setJtFld_endJt_clrBtn.setEnable(False)
            # cmds.button(self.setJtFld_endJt_clrBtn
            #             , e = True
            #             , enable = False
            #             )
            message(u'end joint の登録をクリアーしました')

    # 完全に新規
    # UI
    def reset_iKSplineHandleSetting(self, *args):
        u""" < UI >

        ::

          完全に新規
        """
        self.ikSpHdleSetting_rootOnCurve_ckBx.setValue(False)  # mySetting default: False, maya setting default: True
        # cmds.checkBox(self.ikSpHdleSetting_rootOnCurve_ckBx
        #               , e = True
        #               , v = False
        #               )  # mySetting default: False, maya setting default: True

        self.ikSpHdleSetting_parentCurve_ckBx.setValue(False)  # mySetting default: False, maya setting default: True
        # cmds.checkBox(self.ikSpHdleSetting_parentCurve_ckBx
        #               , e = True
        #               , v = False
        #               )  # mySetting default: False, maya setting default: True

        self.ikSpHdleSetting_createCurve_ckBx.setValue(True)  # mySetting default: True, maya setting default: True
        # cmds.checkBox(self.ikSpHdleSetting_createCurve_ckBx
        #               , e = True
        #               , v = True
        #               )  # mySetting default: True, maya setting default: True

        self.ikSpHdleSetting_simplifyCurve_ckBx.setValue(True)  # mySetting default: True, maya setting default: True
        # cmds.checkBox(self.ikSpHdleSetting_simplifyCurve_ckBx
        #               , e = True
        #               , v = True
        #               )  # mySetting default: True, maya setting default: True
        message(u'maya default: IK SplineHandle Settings の必要箇所のみ'
                u'Reset 致しました。'
                )

    # 完全に新規
    # check button 押下で実行される関数
    def check_naming_command(self, *args):
        u""" < check button 押下で実行される関数 です >

        ::

          完全に新規
        """
        get_cmnTxtFld_A1 = self.cmnTxtFld_A1.getText() or ''
        # get_cmnTxtFld_A1 = pm.textField(self.cmnTxtFld_A1, q = True, tx = True) or ''
        print(get_cmnTxtFld_A1)
        if not get_cmnTxtFld_A1:
            YO_logProcess.action('WARNING', u'{}\n\t\t\tLine Number:{}\n'
                                            u'ストップ\n'
                                            u'各 textFiled 内に、ユーザー指定の文字列'
                                            u'が充分に挿入されていません。'
                                            u'少なくとも、'
                                            u'第1単語フィールドへの文字列挿入は必須です。'
                                            u'Spline IK 作成の実行はストップしました。check button push'
                                 .format(self.title, YO_logger2.getLineNo())
                                 )
            # message_warning(u'各 textFiled 内に、ユーザー指定の文字列'
            #                      u'が充分に挿入されていません。'
            #                      u'少なくとも、'
            #                      u'第1単語フィールドへの文字列挿入は必須です。'
            #                      u'Spline IK 作成の実行はストップしました。check button push'
            #                      )
            pass
        else:
            # check用 textField spIKHandle name
            spIKHndle_name_chk = self.checkAndReturn_cTxtFld_spIKHndle_strAll()
            # check用 textField spIKCrv name
            spIKCrv_name_chk = self.checkAndReturn_cTxtFld_spIKCrv_strAll()
            # print(spIKHndle_name_chk, spIKCrv_name_chk)
            if not spIKHndle_name_chk and not spIKCrv_name_chk:
                pass
            else:
                self.cTxt_spIKHndle_ckName.setLabel(spIKHndle_name_chk)
                # cmds.text(self.cTxt_spIKHndle_ckName
                #           , e = True
                #           , label = spIKHndle_name_chk
                #           )
                self.cTxt_spIKCrv_ckName.setLabel(spIKCrv_name_chk)
                # cmds.text(self.cTxt_spIKCrv_ckName
                #           , e = True
                #           , label = spIKCrv_name_chk
                #           )

    # 完全に新規
    # splineIKHandle 名を、コマンド文中の文字列リスト(n)から抽出する関数
    def checkAndReturn_fromCmd_spIKHndle_strAll(self):
        u""" < splineIKHandle 名を、コマンド文中の文字列リスト(n)から抽出する関数 です >

        ::

          完全に新規

        #########################

        #.
            :return: spIKHndle_name
            :rtype: str

        #########################
        """
        str1, str2, str3, str4, str5 = self.wordListsSet_fromCmd
        # str2 = str2 + 'Hndle'
        mainStrList = [i for i in (str1, str2, str3, str4, str5)]
        # print(mainStrList)

        # None を返してくるかもしれない
        spIKHndle_noSideType_name = str1 + '_' + str2
        # None を返してくるかもしれない
        spIKHndle_addSideType_name = str1 + '_' + str2 + str3 + '_' + str4 + str5

        spIKHndle_name = ''

        if '' is str1:
            message_warning(u'ユーザー指定である、<スプラインIKハンドル名> Spline IK Handle の入力フィールド'
                            u'が不完全です。'
                            u'ご確認ください。'
                            )
        else:
            if str5:  # サイド名がある場合
                # None を返してくるかもしれない
                spIKHndle_name = spIKHndle_addSideType_name
            else:  # サイド名が無い場合
                # None を返してくるかもしれない
                spIKHndle_name = spIKHndle_noSideType_name
        return spIKHndle_name

    # 完全に新規
    # cTxtFld_splineIKHandle 名を、全フィールド入力から抽出する関数
    def checkAndReturn_cTxtFld_spIKHndle_strAll(self):
        u""" < cTxtFld_splineIKHandle 名を、全フィールド入力から抽出する関数 です >

        ::

          完全に新規

        #########################

        #.
            :return: spIKHndle_name
            :rtype: str

        #########################
        """
        str1, str2, str3, str4, str5 = self.outPut_cTxtFld()
        # str2 = str2 + 'Hndle'
        mainStrList = [i for i in (str1, str2, str3, str4, str5)]
        # print(mainStrList)

        # None を返してくるかもしれない
        spIKHndle_noSideType_name = str1 + '_' + str2
        # None を返してくるかもしれない
        spIKHndle_addSideType_name = str1 + '_' + str2 + str3 + '_' + str4 + str5

        spIKHndle_name = ''

        if '' is str1:
            message_warning(u'ユーザー指定である、<スプラインIKハンドル名> Spline IK Handle の入力フィールド'
                            u'が不完全です。'
                            u'ご確認ください。'
                            )
        else:
            if str5:  # サイド名がある場合
                # None を返してくるかもしれない
                spIKHndle_name = spIKHndle_addSideType_name
            else:  # サイド名が無い場合
                # None を返してくるかもしれない
                spIKHndle_name = spIKHndle_noSideType_name
        return spIKHndle_name

    # 完全に新規
    # cTxtFld_splineIKCurve 名を、全フィールド入力から抽出する関数
    def checkAndReturn_cTxtFld_spIKCrv_strAll(self):
        u""" < cTxtFld_splineIKCurve 名を、全フィールド入力から抽出する関数 です >

        ::

          完全に新規

        #########################

        #.
            :return: spIKCrv_name
            :rtype: str

        #########################
        """
        str1, str2, str3, str4, str5 = self.outPut_cTxtFld()
        if str2 == 'spIKHndle':
            str2 = 'spIKCrv'
        elif str2 == 'splineIKHandle':
            str2 = 'splineIKCurve'
        mainStrList = [i for i in (str1, str2, str3, str4, str5)]
        # print(mainStrList)

        spIKCrv_noSideType_name = str1 + '_' + str2
        spIKCrv_addSideType_name = str1 + '_' + str2 + str3 + '_' + str4 + str5

        spIKCrv_name = ''

        if '' is str1:
            message_warning(u'ユーザー指定である、<スプラインIKハンドル名> Spline IK Handle の入力フィールド'
                            u'が不完全です。'
                            u'ご確認ください。'
                            )
        else:
            if str5:  # サイド名がある場合
                spIKCrv_name = spIKCrv_addSideType_name
            else:  # サイド名が無い場合
                spIKCrv_name = spIKCrv_noSideType_name
        return spIKCrv_name

    # 完全に新規
    # cTxtFld_splineIKEffector 名を、全フィールド入力から抽出する関数
    def checkAndReturn_cTxtFld_spIKEffector_strAll(self):
        u""" < cTxtFld_splineIKEffector 名を、全フィールド入力から抽出する関数 です >

        ::

          完全に新規

        #########################

        #.
            :return: spIKEfctr_name
            :rtype: str

        #########################
        """
        str1, str2, str3, str4, str5 = self.outPut_cTxtFld()
        if str2 == 'spIKHndle':
            str2 = 'spIKEfctr'
        elif str2 == 'splineIKHandle':
            str2 = 'splineIKEffector'
        mainStrList = [i for i in (str1, str2, str3, str4, str5)]
        # print(mainStrList)

        spIKEfctr_noSideType_name = str1 + '_' + str2
        spIKEfctr_addSideType_name = str1 + '_' + str2 + str3 + '_' + str4 + str5

        spIKEfctr_name = ''

        if '' is str1:
            message_warning(u'ユーザー指定である、<スプラインIKハンドル名> Spline IK Handle の入力フィールド'
                            u'が不完全です。'
                            u'ご確認ください。'
                            )
        else:
            if str5:  # サイド名がある場合
                spIKEfctr_name = spIKEfctr_addSideType_name
            else:  # サイド名が無い場合
                spIKEfctr_name = spIKEfctr_noSideType_name
        return spIKEfctr_name

    # 完全に新規
    # 全フィールド入力から文字列を抽出する関数
    def outPut_cTxtFld(self):
        u""" < 全フィールド入力から文字列を抽出する関数 です >

        ::

          完全に新規

        #########################

        #.
            :return: str1, str2, str3, str4, str5
            :rtype: tuple[str, str, str, str, str]

        #########################
        """
        str1 = self.cmnTxtFld_A1.getText() or ''
        # str1 = cmds.textField(self.cmnTxtFld_A1, q = True, text = True) or ''
        str2 = self.cmnTxtFld_B1.getText() or ''
        # str2 = cmds.textField(self.cmnTxtFld_B1, q = True, text = True) or ''
        str3 = self.cmnTxtFld_C1.getText() or ''
        # str3 = cmds.textField(self.cmnTxtFld_C1, q = True, text = True) or ''
        str4 = self.cmnTxtFld_C2.getText() or ''
        # str4 = cmds.textField(self.cmnTxtFld_C2, q = True, text = True) or ''
        str5 = self.cmnTxtFld_C3.getText() or ''
        # str5 = cmds.textField(self.cmnTxtFld_C3, q = True, text = True) or ''
        # print(str1, str2, str3, str4, str5)
        return str1, str2, str3, str4, str5

    # 完全に新規
    # UIの textFiled start joint 登録入力済フィールドから登録済み文字列を抜き出す関数
    def getNodeName_fromStaTxtFld(self):
        u""" < UIの textFiled start joint 登録入力済フィールドから登録済み文字列を抜き出す関数 です>

        ::

          完全に新規

        #########################

        #.
            :return: getStaNodeName_fromUI
            :rtype: str

        #########################
        """
        getStaNodeName_fromUI = self.setJtFld_staJt_txtFld.getText()  # str
        # getStaNodeName_fromUI = cmds.textField(self.setJtFld_staJt_txtFld, q = True, tx = True)  # str
        if getStaNodeName_fromUI == '...':
            getStaNodeName_fromUI = ''
        return getStaNodeName_fromUI

    # 完全に新規
    # UIの textFiled end joint 登録入力済フィールドから登録済み文字列を抜き出す関数
    def getNodeName_fromEndTxtFld(self):
        u""" < UIの textFiled end joint 登録入力済フィールドから登録済み文字列を抜き出す関数 です>

        ::

          完全に新規

        #########################

        #.
            :return: getEndNodeName_fromUI
            :rtype: str

        #########################
        """
        getEndNodeName_fromUI = self.setJtFld_endJt_txtFld.getText()  # str
        # getEndNodeName_fromUI = cmds.textField(self.setJtFld_endJt_txtFld, q = True, tx = True)  # str
        if getEndNodeName_fromUI == '...':
            getEndNodeName_fromUI = ''
        return getEndNodeName_fromUI

    # 完全に新規
    # UIのチェックボックスのカレントを辞書出力する関数
    def queryEachFlagArg_ikSpHdleSetting(self):
        u"""< UIのチェックボックスのカレントを辞書出力する関数 です >

        ::

          完全に新規

        #########################

        #.
            :return: qEhFlgArgDict_ikSpHdlSttng

            detail):
                OrderedDict([('roc', roc), ('pcv', pcv), ('ccv', ccv), ('scv', scv), ('grp', grp)])

                要素数: 5

            my setting default:
                OrderedDict([('roc', False), ('pcv', False), ('ccv', True), ('scv', True), ('grp', True)])

            :rtype: OrderedDict[str, bool]

        #########################
        """
        qEhFlgArgDict_ikSpHdlSttng = OrderedDict()  # dict(順番保持版)  空からスタート

        # roc ###########
        roc = self.ikSpHdleSetting_rootOnCurve_ckBx.getValue()  # type: bool  # mySetting default: False, maya setting default: True
        # roc = cmds.checkBox(self.ikSpHdleSetting_rootOnCurve_ckBx
        #                     , q = True
        #                     , v = True
        #                     )  # type: bool  # mySetting default: False, maya setting default: True
        # append
        qEhFlgArgDict_ikSpHdlSttng['roc'] = roc

        # pcv ###########
        pcv = self.ikSpHdleSetting_parentCurve_ckBx.getValue()  # type: bool  # mySetting default: False, maya setting default: True
        # pcv = cmds.checkBox(self.ikSpHdleSetting_parentCurve_ckBx
        #                     , q = True
        #                     , v = True
        #                     )  # type: bool  # mySetting default: False, maya setting default: True
        # append
        qEhFlgArgDict_ikSpHdlSttng['pcv'] = pcv

        # ccv ###########
        ccv = self.ikSpHdleSetting_createCurve_ckBx.getValue()  # type: bool  # mySetting default: True, maya setting default: True
        # ccv = cmds.checkBox(self.ikSpHdleSetting_createCurve_ckBx
        #                     , q = True
        #                     , v = True
        #                     )  # type: bool  # mySetting default: True, maya setting default: True
        # append
        qEhFlgArgDict_ikSpHdlSttng['ccv'] = ccv

        # scv ###########
        scv = self.ikSpHdleSetting_simplifyCurve_ckBx.getValue()  # type: bool  # mySetting default: True, maya setting default: True
        # scv = cmds.checkBox(self.ikSpHdleSetting_simplifyCurve_ckBx
        #                     , q = True
        #                     , v = True
        #                     )  # type: bool  # mySetting default: True, maya setting default: True
        # append
        qEhFlgArgDict_ikSpHdlSttng['scv'] = scv

        # grp ###########
        grp = self.ikSpHdleSetting_grouping_ckBx.getValue()  # type: bool  # mySetting default: True
        # grp = cmds.checkBox(self.ikSpHdleSetting_grouping_ckBx
        #                     , q = True
        #                     , v = True
        #                     )  # type: bool  # mySetting default: True
        # append
        qEhFlgArgDict_ikSpHdlSttng['grp'] = grp

        return qEhFlgArgDict_ikSpHdlSttng

    # 完全に新規
    # 第2単語フィールド @ at mark 誤入力判別 関数
    # コマンドベース入力における、特殊制限
    def wrong_input_determining_tFldB1_fromCmd(self, wordLists):
        u""" < 第2単語フィールド @ at mark 誤入力判別 関数 >

        ::

          コマンドベース入力における、特殊制限
          第2単語フィールド @ at mark 誤入力判別 関数

          完全に新規

        #############################

        #.
            :param list of str wordLists:

        #.
            :return: isWrong
                True: 誤入力発見, False: 誤入力なし
            :rtype isWrong: bool

        ############################
        """
        tFldB1 = wordLists[1]
        isWrong = True  # default: True: 誤入力発見
        if '@' in tFldB1:
            isWrong = True  # True: 誤入力発見
            YO_logProcess.action('WARNING', u'{}\n\t\t\tLine Number:{}\n'
                                            u'ストップ\n'
                                            u'第2単語フィールド に、'
                                            u'@ at mark があります。'
                                            u'当ツールでは特殊制限を設け、ここでは許可しません。'
                                            u'Spline IK 作成の実行はストップしました。0-wrong_input_tFldB1'
                                 .format(self.title, YO_logger2.getLineNo())
                                 )
            # message_warning(u'第2単語フィールド に、'
            #                      u'@ at mark があります。'
            #                      u'当ツールでは特殊制限を設け、ここでは許可しません。'
            #                      u'Spline IK 作成の実行はストップしました。0-wrong_input_tFldB1')
            pass
        else:
            isWrong = False  # False: 誤入力なし
        return isWrong
    # 2. UI-2. 追加オプション コマンド群 ###################################################### end

    # その他 アルゴリズムとなる コマンド群 ################################################ start
    # ...
    # その他 アルゴリズムとなる コマンド群 ################################################# end

    # 3. UI-3. common ボタン コマンド群 ################################################# start

    ##########################################
    # <UI用>
    ##########################################
    # プロセスの大枠 #######
    #######################
    # proc1. カレントの、textField 文字列を抜き出します。
    # <共通>
    #   proc1.5
    # <共通>
    #   proc2.1. spline IK 作成
    # <共通>
    #   proc2.2. 最後に、共通な naming 操作 を行っています。
    ###########################################

    # base から継承 override 変更 (独自に定義しなおして上書き)
    # < UI用 >
    # proc1. #
    # Execute 実行 関数
    # @instance.declogger
    def ui_executeBtnCmd(self, *args):
        u""" < UI用 >

        ::

          base から継承 override 変更 (独自に定義しなおして上書き)
              proc1.
                Execute 実行 関数

        """
        self.runInUiOrCommand = 'fromUI'
        # print(self.runInUiOrCommand)

        # UIありきでの実行
        print('\n## ui_executeBtn type ##\n')
        print(u'## 継続中 ########## spIK proc1 (ui_executeBtn type)')

        # ##############################################################
        # proc1. #
        # カレントの、textField 文字列を抜き出します。
        # ###########################################
        self.qEhFlgArgDict_ikSpHdlSttng = self.queryEachFlagArg_ikSpHdleSetting()
        # default: OrderedDict(roc = False, pcv = False, ccv = True, scv = True, grp = True)
        # print(self.qEhFlgArgDict_ikSpHdlSttng)  # dict
        self.mode = self.currentMode()  # int
        self.currentTxt_A1 = self.get_currentTxt_A1()  # str
        self.currentTxt_B1 = self.get_currentTxt_B1()  # str
        self.currentTxt_C1 = self.get_currentTxt_C1()  # str
        self.currentTxt_C2 = self.get_currentTxt_C2()  # str
        self.currentTxt_C3 = self.get_currentTxt_C3()  # str
        self.currentCbx_roc = self.qEhFlgArgDict_ikSpHdlSttng['roc']  # bool rootOnCurve
        self.currentCbx_pcv = self.qEhFlgArgDict_ikSpHdlSttng['pcv']  # bool parentCurve
        self.currentCbx_ccv = self.qEhFlgArgDict_ikSpHdlSttng['ccv']  # bool createCurve
        self.currentCbx_scv = self.qEhFlgArgDict_ikSpHdlSttng['scv']  # bool simplifyCurve
        self.getStaNodeName_fromUI = self.getNodeName_fromStaTxtFld()  # str startJoint
        self.getEndNodeName_fromUI = self.getNodeName_fromEndTxtFld()  # str endEffector
        self.currentCbx_grp = self.qEhFlgArgDict_ikSpHdlSttng['grp']  # bool simplifyCurve

        # ここ大事!!
        if self.currentCbx_roc:
            currentCbx_roc = 1  # int
        else:
            currentCbx_roc = 0  # int
        if self.currentCbx_pcv:
            currentCbx_pcv = 1  # int
        else:
            currentCbx_pcv = 0  # int
        if self.currentCbx_ccv:
            currentCbx_ccv = 1  # int
        else:
            currentCbx_ccv = 0  # int
        if self.currentCbx_scv:
            currentCbx_scv = 1  # int
        else:
            currentCbx_scv = 0  # int
        if self.currentCbx_grp:
            currentCbx_grp = 1  # int
        else:
            currentCbx_grp = 0  # int

        print(u'\n'
              u'// Result: {packageName}.'
              u'{title}.{className}().exe('
              u'mode = {modeInt}'
              u', n = [u\'{a}\', u\'{b}\', u\'{c1}\', u\'{c2}\', u\'{c3}\']'
              u', rootOnCurve = {roc}'
              u', parentCurve = {pcv}'
              u', createCurve = {ccv}'
              u', simplifyCurve = {scv}'
              u', startJoint = u\'{sj}\''
              u', endEffector = u\'{ee}\''
              u', grouping = {grp}'
              u')'
              u'\n'
              .format(packageName = self.pkgName
                      , title = self.title + self.id, className = self.className
                      , modeInt = self.mode
                      , a = self.currentTxt_A1, b = self.currentTxt_B1
                      , c1 = self.currentTxt_C1
                      , c2 = self.currentTxt_C2
                      , c3 = self.currentTxt_C3
                      , roc = currentCbx_roc
                      , pcv = currentCbx_pcv
                      , ccv = currentCbx_ccv
                      , scv = currentCbx_scv
                      , sj = self.getStaNodeName_fromUI
                      , ee = self.getEndNodeName_fromUI
                      , grp = currentCbx_grp
                      )
              )
        # ##############################################################

        # ##############################
        # 一時的、選択リスト(1回目)
        # ##############################
        # 予め出力 コンポーネント選択関連
        # self.selectionLists = commonCheckSelection()  # 自動で空にもなる
        # ##############################
        # print(u'コンポーネント選択関連\n\t'
        #       u'self.selectionLists : \n\t\t'
        #       u'{}'.format(self.selectionLists)
        #       )
        # ##############################

        # 予め出力
        # シーン内 DG name 全リストを出力する メソッド の実行
        self.getObj = self.getDGAll_fromScene()
        # print(self.getObj)

        # 予め出力 TextField関連
        self.wordListsSet_fromUI.__init__()  # 常に初期化で空にする
        self.wordListsSet_fromUI = self.createLists_fromCurrentTxtAll()
        # ##############################
        # print(u'TextField関連\n\t'
        #       u'self.wordListsSet_fromUI : \n\t\t'
        #       u'{}'.format(self.wordListsSet_fromUI)
        #       )
        # ##############################

        if not self.getStaNodeName_fromUI or not self.getEndNodeName_fromUI:  # A
            YO_logProcess.action('WARNING', u'{}\n\t\t\tLine Number:{}\n'
                                            u'ストップ\n'
                                            u'start joint, end joint の何れか、もしくは両方の '
                                            u'UI textFiled への登録が、未だなされていません。'
                                            u'Spline IK 作成はストップしました。00-A'
                                 .format(self.title, YO_logger2.getLineNo())
                                 )
            # message_warning(u'start joint, end joint の何れか、もしくは両方の '
            #                      u'UI textFiled への登録が、未だなされていません。'
            #                      u'Spline IK 作成はストップしました。00-A'
            #                      )
            pass
        elif self.getStaNodeName_fromUI and self.getEndNodeName_fromUI:  # B
            # 共通な一連の関数のまとまり です
            # 場合分けによって、後の方で、proc2.rename 操作 に入っていきます
            self.setOfCommonFunctions(self.wordListsSet_fromUI)
    # 3. UI-3. common ボタン コマンド群 ################################################## end

    # 5. スクリプトベースコマンド入力への対応 ############################################# start

    ##########################################
    # <スクリプトベース用>
    ##########################################
    # プロセスの大枠 #######
    #######################
    # proc1. カレントの、textField 文字列を抜き出します。
    # <共通>
    #   proc1.5
    # <共通>
    #   proc2.1. spline IK 作成
    # <共通>
    #   proc2.2. 最後に、共通な naming 操作 を行っています。
    ###########################################

    # base から継承 override 変更 (独自に定義しなおして上書き)
    # < スクリプトベース用 >
    # proc1. #
    # analysis_strs_fromCmd2 メソッドを利用して、必要な文字列を抜き出します。
    # 引数: relative 追加
    def exe(self, mode = 0, n = None
            , rootOnCurve = 0, parentCurve = 0, createCurve = 1, simplifyCurve = 1
            , startJoint = '', endEffector = ''
            , grouping = 1
            ):
        u""" < スクリプトベースコマンドの YO_createSpIkAndRename 基本出力をインスタンス化する関数 です>

        ::

          proc1. #

          引数: rootOnCurve, parentCurve, createCurve, simplifyCurve, startJoint, endEffector, grouping 追加

          original 継承から変更 override(独自に定義しなおして上書き)

        #######################

        #.
            :param int mode: rename mode: 強制的:0, 構成要素をキープ:1 何れか

            e.g.): mode = 0

        #.
            :param list[str] n: 文字列リスト

            e.g.): n = [u'spineSpIk', u'spIKHndle', u'', u'', u'L']

        #.
            :param int rootOnCurve: bool(0/1)   カーブにロック

            e.g.): rootOnCurve = 0

        #.
            :param int parentCurve: bool(0/1)   ジョイントの親が、自動的にカーブの親

            e.g.): parentCurve = 0

        #.
            :param int createCurve: bool(0/1)   カーブを自動的に作成

            e.g.): createCurve = 1

        #.
            :param int simplifyCurve: bool(0/1)   カーブを単純化

            e.g.): simplifyCurve = 1

        #.
            :param str startJoint: Spline IK のスタートとなるジョイント

            e.g.): startJoint = u'spineA_spIKjt'

        #.
            :param str endEffector: Spline IK の末端となるジョイント

            e.g.): endEffector = u'spineTip_spIKjt'

        #.
            :param int grouping: 適切に Grouping

            e.g.): grouping = 1

        #######################
        """
        if n is None:
            n = []
        # cls = cls()
        # title = cls.title
        # className = cls.className

        self.runInUiOrCommand = 'fromCmd'
        # print(self.runInUiOrCommand)

        # UI不要での実行
        print('\n## command_execute type ##\n')
        print(u'## 継続中 ########## spIK proc1 (command_execute type)')

        # ##############################################################
        # proc1. #
        # カレントの、textField 文字列を抜き出します。
        # ###########################################
        modeInt_fromCmd, wordListsSet_fromCmd\
            , rootOnCurve_int, parentCurve_int\
            , createCurve_int,  simplifyCurve_int\
            , startJoint_str, endEffector_str \
            , grouping_int\
            = self.analysis_strs_fromCmd3(mode, n
                                          , rootOnCurve, parentCurve, createCurve, simplifyCurve
                                          , startJoint, endEffector
                                          , grouping
                                          )
        self.mode = modeInt_fromCmd  # str
        self.roc_fromCmd = strtobool(rootOnCurve_int)  # str -> bool
        self.pcv_fromCmd = strtobool(parentCurve_int)  # str -> bool
        self.ccv_fromCmd = strtobool(createCurve_int)  # str -> bool
        self.scv_fromCmd = strtobool(simplifyCurve_int)  # str -> bool
        self.sj_fromCmd = startJoint_str
        self.ee_fromCmd = endEffector_str
        self.grp_fromCmd = strtobool(grouping_int)  # str -> bool

        print(u'\n'
              u'// Result: {packageName}.'
              u'{title}.{className}().exe('
              u'mode = {modeInt}'
              u', n = {textAll}'
              u', rootOnCurve = {rootOnCurve_int}'
              u', parentCurve = {parentCurve_int}'
              u', createCurve = {createCurve_int}'
              u', simplifyCurve = {simplifyCurve_int}'
              u', startJoint = u\'{startJoint_str}\''
              u', endEffector = u\'{endEffector_str}\''
              u', grouping = {grouping_int}'
              u')'
              u'\n'
              .format(packageName = self.pkgName
                      , title = self.title + self.id, className = self.className
                      , modeInt = mode
                      , textAll = n
                      , rootOnCurve_int = rootOnCurve
                      , parentCurve_int = parentCurve
                      , createCurve_int = createCurve
                      , simplifyCurve_int = simplifyCurve
                      , startJoint_str = startJoint
                      , endEffector_str = endEffector
                      , grouping_int = grouping
                      )
              )
        # ##############################################################

        # 予め出力
        # シーン内 DG name 全リストを出力する メソッド の実行
        self.getObj = self.getDGAll_fromScene()
        # print(self.getObj)

        # 予め出力済 TextField関連をコマンドから抽出
        # print(modeInt_fromCmd, wordListsSet_fromCmd)
        self.wordListsSet_fromCmd.__init__()  # 常に初期化で空にする
        self.wordListsSet_fromCmd = wordListsSet_fromCmd
        ##############################
        print(u'TextField関連\n\t'
              u'self.wordListsSet_fromCmd(wordLists) : \n\t\t'
              u'{}'.format(self.wordListsSet_fromCmd)
              )
        ##############################

        if not startJoint_str or not endEffector_str:  # A
            YO_logProcess.action('WARNING', u'{}\n\t\t\tLine Number:{}\n'
                                            u'ストップ\n'
                                            u'start joint, end joint の何れか、もしくは両方の '
                                            u'UI textFiled への登録が、未だなされていません。'
                                            u'Spline IK 作成はストップしました。spIK proc1-A'
                                 .format(self.title, YO_logger2.getLineNo())
                                 )
            # message_warning(u'start joint, end joint の何れか、もしくは両方の '
            #                     u'UI textFiled への登録が、未だなされていません。'
            #                     u'Spline IK 作成はストップしました。spIK proc1-A'
            #                     )
            pass
        elif startJoint_str and endEffector_str:  # B
            # 共通な一連の関数のまとまり です
            # 場合分けによって、
            #   後の方で、proc2.rename 操作 に入っていきます
            self.setOfCommonFunctions(self.wordListsSet_fromCmd)

    # 完全に新規
    # original( self.analysis_strs_fromCmd() ) からの引数の内容違いによる変更で、新規で定義
    # < スクリプトベース用 >
    # コマンド文字列の parameter mode, parameter relative, parameter n を分析し、
    # modeInt_fromCmd, relativeValue_fromCmd, wordListsSet_fromCmd
    # を出力する メソッド
    def analysis_strs_fromCmd3(self, mode, n, roc, pcv, ccv, scv, sj, ee, grp):
        u""" < コマンド文字列の parameter mode, parameter relative, parameter n を分析 >

        ::

          modeInt_fromCmd, relativeValue_fromCmd, wordListsSet_fromCmd を出力する メソッド

          original( self.analysis_strs_fromCmd() ) からの内容違いによる変更で、
            定義しなおして、
                新規

        #################

        #.
            :param int mode:
            :param list[str] n:
            :param int roc:
            :param int pcv:
            :param int ccv:
            :param int scv:
            :param str sj: start joint
            :param str ee: end joint
            :param int grp:

        #.
            :return:
                modeInt_fromCmd, wordListsSet_fromCmd
                , rocInt_fromCmd, pcvInt_fromCmd, ccvInt_fromCmd, scvInt_fromCmd
                , sjStr_fromCmd, eeStr_fromCmd
                , grpInt_fromCmd
            :rtype: tuple[str, list[str], str, str, str, str, str, str, str]

        #################
        """
        #############################################
        # 分析1 mode ###  intを一旦文字列に変換・分析し、文字列として返す
        modeStrs = 'mode = {}'.format(mode)  # 先ず、文字列にする  # print(typStrs)
        # print(modeStrs)
        patternMode = re.compile(r'(?P<ptnModeInt>[0-1])')  # 0 or 1
        # パターン定義: 'mode = ' と , で囲まれた文字列を最短文字列で見つける
        search = patternMode.finditer(modeStrs)  # 調べる関数
        modeInt_fromCmd = []  # コマンド文字列から抽出の modeInt
        iterator = patternMode.finditer(modeStrs)
        for itr in iterator:
            modeInt_fromCmd.append(itr.group('ptnModeInt'))  # 見つけた順にリストに格納する
        modeInt_fromCmd = modeInt_fromCmd[0]

        #############################################
        # 分析2 n ###  リスト文字列を一旦文字列に変換・分析し、リスト文字列として返す
        # あらかじめ用意されている文字列, 'n = [u'***'...],'から、必要な文字列 *** を抽出する
        nStrs = 'n = {}'.format(n)  # 先ず、文字列にする
        # print(nStrs)
        patternN = re.compile(r'\'(?P<ptnNStr>.*?)\'')  # re.compile(r'u\'(?P<ptnNStr>.*?)\'') からの変更
        # パターン定義: u' と ' で囲まれた文字列を最短文字列で見つける
        wordListsSet_fromCmd = []  # コマンド文字列から抽出の wordListsSet
        search = patternN.finditer(nStrs)  # 調べる関数
        # あるならば
        if search:
            iterator = patternN.finditer(nStrs)
            for itr in iterator:
                # print(itr.group('ptnN'))
                wordListsSet_fromCmd.append(itr.group('ptnNStr'))  # 見つけた順にリストに格納する
        # print(wordListsSet_fromCmd)

        #############################################
        # 分析3 roc ###
        rocStrs = 'rootOnCurve = {}'.format(roc)  # 先ず、文字列にする  # print(typStrs)
        # print(rocStrs)
        patternRoc = re.compile(r'(?P<ptnRocStr>[0-1])')  # 0 or 1
        # パターン定義: 'rootOnCurve = ' と , で囲まれた文字列を最短文字列で見つける
        search = patternRoc.finditer(rocStrs)  # 調べる関数
        rocInt_fromCmd = []  # コマンド文字列から抽出の rootOnCurve_int
        iterator = patternRoc.finditer(rocStrs)
        for itr in iterator:
            rocInt_fromCmd.append(itr.group('ptnRocStr'))  # 見つけた順にリストに格納する
        rocInt_fromCmd = rocInt_fromCmd[0]
        # print(rocInt_fromCmd)

        #############################################
        # 分析4 pcv ###
        pcvStrs = 'parentCurve = {}'.format(pcv)  # 先ず、文字列にする  # print(typStrs)
        # print(pcvStrs)
        patternPcv = re.compile(r'(?P<ptnPcvStr>[0-1])')  # 0 or 1
        # パターン定義: 'parentCurve = ' と , で囲まれた文字列を最短文字列で見つける
        search = patternPcv.finditer(pcvStrs)  # 調べる関数
        pcvInt_fromCmd = []  # コマンド文字列から抽出の parentCurve_int
        iterator = patternPcv.finditer(pcvStrs)
        for itr in iterator:
            pcvInt_fromCmd.append(itr.group('ptnPcvStr'))  # 見つけた順にリストに格納する
        pcvInt_fromCmd = pcvInt_fromCmd[0]
        # print(pcvInt_fromCmd)

        #############################################
        # 分析5 ccv ###
        ccvStrs = 'createCurve = {}'.format(ccv)  # 先ず、文字列にする  # print(typStrs)
        # print(ccvStrs)
        patternCcv = re.compile(r'(?P<ptnCcvStr>[0-1])')  # 0 or 1
        # パターン定義: 'createCurve = ' と , で囲まれた文字列を最短文字列で見つける
        search = patternCcv.finditer(ccvStrs)  # 調べる関数
        ccvInt_fromCmd = []  # コマンド文字列から抽出の createCurve_int
        iterator = patternCcv.finditer(ccvStrs)
        for itr in iterator:
            ccvInt_fromCmd.append(itr.group('ptnCcvStr'))  # 見つけた順にリストに格納する
        ccvInt_fromCmd = ccvInt_fromCmd[0]
        # print(ccvInt_fromCmd)

        #############################################
        # 分析6 scv ###
        scvStrs = 'simplifyCurve = {}'.format(scv)  # 先ず、文字列にする  # print(typStrs)
        # print(scvStrs)
        patternScv = re.compile(r'(?P<ptnScvStr>[0-1])')  # 0 or 1
        # パターン定義: 'createCurve = ' と , で囲まれた文字列を最短文字列で見つける
        search = patternScv.finditer(scvStrs)  # 調べる関数
        scvInt_fromCmd = []  # コマンド文字列から抽出の simplifyCurve_int
        iterator = patternScv.finditer(scvStrs)
        for itr in iterator:
            scvInt_fromCmd.append(itr.group('ptnScvStr'))  # 見つけた順にリストに格納する
        scvInt_fromCmd = scvInt_fromCmd[0]
        # print(scvInt_fromCmd)

        #############################################
        # 分析7 sj ###
        # あらかじめ用意されている文字列, 'startJoint = u'***','から、必要な文字列 *** を抽出する
        sjStrs = 'startJoint = u\'{}\''.format(sj)  # 先ず、文字列にする
        # print(sjStrs)
        patternSj = re.compile(r'\'(?P<ptnSjStr>.*?)\'')  # re.compile(r'u\'(?P<ptnSjStr>.*?)\'') からの変更
        # パターン定義: u' と ' で囲まれた文字列を最短文字列で見つける
        sjStr_fromCmd = []  # コマンド文字列から抽出の startJoint_str
        search = patternSj.finditer(sjStrs)  # 調べる関数
        # あるならば
        if search:
            iterator = patternSj.finditer(sjStrs)
            for itr in iterator:
                # print(itr.group('ptnSjStr'))
                sjStr_fromCmd.append(itr.group('ptnSjStr'))  # 見つけた順にリストに格納する
        sjStr_fromCmd = sjStr_fromCmd[0]
        # print(sjStr_fromCmd)

        #############################################
        # 分析8 ee ###
        # あらかじめ用意されている文字列, 'endEffector = u'***','から、必要な文字列 *** を抽出する
        eeStrs = 'endEffector = u\'{}\''.format(ee)  # 先ず、文字列にする
        # print(eeStrs)
        patternEe = re.compile(r'\'(?P<ptnEeStr>.*?)\'')  # re.compile(r'u\'(?P<ptnEeStr>.*?)\'') からの変更
        # パターン定義: u' と ' で囲まれた文字列を最短文字列で見つける
        eeStr_fromCmd = []  # コマンド文字列から抽出の endEffector_str
        search = patternEe.finditer(eeStrs)  # 調べる関数
        # あるならば
        if search:
            iterator = patternEe.finditer(eeStrs)
            for itr in iterator:
                # print(itr.group('ptnEeStr'))
                eeStr_fromCmd.append(itr.group('ptnEeStr'))  # 見つけた順にリストに格納する
        eeStr_fromCmd = eeStr_fromCmd[0]
        # print(sjStr_fromCmd)

        #############################################
        # 分析9 grp ###
        grpStrs = 'grouping = {}'.format(grp)  # 先ず、文字列にする  # print(typStrs)
        # print(grpStrs)
        patternGrp = re.compile(r'(?P<ptnGrpInt>[0-1])')  # 0 or 1
        # パターン定義: 'grouping = ' と , で囲まれた文字列を最短文字列で見つける
        search = patternGrp.finditer(grpStrs)  # 調べる関数
        grpInt_fromCmd = []  # コマンド文字列から抽出の modeInt
        iterator = patternMode.finditer(grpStrs)
        for itr in iterator:
            grpInt_fromCmd.append(itr.group('ptnModeInt'))  # 見つけた順にリストに格納する
        grpInt_fromCmd = grpInt_fromCmd[0]

        return modeInt_fromCmd, wordListsSet_fromCmd\
            , rocInt_fromCmd, pcvInt_fromCmd, ccvInt_fromCmd, scvInt_fromCmd\
            , sjStr_fromCmd, eeStr_fromCmd\
            , grpInt_fromCmd
    # 5. スクリプトベースコマンド入力への対応 ############################################### end

    # 「splineIK 作成と、naming の核となる コマンド群」 #################################### start
    # 共通な一連の関数のまとまり ########################################### start
    # 共通な一連の関数のまとまり です
    # base から継承 override 変更 (独自に定義しなおして上書き)
    # proc1.5. #
    # 場合分けによって、後の方で、
    #   - proc2. rename 操作 に入る箇所 継続
    #       具体的な箇所: # DBBB
    #   - イレギュラー操作箇所 継続
    #       具体的な箇所: # DAAA
    #   - 他はすべて操作 ストップ
    # させます
    # @instance.declogger
    def setOfCommonFunctions(self, wordLists):
        u""" < 共通な一連の関数のまとまり です >

        ::

          base から継承 override 変更 (独自に定義しなおして上書き)

          proc1.5.
          場合分けによって、後の方で、
              - proc2. rename 操作 に入る箇所 継続
                  具体的な箇所: # DBBB
              - イレギュラー操作箇所 継続
                  具体的な箇所: # DAAA
              - 他はすべて操作 ストップ
          させます

        #######################

        #.
            :param wordLists: list of str

        #######################
        """
        print(u'## 継続中 ########## spIK proc1.5')
        # 予め出力 TextField関連
        # textField の待機文字列が、十分にセットされているかどうかの真偽を出力する メソッド
        self.isSet_reqTxtFld = self.isSet_requiredTextField(wordLists)
        # ##############################
        # print(u'TextField関連\n\t'
        #       u'self.isSet_reqTxtFld : \n\t\t'
        #       u'{}'.format(self.isSet_reqTxtFld)
        #       )
        # ##############################

        # 予め出力
        self.newLists.__init__()  # self.newLists のみ、念のため空にして初期化
        # print(self.newLists)

        # 予め出力 TextField関連
        # @ (at mark) の数を調べる関数 実行
        self.atMark_count = self.atMark_count_fromCurrentTxt(wordLists)  # int
        # ##############################
        # print(u'TextField関連\n\t'
        #       u'self.atMark_count : \n\t\t'
        #       u'{}'.format(self.atMark_count)
        #       )
        # ##############################

        # 予め出力 TextField関連
        self.strsDecompListsAll = self.waitingWordStrs_patternCheck_exe(wordLists)  # 多重リスト
        # ##############################
        # print(u'TextField関連\n\t'
        #       u'self.strsDecompListsAll : \n\t\t'
        #       u'{}'.format(self.strsDecompListsAll)
        #       )
        # ##############################

        # ##############################
        # print(u'TextField関連\n\t'
        #       u'self.isRelative : \n\t\t'
        #       u'{}'.format(self.isRelative)
        #       )
        # ##############################

        # print(self.selectionLists)  # コンポーネント選択中

        # 予め出力
        # イレギュラー対応用変数を出力するための関数 実行
        # ここでいうイレギュラーとは、「選択1っ、atMark 0、TextField関連が完全 の時」 を言います
        # イレギュラー対応用変数 self.waiting_last_string (default: '') を予め出力
        # イレギュラー対応用変数 self.is_exists_forNCName (default: False) を予め出力
        # 選択1っ、atMark 0、TextField関連が完全 の時だけに対応
        self.renameFunction_inIrregularCases()

        # 修正3
        # コマンド実行時、UI実行時 どちらでも splineIk 作成前に、シーン内の重複ノード名を検索判断する仕組みを修正
        # print(self.runInUiOrCommand)
        if self.runInUiOrCommand == 'fromCmd':
            # print('self.wordListsSet_fromCmd: {}'.format(self.wordListsSet_fromCmd))
            # 追加2
            spIKHndle_name_chk = self.checkAndReturn_fromCmd_spIKHndle_strAll()
            # print(spIKHndle_name_chk)
        else:  # fromUI
            # print('self.outPut_cTxtFld(): {}'.format(self.outPut_cTxtFld()))
            # 追加2
            spIKHndle_name_chk = self.checkAndReturn_cTxtFld_spIKHndle_strAll()
            # print(spIKHndle_name_chk)
        # 追加2
        self.waiting_last_string = spIKHndle_name_chk

        # TextField名の構成から判断された、待機している最終文字
        # ##############################
        print(u'TextField名の構成から判断された、待機している最終文字\n\t'
              u'self.waiting_last_string : \n\t\t'
              u'{}'.format(self.waiting_last_string))
        ##############################

        # 追加2
        self.is_exists_forNCName \
            = self.searchForDuplicateName(self.getObj, self.waiting_last_string)

        # self.waiting_last_string が、
        # self.getObj リスト内に、
        # 重複した名前として既にあるかどうかを探しあて、存在の真偽を出力する メソッドの実行
        # False: 重複していない
        # True: 重複している 注意!
        ##############################
        print(u'<イレギュラー対応用>重複した名前として、'
              u'待機している最終文字が既にあるかどうかを探しあて、存在の真偽\n\t'
              u'self.is_exists_forNCName : \n\t\t'
              u'{}'
              .format(self.is_exists_forNCName)
              )
        ##############################

        ##############################
        # print(self.mode, type(self.mode))
        # print(self.isRelative, type(self.isRelative))
        ##############################

        ##############################
        # 場合分けによって、後の方で、
        #   - proc2. rename 操作 に入る箇所 継続
        #       具体的な箇所: # DBBB
        #   - イレギュラー操作箇所 継続
        #       具体的な箇所: # DAAA
        #   - 他はすべて操作 ストップ
        # させます
        #############
        # atMark 0
        if self.atMark_count == 0:  # DA
            print(u'継続 DA')
            # TextField関連が完全
            if self.isSet_reqTxtFld:  # DAA
                print(u'継続 DAA')
                # False: 重複していない
                # 選択1っ、atMark 0、TextField関連が完全、重複していない
                if self.is_exists_forNCName is False:  # DAAA
                    # コマンドベース入力
                    # 第3単語-要素1フィールド、要素2フィールド、要素3フィールド誤入力判別 実行 追加
                    isWrong = self.wrong_input_determining_fromCmd(wordLists)
                    if not isWrong:  # DAAA  # False: 誤入力なし で継続
                        print(u'継続 DAAA')
                        # ###########################################
                        # proc2.1. spline IK 作成
                        # proc2.2. 最後に、共通な naming 操作
                        #   を順番に一遍に行っています。
                        # ###########################################
                        print('******** splineIK create and naming, proc start.. '
                              '************************************************'
                              'inIrregularCases spIK proc1.5-DAAA'
                              )
                        self.spIK_create_and_rename_exe(wordLists)
                        ##############################
                        print('******** splineIK create and naming, proc done '
                              '************************************************'
                              'inIrregularCases spIK proc1.5-DAAA'
                              )
                        ##############################
                # True: 重複している 注意!
                else:  # DAAB
                    # print(u'ストップ DAAB')
                    YO_logProcess.action('ERROR', u'{}\n\t\t\tLine Number:{}\n'
                                                  u'ストップ DAAB\n'
                                                  u'各 textFiled 内へのユーザー指定の文字列'
                                                  u'は充分に挿入されていますが、'
                                                  u'待機している最終文字列 \'{}\' '
                                                  u'は、'
                                                  u'予めシーン内の文字列リスト内に、'
                                                  u'重複して存在している可能性があるため'
                                                  u'Spline IK 作成はストップしました。spIK proc1.5-DAAB'
                                         .format(self.title
                                                 , YO_logger2.getLineNo()
                                                 , self.waiting_last_string)
                                         )
                    # message_warning(u'各 textFiled 内へのユーザー指定の文字列'
                    #                      u'は充分に挿入されていますが、'
                    #                      u'待機している最終文字列 \'{}\' '
                    #                      u'は、'
                    #                      u'予めシーン内の文字列リスト内に、'
                    #                      u'重複して存在している可能性があるため'
                    #                      u'Spline IK 作成はストップしました。spIK proc1.5-DAAB'
                    #                      .format(self.waiting_last_string)
                    #                      )
                    pass
            # TextField関連が完全でない
            else:  # DAB
                # print(u'ストップ DAB')
                YO_logProcess.action('WARNING', u'{}\n\t\t\tLine Number:{}\n'
                                                u'ストップ DAB\n'
                                                u'各 textFiled 内に、ユーザー指定の文字列'
                                                u'が充分に挿入されていません。'
                                                u'少なくとも、'
                                                u'第1単語フィールドへの文字列挿入は必須です。'
                                                u'Spline IK 作成はストップしました。spIK proc1.5-DAB'
                                     .format(self.title, YO_logger2.getLineNo())
                                     )
                # message_warning(u'各 textFiled 内に、ユーザー指定の文字列'
                #                      u'が充分に挿入されていません。'
                #                      u'少なくとも、'
                #                      u'第1単語フィールドへの文字列挿入は必須です。'
                #                      u'Spline IK 作成はストップしました。spIK proc1.5-DAB'
                #                      )
                pass
        # atMark 0でない
        else:  # DB
            # TextField関連が完全でない
            if not self.isSet_reqTxtFld:  # DBA
                # print(u'ストップ DBA')
                YO_logProcess.action('WARNING', u'{}\n\t\t\tLine Number:{}\n'
                                                u'ストップ DBA\n'
                                                u'単独選択で実行中です。'
                                                u'各 textFiled 内に、ユーザー指定の文字列'
                                                u'が充分に挿入されていません。'
                                                u'少なくとも、'
                                                u'第1単語フィールドへの文字列挿入は必須です。'
                                                u'Spline IK 作成の実行はストップしました。spIK proc1.5-DBA'
                                     .format(self.title, YO_logger2.getLineNo())
                                     )
                # message_warning(u'単独選択で実行中です。'
                #                      u'各 textFiled 内に、ユーザー指定の文字列'
                #                      u'が充分に挿入されていません。'
                #                      u'少なくとも、'
                #                      u'第1単語フィールドへの文字列挿入は必須です。'
                #                      u'Spline IK 作成の実行はストップしました。spIK proc1.5-DBA'
                #                      )
                pass
            # TextField関連が完全
            else:  # DBB
                print(u'継続 DBB')
                # atMark 多い
                if self.atMark_count >= 2:  # DBBA
                    # print(u'ストップ DBBA')
                    YO_logProcess.action('ERROR', u'{}\n\t\t\tLine Number:{}\n'
                                                  u'ストップ DBBA\n'
                                                  u'各 textFiled 内に、@ (at mark) '
                                                  u'が複数挿入されています。'
                                                  u'可能な限り、一つの入力で留めてください。'
                                                  u'Spline IK 作成の実行はストップしました。spIK proc1.5-DBBA'
                                         .format(self.title, YO_logger2.getLineNo())
                                         )
                    # message_warning(u'各 textFiled 内に、@ (at mark) '
                    #                      u'が複数挿入されています。'
                    #                      u'可能な限り、一つの入力で留めてください。'
                    #                      u'Spline IK 作成の実行はストップしました。spIK proc1.5-DBBA'
                    #                      )

                    pass
                # 選択1っ、atMark 1、TextField関連が完全
                elif self.atMark_count == 1:  # DBBB
                    # コマンドベース入力

                    # ############################# start
                    # 当ツールのみの特殊制限
                    # 第2単語フィールド @ at mark 誤入力判別 実行 追加
                    isWrong_special = self.wrong_input_determining_tFldB1_fromCmd(wordLists)
                    if not isWrong_special:  # False: 誤入力なし で継続
                        # ############################# end

                        # 第3単語-要素1フィールド、要素2フィールド、要素3フィールド誤入力判別 実行 追加
                        isWrong = self.wrong_input_determining_fromCmd(wordLists)
                        if not isWrong:  # DBBB  # False: 誤入力なし で継続
                            print(u'継続 DBBB')
                            # ###########################################
                            # proc2.1. spline IK 作成
                            # proc2.2. 最後に、共通な naming 操作
                            #   を順番に一遍に行っています。
                            # ###########################################
                            print('******** splineIK create and naming, proc start.. '
                                  '************************************************'
                                  'spIK proc1.5-DBBB'
                                  )
                            self.spIK_create_and_rename_exe(wordLists)
                            ##############################
                            print('******** splineIK create and naming, proc done '
                                  '************************************************'
                                  'spIK proc1.5-DBBB'
                                  )
                            ##############################
    # 共通な一連の関数のまとまり ############################################# end

    # spline IK作成と naming を一遍に操作 ################################# start
    # 完全に新規
    # 一遍に操作
    # ###########################################
    # proc2.1. spline IK 作成
    # proc2.2. 最後に、共通な naming 操作
    #   を順番に一遍に行っています。
    # ###########################################
    # @instance.declogger
    def spIK_create_and_rename_exe(self, wordLists):
        u""" < 一遍に操作 >

        ::

          完全に新規

          一遍に操作
          proc2.1. spline IK 作成
          proc2.2. 最後に、共通な naming 操作
            を順番に一遍に行っています

        ####################

        #.
            :param wordLists: list of str

        ####################
        """
        print(self.runInUiOrCommand)
        spIKCrv_name = ''
        spIKEfctr_name = ''
        spIKHndle_gp = ''
        spIKCtrl_gp = ''
        newNodes = []
        if self.runInUiOrCommand == 'fromCmd':  #
            print(u'## 継続中 ########## spIK proc2.1 fromCmd')
            # print(wordLists)
            # print(self.roc_fromCmd, self.pcv_fromCmd, self.ccv_fromCmd, self.scv_fromCmd
            #       , self.sj_fromCmd, self.ee_fromCmd
            #       , self.grp_fromCmd
            #       )
            spIk_list = cmds.ikHandle(
                solver = 'ikSplineSolver'
                , rootOnCurve = self.roc_fromCmd
                , parentCurve = self.pcv_fromCmd
                , createCurve = self.ccv_fromCmd
                , simplifyCurve = self.scv_fromCmd
                , startJoint = self.sj_fromCmd  # sj
                , endEffector = self.ee_fromCmd  # ee
            )
            cmds.select(spIk_list, r = True)
            selectionLists_orijinal = commonCheckSelection()  # 自動で空にもなる
            self.selectionLists = selectionLists_orijinal
            self.selectionLists = self.selectionLists[:1]  # 敢えて[1][2] をリストから除外

            print(u'## 継続中 ########## spIK proc2.2 fromCmd')
            self.selectionLists = self.checkAndDoUniqueName_forSlNode(self.selectionLists)
            self.start_executeCmd(self.selectionLists, self.mode, wordLists)
            self.spIKHndle_name = commonCheckSelection()[0]

            newNodes.append(self.spIKHndle_name)

            spIKHndle_str2List = self.spIKHndle_name.split('_')
            replace_str = ''
            spIKEfctr_name = ''
            if '_' in self.spIKHndle_name:
                if len(spIKHndle_str2List) == 2:
                    if spIKHndle_str2List[1] == 'spIKHndle':
                        replace_str = spIKHndle_str2List[1].replace('Hndle', 'Efctr')
                    elif spIKHndle_str2List[1] == 'splineIKHandle':
                        replace_str = spIKHndle_str2List[1].replace('Handle', 'Effector')
                    spIKEfctr_name = spIKHndle_str2List[0] + '_' + replace_str
                elif len(spIKHndle_str2List) == 3:
                    if spIKHndle_str2List[1] == 'spIKHndle':
                        replace_str = spIKHndle_str2List[1].replace('Hndle', 'Efctr')
                    elif spIKHndle_str2List[1] == 'splineIKHandle':
                        replace_str = spIKHndle_str2List[1].replace('Handle', 'Effector')
                    spIKEfctr_name = spIKHndle_str2List[0] + '_' + replace_str + '_' + spIKHndle_str2List[2]
                cmds.rename(selectionLists_orijinal[1], spIKEfctr_name)

                newNodes.append(spIKEfctr_name)

            replace_str = ''
            spIKCrv_name = ''
            if '_' in self.spIKHndle_name:
                if len(spIKHndle_str2List) == 2:
                    if spIKHndle_str2List[1] == 'spIKHndle':
                        replace_str = spIKHndle_str2List[1].replace('Hndle', 'Crv')
                    elif spIKHndle_str2List[1] == 'splineIKHandle':
                        replace_str = spIKHndle_str2List[1].replace('Handle', 'Curve')
                    spIKCrv_name = spIKHndle_str2List[0] + '_' + replace_str
                elif len(spIKHndle_str2List) == 3:
                    if spIKHndle_str2List[1] == 'spIKHndle':
                        replace_str = spIKHndle_str2List[1].replace('Hndle', 'Crv')
                    elif spIKHndle_str2List[1] == 'splineIKHandle':
                        replace_str = spIKHndle_str2List[1].replace('Handle', 'Curve')
                    spIKCrv_name = spIKHndle_str2List[0] + '_' + replace_str + '_' + spIKHndle_str2List[2]
                cmds.rename(selectionLists_orijinal[2], spIKCrv_name)

                newNodes.append(spIKCrv_name)

            # grouping ############################################################### start
            spIKHndle_gp = ''
            spIKCtrl_gp = ''
            # print(self.currentTxt_A1, self.currentTxt_B1
            #       , self.currentTxt_C1, u'Gp', self.currentTxt_C3
            #       )
            # print(u'{}'.format(wordLists[0]), u'{}'.format(wordLists[1])
            #       , u'{}'.format(wordLists[2]), u'{}'.format(wordLists[3]), u'{}'.format(wordLists[4])
            #       )
            # grouping 無し
            if not self.grp_fromCmd:  # False
                message_warning(u'grouping を行わずに実行いたしました。spIK proc2.2 fromCmd')
                cmds.select(self.spIKHndle_name, spIKCrv_name, r = True)  # 選択して終わり
            # grouping 有り
            else:  # True
                # grouping and group naming

                # spIKHndle grouping
                tempGroupA = cmds.group(self.spIKHndle_name)
                # rename tool 発動
                RT_Modl().exe(mode = self.mode, n = [
                    u'{}'.format(wordLists[0])
                    , u'{}'.format(wordLists[1])
                    , u'{}'.format(wordLists[2])
                    , u'Gp'
                    , u'{}'.format(wordLists[4])
                    ]
                              )
                spIKHndle_gp = commonCheckSelection()[0]

                # # spIKCrv grouping
                replace_str = ''
                if spIKHndle_str2List[1] == 'spIKHndle':
                    replace_str = spIKHndle_str2List[1].replace('Hndle', 'Ctrl')
                elif spIKHndle_str2List[1] == 'splineIKHandle':
                    replace_str = spIKHndle_str2List[1].replace('Handle', 'Ctrl')
                tempGroupB = cmds.group(spIKCrv_name)
                # rename tool 発動
                RT_Modl().exe(mode = self.mode, n = [
                    u'{}'.format(wordLists[0])
                    , replace_str
                    , u'{}'.format(wordLists[2])
                    , u'Gp'
                    , u'{}'.format(wordLists[4])
                    ]
                              )
                spIKCtrl_gp = commonCheckSelection()[0]
                message(u'grouping で実行いたしました。spIK proc2.2 fromCmd')
                cmds.select(spIKHndle_gp, spIKCtrl_gp, r = True)  # 選択して終わり

                newNodes.append(spIKHndle_gp)
                newNodes.append(spIKCtrl_gp)

            # grouping ############################################################### end
        elif self.runInUiOrCommand == 'fromUI':
            print(u'## 継続中 ########## spIK proc2.1 fromUI')
            # print(wordLists)
            # print(self.qEhFlgArgDict_ikSpHdlSttng['roc']
            #       , self.qEhFlgArgDict_ikSpHdlSttng['pcv']
            #       , self.qEhFlgArgDict_ikSpHdlSttng['ccv']
            #       , self.qEhFlgArgDict_ikSpHdlSttng['scv']
            #       , self.getStaNodeName_fromUI
            #       , self.getEndNodeName_fromUI
            #       , self.qEhFlgArgDict_ikSpHdlSttng['grp']
            #       )
            # ##################################################################################
            # proc2.1. #
            # spline IK 関連 作成
            # ###########################################
            # print(self.isRelative)
            # spline IK 関連作成 ################################## start
            # print(self.getNode_fromStaJtTxtFld, self.getNode_fromEndJtTxtFld)
            spIk_list = cmds.ikHandle(
                solver = 'ikSplineSolver'
                , rootOnCurve = self.qEhFlgArgDict_ikSpHdlSttng['roc']
                # maya default: True, my setting: False

                , parentCurve = self.qEhFlgArgDict_ikSpHdlSttng['pcv']
                # maya default: True, my setting: False

                , createCurve = self.qEhFlgArgDict_ikSpHdlSttng['ccv']
                # maya default: True, my setting: True

                , simplifyCurve = self.qEhFlgArgDict_ikSpHdlSttng['scv']
                # maya default: True, my setting: True

                , startJoint = self.getStaNodeName_fromUI  # sj
                , endEffector = self.getEndNodeName_fromUI  # ee
                                      )
            # print(spIk_list)  # ikHandle1 effector1 curve1 の順
            cmds.select(spIk_list, r = True)
            # spline IK 関連作成 ################################## end

            # keep
            selectionLists_orijinal = commonCheckSelection()  # 自動で空にもなる

            self.selectionLists = selectionLists_orijinal
            # print(self.selectionLists)
            self.selectionLists = self.selectionLists[:1]  # 敢えて[1][2] をリストから除外
            # print(self.selectionLists)

            print(u'## 継続中 ########## spIK proc2.2 fromUI')
            # ##################################################################################
            # proc2.2. #
            # naming 操作
            # ###########################################
            ###########################
            # spline IK Handle のリネーム ############################################# start
            # original ネーミングエンジンを利用
            # 選択した全ノード名に対して、unique name にして更新する メソッド の実行
            self.selectionLists = self.checkAndDoUniqueName_forSlNode(self.selectionLists)
            # print(self.selectionLists)
            # original ネーミングエンジンを利用
            # rename の開始
            self.start_executeCmd(self.selectionLists, self.mode, wordLists)
            # spline IK Handle のリネーム ############################################### end
            ###########################
            self.spIKHndle_name = commonCheckSelection()[0]
            # print(self.spIKHndle_name)

            newNodes.append(self.spIKHndle_name)

            spIKHndle_str2List = self.spIKHndle_name.split('_')

            ###########################
            # spline IK Curve のリネーム ############################################## start
            replace_str = ''
            spIKCrv_name = ''
            if '_' in self.spIKHndle_name:
                if len(spIKHndle_str2List) == 2:
                    if spIKHndle_str2List[1] == 'spIKHndle':
                        replace_str = spIKHndle_str2List[1].replace('Hndle', 'Crv')
                    elif spIKHndle_str2List[1] == 'splineIKHandle':
                        replace_str = spIKHndle_str2List[1].replace('Handle', 'Curve')
                    spIKCrv_name = spIKHndle_str2List[0] + '_' + replace_str
                elif len(spIKHndle_str2List) == 3:
                    if spIKHndle_str2List[1] == 'spIKHndle':
                        replace_str = spIKHndle_str2List[1].replace('Hndle', 'Crv')
                    elif spIKHndle_str2List[1] == 'splineIKHandle':
                        replace_str = spIKHndle_str2List[1].replace('Handle', 'Curve')
                    spIKCrv_name = spIKHndle_str2List[0] + '_' + replace_str + '_' + spIKHndle_str2List[2]
                cmds.rename(selectionLists_orijinal[2], spIKCrv_name)

                newNodes.append(spIKCrv_name)

            # spline IK Curve のリネーム ################################################ end
            ###########################
            # print(spIKCrv_name)

            ###########################
            # spline IK Effector のリネーム ########################################### start
            replace_str = ''
            spIKEfctr_name = ''
            if '_' in self.spIKHndle_name:
                if len(spIKHndle_str2List) == 2:
                    if spIKHndle_str2List[1] == 'spIKHndle':
                        replace_str = spIKHndle_str2List[1].replace('Hndle', 'Efctr')
                    elif spIKHndle_str2List[1] == 'splineIKHandle':
                        replace_str = spIKHndle_str2List[1].replace('Handle', 'Effector')
                    spIKEfctr_name = spIKHndle_str2List[0] + '_' + replace_str
                elif len(spIKHndle_str2List) == 3:
                    if spIKHndle_str2List[1] == 'spIKHndle':
                        replace_str = spIKHndle_str2List[1].replace('Hndle', 'Efctr')
                    elif spIKHndle_str2List[1] == 'splineIKHandle':
                        replace_str = spIKHndle_str2List[1].replace('Handle', 'Effector')
                    spIKEfctr_name = spIKHndle_str2List[0] + '_' + replace_str + '_' + spIKHndle_str2List[2]
                cmds.rename(selectionLists_orijinal[1], spIKEfctr_name)

                newNodes.append(spIKEfctr_name)

            # spline IK Effector のリネーム ############################################# end
            ###########################
            # print(spIKEfctr_name)

            # grouping ############################################################### start
            spIKHndle_gp = ''
            spIKCtrl_gp = ''
            # grouping 無し
            if not self.qEhFlgArgDict_ikSpHdlSttng['grp']:  # False
                message_warning(u'grouping を行わずに実行いたしました。spIK proc2.2 fromUI')
                cmds.select(self.spIKHndle_name, spIKCrv_name, r = True)  # 選択して終わり
            # grouping 有り
            else:  # True
                # grouping and group naming

                # spIKHndle grouping
                tempGroupA = cmds.group(self.spIKHndle_name)
                # rename tool 発動
                RT_Modl().exe(mode = self.mode, n = [
                    self.currentTxt_A1
                    , self.currentTxt_B1
                    , self.currentTxt_C1
                    , u'Gp'
                    , self.currentTxt_C3
                    ]
                              )
                spIKHndle_gp = commonCheckSelection()[0]

                # # spIKCrv grouping
                replace_str = ''
                if spIKHndle_str2List[1] == 'spIKHndle':
                    replace_str = spIKHndle_str2List[1].replace('Hndle', 'Ctrl')
                elif spIKHndle_str2List[1] == 'splineIKHandle':
                    replace_str = spIKHndle_str2List[1].replace('Handle', 'Ctrl')
                tempGroupB = cmds.group(spIKCrv_name)
                # rename tool 発動
                RT_Modl().exe(mode = self.mode, n = [
                    self.currentTxt_A1
                    , replace_str
                    , self.currentTxt_C1
                    , u'Gp'
                    , self.currentTxt_C3
                    ]
                              )
                spIKCtrl_gp = commonCheckSelection()[0]
                message(u'grouping で実行いたしました。spIK proc2.2 fromUI')
                cmds.select(spIKHndle_gp, spIKCtrl_gp, r = True)  # 選択して終わり

                newNodes.append(spIKHndle_gp)
                newNodes.append(spIKCtrl_gp)

            # grouping ############################################################### end
        for newNodeIndex in newNodes:
            YO_logProcess.action('INFO'
                                 , u'{}\n\t\t\tLine Number:{}\n'.format(self.title
                                                                        , YO_logger2.getLineNo()
                                                                        )
                                 + newNodeIndex
                                 )
        # print(self.spIKHndle_name)
        # print(spIKCrv_name)
        # print(spIKEfctr_name)
        # print(spIKHndle_gp)
        # print(spIKCtrl_gp)
    # spline IK作成と naming を一遍に操作 ################################### end
    # 「splineIK 作成と、naming の核となる コマンド群」 ###################################### end


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
