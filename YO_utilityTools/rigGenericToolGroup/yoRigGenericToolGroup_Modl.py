# -*- coding: utf-8 -*-

u"""
yoRigGenericToolGroup_Modl.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -5.5-
:Date: 2024/05/17

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PySide2 version: 5.15.2

-リマインダ-
    done: 2024/05/17
        - 追加6 と 変更6 と 新規6
            - 概要: ***_View モジュール の tabB の
                IHIツールの Hide, Show の呼び出し の改善
                に伴う、
                当 ***_Modl モジュール への関連を 変更
            - 詳細:
                ::

                    +   # 全タブ 用
                        # 各ツールの UI起動の呼び出し 関数
                        def call_eachToolUIBoot(self, caseIndex: str = None):
                            ...
                            switch_dict = {...
                                           # 追加6
                                           'caseB3hide': lambda: isHistInter.hide(),
                                           'caseB3show': lambda: isHistInter.show(),
                                           ...
                                           }
                           ...

                    +   # 変更6 ############################################################### start
                        # 未使用にしたので、以下は一旦キャンセルにしました。
                        # # 追加4
                        # # タブB 用 (group2)
                        # # IHIツールの Hide, Show の呼び出し 関数
                        # def call_eachToolCommandBoot(self, caseIndexOption: str = None):
                        #     ...
                        # 変更6 ############################################################### end
        version = '-5.5-'

    done: 2024/05/08
        追加と変更と新規5
            - 概要: ***_View モジュール へ 新規tabF の 追加に伴う、
                当 ***_Modl モジュール への関連を 追加
            - 詳細:
                ::

                    +   # 追加と変更と新規5
                        # caseF ################################################################## start
                        try:
                            from ..skinWeightsExpImpTool import yoSkinWeightsExpImpTool_main
                        except (ModuleNotFoundError, ImportError):
                            yoSkinWeightsExpImpTool_main = None
                            sendWarningInformation('yoSkinWeightsExpImpTool_main')
                        # caseF ################################################################## end

                    +   # 全タブ 用
                        # 各ツールの UI起動の呼び出し 関数
                        def call_eachToolUIBoot(self, caseIndex: str = None):
                            ...
                            switch_dict = {...
                                           # 追加と変更と新規5
                                           'caseF1': lambda: yoSkinWeightsExpImpTool_main.main(),
                                           }
                            ...
        version = '-5.1-'

    done: 2024/05/01
        追加4
            - 概要: ***_View モジュール の tabB へ
                IHIツールの Hide, Show の呼び出し 追加
                に伴う、当 ***_Modl モジュール への関連を 追加
            - 詳細:
                ::

                    +   # 追加4
                        # caseB3 ################################################################# start
                        try:
                            from .. import yoIsHistoricallyInteresting as isHistInter
                        except (ModuleNotFoundError, ImportError):
                            isHistInter = None
                            sendWarningInformation('isHistInter')
                        # caseB3 ################################################################# end

                    +   # 追加4
                        # タブB 用 (group2)
                        # IHIツールの Hide, Show の呼び出し 関数
                        def call_eachToolCommandBoot(self, caseIndexOption: str = None):
                            ...
        version = '-5.0-'

    done: 2024/04/11~2024/04/17
        追加3
            - 概要: ***_View モジュール の tabA,D の 各ツールの
                Help の呼び出し 追加
                コマンド実行する記述例 の呼び出し 追加
                に伴う、
                当 ***_Modl モジュール への関連を 追加
            - 詳細:
                ::

                    +   # 追加3
                        try:
                            from ..renameTool import config as renameToolConfig
                        except (ModuleNotFoundError, ImportError):
                            renameToolConfig = None
                            sendWarningInformation('renameToolConfig')
                        try:
                            from ..renameTool.config import CommandExample as renameToolCommandExample
                        except (ModuleNotFoundError, ImportError):
                            renameToolCommandExample = None
                            sendWarningInformation('renameToolCommandExample')

                    +   # 追加3
                        try:
                            from ..createSpaceNode import config as createSpaceNodeConfig
                        except (ModuleNotFoundError, ImportError):
                            createSpaceNodeConfig = None
                            sendWarningInformation('createSpaceNodeConfig')
                        try:
                            from ..createSpaceNode.config import CommandExample as createSpaceNodeCommandExample
                        except (ModuleNotFoundError, ImportError):
                            createSpaceNodeCommandExample = None
                            sendWarningInformation('createSpaceNodeCommandExample')

                    +   # 追加3
                        try:
                            from ..pointConstraintByMatrix import config as pConByMatConfig
                        except (ModuleNotFoundError, ImportError):
                            pConByMatConfig = None
                            sendWarningInformation('pConByMatConfig')
                        try:
                            from ..pointConstraintByMatrix.config import CommandExample as pConByMatCommandExample
                        except (ModuleNotFoundError, ImportError):
                            pConByMatCommandExample = None
                            sendWarningInformation('pConByMatCommandExample')

                    +   # 追加3
                        try:
                            from ..orientConstraintByMatrix import config as oConByMatConfig
                        except (ModuleNotFoundError, ImportError):
                            oConByMatConfig = None
                            sendWarningInformation('oConByMatConfig')
                        try:
                            from ..orientConstraintByMatrix.config import CommandExample as oConByMatCommandExample
                        except (ModuleNotFoundError, ImportError):
                            oConByMatCommandExample = None
                            sendWarningInformation('oConByMatCommandExample')

                    +   # 追加3
                        try:
                            from ..scaleConstraintByMatrix import config as scConByMatConfig
                        except (ModuleNotFoundError, ImportError):
                            scConByMatConfig = None
                            sendWarningInformation('scConByMatConfig')
                        try:
                            from ..scaleConstraintByMatrix.config import CommandExample as scConByMatCommandExample
                        except (ModuleNotFoundError, ImportError):
                            scConByMatCommandExample = None
                            sendWarningInformation('scConByMatCommandExample')

                    +   # 追加3
                        try:
                            from ..shearConstraintByMatrix import config as shConByMatConfig
                        except (ModuleNotFoundError, ImportError):
                            shConByMatConfig = None
                            sendWarningInformation('shConByMatConfig')
                        try:
                            from ..shearConstraintByMatrix.config import CommandExample as shConByMatCommandExample
                        except (ModuleNotFoundError, ImportError):
                            shConByMatCommandExample = None
                            sendWarningInformation('shConByMatCommandExample')

                    +   # 追加3
                        # タブD 用 (group4)
                        # 各ツールの Help起動の呼び出し 関数
                        def call_eachToolHelpBoot(self, caseIndex: str = None):
                            ...

                    +   # 追加3
                        # タブD 用 (group4)
                        # 各ツールの UI起動せずにコマンド実行する記述例の呼び出し 関数
                        def call_eachToolCommandExampleBoot(self, caseIndex: str = None):
                            ...
        version = '-4.0-'

    done: 2024/04/11
        追加2
            - 概要: ***_View モジュール の tabB へ YO_constraintToGeometry2 UI の呼び出し 追加
                に伴う、当 ***_Modl モジュール への関連を 追加
            - 詳細:
                ::

                    +   ...
                        # 追加2
                        try:
                            from .. import YO_constraintToGeometry2
                        except (ModuleNotFoundError, ImportError):
                            YO_constraintToGeometry2 = None
                            sendWarningInformation('YO_constraintToGeometry2')
                        ...

                    +   ...
                        switch_dict = {...
                                       # 追加2
                                       'caseB2': lambda: YO_constraintToGeometry2.UI.showUI(),
                                       ...
                                       }
                        ...
        version = '-3.1-'

    done: 2024/04/09
        追加1
            - 概要: tabE へ Node current view として reference の on/off 表示切り替え を追加
            - 詳細:
                ::

                    +   # Node: current view 表示 用
                        def call_checkBoxAction_nv(self
                                                   , caseIndex: str, cBxWid_name
                                                   , longName: str, state: int
                                                   , *args
                                                   ):
                                                   ...

        version = '-3.0-'

    done: 2024/03/17~
        新規
        version = '-2.0-'

    done: 2024/01/26~
        新規
        version = '-1.0-'

"""

