# -*- coding: utf-8 -*-

u"""
YO_createSpaceNode3_Modl.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -6.0-
:Date: 2024/05/222

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PyMel version: 1.2.0
    - PySide2 version: 5.15.2

-リマインダ-
    done: 2024/05/22
        - 変更8 と 追加8 と 新規8
            - 概要: ユニークでない名前 のノードの space 作成におけるバグ修正 その2
            - 詳細:
                ::

                    +   def setOfCommonFunctions4(self, wordLists):
                            ...
                            if len(self.selectionLists) == 0:
                                ...
                            else:
                                ...
                                # 追加8 ####################################################### start
                                parentList = []
                                for selIndex in self.selectionLists:
                                    cmds.select(selIndex, r = True)
                                    cmds.pickWalk(direction = 'up')
                                    parent = cmds.ls(sl = True)[0]
                                    parentList.append(parent)
                                # print(f'parentList: {parentList}')
                                # 追加8 ####################################################### end
                                ...
                                # 変更7, 変更8
                                # 所定の位置まで格納し終わる
                                for count, (spaceNodeInfo,
                                            selIndex, parentIndex
                                            ) in enumerate(
                                    zip(spaceNodeInfoLists, self.selectionLists, parentList)
                                    ):
                                    ...
                                    if spaceNodeInfo[1] != u'None':
                                        ...
                                        if '|' in selIndex:
                                            # 最後の|を境に文字列を2分割し、最後の要素を取得します
                                            first_part = selIndex.rsplit('|', 1)[0]
                                            last_part = selIndex.rsplit('|', 1)[1]
                                            last_part = last_part + 'Temp'
                                            ...
                                            temp = spaceNodeInfo[0].replace(last_part, '')
                                            ...
                                            resultA = temp.replace('_', '')
                                            ...
                                            temp1 = cmds.parent(spaceNodeInfo[0], first_part)
                                            temp2 = cmds.parent(selIndex, spaceNodeInfo[0])
                                            # print(temp1[0], temp2[0])
                                            resultB = temp1[0].replace(temp, resultA)
                                            ...
                                            cmds.rename(spaceNodeInfo[0], resultB)
                                            spaceNodes[count] = resultB  # 該当のインデックスのみ仮名のノードで置き換える
                                        else:
                                            if '|' in parentIndex:
                                                cmds.parent(spaceNodeInfo[0], parentIndex)
                                                cmds.parent(selIndex, spaceNodeInfo[0])
                                            else:
                                                cmds.parent(spaceNodeInfo[0], spaceNodeInfo[1])
                                                cmds.parent(selIndex, spaceNodeInfo[0])
                                    ...
                                    elif spaceNodeInfo[1] == u'None':
                                        ...
                                        cmds.parent(selIndex, spaceNodeInfo[0])
        version = '-6.0-'

    done: 2024/05/20
        - 変更7 と 追加7 と 新規7
            - 概要: ユニークでない名前 のノードの space 作成におけるバグ修正
            - 詳細:
                ::

                    +   def setOfCommonFunctions4(self, wordLists):
                            ...
                            if len(self.selectionLists) == 0:
                                ...
                            else:
                                ...
                                # 変更7
                                # 所定の位置まで格納し終わる
                                for count, (spaceNodeInfo,
                                            selIndex) in enumerate(zip(spaceNodeInfoLists,
                                                                       self.selectionLists)
                                                                   ):
                                    # print(spaceNodeInfo, selIndex)
                                    if spaceNodeInfo[1] != u'None':
                                        # # 1つでも|があれば、必ず、最後の|を境にして、最後の分割文字列を取得
                                        if '|' in selIndex:
                                            # 最後の|を境に文字列を2分割し、最後の要素を取得します
                                            first_part = selIndex.rsplit('|', 1)[0]
                                            last_part = selIndex.rsplit('|', 1)[1]
                                            last_part = last_part + 'Temp'
                                            ...
                                            temp = spaceNodeInfo[0].replace(last_part, '')
                                            ...
                                            resultA = temp.replace('_', '')
                                            ...
                                            temp1 = cmds.parent(spaceNodeInfo[0], first_part)
                                            temp2 = cmds.parent(selIndex, spaceNodeInfo[0])
                                            ...
                                            resultB = temp1[0].replace(temp, resultA)
                                            ...
                                            cmds.rename(spaceNodeInfo[0], resultB)
                                            ...
                                            spaceNodes[count] = resultB  # 該当のインデックスのみ仮名のノードで置き換える
                                            ...
                                    else:
                                        ...
                                ...
        version = '-5.0-'

    done: 2024/05/13~2024/05/15
        - 変更6 と 追加6
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
                - 定義箇所:
                    本来は、
                        あらかじめ カスタムの Script Editor2 モジュール
                            を定義するのですが、
                                当モジュール自体が、
                                    親クラスである、
                                        from ..renameTool.YO_renameTool5_Modl import RT_Modl
                                    を既に import 済であり、
                                その YO_renameTool5_Modl モジュールに、
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
                    クラス継承基は、YO_renameTool5_Modl(RT_Modl) です
                    つまり、YO_renameTool5_Modl(RT_Modl) から再利用しているため、
                        ここでは不必要なだけであり。
                            実際には、YO_renameTool5_Modl(RT_Modl) から読み込まれており、
                                しっかりと、使用されています。
                    ::

                        +   def __init__(self, _model):
                                ...
                                # 追加6 ########################################################### start
                                # クラス継承元 YO_renameTool5_Modl(RT_Modl) のメソッドを 再利用しているので、ここでは不必要 です
                                # self.scriptEditor2_chunk1()
                                # クラス継承元 YO_renameTool5_Modl(RT_Modl) のメソッドを 再利用しているので、ここでは不必要 です
                                # self.scriptEditor2_chunk2()
                                # 追加6 ########################################################### end

                        +   # 追加6 ########################################################### start
                            # クラス継承元 YO_renameTool5_Modl(RT_Modl) のメソッドを 再利用しているので、ここでは不必要 です
                            # def scriptEditor2_chunk1(self):
                            #     pass

                            # クラス継承元 YO_renameTool5_Modl(RT_Modl) のメソッドを 再利用しているので、ここでは不必要 です
                            # def scriptEditor2_chunk2(self):
                            #     pass

                            # クラス継承元 YO_renameTool5_Modl(RT_Modl) のメソッドを 再利用しているので、ここでは不必要 です
                            # def create_scriptEditor2_and_show(self):
                            #     pass

                            # クラス継承元 YO_renameTool5_Modl(RT_Modl) のメソッドを 再利用しているので、ここでは不必要 です
                            # @Slot()
                            # def on_scriptEditor2_closed(self):
                            #     pass
                            # 追加6 ########################################################### end
                - 置換した箇所: 以下のように、置き換えます
                    先ず2箇所
                    ::

                        +   def ui_executeBtnCmd(self, *args):
                                ...
                                # 追加6 ####################################################### start
                                check_string = 'check'
                                ...
                                elif state == 'open':
                                        print('open済、再利用')
                                        self.scriptEditor2.append_default('open済、再利用')
                                # 追加6 ####################################################### end
                                ...

                        +   def exe(self, *args):
                                ...
                                # 追加6 ####################################################### start
                                check_string = 'check'
                                ...
                                elif state == 'open':
                                        print('open済、再利用')
                                        self.scriptEditor2.append_default('open済、再利用')
                                # 追加6 ####################################################### end
                                ...
                    その他、多数ある箇所
                    ::

                        +   # 追加6 ########################################################### start
                            self.scriptEditor2.append_default(...)
                            # 追加6 ########################################################### end

                        +   # 追加6 ########################################################### start
                            self.scriptEditor2.append_error(...)
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

                  -     from YO_utilityTools.lib import ...
                  +     from ..lib import ...

                  -     from YO_utilityTools.renameTool.YO_renameTool5_Modl import RT_Modl
                  +     from ..renameTool.YO_renameTool5_Modl import RT_Modl

        version = '-3.1-'

    done: 2023//10/25
        汎用箇所を、モジュールとして読み込みに変更

        version = '-3.0-'

    done: 2023/10/09
        - 不具合修正1
            - 詳細: 複数選択で、UIモードは問題ないが、コマンドモードで修正

        version = '-2.8-'

    done: 2023/10/06
        - 変更箇所2(追加3)
            - 概要: 選択実行したノード全てを、改めて全選択するための選択ノード名リスト格納宣言
            - 詳細: 以下参照
                - baseとなる派生元(renameTool5)からの、以下関数・変数を 再利用しています
                .. Note::
                    実際には当コード内では、新規追加定義の記述は不要ですが、以下抜粋で列挙します

                - 以下、base(renameTool5)からの派生を抜粋し列挙
                    ::

                      def __init__(self):
                        ...
                        # base から継承で再利用しているので不要
                        # self.constructor_chunk_addA()  # コンストラクタのまとまりaddA # その他の定義2
                        ...

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

                - 当コード内で、実際に必要となる新規追加定義の記述は以下
                    ::

                      def ui_executeBtnCmd(self, *args):
                        ...

                      def exe(self, mode = 0, n = None, nodeType = ''):
                        ...

                      両関数の必要な箇所へ...以下を追加

                      +        # 追加3
                               # 派生元 renameTool5 独自の 選択ノードの明示に使用
                               self.initSelectionNodeUUIDLists.__init__()  # 常に初期化で空にする
                               self.initSelectionNode_storeUUID(self.selectionLists)

                      +        # 追加3
                               # かなり初期の段階で選択を実行します
                               # b/c): 派生元 renameTool5 独自の 選択ノードの明示に使用
                               cmds.select(cl = True)
                               self.initSelectionNode_reSelect(self.initSelectionNodeUUIDLists)

        version = '-2.7-'

    done: 2023/10/06
        コメントアウト記述を一旦整理

        version = '-2.6-'

    done: 2023/09/21
        - python2系 -> python3系 変換
            - 変換箇所1
                - 概要: unicode関連
                    - 対象箇所
                        - # 分析2 n ###
                        - # 分析3 typ ###
                - 詳細: 以下参照
                ::

                  -
                            def analysis_strs_fromCmd4(self, mode, n, typ):
                                ...
                                #############################################
                                # 分析2 n ###  リスト文字列を一旦文字列に変換・分析し、リスト文字列として返す
                                # あらかじめ用意されている文字列, 'n = [u'***'...],'から、必要な文字列 *** を抽出する
                                ...
                                patternN = re.compile(r'u\'(?P<ptnNStr>.*?)\'')  # 変更対象箇所
                                ...
                                #############################################
                                # 分析3 typ ###
                                # あらかじめ用意されている文字列, 'nodeType = u'***','から、必要な文字列 *** を抽出する
                                ...
                                patternTyp = re.compile(r'u\'(?P<ptnTypStr>.*?)\'')  # 変更対象箇所
                                ...

                  +
                            def analysis_strs_fromCmd4(self, mode, n, typ):
                                ...
                                #############################################
                                # 分析2 n ###  リスト文字列を一旦文字列に変換・分析し、リスト文字列として返す
                                # あらかじめ用意されている文字列, 'n = [u'***'...],'から、必要な文字列 *** を抽出する
                                ...
                                patternN = re.compile(r'\'(?P<ptnNStr>.*?)\'')  # 変更
                                ...
                                #############################################
                                # 分析3 typ ###
                                # あらかじめ用意されている文字列, 'nodeType = u'***','から、必要な文字列 *** を抽出する
                                ...
                                patternTyp = re.compile(r'\'(?P<ptnTypStr>.*?)\'')  # 変更
                                ...

        version = '-2.0-'

    done: 2023/5/19
        - 追加1
            - 、u'underScoresCount1'判別時に、
                文字列を split した 2nd の文字列の先頭文字の大小で、識別子なのかそうでないのかを
                    判別することを、space node 作成時に反映

        version = '-1.1-'

    done: 2023/04/17~2023/05/08
        新規

        version = '-1.0-'
"""

