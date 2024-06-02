# -*- coding: utf-8 -*-

u"""
createClusterAndRenameTool  package

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -3.1-
:Date: 2023/12/22

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PyMel version: 1.2.0

概要(overview):
    独自規格の命名規則に基づいた Cluster Handle と Cluster を命名しつつ、
        それらを同時に効率良く作成するツール
            の バージョン6(PyMel版)
                MVCモデルパッケージ
                    です
詳細(details):
    クラスター作成は、一回づつを基本としています。連続で行いたい時は、for in loop 等で繰り返してください。

    独自規格の命名規則に基づいた、Cluster Handle ・ Cluster 共に同時作成し、ネーミングの統一も独自規格で行います。

    relative を考慮するか、も必須となっています。

        **default: False(0)**

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
        import YO_utilityTools.createClusterAndRenameTool.YO_createClusterAndRename6_main
        reload(YO_utilityTools.createClusterAndRenameTool.YO_createClusterAndRename6_main)
        # from <パッケージ名> import <モジュール名>
        from YO_utilityTools.createClusterAndRenameTool import YO_createClusterAndRename6_main
        # <モジュール名>.<□□:機能名>()
        YO_createClusterAndRename6_main.main()

        # UI立ち上げずに、コマンドで実行するには
        # 以下 e.g.):
        # import <パッケージ名>.<モジュール名>
        import YO_utilityTools.createClusterAndRenameTool.YO_createClusterAndRename6_Modl
        reload(YO_utilityTools.createClusterAndRenameTool.YO_createClusterAndRename6_Modl)
        # from <パッケージ名> import <モジュール名>
        from YO_utilityTools.createClusterAndRenameTool import YO_createClusterAndRename6_Modl
        # <モジュール名>.<クラス名>().<□□:機能名>()
        YO_createClusterAndRename6_Modl.CCAndRT_Modl().exe(mode = 0, relative = 0, n = [u'spineSpIk@', u'clstHndle', u'', u'', u'L'])

注意(note):
    ・ 当ツールは、renameTool に準じていますが、各textFieldに若干の制限を設けています。
        * @ at mark の使用は、第1単語 でのみ許可

        * 第2単語(ローワーキャメルケース記述) には予め、役割目を設定済み(ユーザータイピング入力を制限)

        * 第3単語(アッパーキャメルケース記述) 第3単語-要素1、第3単語-要素2 はそれぞれ使用不可

            以下詳細
                使用不可
                    textField C1. 第3単語-要素1 不要
                        ナンバリング用識別子領域
                    textField C2. 第3単語-要素2 不要
                        文字列 Gp 識別子領域
    ・ 他に必須な独自モジュール
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
        renameTool の help をご覧ください。

        **default: 0(強制的モード)**

    ・ textField: ネーミングの決定
        renameTool の help をご覧ください。
        ::

            e.g.): lip_clstHndle      e.g.): spineSpIkA_clstHndle_L
                tFld A1. lip              tFld A1. spineSpIk@
                tFld B1. clstHndle        tFld B1. clstHndle
                tFld C1. blank            tFld C1. blank
                tFld C2. blank            tFld C2. blank
                tFld C3. blank            tFld C3. L
                         +                         +
                   lip_CLST                  spineSpIkA_L_CLST

        補足):
            第2単語
                第2単語には予め、役割目を設定済み(ユーザータイピング入力を制限)です。

        **default: 'clstHndle'**

    ・ Use identifiers for automatic numbering: 自動でナンバリングするための識別子の準備ボタン
        連続で、自動ナンバリングを実行するための on/off です。
        クラスター作成は、一回づつを基本としていますが、ネーミングを連番で統一作成する場合に利用します。
        試しに、手動でボタンをトグルしてみると明らかですが、
        第1単語(ローワーキャメルケース記述)入力文字列の末尾に @ (at mark)を自動で 挿入/未挿入 します。

        **default: 0(False)**

    ・ relative: 相対モードの on/off 選択
        maya cluster deformer の標準アトリビュートに準じています。

        **default: 0(False)**

    ・ ↓↓ naming check ! ↓↓: 命名を予めチェックできるボタン
        押下ください。

-UIを立ち上げずにコマンドベースで実行する方法-
    使用法(usage):
        e.g.): 強制的モード、relativeを off で、'spineSpIkA_clstHndle_L' とネーミングしてクラスターを作成したい時は。。。
            :param mode: str(0/1)    rename mode(ネーミングのモード)
                0(強制的モード)
            :param relative: bool(0/1)     relative 相対モード
                0(False)
            :param n: list of string(range 5)
                tFld A1. ベースとなる文字列 + ナンバリング用識別文字列
                    spineSpIk@
                tFld B1. 役割等を表す入力領域
                    clstHndle
                tFld C1. ナンバリング用識別子
                    blank
                tFld C2. 文字列 Gp 識別子
                    blank
                tFld C3. サイド用識別子
                    L
            mode 0、 relative 0 と、
                'spineSpIk@' + '_' + 'clstHndle' + '_' + '' + '' + 'L'
            で構成します。

            <longName>:
                ::

                    YO_createClusterAndRename6_Modl.CCAndRT_Modl().exe(mode = 0, relative = 0, n = [u'spineSpIk@', u'clstHndle', u'', u'', u'L'])
            <shortName>:
                ::

                  *****

-リマインダ-
    done: 2023/12/22
        - 変換箇所4
            絶対パス から 相対パス へ記述変更
                - YO_createClusterAndRename6_Modl.py 変更記述あり
                - YO_createClusterAndRename6_View.py 変更記述あり
                - YO_createClusterAndRename6_Ctlr.py 変更記述あり
                - YO_createClusterAndRename6_main.py 変更記述あり
            詳細はそれ自身のリマインダに記述...

        version = '-3.1-'

    done: 2023//10/26
        汎用箇所を、モジュールとして読み込みに変更
            - YO_createClusterAndRename6_Modl.py 変更記述あり
            - YO_createClusterAndRename6_View.py 変更記述あり
            - YO_createClusterAndRename6_main.py 変更記述あり
            詳細はそれ自身のリマインダに記述...

        version = '-3.0-'

    done: 2023/10/04
        python2系 -> python3系 変換
            - YO_createClusterAndRename6_main.py 変換記述あり
            詳細はそれ自身のリマインダに記述...

        version = '-2.5-'

    done: 2023/09/21
        python2系 -> python3系 変換
            - YO_createClusterAndRename6_main.py 変換記述あり
            - YO_createClusterAndRename6_Modl.py 変換記述あり
            詳細はそれ自身のリマインダに記述...

        version = '-2.0-'

    done: 2023/03/03~2022/04/13
        新規

        version = '-1.0-'
"""

TITLE = 'YO_createClusterAndRename6'  # MVCモデルを意識しファイル分割した、パッケージ記述
VERSION = '-3.1- <py 3.7.7, ui:PyMel 1.2.0>'
SPACE = ' '

if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