# 標準ライブラリ #################################################################

# サードパーティライブラリ #########################################################
import maya.cmds as cmds
import maya.OpenMaya as om

# ローカルで作成したモジュール ######################################################
# 汎用ライブラリー の使用 ################################################################ start
from ..lib.message import message
from ..lib.message_warning import message_warning
from ..lib.commonCheckSelection import commonCheckSelection
from ..lib.commonCheckJoint import commonCheckJoint
from ..lib.commonCheckMesh import commonCheckMesh
from ..lib.commonCheckCurve import commonCheckCurve
from ..lib.commonCheckShape import commonCheckShape
# 汎用ライブラリー の使用 ################################################################## end
parentDir = 'YO_utilityTools'
def sendWarningInformation(moduleNameByString: str):
    print('\n' + '###' * 20)
    om.MGlobal.displayWarning(f'{parentDir}.{moduleNameByString}'
                              u'\n\t' + u':<NG> result: 上記の 所定の箇所 に、\n\t\t'
                                        f'{moduleNameByString}'
                                        u'\n\t\t\tが存在しません。'
                                        u'よって、ロードしませんでした。\n'
                              )
    print('###' * 20 + '\n')
# 各ツールの読み込み ############################################################## start
# 若干冗長な記述ですが、現状では、一番保守しやすい記述です
# caseA1 ################################################################# start
try:
    from ..renameTool import YO_renameTool5_main