# 標準ライブラリ
import re
# from functools import partial  # partial 利用時は、最後の引数に、*args 要時あり
# from distutils.util import strtobool
# import pprint

# サードパーティライブラリ #########################################################
import maya.cmds as cmds
# from pymel import core as pm
# import maya.OpenMaya as om

# ローカルで作成したモジュール ######################################################
# basic_configuration_for_derivation(派生用の基本構成)
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
# from YO_utilityTools.YO_optionVar import upDateOptionVarsDictCmd  # オプション変数をdict操作し、更新をかける関数
# from YO_utilityTools.YO_optionVar import upDateOptionVarCmd  # オプション変数に更新をかける関数
# 汎用ライブラリー の使用 ################################################################## end

# mvc_model_module_that_become_derived_basis(派生基となるMVCモデルモジュール)
from ..renameTool.YO_renameTool5_Modl import RT_Modl


class CSpaceNode_Modl(RT_Modl):
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
                .. note::
                  proc1. # と便宜的に述べています。
                  初めに、カレントの、textField 文字列を抜き出します。
                  mainは
                    def ui_executeBtnCmd(self, *args):
                        ...
                  次に、後の proc1.5. # へ移ります。

            - 5. スクリプトベースコマンド入力への対応
                .. note::
                  proc1. # と便宜的に述べています。
                  初めに、analysis_strs_fromCmd4 メソッドを利用して、必要な文字列を抜き出します。
                  mainは
                    def exe(self, mode = 0, n = None, nodeType = ''):
                        ...
                  次に、後の proc1.5. # へ移ります。

            - 「spaceNode 作成と、naming の核となる コマンド群」
                - 共通な一連の関数のまとまり
                    .. note::
                      proc1.5. #
                        def setOfCommonFunctions4(self, wordLists):
                          ...
                      proc1.5. # と便宜的に述べていますが、
                        必ず、この proc1.5. # を経ています。
                            イレギュラー対応 はここで行っています。
                      次に、proc2.1. #
                        type1, type2 どちらかへ偏移します。
                      そして、proc2.2. #
                        最後に、共通な naming の操作を行っています。

                - spaceNode作成
                    .. note::
                      proc2.1. spaceNode作成
                        はここで行われています。
                      type1, type2 と分岐します。

    ######
    """
    def __init__(self):
        super(CSpaceNode_Modl, self).__init__()  # RT_Modl からの派生宣言

        # base から継承で、同じ内容だが新規扱い(override)
        self.constructor_chunk1()  # コンストラクタのまとまり1 # パッケージ名等の定義
        # base から継承で、同じ内容だが新規扱い(override)
        self.constructor_chunk2()  # コンストラクタのまとまり2 # タイトル等の定義

        # base から継承で再利用しているので不要
        # self.constructor_chunk3()  # コンストラクタのまとまり3 # その他の定義
        # self.constructor_chunk4()  # コンストラクタのまとまり4 # UIコントロールに関わる定義

        # 完全に新規
        self.constructor_chunk5()  # コンストラクタのまとまり5 # UIコントロールに関わる定義の追加

        # 追加2
        # 完全に新規
        self.constructor_chunk6()  # コンストラクタのまとまり6 # その他の定義

        # base から継承 override 変更 (独自に定義しなおして上書き)
        self.settingOptionVar()  # コンストラクタのまとまりA # optionVar のセッティング
        # base から継承 override 変更 (独自に定義しなおして上書き)
        self.startOptionVarCmd()  # コンストラクタのまとまりB # optionVar の初期実行コマンド

        # self.options = pm.optionVar  # type: # OptionVarDict
        # self.options = upDateOptionVarsDictCmd()  # type: # dict

        # 追加
        self.constructor_chunk_addB_uuid()  # コンストラクタのまとまりaddB # uuid格納用

        # 追加6 ########################################################### start
        # クラス継承元 YO_renameTool5_Modl(RT_Modl) のメソッドを 再利用しているので、ここでは不必要 です
        # self.scriptEditor2_chunk1()
        # クラス継承元 YO_renameTool5_Modl(RT_Modl) のメソッドを 再利用しているので、ここでは不必要 です
        # self.scriptEditor2_chunk2()
        # 追加6 ########################################################### end

    # 追加6 ########################################################### start
    # クラス継承元 YO_renameTool5_Modl(RT_Modl) のメソッドを 再利用しているので、ここでは不必要 です
    # def scriptEditor2_chunk1(self):
    #     pass

    # クラス継承元 YO_renameTool5_Modl(RT_Modl) のメソッドを 再利用しているので、ここでは不必要 です
    # def scriptEditor2_chunk2(self):
    #     pass

    # クラス継承元 YO_renameTool5_Modl(RT_Modl) のメソッドを 再利用しているので、ここでは不必要 です
    # def create_scriptEditor2_and_show(self):
    #     pass

    # クラス継承元 YO_renameTool5_Modl(RT_Modl) のメソッドを 再利用しているので、ここでは不必要 です
    # @Slot()
    # def on_scriptEditor2_closed(self):
    #     pass
    # 追加6 ########################################################### end

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
        self.bgcGray = [0.5, 0.5, 0.5]  # list of float

        self.current_nodeType = str  # 'locator' or 'null' or 'joint'

        self.typ_fromCmd = str  # 'locator' or 'null' or 'joint'

    # 追加2
    # 完全に新規
    # コンストラクタのまとまり6 # その他の定義
    def constructor_chunk6(self):
        u""" < コンストラクタのまとまり6 # その他の定義 です >

        ::

          追加2
          完全に新規

        #######################
        """
        self.typRecordList = []

    # 追加
    # コンストラクタのまとまりaddA # uuid格納用
    def constructor_chunk_addB_uuid(self):
        u""" < コンストラクタのまとまりaddB # uuid格納用 です >

        ::

          追加
          独自の 選択ノードの明示に使用
        """
        # 格納用リスト宣言
        self.initSelectionNodeUUIDListsB = yo_uuid.initSelectionNodeUUIDLists

    # base から継承 override 変更 (独自に定義しなおして上書き)
    # コンストラクタのまとまりA # optionVar のセッティング
    def settingOptionVar(self):
        u""" < コンストラクタのまとまりA # optionVar のセッティング です >

        ::

          base から継承 override 変更 (独自に定義しなおして上書き)

        #######################
        """
        # dict  # range is 6 + # range is 1
        # key:   [type(str)
        # , type(str), type(str), type(str), type(str), type(str)  # range is 6
        # , type(str)  # range is 1
        # ]
        # value: [type(str)
        # , type(str), type(str), type(str), type(str), type(str)  # range is 6
        # , type(str)  # range is 1
        # ]
        self.opVar_dictVal_dflt_list = ['mode1'
            , '~', '~[Space]', '~', '', ''
                                        ]  # range is 6
        # value: [type(str)
        #          , type(str), type(str), type(str), type(str), type(str)
        #         ]  # range is 6

        # add node type
        self.opVar_dictVal_dflt_list_addCSpaceNode = ['locator']  # range is 1('locator' or 'null' or 'joint')
        # value: [type(str)]  # range is 1

        # OptionVar DATA naming ########################################################### start
        # save settings menu により、maya optionVar への 辞書登録を実施する準備です
        # dict  # range is 6 + # range is 1
        # key:   [type(str)
        # , type(str), type(str), type(str), type(str), type(str)  # range is 6
        # , type(str) # range is 1
        # ]
        # value: [type(str)
        # , type(str), type(str), type(str), type(str), type(str)  # range is 6
        # , type(str) # range is 1
        # ]

        # range is 6
        self.optionVar01_mode_key = self.title + self.underScore + 'rdBtn_text'  # type: str
        self.optionVar01_tFld_key = self.title + self.underScore + 'txtFldA1_text'  # type: str
        self.optionVar02_tFld_key = self.title + self.underScore + 'txtFldB1_text'  # type: str
        self.optionVar03_tFld_key = self.title + self.underScore + 'txtFldC1_text'  # type: str
        self.optionVar04_tFld_key = self.title + self.underScore + 'txtFldC2_text'  # type: str
        self.optionVar05_tFld_key = self.title + self.underScore + 'txtFldC3_text'  # type: str

        # range is 1
        self.optionVar01_nTyp_key = self.title + self.underScore + 'opMnuA_str'  # type: str
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
        # 「"YO_createSpaceNode3_rdBtn_text"というkeyが初めて実行されてるから無いよ！」
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
        # 「"YO_createSpaceNode3_txtFldA1_text"というkeyが初めて実行されてるから無いよ！」
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
        # 「"YO_createSpaceNode3_txtFldB1_text"というkeyが初めて実行されてるから無いよ！」
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
        # 「"YO_createSpaceNode3_txtFldC1_text"というkeyが初めて実行されてるから無いよ！」
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
        # 「"YO_createSpaceNode3_txtFldC2_text"というkeyが初めて実行されてるから無いよ！」
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
        # 「"YO_createSpaceNode3_txtFldC2_text"というkeyが初めて実行されてるから無いよ！」
        # というエラーが出るのでそれを回避しています
        # #######################
        if getOptionVarCmd(self.optionVar05_tFld_key) is None:  # set default
            setOptionVarCmd(self.optionVar05_tFld_key, self.opVar_dictVal_dflt_list[5])
            # self.options[self.optionVar05_tFld_key] = self.opVar_dictVal_def_list[5]  # dict type(value): str

        # add node type
        self.cOpMnu_nodeType = None  # type: pm.optionMenu
        # #######################
        # 補足 #
        # 初めてmayaで実行すると、optionVar は辞書なので
        # 「"YO_createSpaceNode3_opMnuA_str"というkeyが初めて実行されてるから無いよ！」
        # というエラーが出るのでそれを回避しています
        # #######################
        if getOptionVarCmd(self.optionVar01_nTyp_key) is None:  # set default
            setOptionVarCmd(self.optionVar01_nTyp_key, self.opVar_dictVal_dflt_list_addCSpaceNode[0])
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
        # self.options へ ["YO_createSpaceNode3_rdBtn_text"] を保存
        getSel_fromRdBtn = self.cmnModeRdBtnClcton.getSelect()
        # self.options[self.optionVar01_mode_key] = getSel_fromRdBtn
        setOptionVarCmd(self.optionVar01_mode_key, getSel_fromRdBtn)

        # tFld_key A1
        # self.options へ ["YO_createSpaceNode3_txtFldA1_text"] を保存
        getTxt_fromTxtFldA1 = self.cmnTxtFld_A1.getText()
        # self.options[self.optionVar01_tFld_key] = getTxt_fromTxtFldA1
        setOptionVarCmd(self.optionVar01_tFld_key, getTxt_fromTxtFldA1)

        # tFld_key B1
        # self.options へ ["YO_createSpaceNode3_txtFldB1_text"] を保存
        getTxt_fromTxtFldB1 = self.cmnTxtFld_B1.getText()
        # self.options[self.optionVar02_tFld_key] = getTxt_fromTxtFldB1
        setOptionVarCmd(self.optionVar02_tFld_key, getTxt_fromTxtFldB1)

        # tFld_key C1
        # self.options へ ["YO_createSpaceNode3_txtFldC1_text"] を保存
        getTxt_fromTxtFldC1 = self.cmnTxtFld_C1.getText()
        # self.options[self.optionVar03_tFld_key] = getTxt_fromTxtFldC1
        setOptionVarCmd(self.optionVar03_tFld_key, getTxt_fromTxtFldC1)

        # tFld_key C2
        # self.options へ ["YO_createSpaceNode3_txtFldC2_text"] を保存
        getTxt_fromTxtFldC2 = self.cmnTxtFld_C2.getText()
        # self.options[self.optionVar04_tFld_key] = getTxt_fromTxtFldC2
        setOptionVarCmd(self.optionVar04_tFld_key, getTxt_fromTxtFldC2)

        # tFld_key C3
        # self.options へ ["YO_createSpaceNode3_txtFldC3_text"] を保存
        getTxt_fromTxtFldC3 = self.cmnTxtFld_C3.getText()
        # self.options[self.optionVar05_tFld_key] = getTxt_fromTxtFldC3
        setOptionVarCmd(self.optionVar05_tFld_key, getTxt_fromTxtFldC3)

        # add node type
        # nTyp_key
        # self.options へ ["YO_createSpaceNode3_rdBtnA_bool"] を保存
        getVal_fromOpMnuA = self.cOpMnu_nodeType.getValue()
        # self.options[self.optionVar01_atNm_key] = getVal_fromOpMnuA
        setOptionVarCmd(self.optionVar01_nTyp_key, getVal_fromOpMnuA)

        message(args[0])

        print(getSel_fromRdBtn
              , getTxt_fromTxtFldA1, getTxt_fromTxtFldB1
              , getTxt_fromTxtFldC1, getTxt_fromTxtFldC2, getTxt_fromTxtFldC3
              , getVal_fromOpMnuA
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
        # if len(tFld_key_A1):
        #     self.cmnTxtFld_A1.setFont(self.defaultFont)

        # tFld_key_B1
        tFld_key_B1 = getOptionVarCmd(self.optionVar02_tFld_key)
        # self.cmnTxtFld_B1.setText(self.options[self.optionVar02_tFld_key])
        self.cmnTxtFld_B1.setText(tFld_key_B1)
        # font 変更も加味
        # if len(tFld_key_B1):
        #     self.cmnTxtFld_B1.setFont(self.defaultFont)

        # tFld_key_C1
        tFld_key_C1 = getOptionVarCmd(self.optionVar03_tFld_key)
        # self.cmnTxtFld_C1.setText(self.options[self.optionVar03_tFld_key])
        self.cmnTxtFld_C1.setText(tFld_key_C1)
        # font 変更も加味
        # if len(tFld_key_C1):
        #     self.cmnTxtFld_C1.setFont(self.defaultFont)

        # tFld_key_C2
        tFld_key_C2 = getOptionVarCmd(self.optionVar04_tFld_key)
        # self.cmnTxtFld_C2.setText(self.options[self.optionVar04_tFld_key])
        self.cmnTxtFld_C2.setText(tFld_key_C2)
        # font 変更も加味
        # if len(tFld_key_C2):
        #     self.cmnTxtFld_C2.setFont(self.defaultFont)

        # tFld_key_C3
        tFld_key_C3 = getOptionVarCmd(self.optionVar05_tFld_key)
        # self.cmnTxtFld_C3.setText(self.options[self.optionVar05_tFld_key])
        self.cmnTxtFld_C3.setText(tFld_key_C3)
        # font 変更も加味
        # if len(tFld_key_C3):
        #     self.cmnTxtFld_C3.setFont(self.defaultFont)

        # add node type
        # nTyp_key
        nTyp_key = getOptionVarCmd(self.optionVar01_nTyp_key)
        # self.cOpMnu_nodeType.setValue(self.options[self.optionVar01_nTyp_key])
        self.cOpMnu_nodeType.setValue(nTyp_key)

        message(args[0])  # message output

        # print(self.options[self.optionVar01_mode_key]
        #
        #       , self.options[self.optionVar01_tFld_key]
        #       , self.options[self.optionVar02_tFld_key]
        #       , self.options[self.optionVar03_tFld_key]
        #       , self.options[self.optionVar04_tFld_key]
        #       , self.options[self.optionVar05_tFld_key]
        #
        #       , self.options[self.optionVar01_nTyp_key]
        #       )

        print(mode_key
              , tFld_key_A1, tFld_key_B1, tFld_key_C1, tFld_key_C2, tFld_key_C3
              , nTyp_key
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
        setOptionVarCmd(self.optionVar01_nTyp_key, self.opVar_dictVal_dflt_list_addCSpaceNode[0])  # int(1)
        # self.options[self.optionVar01_mode_key] = self.opVar_dictVal_def_list[0]  # 'mode0'
        # self.options[self.optionVar01_tFld_key] = self.opVar_dictVal_def_list[1]  # ''
        # self.options[self.optionVar02_tFld_key] = self.opVar_dictVal_def_list[2]  # 'clstHndle'
        # self.options[self.optionVar03_tFld_key] = self.opVar_dictVal_def_list[3]  # ''
        # self.options[self.optionVar04_tFld_key] = self.opVar_dictVal_def_list[4]  # ''
        # self.options[self.optionVar05_tFld_key] = self.opVar_dictVal_def_list[5]  # ''
        # self.options[self.optionVar01_atNm_key] = self.opVar_dictVal_dflt_list_addCSpaceNode[0]  # 'locator'
    # 4. UI-4. OptionVar を利用したパラメータ管理 コマンド群 ############################### end

    # 2. UI-2. 追加オプション コマンド群 ################################################ start
    # node type optionMenu 選択ボタン フィールド の現在のモードを抽出する関数
    # 新規
    def get_current_nodeType_opMnu(self, *args):
        u""" < node type optionMenu 選択ボタン フィールド の現在のモードを抽出する関数 です >

        ::

          新規

        ####################

        #.

            :return: opMnuA
            :rtype: str

        ####################
        """
        opMnuA = cmds.optionMenu(self.cOpMnu_nodeType, q = True, v = True)
        return opMnuA
    # 2. UI-2. 追加オプション コマンド群 ################################################## end

    # その他 アルゴリズムとなる コマンド群 ################################################ start
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
    #   proc2.1. spaceNode作成
    # <共通>
    #   proc2.2. 最後に、共通な naming 操作 を行っています。
    ##########################################

    # base から継承 override 変更 (独自に定義しなおして上書き)
    # < UI用 >
    # proc1. #
    # Execute 実行 関数
    # @instance.declogger
    def ui_executeBtnCmd(self, *args):
        u""" < proc1.Execute 実行 関数  です >

        ::

          original 継承から変更 override(独自に定義しなおして上書き)
        """
        # 追加6 ####################################################### start
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
        # 追加6 ####################################################### end

        self.runInUiOrCommand = 'fromUI'

        # UIありきでの実行
        # 追加6 ####################################################### start
        self.scriptEditor2.append_default('\n## ui_executeBtn type ##\n')
        self.scriptEditor2.append_default(u'## 継続中 ########## create spaceNode proc 1 (ui_executeBtn type)')
        # 追加6 ####################################################### end

        # print('\n## ui_executeBtn type ##\n')
        # print(u'## 継続中 ########## create spaceNode proc 1 (ui_executeBtn type)')

        # ##############################################################
        # proc1. #
        # カレントの、textField 文字列を抜き出します。
        # ###########################################
        self.mode = self.currentMode()  # int
        self.currentTxt_A1 = self.get_currentTxt_A1()  # str
        self.currentTxt_B1 = self.get_currentTxt_B1()  # str
        self.currentTxt_C1 = self.get_currentTxt_C1()  # str
        self.currentTxt_C2 = self.get_currentTxt_C2()  # str
        self.currentTxt_C3 = self.get_currentTxt_C3()  # str
        self.current_nodeType = self.get_current_nodeType_opMnu()  # str

        print(u'\n'
              u'// Result: {packageName}.'
              u'{title}.{className}().exe('
              u'mode = {modeInt}'
              u', n = [u\'{a}\', u\'{b}\', u\'{c1}\', u\'{c2}\', u\'{c3}\']'
              u', nodeType = u\'{typ}\''
              u')'
              u'\n'
              .format(packageName = self.pkgName
                      , title = self.title + self.id, className = self.className
                      , modeInt = self.mode
                      , a = self.currentTxt_A1, b = self.currentTxt_B1
                      , c1 = self.currentTxt_C1
                      , c2 = self.currentTxt_C2
                      , c3 = self.currentTxt_C3
                      , typ = self.current_nodeType
                      )
              )
        # ##############################################################

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

        # 追加3
        # 派生元 renameTool5 独自の 選択ノードの明示に使用
        self.initSelectionNodeUUIDListsB.__init__()  # 常に初期化で空にする
        yo_uuid.initSelectionNode_storeUUID(self.selectionLists)

        # 予め出力
        # シーン内 DG name 全リストを出力する メソッド の実行
        self.getObj = self.getDGAll_fromScene()
        # print(self.getObj)

        # 予め出力 TextField関連
        self.wordListsSet_fromUI.__init__()  # 常に初期化で空にする
        self.wordListsSet_fromUI = self.createLists_fromCurrentTxtAll()

        # 追加2
        # 特にコントローラのspace作成時( e.g.: u'spineA_L' )ネーミング時のイレギュラーを想定
        self.typRecordList.__init__()  # 常に初期化で空にする
        for selIndex in self.selectionLists:
            typ = self.strCompsCheck_exe(selIndex)[3]  # tuple[str, str, str, unicode][3]
            self.typRecordList.append(typ)  # return 'underScoresCount1'時を検出したい
        # print(self.typRecordList)

        # ##############################
        # print(u'TextField関連\n\t'
        #       u'self.wordListsSet_fromUI(wordLists) : \n\t\t'
        #       u'{}'.format(self.wordListsSet_fromUI))
        # ##############################

        # 追加6 ####################################################### start
        self.scriptEditor2.append_default(self.current_nodeType)  # nodeType information outPut
        # 追加6 ####################################################### end
        # print(self.current_nodeType)  # nodeType information outPut

        # 共通な一連の関数のまとまり です
        # 場合分けによって、後の方で、
        #   proc1.5., proc2.1, 2.2  操作 に移っていきます
        self.setOfCommonFunctions4(self.wordListsSet_fromUI)

        # 追加3
        # かなり初期の段階で選択を実行します
        # b/c): 派生元 renameTool5 独自の 選択ノードの明示に使用
        cmds.select(cl = True)
        yo_uuid.initSelectionNode_reSelect(self.initSelectionNodeUUIDListsB)
    # 3. UI-3. common ボタン コマンド群 ################################################## end

    # 5. スクリプトベースコマンド入力への対応 ############################################# start

    ##########################################
    # <スクリプトベース用>
    ##########################################
    # プロセスの大枠 #######
    #######################
    # parameter mode, parameter n, parameter nodeType を対象に、
    # proc1. analysis_strs_fromCmd4 メソッドを利用して、必要な文字列を抜き出します。
    # <共通>
    #   proc1.5.
    # <共通>
    #   proc2.1. spaceNode作成
    # <共通>
    #   proc2.2. 最後に、共通な naming 操作 を行っています。
    ##########################################

    # base から継承 override 変更 (独自に定義しなおして上書き)
    # < スクリプトベース用 >
    # proc1. #
    # analysis_strs_fromCmd4 メソッドを利用して、必要な文字列を抜き出します。
    # 引数: relative 追加
    def exe(self, mode = 0, n = None, nodeType = ''):
        u"""< スクリプトベース用 >

        ::

          base から継承 override 変更 (独自に定義しなおして上書き)

          proc1.
            analysis_strs_fromCmd4 メソッドを利用して、必要な文字列を抜き出します。
                引数: nodeType 追加

        #######################

        #.
            :param int mode: rename mode: 強制的:0, 構成要素をキープ:1 何れか

            e.g.): mode = 1
        #.
            :param list of str n: 文字列リスト

            e.g.): n = [u'~', u'~[Space]', u'~', u'', u'']- 基本左記で固定
        #.
            :param str nodeType: 'locator' or ’null’ or ’joint’ 何れか

            e.g.): nodeType = u'joint'

        #######################
        """
        # 追加6 ####################################################### start
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
        # 追加6 ####################################################### end

        if n is None:
            n = []
        # cls = cls()
        # title = cls.title
        # className = cls.className

        self.runInUiOrCommand = 'fromCmd'

        # UI不要での実行
        # 追加6 ####################################################### start
        self.scriptEditor2.append_default('\n## command_execute type ##\n')
        self.scriptEditor2.append_default(u'## 継続中 ########## create spaceNode proc1 (command_execute type)')
        # 追加6 ####################################################### end

        # print('\n## command_execute type ##\n')
        # print(u'## 継続中 ########## create spaceNode proc1 (command_execute type)')

        # ##############################################################
        modeInt_fromCmd, wordListsSet_fromCmd, nodeType_str \
            = self.analysis_strs_fromCmd4(mode, n, nodeType)
        self.mode = modeInt_fromCmd  # str
        self.typ_fromCmd = nodeType_str

        print(u'\n'
              u'// Result: {packageName}.'
              u'{title}.{className}().exe('
              u'mode = {modeInt}'
              u', '
              u'n = {textAll}'
              u', '
              u'type = u\'{nodeType_str}\''
              u')'
              u'\n'
              .format(packageName = self.pkgName
                      , title = self.title + self.id, className = self.className
                      , modeInt = mode
                      , textAll = n
                      , nodeType_str = nodeType
                      )
              )
        # ##############################################################

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

        # 追加3
        # 派生元 renameTool5 独自の 選択ノードの明示に使用
        self.initSelectionNodeUUIDListsB.__init__()  # 常に初期化で空にする
        yo_uuid.initSelectionNode_storeUUID(self.selectionLists)

        # 予め出力
        # シーン内 DG name 全リストを出力する メソッド の実行
        self.getObj = self.getDGAll_fromScene()
        # print(self.getObj)

        # 予め出力 TextField関連ttrft
        self.wordListsSet_fromCmd.__init__()  # 常に初期化で空にする
        self.wordListsSet_fromCmd = wordListsSet_fromCmd

        # 追加2
        # 特にコントローラのspace作成時( e.g.: u'spineA_L' )ネーミング時のイレギュラーを想定
        self.typRecordList.__init__()  # 常に初期化で空にする
        for selIndex in self.selectionLists:
            typ = self.strCompsCheck_exe(selIndex)[3]  # tuple[str, str, str, unicode][3]
            self.typRecordList.append(typ)  # return 'underScoresCount1'時を検出したい
        # print(self.typRecordList)

        # ##############################
        # print(u'TextField関連\n\t'
        #       u'self.wordListsSet_fromCmd(wordLists) : \n\t\t'
        #       u'{}'.format(self.wordListsSet_fromCmd))
        # ##############################

        # 追加6 ####################################################### start
        self.scriptEditor2.append_default(self.typ_fromCmd)  # nodeType information outPut
        # 追加6 ####################################################### end
        # print(self.typ_fromCmd)  # nodeType information outPut

        # 共通な一連の関数のまとまり です
        # 場合分けによって、後の方で、
        #   proc1.5., proc2.1, 2.2  操作 に移っていきます
        self.setOfCommonFunctions4(self.wordListsSet_fromCmd)

        # 追加3
        # かなり初期の段階で選択を実行します
        # b/c): 派生元 renameTool5 独自の 選択ノードの明示に使用
        cmds.select(cl = True)
        yo_uuid.initSelectionNode_reSelect(self.initSelectionNodeUUIDListsB)

    # 完全に新規
    # original( self.analysis_strs_fromCmd() ) からの引数の内容違いによる変更で、新規で定義
    # < スクリプトベース用 >
    # コマンド文字列の parameter mode, parameter n, parameter nodeType を分析し、
    # modeInt_fromCmd, wordListsSet_fromCmd, typStr_fromCmd
    # を出力する メソッド
    def analysis_strs_fromCmd4(self, mode, n, typ):
        u""" < スクリプトベース用 >

        ::

          完全に新規
            original( self.analysis_strs_fromCmd() ) からの引数の内容違いによる変更で、新規で定義

          コマンド文字列の parameter mode, parameter n, parameter nodeType を分析し、
            modeInt_fromCmd, wordListsSet_fromCmd, typStr_fromCmd
                を出力する メソッド

        ######################

        #.

            :param str mode:
            :param list[str] n:
            :param str typ:

        #.
            :return: modeInt_fromCmd, wordListsSet_fromCmd, typStr_fromCmd
            :rtype: tuple[str, list[str], str]

        ######################
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
        patternN = re.compile(r'\'(?P<ptnNStr>.*?)\'')  # 変換箇所1: re.compile(r'u\'(?P<ptnNStr>.*?)\'') からの変更
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
        # 分析3 typ ###
        # あらかじめ用意されている文字列, 'nodeType = u'***','から、必要な文字列 *** を抽出する
        typStrs = 'nodeType = u\'{}\''.format(typ)  # 先ず、文字列にする
        # print(typStrs)
        patternTyp = re.compile(r'\'(?P<ptnTypStr>.*?)\'')  # 変換箇所1: re.compile(r'u\'(?P<ptnTypStr>.*?)\'') からの変更
        # パターン定義: u' と ' で囲まれた文字列を最短文字列で見つける
        typStr_fromCmd = []  # コマンド文字列から抽出の startJoint_str
        search = patternTyp.finditer(typStrs)  # 調べる関数
        # あるならば
        if search:
            iterator = patternTyp.finditer(typStrs)
            for itr in iterator:
                # print(itr.group('ptnTypStr'))
                typStr_fromCmd.append(itr.group('ptnTypStr'))  # 見つけた順にリストに格納する
        typStr_fromCmd = typStr_fromCmd[0]
        # print(typStr_fromCmd)

        return modeInt_fromCmd, wordListsSet_fromCmd, typStr_fromCmd
    # 5. スクリプトベースコマンド入力への対応 ############################################### end

    # 「spaceNode 作成と、naming の核となる コマンド群」 ##################################### start
    # 共通な一連の関数のまとまり ########################################### start
    # 共通な一連の関数のまとまり です
    # original( self.setOfCommonFunctions() )からの内容違いによる変更で、override せずに新規
    # proc1.5. #
    # 場合分けによって、
    #   - 未選択の場合  # A ストップ
    #   - 選択の場合（複数も可）  # D 継続
    # させます
    # @instance.declogger
    def setOfCommonFunctions4(self, wordLists):
        u""" < 共通な一連の関数のまとまり です >

        ::

          original( self.setOfCommonFunctions() )からの内容違いによる変更で、
            override せずに新規

          proc1.5
          場合分けによって、
              - 未選択の場合  # A ストップ
              - 選択の場合（複数も可）  # D 継続
          させます

        #######################

        #.

            :param wordLists:
            :type wordLists: list of str

        #######################
        """
        # 追加6 ####################################################### start
        self.scriptEditor2.append_default(u'## 継続中 ########## spaceNode proc1.5')
        # 追加6 ####################################################### end

        # print(u'## 継続中 ########## spaceNode proc1.5')

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

        # print(self.selectionLists)  # コンポーネント選択中

        # 予め出力
        # イレギュラー対応用変数を出力するための関数 実行
        # ここでいうイレギュラーとは、「選択1っ、atMark 0、TextField関連が完全 の時」 を言います
        # イレギュラー対応用変数 self.waiting_last_string (default: '') を予め出力
        # イレギュラー対応用変数 self.is_exists_forNCName (default: False) を予め出力
        # 選択1っ、atMark 0、TextField関連が完全 の時だけに対応
        self.renameFunction_inIrregularCases()

        # TextField名の構成から判断された、待機している最終文字
        # ##############################
        # print(u'TextField名の構成から判断された、待機している最終文字\n\t'
        #       u'self.waiting_last_string : \n\t\t'
        #       u'{}'.format(self.waiting_last_string))
        # ##############################

        # self.waiting_last_string が、
        # self.getObj リスト内に、
        # 重複した名前として既にあるかどうかを探しあて、存在の真偽を出力する メソッドの実行
        # False: 重複していない
        # True: 重複している 注意!
        # ##############################
        # print(u'<イレギュラー対応用>重複した名前として、'
        #       u'待機している最終文字が既にあるかどうかを探しあて、存在の真偽\n\t'
        #       u'self.is_exists_forNCName : \n\t\t'
        #       u'{}'.format(self.is_exists_forNCName)
        #       )
        # ##############################

        ##############################
        # 場合分けによって、
        #   - 未選択の場合  # A ストップ
        #   - 選択の場合（複数も可）  # D 継続
        # させます
        #############
        # 未選択の場合  # A
        if len(self.selectionLists) == 0:  # A
            # print(u'ストップ A')

            # 追加6 ####################################################### start
            self.scriptEditor2.append_error( u'{}\n\t\t\tLine Number:{}\n'
                                             u'ストップ A\n'
                                             u'何も選択されていないため、'
                                             u'実行する対象がありません。'
                                             u'spaceNode 作成 の実行はストップしました。spaceNode proc 1.5-A'
                                             .format(self.title, YO_logger2.getLineNo())
                                            )
            # 追加6 ####################################################### end

            # YO_logProcess.action('ERROR'
            #                      , u'{}\n\t\t\tLine Number:{}\n'
            #                        u'ストップ A\n'
            #                        u'何も選択されていないため、'
            #                        u'実行する対象がありません。'
            #                        u'spaceNode 作成 の実行はストップしました。spaceNode proc 1.5-A'
            #                      .format(self.title, YO_logger2.getLineNo())
            #                      )

            # self.message_warning(u'何も選択されていないため、'
            #                      u'実行する対象がありません。'
            #                      u'spaceNode 作成 の実行はストップしました。spaceNode proc 1.5-A'
            #                      )
            pass
        #############
        # 選択の場合（複数も可）  # D
        else:  # D
            # 追加6 ####################################################### start
            self.scriptEditor2.append_default(u'継続 D')

            self.scriptEditor2.append_default('******** spaceNode create and naming, proc start.. '
                  '*********************************'
                  'spaceNode proc1.5-D')
            # 追加6 ####################################################### end

            # print(u'継続 D')
            #
            # print('******** spaceNode create and naming, proc start.. '
            #       '*********************************'
            #       'spaceNode proc1.5-D')

            cmds.select(cl = True)
            spaceNodeInfoLists = []
            spaceNodes = []
            nodeType = ''
            # 追加6 ####################################################### start
            self.scriptEditor2.append_default(self.runInUiOrCommand)
            # 追加6 ####################################################### end

            # print(self.runInUiOrCommand)

            if self.runInUiOrCommand == 'fromUI':
                nodeType = self.current_nodeType
            elif self.runInUiOrCommand == 'fromCmd':
                nodeType = self.typ_fromCmd

            # ###########################################
            # proc2.1. spaceNode作成
            # proc2.2. 最後に、共通な naming 操作
            #   を順番に行っています。
            # ###########################################

            # proc2.1. spaceNode作成

            # print(self.typRecordList)
            # for typ in self.typRecordList:
            #     print(typ)
            #
            # print(self.selectionLists, self.typRecordList)

            # 追加8 ####################################################### start
            parentList = []
            for selIndex in self.selectionLists:
                cmds.select(selIndex, r = True)
                cmds.pickWalk(direction = 'up')
                parent = cmds.ls(sl = True)[0]
                parentList.append(parent)
            # print(f'parentList: {parentList}')
            # 追加8 ####################################################### end

            for selIndex, typ in zip(self.selectionLists, self.typRecordList):
                # print(selIndex, typ)
                if typ == u'underScoresCount1':  # 追加2
                    _, splitSelStr_2nd = selIndex.split('_')
                    # print(splitSelStr_2nd)
                    if splitSelStr_2nd.isupper():  # 大文字ならば、識別子の可能性があるので、
                        # proc2.1. # spaceNode作成 type2
                        # print('dividing_if \n\t\"A\"')
                        # print('\t\"type2 exe2 ..\"')
                        spaceNode, parentNodeName = self.createNode_and_posToTheWorld_exe2(selIndex, nodeType)
                        # print(spaceNode, parentNodeName)
                    else:
                        # proc2.1. spaceNode作成 type1
                        # print('dividing_if \n\t\"B\"')
                        # print('\t\"type1 exe ..\"')
                        spaceNode, parentNodeName = self.createNode_and_posToTheWorld_exe(selIndex, nodeType)
                        # print(spaceNode, parentNodeName)
                else:
                    # proc2.1. spaceNode作成 type1
                    # print('dividing_if \n\t\"C\"')
                    # print('\t\"type1 exe ..\"')
                    spaceNode, parentNodeName = self.createNode_and_posToTheWorld_exe(selIndex, nodeType)
                    # print(spaceNode, parentNodeName)

                # print(spaceNode, parentNodeName)

                spaceNodes.append(spaceNode)
                spaceNodeInfo = (spaceNode, parentNodeName)  # tuple化した対の情報
                # print(f'spaceNodeInfo: {spaceNodeInfo}')
                spaceNodeInfoLists.append(spaceNodeInfo)  # その保持

                # print(spaceNode, parentNodeName)
                # print(spaceNodeInfoLists)

            # print(f'spaceNodeInfoLists: {spaceNodeInfoLists}')
            # print(f'self.selectionLists: {self.selectionLists}')

            # 変更7, 変更8
            # 所定の位置まで格納し終わる
            for count, (spaceNodeInfo,
                        selIndex, parentIndex
                        ) in enumerate(
                zip(spaceNodeInfoLists, self.selectionLists, parentList)
                ):
                # print('*******')
                # print(f'selIndex: {selIndex}')
                # print(f'spaceNodeInfo: {spaceNodeInfo}')
                # print(f'spaceNodeInfo[0]: {spaceNodeInfo[0]}')
                # print(f'spaceNodeInfo[1]: {spaceNodeInfo[1]}')  # uniqueでない
                # print(f'parentIndex: {parentIndex}')  # unique
                # print('*******')
                if spaceNodeInfo[1] != u'None':
                    # print('not None')
                    # # 1つでも|があれば、必ず、最後の|を境にして、最後の分割文字列を取得
                    if '|' in selIndex:
                        # 最後の|を境に文字列を2分割し、最後の要素を取得します
                        first_part = selIndex.rsplit('|', 1)[0]
                        last_part = selIndex.rsplit('|', 1)[1]
                        last_part = last_part + 'Temp'
                        # print(f'first_part: {first_part}')
                        # print(f'last_part: {last_part}')
                        # print(f'spaceNodeInfo[0]: {spaceNodeInfo[0]}')
                        # print(f'spaceNodeInfo[1]: {spaceNodeInfo[1]}')  # uniqでない
                        temp = spaceNodeInfo[0].replace(last_part, '')
                        # print(f'temp: {temp}')
                        resultA = temp.replace('_', '')
                        # print(f'resultA: {resultA}')
                        temp1 = cmds.parent(spaceNodeInfo[0], first_part)
                        temp2 = cmds.parent(selIndex, spaceNodeInfo[0])
                        # print(temp1[0], temp2[0])
                        resultB = temp1[0].replace(temp, resultA)
                        # print(f'spaceNodeInfo[0]: {spaceNodeInfo[0]}')
                        # print(f'resultB: {resultB}')
                        cmds.rename(spaceNodeInfo[0], resultB)
                        spaceNodes[count] = resultB  # 該当のインデックスのみ仮名のノードで置き換える
                    else:
                        if '|' in parentIndex:
                            cmds.parent(spaceNodeInfo[0], parentIndex)
                            cmds.parent(selIndex, spaceNodeInfo[0])
                        else:
                            cmds.parent(spaceNodeInfo[0], spaceNodeInfo[1])
                            cmds.parent(selIndex, spaceNodeInfo[0])
                # if spaceNodeInfo[1] != u'None':
                #     pass
                #     # cmds.parent(spaceNodeInfo[0], spaceNodeInfo[1])
                #     # cmds.parent(selIndex, spaceNodeInfo[0])
                elif spaceNodeInfo[1] == u'None':
                    # print('None')
                    # print(f'selIndex: {selIndex}')
                    # print(f'spaceNodeInfo[0]: {spaceNodeInfo[0]}')
                    cmds.parent(selIndex, spaceNodeInfo[0])

            # print('spaceNodes: {}'.format(spaceNodes))

            # proc2.2. 最後に、共通な naming 操作
            # original ネーミングエンジンを利用
            # 選択した全ノード名に対して、unique name にして更新する メソッド の実行
            self.selectionLists = self.checkAndDoUniqueName_forSlNode(spaceNodes)

            # print('selectionLists: {}'.format(self.selectionLists))
            # print('######' * 10)
            # print('koko A')
            # print('######' * 10)
            # print(u'self.selectionLists: \n\t\t'
            #       u'{}'.format(self.selectionLists)
            #       )

            # print(self.mode, wordLists)

            # original ネーミングエンジンを利用
            # 追加6 ####################################################### start
            self.scriptEditor2.append_default(u'YO original ネーミングエンジンを利用')
            # 追加6 ####################################################### end

            # print(u'YO original ネーミングエンジンを利用')
            # print(f'selectionLists: {self.selectionLists}')
            # print(f'self.mode: {self.mode}')
            # print(f'wordLists: {wordLists}')

            # rename の開始
            self.start_executeCmd(self.selectionLists, self.mode, wordLists)  # YO original ネーミングエンジンを利用

            # # 不具合修正1
            # # spaceを仮に作り終えているので、必ず'up'direction 出来る
            cmds.select(cl = True)
            # print(f'self.initSelectionNodeUUIDListsB: {self.initSelectionNodeUUIDListsB}')
            yo_uuid.initSelectionNode_reSelect(self.initSelectionNodeUUIDListsB)
            cmds.pickWalk(direction = 'up')
            # parent = cmds.ls(sl = True)[0]
            # print(f'parent: {parent}')

            # # self.selectionLists の更新
            self.selectionLists = commonCheckSelection()
            # print('######' * 10)
            # print('koko B')
            # print('######' * 10)
            # print(u'self.selectionLists: \n\t\t'
            #       u'{}'.format(self.selectionLists)
            #       )

            # # 正規化された仮のネーミング
            # print(u'新規作成された以下のSpaceノードは、正規化された仮のネーミングが施されています。\n'
            #       u'\t最終的なネーミングでは。、未だございません。')
            # print(u'仮name: \n\t\t'
            #       u'{}'.format(self.selectionLists)
            #       )
            # print('\n')

            for count, (selIndex
                        , typ) in enumerate(zip(self.selectionLists,
                                                self.typRecordList)
                                            ):
                # print(f'selIndex: {selIndex}')
                # print(f'typ: {typ}')
                # print('continue..')
                # 選択されているオブジェクト名の文字列の構成を調べ出力する メソッド 実行
                if typ == u'underScoresCount1':  # 追加2
                    # print(u'maya original ネーミングエンジンを利用')
                    newNameA = selIndex.replace('Temp', '')  # maya original ネーミングエンジンを利用
                    newName = newNameA.replace('newSpace', 'space')
                    # print(f'newName: {newName}')
                    cmds.rename(selIndex, newName)
                else:
                    # print(u'maya original ネーミングエンジンを利用')
                    newName = selIndex.replace('Temp', '')  # maya original ネーミングエンジンを利用
                    # print(f'newName: {newName}')
                    cmds.rename(selIndex, newName)

            # self.selectionLists の更新
            self.selectionLists = commonCheckSelection()
            # print(f'selectionLists: {self.selectionLists}')

            # 最終的なネーミング
            # 追加6 ####################################################### start
            self.scriptEditor2.append_default('***********' * 5)

            self.scriptEditor2.append_default(u'final name: \n\t\t'
                  u'{}'.format(self.selectionLists)
                  )
            # 追加6 ####################################################### end

            # print('***********' * 5)
            #
            # print(u'final name: \n\t\t'
            #       u'{}'.format(self.selectionLists)
            #       )

            for selIndex in self.selectionLists:
                self.selCompStrs_1st\
                    , self.selCompStrs_2nd\
                    , self.selCompStrs_3rd\
                    , self.typ = self.strCompsCheck_exe(selIndex)
                # print(self.selCompStrs_2nd)
                isTitle = self.selCompStrs_2nd.istitle()  # 大文字で始まるか否か
                if isTitle:
                    if self.selCompStrs_2nd == 'Space':
                        newName = selIndex.replace('Space', 'space')
                        cmds.rename(selIndex, newName)
                else:
                    pass
            # 追加6 ####################################################### start
            self.scriptEditor2.append_default('******** spaceNode create and naming, proc done '
                  '*********************************'
                  'spaceNode proc1.5-D'
                  )
            # 追加6 ####################################################### end

            # print('******** spaceNode create and naming, proc done '
            #       '*********************************'
            #       'spaceNode proc1.5-D'
            #       )
    # 共通な一連の関数のまとまり ############################################# end

    # spaceNode作成 操作 ################################################## start
    # 完全に新規
    # nodeCreate and position to the world space 実行関数
    # ###########################################
    # proc2.1. # spaceNode作成 type1
    # ###########################################
    # @instance.declogger
    def createNode_and_posToTheWorld_exe(self, selIndex = None, nodeType = None):
        u""" < nodeCreate and position to the world space 実行関数 です >

        ::

          完全に新規

          proc2.1. # spaceNode作成 type1

        ###########################

        #.

            :param str selIndex: 単独選択
            :param str nodeType: ノードタイプ

        #.

            :return: spaceNode, parentNodeName
            :rtype: tuple[str, str]

        ###########################
        """
        # print(selIndex, nodeType)
        try:  # 親があるパターン
            # parentNodeName = cmds.listRelatives(selIndex, p = True, f = True)[0]
            parentNodeName = cmds.listRelatives(selIndex, parent = True)[0]
            # print(parentNodeName)
        except:  # 親が無いパターン
            parentNodeName = u'None'
            # print(parentNodeName)
        spaceNode = ''
        tempName = 'Temp'

        if nodeType == u'locator':
            spaceNode = cmds.spaceLocator(p = [0, 0, 0], n = u'{}{}'.format(selIndex, tempName))[0]
            cmds.pointConstraint(selIndex, spaceNode, weight = 1, offset = [0, 0, 0])
            cmds.orientConstraint(selIndex, spaceNode, weight = 1, offset = [0, 0, 0])
            cmds.scaleConstraint(selIndex, spaceNode, weight = 1, offset = [1, 1, 1])
            cmds.delete(spaceNode, constraints = True)
        elif nodeType == u'null':
            spaceNode = cmds.group(empty = True, n = u'{}{}'.format(selIndex, tempName))
            cmds.pointConstraint(selIndex, spaceNode, weight = 1, offset = [0, 0, 0])
            cmds.orientConstraint(selIndex, spaceNode, weight = 1, offset = [0, 0, 0])
            cmds.scaleConstraint(selIndex, spaceNode, weight = 1, offset = [1, 1, 1])
            pConstNode = cmds.listRelatives(spaceNode, typ = 'pointConstraint')
            oConstNode = cmds.listRelatives(spaceNode, typ = 'orientConstraint')
            sConstNode = cmds.listRelatives(spaceNode, typ = 'scaleConstraint')
            cmds.delete(pConstNode, oConstNode, sConstNode)
        elif nodeType == u'joint':
            cmds.select(cl = True)
            spaceNode = cmds.joint(p = [0, 0, 0], n = u'{}{}'.format(selIndex, tempName))
            cmds.pointConstraint(selIndex, spaceNode, weight = 1, offset = [0, 0, 0])
            cmds.orientConstraint(selIndex, spaceNode, weight = 1, offset = [0, 0, 0])
            cmds.scaleConstraint(selIndex, spaceNode, weight = 1, offset = [1, 1, 1])
            cmds.delete(spaceNode, constraints = True)
        return spaceNode, parentNodeName

    # 追加2
    # 完全に新規
    # u'underScoresCount1'用
    # nodeCreate and position to the world space 実行関数
    # ###########################################
    # proc2.1. # spaceNode作成 type2
    # ###########################################
    # @instance.declogger
    def createNode_and_posToTheWorld_exe2(self, selIndex = None, nodeType = None):
        u""" < nodeCreate and position to the world space 実行関数 です >

        ::

          追加2
          完全に新規
          u'underScoresCount1'用

          proc2.1. # spaceNode作成 type2

        ###########################

        #.

            :param str selIndex: 単独選択
            :param str nodeType: ノードタイプ

        #.

            :return: spaceNode, parentNodeName
            :rtype: tuple[str, str]

        ###########################
        """
        # print(selIndex, nodeType)
        splitSelStr_1st, splitSelStr_2nd = selIndex.split('_')
        # print(splitSelStr_1st, splitSelStr_2nd)
        underScore = u'_'
        new = u'new'
        newName = splitSelStr_1st + underScore + new + underScore + splitSelStr_2nd
        # print(newName)

        try:  # 親があるパターン
            # parentNodeName = cmds.listRelatives(selIndex, p = True, f = True)[0]
            parentNodeName = cmds.listRelatives(selIndex, parent = True)[0]
            # print(parentNodeName)
        except:  # 親が無いパターン
            parentNodeName = u'None'
            # print(parentNodeName)
        spaceNode = ''
        tempName = 'Temp'

        if nodeType == u'locator':
            spaceNode = cmds.spaceLocator(p = [0, 0, 0], n = u'{}{}'.format(newName, tempName))[0]
            cmds.pointConstraint(selIndex, spaceNode, weight = 1, offset = [0, 0, 0])
            cmds.orientConstraint(selIndex, spaceNode, weight = 1, offset = [0, 0, 0])
            cmds.scaleConstraint(selIndex, spaceNode, weight = 1, offset = [1, 1, 1])
            cmds.delete(spaceNode, constraints = True)
        elif nodeType == u'null':
            spaceNode = cmds.group(empty = True, n = u'{}{}'.format(newName, tempName))
            cmds.pointConstraint(selIndex, spaceNode, weight = 1, offset = [0, 0, 0])
            cmds.orientConstraint(selIndex, spaceNode, weight = 1, offset = [0, 0, 0])
            cmds.scaleConstraint(selIndex, spaceNode, weight = 1, offset = [1, 1, 1])
            pConstNode = cmds.listRelatives(spaceNode, typ = 'pointConstraint')
            oConstNode = cmds.listRelatives(spaceNode, typ = 'orientConstraint')
            sConstNode = cmds.listRelatives(spaceNode, typ = 'scaleConstraint')
            cmds.delete(pConstNode, oConstNode, sConstNode)
        elif nodeType == u'joint':
            cmds.select(cl = True)
            spaceNode = cmds.joint(p = [0, 0, 0], n = u'{}{}'.format(newName, tempName))
            cmds.pointConstraint(selIndex, spaceNode, weight = 1, offset = [0, 0, 0])
            cmds.orientConstraint(selIndex, spaceNode, weight = 1, offset = [0, 0, 0])
            cmds.scaleConstraint(selIndex, spaceNode, weight = 1, offset = [1, 1, 1])
            cmds.delete(spaceNode, constraints = True)
        return spaceNode, parentNodeName
    # spaceNode作成 操作 #################################################### end
    # 「spaceNode 作成と、naming の核となる コマンド群」 ####################################### end

if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
