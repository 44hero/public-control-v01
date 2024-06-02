# -*- coding: utf-8 -*-

u"""
YO_renameTool5_Modl.py

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
                    における、
                        定義
                            と
                        置換
            - 詳細: カスタムの Script Editor2 (PySide2作成UI) で置き換える為には、
                from ..TemplateForPySide2.CustomScriptEditor2SPIModule import custom_scriptEditor2_instance
                モジュールを必要とします
                - 定義箇所: 以下のように、あらかじめ カスタムの Script Editor2 モジュール
                    を定義します
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
                - 置換した箇所: 以下のように、置き換えます
                    先ず2箇所
                    ::

                        +   def ui_executeBtnCmd(self, *args):
                                ...
                                # 追加7 ####################################################### start
                                check_string = 'check'
                                ...
                                elif state == 'open':
                                        print('open済、再利用')
                                        self.scriptEditor2.append_default('open済、再利用')
                                # 追加7 ####################################################### end
                                ...

                        +   def exe(self, *args):
                                ...
                                # 追加7 ####################################################### start
                                check_string = 'check'
                                ...
                                elif state == 'open':
                                        print('open済、再利用')
                                        self.scriptEditor2.append_default('open済、再利用')
                                # 追加7 ####################################################### end
                                ...
                    その他、多数ある箇所
                    ::

                        +   # 追加7 ########################################################### start
                            self.scriptEditor2.append_default(...)
                            # 追加7 ########################################################### end

                        +   # 追加7 ########################################################### start
                            self.scriptEditor2.append_error(...)
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

    done: 2023/11/20
        - 変換箇所5
            - 概要: プロセス出力をダイエット
            - 詳細: 以下の箇所 合計28箇所中、 ERROR 箇所を除く 合計23箇所 をコメントアウト
            ::

                # YO_logProcess.action(...)

        version = '-4.1-'

    done: 2023/10/25
        汎用箇所を、モジュールとして読み込みに変更

        version = '-4.0-'

    done: 2023/09/08~2023/09/20
        - python2系 -> python3系 変換
            - 変換箇所1
                - 概要: dict関連
                - 詳細: 以下参照
                ::

                    -   for ptnNumber_keys, ptnFindStrs_values in ptn_dict.items():...
                    +   for ptnNumber_keys, ptnFindStrs_values in list(ptn_dict.items()):...
            - 変換箇所2
                - 概要: dict関連
                - 詳細: 以下参照
                ::

                    -   for keys, values in ptnX_dict.items():...
                    +   for keys, values in list(ptnX_dict.items()):...
            - 変換箇所3
                - 概要: dict関連
                - 詳細: 以下参照
                ::

                    -   for keysD, valuesD in ptn_dictD.items():...
                    +   for keysD, valuesD in list(ptn_dictD.items()):...
            - 変換箇所4
                - 概要: unicode関連
                - 詳細: 以下参照
                ::

                    -   def analysis_strs_fromCmd(self, mode, n):
                            ...
                            #############################################
                            # 分析2 n ###
                            ...
                            patternC = re.compile(r'u\'(?P<ptnC>.*?)\'')  # 変更対象箇所
                            ...

                    +   def analysis_strs_fromCmd(self, mode, n):
                            ...
                            #############################################
                            # 分析2 n ###
                            ...
                            patternC = re.compile(r'\'(?P<ptnC>.*?)\'')  # 変更
                            ...
      version = '-3.0-'

    done: 2023/09/08
        - 追加
            - リネームし終わったノード全てを改めて全選択するためのノード名リスト格納宣言
                - 新規関数
                    ::

                        # コンストラクタのまとまりaddA # その他の定義2
                        def constructor_chunk_addA(self):
                            ...
                            # 格納用リスト宣言
                            self.initSelectionNodeUUIDLists = []
                            ...

                        # 単独選択ノードから単独UUID番号をゲットする関数
                        def get_ID_fromSel(self, sel):
                            ...

                        # 単独UUID番号から単独ノードを選択する関数
                        def select_fromID(self, get_ID):
                            ...

                        # 選択ノードの明示の為に準備する格納用
                        def initSelectionNode_storeUUID(self, lists):
                            ...

                        # 選択ノードの明示の為の再選択用
                        def initSelectionNode_reSelect(self, lists):
                            ...
                - コード
                    ::

                        def ui_executeBtnCmd(self, *args):
                            ...

                        def exe(self, mode = 0, n = None, nodeType = ''):
                            ...

                        両関数へ...以下を追加

                        +   # 追加
                            # 派生元 renameTool5 独自の 選択ノードの明示に使用
                            self.initSelectionNodeUUIDLists.__init__()  # 常に初期化で空にする
                            self.initSelectionNode_storeUUID(self.selectionLists)

                        +   # 追加
                            # かなり初期の段階で選択を実行します
                            # b/c): 派生元 renameTool5 独自の 選択ノードの明示に使用
                            cmds.select(cl = True)
                            self.initSelectionNode_reSelect(self.initSelectionNodeUUIDLists)
        version = '-2.6-'

    done: 2023/05/31
        - エラー修正1
            - 選択された全ノード名に対して、unique name になるように内容を見直す
        - 新規1
            - エラー修正1に伴う追加1
                - 必要な関数の追加
        version = '-2.5-'

    done: 2023/03/13~2022/04/10
        - 派生ファイル作成を考慮してコードの見直し
        version = '-2.0-'

    done: 2023/02/22~2022/02/23
        - 新規
        version = '-1.0-'
"""

# 標準ライブラリ #################################################################
import re
import string
from importlib import reload
# from functools import partial  # partial 利用時は、最後の引数に、*args 要時あり
from time import sleep
from typing import Any, List
# import pprint

# サードパーティライブラリ #########################################################
import maya.cmds as cmds
# from pymel import core as pm
# import maya.OpenMaya as om
# 追加7
from PySide2.QtCore import Slot

# ローカルで作成したモジュール ######################################################
# basic_configuration(基本構成)
from .config import SPACE, TITLE, VERSION
# 汎用ライブラリー の使用 ################################################################ start
from ..lib.message import message
from ..lib.message_warning import message_warning
# from ..lib.commonCheckJoint import commonCheckJoint  # :return: bool
from ..lib.commonCheckSelection import commonCheckSelection  # :return: string
# 個別ノードの持つ単独UUID番号、に対する独自操作 モジュール
from ..lib.YO_uuID import UUID
yo_uuid = UUID()
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
# 追加7
import YO_utilityTools.TemplateForPySide2.CustomScriptEditor2
reload(YO_utilityTools.TemplateForPySide2.CustomScriptEditor2)
from ..TemplateForPySide2.CustomScriptEditor2SPIModule import custom_scriptEditor2_instance