except (ModuleNotFoundError, ImportError):
    YO_renameTool5_main = None
    sendWarningInformation('YO_renameTool5_main')
# 追加3
try:
    from ..renameTool import config as renameToolConfig
except (ModuleNotFoundError, ImportError):
    renameToolConfig = None
    sendWarningInformation('renameToolConfig')
try:
    from ..renameTool.config import CommandExample as renameToolCommandExample
except (ModuleNotFoundError, ImportError):
    renameToolCommandExample = None
    sendWarningInformation('renameToolCommandExample')
# caseA1 ################################################################# end

# caseA2 ################################################################# start
try:
    from ..createSpaceNode import YO_createSpaceNode3_main
except (ModuleNotFoundError, ImportError):
    YO_createSpaceNode3_main = None
    sendWarningInformation('YO_createSpaceNode3_main')
# 追加3
try:
    from ..createSpaceNode import config as createSpaceNodeConfig
except (ModuleNotFoundError, ImportError):
    createSpaceNodeConfig = None
    sendWarningInformation('createSpaceNodeConfig')
try:
    from ..createSpaceNode.config import CommandExample as createSpaceNodeCommandExample
except (ModuleNotFoundError, ImportError):
    createSpaceNodeCommandExample = None
    sendWarningInformation('createSpaceNodeCommandExample')
# caseA2 ################################################################# end

# caseB1 ################################################################# start
try:
    from .. import YO_nodeCreateToWorldSpace
except (ModuleNotFoundError, ImportError):
    YO_nodeCreateToWorldSpace = None
    sendWarningInformation('YO_nodeCreateToWorldSpace')
# caseB1 ################################################################# end

# 追加2
# caseB2 ################################################################# start
try:
    from .. import YO_constraintToGeometry2
except (ModuleNotFoundError, ImportError):
    YO_constraintToGeometry2 = None
    sendWarningInformation('YO_constraintToGeometry2')
# caseB2 ################################################################# end

# 追加4
# caseB3 ################################################################# start
try:
    from .. import yoIsHistoricallyInteresting as isHistInter
except (ModuleNotFoundError, ImportError):
    isHistInter = None
    sendWarningInformation('isHistInter')
# caseB3 ################################################################# end

# caseC1 ################################################################# start
try:
    from ..createClusterAndRenameTool import YO_createClusterAndRename6_main
except (ModuleNotFoundError, ImportError):
    YO_createClusterAndRename6_main = None
    sendWarningInformation('YO_createClusterAndRename6_main')

# caseC2 ################################################################# start
try:
    from ..createSpIkAndRenameTool import YO_createSpIkAndRename3_main
except (ModuleNotFoundError, ImportError):
    YO_createSpIkAndRename3_main = None
    sendWarningInformation('YO_createSpIkAndRename3_main')

# caseD ################################################################## start
try:
    from ..pointConstraintByMatrix import YO_pointConstraintByMatrix1_main
except (ModuleNotFoundError, ImportError):
    YO_pointConstraintByMatrix1_main = None
    sendWarningInformation('YO_pointConstraintByMatrix1_main')
# 追加3
try:
    from ..pointConstraintByMatrix import config as pConByMatConfig
except (ModuleNotFoundError, ImportError):
    pConByMatConfig = None
    sendWarningInformation('pConByMatConfig')
try:
    from ..pointConstraintByMatrix.config import CommandExample as pConByMatCommandExample
except (ModuleNotFoundError, ImportError):
    pConByMatCommandExample = None
    sendWarningInformation('pConByMatCommandExample')

try:
    from ..orientConstraintByMatrix import YO_orientConstraintByMatrix1_main
except (ModuleNotFoundError, ImportError):
    YO_orientConstraintByMatrix1_main = None
    sendWarningInformation('YO_orientConstraintByMatrix1_main')
# 追加3
try:
    from ..orientConstraintByMatrix import config as oConByMatConfig
except (ModuleNotFoundError, ImportError):
    oConByMatConfig = None
    sendWarningInformation('oConByMatConfig')
try:
    from ..orientConstraintByMatrix.config import CommandExample as oConByMatCommandExample
except (ModuleNotFoundError, ImportError):
    oConByMatCommandExample = None
    sendWarningInformation('oConByMatCommandExample')

try:
    from ..scaleConstraintByMatrix import YO_scaleConstraintByMatrix1_main
except (ModuleNotFoundError, ImportError):
    YO_scaleConstraintByMatrix1_main = None
    sendWarningInformation('YO_scaleConstraintByMatrix1_main')
# 追加3
try:
    from ..scaleConstraintByMatrix import config as scConByMatConfig
