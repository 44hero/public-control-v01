# -*- coding: utf-8 -*-

u"""
skinWeightsExpImpTool package

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -3.1-
:Date: 2024/06/07

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PySide2 version: 5.15.2

概要(overview):
    maya 用の skin weights の export, import ツールです。
詳細(details):
    ***
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
        import YO_utilityTools.skinWeightsExpImpTool.yoSkinWeightsExpImpTool_main
        reload(YO_utilityTools.skinWeightsExpImpTool.yoSkinWeightsExpImpTool_main)
        # from <パッケージ名> import <モジュール名>
        from YO_utilityTools.skinWeightsExpImpTool import yoSkinWeightsExpImpTool_main
        # <モジュール名>.<□□:機能名>()
        yoSkinWeightsExpImpTool_main.main()

注意(note):
    ・ 他に必須な独自モジュール
        ::

            import YO_utilityTools.skinWeightsExpImpTool.config as docstring
            from YO_utilityTools.lib.commonCheckSelection import commonCheckSelection
            # basic_configuration(基本構成)
            from .config import SPACE, TITLE, VERSION

            from .yoSkinWeightsExpImpTool_Modl import SkinWeightExpImp_Modl
            from .yoSkinWeightsExpImpTool_Ctlr import SkinWeightExpImp_Ctlr

            # shiboken2 独自モジュール
            from ..TemplateForPySide2.qt import getMayaWindow  # 利用時は、getMayaWindow()

            from ..TemplateForPySide2.pyside2IniFileSetting import IniFileSetting
            from ..TemplateForPySide2.Container import Container
            from ..TemplateForPySide2.MyTabWidget import MyTabWidget
            from ..TemplateForPySide2.CustomScriptEditor import CustomScriptEditor

            from ..TemplateForPySide2.type1.templateForPySide2_type1_View import Tpl4PySide2_Type1_View
            # 汎用ライブラリー の使用 #################################################### start
            from ..lib.message import message
            from ..lib.message_warning import message_warning
            from ..lib.yoGetAttributeFromModule import GetAttrFrmMod
            from ..lib.commonCheckCurve import commonCheckCurve
            from ..lib.commonCheckMesh import commonCheckMesh
            from ..lib.commonCheckSurface import commonCheckSurface
            from ..lib.commonCheckShape import commonCheckShape
            from ..lib.commonCheckSkinCluster import commonCheckSkinCluster
            # 汎用ライブラリー の使用 #################################################### end
            from ..TemplateForPySide2.CustomScriptEditor2SPIModule import custom_scriptEditor2_instance

<UI 説明>
    大別して、
        上部: Export 作業エリア
        下部: Import 作業エリア
    です。
    確実な Export, Import を実行する関係上、
        基本的に、任意のノードを view 上で必ず選択してからでないと、
            実行出来ない仕様にしています。

-リマインダ-
    done: 2024/06/07
        - 追加3
            - 概要: カスタムの Script Editor2 への プロセス文字列 出力 を加味
            - 詳細:
                - yoSkinWeightsExpImpTool_View.py 変更記述あり
                詳細はそれ自身のリマインダに記述...
        version = '-3.1-'

    done: 2024/06/07
        - 変更2 と 追加2 と 新規2
            - 概要: カスタムの の Script Editor へのログ出力 を、
                カスタムの Script Editor2 (PySide2作成UI) で置き換え
            - 詳細: カスタムの Script Editor2 (PySide2作成UI) で置き換える為には、
                from ..TemplateForPySide2.CustomScriptEditor2SPIModule import custom_scriptEditor2_instance
                モジュールを必要とします
                また、
                    他のモジュール でも シングルトンモジュール として再利用している関係で
                        エラーの影響が及びます
                そのエラーの影響を回避する目的として、
                    以下のように、あらかじめ カスタムの Script Editor2 モジュール
                        を定義しています
                - yoSkinWeightsExpImpTool_View.py 変更記述あり
                詳細はそれ自身のリマインダに記述...
        version = '-3.0-'

    done: 2024/05/08~2024/05/09
        追加と変更と新規1
            - 概要: outPut 専用 script_editor ウィジェット の挙動修正
                に伴う、
                各モジュール への関連を 追加
            - 詳細: メインとなるUIとのセットで出現することを想定しているのだが、
                個別にUIを誤って閉じてしまった場合等、エラー回避を主な目的とした、ｺｰﾄﾞ修正と追加
                - yoSkinWeightsExpImpTool_View.py 変更記述あり
                詳細はそれ自身のリマインダに記述...
        version = '-2.0-'

    done: 2024/04/21~2024/04/25
        新規
        version = '-1.0-'
"""

TITLE = 'yoSkinWeightsExpImpTool'  # MVCモデルを意識しファイル分割した、パッケージ記述
VERSION = '-3.1- <py 3.7.7, ui:PySide2 5.15.2>'
SPACE = ' '

if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
