# -*- coding: utf-8 -*-

u"""
YO_shearConstraintByMatrix1_Modl.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -5.5-
:Date: 2024/05/25

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PyMel version: 1.2.0
    - PySide2 version: 5.15.2

-リマインダ-
    done: 2024/05/25
        - 変更12
            - 概要: source, target について、
                片方もしくは両方が シーンに存在しない時、
                以降の実行中止させる 明示と中止の実行
            - 詳細:
                ::

                    -   # コマンドベース
                        self.command(connect = cnctAllValue, source = src, target = tgt)  # proc1.5. へ渡る

                    +   # 変更12 ########################################################## start
                        if not cmds.objExists(src) or not cmds.objExists(tgt):
                            # 修正10 ########################################################## start
                            self.scriptEditor2.append_error(u'source, target について、'
                                                            u'片方もしくは両方が '
                                                            u'当シーンには存在しない為、以降の実行は中止しました。')
                            # 修正10 ########################################################## start
                            # print(u'source, target について、'
                            #       u'片方もしくは両方が '
                            #       u'当シーンには存在しない為、以降の実行は中止しました。')

                            pass
                        else:
                            # コマンドベース
                            self.command(connect = cnctAllValue, source = src, target = tgt)  # proc1.5. へ渡る
                        # 変更12 ########################################################## end
        version = '-5.5-'

    done: 2024/05/16
        - 変更11 追加11 追加11
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
                - 置換した箇所: 以下のように、置き換えます
                    先ず3箇所
                    ::

                        +   def ui_executeBtnCmd(self, *args):
                                ...
                                # 追加11 ####################################################### start
                                check_string = 'check'
                                ...
                                elif state == 'open':
                                        print('open済、再利用')
                                        self.scriptEditor2.append_default('open済、再利用')
                                # 追加11 ####################################################### end
                                ...

                        +   def breakAndReset(self, *args):
                                ...
                                # 追加11 ####################################################### start
                                check_string = 'check'
                                ...
                                elif state == 'open':
                                        print('open済、再利用')
                                        self.scriptEditor2.append_default('open済、再利用')
                                # 追加11 ####################################################### end
                                ...

                        +   def command(sself, *args, **kwargs):
                                ...
                                # 追加11 ####################################################### start
                                check_string = 'check'
                                ...
                                elif state == 'open':
                                        print('open済、再利用')
                                        self.scriptEditor2.append_default('open済、再利用')
                                # 追加11 ####################################################### end
                                ...
                    その他、多数ある箇所
                    ::

                        +   # 追加11 ########################################################### start
                            self.scriptEditor2.append_default(...)
                            # 追加11 ########################################################### end

                        +   # 追加11 ########################################################### start
                            self.scriptEditor2.append_error(...)
                            # 追加11 ########################################################### end
        version = '-5.0-'

    done: 2024/05/16
        - 修正10
            - 概要: バグ修正
            - 詳細: ソースに 親が無くワールド空間の場合 発生
                ::

                    -   def cnctSrcHircyTgtHircy2MltMat_exe(self, *args, **kwargs):
                            ...
                            self.srcP = cmds.listRelatives(src, p = True)[0]
                            ...
                            if not ToF:
                                ...
                                # 階層をたどり、接続の有無まで行う、最終接続 sub main 関数

                    +   def cnctSrcHircyTgtHircy2MltMat_exe(self, *args, **kwargs):
                            ...
                            # 修正10 ########################################################## start
                            srcP_list = cmds.listRelatives(src, p = True) or []
                            if not srcP_list:
                                print("親ノード: root")
                                pass
                            else:
                                self.srcP = srcP_list[0]
                                print("親ノード:", self.srcP)
                                srcP = self.srcP
                                ...
                                if not ToF:
                                    ...
                                    # 階層をたどり、接続の有無まで行う、最終接続 sub main 関数
                            # 修正10 ########################################################## end
        version = '-5.0-'

    done: 2024/05/15
        - 修正箇所9
            - 概要: バグ修正
            - 詳細: ターゲットが 必ずしも joint とは限らない場合に 発生
                ::

                    -   def breakAndReset(self, *args):
                            ...
                            if not self.newNodesAll:
                                pass
                                message_warning(u'幾つかのコネクションに'
                                                u'想定外な接続が見つかりました。'
                                                u'実行は中断されました。'
                                                )
                            else:
                                # 変換箇所7
                                print(f'\tdelete those nodes: {self.newNodesAll}')
                                cmds.delete(self.newNodesAll)
                                print('***' * 15 + '\n')
                                ...

                    +   def breakAndReset(self, *args):
                            ...
                            # 修正箇所9 ########################################### start
                            # joint かつ self.newNodesAll が空っぽなら
                            if not self.newNodesAll and isJoint:
                                pass
                                message_warning(u'幾つかのコネクションに'
                                                u'想定外な接続が見つかりました。'
                                                u'実行は中断されました。'
                                                )
                            # self.newNodesAll が空っぽでないなら、joint を含み それ以外でもなんでも
                            elif self.newNodesAll:
                                # 変換箇所7
                                print(f'\tdelete those nodes: {self.newNodesAll}')
                                cmds.delete(self.newNodesAll)
                            # 修正箇所9 ########################################### end
                            ...
                            # 修正箇所9 ########################################### start
                            # joint を含み それ以外でもなんでも 以下実行
                            print('***' * 15 + '\n')
                            ...
                            # 修正箇所9 ########################################### end
        version = '-5.0-'

    done: 2024/05/16
        - 暫定追加修正1
            - 概要: ソース名 が想定を超え、ネーミング が上手く発動しない箇所を修正
            - 詳細:
                ソース名 の strsCompLists[0], strsCompLists[1]
                    の内、
                strsCompLists[1] が、L, R, C 以外で、['jt*', 'if*', 'ctrl*', 'Gp*', 'GP*']
                    の場合に、上手くネーミング出来ないバグ修正
                - 原因:
                    source 側への登録ノードに対して、
                        元来は、コントローラ側としての登録としてしか想定をしておらず、
                            第二単語に、L, R, C、以外は想定しておらず。。
                ::

                    +   def strCompLists_count_caseDividing_exe(self, strsCompLists = None
                                                , utilNodeShortNameSet = None
                                                ):
                            ...
                            elif len(strsCompLists) == 2:
                                ...
                                # 暫定追加修正1 ['jt', 'if', 'ctrl', 'Gp', 'GP'] に対応 ######### start
                                pattern = r'^(jt|if|ctrl|Gp|GP).*'  # jt, if, ctrl, Gp, GP で始まる文字列に一致する正規表現パターン
                                ...
                                if re.match(pattern, strsCompLists[1]):
                                    print(f'strsCompLists[1]: {strsCompLists[1].capitalize()}')  # 先頭を大文字
                                    newStrsCompLists = [
                                        strsCompLists[0] + strsCompLists[1].capitalize()]
                                    print(f'newStrsCompLists[0]: {newStrsCompLists[0]}')  # 先頭を大文字
                                    ...
                                    utilNodeShortName = utilNodeShortNameSet.replace(' ', '')
                                    ...
                                    RT_Modl().exe(mode = 0
                                                  , n = [u'{}'.format(newStrsCompLists[0])
                                            , u'{}@'.format(utilNodeShortName)
                                            , u''  # 変更 memo): old - > u'~'
                                            , u''
                                            , u''
                                                         ]
                                                  )
                                else:
                                    ...
                                    RT_Modl().exe(mode = 0
                                                  , n = [u'{}'.format(strsCompLists[0])
                                            , u'{}@'.format(utilNodeShortName)
                                                         # test 変更 memo): old - > u'{}{}@'.format(strsCompLists[1], utilNodeShortName
                                            , u''  # 変更 memo): old - > u'~'
                                            , u''
                                            , u'{}'.format(strsCompLists[1])
                                                         ]
                                                  )
                                # 暫定追加修正1 ['jt', 'if', 'ctrl', 'Gp', 'GP'] に対応 ######### end
                            ...
        version = '-5.0-'

    done: 2024/01/04
        - 変換箇所8
            - 概要: 絶対パス から 相対パス へ記述変更
            - 詳細:
                ::

                  -     from YO_utilityTools.shearConstraintByMatrix.[...] import ...
                  +     from .[...] import ...

                  -     from YO_utilityTools.lib.[...] import ...
                  +     from ..lib.[...] import ...

                  -     from YO_utilityTools.lib import ...
                  +     from ..lib import ...

                  -     from YO_utilityTools.renameTool.YO_renameTool5_Modl import RT_Modl
                  +     from ..renameTool.YO_renameTool5_Modl import RT_Modl

        version = '-2.3-'

    done: 2023/11/20
        - 変換箇所7
            - 概要: プロセス出力をダイエット
            - 詳細: 以下の箇所 合計7箇所 をコメントアウト
            ::

              # print(...)

        version = '-2.2-'

    done: 2023/11/17
        - 新規2
            - 概要: 新規に作成された utilityNode の multMatrixNode のみを確実に探し当てる関数
            - 詳細箇所:
                ::

                  def search_multMatrixNode_Sher(self, selectionNode):
                    ...

        version = '-2.1-'

    done: 2023/11/16
        - 生かさない箇所1
            - 概要: shearConstraint だけに特化した記述
            - 詳細箇所:
                ::

                  ...
                  # cmds.connectAttr("{}.outputQuat".format(dM)
                  #                    , "{}.input1Quat".format(qPrd)
                  #                    , f = True
                  #                    )
                  ...

        version = '-2.0-'

    done: 2023/11/13~2023/11/15
        - 新規1
            - 概要: 新規に作成された utilityNode を一括で確実にリスト登録する関数
            - 詳細箇所:
                ::

                  def check_utilityNode_Connections_Sher(self, selectionNode):
                    ...

            - 概要: 新規に作成された utilityNode の decomposeMatrixNode のみを確実に探し当てる関数
            - 詳細箇所:
                ::

                  def search_decomposeMatrixNode_Sher(self, selectionNode):
                    ...

        - 変更箇所1
            - 概要: shearConstraint だけに特化した記述に変更
            - 詳細箇所: これまで T, R, S, Shear を一遍に実行していた箇所を Shear 実行のみにした
                ::

                  def createInitAttr_Sher(self, tgt, *args):
                    ...
                  def setInitAttr_Sher(self, tgt, *args):
                    ...
                  def delInitAttr_Sher(self, tgt, *args):
                    ...
                    
        version = '-1.0-'

    done: 2023/11/13~2023/11/15
        - 新規

        version = '-1.0-'
"""