except (ModuleNotFoundError, ImportError):
    scConByMatConfig = None
    sendWarningInformation('scConByMatConfig')
try:
    from ..scaleConstraintByMatrix.config import CommandExample as scConByMatCommandExample
except (ModuleNotFoundError, ImportError):
    scConByMatCommandExample = None
    sendWarningInformation('scConByMatCommandExample')

try:
    from ..shearConstraintByMatrix import YO_shearConstraintByMatrix1_main
except (ModuleNotFoundError, ImportError):
    YO_shearConstraintByMatrix1_main = None
    sendWarningInformation('YO_shearConstraintByMatrix1_main')

# 追加3
try:
    from ..shearConstraintByMatrix import config as shConByMatConfig
except (ModuleNotFoundError, ImportError):
    shConByMatConfig = None
    sendWarningInformation('shConByMatConfig')
try:
    from ..shearConstraintByMatrix.config import CommandExample as shConByMatCommandExample
except (ModuleNotFoundError, ImportError):
    shConByMatCommandExample = None
    sendWarningInformation('shConByMatCommandExample')

try:
    from .. import YO_parentConstraintByMatrix5
except (ModuleNotFoundError, ImportError):
    YO_parentConstraintByMatrix5 = None
    sendWarningInformation('YO_parentConstraintByMatrix5')
try:
    from .. import YO_parentConstraintByMatrix62
except (ModuleNotFoundError, ImportError):
    YO_parentConstraintByMatrix62 = None
    sendWarningInformation('YO_parentConstraintByMatrix62')
# caseD ################################################################## end

# caseE ################################################################## start
try:
    from .. import YO_jointDrawStyle_change
except (ModuleNotFoundError, ImportError):
    YO_jointDrawStyle_change = None
    sendWarningInformation('YO_jointDrawStyle_change')
try:
    from .. import YO_jointRadiusSlider
except (ModuleNotFoundError, ImportError):
    YO_jointRadiusSlider = None
    sendWarningInformation('YO_jointRadiusSlider')
# caseE ################################################################## end

# 追加と変更と新規5
# caseF ################################################################## start
try:
    from ..skinWeightsExpImpTool import yoSkinWeightsExpImpTool_main
except (ModuleNotFoundError, ImportError):
    yoSkinWeightsExpImpTool_main = None
    sendWarningInformation('yoSkinWeightsExpImpTool_main')
# caseF ################################################################## end
# 各ツールの読み込み ############################################################## end