class RT_Modl(object):
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

            - 「rename の核となる コマンド群」

                - 共通な一連の関数のまとまり

                - イレギュラー対応用

                - rename操作

    ######
    """
    def __init__(self):
        self.constructor_chunk1()  # コンストラクタのまとまり1 # パッケージ名等の定義
        self.constructor_chunk2()  # コンストラクタのまとまり2 # タイトル等の定義
        self.constructor_chunk3()  # コンストラクタのまとまり3 # その他の定義
        self.constructor_chunk4()  # コンストラクタのまとまり4 # UIコントロールに関わる定義

        self.settingOptionVar()  # コンストラクタのまとまりA # optionVar のセッティング
        self.startOptionVarCmd()  # コンストラクタのまとまりB # optionVar の初期実行コマンド

        # self.options = pm.optionVar  # type: # OptionVarDict
        # self.options = upDateOptionVarsDictCmd()  # type: # dict

        # 追加
        self.constructor_chunk_addA_uuid()  # コンストラクタのまとまりaddA # uuid格納用

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

    # コンストラクタのまとまり群 ######################################################### start
    # コンストラクタのまとまり1 # パッケージ名等の定義
    def constructor_chunk1(self):
        u""" < コンストラクタのまとまり1 # パッケージ名等の定義 です > """
        self.pkgName = __package__
        self.id = '_Modl'

    # コンストラクタのまとまり2 # タイトル等の定義
    def constructor_chunk2(self):
        u""" < コンストラクタのまとまり2 # タイトル等の定義 です > """
        self.title = TITLE
        # self.win = TITLE + '_ui'
        # self.space = SPACE
        # self.version = VERSION
        self.underScore = '_'

    # コンストラクタのまとまり3 # その他の定義
    def constructor_chunk3(self):
        u""" < コンストラクタのまとまり3 # その他の定義 です > """
        self.defaultFont = 'plainLabelFont'
        self.tempFont = 'obliqueLabelFont'

        self.warningMessage_default = u'共通:規定文字以外が一つ以上見つかったので、' \
                                      u'該当箇所は全てキャメル表記に強制します。'

        self.className = self.__class__.__name__  # class name を出力

    # コンストラクタのまとまり4 # UIコントロールに関わる定義
    def constructor_chunk4(self):
        u""" < コンストラクタのまとまり4 # UIコントロールに関わる定義 です > """
        self.mode = 0
        self.mode_collection = 'mode0'
        self.mode_handleNameLists = ('mode0', 'mode1')  # 各radioButton のハンドル名です

        self.textFieldBgc_A1 = [0.65, 0.6, 0.6]
        self.textFieldBgc_B1 = [0.6, 0.65, 0.6]
        self.textFieldBgc_C = [0.6, 0.6, 0.65]
        self.textFieldBgc_C_headsUp = [0.8, 0.6, 0.8]  # 注意喚起カラー

        self.currentTxt_A1 = u''
        self.currentTxt_B1 = u''
        self.currentTxt_C1 = u''
        self.currentTxt_C2 = u''
        self.currentTxt_C3 = u''

        self.wordListsSet_fromUI = []  # UIから抽出の wordListsSet
        self.selectionLists = []  # 初期選択リスト
        self.newLists = []  # 初期選択リストの変化に対応した 新規 格納場所 仮リスト
        self.strsDecompListsAll = []  # それぞれの要素の, 分解リスト格納場所 [[], [], [], [], []]
        self.getObj = []  # シーン内のDGノード名の格納場所 リスト
        self.is_exists_forSlNode = False  # is exists forSelectedNode(選択しているノードに対しての真偽)
        self.is_exists_forNCName = False  # is exists forNewCandidateName(新規候補名に対しての真偽)

        # 追加
        self.isSet_reqTxtFld = False  # textField の待機文字列が、十分にセットされているかどうかの真偽
        # self.isUniqueName_list = []  # 選択された全ノードに対して、一つずつ、unique な名前かどうか真偽をリスト化 list of bool
        self.atMark_count = int  # @ (at mark) の数  # int
        self.selCompStrs_1st, self.selCompStrs_2nd, self.selCompStrs_3rd, self.typ = str, str, str, str
        self.assemble_A, self.assemble_B, self.assemble_C1, self.assemble_C2, self.assemble_C3 = '', '', '', '', ''
        self.waiting_last_string = ''  # イレギュラー対応用変数
        self.wordListsSet_fromCmd = []  # コマンドから抽出の wordListsSet

    # 追加
    # コンストラクタのまとまりaddA # uuid格納用
    def constructor_chunk_addA_uuid(self):
        u""" < コンストラクタのまとまりaddA # uuid格納用 です >

        ::

          追加
          独自の 選択ノードの明示に使用
        """
        # 格納用リスト宣言
        self.initSelectionNodeUUIDListsA = yo_uuid.initSelectionNodeUUIDLists

    # コンストラクタのまとまりA # optionVar のセッティング
    def settingOptionVar(self):
        u""" < コンストラクタのまとまりA # optionVar のセッティング です > """
        # dict  # range is 6
        # key:   [type(str)
        # , type(str), type(str), type(str), type(str), type(str)
        # ]  # range is 6
        # value: [type(str)
        # , type(str), type(str), type(str), type(str), type(str)
        # ]  # range is 6
        self.opVar_dictVal_dflt_list = ['mode0'
            , '', '', '', '', ''
                                        ]  # range is 6

        # DATA naming ########################################################### start
        # save settings menu により、maya optionVar への 辞書登録を実施する準備です
        # dict  # range is 6
        # key:   [type(str)
        # , type(str), type(str), type(str), type(str), type(str)
        # ]  # range is 6
        # value: [type(str)
        # , type(str), type(str), type(str), type(str), type(str)
        # ]  # range is 6

        # range is 6
        self.optionVar01_mode_key = self.title + self.underScore + 'rdBtn_text'  # type: str
        self.optionVar01_tFld_key = self.title + self.underScore + 'txtFldA1_text'  # type: str
        self.optionVar02_tFld_key = self.title + self.underScore + 'txtFldB1_text'  # type: str
        self.optionVar03_tFld_key = self.title + self.underScore + 'txtFldC1_text'  # type: str
        self.optionVar04_tFld_key = self.title + self.underScore + 'txtFldC2_text'  # type: str
        self.optionVar05_tFld_key = self.title + self.underScore + 'txtFldC3_text'  # type: str
        # DATA naming ########################################################### end

    # コンストラクタのまとまりB # optionVar の初期実行コマンド
    def startOptionVarCmd(self):
        u""" < コンストラクタのまとまりB # optionVar の初期実行コマンド です > """
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
            # self.options[self.optionVar01_mode_key] = self.opVar_dictVal_dflt_list[0]  # dict type(value): str

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
            # self.options[self.optionVar01_tFld_key] = self.opVar_dictVal_dflt_list[1]  # dict type(value): str

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
            # self.options[self.optionVar02_tFld_key] = self.opVar_dictVal_dflt_list[2]  # dict type(value): str

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
            # self.options[self.optionVar03_tFld_key] = self.opVar_dictVal_dflt_list[3]  # dict type(value): str

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
            # self.options[self.optionVar04_tFld_key] = self.opVar_dictVal_dflt_list[4]  # dict type(value): str

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
            # self.options[self.optionVar05_tFld_key] = self.opVar_dictVal_dflt_list[5]  # dict type(value): str
    # コンストラクタのまとまり群 ########################################################### end

    # 1. UI-1. メニュー コマンド群 ###################################################### start
    # Save Settings 実行による optionVar の保存 関数
    def editMenuSaveSettingsCmd(self, *args):
        u""" < Save Settings 実行による optionVar の保存 関数 です > """
        # mode key
        # self.options へ ["YO_renameTool4_PyMel_rdBtn_text"] を保存
        getSel_fromRdBtn = self.cmnModeRdBtnClcton.getSelect()
        # print (self.options[self.optionVar01_mode_key])
        # self.options[self.optionVar01_mode_key] = getSel_fromRdBtn
        # print (self.options[self.optionVar01_mode_key])
        setOptionVarCmd(self.optionVar01_mode_key, getSel_fromRdBtn)
        # self.options = upDateOptionVarsDictCmd()

        # tFld_key A1
        # self.options へ ["YO_renameTool4_PyMel_txtFldA1_text"] を保存
        getTxt_fromTxtFldA1 = self.cmnTxtFld_A1.getText()
        # print (self.options[self.optionVar01_tFld_key])
        # self.options[self.optionVar01_tFld_key] = getTxt_fromTxtFldA1
        # print (self.options[self.optionVar01_tFld_key])
        setOptionVarCmd(self.optionVar01_tFld_key, getTxt_fromTxtFldA1)
        # self.options = upDateOptionVarsDictCmd()

        # tFld_key B1
        # self.options へ ["YO_renameTool4_PyMel_txtFldB1_text"] を保存
        getTxt_fromTxtFldB1 = self.cmnTxtFld_B1.getText()
        # print (self.options[self.optionVar02_tFld_key])
        # self.options[self.optionVar02_tFld_key] = getTxt_fromTxtFldB1
        # print (self.options[self.optionVar02_tFld_key])
        setOptionVarCmd(self.optionVar02_tFld_key, getTxt_fromTxtFldB1)
        # self.options = upDateOptionVarsDictCmd()

        # tFld_key C1
        # self.options へ ["YO_renameTool4_PyMel_txtFldC1_text"] を保存
        getTxt_fromTxtFldC1 = self.cmnTxtFld_C1.getText()
        # print (self.options[self.optionVar03_tFld_key])
        # self.options[self.optionVar03_tFld_key] = getTxt_fromTxtFldC1
        # print (self.options[self.optionVar03_tFld_key])
        setOptionVarCmd(self.optionVar03_tFld_key, getTxt_fromTxtFldC1)
        # self.options = upDateOptionVarsDictCmd()

        # tFld_key C2
        # self.options へ ["YO_renameTool4_PyMel_txtFldC2_text"] を保存
        getTxt_fromTxtFldC2 = self.cmnTxtFld_C2.getText()
        # print (self.options[self.optionVar04_tFld_key])
        # self.options[self.optionVar04_tFld_key] = getTxt_fromTxtFldC2
        # print (self.options[self.optionVar04_tFld_key])
        setOptionVarCmd(self.optionVar04_tFld_key, getTxt_fromTxtFldC2)
        # self.options = upDateOptionVarsDictCmd()

        # tFld_key C3
        # self.options へ ["YO_renameTool4_PyMel_txtFldC3_text"] を保存
        getTxt_fromTxtFldC3 = self.cmnTxtFld_C3.getText()
        # print (self.options[self.optionVar05_tFld_key])
        # self.options[self.optionVar05_tFld_key] = getTxt_fromTxtFldC3
        # print (self.options[self.optionVar05_tFld_key])
        setOptionVarCmd(self.optionVar05_tFld_key, getTxt_fromTxtFldC3)
        # self.options = upDateOptionVarsDictCmd()

        message(args[0])

        # print(getSel_fromRdBtn
        #       , getTxt_fromTxtFldA1, getTxt_fromTxtFldB1
        #       , getTxt_fromTxtFldC1, getTxt_fromTxtFldC2, getTxt_fromTxtFldC3
        #       )

    # Reload 実行 関数
    # View へ移動...

    # Help 実行 関数
    # View へ移動...

    # Close 実行 関数
    # View へ移動...
    # 1. UI-1. メニュー コマンド群 ######################################################## end

    # 4. UI-4. OptionVar を利用したパラメータ管理 コマンド群 ############################# start
    # UI-4. optionVar からの値の復元 実行 関数
    def restoreOptionVarCmd(self, *args):
        u""" < UI-4. optionVar からの値の復元 実行 関数 です > """
        # mode_key
        # self.cmnModeRdBtnClcton.setSelect(self.options[self.optionVar01_mode_key])
        mode_key = getOptionVarCmd(self.optionVar01_mode_key)  # type: str
        self.cmnModeRdBtnClcton.setSelect(mode_key)  # type: pm.radioCollection

        # tFld_key_A1
        # self.cmnTxtFld_A1.setText(self.options[self.optionVar01_tFld_key])
        tFld_key_A1 = getOptionVarCmd(self.optionVar01_tFld_key)  # type: str
        self.cmnTxtFld_A1.setText(tFld_key_A1)  # type: pm.textField
        # font 変更も加味
        if len(tFld_key_A1):
            self.cmnTxtFld_A1.setFont(self.defaultFont)

        # tFld_key_B1
        # self.cmnTxtFld_B1.setText(self.options[self.optionVar02_tFld_key])
        tFld_key_B1 = getOptionVarCmd(self.optionVar02_tFld_key)  # type: str
        self.cmnTxtFld_B1.setText(tFld_key_B1)  # type: pm.textField
        # font 変更も加味
        if len(tFld_key_B1):
            self.cmnTxtFld_B1.setFont(self.defaultFont)

        # tFld_key_C1
        # self.cmnTxtFld_C1.setText(self.options[self.optionVar03_tFld_key])
        tFld_key_C1 = getOptionVarCmd(self.optionVar03_tFld_key)  # type: str
        self.cmnTxtFld_C1.setText(tFld_key_C1)  # type: pm.textField
        # font 変更も加味
        if len(tFld_key_C1):
            self.cmnTxtFld_C1.setFont(self.defaultFont)

        # tFld_key_C2
        # self.cmnTxtFld_C2.setText(self.options[self.optionVar04_tFld_key])
        tFld_key_C2 = getOptionVarCmd(self.optionVar04_tFld_key)  # type: str
        self.cmnTxtFld_C2.setText(tFld_key_C2)  # type: pm.textField
        # font 変更も加味
        if len(tFld_key_C2):
            self.cmnTxtFld_C2.setFont(self.defaultFont)

        # tFld_key_C3
        # self.cmnTxtFld_C3.setText(self.options[self.optionVar05_tFld_key])
        tFld_key_C3 = getOptionVarCmd(self.optionVar05_tFld_key)  # type: str
        self.cmnTxtFld_C3.setText(tFld_key_C3)  # type: pm.textField
        # font 変更も加味
        if len(tFld_key_C3):
            self.cmnTxtFld_C3.setFont(self.defaultFont)

        message(args[0])  # message output

        # print(self.options[self.optionVar01_mode_key]
        #       , self.options[self.optionVar01_tFld_key]
        #       , self.options[self.optionVar02_tFld_key]
        #       , self.options[self.optionVar03_tFld_key]
        #       , self.options[self.optionVar04_tFld_key]
        #       , self.options[self.optionVar05_tFld_key]
        #       )

        # print(mode_key
        #       , tFld_key_A1, tFld_key_B1
        #       , tFld_key_C1, tFld_key_C2, tFld_key_C3
        #       )

    # UI-4. optionVar の value を default に戻す操作 関数
    def set_default_value_toOptionVar(self):
        u""" < UI-4. optionVar の value を default に戻す操作 関数 です >

        ::

          self.opVar_dictVal_dflt_list = ['mode0', '', '', '', '', '']  # list of str

        """
        # self.options[self.optionVar01_mode_key] = self.opVar_dictVal_dflt_list[0]  # 'mode0'
        # self.options[self.optionVar01_tFld_key] = self.opVar_dictVal_dflt_list[1]  # ''
        # self.options[self.optionVar02_tFld_key] = self.opVar_dictVal_dflt_list[2]  # ''
        # self.options[self.optionVar03_tFld_key] = self.opVar_dictVal_dflt_list[3]  # ''
        # self.options[self.optionVar04_tFld_key] = self.opVar_dictVal_dflt_list[4]  # ''
        # self.options[self.optionVar05_tFld_key] = self.opVar_dictVal_dflt_list[5]  # ''

        setOptionVarCmd(self.optionVar01_mode_key, self.opVar_dictVal_dflt_list[0])  # 'mode0'
        setOptionVarCmd(self.optionVar01_tFld_key, self.opVar_dictVal_dflt_list[1])  # ''
        setOptionVarCmd(self.optionVar02_tFld_key, self.opVar_dictVal_dflt_list[2])  # ''
        setOptionVarCmd(self.optionVar03_tFld_key, self.opVar_dictVal_dflt_list[3])  # ''
        setOptionVarCmd(self.optionVar04_tFld_key, self.opVar_dictVal_dflt_list[4])  # ''
        setOptionVarCmd(self.optionVar05_tFld_key, self.opVar_dictVal_dflt_list[5])  # ''
    # 4. UI-4. OptionVar を利用したパラメータ管理 コマンド群 ############################### end

    # 2. UI-2. 追加オプション コマンド群 ################################################ start
    # radioCollection 内の2つの内、どちらを選択中かを get する関数
    def get_currentModeRdBtn(self):
        u""" < radioCollection 内の2つの内、どちらを選択中かを get する関数 です >

        #######################

        #.
            :return: self.mode_collection
            :rtype: str

        #######################
        """
        self.mode_collection = self.cmnModeRdBtnClcton.getSelect()
        return self.mode_collection

    # current mode を 0 or 1 で出力するメソッド
    def currentMode(self):
        u""" < current mode を 0 or 1 で出力するメソッド >

        #######################

        #.
            :return: self.mode
            :rtype: int

        #######################
        """
        self.mode_collection = self.get_currentModeRdBtn()
        if self.mode_collection == 'mode0':
            self.mode = 0
        elif self.mode_collection == 'mode1':
            self.mode = 1
        return self.mode

    # このメソッドにより、current text string を、モード変更により、変化させています。
    # もしも、textField 一つにでも 何か入力があった場合は、
    # モード変更しても、current text string を変更させず、引き継ぐ挙動をします。
    def currentModeCmd(self, mode_textStr, *args):
        u""" <>

        ::

          このメソッドにより、current text string を、モード変更により、変化させています。
          もしも、textField 一つにでも 何か入力があった場合は、
          モード変更しても、current text string を変更させず、引き継ぐ挙動をします。

        #######################

        #.
            :param str mode_textStr:

        #######################
        """
        # print(mode_textStr)
        self.currentTxt_A1 = self.get_currentTxt_A1()
        self.currentTxt_B1 = self.get_currentTxt_B1()
        self.currentTxt_C1 = self.get_currentTxt_C1()
        self.currentTxt_C2 = self.get_currentTxt_C2()
        self.currentTxt_C3 = self.get_currentTxt_C3()
        # print(self.currentTxt_A1, self.currentTxt_B1
        #       , self.currentTxt_C1, self.currentTxt_C2, self.currentTxt_C3
        #       )
        if mode_textStr == 'mode1':
            if self.currentTxt_A1 == u'' and self.currentTxt_B1 == u''\
                    and self.currentTxt_C1 == u''\
                    and self.currentTxt_C2 == u'' \
                    and self.currentTxt_C3 == u''\
                    :
                self.edt_currentTxt_A1(u'~')
                self.edt_currentTxt_B1(u'~')
                self.edt_currentTxt_C1(u'~')
                self.edt_currentTxt_C2(u'')
                self.edt_currentTxt_C3(u'')
        elif mode_textStr == 'mode0':
            if self.currentTxt_A1 == u'~' and self.currentTxt_B1 == u'~'\
                    and self.currentTxt_C1 == u'~' \
                    and self.currentTxt_C2 == u'' \
                    and self.currentTxt_C3 == u''\
                    :
                self.edt_currentTxt_A1(u'')
                self.edt_currentTxt_B1(u'')
                self.edt_currentTxt_C1(u'')
                self.edt_currentTxt_C2(u'')
                self.edt_currentTxt_C3(u'')

    # textField A1 setメソッド
    def edt_currentTxt_A1(self, textStr, *args):
        u""" < textField A1 setメソッド >

        #######################

        #.
            :param str textStr:

        #.
            :return: self.currentTxt_A1
            :rtype : str

        #######################
        """
        self.currentTxt_A1 = self.cmnTxtFld_A1.setText(textStr)
        return self.currentTxt_A1

    # textField B1 setメソッド
    def edt_currentTxt_B1(self, textStr, *args):
        u""" < textField B1 setメソッド >

        #######################

        #.
            :param str textStr:

        #.
            :return: self.currentTxt_B1
            :rtype: str

        #######################
        """
        self.currentTxt_B1 = self.cmnTxtFld_B1.setText(textStr)
        return self.currentTxt_B1

    # textField C1 setメソッド
    def edt_currentTxt_C1(self, textStr, *args):
        u""" < textField C1 setメソッド >

        #######################

        #.
            :param str textStr:

        #.
            :return: self.currentTxt_C1
            :rtype: str

        #######################
        """
        self.currentTxt_C1 = self.cmnTxtFld_C1.setText(textStr)
        return self.currentTxt_C1

    # textField C2 setメソッド
    def edt_currentTxt_C2(self, textStr, *args):
        u""" < textField C2 setメソッド >

        #######################

        #.
            :param str textStr:

        #.
            :return: self.currentTxt_C2
            :rtype: str

        #######################
        """
        self.currentTxt_C2 = self.cmnTxtFld_C2.setText(textStr)
        return self.currentTxt_C2

    # textField C3 setメソッド
    def edt_currentTxt_C3(self, textStr, *args):
        u""" < textField C3 setメソッド >

        #######################

        #.
            :param str textStr:

        #.
            :return: self.currentTxt_C3
            :rtype: str

        #######################
        """
        self.currentTxt_C3 = self.cmnTxtFld_C3.setText(textStr)
        return self.currentTxt_C3

    # textField A1 の current text を返す getメソッド
    def get_currentTxt_A1(self):
        u""" < textField A1 の current text を返す getメソッド >

        #######################

        #.
            :return: self.currentTxt_A1
            :rtype: str

        #######################
        """
        self.currentTxt_A1 = self.cmnTxtFld_A1.getText()
        return self.currentTxt_A1

    # textField B1 の current text を返す getメソッド
    def get_currentTxt_B1(self):
        u""" < textField B1 の current text を返す getメソッド >

        #######################

        #.
            :return: self.currentTxt_B1
            :rtype: str

        #######################
        """
        self.currentTxt_B1 = self.cmnTxtFld_B1.getText()
        return self.currentTxt_B1

    # textField C1 の current text を返す getメソッド
    def get_currentTxt_C1(self):
        u""" < textField C1 の current text を返す getメソッド >

        #######################

        #.
            :return: self.currentTxt_C1
            :rtype: str

        #######################
        """
        self.currentTxt_C1 = self.cmnTxtFld_C1.getText()
        return self.currentTxt_C1

    # textField C2 の current text を返す getメソッド
    def get_currentTxt_C2(self):
        u""" < textField C2 の current text を返す getメソッド >

        #######################

        #.
            :return: self.currentTxt_C2
            :rtype: str

        #######################
        """
        self.currentTxt_C2 = self.cmnTxtFld_C2.getText()
        return self.currentTxt_C2

    # textField C3 の current text を返す getメソッド
    def get_currentTxt_C3(self):
        u""" < textField C3 の current text を返す getメソッド >

        #######################

        #.
            :return: self.currentTxt_C3
            :rtype: str

        #######################
        """
        self.currentTxt_C3 = self.cmnTxtFld_C3.getText()
        return self.currentTxt_C3

    # 各 textField から抽出した strings をまとめ、list にする メソッド
    def createLists_fromCurrentTxtAll(self):
        u""" < 各 textField から抽出した strings をまとめ、list にする メソッド >

        #######################

        #.
            :return: self.wordListsSet_fromUI
            :rtype: list

        #######################
        """
        self.currentTxt_A1 = self.get_currentTxt_A1()
        self.currentTxt_B1 = self.get_currentTxt_B1()
        self.currentTxt_C1 = self.get_currentTxt_C1()
        self.currentTxt_C2 = self.get_currentTxt_C2()
        self.currentTxt_C3 = self.get_currentTxt_C3()
        for tx in (self.currentTxt_A1, self.currentTxt_B1
                   , self.currentTxt_C1, self.currentTxt_C2, self.currentTxt_C3):
            self.wordListsSet_fromUI.append(tx)
        return self.wordListsSet_fromUI

    # pop up menu 用 制限
    # 各 textField 上に出現する pop up menu の 実行コマンド
    def textFieldPupMnuCmd(self, cmnPUpMnu, textStr, *args):
        u""" < pop up menu 用 制限 >

        ::

          各 textField 上に出現する pop up menu の 実行コマンド

        #######################

        #.
            :param str cmnPUpMnu:
            :param str textStr:

        #######################
        """
        # print(cmnPUpMnu, textStr)
        if cmnPUpMnu == u'cmnPUpMnu_A1':  # 後ろに追加 or 総入れ替え
            self.currentTxt_A1 = self.get_currentTxt_A1()
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

            if textStr == u'~' or textStr == u'':  # 総入れ替え
                self.cmnTxtFld_B1.setText(textStr)
            elif textStr == u'spIKjt' \
                    or textStr == u'jt' or textStr == u'if' \
                    or textStr == u'jtPxy' or textStr == u'ctrl':  # 総入れ替え
                self.cmnTxtFld_B1.setText(textStr)
            elif textStr == u'geo' or textStr == u'bindGeo':  # 総入れ替え
                self.cmnTxtFld_B1.setText(textStr)
            elif textStr == u'@':  # 追加
                self.currentTxt_B1 = self.get_currentTxt_B1()  # 一旦現状を get する
                # @ 識別子 の複数入力を検知し、強制的に独自規定で1つに制限するメソッド 実行
                result = self.limitAtSignIdMultipleInputToOneCmd(self.currentTxt_B1, 2)
                self.cmnTxtFld_B1.setText(result)  # 修正

            self.cmnTxtFld_B1.setFont(self.defaultFont)

        elif cmnPUpMnu == u'cmnPUpMnu_C1':  # 総入れ替え
            self.cmnTxtFld_C1.setText(textStr)
            self.cmnTxtFld_C1.setFont(self.defaultFont)

            if textStr == u'@':
                # 注意喚起 発動
                message_warning(u'第3単語-要素2フィールド または 第3単語-要素3フィールド'
                                u'への入力が必須となります。'
                                u'ご注意ください。'
                                )
                # カウントアップを利用し明滅を表現する注意喚起メソッドの実行
                self.headsUp_timer(7)  # 注意喚起カラー明滅
            elif textStr == u'':
                # 注意喚起カラーの解除
                self.cmnTxtFld_C1.setBackgroundColor(self.textFieldBgc_C)
                self.cmnTxtFld_C2.setBackgroundColor(self.textFieldBgc_C)
                self.cmnTxtFld_C3.setBackgroundColor(self.textFieldBgc_C)

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
                # 注意喚起カラーの解除
                self.cmnTxtFld_C1.setFont(self.defaultFont)
                self.cmnTxtFld_C1.setBackgroundColor(self.textFieldBgc_C)
                self.cmnTxtFld_C2.setFont(self.defaultFont)
                self.cmnTxtFld_C2.setBackgroundColor(self.textFieldBgc_C)
                self.cmnTxtFld_C3.setFont(self.defaultFont)
                self.cmnTxtFld_C3.setBackgroundColor(self.textFieldBgc_C)

    # カウントアップを利用し明滅を表現する注意喚起メソッド
    def headsUp_timer(self, secs):
        u""" < カウントアップを利用し明滅を表現する注意喚起メソッド です >

        #######################

        #.
            :param float secs: 秒

        #######################
        """
        for i in range(0, secs):
            # print(i)
            sleep(0.25)
            if i % 2 == 0:  # 偶数
                # 注意喚起カラー暗
                self.cmnTxtFld_C1.setBackgroundColor(self.textFieldBgc_C_headsUp)
                self.cmnTxtFld_C2.setBackgroundColor(self.textFieldBgc_C_headsUp)
                self.cmnTxtFld_C3.setBackgroundColor(self.textFieldBgc_C_headsUp)
                cmds.refresh()
            else:  # 奇数
                # 注意喚起カラー明
                self.cmnTxtFld_C1.setBackgroundColor(self.textFieldBgc_C)
                self.cmnTxtFld_C2.setBackgroundColor(self.textFieldBgc_C)
                self.cmnTxtFld_C3.setBackgroundColor(self.textFieldBgc_C)
                cmds.refresh()
        # print(u'時間です！！！')

    # textField へのタイピング入力 用 制限
    # 各 textField へのタイピング入力に、一連の制限をかける コマンド
    def limitedTypingInputCmd(self, cmnTxtFld, *args):
        u""" < textField へのタイピング入力 用 制限>

        ::

          各 textField へのタイピング入力に、一連の制限をかける コマンド

        #######################

        #.
            :param str cmnTxtFld:

        #######################

        """
        # print(cmnTxtFld)
        if cmnTxtFld == u'cmnTxtFld_A1':
            self.currentTxt_A1 = self.get_currentTxt_A1()
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
                # print('A')
                # print(self.currentTxt_A1)
                # print('B')
                self.currentTxt_A1 = self.exceptCheck_A1(self.currentTxt_A1)  # 更に調べます。。。
                # print(self.currentTxt_A1)
                # print('D')
                # @ 識別子 の複数入力を検知し、強制的に独自規定で1つに制限するメソッド 実行
                result = self.limitAtSignIdMultipleInputToOneCmd(self.currentTxt_A1, 1)
                self.cmnTxtFld_A1.setText(result)
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
                self.currentTxt_B1 = self.exceptCheck_B1(self.currentTxt_B1)  # 更に調べます。。。
                # print(self.currentTxt_B1)
                # print('C')
                # @ 識別子 の複数入力を検知し、強制的に独自規定で1つに制限するメソッド 実行
                result = self.limitAtSignIdMultipleInputToOneCmd(self.currentTxt_B1, 2)
                self.cmnTxtFld_B1.setText(result)

    # textField へのタイピング入力 用 制限
    # txtFld A1 内で、規定許可文字 @,~ 識別子 以外の入力を検知し、強制的に独自規定で置き換えるメソッド
    def exceptCheck_A1(self, current_text):
        u""" < textField へのタイピング入力 用 制限 >

        ::

          txtFld A1 内で、規定許可文字 @,~ 識別子 以外の入力を検知し、強制的に独自規定で置き換えるメソッド

        #######################

        #.
            :param str current_text:

        #.
            :return: self.currentTxt_A1
            :rtype: str

        #######################
        """
        # print('C')
        # print(current_text)
        patternA = re.compile(r'[ !"#$%&\'()*+,-./:;<=>?^_`{|}\[\]]+(.)')
        # パターンA定義:規定した文字以外が一つ以上あるか
        search = patternA.search(current_text)  # 調べる関数
        if search:  # あるならば
            iterator = patternA.finditer(current_text)
            # マッチする部分をイテレータで返す関数
            for itr in iterator:
                # print(itr.group(0), itr.group(1))
                # itr.group(0):一致の全体, itr.group(1):一致の一部
                # 自分自身currentTxtに代入（上書き）
                current_text = current_text.replace(itr.group(0), itr.group(1).upper())
                message_warning(self.warningMessage_default)
            self.cmnTxtFld_A1.setText(current_text)
            self.cmnTxtFld_A1.setFont(self.tempFont)
            self.cmnTxtFld_A1.setInsertionPosition(0)
        self.currentTxt_A1 = current_text
        return self.currentTxt_A1

    # textField へのタイピング入力 用 制限
    # txtFld B1 内で、規定許可文字 [],@,~ 識別子 以外の入力を検知し、強制的に独自規定で置き換えるメソッド
    def exceptCheck_B1(self, current_text):
        u""" < textField へのタイピング入力 用 制限 >

        ::

          txtFld B1 内で、規定許可文字 [],@,~ 識別子 以外の入力を検知し、強制的に独自規定で置き換えるメソッド

        #######################

        #.
            :param str current_text:

        #.
            :return: self.currentTxt_B1
            :rtype: str

        #######################
        """
        # print('B')
        # print(current_text)
        patternB = re.compile(r'[ !"#$%&\'()*+,-./:;<=>?^_`{|}@]+(.)')
        # パターンB定義:規定した文字以外が一つ以上あるか
        search = patternB.search(current_text)  # 調べる関数
        if search:  # あるならば
            iterator = patternB.finditer(current_text)
            # マッチする部分をイテレータで返す関数
            for itr in iterator:
                # print(itr.group(0), itr.group(1))
                # itr.group(0):一致の全体, itr.group(1):一致の一部
                # 自分自身currentTxtに代入（上書き)
                current_text = current_text.replace(itr.group(0), itr.group(1).upper())
            message_warning(self.warningMessage_default)
            self.cmnTxtFld_B1.setText(current_text)
            self.cmnTxtFld_B1.setFont(self.tempFont)
            self.cmnTxtFld_B1.setInsertionPosition(0)
        self.currentTxt_B1 = current_text
        return self.currentTxt_B1

    # pop up menu入力, textFieldタイピング入力 共通な 入力 制限
    # @ 識別子 の複数入力を検知し、強制的に独自規定で1つに制限するメソッド
    def limitAtSignIdMultipleInputToOneCmd(self, current_text, tFldID):
        u""" < pop up menu入力, textFieldタイピング入力 共通な 入力 制限 >

        ::

          @ 識別子 の複数入力を検知し、強制的に独自規定で1つに制限するメソッド

        #######################

        #.
            :param str current_text:
            :param int tFldID: textField ID は、第1単語 or 第2単語 どちらかです
                1 or 2

        #.
            :return: current_text
            :rtype: str

        #######################
        """
        countAtMark = current_text.count(u'@')  # @ の数を調べる
        if countAtMark > 1:  # @ の数が1を超えたら超えないように修正をかける
            message_text = u'第{}単語:@記述を複数挿入しようとしています。' \
                           u'@を1つで強制記述修正します。'.format(tFldID)
            message_warning(message_text)
            result = current_text[:-1]
            # self.cmnTxtFld_A1.setText(result)  # 修正
            current_text = result
        return current_text

    # 第3単語-要素1フィールド、要素2フィールド、要素3フィールド誤入力判別 関数
    # 追加
    def wrong_input_determining_fromCmd(self, wordLists):
        u""" < 3単語-要素1フィールド、要素2フィールド、要素3フィールド誤入力判別 関数 です >

        ::

          追加

        #######################

        #.
            :param list[str] wordLists:

        #.
            :return: isWrong
                True: 誤入力発見, False: 誤入力なし
                何れか
            :rtype isWrong: bool

        #######################
        """
        # print(wordLists[2:])
        tFldC1, tFldC2, tFldC3 = wordLists[2], wordLists[3], wordLists[4]
        # print(tFldC1, tFldC2, tFldC3)
        isWrong = True  # default: True: 誤入力発見
        # ####################
        # atMark 無しでのサポート
        if tFldC1 == '' and tFldC2 == '' and (tFldC3 == 'L' or tFldC3 == 'R'
                                              or tFldC3 == 'C' or tFldC3 == 'M'):  # ex.: ***_jt_L
            isWrong = False  # False: 誤入力なし
        elif tFldC1 == '' and tFldC2 == 'Gp' and (tFldC3 == 'L' or tFldC3 == 'R'
                                                or tFldC3 == 'C' or tFldC3 == 'M'
                                                  or tFldC3 == ''):  # ex.: ***_jt_GpL, ***_jt_Gp
            isWrong = False  # False: 誤入力なし
        elif tFldC1 == '' and tFldC2 == '' and tFldC3 == '':  # ex.: ***_jt
            isWrong = False  # False: 誤入力なし
        # ####################
        # atMark 有りでのサポート
        elif tFldC1 == '@' and tFldC2 == 'Gp' and tFldC3 == '':  # ex.: ***_jt_@Gp
            isWrong = False  # False: 誤入力なし
        elif tFldC1 == '@' and tFldC2 == '' and (tFldC3 == 'L' or tFldC3 == 'R'
                                                 or tFldC3 == 'C' or tFldC3 == 'M'):  # ex.: ***_jt_@L
            isWrong = False  # False: 誤入力なし
        elif tFldC1 == '@' and tFldC2 == 'Gp' and (tFldC3 == 'L' or tFldC3 == 'R'
                                                   or tFldC3 == 'C' or tFldC3 == 'M'):  # ex.: ***_jt_@GpL
            isWrong = False  # False: 誤入力なし
        else:
            isWrong = True  # True: 誤入力発見

            # 変換箇所5
            # YO_logProcess.action('WARNING'
            #                      , u'{}\n\t\t\tLine Number:{}\n'
            #                        u'ストップ\n'
            #                        u'第3単語-要素1フィールド、要素2フィールド、要素3フィールド の何れかで、'
            #                        u'独自規格の命名規則に反した誤入力の可能性があります。'
            #                        u'独自規格の命名規則についての詳細は、help をご覧ください。'
            #                        u'rename の実行はストップしました。0-wrong_input'
            #                      .format(self.title, YO_logger2.getLineNo())
            #                      )

            # message_warning(u'第3単語-要素1フィールド、要素2フィールド、要素3フィールド の何れかで、'
            #                      u'独自規格の命名規則に反した誤入力の可能性があります。'
            #                      u'独自規格の命名規則についての詳細は、help をご覧ください。'
            #                      u'rename の実行はストップしました。0-wrong_input'
            #                      )

            pass
        #     message_warning(u'第3単語-要素2フィールド、要素3フィールドどちらかに、@ (at mark) '
        #                          u'が誤って入力されています。'
        #                          u'要素2フィールドでは、文字列 Gp 識別子（グループの意）、'
        #                          u'要素3フィールドでは、サイド用識別子、'
        #                          u'である必要があります。'
        #                          u'rename の実行はストップしました。0-A')
        #     message_warning(u'第3単語-要素2フィールドに、@ (at mark) '
        #                          u'が誤って入力されています。'
        #                          u'文字列 Gp 識別子（グループの意）、'
        #                          u'である必要があります。'
        #                          u'rename の実行はストップしました。0-B')
        #     message_warning(u'第3単語-要素3フィールドに、@ (at mark) '
        #                          u'が誤って入力されています。'
        #                          u'サイド用識別子、'
        #                          u'である必要があります。'
        #                          u'rename の実行はストップしました。0-C')
        #     message_warning(u'第3単語-要素1フィールドに、単独の @ (at mark) '
        #                          u'を判別しました。'
        #                          u'利用したい場合には、'
        #                          u'第3単語-要素2フィールドもしくは要素3フィールド'
        #                          u'に、'
        #                          u'必要な識別子を同時に準備する必要があります。'
        #                          u'@ (at mark) を必要とする場合は、'
        #                          u'可能な限り、第1単語フィールドもしくは 第2単語フィールド'
        #                          u'での、一つの使用で留めてください。'
        #                          u'rename の実行はストップしました。0-')
        #     pass
        return isWrong
    # 2. UI-2. 追加オプション コマンド群 ################################################## end

    # その他 アルゴリズムとなる コマンド群 ################################################ start
    # 選択された全ノードに対して、一つずつ、unique な名前かどうかを調べ、
    # True, False のリストを返す メソッド
    #   e.g.) [True, False, ...]
    # 選択された全ノードリストの長さ、と、True・False のリストの長さは、常に同じ！！
    def is_uniqueName(self, selects):
        u""" <>

        ::

          選択された全ノードに対して、一つずつ、unique な名前かどうかを調べ、
          True, False のリストを返す メソッド
              e.g.) [True, False, ...]
          選択された全ノードリストの長さ、と、True・False のリストの長さは、常に同じ！！

        #######################

        #.
            :param list[str] selects:

        #.
            :return: is_uniqueName_lists
            :rtype: list[bool]

            e.g.): [True, False, ...]

        #######################
        """
        is_uniqueName_lists = []
        for selIndex in selects:
            # print(selIndex)
            # 最後から一番目の '|' を境にした 1回 分割メソッド の実行
            selIndex_split = selIndex.rsplit('|', 1)
            # $(selIndex_split)
            # 必ず、[u'***', u'***'] に分割される
            # unique だと、必ずselIndex_split[0]は u'' で空になる所に着目
            # print(len(selIndex_split))
            if len(selIndex_split) == 1:  # unique だと、len(selIndex_split) は必ず 1
                is_uniqueName_lists.append(True)
            else:  # unique でなければ、len(selIndex_split) は必ず 2
                is_uniqueName_lists.append(False)
        return is_uniqueName_lists

    # 個別ノードの持つ単独UUID番号、に対する独自操作 コマンド群 ################### start
    # 追加
    # エラー修正1に伴う追加1
    # 単独選択ノードから単独UUID番号をゲットする関数
    # from ..lib.YO_uuID import UUID へ移動...

    # 追加
    # エラー修正1に伴う追加1
    # 単独UUID番号から単独ノードを選択する関数
    # from ..lib.YO_uuID import UUID へ移動...

    # 追加
    # 選択ノードの明示の為に準備する格納用
    # 独自の 選択ノードの明示に使用
    # 格納用
    # from ..lib.YO_uuID import UUID へ移動...

    # 追加
    # 選択ノードの明示の為の再選択用
    # 独自の 選択ノードの明示に使用
    # 再選択用
    # from ..lib.YO_uuID import UUID へ移動...
    # 個別ノードの持つ単独UUID番号、に対する独自操作 コマンド群 ##################### end

    # エラー修正1
    # 選択された全ノード名に対して、unique name かどうかを判断し、
    # unique name でない場合は、unique name になるように、
    # 仮に rename を施し、初期選択ノードを更新する メソッド。
    # 初期選択ノードの変化に対応させるのが目的です。
    # @instance.declogger
    def checkAndDoUniqueName_forSlNode(self, lists):
        u""" < unique name かどうかを判断し、unique name にする メソッド >

        ::

          エラー修正1
          選択された全ノード名に対して、unique name かどうかを判断し、
            unique name でない場合は、unique name になるように、
                仮に rename を施し、初期選択ノードを更新する メソッド。

          初期選択ノードの変化に対応させるのが目的です。

        #######################

        #.
            :param list[str] lists:

        #.
            :return: selectionLists
            :rtype: list[str]

        #######################
        """
        selectionLists = lists
        count = len(selectionLists)

        # selection node name, check unique
        # 全選択ノードに対して、一つずつ、unique な名前かどうかを調べ、
        # True, False のリストを返す メソッド の 実行
        # e.g.) [True, False, ...]
        is_uniqueName_selections = self.is_uniqueName(selectionLists)

        uuidSelectionLists = []
        for index in selectionLists:
            uuidSelectionLists.append(yo_uuid.get_ID_fromSel(index))  # 選択ノードからIDを取得する
        cmds.select(cl = True)

        # 追加7 ####################################################### start
        self.scriptEditor2.append_default('\n' + 'checkAndDoUniqueName' + '-------' * 10 + 'start')
        self.scriptEditor2.append_default('checkAndDoUniqueName start..')
        self.scriptEditor2.append_default('\t selectionLists: {}'.format(selectionLists))
        # 追加7 ####################################################### end

        # print('\n' + 'checkAndDoUniqueName' + '-------' * 10 + 'start')
        # print('checkAndDoUniqueName start..')
        # print('\t selectionLists: {}'.format(selectionLists))

        # print('\t count: {}'.format(count))
        # print('\t is_uniqueName_selections: {}'.format(is_uniqueName_selections))
        # print('\t uuidSelectionLists: {}'.format(uuidSelectionLists))

        newLists = []

        for indexNum, (isUn_selIndex, uuidIndex) in enumerate(
                zip(is_uniqueName_selections, uuidSelectionLists)
                ):
            # 追加7 ####################################################### start
            self.scriptEditor2.append_default('\n' + '*********' * 10)
            self.scriptEditor2.append_default(u'{}番目: {} は、'.format(indexNum + 1, selectionLists[indexNum]))
            # 追加7 ####################################################### end

            # print('\n' + '*********' * 10)
            # print(u'{}番目: {} は、'.format(indexNum + 1, selectionLists[indexNum]))

            # print(isUn_selIndex, uuidIndex)
            # isUn_selIndex: True or False をトリガーとする
            # checkAndDoUniqueName proc

            if isUn_selIndex:  # True ならば。。そのまま  # checkAndDoUniqueName procA
                # 追加7 ####################################################### start
                self.scriptEditor2.append_default(u'######## unique です。 #####################')
                self.scriptEditor2.append_default(u'######## 変更は行いません。..終わり')
                self.scriptEditor2.append_default('******** checkAndDoUniqueName done '
                      '*********************rename checkAndDoUniqueName procA'
                      )
                self.scriptEditor2.append_default('*********' * 10)
                # 追加7 ####################################################### end

                # print(u'######## unique です。 #####################')
                # print(u'######## 変更は行いません。..終わり')
                # print('******** checkAndDoUniqueName done '
                #       '*********************rename checkAndDoUniqueName procA'
                #       )
                # print('*********' * 10)
                pass
            else:  # checkAndDoUniqueName procB
                # 追加7 ####################################################### start
                self.scriptEditor2.append_default(u'######## unique ではありません。 #############')
                # 追加7 ####################################################### end

                # print(u'######## unique ではありません。 #############')

                longName_selIndex = cmds.ls(uuidIndex, long = True)[0]  # uuidIndex: unique
                # print('longName_selIndex: {}'.format(longName_selIndex))

                # 最後から一番目の '|' を境にした 1回 分割メソッド の実行し、
                # 必ず2つ分割されるリストが作成され、その中のindex1を抽出
                objName_selIndex = longName_selIndex.rsplit('|', 1)[1]
                # print('objName_selIndex: {}'.format(objName_selIndex))

                # 追加7 ####################################################### start
                self.scriptEditor2.append_default(u'######## {} ########'.format(objName_selIndex))
                # 追加7 ####################################################### end

                # print(u'######## {} ########'.format(objName_selIndex))

                newName = objName_selIndex + '#'
                # print(newName)
                yo_uuid.select_fromID(uuidIndex)  # IDを利用してノードを選択する
                # 単独
                sel = commonCheckSelection()[0]
                # print(sel)
                cmds.rename(sel, newName)  # current index, renamed and update

                # if indexNum + 1 < count:
                #     nextID = uuidSelectionLists[indexNum + 1]
                #     select_fromID(nextID)  # IDを利用してノードを選択する
                #     nextSel = commonCheckSelection()[0]
                #     print(nextSel)  # get next newName
                #     # cmds.rename(selNext, nextSel)  # next index, renamed and update
                # elif indexNum + 1 == count:
                #     pass

                # 変換箇所5
                # YO_logProcess.action('WARNING'
                #                      , u'{}\n\t\t\tLine Number:{}\n'
                #                        u'######## 重複名を検知...\n'
                #                        u'######## 一時的にナンバーリング rename を実施。\n'
                #                        u'######## 選択されていたノードを、強制的に unique にし、続行..\n'
                #                      .format(self.title, YO_logger2.getLineNo())
                #                      )

                # 追加7 ####################################################### start
                self.scriptEditor2.append_default(u'######## 強制的に unique にしました。..終わり')
                self.scriptEditor2.append_default('******** checkAndDoUniqueName done '
                      '*********************rename checkAndDoUniqueName procB'
                      )
                self.scriptEditor2.append_default('*********' * 10)
                # 追加7 ####################################################### end

                # print(u'######## 強制的に unique にしました。..終わり')
                # print('******** checkAndDoUniqueName done '
                #       '*********************rename checkAndDoUniqueName procB'
                #       )
                # print('*********' * 10)

                # print(u'######## 重複名を検知...\n'
                #       u'######## 一時的にナンバーリング rename を実施。\n'
                #       u'######## 選択されていたノードを、強制的に unique にし、続行..\n'
                #       )

        # for isUn_selIndex, selIndex in zip(is_uniqueName_selections, selectionLists):
        #     # print(isUn_selIndex, selIndex)
        #     if isUn_selIndex:  # True ならば。。そのまま
        #         # print(u'######## 選択されている以下は、unique です。 #####################')
        #         # print(selIndex)
        #         # print(u'######## 変更は行いません。..終わり\n')
        #         newLists.append(selIndex)
        #     elif not isUn_selIndex:  # False ならば。。unique にする
        #         # print(u'######## 選択されている以下は、unique ではありません。 #############')
        #         longName_selIndex = cmds.ls(selIndex, long = True)[0]
        #         # print(longName_selIndex)
        #         cmds.select(selIndex, r = True)  # 選んだノードに対して..
        #         # 最後から一番目の '|' を境にした 1回 分割メソッド の実行し、
        #         # 必ず2つ分割されるリストが作成され、その中のindex1を抽出
        #         objName_selIndex = longName_selIndex.rsplit('|', 1)[1]
        #         # print(objName_selIndex)
        #         # counts_obj = self.getObj.count(objName_selIndex)
        #         # print(counts_obj)
        #         # objName_selIndex(選択しているノードのobject名)に対しての真偽
        #         # (選択したノードの)object名が、重複名として既にシーン内にあるかどうかの
        #         # 真偽出力メソッド 実行
        #         # (選択したノードの)object名 : objName_selIndex
        #         # 対象のリスト(シーン内 DG name 全リスト) : self.getObj lists
        #         # self.is_exists_forSlNode = self.searchForDuplicateName(self.getObj, objName_selIndex)
        #         # print('***')
        #         # print(self.is_exists_forSlNode)
        #         newName = objName_selIndex + '#'
        #         # 一時的に maya default ナンバーリング rename を施し、重複を無くす
        #         cmds.rename(selIndex, newName)
        #         new = cmds.ls(sl = True)[0]
        #         # print(new)
        #         newLists.append(new)
        #         # print('{} --> {}'.format(objName_selIndex, new))
        #         print(u'######## {} ########'.format(objName_selIndex))
        #         YO_logProcess.action('INFO'
        #                              , u'{}\n\t\t\tLine Number:{}\n'
        #                                u'######## 重複名を検知...\n'
        #                                u'######## 一時的にナンバーリング rename を実施。\n'
        #                                u'######## 選択されていたノードを、強制的に unique にし、続行..\n'
        #                              .format(self.title, YO_logger2.getLineNo())
        #                              )
        #         # print(u'######## 重複名を検知...\n'
        #         #       u'######## 一時的にナンバーリング rename を実施。\n'
        #         #       u'######## 選択されていたノードを、強制的に unique にし、続行..\n'
        #         #       )
        # print('newLists: {}'.format(newLists))
        # cmds.select(cl = True)
        # selectionLists = newLists
        # # print(selectionLists)
        # cmds.select(selectionLists, r = True)  # selectionLists の更新 完了
        for uuidIndex in uuidSelectionLists:
            yo_uuid.select_fromID(uuidIndex)  # IDを利用してノードを選択する
            sel = commonCheckSelection()[0]
            newLists.append(sel)
        selectionLists = newLists

        # 追加7 ####################################################### start
        self.scriptEditor2.append_default('..checkAndDoUniqueName done')
        self.scriptEditor2.append_default('\t selectionLists: {}'.format(selectionLists))
        self.scriptEditor2.append_default('checkAndDoUniqueName' + '-------' * 10 + 'end' + '\n')
        # 追加7 ####################################################### end

        # print('..checkAndDoUniqueName done')
        # print('\t selectionLists: {}'.format(selectionLists))
        # print('checkAndDoUniqueName' + '-------' * 10 + 'end' + '\n')

        return selectionLists

    # 選択された全ノード名に対して、余分なアンダースコアーがあるかどうかを調べ、
    # あったら、除外し終えた文字列を、なければそのままの文字列になるように、
    # rename を施し、初期選択ノードを更新する メソッド。
    # 初期選択ノードの変化に対応させるのが目的です。
    # 様々なケースへの対応を想定した場合、精度があがりそう!!
    def checkAndDoLimitationOfUnderScore_forSlNode(self, lists):
        u""" <>

        ::

          選択された全ノード名に対して、余分なアンダースコアーがあるか
          あったら、除外し終えた文字列を、なければそのままの文字列にな
          rename を施し、初期選択ノードを更新する メソッド。

          初期選択ノードの変化に対応させるのが目的です。
          様々なケースへの対応を想定した場合、精度があがりそう!!

        #######################

        #.
            :param list[str] lists:

        #.
            :return: selectionLists
            :rtype: list[str]

        #######################
        """
        selectionLists = lists
        newLists = []
        ####################################
        # 既存のノードネームに対して
        # 余分なアンダースコアーの除去 第1弾
        ####################################
        # (mode1 -filter 1) underScore_check 11, 12 method それぞれの実行
        for selIndex in selectionLists:
            # print(selIndex)
            # (mode1 -filter 1 -1) underScore_check11() メソッド 実行
            newIndex_check1 = self.underScore_check11(selIndex)
            # print(newIndex_check1)
            if newIndex_check1 != selIndex:
                cmds.rename(selIndex, newIndex_check1)
                # (mode1 -filter 1 -2) underScore_check12() メソッド 実行
                newIndex_check2 = self.underScore_check12(newIndex_check1)
                # print(newIndex_check2)
                if newIndex_check2 != newIndex_check1:
                    cmds.rename(newIndex_check1, newIndex_check2)
                    newLists.append(newIndex_check2)
                else:
                    newLists.append(newIndex_check1)
            elif newIndex_check1 == selIndex:
                # (mode1 -filter 1 -2) underScore_check12() メソッド 実行
                newIndex_check2 = self.underScore_check12(selIndex)
                # print(newIndex_check2)
                if newIndex_check2 != selIndex:
                    cmds.rename(selIndex, newIndex_check2)
                    newLists.append(newIndex_check2)
                else:
                    newLists.append(selIndex)
        # print(newLists)
        # print('***')
        cmds.select(newLists, r = True)  # 一時的に、newLists として作成
        # print('****')
        selectionLists = commonCheckSelection()
        # (mode1 -filter 1) の実行後のため、初期の選択リストは、既に存在しなくなるので、
        # newLists を selectionLists として、更新し登録しなおしておく。
        cmds.select(cl = True)
        # print('**')
        # newLists は 更新 override され、中身が残ったままなので、
        # 次の override の準備に再利用するため、リストを(元の)空にしておく。
        # if len(newLists) > 0:
        #     del newLists[:]
        # self.newLists.__init__()  # newLists のみ、再初期化
        newLists = []
        # print('koko000')
        # print(newLists)
        cmds.select(selectionLists, r = True)
        # print('koko001')
        # print(selectionLists)

        ####################################
        # 既存のノードネームに対して
        # 余分なアンダースコアーの除去 第2弾
        ####################################
        # (mode1 -filter 2) underScore_check 21, 22 method
        for selIndex in selectionLists:
            # print(selIndex)
            # (mode1 -filter 2 -1) underScore_check21() method 実行
            check21 = self.underScore_check21(selIndex)  # '_', 文字列, のそれぞれのリスト作成
            underScoreLists = check21[0]  # '_'全リスト
            strsOnlyLists = check21[1]  # 連続文字列のリスト3つまで
            # print(underScoreLists, strsOnlyLists)
            # (mode1 -filter 2 -2) underScore_check22() method 実行
            check22 = self.underScore_check22(selIndex)  # 最後の文字列のみの抽出
            lastStrs = check22
            # print(lastStrs)
            # print(u'文字列中にあるアンダースコアー全リスト\n'
            #       + '\t is {}'.format(underScoreLists)
            #       )
            # print(u'連続文字列のリストを初めから3つまで\n'
            #       + '\t is {}'.format(strsOnlyLists)
            #       )
            # print(u'最後の文字列のみ\n'
            #       + '\t is {}'.format(lastStrs)
            #       )
            if len(underScoreLists) == 3:  # '_'`が3つあった場合、新規にrename
                newStrings = '{}_{}_{}{}'.format(strsOnlyLists[0]
                                                 , strsOnlyLists[1]
                                                 , strsOnlyLists[2]
                                                 , lastStrs
                                                 )
                # print(newStrings)  # 新規にrename
                cmds.rename(selIndex, newStrings)
                newLists.append(newStrings)
            else:
                newLists.append(selIndex)
        # print('koko002')
        # print(newLists)
        # print('***')
        cmds.select(newLists, r = True)  # 一時的に、newLists として作成
        # print('****')
        selectionLists = commonCheckSelection()
        # (mode1 -filter 2) の実行後のため、初期の選択リストは、既に存在しなくなるので、
        # self.newLists を self.selectionLists として、更新し登録しなおしておく。
        return selectionLists

    # 選択されたノードネームに対して
    # 余分なアンダースコアーの除去 第1弾(mode1 -filter 1 -1)
    # 最後に'_'があるかどうか調べる(複数_にも対応)。
    # あったら、除外し終えた文字列を、
    # なければそのままの文字列を、出力する メソッド。
    def underScore_check11(self, textStr, *args):
        u""" <>

        ::

          選択されたノードネームに対して
          余分なアンダースコアーの除去 第1弾(mode1 -filter 1 -1)
          最後に'_'があるかどうか調べる(複数_にも対応)。

          あったら、除外し終えた文字列を、
          なければそのままの文字列を、出力する メソッド。

        #######################

        #.
            :param str textStr:

        #.
            :return: textStr
            :rtype: str

        #######################
        """
        # print(textStr, args)
        patternA = re.compile(r'(?P<ptn1>.*?)(?P<ptn2>_+$)')
        matchObjA = patternA.finditer(textStr)
        for itA in matchObjA:
            ptnA_dict = itA.groupdict()
            # print(ptn_dictA['ptn1'])  # or itA.group('ptn1')
            text_removeLastStr = ptnA_dict['ptn1']
            count = len(itA.groups())
            if count == 2:
                textStr = text_removeLastStr
        return textStr

    # 選択されたノードネームに対して
    # 余分なアンダースコアーの除去 第1弾(mode1 -filter 1 -2)
    # 連続'_'が文字列中にあるかどうか調べる。
    # あったら、'_'1つの記述に変換し終えた文字列を、
    # なければそのままの文字列を、出力する メソッド。
    def underScore_check12(self, textStr, *args):
        u""" <>

        ::

          選択されたノードネームに対して
          余分なアンダースコアーの除去 第1弾(mode1 -filter 1 -2)
          連続'_'が文字列中にあるかどうか調べる。

          あったら、'_'1つの記述に変換し終えた文字列を、
          なければそのままの文字列を、出力する メソッド。

        #######################

        #.
            :param str textStr:

        #.
            :return: textStr
            :rtype: str

        #######################
        """
        patternC1 = re.compile(r'(?P<ptn1>_{2,10})')
        matchObjC1 = patternC1.finditer(textStr)
        for itC1 in matchObjC1:
            ptnC1_dict = itC1.groupdict()
            count = len(itC1.groups())
            if count is not None:  # 修正前は、if not count == None...でした
                matchObjC2 = patternC1.sub('_', textStr)  # 実際に置換する操作
                textStr = matchObjC2
        return textStr

    # 選択されたノードネームに対して
    # 余分なアンダースコアーの除去 第2弾(mode1 -filter 2 -1)
    # '_'が文字列中に3つ以上あるかどうか調べる為の準備1
    # '_', 文字列, のそれぞれのリスト作成
    # 文字列中にあるアンダースコアーの全リストと、
    # そのアンダースコアーの前後にある、連続文字列のリストを初めから3つまでを、出力する メソッド。
    def underScore_check21(self, textStr, *args):
        u""" <>

        ::

          選択されたノードネームに対して
          余分なアンダースコアーの除去 第2弾(mode1 -filter 2 -1)
          '_'が文字列中に3つ以上あるかどうか調べる為の準備1

          '_', 文字列, のそれぞれのリスト作成

          文字列中にあるアンダースコアーの全リストと、そのアンダースコアーの前後にある、
          連続文字列のリストを初めから3つまでを、出力する メソッド。

        #######################

        #.
            :param str textStr:

        #.
            :return: textStr
            :rtype: str

        #######################
        """
        patternB = re.compile(r'(?P<ptn1>.*?)(?P<ptn2>_)')
        matchObjB = patternB.finditer(textStr)
        underScoreLists = []
        strsOnlyLists = []
        for itB in matchObjB:
            # print(itB.groups())
            ptn_dictB = itB.groupdict()
            # print(ptn_dictB)
            ptn_tupleB = sorted(ptn_dictB.items())
            # print(ptn_tupleB)
            strsCompLists = []
            for ptnB in ptn_tupleB:
                # print(ptnB)
                strsCompLists.append(ptnB[1])
            # print(strsCompLists)
            strsCompLists.pop(0)
            underScoreLists.append(strsCompLists[0])

            ptn_tupleB = sorted(ptn_dictB.items())
            strsCompLists = []
            for ptnB in ptn_tupleB:
                # print(ptnB)
                strsCompLists.append(ptnB[1])
            # print(strsCompLists)
            strsCompLists.pop(1)
            # print(strsCompLists)
            strsOnlyLists.append(strsCompLists[0])
        # if len(underScoreLists) == 0:
        #     underScoreLists = None
        if len(strsOnlyLists) == 0:
            strsOnlyLists = textStr
        return underScoreLists, strsOnlyLists

    # 選択されたノードネームに対して
    # 余分なアンダースコアーの除去 第2弾(mode1 -filter 2 -2)
    # '_'が文字列中に3つ以上あるかどうか調べる為の準備2
    # 最後の文字列のみの抽出
    # 文字列の内、最後のアンダースコアーの後に来る連続文字列のみを、出力する メソッド。
    def underScore_check22(self, textStr, *args):
        u""" <>

        ::

          選択されたノードネームに対して
          余分なアンダースコアーの除去 第2弾(mode1 -filter 2 -2)
          '_'が文字列中に3つ以上あるかどうか調べる為の準備2

          最後の文字列のみの抽出
          文字列の内、最後のアンダースコアーの後に来る連続文字列のみを、出力する メソッド。

        #######################

        #.
            :param str textStr:

        #.
            :return: lastStrs
            :rtype: str

        #######################
        """
        patternD = re.compile(r'(?P<ptn1>.*)_(?P<ptn2>.*?$)')  # 最後の'_'の後ろにくる文字列抽出
        matchObjD = patternD.finditer(textStr)
        for itD in matchObjD:
            # print(itD.groups())
            ptn_dictD = itD.groupdict()
            # print(ptn_dictD)
            ptn_tupleD = sorted(ptn_dictD.items())
            # print(ptn_tupleD)
            strsSepLists = []  # このリストは必ず2つにセパレートされる
            for ptnD in ptn_tupleD:
                # print(ptnD)
                strsSepLists.append(ptnD[1])
            # print(strsSepLists)
            lastStrs = strsSepLists[1]
            # print(lastStrs)
            return lastStrs

    # 待機している単語文字列 A, B, C1, C2, C3 から,想定する規定パターンを抽出し,
    # 分解して出力するメソッド。
    def waitingWordStrs_patternCheck_exe(self, wordLists):
        u""" < 待機している単語文字列 A, B, C1, C2, C3 から,想定する規定パターンを抽出し,分解して出力するメソッド >

        #######################

        #.
            :return: self.strsDecompListsAll
            :rtype: list

            e.g.): [[], [], [], [], []]

        #######################
        """
        patternE = re.compile(
            r'(?P<pattern1a>~)(?P<pattern1b>\[)(?P<pattern1c>.*?)(?P<pattern1d>])(?P<pattern1e>[a-zA-Z].*)'
            r'|'
            r'(?P<pattern11a>~)(?P<pattern11b>\[)(?P<pattern11c>.*?)(?P<pattern11d>])'
            r'|'
            r'(?P<pattern12a>~)(?P<pattern12b>@)(?P<pattern12c>[a-zA-Z].*)'
            r'|'
            r'(?P<pattern2a>~)(?P<pattern2b>@)'
            r'|'
            r'(?P<pattern3a>~)(?P<pattern3b>[a-zA-Z].*)'
            r'|'
            r'(?P<pattern10>~)'
            r'|'
            r'(?P<pattern4>@)'
            r'|'
            r'(?P<pattern5a>[a-zA-Z]+)(?P<pattern5b>@)'
            r'|'
            r'(?P<pattern6a>[a-zA-Z]+)(?P<pattern6b>\[)(?P<pattern6c>.*?)(?P<pattern6d>])(?P<pattern6e>[a-zA-Z].*)'
            r'|'
            r'(?P<pattern16a>[a-zA-Z]+)(?P<pattern16b>\[)(?P<pattern16c>.*?)(?P<pattern16d>])'
            r'|'
            r'(?P<pattern8>[a-zA-Z].*)'
            r'|'
            )
        # それぞれの要素の, 分解リスト格納場所 の中身を常に空にしてから以下実行
        self.strsDecompListsAll.__init__()

        for e, index in enumerate(wordLists):
            # print(u'待機個別文字列')
            # print(u'No.{} textField word'.format(e + 1), index)
            iterator = patternE.finditer(index)  # patternE で調べる 関数の実行
            if (e + 1) == 1:
                tFld_name = []  # 'tFld_A'
                # print(tFld_name)
                # patternE にマッチしたものだけを整理し出力するメソッド 実行
                strsCompLists = self.ptnMatch_strsComp_output(iterator)
                for sCL_index in strsCompLists:
                    tFld_name.append(sCL_index)
                self.strsDecompListsAll.append(tFld_name)
            elif (e + 1) == 2:
                tFld_name = []  # 'tFld_B'
                # print(tFld_name)
                # patternE にマッチしたものだけを整理し出力するメソッド 実行
                strsCompLists = self.ptnMatch_strsComp_output(iterator)
                for sCL_index in strsCompLists:
                    tFld_name.append(sCL_index)
                self.strsDecompListsAll.append(tFld_name)
            elif (e + 1) == 3:
                tFld_name = []  # 'tFld_C1'
                # print(tFld_name)
                # patternE にマッチしたものだけを整理し出力するメソッド 実行
                strsCompLists = self.ptnMatch_strsComp_output(iterator)
                for sCL_index in strsCompLists:
                    tFld_name.append(sCL_index)
                self.strsDecompListsAll.append(tFld_name)
            elif (e + 1) == 4:
                tFld_name = []  # 'tFld_C2'
                # print(tFld_name)
                # patternE にマッチしたものだけを整理し出力するメソッド 実行
                strsCompLists = self.ptnMatch_strsComp_output(iterator)
                for sCL_index in strsCompLists:
                    tFld_name.append(sCL_index)
                self.strsDecompListsAll.append(tFld_name)
            elif (e + 1) == 5:
                tFld_name = []  # 'tFld_C3'
                # print(tFld_name)
                # patternE にマッチしたものだけを整理し出力するメソッド 実行
                strsCompLists = self.ptnMatch_strsComp_output(iterator)
                for sCL_index in strsCompLists:
                    tFld_name.append(sCL_index)
                self.strsDecompListsAll.append(tFld_name)
        return self.strsDecompListsAll

    # patternE にマッチしたものだけを整理し、出力するメソッド。
    # waitingWordStrs_patternCheck_exe メソッド に依存
    def ptnMatch_strsComp_output(self, iterator, *args):
        u""" < patternE にマッチしたものだけを整理し、出力するメソッド >

        ::

          waitingWordStrs_patternCheck_exe メソッド に依存

        #######################

        #.
            :param iterator:
            :type iterator:

        #.
            :return: strsCompLists
            :rtype: list

        #######################
        """
        for itr in iterator:
            # print('#### find a patternE match!! ####')
            # print('#### those pattern strings is .. u\'{}\' .'.format(index))
            # print(itr.groups())
            # print(itr.groupdict())  #パターンヒットを辞書として出力出来る
            ptn_dict = itr.groupdict()
            ptnFindStrs_isNone = None
            for ptnNumber_keys, ptnFindStrs_values in list(ptn_dict.items()):  # 変換箇所1: ptn_dict.items() からの変換
                # print(ptnNumber_keys, ptnFindStrs_values)
                if ptnFindStrs_values == ptnFindStrs_isNone:
                    # value が None の keys のみを辞書から削除
                    # print(ptnNumber_keys)
                    ptn_dict.pop(ptnNumber_keys)
            # print(ptn_dict)
            # 余計なものを省いた最終辞書を, ちゃんと綺麗にソートしたいが,
            # 辞書はソートできないので keys でソートする。するとタプルになってしまう。
            ptn_tuple = sorted(ptn_dict.items())
            # print(ptn_tuple)
            strsCompLists = []
            for ptn in ptn_tuple:
                # タプルの各要素の内,欲しいのは index[1] なので,
                # 新規リストへ index[1] のみを順次格納する。
                # print(ptn[1])
                strsCompLists.append(ptn[1])
            # print(strsCompLists)
            return strsCompLists

    # decimalNumber to 26 decimalNumber 10進数から26進数への変換し、出力する メソッド
    def deciNum_to_26deciNum(self, n):
        u""" < 10進数から26進数への変換し、出力する メソッド >

        #######################

        #.
            :param int n:

        #.
            :return: chars
            :rtype: str

        #######################
        """
        shou1, amari1 = divmod(n, 26)
        chars = ''
        # print(n)
        # print(u'start----')
        # print(u'{}を26で割り算 1回目:商(shou1)-> {}, 余り(amari1)-> {}'
        # .format(n, shou1, amari1)
        # )
        # print(u'a1. 1桁目は 余り(amari1) を利用\n\t{}'
        # .format(amari1)
        # )  # 1桁目は必ずamari1:余り(1)
        chars = string.ascii_uppercase[amari1]
        if shou1 > 25:
            shou2, amari2 = divmod(shou1, 26)
            # print(u'\t商(shou1) {}を 26 で割り算 2回目:商(shou2)-> {}, 余り(amari2)-> {}'
            #       .format(shou1, shou2, amari2)
            #       )
            # print(u'b2. 2桁目は 余り(amari2) を利用\n\t{}'.format(amari2))
            chars = string.ascii_uppercase[amari2] + chars
            if 25 >= shou2 >= 1:
                # print(u'c1. 3桁目は 商(shou2) を利用\n\t{}'.format(shou2))
                chars = string.ascii_uppercase[shou2] + chars
            if shou2 > 25:
                shou3, amari3 = divmod(shou2, 25)
                # print(u'\t\t商(shou2) {}を 26 で割り算 3回目:商(shou3)-> {}, 余り(amari3)-> {}'
                #       .format(shou2, shou3, amari3)
                #       )
                # print(u'c2. 3桁目は 余り(amari3) を利用\n\t{}'.format(amari3))
                chars = string.ascii_uppercase[amari3] + chars
                if 25 >= shou3 >= 1:
                    # print(u'd1. 4桁目は 商(shou3) を利用\n\t{}'.format(shou3))
                    chars = string.ascii_uppercase[shou3] + chars
        if 25 >= shou1 >= 1:
            # print(u'b1. 2桁目は 商(shou1) を利用\n\t{}'.format(shou1))
            chars = string.ascii_uppercase[shou1] + chars
        # print(u'-----end')
        # print(u'{} -> {}\n'.format(n, chars))
        # print(type(chars))
        return chars

    # 26 decimalNumber to decimalNumber 26進数から10進数への変換し、出力する メソッド
    def deciNum26_to_deciNum(self, chars):
        u""" < 26進数から10進数への変換し、出力する メソッド >

        #######################

        #.
            :param str chars:

        #.
            :return: num
            :rtype: int

        #######################
        """
        num = 0
        for c in chars:
            # print('c is {}'.format(c))
            # print('\t ord(c) is {}'.format(ord(c)))
            num = num * 26 + (ord(c) - 65)  # print('\t num is {}'.format(num))
        return num

    def nextChar_fromChar(self, char):
        u""" <>

        #######################

        #.
            :param str char:

        #.
            :return: next_char
            :rtype: str

        #######################
        """
        num = self.deciNum26_to_deciNum(char)
        # print(num)
        deciNum26 = self.deciNum_to_26deciNum(num)
        # print(deciNum26)
        num += 1
        # print(num)
        next_char = self.deciNum_to_26deciNum(num)
        return next_char

    # 選択されているオブジェクト名の文字列の構成を調べ、出力する メソッド
    # stringComponents の略
    def strCompsCheck_exe(self, selIndex = None):
        u""" < 選択されているオブジェクト名の文字列の構成を調べ、出力する メソッド >

        ::

          stringComponents の略

        #######################

        #.
            :param str selIndex:

        #.
            :return:
                self.selCompStrs_1st
                , self.selCompStrs_2nd
                , self.selCompStrs_3rd
                , self.typ
            :rtype: tuple[str, str, str, unicode]

        #######################
        """
        patternD = re.compile(r'(.*?)_(.*?)_(.*)|(.*?)_(.*)|(.*\w)')
        # パターン定義:'_'で終わる最短文字列を見つける。
        # ただし、"_"は2ケまでを上限とし、それ以上見つかったときは1ワードとする
        selCompStrs_1st, selCompStrs_2nd, selCompStrs_3rd, type = None, None, None, None
        # print('[{}] strings is componented ...here..'.format(selIndex))
        iterator = patternD.finditer(selIndex)  # 調べる関数
        typ = ''
        for itr in iterator:
            # print(itr.groups())
            if itr.group(6) is None:
                if itr.group(1) is None and itr.group(2) is None and itr.group(3) is None:
                    # print('\tselCompStrs_1st is {}'.format(itr.group(4)))
                    # print('\tselCompStrs_2nd is {}\n'.format(itr.group(5)))
                    selCompStrs_1st = itr.group(4)
                    selCompStrs_2nd = itr.group(5)
                    typ = u'underScoresCount1'
                elif itr.group(4) is None and itr.group(5) is None:
                    # print('\tselCompStrs_1st is {}'.format(itr.group(1)))
                    # print('\tselCompStrs_2nd is {}'.format(itr.group(2)))
                    # print('\tselCompStrs_3rd is {}\n'.format(itr.group(3)))
                    selCompStrs_1st = itr.group(1)
                    selCompStrs_2nd = itr.group(2)
                    selCompStrs_3rd = itr.group(3)
                    typ = u'underScoresCount2'
            if not itr.group(6) is None:
                # print('\tselCompStrs_1st is {} only\n'.format(itr.group(6)))
                selCompStrs_1st = itr.group(6)
                typ = u'underScoresCount0'
        self.selCompStrs_1st = str(selCompStrs_1st)  # unicode to string
        self.selCompStrs_2nd = str(selCompStrs_2nd)  # unicode to string
        self.selCompStrs_3rd = str(selCompStrs_3rd)  # unicode to string
        self.typ = typ
        return self.selCompStrs_1st, self.selCompStrs_2nd, self.selCompStrs_3rd, self.typ

    # textField の待機文字列が、十分にセットされているかどうかの真偽を出力する メソッド
    # 追加
    def isSet_requiredTextField(self, wordListsSet):
        u""" < textField の待機文字列が、十分にセットされているかどうかの真偽を出力する メソッド >

        ::

          追加

        #######################

        #.
            :param list of str wordListsSet:

        #.
            :return: isSet
            :rtype: bool

        #######################
        """
        # print('txFldA1 : \n\t{}'.format(wordListsSet[0]))
        # print('txFldB1 : \n\t{}'.format(wordListsSet[1]))
        isSet = False
        if wordListsSet[0] == '':
            return isSet
        else:
            isSet = True
            return isSet

    # textField の待機文字列 における @ 文字の存在の真偽を出力する メソッド
    def serchAtMark_fromCurrentTxt(self, textStr):
        u""" < textField の待機文字列 における @ 文字の存在の真偽を出力する メソッド >

        #######################

        #.
        :param str textStr:

        #.
            :return: True or False
            :rtype: bool

        #######################
        """
        return '@' in textStr

    # @ (at mark) の数を調べるメソッド
    def atMark_count_fromCurrentTxt(self, wordLists):
        u""" < @ (at mark) の数を調べるメソッド >

        #######################

        #.
            :param list of str wordLists:

        #.
            :return: atMark_count
            :rtype: int

        #######################
        """
        is_atMark_lists = []
        for txtIndex in wordLists:
            # textField の待機文字列 における @ 文字の真偽を出力するメソッド 実行
            is_atMark = self.serchAtMark_fromCurrentTxt(txtIndex)
            is_atMark_lists.append(is_atMark)
        # print(is_atMark_lists)  # e.g.) [True, False, False, False, False]

        # listsの5ケの内 True をカウントする countメソッド 実行
        atMark_count = is_atMark_lists.count(True)
        return atMark_count

    # 各 textField の待機文字列から分解し整理し終えた文字列に対し、
    # 組み立てを行い、出力する メソッド
    def tFld_strs_assemble(self, tFld_decomp, selNode_strs, char):
        u""" < 各 textField の待機文字列から分解し整理し終えた文字列に対し、組み立てを行い、出力する メソッド >

        #######################

        #.
            :param list of str tFld_decomp:
            :param str selNode_strs:
            :param str char:

        #.
            :return: assembleStrs
            :rtype: unicode

        #######################
        """
        # print(tFld_decomp, selNode_strs)
        # textField as selNode_strs
        assembleStrs = u''

        # tuple 化してオリジナルをキープしておく
        tFld_decomp_tuple = tuple(tFld_decomp)
        # print(tFld_decomp_tuple)

        # 1. 単独文字列のみ, の抽出用
        # singleStrings only : sglStrsOly
        # tFld_decomp_sglStrsOly でリスト化
        tFld_decomp_listsA1 = list(tFld_decomp_tuple)  # 初期化
        # print(tFld_decomp_listsA1)
        if '~' in tFld_decomp_listsA1:
            findIndex = tFld_decomp_listsA1.index('~')
            tFld_decomp_listsA1.pop(findIndex)  # '~' 削除
        if '@' in tFld_decomp:
            findIndex = tFld_decomp_listsA1.index('@')
            tFld_decomp_listsA1.pop(findIndex)  # '@' 削除
        if '[' and ']' in tFld_decomp_listsA1:
            sqb_start_index = tFld_decomp_listsA1.index('[')  # '[]'のうち'['の 抽出
            tFld_decomp_listsA1.pop(sqb_start_index + 1)  # 先に'[]'に囲まれた文字列の 抽出と削除
            sqb_start_index = tFld_decomp_listsA1.index('[')  # 再度 '[]'のうち'['の 抽出
            tFld_decomp_listsA1.pop(sqb_start_index)  # '['の 削除
            sqb_end_index = tFld_decomp_listsA1.index(']')  # '[]'のうち']'の 抽出
            tFld_decomp_listsA1.pop(sqb_end_index)  # ']'の 削除
        tFld_decomp_sglStrsOly = tFld_decomp_listsA1
        # print(tFld_decomp_sglStrsOly)

        # 2. []内文字列のみ, の抽出用# surrounded by sqb strings : surdBySqb_strs
        # tFld_decomp_surdBySqb_strs でリスト化
        tFld_decomp_listsA2 = list(tFld_decomp_tuple)  # 初期化
        # print(tFld_decomp_listsA2)
        if '~' in tFld_decomp_listsA2:
            findIndex = tFld_decomp_listsA2.index('~')
            tFld_decomp_listsA2.pop(findIndex)  # '~' 削除
        if '@' in tFld_decomp_listsA2:
            findIndex = tFld_decomp_listsA2.index('@')
            tFld_decomp_listsA2.pop(findIndex)  # '@' 削除
        if '[' and ']' in tFld_decomp_listsA2:
            sqb_start_index = tFld_decomp_listsA2.index('[')  # '[]'のうち'['の 抽出
            tFld_decomp_listsA2.pop(sqb_start_index)  # '['の 削除
            sqb_end_index = tFld_decomp_listsA2.index(']')  # '[]'のうち']'の 抽出
            tFld_decomp_listsA2.pop(sqb_end_index)  # ']'の 削除
        tFld_decomp_surdBySqb_strs = tFld_decomp_listsA2
        for sglStrsOly_index in tFld_decomp_sglStrsOly:
            tFld_decomp_surdBySqb_strs.remove(sglStrsOly_index)
        # print(tFld_decomp_surdBySqb_strs)

        # 3. オリジナルリストから、'[', ']'文字列のみを排除したリスト化 用
        # tFld_decomp_temp_lists でリスト化
        tFld_decomp_listsA3 = list(tFld_decomp_tuple)  # 初期化
        findLists = []
        tgLists = ['[', ']']
        for ind in tFld_decomp_listsA3:
            for tg in tgLists:
                finding = ind.rfind(tg)
                if finding == 0:
                    findLists.append(tg)
        for find_index in findLists:
            tFld_decomp_listsA3.remove(find_index)
        tFld_decomp_temp_lists = tFld_decomp_listsA3
        # print(tFld_decomp_temp_lists)

        # 最終的に, 組み立てに必要となる文字列のリスト化 作成 用
        # tFld_assembleLists でリスト化
        tFld_assembleLists = []
        for tFld_dec_temp_index in tFld_decomp_temp_lists:  # 前から順に追加しているところがミソ
            if tFld_dec_temp_index == '~':
                tFld_assembleLists.append(selNode_strs)
            if tFld_dec_temp_index == '@':
                tFld_assembleLists.append(char)
            if len(tFld_decomp_surdBySqb_strs) > 0:
                if tFld_dec_temp_index == tFld_decomp_surdBySqb_strs[0]:
                    tFld_assembleLists.append(tFld_decomp_surdBySqb_strs[0])
            if len(tFld_decomp_sglStrsOly) > 0:
                for index in tFld_decomp_sglStrsOly:
                    if index == tFld_dec_temp_index:
                        tFld_assembleLists.append(index)

        # print(u'待機文字列の分解した結果: {}'.format(tFld_assembleLists))
        for tFld_as_index in tFld_assembleLists:
            assembleStrs = assembleStrs + tFld_as_index

        return assembleStrs

    # 各 textField の待機文字列から分解し整理し終えた文字列に対し、
    # 組み立て終えた、各々を出力する メソッド
    def eachOneAssembled(self, lists, n1_str, n2_str, n3_str, char):
        u""" < 各 textField の待機文字列から分解し整理し終えた文字列に対し、組み立て終えた、各々を出力する メソッド >

        #######################

        #.
            :param list lists:
            :param str n1_str:
            :param str n2_str:
            :param str n3_str:
            :param str char:

        #.
            :return:
                self.assemble_A
                , self.assemble_B
                , self.assemble_C1, self.assemble_C2, self.assemble_C3
            :rtype: tuple[unicode, unicode, unicode, unicode, unicode]

        #######################
        """
        # print('koko')
        # print(char)
        self.assemble_A = self.tFld_strs_assemble(lists[0], n1_str, char)
        # print('A :' + self.assemble_A)
        # textField A as selNode_1st_strs ###
        # print('is {}'.format(type(self.assemble_A)))

        self.assemble_B = self.tFld_strs_assemble(lists[1], n2_str, char)
        # print('B :' + self.assemble_B)
        # textField B as selNode_2nd_strs ###
        # print('is {}'.format(type(self.assemble_B)))

        self.assemble_C1 = self.tFld_strs_assemble(lists[2], n3_str, char)
        # print('C1 :' + self.assemble_C1)
        # textField C1 as selNode_3rd_strs no1 ###
        # print('is {}'.format(type(self.assemble_C1)))

        self.assemble_C2 = self.tFld_strs_assemble(lists[3], n3_str, char)
        # print('C2 :' + self.assemble_C2)
        # textField C2 as selNode_3rd_strs no1 ###
        # print('is {}'.format(type(self.assemble_C2)))

        self.assemble_C3 = self.tFld_strs_assemble(lists[4], n3_str, char)
        # print('C3 :' + self.assemble_C3)
        # textField C3 as selNode_3rd_strs no1 ###
        # print('is {}'.format(type(self.assemble_C3)))

        # print(self.typ)
        # print(self.assemble_A, self.assemble_B
        #       , self.assemble_C1, self.assemble_C2, self.assemble_C3, self.typ)
        return (self.assemble_A, self.assemble_B
                , self.assemble_C1, self.assemble_C2, self.assemble_C3
                )

    # 各 textField の待機文字列から分解し整理し終えた文字列に対し、
    # 組み立て終えた各々をいったんすべて連結し、出力する メソッド
    def eachOneAssembled_combined_temp(self, textStr_A, textStr_B
                                       , textStr_C1, textStr_C2, textStr_C3
                                       ):
        u""" < 各 textField の待機文字列から分解し整理し終えた文字列に対し、組み立て終えた各々をいったんすべて連結し、出力する メソッド >

        #######################

        #.
            :param str textStr_A:
            :param str textStr_B:
            :param str textStr_C1:
            :param str textStr_C2:
            :param str textStr_C3:

        #.
            :return: temp_strs
            :rtype: str

        #######################
        """
        temp_strs = ('{}_{}_{}{}{}'
                     .format(textStr_A, textStr_B
                             , textStr_C1, textStr_C2, textStr_C3
                             )
                     )
        return temp_strs

    # textField の待機文字列から分解・整理・連結 し終えた仮の待機文字列に対し、
    # 余分なアンダースコアーやNoneが付随してしまう事がある為、それを避けるため、
    # あれば除去し、出力する メソッド
    # (改訂)
    def exceptCheck_patternX(self, temp_strs):
        u"""< 余分なアンダースコアーを操作する メソッド >

        ::

          textField の待機文字列から分解・整理・連結 し終えた仮の待機文字列に対し、
            余分なアンダースコアーやNoneが付随してしまう事がある為、それを避けるため、
                あれば除去し、出力する メソッドです。

          (改訂)

        #######################

        #.
            :param str temp_strs:

        #.
            :return: temp_strs
            :rtype: str

        #######################
        """
        # print(temp_strs)
        ptnX_strs = ''
        patternX = re.compile(r'(?P<ptnA>_{0,}None.*)'
                              r'|'
                              r'(?P<ptnB>_{1,}$)'
                              r'|'
                              r'(?P<ptnC>__)+'
                              r'|'
                              r'(?P<ptnF>^_+)'
                              )
        # ptnA:(_{0,}None.*) :途中に _ None が複数発生するパターン
        # ptnB:(_{1,}$)      :最後に _ が1ケ以上発生するパターン
        # ptnC:(__)+         :途中に _ が2ケ以上連続で発生するパターン
        # ptnF:(^_+)         :最初に _ が1ケ以上発生するパターン
        search = patternX.search(temp_strs)  # ptnA, ptnB, ptnC のみ調べる関数

        # 追加1(ptnAに限る！！)
        patternXD = re.compile(r'(?P<ptnD>_None[a-zA-Z]+)')
        # ptnD:(_None[a-zA-Z]+): _None の後ろにアルファベット(規定の26進数カウント)が見つかったときのパターン
        # 追加2(ptnCに限る！！)
        patternXE = re.compile(r'(?P<ptnE>^_+)')
        # ptnE:(^_+)         :最初に _ が1ケ以上発生するパターン

        if search:  # もしあれば以下を実行
            matchObj = patternX.finditer(temp_strs)
            for it in matchObj:
                ptnX_dict = it.groupdict()
                for keys, values in list(ptnX_dict.items()):  # 変換箇所2: ptnX_dict.items() からの変換
                    if values is not None:
                        # print(keys, values)
                        if keys == 'ptnA':
                            searchXD = patternXD.search(values)  # D を調べる関数X
                            if searchXD:  # ptnD がもしあれば以下を実行
                                matchObjXD = patternXD.finditer(values)
                                for itXD in matchObjXD:
                                    ptn_dictD = itXD.groupdict()
                                    # print(ptn_dictD)
                                    for keysD, valuesD in list(ptn_dictD.items()):  # 変換箇所3: ptn_dictD.items() からの変換
                                        # print(keysD, valuesD)
                                        if valuesD != 'None':
                                            # print(keysD, valuesD)
                                            # print(valuesD)  # or itXD.group('ptnD')
                                            # 1.strs 新たに作成された文字列
                                            repStrs = valuesD.replace('None', '')
                                            # 2.一度 patternX で実行された、
                                            # パターン箇所を全削除作成されてしまった文字列
                                            ptnX_strs = patternX.sub('', temp_strs)
                                            # 1. 2. の文字列を組合わせる
                                            ptnX_strs = ptnX_strs + repStrs
                            else:  # ptnD が, もしなければ以下を実行
                                ptnX_strs = patternX.sub('', temp_strs)  # パターン箇所を全削除
                        elif keys == 'ptnB':
                            ptnX_strs = patternX.sub('', temp_strs)  # パターン箇所を全削除
                        elif keys == 'ptnC':
                            ptnX_strs = patternX.sub('_', temp_strs)  # パターン箇所を置換
                            # print(ptnX_strs)
                            # searchXE = patternXE.search(values)  # E を調べる関数X
                            # if searchXE:  # ptnE がもしあれば以下を実行
                            #     matchObjXE = patternXE.finditer(values)
                            #     for itXE in matchObjXE:
                            #         ptn_dictE = itXE.groupdict()
                            #         print(ptn_dictE)
                            #         for keysE, valuesE in ptn_dictE.items():
                            #             print(keysE, valuesE)
                            #             print('*')
                            #             if valuesE:
                            #                 ptnX_strs = patternX.sub('', temp_strs)  # パターン箇所を全削除
                            #                 print(ptnX_strs)
                        elif keys == 'ptnF':
                            ptnX_strs = patternX.sub('', temp_strs)  # パターン箇所を全削除
                        return ptnX_strs
        return temp_strs  # もしなければ temp_strs をそのまま使用

    # シーン内から、DG name を全てリストし、出力する メソッド
    def getDGAll_fromScene(self):
        u""" < シーン内から、DG name を全てリストし、出力する メソッド >

        #######################

        #.
            :return: getName
            :rtype: list of str

        #######################
        """
        getObj = cmds.ls(long = True, dag = True)  # 常時更新の、新規リスト作成
        r = re.compile(r'[0-9]*$')
        lists = []
        for i, obj in enumerate(getObj):
            objName = (re.sub(r'[0-9]*$', r'', obj))
            # print(objName)
            no = r.search(obj).group(0)
            # print(no)
            if no == '':
                no = 0
            else:
                no = int(no)
            # print(no)
            value = (obj.count('|'))
            # print(value)
            lists.append([obj, objName, no, value])
        # for l in lists:
        #     print(l)
        getObj = [k[0] for k in sorted(lists, key = lambda x: (-x[3], x[1], x[2]))]
        # print(getObj)
        getName = [obj.rsplit('|', 1)[1] for obj in getObj]
        # 必ず末尾(右)から1番目の'|'で2つに分割し、その[1]番目を出力する、rsplit メソッド の実行
        # print(getName)
        return getName

    # 任意の文字列が、
    # 任意の文字列リスト内に、
    # 重複した名前として既にあるかどうかを探しあて、存在の真偽を出力する メソッド
    def searchForDuplicateName(self, strsLists, strs):
        u""" < 重複した名前として、存在の真偽を出力する メソッド>

        ::

          任意の文字列が、
            任意の文字列リスト内に、
                重複した名前として既にあるかどうかを探しあて、存在の真偽を出力する
                    メソッドです。

        #######################

        #.
            :param list of str strsLists:
            :param str strs:

        #.
            :return:
            :rtype: bool

        #######################
        """
        return strs in strsLists
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
    #   proc2. 最後に、共通な rename 操作 を行っています。
    #       proc2-main1. proc2-main3.
    ##########################################

    # < UI用 >
    # proc1. #
    # Execute 実行 関数
    # @instance.declogger
    def ui_executeBtnCmd(self, *args):
        u""" < UI用 >

        ::

          proc1.
            Execute 実行 関数

        """
        # 追加7 ####################################################### start
        check_string = 'check'
        # message(check_string)
        # print(self.statusCurrent_scriptEditor2)
        print(check_string)
        state: str = self.statusCurrent_scriptEditor2
        print(state)
        if state == 'closed':
            self.create_scriptEditor2_and_show()
            print('reOpen')
            self.scriptEditor2.append_default('reOpen')
        elif state == 'open':
            print('open済、再利用')
            self.scriptEditor2.append_default('open済、再利用')
        # 追加7 ####################################################### end

        # UIありきでの実行
        self.scriptEditor2.append_default('\n## ui_executeBtn type ##\n')
        self.scriptEditor2.append_default(u'## 継続中 ########## rename proc 1 (ui_executeBtn type)')
        # print('\n## ui_executeBtn type ##\n')
        # print(u'## 継続中 ########## rename proc 1 (ui_executeBtn type)')

        # ##############################################################
        # proc1. #
        # カレントの、textField 文字列を抜き出します。
        # ###########################################
        self.mode = self.currentMode()
        self.currentTxt_A1 = self.get_currentTxt_A1()
        self.currentTxt_B1 = self.get_currentTxt_B1()
        self.currentTxt_C1 = self.get_currentTxt_C1()
        self.currentTxt_C2 = self.get_currentTxt_C2()
        self.currentTxt_C3 = self.get_currentTxt_C3()

        print(u'\n'
              u'// Result: {packageName}.'
              u'{title}.{className}().exe('
              u'mode = {modeInt}'
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
                      , modeInt = self.mode
                      , a = self.currentTxt_A1, b = self.currentTxt_B1
                      , c1 = self.currentTxt_C1
                      , c2 = self.currentTxt_C2
                      , c3 = self.currentTxt_C3
                      )
              )
        # ##############################################################

        # print(self.mode, self.wordListsSet_fromUI)

        # ##############################
        # 一時的、選択リスト(1回目)
        # ##############################
        # 予め出力 選択ノード関連
        self.selectionLists = commonCheckSelection()  # 自動で空にもなる
        # ##############################
        # print(u'選択ノード関連\n\t'
        #       u'self.selectionLists : \n\t\t'
        #       u'{}'.format(self.selectionLists))
        # print(u'選択ノード関連\n\t'
        #       u'len(self.selectionLists) : \n\t\t'
        #       u'{}'.format(len(self.selectionLists)))
        # ##############################

        # 追加
        # 当ツール renameTool5 独自の 選択ノードの明示に使用
        self.initSelectionNodeUUIDListsA.__init__()  # 常に初期化で空にする
        yo_uuid.initSelectionNode_storeUUID(self.selectionLists)

        # 予め出力
        # シーン内 DG name 全リストを出力する メソッド の実行
        self.getObj = self.getDGAll_fromScene()
        # print(self.getObj)

        # 予め出力 TextField関連ttrft
        self.wordListsSet_fromUI.__init__()  # 常に初期化で空にする
        self.wordListsSet_fromUI = self.createLists_fromCurrentTxtAll()
        # ##############################
        # print(u'TextField関連\n\t'
        #       u'self.wordListsSet_fromUI(wordLists) : \n\t\t'
        #       u'{}'.format(self.wordListsSet_fromUI)
        #       )
        # ##############################

        # 共通な一連の関数のまとまり です
        # 場合分けによって、後の方で、
        #   proc1.5., proc2. rename 操作 に入っていきます
        self.setOfCommonFunctions(self.wordListsSet_fromUI)

        # 追加
        # かなり初期の段階で選択を実行します
        # b/c): 当ツール renameTool5 独自の 選択ノードの明示に使用
        cmds.select(cl = True)
        yo_uuid.initSelectionNode_reSelect(self.initSelectionNodeUUIDListsA)
    # 3. UI-3. common ボタン コマンド群 ################################################## end

    # 5. スクリプトベースコマンド入力への対応 ############################################# start

    ##########################################
    # <スクリプトベース用>
    ##########################################
    # プロセスの大枠 #######
    #######################
    # parameter mode, parameter n を対象に、
    # proc1. analysis_strs_fromCmd メソッドを利用して、必要な文字列を抜き出します。
    # <共通>
    #   proc1.5.
    # <共通>
    #   proc2. 最後に、共通な rename 操作 を行っています。
    #       proc2-main1. proc2-main3.
    ##########################################

    # < スクリプトベース用 >
    # proc1. #
    # analysis_strs_fromCmd メソッドを利用して、必要な文字列を抜き出します。
    def exe(self, mode = 0, n = None):
        u"""< スクリプトベース用 >

        ::

          proc1.
              analysis_strs_fromCmd メソッドを利用して、必要な文字列を抜き出します。

        #######################

        #.
            :param int mode:
                rename mode: 強制的:0, 構成要素をキープ:1 何れか

            e.g.): mode = 1
        #.
            :param list[str] n: 文字列リスト(range 5)

            e.g.): n = [u'lip', u'jt@', u'', u'', u'L']

        #######################
        """
        # 追加7 ####################################################### start
        check_string = 'check'
        # message(check_string)
        # print(self.statusCurrent_scriptEditor2)
        print(check_string)
        state: str = self.statusCurrent_scriptEditor2
        print(state)
        if state == 'closed':
            self.create_scriptEditor2_and_show()
            print('reOpen')
            self.scriptEditor2.append_default('reOpen')
        elif state == 'open':
            print('open済、再利用')
            self.scriptEditor2.append_default('open済、再利用')
        # 追加7 ####################################################### end

        if n is None:
            n = []
        # title = cls.title
        # className = cls.className

        # UI不要での実行
        # 追加7 ####################################################### start
        self.scriptEditor2.append_default('\n## command_execute type ##\n')
        self.scriptEditor2.append_default(u'## 継続中 ########## rename proc 1 (command_execute type)')
        # 追加7 ####################################################### end
        # print('\n## command_execute type ##\n')
        # print(u'## 継続中 ########## rename proc 1 (command_execute type)')

        print(u'\n'
              u'// Result: {packageName}.'
              u'{title}.{className}().exe('
              u'mode = {modeInt}'
              u', '
              u'n = {textAll}'
              u')'
              u'\n'
              .format(packageName = self.pkgName
                      , title = self.title + self.id, className = self.className
                      , modeInt = mode
                      , textAll = n
                      )
              )
        # ##############################################################
        # proc1. #
        # コマンド文字列の parameter mode, parameter n を分析し、
        # modeInt_fromCmd, wordListsSet_fromCmd を出力する メソッド の実行
        # ###########################################
        modeInt_fromCmd, wordListsSet_fromCmd = self.analysis_strs_fromCmd(mode, n)
        self.mode = modeInt_fromCmd

        # print(modeInt_fromCmd, wordListsSet_fromCmd)

        # ##############################################################

        # ##############################
        # 一時的、選択リスト(1回目)
        # ##############################
        # 予め出力 選択ノード関連
        self.selectionLists = commonCheckSelection()  # 自動で空にもなる
        # ##############################
        # print(u'選択ノード関連\n\t'
        #       u'self.selectionLists : \n\t\t'
        #       u'{}'.format(self.selectionLists)
        #       )
        # print(u'選択ノード関連\n\t'
        #       u'len(self.selectionLists) : \n\t\t'
        #       u'{}'.format(len(self.selectionLists))
        #       )
        # ##############################

        # 追加
        # 当ツール renameTool5 独自の 選択ノードの明示に使用
        self.initSelectionNodeUUIDListsA.__init__()  # 常に初期化で空にする
        yo_uuid.initSelectionNode_storeUUID(self.selectionLists)

        # 予め出力
        # シーン内から、DG name を全てリストし、出力する メソッド の実行
        self.getObj = self.getDGAll_fromScene()
        # print(self.getObj)

        # 予め出力済 TextField関連をコマンドから抽出
        # print(modeInt_fromCmd, wordListsSet_fromCmd)
        self.wordListsSet_fromCmd.__init__()  # 常に初期化で空にする
        self.wordListsSet_fromCmd = wordListsSet_fromCmd
        # ##############################
        # print(u'TextField関連\n\t'
        #       u'self.wordListsSet_fromCmd(wordLists) : \n\t\t'
        #       u'{}'.format(self.wordListsSet_fromCmd)
        #       )
        # ##############################

        # 共通な一連の関数のまとまり です
        # 場合分けによって、後の方で、
        #   proc1.5., proc2. rename 操作 に入っていきます
        self.setOfCommonFunctions(self.wordListsSet_fromCmd)

        # 追加
        # かなり初期の段階で選択を実行します
        # b/c): 当ツール renameTool5 独自の 選択ノードの明示に使用
        cmds.select(cl = True)
        yo_uuid.initSelectionNode_reSelect(self.initSelectionNodeUUIDListsA)

    # < スクリプトベース用 >
    # コマンド文字列の parameter mode, parameter n を分析し、
    # 必要な文字列 modeInt_fromCmd, wordListsSet_fromCmd
    # を出力する メソッド
    def analysis_strs_fromCmd(self, mode, n):
        u""" < スクリプトベース用 >

        ::

          コマンド文字列の parameter mode, parameter n を分析し、
            必要な文字列 modeInt_fromCmd, wordListsSet_fromCmd
                を出力する メソッドです

        #######################

        #.
            :param int mode:

        #.
            :param list of str n:

        #.
            :return: modeInt_fromCmd, wordListsSet_fromCmd
            :rtype tuple[str, list[str]:

        #######################
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
        modeInt_fromCmd = modeInt_fromCmd[0]  # type: str
        # print(modeInt_fromCmd)

        #############################################
        # 分析2 n ###  リスト文字列を一旦文字列に変換・分析し、リスト文字列として返す
        # あらかじめ用意されている文字列, 'n = [u'***'...],'から、必要な文字列 *** を抽出する
        strs = 'n = {}'.format(n)  # 先ず、文字列にする
        # print(strs)
        patternC = re.compile(r'\'(?P<ptnC>.*?)\'')  # 変換箇所4: re.compile(r'u\'(?P<ptnC>.*?)\'') からの変更
        # パターン定義: u' と ' で囲まれた文字列を最短文字列で見つける
        wordListsSet_fromCmd: List[str | Any] = []  # コマンド文字列から抽出の wordListsSet
        search = patternC.finditer(strs)  # 調べる関数
        # あるならば
        if search:
            iterator = patternC.finditer(strs)
            for itr in iterator:
                # print(itr.group('ptnC'))
                wordListsSet_fromCmd.append(itr.group('ptnC'))  # 見つけた順にリストに格納する
        # print(wordListsSet_fromCmd)

        return modeInt_fromCmd, wordListsSet_fromCmd
    # 5. スクリプトベースコマンド入力への対応 ############################################### end

    # 「rename の核となる コマンド群」 #################################################### start
    # 共通な一連の関数のまとまり ########################################### start
    # 共通な一連の関数のまとまり です
    # proc1.5. #
    # 場合分けによって、後の方で、
    #   - proc2. rename 操作 に入る箇所 継続
    #       具体的な箇所: # DBBB, # CBB
    #   - イレギュラー操作箇所 継続
    #       具体的な箇所: # DAAA
    #   - 他はすべて操作 ストップ
    # させます
    # @instance.declogger
    def setOfCommonFunctions(self, wordLists):
        u""" < 共通な一連の関数のまとまり です >

        ::

          proc1.5.
          場合分けによって、後の方で、
              - proc2. rename 操作 に入る箇所 継続
                  具体的な箇所: # DBBB, # CBB
              - イレギュラー操作箇所 継続
                  具体的な箇所: # DAAA
              - 他はすべて操作 ストップ
          させます

        #######################

        #.
            :param list[str] wordLists:

        #######################
        """
        # 追加7 ####################################################### start
        self.scriptEditor2.append_default(u'## 継続中 ########## rename proc 1.5')
        # 追加7 ####################################################### end

        # print(u'## 継続中 ########## rename proc 1.5')

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

        # 予め出力 選択ノード関連
        # 選択された全ノードに対して、一つずつ、unique な名前かどうかを調べ、True, False のリストを返す メソッド
        # self.isUniqueName_list = self.is_uniqueName(self.selectionLists)  # list of bool
        # ##############################
        # print(u'選択ノード関連\n\t'
        #       u'self.isUniqueName_list : \n\t\t'
        #       u'{}'.format(self.isUniqueName_list)
        #       )
        # ##############################

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

        # print(f'self.selectionLists: {self.selectionLists}')  # 選択中

        # 予め出力
        # イレギュラー対応用変数を出力するための関数 実行
        # ここでいうイレギュラーとは、「選択1っ、atMark 0、TextField関連が完全 の時」 を言います
        # イレギュラー対応用変数 self.waiting_last_string (default: '') を予め出力
        # イレギュラー対応用変数 self.is_exists_forNCName (default: False) を予め出力
        # 選択1っ、atMark 0、TextField関連が完全 の時だけに対応
        self.renameFunction_inIrregularCases()

        # TextField名の構成から判断された、待機している最終文字
        # # ##############################
        # print(u'<イレギュラー対応用>TextField名の構成から判断された、待機している最終文字\n\t'
        #       u'self.waiting_last_string : \n\t\t'
        #       u'{}'.format(self.waiting_last_string)
        #       )
        # # ##############################

        # self.waiting_last_string が、
        # self.getObj リスト内に、
        # 重複した名前として既にあるかどうかを探しあて、存在の真偽を出力する メソッドの実行
        # False: 重複していない
        # True: 重複している 注意!
        ##############################

        # 変換箇所5
        # YO_logProcess.action('DEBUG'
        #                      , u'{}\n\t\t\tLine Number:{}\n'
        #                        u'<イレギュラー対応用>重複した名前として、'
        #                        u'待機している最終文字が既にあるかどうかを探しあて、存在の真偽\n\t'
        #                        u'self.is_exists_forNCName : \n\t\t'
        #                        u'{}'
        #                      .format(self.title
        #                              , YO_logger2.getLineNo()
        #                              , self.is_exists_forNCName
        #                              )
        #                      )

        # print(u'<イレギュラー対応用>重複した名前として、待機している最終文字が既にあるかどうかを探しあて、存在の真偽\n\t'
        #       u'self.is_exists_forNCName : \n\t\t'
        #       u'{}'.format(self.is_exists_forNCName)
        #       )

        ##############################

        ##############################
        # 場合分けによって、後の方で、
        #   - proc2. rename 操作 に入る箇所 継続
        #       具体的な箇所: # DBBB, # CBB
        #   - イレギュラー操作箇所 継続
        #       具体的な箇所: # DAAA
        #   - 他はすべて操作 ストップ
        # させます
        #############
        # 未選択の場合  # A
        if len(self.selectionLists) == 0:  # A
            # print(u'ストップ A')

            # 追加7 ####################################################### start
            self.scriptEditor2.append_error(u'{}\n\t\t\tLine Number:{}\n'
                                            u'ストップ A\n'
                                            u'何も選択されていないため、'
                                            u'rename する対象がありません。'
                                            u'rename の実行はストップしました。rename proc 1.5-A'
                                            .format(self.title, YO_logger2.getLineNo())
                                            )
            # 追加7 ####################################################### end

            # 変換箇所5
            # YO_logProcess.action('ERROR'
            #                      , u'{}\n\t\t\tLine Number:{}\n'
            #                        u'ストップ A\n'
            #                        u'何も選択されていないため、'
            #                        u'rename する対象がありません。'
            #                        u'rename の実行はストップしました。rename proc 1.5-A'
            #                      .format(self.title, YO_logger2.getLineNo())
            #                      )

            # message_warning(u'何も選択されていないため、'
            #                      u'rename する対象がありません。'
            #                      u'rename の実行はストップしました。rename proc 1.5-A'
            #                      )

            pass
        #############
        # 選択1つの場合  # D
        elif len(self.selectionLists) == 1:  # D
            # 追加7 ####################################################### start
            self.scriptEditor2.append_default(u'単独選択で実行中..')
            # 追加7 ####################################################### end

            # print(u'単独選択で実行中..')

            # atMark 0
            if self.atMark_count == 0:  # DA
                # 追加7 ####################################################### start
                self.scriptEditor2.append_default(u'継続 DA')
                # 追加7 ####################################################### end

                # print(u'継続 DA')

                # TextField関連が完全
                if self.isSet_reqTxtFld:  # DAA
                    # 追加7 ####################################################### start
                    self.scriptEditor2.append_default(u'継続 DAA')
                    # 追加7 ####################################################### end

                    # print(u'継続 DAA')

                    # False: 重複していない
                    # 選択1っ、atMark 0、TextField関連が完全、重複していない
                    if self.is_exists_forNCName is False:  # DAAA
                        # コマンドベース入力
                        # 第3単語-要素1フィールド、要素2フィールド、要素3フィールド誤入力判別 実行 追加
                        isWrong = self.wrong_input_determining_fromCmd(wordLists)
                        if not isWrong:  # DAAA  # False: 誤入力なし で継続
                            # 追加7 ####################################################### start
                            self.scriptEditor2.append_default(u'継続 DAAA')
                            self.scriptEditor2.append_default('******** inIrregularCases rename start.. '
                                  '************************************************'
                                  'inIrregularCases rename proc 1.5-DAAA'
                                  )
                            # 追加7 ####################################################### end

                            # print(u'継続 DAAA')
                            # print('******** inIrregularCases rename start.. '
                            #       '************************************************'
                            #       'inIrregularCases rename proc 1.5-DAAA'
                            #       )

                            cmds.rename(self.selectionLists[0], self.waiting_last_string)
                            ##############################
                            # 追加7 ####################################################### start
                            self.scriptEditor2.append_default('******** inIrregularCases rename done '
                                  '************************************************'
                                  'inIrregularCases rename proc 1.5-DAAA'
                                  )
                            # 追加7 ####################################################### end

                            # print('******** inIrregularCases rename done '
                            #       '************************************************'
                            #       'inIrregularCases rename proc 1.5-DAAA'
                            #       )
                            ##############################
                    # True: 重複している 注意!
                    else:  # DAAB
                        # print(u'ストップ DAAB')

                        # 追加7 ####################################################### start
                        self.scriptEditor2.append_error(
                            u'{}\n\t\t\tLine Number:{}\n'
                            u'ストップ DAAB\n'
                            u'各 textFiled 内へのユーザー指定の文字列'
                            u'は充分に挿入されていますが、'
                            u'待機している最終文字列 \'{}\' '
                            u'は、'
                            u'予めシーン内の文字列リスト内に、'
                            u'重複して存在している可能性があるため'
                            u'rename の実行はストップしました。rename proc 1.5-DAAB'
                            .format(self.title
                                    , YO_logger2.getLineNo()
                                    , self.waiting_last_string
                                    )
                            )
                        # 追加7 ####################################################### end

                        # # 変換箇所5
                        # YO_logProcess.action('ERROR'
                        #                      , u'{}\n\t\t\tLine Number:{}\n'
                        #                        u'ストップ DAAB\n'
                        #                        u'各 textFiled 内へのユーザー指定の文字列'
                        #                        u'は充分に挿入されていますが、'
                        #                        u'待機している最終文字列 \'{}\' '
                        #                        u'は、'
                        #                        u'予めシーン内の文字列リスト内に、'
                        #                        u'重複して存在している可能性があるため'
                        #                        u'rename の実行はストップしました。rename proc 1.5-DAAB'
                        #                      .format(self.title
                        #                              , YO_logger2.getLineNo()
                        #                              , self.waiting_last_string
                        #                              )
                        #                      )

                        # message_warning(u'各 textFiled 内へのユーザー指定の文字列'
                        #                      u'は充分に挿入されていますが、'
                        #                      u'待機している最終文字列 \'{}\' '
                        #                      u'は、'
                        #                      u'予めシーン内の文字列リスト内に、'
                        #                      u'重複して存在している可能性があるため'
                        #                      u'rename の実行はストップしました。rename proc 1.5-DAAB'
                        #     .format(self.waiting_last_string)
                        #                      )

                        pass
                # TextField関連が完全でない
                else:  # DAB
                    # print(u'ストップ DAB')

                    # 変換箇所5
                    # YO_logProcess.action('WARNING'
                    #                      , u'{}\n\t\t\tLine Number:{}\n'
                    #                        u'ストップ DAB\n'
                    #                        u'各 textFiled 内に、ユーザー指定の文字列'
                    #                        u'が充分に挿入されていません。'
                    #                        u'少なくとも、'
                    #                        u'第1単語フィールドへの文字列挿入は必須です。'
                    #                        u'rename の実行はストップしました。rename proc 1.5-DAB'
                    #                      .format(self.title, YO_logger2.getLineNo())
                    #                      )

                    # message_warning(u'各 textFiled 内に、ユーザー指定の文字列'
                    #                      u'が充分に挿入されていません。'
                    #                      u'少なくとも、'
                    #                      u'第1単語フィールドへの文字列挿入は必須です。'
                    #                      u'rename の実行はストップしました。rename proc 1.5-DAB'
                    #                      )

                    pass
            # atMark 0でない
            else:  # DB
                # TextField関連が完全でない
                if not self.isSet_reqTxtFld:  # DBA
                    # print(u'ストップ DBA')

                    # 変換箇所5
                    # YO_logProcess.action('WARNING'
                    #                      , u'{}\n\t\t\tLine Number:{}\n'
                    #                        u'ストップ DBA\n'
                    #                        u'単独選択で実行中です。'
                    #                        u'各 textFiled 内に、ユーザー指定の文字列'
                    #                        u'が充分に挿入されていません。'
                    #                        u'少なくとも、'
                    #                        u'第1単語フィールドへの文字列挿入は必須です。'
                    #                        u'rename の実行はストップしました。rename proc 1.5-DBA'
                    #                      .format(self.title, YO_logger2.getLineNo())
                    #                      )

                    # message_warning(u'単独選択で実行中です。'
                    #                      u'各 textFiled 内に、ユーザー指定の文字列'
                    #                      u'が充分に挿入されていません。'
                    #                      u'少なくとも、'
                    #                      u'第1単語フィールドへの文字列挿入は必須です。'
                    #                      u'rename の実行はストップしました。rename proc 1.5-DBA'
                    #                      )

                    pass
                # TextField関連が完全
                else:  # DBB
                    # 追加7 ####################################################### start
                    self.scriptEditor2.append_default(u'継続 DBB')
                    # 追加7 ####################################################### end

                    # print(u'継続 DBB')

                    # atMark 多い
                    if self.atMark_count >= 2:  # DBBA
                        # print(u'ストップ DBBA')

                        # 追加7 ####################################################### start
                        self.scriptEditor2.append_error(
                            u'{}\n\t\t\tLine Number:{}\n'
                            u'ストップ DBBA\n'
                            u'各 textFiled 内に、@ (at mark) '
                            u'が複数挿入されています。'
                            u'可能な限り、一つの入力で留めてください。'
                            u'rename の実行はストップしました。rename proc 1.5-DBBA'
                            .format(self.title
                                    , YO_logger2.getLineNo()
                                    , YO_logger2.getLineNo()
                                )
                            )
                        # 追加7 ####################################################### end

                        # # 変換箇所5
                        # YO_logProcess.action('ERROR'
                        #                      , u'{}\n\t\t\tLine Number:{}\n'
                        #                        u'ストップ DBBA\n'
                        #                        u'各 textFiled 内に、@ (at mark) '
                        #                        u'が複数挿入されています。'
                        #                        u'可能な限り、一つの入力で留めてください。'
                        #                        u'rename の実行はストップしました。rename proc 1.5-DBBA'
                        #                      .format(self.title, YO_logger2.getLineNo())
                        #                      )

                        # message_warning(u'各 textFiled 内に、@ (at mark) '
                        #                      u'が複数挿入されています。'
                        #                      u'可能な限り、一つの入力で留めてください。'
                        #                      u'rename の実行はストップしました。rename proc 1.5-DBBA'
                        #                      )

                        pass
                    # 選択1っ、atMark 1、TextField関連が完全
                    elif self.atMark_count == 1:  # DBBB
                        # コマンドベース入力
                        # 第3単語-要素1フィールド、要素2フィールド、要素3フィールド誤入力判別 実行 追加
                        isWrong = self.wrong_input_determining_fromCmd(wordLists)
                        # 追加7 ####################################################### start
                        self.scriptEditor2.append_default(f'isWrong: {isWrong}')
                        # 追加7 ####################################################### end

                        # print(f'isWrong: {isWrong}')

                        if not isWrong:  # DBBB  # False: 誤入力なし で継続
                            # 追加7 ####################################################### start
                            self.scriptEditor2.append_default(u'継続 DBBB')
                            # 追加7 ####################################################### end

                            # print(u'継続 DBBB')

                            # 変換箇所5
                            # YO_logProcess.action('INFO'
                            #                      , u'******** rename proc start.. '
                            #                        u'************************************************'
                            #                        u'rename proc 1.5-DBBB'
                            #                      )

                            # print('******** rename proc start.. '
                            #       '************************************************'
                            #       'rename proc 1.5-DBBB'
                            #       )

                            # ##############################
                            # 一時的、選択リストの更新(2回目) < ---- ここ重要!!!!!
                            # ##############################
                            # 選択した全ノード名に対して、unique name にして更新する メソッド の実行
                            # 追加7 ####################################################### start
                            self.scriptEditor2.append_default('self.selectionLists: {}'.format(self.selectionLists))
                            # 追加7 ####################################################### end

                            # print('self.selectionLists: {}'.format(self.selectionLists))

                            self.selectionLists = self.checkAndDoUniqueName_forSlNode(self.selectionLists)
                            # 追加7 ####################################################### start
                            self.scriptEditor2.append_default('self.selectionLists: {}'.format(self.selectionLists))  # 選択リストの更新 < ---- ここ重要!!!!!
                            # 追加7 ####################################################### end

                            # print('self.selectionLists: {}'.format(self.selectionLists))  # 選択リストの更新 < ---- ここ重要!!!!!

                            # ##############################################################
                            # proc2. #
                            # rename 操作  --「rename の核となる コマンド群」 に詳細--
                            # ###########################################
                            # rename の核となるメソッドは、以下の計2つ。
                            # proc2-main1. #
                            #   start_executeCmd   ----  rename start code (共通)
                            # proc2-main3. #
                            #   renameMain_exe     ----  rename next code (共通)
                            # ###########################################
                            self.start_executeCmd(self.selectionLists, self.mode, wordLists)

                            # 変換箇所5
                            # YO_logProcess.action('INFO'
                            #                      , u'{}\n\t\t\tLine Number:{}\n'
                            #                        u'******** rename proc done '
                            #                        u'************************************************'
                            #                        u'rename proc 1.5-DBBB'
                            #                      .format(self.title
                            #                              , YO_logger2.getLineNo()
                            #                              )
                            #                      )

                            # print('******** rename proc done '
                            #       '************************************************'
                            #       'rename proc 1.5-DBBB'
                            #       )

                            # ##############################################################
        #############
        # 選択複数の場合  # C
        elif len(self.selectionLists) >= 2:  # C
            # 追加7 ####################################################### start
            self.scriptEditor2.append_default(u'複数選択で実行中..')
            # 追加7 ####################################################### end

            # print(u'複数選択で実行中..')

            # TextField関連が完全でない
            if not self.isSet_reqTxtFld:  # CA
                # print(u'ストップ CA')

                # 変換箇所5
                # YO_logProcess.action('WARNING'
                #                      , u'{}\n\t\t\tLine Number:{}\n'
                #                        u'ストップ CA\n'
                #                        u'複数選択で実行中です。'
                #                        u'各 textFiled 内に、ユーザー指定の文字列'
                #                        u'が充分に挿入されていません。'
                #                        u'少なくとも、'
                #                        u'第1単語フィールドへの文字列挿入は必須です。'
                #                        u'rename の実行はストップしました。rename proc 1.5-CA'
                #                      .format(self.title, YO_logger2.getLineNo())
                #                      )

                # message_warning(u'複数選択で実行中です。'
                #                      u'各 textFiled 内に、ユーザー指定の文字列'
                #                      u'が充分に挿入されていません。'
                #                      u'少なくとも、'
                #                      u'第1単語フィールドへの文字列挿入は必須です。'
                #                      u'rename の実行はストップしました。rename proc 1.5-CA'
                #                      )

                pass
            # TextField関連が完全
            else:  # CB
                if self.atMark_count >= 2:  # CBA
                    # atMark 多い
                    # print(u'ストップ CBA')

                    # 追加7 ####################################################### start
                    self.scriptEditor2.append_error(
                        u'{}\n\t\t\tLine Number:{}\n'
                        u'ストップ CBA\n'
                        u'各 textFiled 内に、@ (at mark) '
                        u'が複数挿入されています。'
                        u'可能な限り、一つの入力で留めてください。'
                        u'rename の実行はストップしました。rename proc 1.5-CBA'
                        .format(self.title
                                , YO_logger2.getLineNo()
                                )
                        )
                    # 追加7 ####################################################### end

                    # # 変換箇所5
                    # YO_logProcess.action('ERROR'
                    #                      , u'{}\n\t\t\tLine Number:{}\n'
                    #                        u'ストップ CBA\n'
                    #                        u'各 textFiled 内に、@ (at mark) '
                    #                        u'が複数挿入されています。'
                    #                        u'可能な限り、一つの入力で留めてください。'
                    #                        u'rename の実行はストップしました。rename proc 1.5-CBA'
                    #                      .format(self.title
                    #                              , YO_logger2.getLineNo()
                    #                              )
                    #                      )

                    # message_warning(u'各 textFiled 内に、@ (at mark) '
                    #                      u'が複数挿入されています。'
                    #                      u'可能な限り、一つの入力で留めてください。'
                    #                      u'rename の実行はストップしました。rename proc 1.5-CBA'
                    #                      )

                    pass
                # 選択複数、atMark 1、TextField関連が完全
                elif self.atMark_count == 1:  # CBB
                    # コマンドベース入力
                    # 第3単語-要素1フィールド、要素2フィールド、要素3フィールド誤入力判別 実行 追加
                    isWrong = self.wrong_input_determining_fromCmd(wordLists)
                    if not isWrong:  # CBB  # False: 誤入力なし で継続
                        # print(u'継続 CBB')

                        # 変換箇所5
                        # YO_logProcess.action('INFO'
                        #                      , u'{}\n\t\t\tLine Number:{}\n'
                        #                        u'継続 CBB  \n'
                        #                        u'******** rename proc start.. '
                        #                        u'************************************************'
                        #                        u'rename proc 1.5-CBB'
                        #                      .format(self.title
                        #                              , YO_logger2.getLineNo()
                        #                              )
                        #                      )

                        # print('******** rename proc start.. '
                        #       '************************************************'
                        #       'rename proc 1.5-CBB'
                        #       )

                        # ##############################
                        # 一時的、選択リストの更新(2回目) < ---- ここ重要!!!!!
                        # ##############################
                        # 選択した全ノード名に対して、unique name にして更新する メソッド の実行
                        # 追加7 ####################################################### start
                        self.scriptEditor2.append_default('self.selectionLists: {}'.format(self.selectionLists))
                        # 追加7 ####################################################### end

                        # print('self.selectionLists: {}'.format(self.selectionLists))

                        self.selectionLists = self.checkAndDoUniqueName_forSlNode(self.selectionLists)
                        # 追加7 ####################################################### start
                        self.scriptEditor2.append_default('self.selectionLists: {}'.format(self.selectionLists))  # 選択リストの更新 < ---- ここ重要!!!!!
                        # 追加7 ####################################################### end

                        # print('self.selectionLists: {}'.format(self.selectionLists))  # 選択リストの更新 < ---- ここ重要!!!!!

                        # ##############################################################
                        # proc2. #
                        # rename 操作  --「rename の核となる コマンド群」 に詳細--
                        # ###########################################
                        # rename の核となるメソッドは、以下の計2つ。
                        # proc2-main1. #
                        #   start_executeCmd   ----  rename start code (共通)
                        # proc2-main3. #
                        #   renameMain_exe     ----  rename next code (共通)
                        # ###########################################
                        self.start_executeCmd(self.selectionLists, self.mode, wordLists)

                        # 変換箇所5
                        # YO_logProcess.action('INFO'
                        #                      , u'{}\n\t\t\tLine Number:{}\n'
                        #                        u'******** rename proc done '
                        #                        u'************************************************'
                        #                        u'rename proc 1.5-CBB'
                        #                      .format(self.title
                        #                              , YO_logger2.getLineNo()
                        #                              )
                        #                      )

                        # print('******** rename proc done '
                        #       '************************************************'
                        #       'rename proc 1.5-CBB'
                        #       )

                        # ##############################################################
                # 選択複数、atMark 0、TextField関連が完全
                elif self.atMark_count == 0:  # CBC
                    # print(u'ストップ CBC')

                    # 追加7 ####################################################### start
                    self.scriptEditor2.append_error(
                        u'{}\n\t\t\tLine Number:{}\n'
                        u'ストップ CBC\n'
                        u'複数選択ですが、'
                        u'各 textFiled 内の何れかに、@ (at mark) '
                        u'を使用せずに実行しています。'
                        u'rename の実行はストップしました。rename proc 1.5-CBC'
                        .format(self.title
                                , YO_logger2.getLineNo()
                                )
                        )
                    # 追加7 ####################################################### end

                    # # 変換箇所5
                    # YO_logProcess.action('ERROR'
                    #                      , u'{}\n\t\t\tLine Number:{}\n'
                    #                        u'ストップ CBC\n'
                    #                        u'複数選択ですが、'
                    #                        u'各 textFiled 内の何れかに、@ (at mark) '
                    #                        u'を使用せずに実行しています。'
                    #                        u'rename の実行はストップしました。rename proc 1.5-CBC'
                    #                      .format(self.title
                    #                              , YO_logger2.getLineNo()
                    #                              )
                    #                      )

                    # message_warning(u'複数選択ですが、'
                    #                      u'各 textFiled 内の何れかに、@ (at mark) '
                    #                      u'を使用せずに実行しています。'
                    #                      u'rename の実行はストップしました。rename proc 1.5-CBC'
                    #                      )

                    pass
    # 共通な一連の関数のまとまり ############################################# end

    # イレギュラー対応用 ################################################### start
    # イレギュラー対応用変数を出力するための関数です。
    # ここでいうイレギュラーとは、「選択1っ、atMark 0、TextField関連が完全 の時」 を言います。
    # イレギュラー対応用変数 self.waiting_last_string (default: '') を予め出力
    # イレギュラー対応用変数 self.is_exists_forNCName (default: False) を予め出力
    # 選択1っ、atMark 0、TextField関連が完全 の時だけに対応しています。
    # @instance.declogger
    def renameFunction_inIrregularCases(self):
        u""" < イレギュラー対応用変数を出力するための関数 >

        ::

          選択1っ、atMark 0、TextField関連が完全 の時だけに対応
        """
        if len(self.selectionLists) == 1 \
                and self.atMark_count == 0 \
                and self.isSet_reqTxtFld\
                :
            self.selCompStrs_1st\
                , self.selCompStrs_2nd\
                , self.selCompStrs_3rd\
                , self.typ \
                = self.strCompsCheck_exe(self.selectionLists[0])
            # ##############################
            # print(u'<イレギュラー対応用>選択ノード名の構成\n\t'
            #       u'{}, {}, {}, {}'
            #       .format(self.selCompStrs_1st, self.selCompStrs_2nd
            #               , self.selCompStrs_3rd
            #               , self.typ)
            #       )
            # ##############################

            self.assemble_A, self.assemble_B\
                , self.assemble_C1, self.assemble_C2, self.assemble_C3 \
                = self.eachOneAssembled(self.strsDecompListsAll
                                        , self.selCompStrs_1st
                                        , self.selCompStrs_2nd
                                        , self.selCompStrs_3rd
                                        , 'A'
                                        )
            ##############################

            # 変換箇所5
            # YO_logProcess.action('DEBUG'
            #                      , u'{}\n\t\t\tLine Number:{}\n'
            #                        u'<イレギュラー対応用>TextField名の構成\n\t'
            #                        u'{}, {}, {}, {}, {}'
            #                      .format(self.title, YO_logger2.getLineNo()
            #                              , self.assemble_A, self.assemble_B
            #                              , self.assemble_C1, self.assemble_C2, self.assemble_C3
            #                              )
            #                      )

            # print(u'<イレギュラー対応用>TextField名の構成\n\t'
            #       u'{}, {}, {}, {}, {}'
            #       .format(self.assemble_A, self.assemble_B
            #       , self.assemble_C1, self.assemble_C2, self.assemble_C3)
            #       )

            ##############################

            strs_next_temp\
                = self.eachOneAssembled_combined_temp(self.assemble_A, self.assemble_B
                                                      , self.assemble_C1
                                                      , self.assemble_C2
                                                      , self.assemble_C3
                                                      )
            ##############################

            # 変換箇所5
            # YO_logProcess.action('DEBUG'
            #                      , u'{}\n\t\t\tLine Number:{}\n'
            #                        u'<イレギュラー対応用>TextField関連\n\t'
            #                        u'strs_next_temp : \n\t\t'
            #                        u'{}'
            #                      .format(self.title
            #                              , YO_logger2.getLineNo()
            #                              , strs_next_temp
            #                              )
            #                      )

            # print(u'<イレギュラー対応用>TextField関連\n\t'
            #       u'strs_next_temp : \n\t\t'
            #       u'{}'.format(strs_next_temp)
            #       )

            ##############################

            self.waiting_last_string = self.exceptCheck_patternX(strs_next_temp)
            ##############################

            # 変換箇所5
            # YO_logProcess.action('DEBUG'
            #                      , u'{}\n\t\t\tLine Number:{}\n'
            #                        u'<イレギュラー対応用>TextField関連\n\t'
            #                        u'TextField名の構成から判断された、待機している最終文字列 : \n\t\t'
            #                        u'{}'
            #                      .format(self.title
            #                              , YO_logger2.getLineNo()
            #                              , self.waiting_last_string
            #                              )
            #                      )

            # print(u'<イレギュラー対応用>TextField関連\n\t'
            #       u'TextField名の構成から判断された、待機している最終文字列 : \n\t\t'
            #       u'{}'.format(self.waiting_last_string)
            #       )

            ##############################

            isExist_verticalLine_sel = '|' in self.selectionLists[0]
            # ##############################
            # print(u'選択ノード関連\n\t'
            #       u'isExist_verticalLine_sel : \n\t\t'
            #       u'{}'.format(isExist_verticalLine_sel))
            # ##############################

            # if isExist_verticalLine_sel:
            #     ##############################
            #     print(u'選択ノード関連\n\t'
            #           u'選択ノード名は'
            #           # u'verticalLine を持っています。よって '
            #           u'unique ではありません。'
            #           u'相対的な名前 : \n\t\t'
            #           u'{}'.format(self.selectionLists[0].split('|')[-1])
            #           )
            #     ##############################
            # else:
            #     ##############################
            #     print(u'選択ノード関連\n\t'
            #           u'選択ノード名は'
            #           # u'verticalLine を持っていません。よって '
            #           u'unique です。'
            #           )
            #     ##############################

            # self.waiting_last_string が、
            # self.getObj リスト内に、
            # 重複した名前として既にあるかどうかを探しあて、存在の真偽を出力する メソッドの実行
            # False: 重複していない
            # True: 重複している 注意!
            self.is_exists_forNCName \
                = self.searchForDuplicateName(self.getObj, self.waiting_last_string)
            # ##############################
            # print(u'待機している最終文字列が、'
            #       u'予めシーン内の文字列リスト内に、重複して存在しているか否か : ')
            #
            # True: 重複している 注意!
            # if self.is_exists_forNCName:
            #     print(u'\t\t{}\n\t\t'
            #           u'重複しています。注意!'.format(self.is_exists_forNCName)
            #           )
            #
            # False: 重複していない
            # else:
            #     print(u'\t\t{}\n\t\t'
            #           u'重複していません。'.format(self.is_exists_forNCName)
            #           )
            # ##############################
    # イレギュラー対応用 ##################################################### end

    # rename操作 ######################################################### start
    # ###########################################
    # rename の核となるメソッドは、以下の計2つ。
    # proc2-main1. #
    #   start_executeCmd   ----  rename start code (共通)
    # proc2-main3. #
    #   renameMain_exe     ----  rename next code (共通)
    # ###########################################

    # mode で分岐させることを目的とした メソッド
    # proc2-main1. #
    # rename start code (共通)
    # mode によって途中の挙動を変えています
    # のちに実行されるメソッドは、 proc2-main3. renameMain_exe です
    # @instance.declogger
    def start_executeCmd(self, selects, mode, wordLists):
        u""" < mode で分岐させることを目的とした メソッド >

        ::

          proc2-main1.
            rename start code (共通)

          mode によって途中の挙動を変えています
          のちに実行されるメソッドは、 proc2-main3. renameMain_exe です

        #######################

        #.
            :param list[str] selects:
            :param int mode:
            :param list[str] wordLists:

        #######################
        """
        # 追加7 ####################################################### start
        self.scriptEditor2.append_default(u'## 継続中 ########## rename proc 2-1')
        # 追加7 ####################################################### end

        # print(u'## 継続中 ########## rename proc 2-1')

        self.selectionLists = selects
        # print(u'self.selectionLists: \n\t\t'
        #       u'{}'.format(self.selectionLists)
        #       )
        # self.mode = mode
        # self.wordListsSet_fromUI = wordLists
        strsDecompListsAll = self.waitingWordStrs_patternCheck_exe(wordLists)
        # print(u'strsDecompListsAll: \n\t\t'
        #       u'{}'.format(strsDecompListsAll)
        #       )
        # print(u'mode: \n\t\t'
        #       u'{}'.format(mode)
        #       )
        # print(mode, self.mode)
        ############
        # mode1 ####
        ############
        if mode == 1:  # A
            # 追加7 ####################################################### start
            self.scriptEditor2.append_default(u'継続 A : mode 1')
            # 追加7 ####################################################### end

            # print(u'継続 A : mode 1')

            # 以下の1行の実行は、様々なケースへの対応を想定した場合、精度があがりそう
            self.selectionLists\
                = self.checkAndDoLimitationOfUnderScore_forSlNode(self.selectionLists)
            # print(self.selectionLists)
        ############
        # mode0 ####
        ############
        elif mode == 0:  # B
            # 追加7 ####################################################### start
            self.scriptEditor2.append_default(u'継続 B : mode 0')
            # 追加7 ####################################################### end

            # print(u'継続 B : mode 0')

            # print(self.selectionLists)
        # print('koko')
        # print(mode, self.mode)
        # 追加11 ####################################################### start
        self.scriptEditor2.append_default(self.selectionLists)
        # 追加11 ####################################################### end
        # print(self.selectionLists)

        self.renameMain_exe(strsDecompListsAll)

    # rename の メイン メソッド
    # proc2-main3. #
    # rename next code (共通)
    # @instance.declogger
    def renameMain_exe(self, textLists, *args):
        u""" < rename の メイン メソッド >

        ::

          proc2-main3.
          rename next code (共通)

        #######################

        #.
            :param list[str] textLists:

        #######################
        """
        # 追加7 ####################################################### start
        self.scriptEditor2.append_default(u'## 継続中 ########## rename proc 2-3')
        # 追加7 ####################################################### end
        # print(u'## 継続中 ########## rename proc 2-3')

        # print(self.selectionLists)
        strsDecompListsAll = textLists
        # print(strsDecompListsAll)
        # for tFld_decomp_index in strsDecompListsAll:
        #     print(tFld_decomp_index)
        #     print('\n')
        # print(u'選択している全てのノード:{} \n'.format(self.selectionLists))
        # print('\n')
        counts = len(self.selectionLists)
        # print(counts)

        chars = []
        # self.selectionLists の個数分(counts)を、10進数から26進数へ変換し、出力しておく
        # 26進数へ変換メソッド 実行
        for count in range(counts):
            char = self.deciNum_to_26deciNum(count)  # 26進数へ変換メソッド 実行
            # print(char)
            chars.append(char)
        self.chars = chars

        # ##############################
        # print(u'一時的に抽出した..')
        # print(u'26進数の待機: {}'.format(self.chars))
        # ##############################

        # print('\n')
        # print('**')
        # print(self.selectionLists, self.chars)
        for selIndex, char in zip(self.selectionLists, self.chars):
            # print(selIndex, char)

            # 変換箇所5
            # YO_logProcess.action('INFO'
            #                      , u'{}\n\t\t\tLine Number:{}\n'
            #                        u'******** rename start.. '
            #                        u'************************************************'
            #                      .format(self.title, YO_logger2.getLineNo())
            #                      )

            # print('******** rename start.. '
            #       '************************************************'
            #       )
            # print('**')

            # ##############################
            # print(selIndex)
            # ##############################

            # print('**')
            # 選択されているオブジェクト名の文字列の構成を調べ出力する メソッド 実行
            self.selCompStrs_1st\
                , self.selCompStrs_2nd\
                , self.selCompStrs_3rd\
                , self.typ\
                = self.strCompsCheck_exe(selIndex)
            # print('*')

            # ##############################
            # print(self.selCompStrs_1st, self.selCompStrs_2nd, self.selCompStrs_3rd, self.typ)
            # # print(type(self.selCompStrs_1st), type(self.selCompStrs_2nd)
            # #       , type(self.selCompStrs_3rd), type(self.typ))
            # ##############################

            # print('**')
            # print(strsDecompListsAll)
            # print(char)
            # 各 textField の組み立てを行い、各々を出力する メソッド 実行
            self.assemble_A, self.assemble_B\
                , self.assemble_C1, self.assemble_C2, self.assemble_C3\
                = self.eachOneAssembled(strsDecompListsAll
                                        , self.selCompStrs_1st
                                        , self.selCompStrs_2nd
                                        , self.selCompStrs_3rd
                                        , char
                                        )

            # ##############################
            # print(self.assemble_A, self.assemble_B
            #       , self.assemble_C1, self.assemble_C2, self.assemble_C3
            #       )
            # ##############################

            # いったんすべて連結し、出力する メソッド 実行
            temp_strs = self.eachOneAssembled_combined_temp(self.assemble_A
                                                            , self.assemble_B
                                                            , self.assemble_C1
                                                            , self.assemble_C2
                                                            , self.assemble_C3
                                                            )
            self.char = char
            # print('***')
            # 仮に連結し終えた待機文字列

            # ##############################
            # print(u'仮に連結し終えた待機文字列 is \n\t{}'.format(temp_strs))
            # ##############################

            # print(self.mode)
            # print('****')
            # ちょっと整理...
            # 余分なアンダースコアーやNoneがあれば除去し、出力する メソッド 実行
            strs_final = self.exceptCheck_patternX(temp_strs)  # strs_final:最終文字列(候補名)

            # ##############################
            # print(u'整理した結果、最終文字列(候補名) is \n\t{}'.format(strs_final))
            # ##############################

            if len(strs_final) == 0:  # 5
                # 変換箇所5
                # YO_logProcess.action('WARNING'
                #                      , u'{}\n\t\t\tLine Number:{}\n'
                #                        u'ストップ\n'
                #                        u'各 textField への文字列が設定されていません。'
                #                        u'rename の実行はストップしました。rename proc 2-3 5'
                #                      .format(self.title, YO_logger2.getLineNo())
                #                      )

                # message_warning(u'各 textField への文字列が設定されていません。'
                #                      u'rename の実行はストップしました。rename proc 2-3 5'
                #                      )

                pass
            else:
                # ##############################
                # print(u'選択したノード を 候補名 で rename しようとしています。1')
                # print('\t{} --> {}'.format(selIndex, strs_final))
                # ##############################

                # strs_final(新規候補名)に対しての真偽
                # 作成された候補名が、重複名として既にシーン内にあるかどうかの真偽出力メソッド 実行
                # 作成された候補名 : strs_final
                # 対象のリスト(シーン内 DG name 全リスト) : self.getObj lists
                self.is_exists_forNCName = self.searchForDuplicateName(self.getObj, strs_final)
                # print('***')

                # 変換箇所5
                # YO_logProcess.action('DEBUG'
                #                      , u'{}\n\t\t\tLine Number:{}\n'
                #                        u'***'
                #                      .format(self.title, YO_logger2.getLineNo())
                #                      )

                # print(self.is_exists_forNCName)  # True or False

                if self.is_exists_forNCName:  # 1
                    # ##############################
                    # print(u'******** 候補名 {} は、'
                    #       u'すでにシーン内に重複名としてあります。rename proc 2-3 1'
                    #       .format(strs_final)
                    #       )
                    # ##############################

                    pass

                # ##############################
                # print(selIndex, strs_final)
                # ##############################

                if self.is_exists_forNCName:
                    while True:
                        if not self.is_exists_forNCName:  # 2
                            # 追加7 ####################################################### start
                            self.scriptEditor2.append_default('*****')
                            # 追加7 ####################################################### end

                            # print('*****')

                            # print(self.is_exists_forNCName)  # True or False
                            if not self.is_exists_forNCName:

                                ##############################

                                # 変換箇所5
                                # YO_logProcess.action('INFO'
                                #                      , u'{}\n\t\t\tLine Number:{}\n'
                                #                        u'******** 候補名 {} は、'
                                #                        u'シーン内ではユニークな名前と判断されました。2'
                                #                      .format(self.title
                                #                              , YO_logger2.getLineNo()
                                #                              , strs_final
                                #                              )
                                #                      )

                                # print(u'******** 候補名 {} は、'
                                #       u'シーン内ではユニークな名前と判断されました。2'
                                #       .format(strs_final)
                                #       )

                                ##############################

                                pass
                            # cmds.select(tgl = True)
                            cmds.rename(selIndex, strs_final)
                            # print('************************')
                            # print('* current obj lists ...*')
                            # print('************************')
                            currentObjLists = self.getDGAll_fromScene()
                            # print(currentObjLists)
                            self.getObj = currentObjLists  # self.getObj の更新

                            ##############################

                            # 変換箇所5
                            # YO_logProcess.action('INFO'
                            #                      , u'{}\n\t\t\tLine Number:{}\n'
                            #                        u'*****************************'
                            #                        u'******** rename done '
                            #                        u'************************************************rename proc 2-3 2'
                            #                        u'\n'
                            #                      .format(self.title
                            #                              , YO_logger2.getLineNo()
                            #                              )
                            #                      )

                            # print('*****************************')
                            # print('******** rename done '
                            #       '************************************************rename proc 2-3 2'
                            #       )
                            # print('\n')

                            ##############################

                            break
                        elif self.is_exists_forNCName:
                            if selIndex == strs_final:  # 3
                                # print('******')

                                # 変換箇所5
                                # YO_logProcess.action('DEBUG'
                                #                      , u'{}\n\t\t\tLine Number:{}\n'
                                #                        u'******'
                                #                      .format(self.title
                                #                              , YO_logger2.getLineNo()
                                #                              )
                                #                      )

                                # print(self.is_exists_forNCName)

                                # ##############################
                                # print(u'しかし..')
                                # print(u'******** 候補名 {} は、'
                                #       u'シーン内ではユニークな名前です。rename proc 2-3 3'
                                #       .format(strs_final)
                                #       )
                                # ##############################

                                # 同階層のときに発生しやすいパターン
                                # e.g.) edfv_jt_A --> edfv_jt_A <match!>
                                # e.g.) group1|edfv_jt_A --> edfv_jt_A <un match!>

                                ##############################

                                # 変換箇所5
                                # YO_logProcess.action('INFO'
                                #                      , u'{}\n\t\t\tLine Number:{}\n'
                                #                        u'******** 変更は行いませんでした。'
                                #                      .format(self.title
                                #                              , YO_logger2.getLineNo()
                                #                              )
                                #                      )

                                # print(u'******** 変更は行いませんでした。')

                                ##############################

                                # print(selIndex, strs_final)
                                # cmds.rename(selIndex, strs_final)  # rename せずにそのまま
                                # print('************************')
                                # print('* current obj lists ...*')
                                # print('************************')
                                currentObjLists = self.getDGAll_fromScene()
                                # print(currentObjLists)
                                self.getObj = currentObjLists  # self.getObj の更新

                                ##############################

                                # 変換箇所5
                                # YO_logProcess.action('DEBUG'
                                #                      , u'{}\n\t\t\tLine Number:{}\n'
                                #                        u'******** rename done '
                                #                        u'************************************************rename proc 2-3 3'
                                #                      .format(self.title
                                #                              , YO_logger2.getLineNo()
                                #                              )
                                #                      )

                                # print('******** rename done '
                                #       '************************************************rename proc 2-3 3'
                                #       )
                                # print('\n')

                                ##############################

                                break
                            elif selIndex != strs_final:  # 4
                                # print('******')
                                # print(self.is_exists_forNCName)

                                # ##############################
                                # print('******** rename CANCEL, next.. '
                                #       '************************\n\n'
                                #       )
                                # print('******** next.. '
                                #       '************************'
                                #       )
                                # ##############################

                                nextChar = self.nextChar_fromChar(self.char)

                                ##############################

                                # 変換箇所5
                                # YO_logProcess.action('DEBUG'
                                #                      , u'{}\n\t\t\tLine Number:{}\n'
                                #                        u'next..'
                                #                      .format(self.title
                                #                              , YO_logger2.getLineNo()
                                #                              )
                                #                      )

                                # print('next..')
                                # print(u'26進数の待機: {}'.format(nextChar))
                                # print(nextChar)

                                ##############################

                                self.assemble_A, self.assemble_B\
                                    , self.assemble_C1, self.assemble_C2, self.assemble_C3\
                                    = self.eachOneAssembled(strsDecompListsAll
                                                            , self.selCompStrs_1st
                                                            , self.selCompStrs_2nd
                                                            , self.selCompStrs_3rd
                                                            , nextChar
                                                            )

                                # ##############################
                                # print(self.assemble_A, self.assemble_B
                                #       , self.assemble_C1, self.assemble_C2, self.assemble_C3, self.typ)
                                # ##############################

                                # 各 textField の待機文字列から分解し整理し終えた文字列に対し、
                                # 組み立て終えた、各々を、 いったんすべて連結し、出力する メソッド 実行
                                strs_next_temp \
                                    = self.eachOneAssembled_combined_temp(self.assemble_A
                                                                          , self.assemble_B
                                                                          , self.assemble_C1
                                                                          , self.assemble_C2
                                                                          , self.assemble_C3
                                                                          )

                                # ##############################
                                # print(strs_next_temp)
                                # ##############################

                                # textField の待機文字列から分解・整理・連結 し終えた仮の待機文字列に対し、
                                # 余分なアンダースコアーやNoneが付随してしまう事がある為、それを避けるため、
                                # あれば除去し、出力する メソッド 実行
                                # (改訂)
                                strs_final = self.exceptCheck_patternX(strs_next_temp)

                                # ##############################
                                # print(strs_final)
                                # ##############################

                                # 次の最終文字列(次の候補名)

                                # ##############################
                                # print(u'次の最終文字列(次の候補名) is \n\t{}'.format(strs_final))
                                # print(u'選択したノード を 候補名 で rename しようとしています。rename proc 2-3 4')
                                # ##############################

                                ##############################
                                # 追加7 ####################################################### start
                                self.scriptEditor2.append_default('\t{} --> {}'.format(selIndex, strs_final))
                                # 追加7 ####################################################### end

                                # print('\t{} --> {}'.format(selIndex, strs_final))

                                ##############################

                                # 再度、
                                # strs_final(新規候補名)に対しての真偽
                                # 作成された候補名が、重複名として既にシーン内にあるかどうかの
                                # 真偽出力メソッド 実行
                                # 作成された候補名 : strs_final
                                # 対象のリスト(シーン内 DG name 全リスト) : self.getObj lists
                                self.is_exists_forNCName = self.searchForDuplicateName(
                                    self.getObj, strs_final)
                                # print('********')
                                # print(self.is_exists_forNCName)  # ここが Falseになるまで繰り返す
                                if self.is_exists_forNCName:  # 2

                                    # ##############################
                                    # print(u'******** 候補名 {} は、'
                                    #       u'すでにシーン内に重複名としてあります。rename proc 2-3 2'
                                    #       .format(strs_final)
                                    #       )
                                    # ##############################

                                    pass
                                self.char = nextChar
                                # self.char の更新  # print('********************')
                                # print('* old obj lists ...*')
                                # print('********************')
                                # print(self.getObj)

                                # ##############################
                                # print('*****************************')
                                # ##############################

                                # print(selIndex, strs_final)
                else:  # 0
                    # print('*************')
                    # print(self.is_exists_forNCName)
                    if not self.is_exists_forNCName:

                        # ##############################
                        # print(u'******** 候補名 {} は、'
                        #       u'シーン内ではユニークな名前と判断されました。rename proc 2-3 0'
                        #       .format(strs_final)
                        #       )
                        # ##############################

                        pass
                    cmds.rename(selIndex, strs_final)

                    ##############################
                    # 追加7 ####################################################### start
                    self.scriptEditor2.append_default('\t{} --> {}'.format(selIndex, strs_final))
                    # 追加7 ####################################################### end

                    # print('\t{} --> {}'.format(selIndex, strs_final))

                    ##############################

                    ##############################
                    # print('****')

                    # 変換箇所5
                    # YO_logProcess.action('DEBUG'
                    #                      , u'{}\n\t\t\tLine Number:{}\n'
                    #                        u'****'
                    #                        u'******** 候補名 {} は、'
                    #                        u'シーン内ではユニークな名前と判断されました。rename proc 2-3 0'
                    #                      .format(self.title
                    #                              , YO_logger2.getLineNo()
                    #                              , strs_final
                    #                              )
                    #                      )

                    # print(u'******** 候補名 {} は、'
                    #       u'シーン内ではユニークな名前と判断されました。rename proc 2-3 0'
                    #       .format(strs_final)
                    #       )

                    ##############################

                    # 変換箇所5
                    # YO_logProcess.action('INFO'
                    #                      , u'{}\n\t\t\tLine Number:{}\n'
                    #                        u'*****************************'
                    #                        u'******** rename done '
                    #                        u'************************************************'
                    #                        u'rename proc 2-3 0'
                    #                        u'\n'
                    #                      .format(self.title, YO_logger2.getLineNo())
                    #                      )

                    # print('*****************************')
                    # print('******** rename done '
                    #       '************************************************'
                    #       'rename proc 2-3 0'
                    #       '\n'
                    #       )

    # rename操作 ########################################################### end
    # 「rename の核となる コマンド群」 ###################################################### end


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