# 標準ライブラリ #################################################################
# from functools import partial  # partial 利用時は、最後の引数に、*args 要時あり
# import pprint
import re

# サードパーティライブラリ #########################################################
import maya.cmds as cmds
# from pymel import core as pm
# Maya Python API 2.0, OpenMaya モジュールのインポートとローカル名 om2 への変更
from maya.api import OpenMaya as om2
# 追加11
from PySide2.QtCore import Slot

# ローカルで作成したモジュール ######################################################
# basic_configuration(基本構成)
from .config import SPACE, TITLE, VERSION
# 汎用ライブラリー の使用 ################################################################ start
# from ..lib.YO_validate import validate_func
# from ..lib.YO_validate import type_checked
from ..lib.message import message
from ..lib.message_warning import message_warning
from ..lib.commonCheckJoint import commonCheckJoint  # :return: bool
from ..lib.commonCheckSelection import commonCheckSelection  # :return: string

# ロギング用モジュール ##################################################### start
from ..lib.YO_logger2 import LogProcess_Output  # ログプロセス出力用クラス
YO_logProcess = LogProcess_Output()
# YO_logProcess.action(....) : 細かな情報出力、として利用しています

# from ..lib import YO_logger2
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
# 追加11
from ..TemplateForPySide2.CustomScriptEditor2SPIModule import custom_scriptEditor2_instance
# renameTool engine を利用します
from ..renameTool.YO_renameTool5_Modl import RT_Modl