class RigGenTlGp_Modl(object):
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
        self.__constructor_chunk2()

    # コンストラクタのまとまり2 # タイトル等の定義
    def __constructor_chunk2(self):
        u""" < コンストラクタのまとまり2 # タイトル等の定義 です > """
        # self.title = TITLE
        # self.win = TITLE + '_ui'
        # self.space = SPACE
        # self.version = VERSION
        # self.underScore = '_'
        pass

    # 1. UI-1. メニュー コマンド群 ###################################################### start
    # Save Settings 実行による optionVar の保存 関数
    def editMenuSaveSettingsCmd(self, *args):
        u""" < Save Settings 実行による optionVar の保存 関数 です > """
        # ...
        message(f'm: {args[0]}')  # message output
        # ...

    # Reload 実行 関数
    # View へ移動...

    # Help 実行 関数
    # View へ移動...

    # Close 実行 関数
    # View へ移動...
    # 1. UI-1. メニュー コマンド群 ######################################################## end

    # 4. UI-4. OptionVar を利用したパラメータ管理 コマンド群 ############################### start
    # UI-4. optionVar からの値の復元 実行 関数
    def restoreOptionVarCmd(self, *args):
        # ...
        message(f'm: {args[0]}')  # message output
        # ...
    # 4. UI-4. OptionVar を利用したパラメータ管理 コマンド群 ################################# end

    # 2. UI-2. 追加オプション コマンド群 ################################################# start
    # UI-4. optionVar の value を default に戻す操作 関数
    def set_default_value_toOptionVar(self, *args):
        # ...
        message(f'm: {args[0]}')  # message output
        # ...
    # 2. UI-2. 追加オプション コマンド群 ################################################### end

    # その他 アルゴリズムとなる コマンド群 ################################################ start
    @staticmethod
    def default_case():
        print("Default case")

    # 全タブ 用
    # 各ツールの UI起動の呼び出し 関数
    def call_eachToolUIBoot(self, caseIndex: str = None):
        u""" < 全タブ 用 各ツールの UI起動の呼び出し 関数 です >

        :param str caseIndex: RigGenTlGp_View で定義されている 各 caseIndex に相当します
        """
        # print(caseIndex)
        switch_dict = {'caseA1': lambda: YO_renameTool5_main.main(),
                       'caseA2': lambda: YO_createSpaceNode3_main.main(),
                       'caseB1': lambda: YO_nodeCreateToWorldSpace.ui(),

                       # 追加2
                       'caseB2': lambda: YO_constraintToGeometry2.UI.showUI(),

                       # 追加6
                       'caseB3hide': lambda: isHistInter.hide(),
                       'caseB3show': lambda: isHistInter.show(),

                       'caseC1': lambda: YO_createClusterAndRename6_main.main(),
                       'caseC2': lambda: YO_createSpIkAndRename3_main.main(),
                       'caseD1': lambda: YO_pointConstraintByMatrix1_main.main(),
                       'caseD2': lambda: YO_orientConstraintByMatrix1_main.main(),
                       'caseD3': lambda: YO_scaleConstraintByMatrix1_main.main(),
                       'caseD4': lambda: YO_shearConstraintByMatrix1_main.main(),
                       'caseD5': lambda: YO_parentConstraintByMatrix5.UI.showUI(),
                       'caseD6': lambda: YO_parentConstraintByMatrix62.UI.showUI(),
                       'caseE1_3j': lambda: YO_jointDrawStyle_change.ui(),
                       'caseE1_4j': lambda: YO_jointRadiusSlider.ui(),

                       # 追加と変更と新規5
                       'caseF1': lambda: yoSkinWeightsExpImpTool_main.main(),
                       }
        func = switch_dict.get(caseIndex)
        if func is not None:
            # print('koko')
            func()
            print(caseIndex)
            if caseIndex == 'caseB3hide':
                message(u'isHistoricallyInteresting hide')
            elif caseIndex == 'caseB3show':
                message(u'isHistoricallyInteresting show')
            # message(u'詳細は Script Editor をご覧ください。')
        else:
            self.default_case()

    # 追加3
    # タブA,D 用 (group4)
    # 各ツールの Help起動の呼び出し 関数
    def call_eachToolHelpBoot(self, caseIndex: str = None):
        u""" < タブA,D 用 (group4) 各ツールの Help起動の呼び出し 関数 です >

        :param str caseIndex: RigGenTlGp_View で定義されている 各 caseIndex に相当します
        :rtype: None
        """
        # print(caseIndex)
        switch_dict = {
            # 追加3
            'caseA1': lambda: help(renameToolConfig),
            'caseA2': lambda: help(createSpaceNodeConfig),

            # 'caseB1': lambda: YO_nodeCreateToWorldSpace.ui(),
            #
            # # 追加2
            # 'caseB2': lambda: YO_constraintToGeometry2.UI.showUI(),
            #
            # 'caseC1': lambda: YO_createClusterAndRename6_main.main(),
            # 'caseC2': lambda: YO_createSpIkAndRename3_main.main(),

            # 追加3
            'caseD1': lambda: help(pConByMatConfig),
            'caseD2': lambda: help(oConByMatConfig),
            'caseD3': lambda: help(scConByMatConfig),
            'caseD4': lambda: help(shConByMatConfig),

            # 'caseD5': lambda: YO_parentConstraintByMatrix5.UI.showUI(),
            # 'caseD6': lambda: YO_parentConstraintByMatrix62.UI.showUI(),
            # 'caseE1_3j': lambda: YO_jointDrawStyle_change.ui(),
            # 'caseE1_4j': lambda: YO_jointRadiusSlider.ui(),
            }
        func = switch_dict.get(caseIndex)
        if func is not None:
            # print('koko')
            func()
            message(u'詳細は Script Editor をご覧ください。')
        else:
            self.default_case()

    # 追加3
    # タブA,D 用 (group4)
    # 各ツールの UI起動せずにコマンド実行する記述例の呼び出し 関数
    def call_eachToolCommandExampleBoot(self, caseIndex: str = None):
        u""" < タブA,D 用 (group4) 各ツールの UI起動せずにコマンド実行する記述例の呼び出し 関数 です >

        :param str caseIndex: RigGenTlGp_View で定義されている 各 caseIndex に相当します
        :rtype: None
        """
        # print(caseIndex)
        switch_dict = {
            # 追加3
            'caseA1': lambda: print(renameToolCommandExample),
            'caseA2': lambda: print(createSpaceNodeCommandExample),

            # 'caseB1': lambda: YO_nodeCreateToWorldSpace.ui(),
            #
            # # 追加2
            # 'caseB2': lambda: YO_constraintToGeometry2.UI.showUI(),
            #
            # 'caseC1': lambda: YO_createClusterAndRename6_main.main(),
            # 'caseC2': lambda: YO_createSpIkAndRename3_main.main(),

            # 追加3
            'caseD1': lambda: print(pConByMatCommandExample),
            'caseD2': lambda: print(oConByMatCommandExample),
            'caseD3': lambda: print(scConByMatCommandExample),
            'caseD4': lambda: print(shConByMatCommandExample),

            # 'caseD5': lambda: YO_parentConstraintByMatrix5.UI.showUI(),
            # 'caseD6': lambda: YO_parentConstraintByMatrix62.UI.showUI(),
            # 'caseE1_3j': lambda: YO_jointDrawStyle_change.ui(),
            # 'caseE1_4j': lambda: YO_jointRadiusSlider.ui(),
            }
        func = switch_dict.get(caseIndex)
        if func is not None:
            # print('koko')
            func()
            message(u'詳細は Script Editor をご覧ください。')
        else:
            self.default_case()

    # 変更6 ############################################################### start
    # 未使用にしたので、以下は一旦キャンセルにしました。
    # # 追加4
    # # タブB 用 (group2)
    # # IHIツールの Hide, Show の呼び出し 関数
    # def call_eachToolCommandBoot(self, caseIndexOption: str = None):
    #     u""" < タブB 用 (group2) IHIツールの Hide, Show の呼び出し 関数 です >
    #
    #     :param str caseIndexOption: RigGenTlGp_View で定義されている
    #         各 caseIndex + caseIndexOption に相当します
    #     :rtype: None
    #     """
    #     # print(caseIndex)
    #     switch_dict = {
    #         'caseB3hide': lambda: isHistInter.hide(),
    #         'caseB3show': lambda: isHistInter.show(),
    #         }
    #     func = switch_dict.get(caseIndexOption)
    #     if func is not None:
    #         # print('koko')
    #         func()
    #         message(u'詳細は Script Editor をご覧ください。')
    #     else:
    #         self.default_case()
    # 変更6 ############################################################### end

    # タブE 用
    # Joint: channel box 表示 用
    def call_checkBoxAction_j(self
                              , caseIndex: str, cBxWid_name
                              , longName: str, state: int
                              , *args
                              ):
        u""" < タブE 用 Joint: channel box 表示 用 >

        :param str caseIndex:
        :param QCheckBox cBxWid_name:
        :param str longName:
        :param int state:
        :param args:
        :type args:
        :return: currentState  : 'show' | 'hide' | None
        :rtype: str
        """
        message(f'm: cBx_j, {longName}: <{caseIndex}>')
        # # message(f'm: cBx_j')
        # print(cBxWid_name)  # type: QCheckBox
        # print(state)

        # print(longName)
        jointAttrList = ['rotateOrder', 'segmentScaleCompensate', 'drawStyle', 'radius']
        isExist = longName in jointAttrList

        currentState = None
        sels = commonCheckSelection()
        if not sels:
            message_warning(u'カレントで未選択の様です。選択して実行してください。')
            currentState = None
            pass
        else:
            for selIndex in sels:
                isJoint = commonCheckJoint(selIndex)
                if isJoint:
                    if state == 2:
                        currentState = 'show'
                        # print(currentState)
                        # for selIndex in sels:
                        cmds.setAttr(f'{selIndex}.{longName}', k = True)
                        message(u'カレントの選択ノード joint のチャンネルボックスへ、'
                                f'{longName} アトリビュートを {currentState} しました。'
                                )
                    else:
                        currentState = 'hide'
                        # print(currentState)
                        # for selIndex in sels:
                        cmds.setAttr(f'{selIndex}.{longName}', k = False)
                        message(u'カレントの選択ノードのチャンネルボックスへ、'
                                f'{longName} アトリビュートを {currentState} しました。'
                                )
                else:
                    message_warning(u'選択したノードの中で、joint で無いオブジェクトが'
                                    u'含まれている様です！！ joint にのみ 実行は一応行っております。'
                                    u'ご確認ください。')
                    currentState = None
        return currentState

    # タブE 用
    # Node: channel box 表示 用
    def call_checkBoxAction_n(self
                              , caseIndex: str, cBxWid_name
                              , longName: str, state: int
                              , *args
                              ):
        u""" < タブE 用 Node: channel box 表示 用 >

        :param str caseIndex:
        :param QCheckBox cBxWid_name:
        :param str longName:
        :param int state:
        :param args:
        :type args:
        :return: currentState  : 'show' | 'hide' | None
        :rtype: str
        """
        message(f'm: cBx_n, {longName}: <{caseIndex}>')
        # # message(f'm: cBx_n')
        # print(cBxWid_name)  # type: QCheckBox
        # print(state)

        # print(longName)
        nodeAttrList = ['shear']
        isExist = longName in nodeAttrList

        currentState = None
        sels = commonCheckSelection()
        if not sels:
            message_warning(u'カレントで未選択の様です。選択して実行してください。')
            currentState = None
            pass
        else:
            for selIndex in sels:
                if state == 2:
                    currentState = 'show'
                    for ax in ['shearXY', 'shearXZ', 'shearYZ']:
                        cmds.setAttr(f'{selIndex}.{ax}'
                                     , k = True
                                     , channelBox = False
                                     )
                    message(u'カレントの選択ノードのチャンネルボックスへ、'
                            f'{longName} アトリビュートを {currentState} しました。'
                            )
                else:
                    currentState = 'hide'
                    for ax in ['shearXY', 'shearXZ', 'shearYZ']:
                        cmds.setAttr(f'{selIndex}.{ax}'
                                     , k = False
                                     , channelBox = False
                                     )
                    message(u'カレントの選択ノードのチャンネルボックスへ、'
                            f'{longName} アトリビュートを {currentState} しました。'
                            )
        return currentState

    # タブE 用
    # Joint: current view 表示 用
    def call_checkBoxAction_jv(self
                               , caseIndex: str, cBxWid_name
                               , longName: str, state: int
                               , *args
                               ):
        u""" < Joint: current view 表示 用 >

        :param str caseIndex:
        :param QCheckBox cBxWid_name:
        :param str longName:
        :param int state:
        :param args:
        :type args:
        :return: currentState  : 'show' | 'hide' | None
        :rtype: str
        """
        message(f'm: cBx_jv, {longName}: <{caseIndex}>')
        # # message(f'm: cBx_jv')
        # print(cBxWid_name)  # type: QCheckBox
        # print(state)

        # print(longName)
        jointAttrList = ['displayLocalAxis']
        isExist = longName in jointAttrList

        currentState = None
        sels = commonCheckSelection()
        if not sels:
            message_warning(u'カレントで未選択の様です。選択して実行してください。')
            currentState = None
            pass
        else:
            for selIndex in sels:
                isJoint = commonCheckJoint(selIndex)
                if isJoint:
                    if state == 2:
                        currentState = 'show'
                        # print(currentState)
                        # for selIndex in sels:
                        cmds.setAttr(f'{selIndex}.{longName}', 1)
                        message(u'カレントの選択ノード joint のcurrent view上での表示として、'
                                f'{longName} アトリビュートを {currentState} しました。'
                                )
                    else:
                        currentState = 'hide'
                        # print(currentState)
                        # for selIndex in sels:
                        cmds.setAttr(f'{selIndex}.{longName}', 0)
                        message(u'カレントの選択ノード joint のcurrent view上での表示として、'
                                f'{longName} アトリビュートを {currentState} しました。'
                                )
                else:
                    message_warning(u'選択したノードの中で、joint で無いオブジェクトが'
                                    u'含まれている様です！！ joint にのみ 実行は一応行っております。'
                                    u'ご確認ください。')
                    currentState = None
        return currentState

    # タブE 用
    # Node: current view 表示 用
    def call_checkBoxAction_nv(self
                               , caseIndex: str, cBxWid_name
                               , longName: str, state: int
                               , *args
                               ):
        u""" < タブE 用 Node: current view 表示 用 >

        :param str caseIndex:
        :param QCheckBox cBxWid_name:
        :param str longName:
        :param int state:
        :param args:
        :type args:
        :return: currentState  : 'show' | 'hide' | None
        :rtype: str
        """
        message(f'm: cBx_nv, {longName}: <{caseIndex}>')
        # # message(f'm: cBx_nv')
        # print(cBxWid_name)  # type: QCheckBox
        # print(state)

        # print(longName)
        nodeAttrList = ['reference']
        isExist = longName in nodeAttrList

        currentState = None
        sels = commonCheckSelection()
        if not sels:
            message_warning(u'カレントで未選択の様です。選択して実行してください。')
            currentState = None
            pass
        else:
            for selIndex in sels:
                hasShape = commonCheckShape(selIndex)
                if hasShape:
                    if state == 2:
                        currentState = 'normal'
                        # print(currentState)
                        # for selIndex in sels:
                        # setAttr "spineSpIkA_spIKCrvShape.overrideEnabled" 0;
                        # setAttr "spineSpIkA_spIKCrvShape.overrideDisplayType" 0;
                        cmds.setAttr(f'{selIndex}.overrideEnabled', 0)
                        cmds.setAttr(f'{selIndex}.overrideDisplayType', 0)
                        message(u'カレントの選択ノード joint のcurrent view上での表示として、'
                                f'{longName} アトリビュートを {currentState} しました。'
                                )
                    else:
                        currentState = 'reference'
                        # print(currentState)
                        # for selIndex in sels:
                        # setAttr "spineSpIkA_spIKCrvShape.overrideEnabled" 1;
                        # setAttr "spineSpIkA_spIKCrvShape.overrideDisplayType" 2;
                        cmds.setAttr(f'{selIndex}.overrideEnabled', 1)
                        cmds.setAttr(f'{selIndex}.overrideDisplayType', 2)
                        message(u'カレントの選択ノード joint のcurrent view上での表示として、'
                                f'{longName} アトリビュートを {currentState} しました。'
                                )
                else:
                    message_warning(u'選択したノードの中で、joint で無いオブジェクトが'
                                    u'含まれている様です！！ joint にのみ 実行は一応行っております。'
                                    u'ご確認ください。')
                    currentState = None
        return currentState

    # タブE 用
    # Mesh: current view 表示 用
    def call_checkBoxAction_mv(self
                               , caseIndex: str, cBxWid_name
                               , longName: str, state: int
                               , *args
                               ):
        u""" < タブE 用 Mesh: current view 表示 用 >

        :param str caseIndex:
        :param QCheckBox cBxWid_name:
        :param str longName:
        :param int state:
        :param args:
        :type args:
        :return: currentState  : 'on' | 'off' | None
        :rtype: str
        """
        message(f'm: cBx_mv, {longName}: <{caseIndex}>')
        # # message(f'm: cBx_mv')
        # print(cBxWid_name)  # type: QCheckBox
        # print(state)

        # print(longName)
        meshAttrList = ['backfaceCulling']
        isExist = longName in meshAttrList

        currentState = None
        sels = commonCheckSelection()
        if not sels:
            message_warning(u'カレントで未選択の様です。選択して実行してください。')
            currentState = None
            pass
        else:
            for selIndex in sels:
                isMesh = commonCheckMesh(selIndex)
                if isMesh:
                    if state == 2:
                        currentState = 'on'
                        cmds.setAttr(f'{selIndex}.{longName}', 3)
                        message(u'カレントの選択ノード mesh のcurrent view上での表示として、'
                                f'{longName} アトリビュートを {currentState} しました。'
                                )
                    else:
                        currentState = 'off'
                        cmds.setAttr(f'{selIndex}.{longName}', 0)
                        message(u'カレントの選択ノード mesh のcurrent view上での表示として、'
                                f'{longName} アトリビュートを {currentState} しました。'
                                )
                else:
                    message_warning(u'選択したノードの中で、mesh で無いオブジェクトが'
                                    u'含まれている様です！！ mesh にのみ 実行は一応行っております。'
                                    u'ご確認ください。')
                    currentState = None
        return currentState

    # タブE 用
    # Curve: channel box 表示 用
    def call_checkBoxAction_c(self
                              , caseIndex: str, cBxWid_name
                              , longName: str, state: int
                              , *args
                              ):
        u""" < タブE 用 Curve: channel box 表示 用 >

        :param str caseIndex:
        :param QCheckBox cBxWid_name:
        :param str longName:
        :param int state:
        :param args:
        :type args:
        :return: currentState  : 'show' | 'hide' | None
        :rtype: str
        """
        message(f'm: cBx_c, {longName}: <{caseIndex}>')
        # # message(f'm: cBx_c')
        # print(cBxWid_name)  # type: QCheckBox
        # print(state)

        # print(longName)
        curveAttrList = ['lineWidth']
        isExist = longName in curveAttrList

        currentState = None
        sels = commonCheckSelection()
        if not sels:
            message_warning(u'カレントで未選択の様です。選択して実行してください。')
            currentState = None
            pass
        else:
            for selIndex in sels:
                isCurve = commonCheckCurve(selIndex)
                if isCurve:
                    if state == 2:
                        currentState = 'show'
                        # print(currentState)
                        # for selIndex in sels:
                        cmds.setAttr(f'{selIndex}.{longName}'
                                     , k = False, channelBox = True
                                     )
                        message(u'カレントの選択ノード curve のチャンネルボックスへ、'
                                f'{longName} アトリビュートを {currentState} しました。'
                                )
                    else:
                        currentState = 'hide'
                        # print(currentState)
                        # for selIndex in sels:
                        cmds.setAttr(f'{selIndex}.{longName}'
                                     , k = False, channelBox = False
                                     )
                        message(u'カレントの選択ノード curve のチャンネルボックスへ、'
                                f'{longName} アトリビュートを {currentState} しました。'
                                )
                else:
                    message_warning(u'選択したノードの中で、curve で無いオブジェクトが'
                                    u'含まれている様です！！ curve にのみ 実行は一応行っております。'
                                    u'ご確認ください。')
                    currentState = None
        return currentState

    # その他 アルゴリズムとなる コマンド群 ################################################### end

    # 3. UI-3. common ボタン コマンド群 ################################################# start
    def ui_executeBtnCmd(self, *args):
        # ...
        message(f'm: {args[0]}')  # message output
        # ...

    # check_type 関数
    # View へ移動...

    # uiOptBtn_changeColorCmd 関数
    # View へ移動...
    # 3. UI-3. common ボタン コマンド群 ################################################### end


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
