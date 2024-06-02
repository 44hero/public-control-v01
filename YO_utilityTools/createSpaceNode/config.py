# -*- coding: utf-8 -*-

u"""
createSpaceNode package

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -6.0-
:Date: 2024/05/22

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PyMel version: 1.2.0
    - PySide2 version: 5.15.2

概要(overview):
    独自の space 作成用リネームツールです。
詳細(details):
    親 space を作りたいノードを選択し実行する事で、
        選択ノードの階層の一つ上階層の親に 親 space が、命名規則に則って1つ作成されます。
    親 space には、locator，null，joint の何れかで作成されるよう設計されています。

    独自規格の命名規則については、renameTool の help をご覧ください。
        つまり、renameTool packageモジュール内部の各クラスを継承しています。
    ・ text ベースのコマンド 出力を搭載
        UI操作実行後、 maya script editor の一行目には必ず、text ベースのコマンド を出力も致します。
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
        import YO_utilityTools.createSpaceNode.YO_createSpaceNode3_main
        reload(YO_utilityTools.createSpaceNode.YO_createSpaceNode3_main)
        # from <パッケージ名> import <モジュール名>
        from YO_utilityTools.createSpaceNode import YO_createSpaceNode3_main
        # <モジュール名>.<□□:機能名>()
        YO_createSpaceNode3_main.main()

        # UI立ち上げずに、コマンドで実行するには
        # 以下 e.g.):
        # import <パッケージ名>.<モジュール名>
        import YO_utilityTools.createSpaceNode.YO_createSpaceNode3_Modl
        reload(YO_utilityTools.createSpaceNode.YO_createSpaceNode3_Modl)
        # from <パッケージ名> import <モジュール名>
        from YO_utilityTools.createSpaceNode import YO_createSpaceNode3_Modl
        # <モジュール名>.<クラス名>().<□□:機能名>()
        YO_createSpaceNode3_Modl.CSpaceNode_Modl().exe(mode = 1, n = [u'~', u'~[Space]', u'~', u'', u''], nodeType = u'locator')

注意(note):
    ・ 当ツールは、renameTool に準じていますが、各textFieldに若干の制限を設けています。
        #.
            第1単語 ユーザータイピング入力を制限

        #.
            第2単語(ローワーキャメルケース記述) には予め、役割目を設定済み(ユーザータイピング入力を制限)

        #.
            第3単語 ユーザータイピング入力を制限
    ・ 他に必須なモジュール
        ::

            from ..lib.message import message
            from ..lib.message_warning import message_warning
            from ..lib.commonCheckJoint import commonCheckJoint  # :return: bool
            from ..lib.commonCheckSelection import commonCheckSelection  # :return: string
            # 個別ノードの持つ単独UUID番号、に対する独自操作 モジュール
            from ..lib.YO_uuID import UUID

            # ロギング用モジュール
            from ..lib import YO_logger2
            from ..lib.YO_logger2 import Decorator  # ログデコレーター用クラスです
            from ..lib.YO_logger2 import LogProcess_Output  # ログプロセス出力用クラスです

            # optionVar_command_library(optionVarを操作するライブラリー)
            from ..lib.YO_optionVar import setOptionVarCmd  # オプション変数を設定する関数
            from ..lib.YO_optionVar import getOptionVarCmd  # オプション変数を取得する関数
            # from ..lib.YO_optionVar import upDateOptionVarsDictCmd  # オプション変数をdict操作し、更新をかける関数
            from ..lib.YO_optionVar import upDateOptionVarCmd  # オプション変数に更新をかける関数

<UI 説明>
    ・ rename mode: ネーミングのモード選択
        現状選択は無効です

        **default: 1(構成要素をキープモード)**

    ・ textField: ネーミングの決定
        renameTool の help をご覧ください。
        ::

            e.g.):                    e.g.):
                lip_jt                    lip
                   ↓                          ↓
                lip_jtSpace               lipSpace

                tFld A1. ~                tFld A1. ~
                tFld B1. ~[Space]         tFld B1. ~[Space]
                tFld C1. ~                tFld C1. ~
                tFld C2. blank            tFld C2. blank
                tFld C3. blank            tFld C3. blank

        補足):
            第1単語
                ユーザータイピング入力を制限しています
            第2単語
                第2単語には予め、役割目 [Space] を設定済み(ユーザータイピング入力を制限)です。
            第3単語
                -要素1
                -要素2
                -要素3
                いずれも、ユーザータイピング入力を制限しています

    ・ node type: 親 space を、locator， null， joint の何れかで作成するのかをメニューで選択
        何れかを選択してください

        **default: u'locator'**

-UIを立ち上げずにコマンドベースで実行する方法-
    使用法(usage):
        e.g.): 既存の 'lip_jt' の親に 'lip_jtSpace ' とネーミングし、 joint で親spaceを作成したい時は。。。
            :param n: list of string(range 5)
                tFld A1. ベースとなる文字列 + ナンバリング用識別文字列
                    ~
                tFld B1. 役割等を表す入力領域
                    ~[Space]
                tFld C1. ナンバリング用識別子
                    ~
                tFld C2. 文字列 Gp 識別子
                    blank
                tFld C3. サイド用識別子
                    blank
            '~' + '_' + '~[Space]' + '_' + '~' + '' + ''
            で構成します。

            <longName>:
                ::

                    YO_utilityTools.createSpaceNode.YO_createSpaceNode3_Modl.CSpaceNode_Modl().exe(mode = 1
                    , n = [u'~', u'~[Space]', u'~', u'', u'']
                    , nodeType = u'locator'
                    )

            <shortName>:
                *****

-リマインダ-
    done: 2024/05/22
        - 変更8 と 追加8 と 新規8
            - 概要: ユニークでない名前 のノードの space 作成におけるバグ修正 その2
                - YO_createSpaceNode3_Modl.py 変更記述あり
            詳細はそれ自身のリマインダに記述...
        version = '-6.0-'

    done: 2024/05/20
        - 変更7 と 追加7 と 新規7
            - 概要: ユニークでない名前 のノードの space 作成におけるバグ修正
                - YO_createSpaceNode3_Modl.py 変更記述あり
            詳細はそれ自身のリマインダに記述...
        version = '-5.0-'

    done: 2024/05/13~2024/05/15
        - 変更6 と 追加6
            - 概要: maya default の Script Editor へのログ出力 を、
                YO_logProcess.action('ERROR'...)
                YO_logProcess.action('WARNING'...)
                    で行っていた箇所を、
                カスタムの Script Editor2 (PySide2作成UI) で置き換え
                - YO_createSpaceNode3_Modl.py 変更記述あり
                - YO_createSpaceNode3_View.py 変更記述あり
            詳細はそれ自身のリマインダに記述...
        version = '-4.0-'

    done: 2023/12/21
        - 変換箇所5
            絶対パス から 相対パス へ記述変更
                - YO_createSpaceNode3_Modl.py 変更記述あり
                - YO_createSpaceNode3_View.py 変更記述あり
                - YO_createSpaceNode3_Ctlr.py 変更記述あり
                - YO_createSpaceNode3_main.py 変更記述あり
            詳細はそれ自身のリマインダに記述...
        version = '-3.1-'

    done: 2023//10/25
        汎用箇所を、モジュールとして読み込みに変更
            - YO_createSpaceNode3_Modl.py 変更記述あり
            - YO_createSpaceNode3_View.py 変更記述あり
            - YO_createSpaceNode3_main.py 変更記述あり
            詳細はそれ自身のリマインダに記述...
        version = '-3.0-'

    done: 2023/10/09
        - YO_createSpaceNode3_Modl.py 変更記述あり
        詳細はそれ自身のリマインダに記述...
        version = '-2.8-'

    done: 2023/10/06
        - YO_createSpaceNode3_Modl.py 変更記述あり
        詳細はそれ自身のリマインダに記述...
        version = '-2.7-'

    done: 2023/10/06
        - YO_createSpaceNode3_Modl.py 変更記述あり
        詳細はそれ自身のリマインダに記述...
        version = '-2.6-'

    done: 2023/10/04
        python2系 -> python3系 変換
            - YO_createSpaceNode3_main.py 変換記述あり
            詳細はそれ自身のリマインダに記述...

        version = '-2.5-'

    done: 2023/09/21
        python2系 -> python3系 変換
            - YO_createSpaceNode3_main.py 変換記述あり
            - YO_createSpaceNode3_Modl.py 変換記述あり
            詳細はそれ自身のリマインダに記述...

        version = '-2.0-'

    done: 2023/04/17~2023/05/08
        新規

        version = '-1.0-'
"""

TITLE = 'YO_createSpaceNode3'  # MVCモデルを意識しファイル分割した、パッケージ記述
VERSION = '-6.0- <py 3.7.7, ui:PyMel 1.2.0 + CSE2:PySide2 5.15.2>'
SPACE = ' '

CommandExample = '''
# UI立ち上げずに、コマンドで実行するには
# 以下 e.g.):
# import <パッケージ名>.<モジュール名>
import YO_utilityTools.createSpaceNode.YO_createSpaceNode3_Modl
reload(YO_utilityTools.createSpaceNode.YO_createSpaceNode3_Modl)
# from <パッケージ名> import <モジュール名>
from YO_utilityTools.createSpaceNode import YO_createSpaceNode3_Modl
# <モジュール名>.<クラス名>().<□□:機能名>()
YO_createSpaceNode3_Modl.CSpaceNode_Modl().exe(mode = 1, n = [u'~', u'~[Space]', u'~', u'', u''], nodeType = u'locator')
'''

if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