class ShConByMat_Modl(object):
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

        # 完全に新規
        self.constructor_chunk5()  # コンストラクタのまとまり5 # UIコントロールに関わる定義の追加

        self.settingOptionVar()  # コンストラクタのまとまりA # optionVar のセッティング
        self.startOptionVarCmd()  # コンストラクタのまとまりB # optionVar の初期実行コマンド

        # self.options = pm.optionVar  # type: # OptionVarDict
        # self.options = upDateOptionVarsDictCmd()  # type: # dict

        # 追加
        self.constructor_chunk_addA()  # コンストラクタのまとまりaddA # その他の定義2

        # 追加11 ########################################################### start
        self.scriptEditor2_chunk1()
        self.scriptEditor2_chunk2()
        # 追加11 ########################################################### end

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
    # 追加11 ########################################################### end

    # common コマンド群 ################################################################ start
    # print message メソッド
    # from ..lib.message import message へ移動...

    # print warning message メソッド
    # from ..lib.message_warning import message_warning へ移動...

    # selection 共通関数 v3 -flatten込み
    # from ..lib.commonCheckSelection import commonCheckSelection へ移動...

    # selection が joint かどうか調べる関数
    # from ..lib.commonCheckJoint import commonCheckJoint へ移動...
    # common コマンド群 ################################################################## end

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

        self.params = []  # list of float, range is 12, T, R, S, SH

    # 完全に新規
    # コンストラクタのまとまり5 # UIコントロールに関わる定義の追加
    def constructor_chunk5(self):
        u""" < コンストラクタのまとまり5 # UIコントロールに関わる定義の追加 です >

        ::

          完全に新規

        #######################
        """
        self.tBtnA_set_src = None
        self.tBtnA_sel_src = None
        self.tBtnA_clr_src = None

        self.tBtnB_set_tgt = None
        self.tBtnB_sel_tgt = None
        self.tBtnB_clr_tgt = None

        self.cBox_cnctAll = None

    # 追加
    # コンストラクタのまとまりaddA # その他の定義2
    def constructor_chunk_addA(self):
        u""" < コンストラクタのまとまりaddA # その他の定義2 です >

        ::

          追加
          当ツール renameTool5 独自の 選択ノードの明示に使用
        """
        # 格納用リスト宣言
        self.initSelectionNodeUUIDLists = []

    # コンストラクタのまとまりA # optionVar のセッティング
    def settingOptionVar(self):
        u""" < コンストラクタのまとまりA # optionVar のセッティング です > """
        # dict  # range is 2
        # key:   [type(str)
        # , type(str)
        # ]  # range is 2
        # value: [type(str)
        # , type(str)
        # ]  # range is 2
        self.opVar_dictVal_dflt_list = ['', ''
                                        ]  # range is 2

        # DATA naming ########################################################### start
        # save settings menu により、maya optionVar への 辞書登録を実施する準備です
        # dict  # range is 2
        # key:   [type(str)
        # , type(str)
        # ]  # range is 2
        # value: [type(str)
        # , type(str)
        # ]  # range is 2

        # range is 2
        self.optionVar01_tFld_key = self.title + self.underScore + 'txtFldSrc_text'  # type: str
        self.optionVar02_tFld_key = self.title + self.underScore + 'txtFldTgt_text'  # type: str
        # DATA naming ########################################################### end

    # コンストラクタのまとまりB # optionVar の初期実行コマンド
    def startOptionVarCmd(self):
        u""" < コンストラクタのまとまりB # optionVar の初期実行コマンド です > """
        # tFld_key_Src
        self.tFldA_set_src = None  # type: pm.textField
        # #######################
        # 補足 #
        # 初めてmayaで実行すると、optionVar は辞書なので
        # 「keyが初めて実行されてるから無いよ！」
        # というエラーが出るのでそれを回避しています
        # #######################
        if getOptionVarCmd(self.optionVar01_tFld_key) is None:  # set default
            setOptionVarCmd(self.optionVar01_tFld_key, self.opVar_dictVal_dflt_list[0])
            # self.options[self.optionVar01_tFld_key] = self.opVar_dictVal_dflt_list[1]  # dict type(value): str

        # tFld_key_Tgt
        self.tFldB_set_tgt = None  # type: pm.textField
        # #######################
        # 補足 #
        # 初めてmayaで実行すると、optionVar は辞書なので
        # 「keyが初めて実行されてるから無いよ！」
        # というエラーが出るのでそれを回避しています
        # #######################
        if getOptionVarCmd(self.optionVar02_tFld_key) is None:  # set default
            setOptionVarCmd(self.optionVar02_tFld_key, self.opVar_dictVal_dflt_list[1])
            # self.options[self.optionVar02_tFld_key] = self.opVar_dictVal_dflt_list[2]  # dict type(value): str
    # コンストラクタのまとまり群 ########################################################### end

    # 1. UI-1. メニュー コマンド群 ###################################################### start
    # Save Settings 実行による optionVar の保存 関数
    def editMenuSaveSettingsCmd(self, *args):
        u""" < Save Settings 実行による optionVar の保存 関数 です > """
        # tFld_key_Src
        getTxt_fromTxtFldA1 = self.tFldA_set_src.getText()
        setOptionVarCmd(self.optionVar01_tFld_key, getTxt_fromTxtFldA1)

        # tFld_key_Tgt
        getTxt_fromTxtFldB1 = self.tFldB_set_tgt.getText()
        setOptionVarCmd(self.optionVar02_tFld_key, getTxt_fromTxtFldB1)

        message(args[0])

        print(getTxt_fromTxtFldA1, getTxt_fromTxtFldB1
              )

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
        u""" < UI-4. optionVar からの値の復元 実行 関数 です >

        ::


        """
        # tFld_key_Src
        tFld_key_Src = getOptionVarCmd(self.optionVar01_tFld_key)  # type: str
        self.tFldA_set_src.setText(tFld_key_Src)  # type: pm.textField
        # cmds.textField(self.tFldA_set_src, edit = True, text = tFld_key_Src)
        # button のステータスも加味
        if len(tFld_key_Src):
            # UI 更新
            self.tBtnA_set_src.setEnable(False)
            self.tBtnA_sel_src.setEnable(True)
            self.tBtnA_clr_src.setEnable(True)
            # cmds.button('tBtnA_set_src', e = True, enable = False)
            # cmds.button('tBtnA_sel_src', e = True, enable = True)
            # cmds.button("tBtnA_clr_src", e = True, enable = True)

        # tFld_key_Tgt
        tFld_key_Tgt = getOptionVarCmd(self.optionVar02_tFld_key)  # type: str
        self.tFldB_set_tgt.setText(tFld_key_Tgt)  # type: pm.textField
        # cmds.textField(self.tFld_key_Tgt, edit = True, text = tFld_key_Tgt)
        if len(tFld_key_Tgt):
            # UI 更新
            self.tBtnB_set_tgt.setEnable(False)
            self.tBtnB_sel_tgt.setEnable(True)
            self.tBtnB_clr_tgt.setEnable(True)
            # cmds.button('tBtnB_set_tgt', e = True, enable = False)
            # cmds.button('tBtnB_sel_tgt', e = True,  enable = True)
            # cmds.button("tBtnB_clr_tgt", e = True, enable = True)

        message(args[0])  # message output

        print(tFld_key_Src, tFld_key_Tgt)

    # UI-4. optionVar の value を default に戻す操作 関数
    def set_default_value_toOptionVar(self):
        u""" < UI-4. optionVar の value を default に戻す操作 関数 です >

        ::

          self.opVar_dictVal_dflt_list = ['', '']  # list of str

        """
        setOptionVarCmd(self.optionVar01_tFld_key, self.opVar_dictVal_dflt_list[0])  # ''
        setOptionVarCmd(self.optionVar02_tFld_key, self.opVar_dictVal_dflt_list[1])  # ''
    # 4. UI-4. OptionVar を利用したパラメータ管理 コマンド群 ############################### end

    # 2. UI-2. 追加オプション コマンド群 ################################################ start
    def ui_tFldA_allBtnCmd(self, command = str, *args):
        selectionLists = commonCheckSelection()
        if not selectionLists:
            if command is 'set':
                message_warning(u'コントローラ側(source) を選択し、Set ボタンを押下し、'
                                u'登録を完了させてください'
                                )
                pass
        else:
            if command is 'set':
                self.tFldA_set_src.setText(selectionLists[0])
                self.tBtnA_set_src.setEnable(False)
                self.tBtnA_sel_src.setEnable(True)
                self.tBtnA_clr_src.setEnable(True)
                cmds.select(selectionLists[0], r = True)
                message(u'コントローラ側(source) を登録しました')
        if command is 'sel':
            self.getNode_fromSrcTxtFld = self.tFldA_set_src.getText()
            cmds.select(self.getNode_fromSrcTxtFld, r = True)
            message(u'登録 コントローラ側(source) を選択します')
        if command is 'clr':
            self.tFldA_set_src.setText('')
            self.tBtnA_set_src.setEnable(True)
            self.tBtnA_sel_src.setEnable(False)
            self.tBtnA_clr_src.setEnable(False)
            message(u'コントローラ側(source) の登録をクリアーしました')

    def ui_tFldB_allBtnCmd(self, command = str, *args):
        selectionLists = commonCheckSelection()
        if not selectionLists:
            if command is 'set':
                message_warning(u'コントロールされる側(target) を選択し、Set ボタンを押下し、'
                                u'登録を完了させてください'
                                )
                pass
        else:
            if command is 'set':
                self.tFldB_set_tgt.setText(selectionLists[0])
                self.tBtnB_set_tgt.setEnable(False)
                self.tBtnB_sel_tgt.setEnable(True)
                self.tBtnB_clr_tgt.setEnable(True)
                cmds.select(selectionLists[0], r = True)
                message(u'コントロールされる側(target) を登録しました')
        if command is 'sel':
            self.getNode_fromTgtTxtFld = self.tFldB_set_tgt.getText()
            cmds.select(self.getNode_fromTgtTxtFld, r = True)
            message(u'登録 コントロールされる側(target) を選択します')
        if command is 'clr':
            self.tFldB_set_tgt.setText('')
            self.tBtnB_set_tgt.setEnable(True)
            self.tBtnB_sel_tgt.setEnable(False)
            self.tBtnB_clr_tgt.setEnable(False)
            message(u'コントロールされる側(target) の登録をクリアーしました')
    # 2. UI-2. 追加オプション コマンド群 ################################################## end

    # その他 アルゴリズムとなる コマンド群 ################################################ start
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
    # @validate_func
    def strCompLists_count_caseDividing_exe(self, strsCompLists = None
                                            , utilNodeShortNameSet = None
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
        if utilNodeShortNameSet is None:
            utilNodeShortNameSet = '***'

        # print('\nkokoA')
        # x = type_checked(strsCompLists, list)
        # y = type_checked(utilNodeShortNameSet, str)
        # print(x, y)

        if len(strsCompLists) == 3:
            # print('3')
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
            # print('2')
            # print(strsCompLists)  # [u'spineA', u'L']
            # utilNodeShortNameSet = utilNodeShortNameSet.title()  # 大文字整形
            utilNodeShortName = utilNodeShortNameSet.replace(' ', '')  # space削除
            # print(utilNodeShortName)  # e.g.): u'multMtrx'

            # 暫定追加修正1 ['jt', 'if', 'ctrl', 'Gp', 'GP'] に対応 ######### start
            pattern = r'^(jt|if|ctrl|Gp|GP).*'  # jt, if, ctrl, Gp, GP で始まる文字列に一致する正規表現パターン
            # print(f'strsCompLists[0]: {strsCompLists[0]}')
            # print(f'strsCompLists[1]: {strsCompLists[1]}')
            if re.match(pattern, strsCompLists[1]):
                # 追加11 ####################################################### start
                self.scriptEditor2.append_default(f'strsCompLists[1]: {strsCompLists[1].capitalize()}')  # 先頭を大文字
                # 追加11 ####################################################### end
                # print(f'strsCompLists[1]: {strsCompLists[1].capitalize()}')  # 先頭を大文字

                newStrsCompLists = [
                    strsCompLists[0] + strsCompLists[1].capitalize()]

                # 追加11 ####################################################### start
                self.scriptEditor2.append_default(f'newStrsCompLists[0]: {newStrsCompLists[0]}')  # 先頭を大文字
                # 追加11 ####################################################### end
                # print(f'newStrsCompLists[0]: {newStrsCompLists[0]}')  # 先頭を大文字

                # print('1') と同等とみなして、
                # 小文字整形(そのまま) + space削除のみ
                utilNodeShortName = utilNodeShortNameSet.replace(' ', '')
                # renameTool 発動
                # 変更1
                # DG命名を見直す
                RT_Modl().exe(mode = 0
                              , n = [u'{}'.format(newStrsCompLists[0])
                        , u'{}@'.format(utilNodeShortName)
                        , u''  # 変更 memo): old - > u'~'
                        , u''
                        , u''
                                     ]
                              )
            else:
                # renameTool 発動
                # 変更1
                # DG命名を見直す
                RT_Modl().exe(mode = 0
                              , n = [u'{}'.format(strsCompLists[0])
                        , u'{}@'.format(utilNodeShortName)
                                     # test 変更 memo): old - > u'{}{}@'.format(strsCompLists[1], utilNodeShortName
                        , u''  # 変更 memo): old - > u'~'
                        , u''
                        , u'{}'.format(strsCompLists[1])
                                     ]
                              )
            # 暫定追加修正1 ['jt', 'if', 'ctrl', 'Gp', 'GP'] に対応 ######### end
        elif len(strsCompLists) == 1:
            # print('1')
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

    # 命名規則のコントロール  ################################################## end

    # 新規作成された outPutNode と inPutNode コネクションに使用される関数 ######## start
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

    # 変更箇所1 未使用
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

    # 変更箇所1 未使用
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

    # 変更箇所1 未使用
    # 新規作成された outPutNode と inPutNode のコネクションを行う
    # (Translate 限定)
    def oP2iP_cnctT_exe(self, outPutNode, inPutNode):
        u""" <新規作成された outPutNode と inPutNode のコネクションを行う
        (Translate 限定)
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
        # print(chkSorcTSShPlugs)
        if chkSorcTSShPlugs == [None, None, None]:
            for ax in list('XYZ'):
                cmds.connectAttr("{}.outputTranslate{}".format(outPutNode, ax)
                                 , "{}.translate{}".format(inPutNode, ax)
                                 , f = True
                                 )

    # 変更箇所1
    # 新規作成された outPutNode と inPutNode のコネクションを行う
    # (Shear 限定)
    def oP2iP_cnctSh_exe(self, outPutNode, inPutNode):
        u""" <新規作成された outPutNode と inPutNode のコネクションを行う
        (Shear 限定)
        >
        """
        chkSorcTSShPlugs = []
        # for ax in list('XYZ'):
        #     # inPutNode 自分自身へ入力されてくる、ソース元をリストする(trans のみ！)
        #     plug = cmds.listConnections('{}.translate{}'.format(inPutNode, ax)
        #                                 , c = False
        #                                 , s = True, d = False, p = True
        #                                 )
        #     chkSorcTSShPlugs.append(plug)
        # for ax in list('XYZ'):
        #     # inPutNode 自分自身へ入力されてくる、ソース元をリストする(scale のみ！)
        #     plug = cmds.listConnections('{}.scale{}'.format(inPutNode, ax)
        #                                 , c = False
        #                                 , s = True, d = False, p = True
        #                                 )
        #     chkSorcTSShPlugs.append(plug)
        for ax in ['XY', 'XZ', 'YZ']:
            # inPutNode 自分自身へ入力されてくる、ソース元をリストする(shear のみ！)
            plug = cmds.listConnections('{}.shear{}'.format(inPutNode, ax)
                                        , c = False
                                        , s = True, d = False, p = True
                                        )
            chkSorcTSShPlugs.append(plug)
        # print(chkSorcTSShPlugs)
        if chkSorcTSShPlugs == [None, None, None]:
            # for ax in list('XYZ'):
            #     cmds.connectAttr("{}.outputTranslate{}".format(outPutNode, ax)
            #                      , "{}.translate{}".format(inPutNode, ax)
            #                      , f = True
            #                      )
            # for ax in list('XYZ'):
            #     cmds.connectAttr("{}.outputScale{}".format(outPutNode, ax)
            #                      , "{}.scale{}".format(inPutNode, ax)
            #                      , f = True
            #                      )
            for ax1, ax2 in zip(['X', 'Y', 'Z'], ['XY', 'XZ', 'YZ']):
                cmds.connectAttr("{}.outputShear{}".format(outPutNode, ax1)
                                 , "{}.shear{}".format(inPutNode, ax2)
                                 , f = True
                                 )
    # 新規作成された outPutNode と inPutNode コネクションに使用される関数 ########## end

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
        selList = commonCheckSelection()
        print(selList)  # type : list of 'unicode'
        # print('\n')
        cmds.select(cl = True)
        pathList = []  # 一旦、お互いのパスをまとめる
        # 追加11 ####################################################### start
        self.scriptEditor2.append_default('***' * 30 + u'調査の開始')
        # 追加11 ####################################################### end
        # print('***' * 30 + u'調査の開始')

        if len(selList) == 0 or len(selList) == 1 or len(selList) >= 3:
            # 追加11 ####################################################### start
            self.scriptEditor2.append_default(u'オブジェクトが2つ選択されていないか、もしくは3つ以上同時に選択されています。')
            self.scriptEditor2.append_default('***' * 20 + u'調査の中止！\n')
            # 追加11 ####################################################### end
            # print(u'オブジェクトが2つ選択されていないか、もしくは3つ以上同時に選択されています。')
            # print('***' * 20 + u'調査の中止！\n')

            pass
        elif len(selList) == 2:
            for sel in selList:
                # 追加11 ####################################################### start
                self.scriptEditor2.append_default('***' * 20)
                # 追加11 ####################################################### end
                # print('***' * 20)

                # 追加11 ####################################################### start
                self.scriptEditor2.append_default(sel)
                # 追加11 ####################################################### end
                # print(sel)

                # print(type(sel))  # sel : <type 'unicode'>
                # print(type(DAGPath(sel)))  # DAGPath(sel) : <type 'OpenMaya.MDagPath'>
                parents = self.get_parents(self.DAGPath(sel))
                # print(type(parents))  # parents : <type 'list'>
                # print(parents)
                A = [c.fullPathName() for c in parents]

                # print(A)  # type : list of 'unicode'

                pathList.append(A)
                if len(A) > 0:
                    # 追加11 ####################################################### start
                    self.scriptEditor2.append_default(u'親は..')
                    self.scriptEditor2.append_default(A[-1])
                    self.scriptEditor2.append_default('***' * 20 + u'調査、完了\n')  # cmds.select(A[-1], r = True)
                    # 追加11 ####################################################### end
                    # print(u'親は..')
                    # print(A[-1])
                    # print('***' * 20 + u'調査、完了\n')  # cmds.select(A[-1], r = True)

                elif len(A) == 0:
                    # 追加11 ####################################################### start
                    self.scriptEditor2.append_default(u'親が見当たりません。')
                    self.scriptEditor2.append_default('***' * 20 + u'調査、完了\n')
                    # 追加11 ####################################################### end
                    # print(u'親が見当たりません。')
                    # print('***' * 20 + u'調査、完了\n')

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
            # 追加11 ####################################################### start
            self.scriptEditor2.append_default('\n' + '***' * 20)
            # 追加11 ####################################################### end
            # print('\n' + '***' * 20)

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

                    # print(u'次を調べます。')
                    srcList_copy.pop()
                    tgtList_copy.pop()
                    counter += 1
                    # print('***' * 5 + '\n')
                else:
                    # print('***' * 5)
                    # print(u'{}巡目'.format(counter))
                    # print(u'{} \n\tと \n{} \n\tは、'.format(srcList_copy, tgtList_copy))
                    # print(u'最後のリスト要素 [-1] が一致していないので、当ツールでは互いの親が'
                    #       u'共通で無いと認識し、skip の対象と判断しました。'
                    #       )

                    # 追加11 ####################################################### start
                    self.scriptEditor2.append_default(u'調査を終了しました。A')
                    self.scriptEditor2.append_default('***' * 5)
                    # 追加11 ####################################################### end
                    # print(u'調査を終了しました。A')
                    # print('***' * 5)

                    break
            else:  # どちらかが空になったら抜ける
                # print('***' * 5)
                # print(u'{}巡目'.format(counter))
                # print(u'{} \n\tと \n{} \n\tは、'.format(srcList_copy, tgtList_copy))
                # print(u'最後のリスト要素 [-1] が一致していないので、当ツールでは互いの親が'
                #       u'共通で無いと認識し、skip の対象と判断しました。'
                #       )

                # 追加11 ####################################################### start
                self.scriptEditor2.append_default(u'調査を終了しました。B')
                self.scriptEditor2.append_default('***' * 5)
                # 追加11 ####################################################### end
                # print(u'調査を終了しました。B')
                # print('***' * 5)

            # 追加11 ####################################################### start
            self.scriptEditor2.append_default('***' * 20)
            # 追加11 ####################################################### end
            # print('***' * 20)

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
                # 追加11 ####################################################### start
                self.scriptEditor2.append_default(u'connected all  !!!')
                # 追加11 ####################################################### end
                # print(u'connected all  !!!')

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
                # 追加11 ####################################################### start
                self.scriptEditor2.append_default(u'not connected...')
                # 追加11 ####################################################### end
                # print(u'not connected...')

        # 追加11 ####################################################### start
        self.scriptEditor2.append_default('***' * 30 + u'調査の終了\n')
        # 追加11 ####################################################### end
        # print('***' * 30 + u'調査の終了\n')

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

        # 変換箇所7
        # print(u'ノード名(name)から MDagPath オブジェクト を生成. '
        #       u'MDagPath オブジェクト: {}'.format(selList.getDagPath(0))
        #       )

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

        # 変換箇所7
        # print(u'MDagPath オブジェクト(dagpath) から フルパスを生成. '
        #       u'フルパス MDagPath オブジェクト: {}'.format(dagpath_copy)
        #       )
        # print(u'\tもしも長ーい名前が返ってきたら、scene 内で名前がダブっている可能性が高いです！！')

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

    # 単独選択ノードから単独UUID番号をゲットする関数
    def get_ID_fromSel(self, sel):  # select one node
        u""" < 単独選択ノードから単独UUID番号をゲットする関数 です >

        ::

          エラー修正1に伴う追加1

        #######################

        #.
            :param str sel: 単独選択ノード名

        #.
            :return : get_ID
                単独UUID番号
            :rtype: str

        #######################
        """
        get_ID = cmds.ls(sel, uuid = True)[0]  # 選択し終えたノードの 単独UUID番号 をゲット
        cmds.select(cl = True)
        return get_ID

    # 単独UUID番号から単独ノードを選択する関数
    def select_fromID(self, get_ID):
        u""" < 単独UUID番号から単独ノードを選択する関数 です >

        ::

          エラー修正1に伴う追加1

        #######################

        #.
            :param str get_ID: 単独UUID番号

        #######################
        """
        getNode = cmds.ls(get_ID)[0]  # 単独UUID番号 を参照して特定ノードの選択
        cmds.select(getNode, r = True)

    # 選択ノードの明示の為に準備する格納用
    # 格納用
    def initSelectionNode_storeUUID(self, lists):
        u""" < 選択ノードの明示の為に準備する格納用 関数 です >

        ::

          格納用
        """
        selectionLists = lists
        uuidSelectionLists = []
        for index in selectionLists:
            uuidSelectionLists.append(self.get_ID_fromSel(index))  # 選択ノードからIDを取得する
        cmds.select(cl = True)
        self.initSelectionNodeUUIDLists = uuidSelectionLists
        return self.initSelectionNodeUUIDLists

    # 選択ノードの明示の為の再選択用
    # 再選択用
    def initSelectionNode_reSelect(self, lists):
        u""" < 選択ノードの明示の為の再選択用 関数 です >

        ::

          再選択用
        """
        uuidSelectionLists = lists
        for index in uuidSelectionLists:
            getNode = cmds.ls(index)[0]  # 単独UUID番号 を参照して特定ノードの選択
            cmds.select(getNode, add = True)

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
    # その他 アルゴリズムとなる コマンド群 ################################################# end

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
    def ui_executeBtnCmd(self, *args):
        u""" < proc1. UI Execute ボタン押下 実行 関数です >

        ::

          proc1.5. へ渡ります
        """
        # 追加11 ####################################################### start
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
        # 追加11 ####################################################### end

        self.src = self.tFldA_set_src.getText()
        # self.src = cmds.textField('tFldA_set_src', q = True, text = True)
        self.tgt = self.tFldB_set_tgt.getText()
        # self.tgt = cmds.textField('tFldB_set_tgt', q = True, text = True)
        self.cnctAll_value = self.cBox_cnctAll.getValue()
        # self.cnctAll_value = cmds.checkBox('cBox_cnctAll', q = True, v = True)
        # print(sorcSkGeo, destSkGeo)
        src = self.src
        tgt = self.tgt
        cnctAllValue = self.cnctAll_value
        # 変更12 ########################################################## start
        if not cmds.objExists(src) or not cmds.objExists(tgt):
            # 修正10 ########################################################## start
            self.scriptEditor2.append_error(u'source, target について、'
                                            u'片方もしくは両方が '
                                            u'当シーンには存在しない為、以降の実行は中止しました。')
            # 修正10 ########################################################## start
            # print(u'source, target について、'
            #       u'片方もしくは両方が '
            #       u'当シーンには存在しない為、以降の実行は中止しました。')

            pass
        else:
            # コマンドベース
            self.command(connect = cnctAllValue, source = src, target = tgt)  # proc1.5. へ渡る
        # 変更12 ########################################################## end
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
        # 追加11 ####################################################### start
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
        # 追加11 ####################################################### end

        sels = commonCheckSelection()
        # print(sels[0])
        if not sels:
            message_warning(u'何も選択されていないため、継続実行を中止しました。'
                            u'reset したいノードを一つ選択し再度実行してください。'
                            u'connection を切断し、基から有った、ローカル数値にリセットいたします。'
                            )
        else:
            # 変換箇所7
            # print('koko2')

            # 追加11 ####################################################### start
            self.scriptEditor2.append_default(sels[0])
            # 追加11 ####################################################### end
            # print(sels[0])

            # 新規1
            # Rotate に関しては、decomposeMatrix とはダイレクト接続されていない為、
            # 独自に、decomposeMatrixNode を探し当てる関数を使用
            dCMtx = self.search_decomposeMatrixNode_Sher(sels[0])
            # dCMtx = cmds.listConnections(sels[0], t = 'decomposeMatrix') or []
            # 追加11 ####################################################### start
            self.scriptEditor2.append_default(f'\t\tfind this node: {dCMtx}')
            # 追加11 ####################################################### end
            # print(f'\t\tfind this node: {dCMtx}')

            isJoint = commonCheckJoint(sels[0])  # joint かどうか、return bool

            # joint の時、特殊
            if isJoint:
                pass
                # 変更箇所1
                # qTElr = cmds.listConnections(sels[0], t = 'quatToEuler') or []
                # # print(self.newNodesAll)
                # # print(qTElr)
                # if not qTElr:
                #     pass
                #     message_warning(u'quatToEuler 等のコネクションが見当たりません。'
                #                     u'matrix を利用した ペアレントコンストレイン でない可能性が'
                #                     u'充分考えられます。'
                #                     )
                # else:
                #     # break connection and delete all nodes
                #     print('***' * 15)
                #     print('joint only job, \n'
                #           '\tbreak connection and delete some nodes..done'
                #           )
                #     cmds.delete(qTElr[0])
                #     print('***' * 15 + '\n')
            # 継続して。。
            # 共通
            if not dCMtx:
                pass
                message_warning(u'以下、どちらかの理由により実行を中断しました。\n'
                                u'①: ターゲットである、{} への接続に一部欠損が充分考えられます。\n'
                                u'②: decomposeMatrix 等のコネクションが見当たりません。'
                                u'matrix を利用した ペアレントコンストレイン でない可能性が'
                                u'充分考えられます。'
                                .format(sels[0])
                                )
            else:
                # initT, initR, initS, initSH = [], [], [], []
                # 変更箇所1
                # initT = []
                # exist_initT = cmds.listAttr(sels[0], st = 'initT') or []
                # if exist_initT:
                #     initT = cmds.getAttr('{}.initT'.format(sels[0]))[0]

                initSH = []

                # 変更箇所1
                # exist_initR = cmds.listAttr(sels[0], st = 'initR') or []
                # if exist_initR:
                #     initR = cmds.getAttr('{}.initR'.format(sels[0]))[0]

                # 変更箇所1
                # exist_initS = cmds.listAttr(sels[0], st = 'initS') or []
                # if exist_initS:
                #     initS = cmds.getAttr('{}.initS'.format(sels[0]))[0]

                # 変更箇所1
                exist_initSH = cmds.listAttr(sels[0], st = 'initSH') or []
                if exist_initSH:
                    initSH = cmds.getAttr('{}.initSH'.format(sels[0]))[0]

                # 変更箇所1
                # if not exist_initT and not exist_initR and not exist_initS and not exist_initSH:
                #     pass
                #     message_warning(u'decomposeMatrix 等のコネクションは見当たるのですが、'
                #                     u'reset を実行するための、独自 attribute である、'
                #                     u'user defined init attr 群が見当たりません。'
                #                     u'当ツールを利用した ペアレントコンストレイン を実行していない'
                #                     u'可能性が'
                #                     u'充分考えられます。'
                #                     u'先ず初めに、'
                #                     u'当ツールを利用した ペアレントコンストレイン を実行している'
                #                     u'必要があります。'
                #                     )
                if not exist_initSH:
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
                    # 追加11 ####################################################### start
                    self.scriptEditor2.append_default('***' * 15)
                    self.scriptEditor2.append_default('common job, \n'
                          '\tbreak connection and delete all nodes..done'
                          )
                    # 追加11 ####################################################### end
                    # print('***' * 15)
                    # print('common job, \n'
                    #       '\tbreak connection and delete all nodes..done'
                    #       )

                    # 新規2
                    # 独自に、multMatrixNode を探し当てる関数を使用
                    mMtx = self.search_multMatrixNode_Sher(dCMtx)
                    # 追加11 ####################################################### start
                    self.scriptEditor2.append_default(f'\t\tfind this node: {mMtx}')
                    # 追加11 ####################################################### end
                    # print(f'\t\tfind this node: {mMtx}')

                    # 追加11 ####################################################### start
                    self.scriptEditor2.append_default(f'\tdelete those nodes: {dCMtx, mMtx}')
                    # 追加11 ####################################################### end
                    # print(f'\tdelete those nodes: {dCMtx, mMtx}')

                    cmds.delete(dCMtx, mMtx)

                    # print(self.newNodesAll)
                    #
                    # for index in self.newNodesAll:
                    #     if cmds.objExists(index):
                    #         cmds.delete(index)

                    # 新規1 # 新規に作成された utilityNode を一括でリスト登録する関数 を利用
                    self.newNodesAll = self.check_utilityNode_Connections_Sher(sels[0])
                    # 追加11 ####################################################### start
                    self.scriptEditor2.append_default(f'\t\tfind those nodes: {self.newNodesAll}')
                    # 追加11 ####################################################### end
                    # print(f'\t\tfind those nodes: {self.newNodesAll}')

                    # 修正箇所9 ########################################### start
                    # joint かつ self.newNodesAll が空っぽなら
                    if not self.newNodesAll and isJoint:
                        pass
                        message_warning(u'幾つかのコネクションに'
                                        u'想定外な接続が見つかりました。'
                                        u'実行は中断されました。'
                                        )
                    # self.newNodesAll が空っぽでないなら、joint を含み それ以外でもなんでも
                    elif self.newNodesAll:
                        # 変換箇所7
                        # 追加11 ####################################################### start
                        self.scriptEditor2.append_default(f'\tdelete those nodes: {self.newNodesAll}')
                        # 追加11 ####################################################### end
                        # print(f'\tdelete those nodes: {self.newNodesAll}')

                        cmds.delete(self.newNodesAll)
                    # 修正箇所9 ########################################### end

                    # 修正箇所9 ########################################### start
                    # joint を含み それ以外でもなんでも 以下実行
                    # インデント レベル を1つ上げる
                    # 追加11 ####################################################### start
                    self.scriptEditor2.append_default('***' * 15 + '\n')
                    # 追加11 ####################################################### end
                    # print('***' * 15 + '\n')

                    # reset attr, from user defined attr
                    # 追加11 ####################################################### start
                    self.scriptEditor2.append_default('***' * 15)
                    self.scriptEditor2.append_default('reset job, \n'
                          '\treset attr, from user defined attr..done'
                          )
                    # 追加11 ####################################################### end
                    # print('***' * 15)
                    # print('reset job, \n'
                    #       '\treset attr, from user defined attr..done'
                    #       )

                    # 変更箇所1
                    # for axis, para in zip(list('xyz'), initT):
                    #     cmds.setAttr('{}.t{}'.format(sels[0], axis), para)
                    # for axis, para in zip(list('xyz'), initR):
                    #     cmds.setAttr('{}.r{}'.format(sels[0], axis), para)

                    # 変更箇所1
                    # for axis, para in zip(list('xyz'), initS):
                    #     cmds.setAttr('{}.s{}'.format(sels[0], axis), para)

                    # 変更箇所1
                    for axis, para in zip(['xy', 'xz', 'yz'], initSH):
                        cmds.setAttr('{}.sh{}'.format(sels[0], axis), para)
                    # 追加11 ####################################################### start
                    self.scriptEditor2.append_default('***' * 15 + '\n')
                    # 追加11 ####################################################### end
                    # print('***' * 15 + '\n')

                    # delete user defined attr
                    # 追加11 ####################################################### start
                    self.scriptEditor2.append_default('***' * 15)
                    self.scriptEditor2.append_default('delete job, \n'
                          '\tdelete user defined attr..done'
                          )
                    # 追加11 ####################################################### end
                    # print('***' * 15)
                    # print('delete job, \n'
                    #       '\tdelete user defined attr..done'
                    #       )

                    self.delInitAttr_Sher(sels[0])

                    # 追加11 ####################################################### start
                    self.scriptEditor2.append_default('***' * 15)
                    # 追加11 ####################################################### end
                    # print('***' * 15)

                    # 追加
                    tgt = sels[0]
                    self.commonResultPrintOut_brkAndRest_version(tgt)  # スクリプトベース 切断実行文を生成する関数
                    message(u'shear '
                            u'に関連する '
                            u'connection を全て削除しました。'
                            u'また、当ツールを使用した、'
                            u'shearConstraintByMatrix を実行する前の、ローカル数値への'
                            u'リセットも行いました。'
                            u'ご確認ください。'
                            )
                    # 修正箇所9 ########################################### end
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
    # 新規のノード作成及び、source target の Shear との接続を行う。
    # また、jointについては、jointOrient との接続もしている。
    # 辞書型引数を複数持つ、当関数 command を必ず経由します
    def command(self, *args, **kwargs):
        u""" < proc1.5.>

        ::

          新規のノード作成及び、source target の Shear との接続を行う。
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
        # 追加11 ####################################################### start
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
        # 追加11 ####################################################### end

        # 追加11 ####################################################### start
        self.scriptEditor2.append_default('\n' + '***' * 20)
        self.scriptEditor2.append_default('kwargs : {}'.format(kwargs))
        # 追加11 ####################################################### end
        # print('\n' + '***' * 20)
        # print('kwargs : {}'.format(kwargs))

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
        # 追加11 ####################################################### start
        self.scriptEditor2.append_default('connect : {}'.format(connectAll))
        # 追加11 ####################################################### end
        # print('connect : {}'.format(connectAll))

        src = kwargs.get('source', kwargs.get('src', val1))  # longName shortName を考慮
        # 追加11 ####################################################### start
        self.scriptEditor2.append_default('source : {}'.format(src))
        # 追加11 ####################################################### end
        # print('source : {}'.format(src))

        tgt = kwargs.get('target', kwargs.get('tgt', val2))  # longName shortName を考慮
        # 追加11 ####################################################### start
        self.scriptEditor2.append_default('target : {}'.format(tgt))
        # 追加11 ####################################################### end
        # print('target : {}'.format(tgt))

        # 追加11 ####################################################### start
        self.scriptEditor2.append_default('***' * 20 + '\n')
        # 追加11 ####################################################### end
        # print('***' * 20 + '\n')

        self.cnctAll_value = connectAll
        self.src = src
        self.tgt = tgt
        self.outPutNode = ''
        self.inPutNode = ''

        if len(src) and len(tgt):  # src, tgt 共に入力セッティングされていれば、実行
            if connectAll:  # 全ての接続を実行
                # 追加11 ####################################################### start
                self.scriptEditor2.append_default(u'source, target 共に set 入力されているため、継続実行しています。')
                # 追加11 ####################################################### end
                # print(u'source, target 共に set 入力されているため、継続実行しています。')

                strsCompLists = self.nodeName_decomp_exeB(src)  # under bar 3 or 2 version
                if strsCompLists is None:
                    strsCompLists = self.nodeName_decomp_exeC(src)  # no under bar version

                # 追加11 ####################################################### start
                self.scriptEditor2.append_default(strsCompLists)
                # 追加11 ####################################################### end
                # print(strsCompLists)

                # ##############################
                # print(u'strsCompLists\n\t'
                #       u'strsCompLists : \n\t\t'
                #       u'{}'.format(strsCompLists)
                #       )
                # ##############################

                # ####################### sample type_checked ###############
                # print('koko')
                # x = type_checked(utilNodeShortNameSet, str)
                # print(x)
                # ####################### sample type_checked ###############

                cmds.createNode('multMatrix')
                utilNodeShortNameSet = 'mult Mtrx' + 'Sher'  # 変更箇所1
                self.strCompLists_count_caseDividing_exe(strsCompLists
                                                         , utilNodeShortNameSet
                                                         )  # naming
                self.mM = cmds.ls(sl = True)[0]
                mM = self.mM

                cmds.createNode('decomposeMatrix')
                utilNodeShortNameSet = 'dcmp Mtrx' + 'Sher'  # 変更箇所1
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

                # 追加11 ####################################################### start
                self.scriptEditor2.append_default(u'target の node type は {} で実行中。。\n'.format(cmds.nodeType(tgt)))
                # 追加11 ####################################################### end
                # print(u'target の node type は {} で実行中。。\n'.format(cmds.nodeType(tgt)))

                if cmds.nodeType(tgt) == 'joint':  # tgt が joint の場合
                    # 先ず, quatNodes系 plug-in の check
                    # checkQuatNodePlugIn()

                    # matrix を利用した parentConstraint を可能とするメイン関数
                    dupTgt, newNodes = self.commonCommand(src, tgt, nodeAll)

                    # print(dupTgt)

                    cmds.createNode('eulerToQuat')
                    utilNodeShortNameSet = 'elerTo Quat' + 'Sher'  # 変更箇所1
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
                    utilNodeShortNameSet = 'quat Invt' + 'Sher'  # 変更箇所1
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
                    utilNodeShortNameSet = 'quat Prod' + 'Sher'  # 変更箇所1
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
                    utilNodeShortNameSet = 'quatTo Eler' + 'Sher'  # 変更箇所1
                    self.strCompLists_count_caseDividing_exe(strsCompLists
                                                             , utilNodeShortNameSet
                                                             )  # naming
                    qTEr = cmds.ls(sl = True)[0]
                    cmds.connectAttr("{}.outputQuat".format(qPrd)
                                     , "{}.inputQuat".format(qTEr)
                                     , f = True
                                     )
                    newNodes.append(qTEr)

                    # 生かさない箇所1 # 一旦不必要な箇所としています
                    # cmds.connectAttr("{}.outputQuat".format(dM)
                    #                  , "{}.input1Quat".format(qPrd)
                    #                  , f = True
                    #                  )

                    # cmds.connectAttr("%s.outputRotateX" % qTEr, "%s.rotateX" % tgt, f = True)
                    # cmds.connectAttr("%s.outputRotateY" % qTEr, "%s.rotateY" % tgt, f = True)
                    # cmds.connectAttr("%s.outputRotateZ" % qTEr, "%s.rotateZ" % tgt, f = True)

                    self.outPutNode = qTEr
                    self.inPutNode = tgt
                    self.outPutNode2 = dM

                    # 変更箇所1
                    # memo): jointOrient考慮した方が良いのか怪しい。。。
                    # memo): 以下の箇所のコメントアウトを解放することで、jointOrient考慮した仕様に変更しますが、後の工程に支障が出ます。
                    # Rotate connected.. ################################# start
                    # print('***' * 15)
                    # print('outPutNode : {}, inPutNode : {}'.format(qTEr, tgt))
                    # print(self.outPutNode, self.inPutNode)
                    # print('***' * 15)
                    # print('Rotate connected..')
                    # self.oP2iP_cnctR_exe(self.outPutNode, self.inPutNode)
                    # Rotate connected.. ################################### end

                    # 変更箇所1
                    # Translate, Scale, Shear connected.. ################ start
                    # print('outPutNode2 : {}, inPutNode : {}'.format(dM, tgt))
                    # print(self.outPutNode2, self.inPutNode)
                    # print('***' * 15)
                    # print('Translate, Scale, Shear connected..')
                    # self.oP2iP_cnctTSSh_exe(self.outPutNode2, self.inPutNode)
                    # Translate, Scale, Shear connected.. ################## end

                    # 変更箇所1
                    # Translate connected.. ############################## start
                    # print('outPutNode2 : {}, inPutNode : {}'.format(dM, tgt))
                    # print(self.outPutNode2, self.inPutNode)
                    # print('***' * 15)
                    # print('Translate connected..')
                    # self.oP2iP_cnctT_exe(self.outPutNode2, self.inPutNode)
                    # Translate connected.. ################################ end

                    # 変更箇所1
                    # Scale, Shear connected.. ################ start
                    # print('outPutNode2 : {}, inPutNode : {}'.format(dM, tgt))
                    # print(self.outPutNode2, self.inPutNode)
                    # print('***' * 15)
                    # print('Scale, Shear connected..')
                    # self.oP2iP_cnctS_exe(self.outPutNode2, self.inPutNode)
                    # Scale, Shear connected.. ################## end

                    # 変更箇所1
                    # Shear connected.. ################ start
                    # 追加11 ####################################################### start
                    self.scriptEditor2.append_default('outPutNode2 : {}, inPutNode : {}'.format(dM, tgt))
                    # self.scriptEditor2.append_default(self.outPutNode2, self.inPutNode)
                    self.scriptEditor2.append_default('***' * 15)
                    self.scriptEditor2.append_default('Shear connected..')
                    # 追加11 ####################################################### end
                    # print('outPutNode2 : {}, inPutNode : {}'.format(dM, tgt))
                    # print(self.outPutNode2, self.inPutNode)
                    # print('***' * 15)
                    # print('Shear connected..')

                    self.oP2iP_cnctSh_exe(self.outPutNode2, self.inPutNode)
                    # Shear connected.. ################## end

                    cmds.setAttr('{}.visibility'.format(dupTgt), 0)
                    # cmds.select(cl = True)
                    # 複製しておいた dupTgt は余計なので削除
                    cmds.delete(dupTgt)
                    newNodes.remove(dupTgt)  # リストからも削除する

                    # 全部選択
                    # 追加11 ####################################################### start
                    self.scriptEditor2.append_default(u'新規で作成されたノードは %s です。' % newNodes)
                    # 追加11 ####################################################### end
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

                    # 変更箇所1
                    # memo): jointOrient考慮した方が良いのか怪しい。。。
                    # memo): 以下の箇所のコメントアウトを解放することで、jointOrient考慮した仕様に変更しますが、後の工程に支障が出ます。
                    # Rotate connected.. ################################# start
                    # print('***' * 15)
                    # print('outPutNode : {}, inPutNode : {}'.format(dM, tgt))
                    # print(self.outPutNode, self.inPutNode)
                    # print('***' * 15)
                    # print('Rotate connected..')
                    # self.oP2iP_cnctR_exe(self.outPutNode, self.inPutNode)
                    # Rotate connected.. ################################### end

                    # 変更箇所1
                    # Translate, Scale, Shear connected.. ################ start
                    # print('outPutNode : {}, inPutNode : {}'.format(dM, tgt))
                    # print(self.outPutNode, self.inPutNode)
                    # print('***' * 15)
                    # print('Translate, Scale, Shear connected..')
                    # self.oP2iP_cnctTSSh_exe(self.outPutNode, self.inPutNode)
                    # Translate, Scale, Shear connected.. ################## end

                    # Translate connected.. ############################## start
                    # print('outPutNode : {}, inPutNode : {}'.format(dM, tgt))
                    # print(self.outPutNode, self.inPutNode)
                    # print('***' * 15)
                    # print('Translate connected..')
                    # self.oP2iP_cnctT_exe(self.outPutNode, self.inPutNode)
                    # Translate connected.. ################################ end

                    # 変更箇所1
                    # Scale, Shear connected.. ################ start
                    # print('outPutNode : {}, inPutNode : {}'.format(dM, tgt))
                    # print(self.outPutNode, self.inPutNode)
                    # print('***' * 15)
                    # print('Scale, Shear connected..')
                    # self.oP2iP_cnctS_exe(self.outPutNode, self.inPutNode)
                    # Scale, Shear connected.. ################## end

                    # 変更箇所1
                    # Shear connected.. ################ start
                    # 追加11 ####################################################### start
                    self.scriptEditor2.append_default('outPutNode : {}, inPutNode : {}'.format(dM, tgt))
                    # self.scriptEditor2.append_default(self.outPutNode, self.inPutNode)
                    self.scriptEditor2.append_default('***' * 15)
                    self.scriptEditor2.append_default('Shear connected..')
                    # 追加11 ####################################################### end
                    # print('outPutNode : {}, inPutNode : {}'.format(dM, tgt))
                    # print(self.outPutNode, self.inPutNode)
                    # print('***' * 15)
                    # print('Shear connected..')

                    self.oP2iP_cnctSh_exe(self.outPutNode, self.inPutNode)
                    # Shear connected.. ################## end

                    cmds.setAttr('{}.visibility'.format(dupTgt), 0)
                    # cmds.select(cl = True)
                    # 複製しておいた dupTgt は余計なので削除
                    cmds.delete(dupTgt)
                    nodeAll.remove(dupTgt)  # リストからも削除する

                    # 全部選択
                    # 追加11 ####################################################### start
                    self.scriptEditor2.append_default(u'新規で作成されたノードは %s です。' % nodeAll)
                    # 追加11 ####################################################### end
                    # print(u'新規で作成されたノードは %s です。' % nodeAll)

                    cmds.select(nodeAll, r = True)

                    self.newNodesAll = nodeAll
                # print(u'現在、新規で作成されたノードは、全て選択された状態です。')

                # 変更箇所1
                # print('***' * 15)
                # print(u'Rotate connected..done')
                # 変更箇所1
                # print('***' * 15)
                # print(u'Translate, Scale, Shear connected..done')
                # print('***' * 15 + '\n')

                # print('***' * 15)
                # print(u'Translate connected..done')
                # print('***' * 15 + '\n')

                # print('***' * 15)
                # print(u'Scale, Shear connected..done')
                # print('***' * 15 + '\n')

                # 追加11 ####################################################### start
                self.scriptEditor2.append_default('***' * 15)
                self.scriptEditor2.append_default(u'Shear connected..done')
                self.scriptEditor2.append_default('***' * 15 + '\n')
                # 追加11 ####################################################### end
                # print('***' * 15)
                # print(u'Shear connected..done')
                # print('***' * 15 + '\n')

                # proc2. へ渡る
                self.cnctSrcHircyTgtHircy2MltMat_exe()  # proc2. へ渡る
                # 追加11 ####################################################### start
                self.scriptEditor2.append_default('***' * 15)
                self.scriptEditor2.append_default(u'Source Hierarchy, Target Hierarchy, to MultMatrix. connected..done')
                self.scriptEditor2.append_default('***' * 15 + '\n')
                # 追加11 ####################################################### end
                # print('***' * 15)
                # print(u'Source Hierarchy, Target Hierarchy, to MultMatrix. connected..done')
                print('***' * 15 + '\n')

                # ######################################################################################
                # 追加 ###################################### start
                cmds.select(tgt)
                self.params = self.getInitAttr(tgt)  # list of float, range is 12, T, R, S, SH
                # 追加11 ####################################################### start
                self.scriptEditor2.append_default('***' * 15)
                self.scriptEditor2.append_default('add attribute, user defined init attr')
                # 追加11 ####################################################### end
                # print('***' * 15)
                # print('add attribute, user defined init attr')

                self.createInitAttr_Sher(tgt)  # add user defined attr

                # 追加11 ####################################################### start
                self.scriptEditor2.append_default('***' * 15 + '\n')
                self.scriptEditor2.append_default('***' * 15)
                self.scriptEditor2.append_default('store attribute, user defined init attr')
                # 追加11 ####################################################### end
                # print('***' * 15 + '\n')
                # print('***' * 15)
                # print('store attribute, user defined init attr')

                self.setInitAttr_Sher(tgt)

                # 追加11 ####################################################### start
                self.scriptEditor2.append_default('***' * 15 + '\n')
                # 追加11 ####################################################### end
                # print('***' * 15 + '\n')

                # self.delInitAttr(tgt)  # delete user defined attr
                # 追加 ######################################## end
                # ######################################################################################

                self.commonResultPrintOut(connectAll, src, tgt)  # コマンドベースの実行文を生成する関数
                message(u'shearConstraint を'
                        u'matrix で実現'
                        u'完了しました。'
                        )
                # self.__init__()  # すべて、元の初期値に戻す
            else:  # 継続実行中止
                pass
                self.commonResultPrintOut(connectAll, src, tgt)  # コマンドベースの実行文を生成する関数
                message_warning(u'create new nodes and connect all : check'
                                u'ボタンが on されていないか、'
                                u'もしくは、コマンド connect = True 記述がなさられていないため、'
                                u'継続実行を中止しました。'
                                )
        else:  # src, tgt 共に入力セッティングされていなければ、何もしない
            pass
            self.commonResultPrintOut(connectAll, src, tgt)  # コマンドベースの実行文を生成する関数
            message_warning(u'source, target 共に set 入力されていないため、'
                            u'継続実行を中止しました。'
                            )

        # print(inspect.getargspec(self.strCompLists_count_caseDividing_exe))

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
        # 修正10 ########################################################## start
        srcP_list = cmds.listRelatives(src, p = True) or []
        if not srcP_list:
            # 追加11 ####################################################### start
            self.scriptEditor2.append_default("親ノード: なし。world 空間です。")
            # 追加11 ####################################################### end
            # print("親ノード: なし。world 空間です。")

            pass
        else:
            self.srcP = srcP_list[0]
            # 追加11 ####################################################### start
            self.scriptEditor2.append_default(f"親ノード: {self.srcP}")
            # 追加11 ####################################################### end
            # print(f"親ノード: {self.srcP}")

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
        # 修正10 ########################################################## end

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
        className = self.className
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
        # 追加11 ####################################################### start
        self.scriptEditor2.append_default('\n' + '***' * 20)
        self.scriptEditor2.append_default('kwargs : {}'.format(kwargs))
        # 追加11 ####################################################### end
        # print('\n' + '***' * 20)
        # print('kwargs : {}'.format(kwargs))

        # target
        key0 = list(kwargs.keys())[0]  # 変換箇所6
        val0 = kwargs.get(key0)

        tgt = kwargs.get('target', kwargs.get('tgt', val0))  # longName shortName を考慮
        # 追加11 ####################################################### start
        self.scriptEditor2.append_default('target : {}'.format(tgt))
        # 追加11 ####################################################### end
        # print('target : {}'.format(tgt))

        # 追加11 ####################################################### start
        self.scriptEditor2.append_default('***' * 20 + '\n')
        # 追加11 ####################################################### end
        # print('***' * 20 + '\n')

        if len(tgt):  # tgt に入力セッティングされていれば、実行
            cmds.select(tgt)
            self.breakAndReset()
            # self.__init__()  # すべて、元の初期値に戻す
        else:  # tgt に入力セッティングされていなければ、何もしない
            pass
            message_warning(u'target に set 入力されていないため、'
                            u'継続実行を中止しました。'
                            )
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
        className = self.className
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

    # 独自規格 attribute 操作一連群 ##################################################### start
    # 追加
    # get initial attribute
    def getInitAttr(self, tgt, *args):
        u""" <get initial attribute>

        ::

          変更箇所1
          追加

        #########################

            :return: params
                range is 12
                [Tx, Ty, Tz, Rx, Ry, Rz, Sx, Sy, Sz, Shxy, Shxz, Shyz]

            :rtype: list of float

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

    # 変更箇所1
    # 追加
    # add attribute, user defined initial attribute
    def createInitAttr_Sher(self, tgt, *args):
        u""" <add attribute, user defined initial attribute>

        ::

          変更箇所1
          追加
        """
        # print (tgt)
        # create init S
        # for ch in list('S'):
        #     cmds.addAttr(tgt, ln = "init{}".format(ch), at = 'double3')
        #     for axis in list('xyz'):
        #         cmds.addAttr(tgt, ln = "init{}{}".format(ch, axis)
        #                      , p = 'init{}'.format(ch), at = 'double'
        #                      )
        #     cmds.setAttr("{}.init{}".format(tgt, ch), 0, 0, 0, type = 'double3')
        # create init Shear
        cmds.addAttr(tgt, ln = "initSH", at = 'double3')
        for axis in ['xy', 'xz', 'yz']:
            cmds.addAttr(tgt, ln = "initSH{}".format(axis)
                         , p = 'initSH', at = 'double'
                         )

    # 変更箇所1
    # 追加
    # store attribute, to user defined initial attribute
    def setInitAttr_Sher(self, tgt, *args):
        u""" <store attribute, to user defined initial attribute>

        ::

          変更箇所1
          追加
        """
        # exist_initT = cmds.listAttr(tgt, st = 'initT') or []
        # exist_initR = cmds.listAttr(tgt, st = 'initR') or []
        # exist_initS = cmds.listAttr(tgt, st = 'initS') or []
        exist_initSH = cmds.listAttr(tgt, st = 'initSH') or []
        # if not exist_initT and not exist_initR and not exist_initS and not exist_initSH:
        #     pass
        # if not exist_initS and not exist_initSH:
        #     pass
        if not exist_initSH:
            pass
        else:
            # print(self.params)  # list of float, range is 12, T, R, S, SH
            paraT, paraR , paraS = self.params[0:3], self.params[3:6], self.params[6:9]
            paraSH = self.params[9:12]

            # 変換箇所7
            # print(paraT, paraR, paraS, paraSH)

            # print(paraS, paraSH)

            # 変換箇所7
            # print(paraSH)

            # for axis, para in zip(list('xyz'), paraT):
            #     cmds.setAttr('{}.initT{}'.format(tgt, axis), para)
            # for axis, para in zip(list('xyz'), paraR):
            #     cmds.setAttr('{}.initR{}'.format(tgt, axis), para)
            # for axis, para in zip(list('xyz'), paraS):
            #     cmds.setAttr('{}.initS{}'.format(tgt, axis), para)
            for axis, para in zip(['xy', 'xz', 'yz'], paraSH):
                cmds.setAttr('{}.initSH{}'.format(tgt, axis), para)

    # 変更箇所1
    # 追加
    # remove attribute, to user defined initial attribute
    def delInitAttr_Sher(self, tgt, *args):
        u""" <remove attribute, to user defined initial attribute>

        ::

          変更箇所1
          追加
        """
        # exist_initT = cmds.listAttr(tgt, st = 'initT') or []
        # exist_initR = cmds.listAttr(tgt, st = 'initR') or []
        # exist_initS = cmds.listAttr(tgt, st = 'initS') or []
        exist_initSH = cmds.listAttr(tgt, st = 'initSH') or []
        # if not exist_initT and not exist_initR and not exist_initS and not exist_initSH:
        #     pass
        # if not exist_initS and not exist_initSH:
        #     pass
        if not exist_initSH:
            pass
        else:
            # delete init S
            # for ch in list('S'):
            #     cmds.deleteAttr(tgt, at = "init{}".format(ch))
            # delete init Shear
            cmds.deleteAttr(tgt, at = "initSH")

    # 新規1
    # 新規に作成された utilityNode を一括でリスト登録する
    def check_utilityNode_Connections_Sher(self, selectionNode):
        u""" < 新規に作成された utilityNode を一括でリスト登録する関数 です >

        ::

          新規1

        #######################

        #.
            :param str selectionNode:

        #.
            :return: check_utilityNodeAll
            :rtype check_utilityNodeAll: list of str

        #######################
        """
        check_utilityNodeAll = []
        # dCMtx = cmds.listConnections(selectionNode
        #                              , c = True, p = False, d = True
        #                              , t = 'decomposeMatrix'
        #                              ) or []
        # print(dCMtx)

        # 関連する utilityNode を確実に探し当てます... ######################## start
        eTQt = cmds.listConnections(selectionNode
                                    , et = True
                                    , t = 'eulerToQuat'
                                    ) or []
        # check_utilityNodeAll.append(eTQt[0])
        for eTQt_index in eTQt:
            # print('koko4')
            # print(eTQt_index)
            qInv = cmds.listConnections(eTQt_index
                                        , et = True
                                        , t = 'quatInvert'
                                        ) or []
            # check_utilityNodeAll.append(qInv[0])
            if qInv[0] and 'Sher' in qInv[0]:  # qInv[0] is True 且つ、 文字列'Sher'を含む
                qPrd = cmds.listConnections(qInv[0]
                                            , et = True
                                            , t = 'quatProd'
                                            ) or []
                # check_utilityNodeAll.append(qPrd[0])
                if qPrd[0] and 'Sher' in qPrd[0]:  # qPrd[0] is True 且つ、 文字列'Sher'を含む
                    qTEr = cmds.listConnections(qPrd[0]
                                                , et = True
                                                , t = 'quatToEuler'
                                                ) or []
                    # check_utilityNodeAll.append(qTEr[0])
                    if qTEr[0] and 'Sher' in qTEr[0]:  # qTEr[0] is True 且つ、 文字列'Sher'を含む
                        # connectList = cmds.listConnections(qTEr[0]
                        #                                    , c = True
                        #                                    , source = False
                        #                                    , destination = True
                        #                                    ) or []
                        # # print('koko5')
                        # print(connectList)
                        # if len(connectList):
                        #     pass
                        # if not connectList:  # コネクションがされていなかったら 真 で実行
                        #     check_utilityNodeAll.append(eTQt_index)
                        #     check_utilityNodeAll.append(qInv[0])
                        #     check_utilityNodeAll.append(qPrd[0])
                        #     check_utilityNodeAll.append(qTEr[0])

                        # print('koko5')
                        isConnectedRxyz = []  # list[bool] of range is 3
                        for axisIndex in 'XYZ':
                            outputR = 'outputRotate' + axisIndex
                            r = 'rotate' + axisIndex
                            isConnectedR = cmds.isConnected('{}.{}'
                                                            .format(qTEr[0], outputR)
                                                            , '{}.{}'
                                                            .format(selectionNode, r)
                                                            )
                            isConnectedRxyz.append(isConnectedR)
                            # isConnectedRx = cmds.isConnected('{}.outputRotate'.format(qTEr[0])
                            #                              , '{}.rotateX'.format(selectionNode)
                            #                              )
                        # print(isConnectedRxyz)
                        if any(isConnectedRxyz):  # 3つの要素の内少なくとも1つがTrueである場合 真 で実行
                            pass
                        elif all(x for x in isConnectedRxyz):  # 3つの要素全てがTrueである場合 真 で実行
                            pass
                        # [False, False, False]
                        else:  # 3つの要素全てがFalse、つまり全てコネクションがされていなかったら 真 で実行
                            check_utilityNodeAll.append(eTQt_index)
                            check_utilityNodeAll.append(qInv[0])
                            check_utilityNodeAll.append(qPrd[0])
                            check_utilityNodeAll.append(qTEr[0])
        # 関連する utilityNode を確実に探し当てます... ########################## end
        return check_utilityNodeAll

    # 新規1
    # 新規に作成された utilityNode の decomposeMatrixNode のみを探し当てる
    def search_decomposeMatrixNode_Sher(self, selectionNode):
        u""" < 新規に作成された utilityNode の decomposeMatrixNode のみを探し当てる関数 です >

        ::

          新規1

        #######################

        #.
            :param str selectionNode:

        #.
            :return: dCMtxNode
            :rtype dCMtxNode: str

        #######################
        """
        dCMtxNode = ''
        # check_utilityNodeAll = []

        # dCMtx = cmds.listConnections(selectionNode
        #                              , c = True, p = False, d = True
        #                              , t = 'decomposeMatrix'
        #                              ) or []
        # print(dCMtx)

        # decomposeMatrix を確実に探し当てるために... ######################## start
        # qTEr = cmds.listConnections(selectionNode
        #                             , et = True
        #                             , t = 'quatToEuler'
        #                             ) or []
        # # check_utilityNodeAll.append(qTEr[0])

        # dCMtxOutSX = cmds.listConnections('{}.sx'.format(selectionNode)
        #                                   , et = True
        #                                   , t = 'decomposeMatrix'
        #                                   ) or []
        # dCMtxOutSY = cmds.listConnections('{}.sy'.format(selectionNode)
        #                                   , et = True
        #                                   , t = 'decomposeMatrix'
        #                                   ) or []
        # dCMtxOutSZ = cmds.listConnections('{}.sz'.format(selectionNode)
        #                                   , et = True
        #                                   , t = 'decomposeMatrix'
        #                                   ) or []

        dCMtxOutShXY = cmds.listConnections('{}.shxy'.format(selectionNode)
                                            , et = True
                                            , t = 'decomposeMatrix'
                                            ) or []
        dCMtxOutShXZ = cmds.listConnections('{}.shxz'.format(selectionNode)
                                            , et = True
                                            , t = 'decomposeMatrix'
                                            ) or []
        dCMtxOutShYZ = cmds.listConnections('{}.shyz'.format(selectionNode)
                                            , et = True
                                            , t = 'decomposeMatrix'
                                            ) or []
        # decomposeMatrix を確実に探し当てるために... ########################## end
        # if not any(dCMtxOutSX and dCMtxOutSY and dCMtxOutSZ
        #            and dCMtxOutShXY and dCMtxOutShXZ and dCMtxOutShYZ
        #            ):  # 6つの要素の内少なくとも1つがFalseである場合 真 で実行
        #     pass
        #     print('any or all None')
        if not any(dCMtxOutShXY and dCMtxOutShXZ and dCMtxOutShYZ
                   ):  # 3つの要素の内少なくとも1つがFalseである場合 真 で実行
            pass
            # 追加11 ####################################################### start
            self.scriptEditor2.append_default('any or all None')
            # 追加11 ####################################################### end
            # print('any or all None')

        # elif (dCMtxOutSX and dCMtxOutSY and dCMtxOutSZ
        #       and dCMtxOutShXY and dCMtxOutShXZ and dCMtxOutShYZ):  # 6つの要素全てがTrue、つまりコネクションがされていたら 真 で実行
        #     dCMtxNode = dCMtxOutSX[0]
        elif dCMtxOutShXY and dCMtxOutShXZ and dCMtxOutShYZ:  # 6つの要素全てがTrue、つまりコネクションがされていたら 真 で実行
            dCMtxNode = dCMtxOutShXY[0]
        return dCMtxNode

    # 新規2
    # 新規に作成された utilityNode の multMatrixNode のみを探し当てる
    def search_multMatrixNode_Sher(self, selectionNode):
        u""" < 新規に作成された utilityNode の decomposeMatrixNode のみを探し当てる関数 です >

        ::

          新規2

        #######################

        #.
            :param str selectionNode:

        #.
            :return: mMtxNode
            :rtype mMtxNode: str

        #######################
        """
        mMtxNode = ''
        mMtx = cmds.listConnections('{}.inputMatrix'.format(selectionNode)
                                    , source = True
                                    , destination = False
                                    , type = 'multMatrix'
                                    ) or []
        if mMtx[0] and 'Sher' in mMtx[0]:  # mMtx[0] is True 且つ、 文字列'Trans'を含む
            mMtxNode = mMtx[0]
        return mMtxNode
    # 独自規格 attribute 操作一連群 ####################################################### end


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
