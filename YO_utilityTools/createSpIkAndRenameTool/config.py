# -*- coding: utf-8 -*-

u"""
createSpIkAndRenameTool package

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
    既定の命名規則に基づいた Spline IK Handle と Curve を作成するツール
        の バージョン3(PyMel版)
            MVCモデルパッケージ
                です
詳細(details):
    現状の命名規則に基づいた、Spline IK Handle ・ Curve 共に同時作成し、ネーミングの統一も行います。

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
        import YO_utilityTools.createSpIkAndRenameTool.YO_createSpIkAndRename3_main
        reload(YO_utilityTools.createSpIkAndRenameTool.YO_createSpIkAndRename3_main)
        # from <パッケージ名> import <モジュール名>
        from YO_utilityTools.createSpIkAndRenameTool import YO_createSpIkAndRename3_main
        # <モジュール名>.<□□:機能名>()
        YO_createSpIkAndRename3_main.main()

        # UI立ち上げずに、コマンドで実行するには
        # 以下 e.g.):
        # import <パッケージ名>.<モジュール名>
        import YO_utilityTools.createSpIkAndRenameTool.YO_createSpIkAndRename3_Modl
        reload(YO_utilityTools.createSpIkAndRenameTool.YO_createSpIkAndRename3_Modl)
        # from <パッケージ名> import <モジュール名>
        from YO_utilityTools.createSpIkAndRenameTool import YO_createSpIkAndRename3_Modl
        # <モジュール名>.<クラス名>().<□□:機能名>()
        YO_createSpIkAndRename3_Modl.CSpIkAndRT_Modl().exe(mode = 0, n = [u'spineSpIk', u'spIKHndle', u'', u'', u'L'], rootOnCurve = 0, parentCurve = 0, createCurve = 1, simplifyCurve = 1, startJoint = u'spineA_spIKjt', endEffector = u'spineTip_spIKjt', grouping = 1)

注意(note):
    ・ 当ツールは、renameTool に準じていますが、各textFieldに若干の制限を設けています。
        #.
            @ at mark の使用は、第1単語 でのみ許可

        #.
            ユーザーによる第1単語入力時には、必ず 'SpIk' 文字列を自動で付加

        #.
            第2単語(ローワーキャメルケース記述) には予め、役割目を設定済み(ユーザータイピング入力を制限)

        #.
            第3単語(アッパーキャメルケース記述) 第3単語-要素1、第3単語-要素2 はそれぞれ使用不可

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
    ・ start joint: Spline IK のスタートとなるジョイント登録をする箇所
        Set ボタン押下により、textField へ、カレントで単独選択したジョイントを登録します。
        sel ボタン押下により、登録ジョイントを確認します。
        C ボタン押下により、登録ジョイントを解除します。

    ・ end joint: Spline IK の末端となるジョイント登録をする箇所
        Set ボタン押下により、textField へ、カレントで単独選択したジョイントを登録します。
        sel ボタン押下により、登録ジョイントを確認します。
        C ボタン押下により、登録ジョイントを解除します。

    ・ rename mode: ネーミングのモード選択
        renameTool の help をご覧ください。

        **default: 0(強制的モード)**

    ・ textField: ネーミングの決定
        renameTool の help をご覧ください。
        ::

            e.g.): spineSpIk_spIKHndle     e.g.): spineSpIkA_spIKHndle_L
                tFld A1. spineSpIk             tFld A1. spineSpIk@
                tFld B1. spIKHndle             tFld B1. spIKHndle
                tFld C1. blank                 tFld C1. blank
                tFld C2. blank                 tFld C2. blank
                tFld C3. blank                 tFld C3. L
                         +                              +
                   spineSpIk_spIKCrv              spineSpIkA_spIKCrv_L
        補足):
            第1単語
                ユーザーによる第1単語(tFld A1)入力時には、必ず 'SpIk' 文字列を
                自動で付加する機能を設定しています。
                'SpIk' とは Spline IK の略名です。
            第2単語
                第2単語には予め、役割目を設定済み(ユーザータイピング入力を制限)です。

    ・ Use identifiers for automatic numbering: 自動でナンバリングするための識別子の準備ボタン
        連続で、自動ナンバリングを実行するための on/off です。
        Spline IK は、start joint・end joint の一連に対して通常は必ず一つと考えられますが、万が一他にもネーミングを連番で統一作成する場合に利用します。
        試しに、手動でボタンをトグルしてみると明らかですが、
        第1単語(ローワーキャメルケース記述)入力文字列の末尾に @ (at mark)を自動で 挿入/未挿入 します。

        **default: 0(False)**

    ・ Required parts of ▼ maya default: IK SplineHandle Settings: Spline IK setting 箇所
        maya 標準の、IK Spline Handle Settings の必要箇所を抜粋しています。
        Root on curve:
            ルートを ikSplineHandle のカーブにロックするかどうかを指定します。

            my setting **default: 0(False)**

            maya setting default: 1(True)

        Auto parent curve:
            ikSplineHandle により影響を受ける最初のジョイントの親が、自動的にカーブの親となるかどうかを指定します。

            my setting **default: 0(False)**

            maya setting default: 1(True)

        Auto create curve:
            ikSplineHandle に対してカーブを自動的に作成するかどうかを指定します。

            my setting **default: 1(True)**

            maya setting default: 1(TRue)

        Auto simplify curve:
            ikSplineHandle カーブを単純化するかどうかを指定します。

            my setting **default: 1(True)**

            maya setting default: 1(TRue)

    ・ Grouping:
        適切に Grouping するかを指定します。（独自規格）

        **default: 1(True)**

    ・ ↓↓ naming check ! ↓↓: 命名を予めチェックできるボタン
        押下ください。

-UIを立ち上げずにコマンドベースで実行する方法-
    使用法(usage):
        e.g.): startJoint 'spineA_spIKjt'、
        endJoint 'spineTip_spIKjt'で、
        強制的モードで、'spineSpIk_spIKHndle_L'
        、 'spineSpIk_spIKCrv_L'とネーミングして
        、Root on curve off、Auto parent curve off、Auto create curve on、Auto simplify curve on で
        、Grouping onで
        、実行作成したい時は。。。
            :param mode: str(0/1)    rename mode(ネーミングのモード)
                0(強制的モード)
            :param n: list of string(range 5)
                tFld A1. ベースとなる文字列 + ナンバリング用識別文字列
                    spineSpIk
                tFld B1. 役割等を表す入力領域
                    spIKHndle
                tFld C1. ナンバリング用識別子
                    blank
                tFld C2. 文字列 Gp 識別子
                    blank
                tFld C3. サイド用識別子
                    L
            :param rootOnCurve: bool(0/1)   カーブにロック
                0(False)
            :param parentCurve: bool(0/1)   ジョイントの親が、自動的にカーブの親
                0(False)
            :param createCurve: bool(0/1)   カーブを自動的に作成
                1(True)
            :param simplifyCurve: bool(0/1)   カーブを単純化
                1(True)
            :param startJoint: string   Spline IK のスタートとなるジョイント
                spineA_spIKjt
            :param endEffector: string  Spline IK の末端となるジョイント
                spineTip_spIKjt
            :param grouping: bool(0/1)  適切に Grouping
                1(True)
            mode 0 と、
                'spineSpIk' + '_' + 'spIKHndle' + '_' + '' + '' + 'L' と、
                    rootOnCurve 0, parentCurve 0, createCurve 1, simplifyCurve 1
                        startJoint 'spineA_spIKjt'
                            endJoint 'spineTip_spIKjt'
                                grouping 1
            で構成します。

            <longName>:
                ::

                    YO_createSpIkAndRename3_Modl.CSpIkAndRT_Modl().exe(mode = 0, n = [u'spineSpIk', u'spIKHndle', u'', u'', u'L'], rootOnCurve = 0, parentCurve = 0, createCurve = 1, simplifyCurve = 1, startJoint = u'spineA_spIKjt', endEffector = u'spineTip_spIKjt', grouping = 1)
            <shortName>:
                ::

                    *****

-リマインダ-
    done: 2023/12/22
        - 変換箇所5
            絶対パス から 相対パス へ記述変更
                - YO_createSpIkAndRename3_Modl.py 変更記述あり
                - YO_createSpIkAndRename3_View.py 変更記述あり
                - YO_createSpIkAndRename3_Ctlr.py 変更記述あり
                - YO_createSpIkAndRename3_main.py 変更記述あり
            詳細はそれ自身のリマインダに記述...

        version = '-3.1-'

    done: 2023//10/25
        汎用箇所を、モジュールとして読み込みに変更
            - YO_createSpIkAndRename3_Modl.py 変更記述あり
            - YO_createSpIkAndRename3_View.py 変更記述あり
            - YO_createSpIkAndRename3_main.py 変更記述あり
            詳細はそれ自身のリマインダに記述...

        version = '-3.0-'

    done: 2023/10/04
        python2系 -> python3系 変換
            - YO_createSpIkAndRename3_main.py 変換記述あり
            詳細はそれ自身のリマインダに記述...

        version = '-2.5-'

    done: 2023/09/13~2023/09/20
        python2系 -> python3系 変換
            - YO_createSpIkAndRename3_main.py 変換記述あり
            - YO_createSpIkAndRename3_Modl.py 変換記述あり
            詳細はそれ自身のリマインダに記述...

        version = '-2.0-'

    done: 2023/04/12~2022/04/13
        新規

        version = '-1.0-'
"""

TITLE = 'YO_createSpIkAndRename3'  # MVCモデルを意識しファイル分割した、パッケージ記述
VERSION = '-3.1- <py 3.7.7, ui:PyMel 1.2.0>'
SPACE = ' '

if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
