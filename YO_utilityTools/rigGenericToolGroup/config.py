# -*- coding: utf-8 -*-

u"""
rigGenericToolGroup package

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -5.5-
:Date: 2024/05/17

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PySide2 version: 5.15.2

概要(overview):
    rig 作業時の汎用性の高いツールをまとめました。
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
        import YO_utilityTools.rigGenericToolGroup.yoRigGenericToolGroup_main
        reload(YO_utilityTools.rigGenericToolGroup.yoRigGenericToolGroup_main)
        # from <パッケージ名> import <モジュール名>
        from YO_utilityTools.rigGenericToolGroup import yoRigGenericToolGroup_main
        # <モジュール名>.<□□:機能名>()
        yoRigGenericToolGroup_main.main()

注意(note):
    ・ 他に必須な独自モジュール
        ::

            import YO_utilityTools.rigGenericToolGroup.config as docstring
            # basic_configuration(基本構成)
            from .config import SPACE, TITLE, VERSION

            from .yoRigGenericToolGroup_Modl import RigGenTlGp_Modl
            from .yoRigGenericToolGroup_Ctlr import RigGenTlGp_Ctlr

            # shiboken2 独自モジュール
            from ..TemplateForPySide2.qt import getMayaWindow  # 利用時は、getMayaWindow()

            from ..TemplateForPySide2.pyside2IniFileSetting import IniFileSetting
            from ..TemplateForPySide2.Container import Container
            from ..TemplateForPySide2.MyTabWidget import MyTabWidget

            from ..TemplateForPySide2.type2.templateForPySide2_type2_View import Tpl4PySide2_Type2_View
            from ..TemplateForPySide2.type2.templateForPySide2_type2_Ctlr import Tpl4PySide2_Type2_Ctlr
            # 汎用ライブラリー の使用 #################################################### start
            from ..lib.message import message
            from ..lib.message_warning import message_warning
            from ..lib.commonCheckSelection import commonCheckSelection
            from ..lib.commonCheckJoint import commonCheckJoint
            from ..lib.commonCheckMesh import commonCheckMesh
            from ..lib.commonCheckCurve import commonCheckCurve
            from ..lib.commonCheckShape import commonCheckShape
            # 汎用ライブラリー の使用 #################################################### end

<UI 説明>
    ***

-リマインダ-
    done: 2024/05/17
        - 追加6 と 変更6 と 新規6
            - 概要: ***_View モジュール の tabB の
                IHIツールの Hide, Show の呼び出し の改善
                に伴う、
                各モジュール への関連を 追加 変更 新規
            - 詳細:
                - rigGenericToolGroup_Modl.py 変更記述あり
                - rigGenericToolGroup_View.py 変更記述あり
                - rigGenericToolGroup_Ctlr.py 変更記述あり
                詳細はそれ自身のリマインダに記述...
        version = '-5.5-'

    done: 2024/05/01
        追加4
            - 概要: ***_View モジュール の tabB へ
                IHIツールの Hide, Show の呼び出し 追加
                に伴う、
                各モジュール への関連を 追加
            - 詳細:
                - rigGenericToolGroup_Modl.py 変更記述あり
                - rigGenericToolGroup_View.py 変更記述あり
                - rigGenericToolGroup_Ctlr.py 変更記述あり
                詳細はそれ自身のリマインダに記述...
        version = '-5.0-'

    done: 2024/04/11~2024/04/17
        追加3
            - 概要: ***_View モジュール の tabA, D の 各ツールの
                Help の呼び出し 追加
                コマンド実行する記述例 の呼び出し 追加
                に伴う、
                各モジュール への関連を 追加
            - 詳細:
                - rigGenericToolGroup_Modl.py 変更記述あり
                - rigGenericToolGroup_View.py 変更記述あり
                - rigGenericToolGroup_Ctlr.py 変更記述あり
                詳細はそれ自身のリマインダに記述...
        version = '-4.0-'

    done: 2024/04/11
        追加2
            - 概要: ***_View モジュール の tabB へ YO_constraintToGeometry2 UI の呼び出し 追加
                に伴う、各モジュール への関連を 追加
            - 詳細:
                - rigGenericToolGroup_Modl.py 変更記述あり
                - rigGenericToolGroup_View.py 変更記述あり
                - rigGenericToolGroup_Ctlr.py 変更記述あり
                詳細はそれ自身のリマインダに記述...
        version = '-3.1-'

    done: 2024/04/09
        追加1
            - 概要: tabE へ Node current view として reference の on/off 表示切り替え を追加
            - 詳細:
                - rigGenericToolGroup_Modl.py 変更記述あり
                - rigGenericToolGroup_View.py 変更記述あり
                - rigGenericToolGroup_Ctlr.py 変更記述あり
                詳細はそれ自身のリマインダに記述...
        version = '-3.0-'

    done: 2024/03/17~
        新規
        version = '-2.0-'

    done: 2024/01/26~2024/03/03
        新規
        version = '-1.0-'

"""

TITLE = 'yoRigGenericToolGroup'  # MVCモデルを意識しファイル分割した、パッケージ記述
VERSION = '-5.5- <py 3.7.7, ui:PySide2 5.15.2>'
SPACE = ' '

if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
