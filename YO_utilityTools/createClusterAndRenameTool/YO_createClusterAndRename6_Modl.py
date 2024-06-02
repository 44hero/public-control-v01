# -*- coding: utf-8 -*-

u"""
YO_createClusterAndRename6_Modl.py

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
        - 変換箇所4
            - 概要: 絶対パス から 相対パス へ記述変更
            - 詳細:
                ::

                  -     from YO_utilityTools.createClusterAndRename.[...] import ...
                  +     from .[...] import ...

                  -     from YO_utilityTools.lib.[...] import ...
                  +     from ..lib.[...] import ...

                  -     from YO_utilityTools.lib import ...
                  +     from ..lib import ...

                  -     from YO_utilityTools.renameTool.YO_renameTool5_Modl import RT_Modl
                  +     from ..renameTool.YO_renameTool5_Modl import RT_Modl

        version = '-3.1-'

    done: 2023//10/26
        汎用箇所を、モジュールとして読み込みに変更

        version = '-3.0-'

    done: 2023/09/21
        - python2系 -> python3系 変換
            - 変換箇所
                - 概要: unicode関連
                    - 対象箇所
                        - # 分析3 n ###
                - 詳細: 以下参照
                ::

                  -
                            def analysis_strs_fromCmd2(self, mode, relative, n):
                                ...
                                #############################################
                                # 分析3 n ###  リスト文字列を一旦文字列に変換・分析し、リスト文字列として返す
                                ...
                                patternC = re.compile(r'u\'(?P<ptnC>.*?)\'')  # 変更対象箇所
                                ...
                  +
                            def analysis_strs_fromCmd(self, mode, n):
                                ...
                                #############################################
                                # 分析3 n ###  リスト文字列を一旦文字列に変換・分析し、リスト文字列として返す
                                ...
                                patternC = re.compile(r'\'(?P<ptnC>.*?)\'')  # 変更
                                ...

      version = '-2.0-'

    done: 2023/05/23~2023/05/24
        - 変更2
            - CLST命名をclst命名に変更
            - 'underScoresCount2' の時、
                e.g.): spine@_clstHndle_L -> spine@_clst_L
                    となるように変更

        version = '-1.5-'

    done: 2023/03/28~2022/04/10
        新規

        version = '-1.0-'
"""

# 標準ライブラリ
import re
# from functools import partial  # partial 利用時は、最後の引数に、*args 要時あり
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
# from ..lib.commonCheckJoint import commonCheckJoint  # :return: bool
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


class CCAndRT_Modl(RT_Modl):
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

            - 「cluster 作成と、naming の核となる コマンド群」

                - 共通な一連の関数のまとまり

                    - イレギュラー対応用

                - クラスター作成と naming を一遍に操作

    ######
    """
    def __init__(self):
        super(CCAndRT_Modl, self).__init__()  # RT_Modl からの派生宣言

        # base から継承で、同じ内容だが新規扱い(override)
        self.constructor_chunk1()  # コンストラクタのまとまり1 # パッケージ名等の定義
        # base から継承で、同じ内容だが新規扱い(override)
        self.constructor_chunk2()  # コンストラクタのまとまり2 # タイトル等の定義

        # base から継承で再利用しているので不要
        # self.constructor_chunk3()  # コンストラクタのまとまり3 # その他の定義
        # self.constructor_chunk4()  # コンストラクタのまとまり4 # UIコントロールに関わる定義

        # 完全に新規
        self.constructor_chunk5()  # コンストラクタのまとまり5 # UIコントロールに関わる定義の追加

        # base から継承 override 変更 (独自に定義しなおして上書き)
        self.settingOptionVar()  # コンストラクタのまとまりA # optionVar のセッティング
        # base から継承 override 変更 (独自に定義しなおして上書き)
        self.startOptionVarCmd()  # コンストラクタのまとまりB # optionVar の初期実行コマンド

        # self.options = pm.optionVar  # type: # OptionVarDict
        # self.options = upDateOptionVarsDictCmd()  # type: # dict

    # common コマンド群 ################################################################ start
    # ...
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
        self.bgcGray = [0.7, 0.7, 0.7]  # list of float

        self.clstHndle_name = ''
        self.clst_name = ''
        self.isRelative = False

        # add textField
        # final naming check 各text名
        self.cTxt_clstHndle_ckName = None
        self.cTxt_clst_ckName = None

    # base から継承 override 変更 (独自に定義しなおして上書き)
    # コンストラクタのまとまりA # optionVar のセッティング
    def settingOptionVar(self):
        u""" < コンストラクタのまとまりA # optionVar のセッティング です >

        ::

          base から継承 override 変更 (独自に定義しなおして上書き)

        #######################
        """
        # dict  # range is 6 + # range is 2
        # key:   [type(str)
        # , type(str), type(str), type(str), type(str), type(str)  # range is 6
        # , type(str), type(str)  # range is 2
        # ]
        # value: [type(str)
        # , type(str), type(str), type(str), type(str), type(str)  # range is 6
        # , type(bool), type(bool)  # range is 2
        # ]
        self.opVar_dictVal_dflt_list = ['mode0'
            , '', 'clstHndle', '', '', ''
                                        ]  # range is 6
        # value: [type(str)
        #          , type(str), type(str), type(str), type(str), type(str)
        #         ]  # range is 6

        # add autoNumbering, relative
        self.opVar_dictVal_dflt_list_addCCAndR = ['False', 'False']  # range is 2
        # value: [type(bool) type(bool)]  # range is 2

        # OptionVar DATA naming ########################################################### start
        # save settings menu により、maya optionVar への 辞書登録を実施する準備です
        # dict  # range is 6 + # range is 2
        # key:   [type(str)
        # , type(str), type(str), type(str), type(str), type(str)  # range is 6
        # , type(str), type(str)  # range is 2
        # ]
        # value: [type(str)
        # , type(str), type(str), type(str), type(str), type(str)  # range is 6
        # , type(bool), type(bool)  # range is 2
        # ]

        # range is 6
        self.optionVar01_mode_key = self.title + self.underScore + 'rdBtn_text'  # type: str
        self.optionVar01_tFld_key = self.title + self.underScore + 'txtFldA1_text'  # type: str
        self.optionVar02_tFld_key = self.title + self.underScore + 'txtFldB1_text'  # type: str
        self.optionVar03_tFld_key = self.title + self.underScore + 'txtFldC1_text'  # type: str
        self.optionVar04_tFld_key = self.title + self.underScore + 'txtFldC2_text'  # type: str
        self.optionVar05_tFld_key = self.title + self.underScore + 'txtFldC3_text'  # type: str

        # range is 2
        self.optionVar01_atNm_key = self.title + self.underScore + 'rdBtnA_bool'  # type: str
        self.optionVar01_rltv_key = self.title + self.underScore + 'rdBtnB_bool'  # type: str
        # OptionVar DATA naming ########################################################### end

    # base から継承 override 変更 (独自に定義しなおして上書き)
    # コンストラクタのまとまりB # optionVar の初期実行コマンド
    def startOptionVarCmd(self):
        u""" < コンストラクタのまとまりB # optionVar の初期実行コマンド です >

        ::

          base から継承 override 変更 (独自に定義しなおして上書き)

        #######################
        """
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
        # 「"YO_createClusterAndRename5_PyMel_rdBtnA_bool"というkeyが初めて実行されてるから無いよ！」
        # というエラーが出るのでそれを回避しています
        # #######################
        if getOptionVarCmd(self.optionVar01_atNm_key) is None:  # set default
            setOptionVarCmd(self.optionVar01_atNm_key, self.opVar_dictVal_dflt_list_addCCAndR[0])
            # self.options[self.optionVar01_atNm_key] = self.opVar_dictVal_def_list_addCCAndR[0]  # dict type(value): bool

        # add relative
        self.cCBx_check_relative = None  # type: pm.checkBox
        # #######################
        # 補足 #
        # 初めてmayaで実行すると、optionVar は辞書なので
        # 「"YO_createClusterAndRename5_PyMel_rdBtnB_bool"というkeyが初めて実行されてるから無いよ！」
        # というエラーが出るのでそれを回避しています
        # #######################
        if getOptionVarCmd(self.optionVar01_rltv_key) is None:  # set default
            setOptionVarCmd(self.optionVar01_rltv_key, self.opVar_dictVal_dflt_list_addCCAndR[1])
            # self.options[self.optionVar01_rltv_key] = self.opVar_dictVal_def_list_addCCAndR[1]  # dict type(value): bool
    # コンストラクタのまとまり群 ########################################################### end

    # 1. UI-1. メニュー コマンド群 ###################################################### start
    # base から継承 override 変更 (独自に定義しなおして上書き)
    # Save Settings 実行による optionVar の保存 関数
    def editMenuSaveSettingsCmd(self, *args):
        u""" < Save Settings 実行による optionVar の保存 関数 です >

        ::

          base から継承 override 変更 (独自に定義しなおして上書き)

        """
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
        # self.options へ ["YO_createClusterAndRename5_PyMel_rdBtnA_bool"] を保存
        getVal_fromRdBtnA = self.autoNumbering_ckBx.getValue()
        # self.options[self.optionVar01_atNm_key] = getVal_fromRdBtnA
        setOptionVarCmd(self.optionVar01_atNm_key, getVal_fromRdBtnA)

        # add relative
        # rltv_key
        # self.options へ ["YO_createClusterAndRename5_PyMel_rdBtnB_bool"] を保存
        getVal_fromRdBtnB = self.cCBx_check_relative.getValue()
        # self.options[self.optionVar01_rltv_key] = getVal_fromRdBtnB
        setOptionVarCmd(self.optionVar01_rltv_key, getVal_fromRdBtnB)

        message(args[0])

        print(getSel_fromRdBtn
              , getTxt_fromTxtFldA1, getTxt_fromTxtFldB1
              , getTxt_fromTxtFldC1, getTxt_fromTxtFldC2, getTxt_fromTxtFldC3
              , getVal_fromRdBtnA, getVal_fromRdBtnB
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

        # add relative
        # rltv_key
        rltv_key = getOptionVarCmd(self.optionVar01_rltv_key)
        # self.cCBx_check_relative.setValue(self.options[self.optionVar01_rltv_key])
        self.cCBx_check_relative.setValue(rltv_key)

        message(args[0])  # message output

        # print(self.options[self.optionVar01_mode_key]
        #
        #       , self.options[self.optionVar01_tFld_key]
        #       , self.options[self.optionVar02_tFld_key]
        #       , self.options[self.optionVar03_tFld_key]
        #       , self.options[self.optionVar04_tFld_key]
        #       , self.options[self.optionVar05_tFld_key]
        #
        #       , self.options[self.optionVar01_atNm_key]
        #       , self.options[self.optionVar01_rltv_key]
        #       )

        print(mode_key
              , tFld_key_A1, tFld_key_B1, tFld_key_C1, tFld_key_C2, tFld_key_C3
              , atNm_key, rltv_key
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
        setOptionVarCmd(self.optionVar01_mode_key, self.opVar_dictVal_dflt_list[0])  # 'mode0'
        setOptionVarCmd(self.optionVar01_tFld_key, self.opVar_dictVal_dflt_list[1])  # ''
        setOptionVarCmd(self.optionVar02_tFld_key, self.opVar_dictVal_dflt_list[2])  # 'clstHndle'
        setOptionVarCmd(self.optionVar03_tFld_key, self.opVar_dictVal_dflt_list[3])  # ''
        setOptionVarCmd(self.optionVar04_tFld_key, self.opVar_dictVal_dflt_list[4])  # ''
        setOptionVarCmd(self.optionVar05_tFld_key, self.opVar_dictVal_dflt_list[5])  # ''
        setOptionVarCmd(self.optionVar01_atNm_key, self.opVar_dictVal_dflt_list_addCCAndR[0])  # bool(0)
        setOptionVarCmd(self.optionVar01_rltv_key, self.opVar_dictVal_dflt_list_addCCAndR[1])  # bool(0)
        # self.options[self.optionVar01_mode_key] = self.opVar_dictVal_def_list[0]  # 'mode0'
        # self.options[self.optionVar01_tFld_key] = self.opVar_dictVal_def_list[1]  # ''
        # self.options[self.optionVar02_tFld_key] = self.opVar_dictVal_def_list[2]  # 'clstHndle'
        # self.options[self.optionVar03_tFld_key] = self.opVar_dictVal_def_list[3]  # ''
        # self.options[self.optionVar04_tFld_key] = self.opVar_dictVal_def_list[4]  # ''
        # self.options[self.optionVar05_tFld_key] = self.opVar_dictVal_def_list[5]  # ''
        # self.options[self.optionVar01_atNm_key] = self.opVar_dictVal_def_list_addCCAndR[0]  # bool(0)
        # self.options[self.optionVar01_rltv_key] = self.opVar_dictVal_def_list_addCCAndR[1]  # bool(0)
    # 4. UI-4. OptionVar を利用したパラメータ管理 コマンド群 ############################### end

    # 2. UI-2. 追加オプション コマンド群 ################################################ start
    # base から継承 override 変更 (独自に定義しなおして上書き)
    # pop up menu 用 制限
    # 各 textField 上に出現する pop up menu の 実行コマンド
    def textFieldPupMnuCmd(self, cmnPUpMnu, textStr, *args):
        u""" < pop up menu 用 制限 >

        ::

          各 textField 上に出現する pop up menu の 実行コマンド
          base から継承 override 変更 (独自に定義しなおして上書き)

        #######################

        #.
            :param str cmnPUpMnu:
            :param str textStr:

        #######################
        """
        print(cmnPUpMnu, textStr)
        if cmnPUpMnu == u'cmnPUpMnu_A1':  # 後ろに追加 or 総入れ替え
            self.currentTxt_A1 = self.get_currentTxt_A1()
            print(self.currentTxt_A1)
            self.cmnTxtFld_A1.setText(u'{}{}'.format(self.currentTxt_A1, textStr))
            self.cmnTxtFld_A1.setInsertionPosition(0)

            if textStr == u'~' or textStr == u'':  # 総入れ替え
                self.cmnTxtFld_A1.setText(textStr)
            elif textStr == u'@':  # 追加
                self.currentTxt_A1 = self.get_currentTxt_A1()  # 一旦現状を get する
                # @ 識別子 の複数入力を検知し、強制的に独自規定で1つに制限するメソッド 実行
                result = self.limitAtSignIdMultipleInputToOneCmd(self.currentTxt_A1, 1)
                self.cmnTxtFld_A1.setText(result)  # 修正

            self.cmnTxtFld_A1.setFont(self.defaultFont)

        elif cmnPUpMnu == u'cmnPUpMnu_B1':  # 後ろに追加 or 総入れ替え
            self.currentTxt_B1 = self.get_currentTxt_B1()
            self.cmnTxtFld_B1.setText(u'{}{}'.format(self.currentTxt_B1, textStr))
            self.cmnTxtFld_B1.setInsertionPosition(0)

            if textStr == u'~' \
                    or textStr == u'' \
                    or textStr == u'clstHndle' \
                    or textStr == u'clusterHandle'\
                    :
                # 総入れ替え
                # original 流用から変更
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
    def doAutoNumbering_ckBx_tgl_command(self, textStr, *args, **kwargs):
        u""" < ナンバリング識別子の付加の on/off の実行関数 です >

        ::

          完全に新規

          self.cmnTxtFld_A1 に付加します

        #################

        #.
            :param str textStr:

        #################
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

    # 完全に新規
    # check button 押下で実行される関数
    def check_naming_command(self, *args):
        u""" < check button 押下で実行される関数 です >

        ::

          完全に新規

        """
        get_cmnTxtFld_A1 = self.cmnTxtFld_A1.getText() or ''
        print(get_cmnTxtFld_A1)
        if not get_cmnTxtFld_A1:
            YO_logProcess.action('WARNING', u'{}\n\t\t\tLine Number:{}\n'
                                            u'ストップ\n'
                                            u'各 textFiled 内に、ユーザー指定の文字列'
                                            u'が充分に挿入されていません。'
                                            u'少なくとも、'
                                            u'第1単語フィールドへの文字列挿入は必須です。'
                                            u'Clustor 作成 の実行はストップしました。check button push'
                                 .format(self.title, YO_logger2.getLineNo())
                                 )
            # message_warning(u'各 textFiled 内に、ユーザー指定の文字列'
            #                      u'が充分に挿入されていません。'
            #                      u'少なくとも、'
            #                      u'第1単語フィールドへの文字列挿入は必須です。'
            #                      u'Clustor 作成 の実行はストップしました。check button push'
            #                      )
            pass
        else:
            self.clstHndle_name = self.checkAndReturn_cTxtFld_clstHndle_strAll()
            self.clst_name = self.create_clst_strAll_from_cTxtFld_clstHndle()
            # print (self.clstHndle_name, self.clst_name)
            if not self.clstHndle_name and not self.clst_name:
                pass
            else:
                self.cTxt_clstHndle_ckName.setLabel(self.clstHndle_name)
                # pm.text(self.cTxt_clstHndle_ckName, e = True, label = self.clstHndle_name)
                self.cTxt_clst_ckName.setLabel(self.clst_name)
                # pm.text(self.cTxt_clst_ckName, e = True, label = self.clst_name)

    # 完全に新規
    # cTxtFld_clstHndle 名を、全フィールド入力から抽出する関数
    def checkAndReturn_cTxtFld_clstHndle_strAll(self):
        u""" < cTxtFld_clstHndle 名を、全フィールド入力から抽出する関数 です >

        ::

          完全に新規

        #######################

        #.
            :return: clstHndle_name
            :rtype clstHndle_name: str

        #######################
        """
        str1, str2, str3, str4, str5 = self.outPut_cTxtFld()
        # print(str1, str2, str3, str4, str5)
        mainStrList = [i for i in (str1, str2, str3, str4, str5)]
        # print(mainStrList)

        # None を返してくるかもしれない
        clstHndle_noSideType_name = str1 + '_' + str2 + str3
        # None を返してくるかもしれない
        clstHndle_addSideType_name = str1 + '_' + str2 + str3 + '_' + str4 + str5

        clstHndle_name = ''

        if '' is str1:
            message_warning(u'ユーザー指定である、<クラスターハンドル名> Cluster Handle の入力フィールド'
                            u'が不完全です。'
                            u'ご確認ください。'
                            )
        else:
            if str5:  # サイド名がある場合
                # None を返してくるかもしれない
                clstHndle_name = clstHndle_addSideType_name
            else:  # サイド名が無い場合
                # None を返してくるかもしれない
                clstHndle_name = clstHndle_noSideType_name
        # print(clstHndle_name)
        return clstHndle_name

    # 完全に新規
    # cTxtFld_clst 名を、cTxtFld_clstHndle 全フィールド入力から再構成する関数
    def create_clst_strAll_from_cTxtFld_clstHndle(self):
        u""" < cTxtFld_clst 名を、cTxtFld_clstHndle 全フィールド入力から再構成する関数 です >

        ::

          完全に新規

        #######################

        #.

            :return: clst_name
            :rtype clst_name: str

        ######################
        """
        str1, str2, str3, str4, str5 = self.outPut_cTxtFld()
        str2 = 'clst'  # 変更2 memo): old - > u'CLST'
        mainStrList = [i for i in (str1, str2, str3, str4, str5)]

        clst_noSideType_name = str1 + '_' + str2
        clst_addSideType_name = str1 + '_' + str5 + '_' + str2

        clst_name = ''

        if '' is str1:
            message_warning(u'ユーザー指定である、<クラスターハンドル名> Cluster Handle の入力フィールド'
                            u'が不完全です。'
                            u'ご確認ください。'
                            )
        else:
            if str5:  # サイド名がある場合
                clst_name = clst_addSideType_name
            else:  # サイド名が無い場合
                clst_name = clst_noSideType_name
        return clst_name

    # 完全に新規
    # 全フィールド入力から文字列を抽出する関数
    def outPut_cTxtFld(self):
        u""" < 全フィールド入力から文字列を抽出する関数 です >
        ::

          完全に新規

        #######################

        #.
            :return: str1, str2, str3, str4, str5
            :rtype str1, str2, str3, str4, str5: Tuple(str)

        #######################
        """
        str1 = self.cmnTxtFld_A1.getText() or ''
        str2 = self.cmnTxtFld_B1.getText() or ''
        str3 = self.cmnTxtFld_C1.getText() or ''
        str4 = self.cmnTxtFld_C2.getText() or ''
        str5 = self.cmnTxtFld_C3.getText() or ''
        # print(str1, str2, str3, str4, str5)
        return str1, str2, str3, str4, str5

    # 完全に新規
    # relative 相対モード を False or True で出力するメソッド
    # コマンドベース入力における、特殊制限
    def get_currentCBx_relativeValue(self):
        u""" < relative 相対モード を False or True で出力するメソッド です >

        ::

          完全に新規

          コマンドベース入力における、特殊制限

        #######################

        #.
            :return: isRelative
            :rtype: bool

        ######################
        """
        isRelative = self.cCBx_check_relative.getValue()
        return isRelative

    # 完全に新規
    # 第2単語フィールド @ at mark 誤入力判別 関数
    # コマンドベース入力における、特殊制限
    def wrong_input_determining_tFldB1_fromCmd(self, wordLists):
        u""" < 第2単語フィールド @ at mark 誤入力判別 関数 >

        ::

          完全に新規

          コマンドベース入力における、特殊制限

        ##################

        #.
            :param list of str wordLists:

        #.
            :return isWrong:
                True: 誤入力発見, False: 誤入力なし
            :rtype: bool

        ##################
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
                                            u'Clustor 作成 の実行はストップしました。0-wrong_input_tFldB1'
                                 .format(self.title, YO_logger2.getLineNo())
                                 )
            # message_warning(u'第2単語フィールド に、'
            #                      u'@ at mark があります。'
            #                      u'当ツールでは特殊制限を設け、ここでは許可しません。'
            #                      u'Clustor 作成 の実行はストップしました。0-wrong_input_tFldB1'
            #                      )
            pass
        else:
            isWrong = False  # False: 誤入力なし
        return isWrong
    # 2. UI-2. 追加オプション コマンド群 ################################################## end

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
    #   proc1.5.
    # <共通>
    #   proc2.1. クラスター作成
    # <共通>
    #   proc2.2. 最後に、共通な naming 操作 を行っています。
    ##########################################

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
        # UIありきでの実行
        print('\n## ui_executeBtn type ##\n')
        print(u'## 継続中 ########## cluster proc1 (ui_executeBtn type)')

        # ##############################################################
        # proc1. #
        # カレントの、textField 文字列を抜き出します。
        # ###########################################
        self.mode = self.currentMode()  # int
        self.isRelative = self.get_currentCBx_relativeValue()  # bool
        self.currentTxt_A1 = self.get_currentTxt_A1()
        self.currentTxt_B1 = self.get_currentTxt_B1()
        self.currentTxt_C1 = self.get_currentTxt_C1()
        self.currentTxt_C2 = self.get_currentTxt_C2()
        self.currentTxt_C3 = self.get_currentTxt_C3()

        # ここ大事!!
        if self.isRelative:
            isRelative_str = 1  # int
        else:
            isRelative_str = 0  # int

        print(u'\n'
              u'// Result: {packageName}.'
              u'{title}.{className}().exe('
              u'mode = {modeInt}'
              u', relative = {relativeValue}'
              u', '
              u'n = ['
              u'u\'{a}\', u\'{b}\''
              u', '
              u'u\'{c1}\', u\'{c2}\', u\'{c3}\''
              u']'
              u')'
              u'\n'
              .format(packageName = self.pkgName
                      , title = self.title + self.id, className = self.className
                      , modeInt = self.mode, relativeValue = isRelative_str
                      , a = self.currentTxt_A1
                      , b = self.currentTxt_B1
                      , c1 = self.currentTxt_C1
                      , c2 = self.currentTxt_C2
                      , c3 = self.currentTxt_C3
                      )
              )
        # ##############################################################

        # ##############################
        # 一時的、選択リスト(1回目)
        # ##############################
        # 予め出力 コンポーネント選択関連
        self.selectionLists = commonCheckSelection()  # 自動で空にもなる
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
        ##############################
        print(u'TextField関連\n\t'
              u'self.wordListsSet_fromUI(wordLists) : \n\t\t'
              u'{}'.format(self.wordListsSet_fromUI)
              )
        ##############################

        # 共通な一連の関数のまとまり です
        # 場合分けによって、
        #   後の方で、proc2. rename 操作 に入っていきます
        self.setOfCommonFunctions(self.wordListsSet_fromUI)
    # 3. UI-3. common ボタン コマンド群 ################################################## end

    # 5. スクリプトベースコマンド入力への対応 ############################################# start

    ##########################################
    # <スクリプトベース用>
    ##########################################
    # プロセスの大枠 #######
    #######################
    # parameter mode, parameter relative, parameter n を対象に、
    # proc1. analysis_strs_fromCmd2 メソッドを利用して、必要な文字列を抜き出します。
    # <共通>
    #   proc1.5.
    # <共通>
    #   proc2.1. クラスター作成
    # <共通>
    #   proc2.2. 最後に、共通な naming 操作 を行っています。
    ##########################################

    # base から継承 override 変更 (独自に定義しなおして上書き)
    # < スクリプトベース用 >
    # proc1. #
    # analysis_strs_fromCmd2 メソッドを利用して、必要な文字列を抜き出します。
    # 引数: relative 追加
    def exe(self, mode = 0, relative = 0, n = None):
        u""" < スクリプトベース用 >

        ::

          base から継承 override 変更 (独自に定義しなおして上書き)

          proc1.
            analysis_strs_fromCmd2 メソッドを利用して、必要な文字列を抜き出します。
                引数: relative 追加

        #######################

        #.
            :param int mode:
                rename mode: 強制的:0, 構成要素をキープ:1 何れか

            e.g.): mode = 1

        #.
            :param int relative:
                maya default cluster attribute relative を off/on(0/1) 何れか

            e.g.): relative = 0

        #.

            :param list[str] n:
                文字列リスト(range 5)

            e.g.): n = [u'spineSpIk@', u'clstHndle', u'', u'', u'L']

        #######################
        """
        if n is None:
            n = []
        # title = cls.title
        # className = cls.className

        # UI不要での実行
        print('\n## command_execute type ##\n')
        print(u'## 継続中 ########## cluster proc1 (command_execute type)')

        # ##############################################################
        # proc1. #
        # コマンド文字列の parameter mode, parameter relative, parameter n を分析し、
        # modeInt_fromCmd, relativeValue_fromCmd, wordListsSet_fromCmd
        #   を出力する メソッド の実行
        # ###########################################
        modeInt_fromCmd, relativeValue_fromCmd, wordListsSet_fromCmd\
            = self.analysis_strs_fromCmd2(mode, relative, n)
        self.mode = modeInt_fromCmd  # str
        self.isRelative = strtobool(relativeValue_fromCmd)  # str -> bool

        print(u'\n'
              u'// Result: {packageName}.'
              u'{title}.{className}().exe('
              u'mode = {modeInt}'
              u', '
              u'relative = {relativeValue}'
              u', '
              u'n = {textAll}'
              u')'
              u'\n'
              .format(packageName = self.pkgName
                      , title = self.title + self.id, className = self.className
                      , modeInt = mode, relativeValue = relative
                      , textAll = n
                      )
              )
        # print(relative, type(relative))
        # ##############################################################

        # ##############################
        # 一時的、選択リスト(1回目)
        # ##############################
        # 予め出力 コンポーネント選択関連
        self.selectionLists = commonCheckSelection()  # 自動で空にもなる
        # ##############################
        # print(u'コンポーネント選択関連\n\t'
        #       u'cls.selectionLists : \n\t\t'
        #       u'{}'.format(cls.selectionLists)
        #       )
        # ##############################

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
    def analysis_strs_fromCmd2(self, mode, relative, n):
        u""" < スクリプトベース用 >

        ::

          完全に新規
            original( self.analysis_strs_fromCmd() ) からの引数の内容違いによる変更で、新規で定義

          コマンド文字列の parameter mode, parameter relative, parameter n を分析し、
            modeInt_fromCmd, relativeValue_fromCmd, wordListsSet_fromCmd
                を出力する メソッド

        ################################

        #.
            :param int mode:
            :param int relative:
            :param list of str n:

        #.
            :return:
                modeInt_fromCmd
                , relativeValue_fromCmd
                , wordListsSet_fromCmd
            :rtype: tuple[str, str, list[str]]

        ################################
        """
        #############################################
        # 分析1 mode ###  intを一旦文字列に変換・分析し、文字列として返す
        modeStrs = 'mode = {}'.format(mode)  # 先ず、文字列にする  # print(typStrs)
        # print(modeStrs)
        patternZ = re.compile(r'(?P<ptnModeInt>[0-1])')  # 0 or 1
        # パターン定義: 'mode = ' と , で囲まれた文字列を最短文字列で見つける
        search = patternZ.finditer(modeStrs)  # 調べる関数
        modeInt_fromCmd = []  # コマンド文字列から抽出の modeInt
        iterator = patternZ.finditer(modeStrs)
        for itr in iterator:
            modeInt_fromCmd.append(itr.group('ptnModeInt'))  # 見つけた順にリストに格納する
        modeInt_fromCmd = modeInt_fromCmd[0]
        # print(modeInt_fromCmd)

        #############################################
        # 分析2 relative ###  intを一旦文字列に変換・分析し、文字列として返す
        relaStrs = 'relative = {}'.format(relative)  # 先ず、文字列にする  # print(typStrs)
        # print(relaStrs)
        patternZ = re.compile(r'(?P<ptnRelaStr>[0-1])')  # 0 or 1
        # パターン定義: 'relative = ' と , で囲まれた文字列を最短文字列で見つける
        search = patternZ.finditer(relaStrs)  # 調べる関数
        relativeValue_fromCmd = []  # コマンド文字列から抽出の relativeValue
        iterator = patternZ.finditer(relaStrs)
        for itr in iterator:
            relativeValue_fromCmd.append(itr.group('ptnRelaStr'))  # 見つけた順にリストに格納する
        relativeValue_fromCmd = relativeValue_fromCmd[0]
        # print(relativeValue_fromCmd)
        # print(relativeValue_fromCmd, type(relativeValue_fromCmd))
        # print(relativeValue_fromCmd, type(bool(relativeValue_fromCmd)))

        #############################################
        # 分析3 n ###  リスト文字列を一旦文字列に変換・分析し、リスト文字列として返す
        # あらかじめ用意されている文字列, 'n = [u'***'...],'から、必要な文字列 *** を抽出する
        strs = 'n = {}'.format(n)  # 先ず、文字列にする
        # print(strs)
        patternC = re.compile(r'\'(?P<ptnC>.*?)\'')  # re.compile(r'u\'(?P<ptnC>.*?)\'') からの変更
        # パターン定義: u' と ' で囲まれた文字列を最短文字列で見つける
        wordListsSet_fromCmd = []  # コマンド文字列から抽出の wordListsSet
        search = patternC.finditer(strs)  # 調べる関数
        # あるならば
        if search:
            iterator = patternC.finditer(strs)
            for itr in iterator:
                # print(itr.group('ptnC'))
                wordListsSet_fromCmd.append(itr.group('ptnC'))  # 見つけた順にリストに格納する
        # print(wordListsSet_fromCmd)

        return modeInt_fromCmd, relativeValue_fromCmd, wordListsSet_fromCmd
    # 5. スクリプトベースコマンド入力への対応 ############################################### end

    # 「cluster 作成と、naming の核となる コマンド群」 ##################################### start
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

          proc1.5. #
          場合分けによって、後の方で、
              - proc2. rename 操作 に入る箇所 継続
                  具体的な箇所: # DBBB, # CBB
              - イレギュラー操作箇所 継続
                  具体的な箇所: # DAA
              - 他はすべて操作 ストップ
          させます

        ###################

        #.
            :param list of str wordLists:

        ###################
        """
        print(u'## 継続中 ########## cluster proc1.5')
        # 予め出力 TextField関連
        # textField の待機文字列が、十分にセットされているかどうかの真偽を出力する メソッド
        self.isSet_reqTxtFld = self.isSet_requiredTextField(wordLists)
        # ##############################
        # print(u'TextField関連\n\t'
        #       u'isSet_requiredTextField : \n\t\t'
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

        print(self.selectionLists)  # コンポーネント選択中

        # 予め出力
        # イレギュラー対応用変数を出力するための関数 実行
        # ここでいうイレギュラーとは、「選択1っ、atMark 0、TextField関連が完全 の時」 を言います
        # イレギュラー対応用変数 self.waiting_last_string (default: '') を予め出力
        # イレギュラー対応用変数 self.is_exists_forNCName (default: False) を予め出力
        # 選択1っ、atMark 0、TextField関連が完全 の時だけに対応
        self.renameFunction_inIrregularCases()

        # TextField名の構成から判断された、待機している最終文字
        # ##############################
        # print(u'<イレギュラー対応用>TextField名の構成から判断された、待機している最終文字\n\t'
        #       u'self.waiting_last_string : \n\t\t'
        #       u'{}'.format(self.waiting_last_string)
        #       )
        # ##############################

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
        #   proc2. rename 操作 に入る箇所
        #       具体的な箇所: # DBBB
        #   イレギュラー操作箇所
        #       具体的な箇所: # DAAA
        #   他はすべて操作をストップさせます
        #############
        # 未選択の場合  # A
        if len(self.selectionLists) == 0:  # A
            # print(u'ストップ A')
            YO_logProcess.action('ERROR', u'{}\n\t\t\tLine Number:{}\n'
                                          u'ストップ A\n'
                                          u'コンポーネント選択がされずに、クラスターを作成しようとしています。'
                                          u'cluster 作成はストップしました。cluster proc1.5-A'
                                 .format(self.title, YO_logger2.getLineNo())
                                 )
            # message_warning(u'コンポーネント選択がされずに、クラスターを作成しようとしています。'
            #                      u'cluster 作成はストップしました。cluster proc1.5-A'
            #                      )
            pass
        #############
        # しっかりとコンポーネント選択している場合  # D
        else:  # D
            # print(u'単独選択で実行中..')
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
                            # proc2.1. クラスター作成
                            # proc2.2. 最後に、共通な naming 操作
                            #   を順番に一遍に行っています。
                            # ###########################################
                            print('******** cluster create and naming, proc start.. '
                                  '************************************************'
                                  'inIrregularCases cluster proc1.5-DAAA'
                                  )
                            self.cluster_create_and_rename_exe(wordLists)
                            ##############################
                            print('******** cluster create and naming, proc done '
                                  '************************************************'
                                  'inIrregularCases cluster proc1.5-DAAA'
                                  )
                            ##############################
                    # True: 重複している 注意!
                    else:  # DAAB
                        # # print(u'ストップ DAAB')
                        YO_logProcess.action('ERROR', u'{}\n\t\t\tLine Number:{}\n'
                                                      u'ストップ DAAB\n'
                                                      u'各 textFiled 内へのユーザー指定の文字列'
                                                      u'は充分に挿入されていますが、'
                                                      u'待機している最終文字列 \'{}\' '
                                                      u'は、'
                                                      u'予めシーン内の文字列リスト内に、'
                                                      u'重複して存在している可能性があるため'
                                                      u'cluster 作成はストップしました。cluster proc1.5-DAAB'
                                             .format(self.title, YO_logger2.getLineNo()
                                                     , self.waiting_last_string
                                                     )
                                             )
                        # message_warning(u'各 textFiled 内へのユーザー指定の文字列'
                        #                      u'は充分に挿入されていますが、'
                        #                      u'待機している最終文字列 \'{}\' '
                        #                      u'は、'
                        #                      u'予めシーン内の文字列リスト内に、'
                        #                      u'重複して存在している可能性があるため'
                        #                      u'cluster 作成はストップしました。cluster proc1.5-DAAB'
                        #                      .format(self.waiting_last_string)
                        #                      )
                        # pass
                # TextField関連が完全でない
                else:  # DAB
                    # print(u'ストップ DAB')
                    YO_logProcess.action('WARNING', u'{}\n\t\t\tLine Number:{}\n'
                                                    u'ストップ DAB\n'
                                                    u'各 textFiled 内に、ユーザー指定の文字列'
                                                    u'が充分に挿入されていません。'
                                                    u'少なくとも、'
                                                    u'第1単語フィールドへの文字列挿入は必須です。'
                                                    u'cluster 作成はストップしました。cluster proc1.5-DAB'
                                         .format(self.title, YO_logger2.getLineNo())
                                         )
                    # message_warning(u'各 textFiled 内に、ユーザー指定の文字列'
                    #                      u'が充分に挿入されていません。'
                    #                      u'少なくとも、'
                    #                      u'第1単語フィールドへの文字列挿入は必須です。'
                    #                      u'cluster 作成はストップしました。cluster proc1.5-DAB'
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
                                                    u'Clustor 作成 の実行はストップしました。cluster proc1.5-DBA'
                                         .format(self.title, YO_logger2.getLineNo())
                                         )
                    # message_warning(u'単独選択で実行中です。'
                    #                      u'各 textFiled 内に、ユーザー指定の文字列'
                    #                      u'が充分に挿入されていません。'
                    #                      u'少なくとも、'
                    #                      u'第1単語フィールドへの文字列挿入は必須です。'
                    #                      u'Clustor 作成 の実行はストップしました。cluster proc1.5-DBA'
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
                                                      u'Clustor 作成 の実行はストップしました。cluster proc1.5-DBBA'
                                             .format(self.title, YO_logger2.getLineNo())
                                             )
                        # message_warning(u'各 textFiled 内に、@ (at mark) '
                        #                      u'が複数挿入されています。'
                        #                      u'可能な限り、一つの入力で留めてください。'
                        #                      u'Clustor 作成 の実行はストップしました。cluster proc1.5-DBBA'
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
                                # proc2.1. クラスター作成
                                # proc2.2. 最後に、共通な naming 操作
                                #   を順番に一遍に行っています。。
                                # ###########################################
                                print('******** cluster create and naming, proc start.. '
                                      '************************************************'
                                      'cluster proc1.5-DBBB'
                                      )
                                self.cluster_create_and_rename_exe(wordLists)
                                ##############################
                                print('******** cluster create and naming, proc done '
                                      '************************************************'
                                      'cluster proc1.5-DBBB'
                                      )
                                ##############################
    # 共通な一連の関数のまとまり ############################################# end

    # クラスター作成と naming を一遍に操作 ################################## start
    # 完全に新規
    # 一遍に操作
    # ###########################################
    # proc2.1. クラスター作成
    # proc2.2. 最後に、共通な naming 操作
    #   を順番に一遍に行っています。
    # ###########################################
    # @instance.declogger
    def cluster_create_and_rename_exe(self, wordLists):
        u""" < 一遍に操作 >

        ::

          完全に新規

          一遍に操作
          proc2.1. クラスター作成
          proc2.2. 最後に、共通な naming 操作
            を順番に一遍に行っています

        #######################

        #.
            :param wordLists: list of str

        #######################
        """
        print(u'## 継続中 ########## cluster proc2.1')
        # ##############################################################################
        # proc2.1. #
        # クラスター作成
        # ###########################################
        # print(self.isRelative)
        # クラスター作成 ################################################### start
        if not self.isRelative:  # False
            clst_list = cmds.cluster(relative = False)  # default is relative off
        else:  # True
            clst_list = cmds.cluster(relative = True)  # relatives チェックボタン 反映
        # clst_list[0] is clst_name
        # clst_list[1] is clstHndle_name
        # print(clst_list[0], clst_list[1])
        cmds.select(clst_list, r = True)
        # print(self.clst_name, self.clstHndle_name)
        # cmds.rename(clst_list[0], self.clst_name)
        # cmds.rename(clst_list[1], self.clstHndle_name)
        # クラスター作成 ##################################################### end

        selectionLists_orijinal = commonCheckSelection()  # 自動で空にもなる
        # print(selectionLists_orijinal)
        selectionLists_orijinal.reverse()  # 順番を入れ替えておく
        self.selectionLists = selectionLists_orijinal
        # print(self.selectionLists)
        self.selectionLists = self.selectionLists[:1]  # 敢えて[1] をリストから除外
        # print(self.selectionLists)

        print(u'## 継続中 ########## cluster proc2.2')
        # ##############################################################################
        # proc2.2. #
        # naming 操作
        # ###########################################
        ###########################
        # clstHndle_name のリネーム ############################################## start
        # original ネーミングエンジンを利用
        # 選択した全ノード名に対して、unique name にして更新する メソッド の実行
        self.selectionLists = self.checkAndDoUniqueName_forSlNode(self.selectionLists)
        # print(self.selectionLists)
        # original ネーミングエンジンを利用
        # rename の開始
        self.start_executeCmd(self.selectionLists, self.mode, wordLists)
        # clstHndle_name のリネーム ############################################## end
        ###########################
        clstHndle_name = commonCheckSelection()[0]  # list of str
        YO_logProcess.action('INFO'
                             , u'{}\n\t\t\tLine Number:{}\n'
                             .format(self.title, YO_logger2.getLineNo())
                             +
                             clstHndle_name
                             )
        # print(clstHndle_name)

        # #########################
        # clst_name のリネーム ################################################### start
        # 既存の clst_name 名の取得
        clst_name = cmds.listConnections(clstHndle_name, type = 'cluster')[0]
        # print(clst_name)
        #
        # clst 名を構成する ############################################### start
        # clstHndle = cmds.ls(sl = True)[0]
        # 選択されているオブジェクト名の文字列の構成を調べ出力する メソッド 実行
        self.strCompsCheck_exe(clstHndle_name)
        # ##############################
        # print(self.selCompStrs_1st, self.selCompStrs_2nd, self.selCompStrs_3rd, self.typ)
        # # print(type(self.selCompStrs_1st), type(self.selCompStrs_2nd)
        # #       , type(self.selCompStrs_3rd), type(self.typ))
        # ##############################
        str2 = 'clst'  # 変更2 memo): old - > u'CLST'
        clst_name_final = ''
        # print(self.selCompStrs_1st, self.selCompStrs_2nd, self.selCompStrs_3rd)
        if self.typ == 'underScoresCount2':  # e.g.): spine@_clstHndle_L -> spine@_clst_L
            clst_name_final = self.selCompStrs_1st + '_' + str2 + '_' + self.selCompStrs_3rd
            # 変更2 memo): old - > self.selCompStrs_1st + '_' + self.selCompStrs_3rd + '_' + str2
        elif self.typ == 'underScoresCount1':  # e.g.): spine@_clstHndle -> spine@_clst
            clst_name_final = self.selCompStrs_1st + '_' + str2
        # clst 名を構成する ################################################# end
        cmds.rename(clst_name, clst_name_final)
        # clst_name のリネーム ################################################### end
        # #########################
        YO_logProcess.action('INFO'
                             , u'{}\n\t\t\tLine Number:{}\n'
                             .format(self.title, YO_logger2.getLineNo())
                             + clst_name_final
                             )
        # print(clst_name_final)
    # クラスター作成と naming を一遍に操作 #################################### end
    # 「cluster 作成と、naming の核となる コマンド群」 ####################################### end


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
