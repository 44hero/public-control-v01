# -*- coding: utf-8 -*-

u"""
pointConstraintByMatrix package

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -5.0-
:Date: 2024/05/16

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PyMel version: 1.2.0
    - PySide2 version: 5.15.2

概要(overview):
    matrix を使用した、point constraint を自動作成するツールです。
詳細(details):
    新規に、pointConstraint と同等な拘束処理を matrix 操作で実現します。

    具体的には、
        multMatrix の matrixIn[0] への setAttr 及び .matrixIn[1] への connectAttr
            から始まり、最後まで完了させており、
                また、multMatrix node -->> decomposeMatrix node のコネクションに至るまで、全ての必要な
                    工程を行っています。

    因みに、target が transform node の時と joint node の時とで、
        作成される node 数と connection 方法に若干の違いがあります。

    **------ note): ここのみ、一旦キャンセルしています。何らかの形で、復活の可能性あり。------ start**
        具体的には、
            target が joint node の時には、
            target の jointOrient も考慮しています。
    **------ note): ここのみ、一旦キャンセルしています。何らかの形で、復活の可能性あり。------ end**

    類似した python module ファイル
        YO_parentConstraintByMatrix62.py ツール (自動接続用)
            をベースに、当ツールを作成。

    当ツールは、
        その、自動作成バージョンにあたり、簡潔な、コード記述実行を目的としています。

    ・ text ベースのコマンド 出力を搭載
        UI操作実行後、 maya script editor には必ず、text ベースのコマンド を出力も致します。
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
        import YO_utilityTools.pointConstraintByMatrix.YO_pointConstraintByMatrix1_main
        reload(YO_utilityTools.pointConstraintByMatrix.YO_pointConstraintByMatrix1_main)
        # from <パッケージ名> import <モジュール名>
        from YO_utilityTools.pointConstraintByMatrix import YO_pointConstraintByMatrix1_main
        # <モジュール名>.<□□:機能名>()
        YO_pointConstraintByMatrix1_main.main()

    <接続編>
        ::

            # UI立ち上げずに、コマンドで実行するには
            # 以下 e.g.):
            # import <パッケージ名>.<モジュール名>
            import YO_utilityTools.pointConstraintByMatrix.YO_pointConstraintByMatrix1_Modl
            reload(YO_utilityTools.pointConstraintByMatrix.YO_pointConstraintByMatrix1_Modl)
            # from <パッケージ名> import <モジュール名>
            from YO_utilityTools.pointConstraintByMatrix import YO_pointConstraintByMatrix1_Modl
            YO_pointConstraintByMatrix1_Modl.PConByMat_Modl().command(connect = True, source = 'spineC', target = 'spineC_jtPxy')

    <切断編>
        ::

            # UI立ち上げずに、コマンドで実行するには
            # 以下 e.g.):
            # import <パッケージ名>.<モジュール名>
            import YO_utilityTools.pointConstraintByMatrix.YO_pointConstraintByMatrix1_Modl
            reload(YO_utilityTools.pointConstraintByMatrix.YO_pointConstraintByMatrix1_Modl)
            # from <パッケージ名> import <モジュール名>
            from YO_utilityTools.pointConstraintByMatrix import YO_pointConstraintByMatrix1_Modl
            YO_pointConstraintByMatrix1_Modl.PConByMat_Modl().brkAndRest_command(target = 'spineC_jtPxy')

注意(note):
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
    ・ source : 制御する側
        コントローラです。 set 入力してください。
    ・ target : 制御される側
        コントロールされる方です。 拘束を必要とする方です。 set 入力してください。

-UIを立ち上げずにコマンドで実行する方法-
    補足(supplementary explanation):
        「接続の有無」,「制御する」側,「制御される」側 さえ明確ならば、UIを立ち上げずにコマンドで実行も出来ます。
    <接続編>
        使用法(usage):
            <各コマンド 説明>
                connect, ct:  「接続の有無」 :bool:
                    e.g.)True
                source, src: 「制御する」側 名 :string:
                    e.g.)'spineC'
                target, tgt: 「制御される」側 名 :string:
                    e.g.)'spineC_jtPxy'

            <longName>:
                ::

                    YO_pointConstraintByMatrix1_Modl.PConByMat_Modl().command(connect = True
                    , source = 'spineC'
                    , target = 'spineC_jtPxy'
                    )
            <shortName>:
                ::

                    YO_pointConstraintByMatrix1_Modl.PConByMat_Modl().command(ct = True
                    , src = 'spineC'
                    , tgt = 'spineC_jtPxy'
                    )
    <切断編>
        使用法(usage):
            <各コマンド 説明>
                target, tgt: 「切断したい、制御されているノード」側 名 :string:
                    e.g.)'spineC_jtPxy'

            <longName>:
                ::

                    YO_pointConstraintByMatrix1_Modl.PConByMat_Modl().brkAndRest_command(target = 'spineC_jtPxy')
            <shortName>:
                ::

                    YO_pointConstraintByMatrix1_Modl.PConByMat_Modl().brkAndRest_command(tgt = 'spineC_jtPxy')

.. note::
    リマインダ-記述内の、
        version = '-3.0-'
            変更箇所2

    これに付随して、

    リマインダ-記述内の、
        version = '-4.0-'
            生かさない箇所1

    相互に大きく関連有り

-リマインダ-
    done: 2024/05/25
        - 変更12
            - 概要: source, target について、
                片方もしくは両方が シーンに存在しない時、
                以降の実行中止させる 明示と中止の実行
                - YO_pointConstraintByMatrix1_Modl.py 変更記述あり
            詳細はそれ自身のリマインダに記述...
        version = '-5.5-'

    done: 2024/05/16
        - 暫定追加修正1
            - 概要: 想定を超えていた、ネーミング が上手く発動しない箇所を修正
                - YO_pointConstraintByMatrix1_Modl.py 変更記述あり
            詳細はそれ自身のリマインダに記述...
        version = '-5.0-'

    done: 2024/05/16
        - 修正11
            - 概要: maya default の Script Editor へのログ出力 を、
                YO_logProcess.action('ERROR'...)
                YO_logProcess.action('WARNING'...)
                    で行っていた箇所を、
                カスタムの Script Editor2 (PySide2作成UI) で置き換え
                - YO_pointConstraintByMatrix1_Modl.py 変更記述あり
                - YO_pointConstraintByMatrix1_View.py 変更記述あり
            詳細はそれ自身のリマインダに記述...
        version = '-5.0-'

    done: 2024/05/16
        - 修正10
            - 概要: バグ修正
            - 詳細: ソースに 親が無くワールド空間の場合 発生
                - YO_pointConstraintByMatrix1_Modl.py 変更記述あり
            詳細はそれ自身のリマインダに記述...
        version = '-5.0-'

    done: 2024/05/15
        - 修正箇所9
            - 概要: バグ修正
            - 詳細: ターゲットが 必ずしも joint とは限らない場合に 発生
                - YO_pointConstraintByMatrix1_Modl.py 変更記述あり
            詳細はそれ自身のリマインダに記述...
        version = '-5.0-'

    done: 2024/01/04
        - 変換箇所8
            絶対パス から 相対パス へ記述変更
                - YO_pointConstraintByMatrix1_Modl.py 変更記述あり
                - YO_pointConstraintByMatrix1_View.py 変更記述あり
                - YO_pointConstraintByMatrix1_Ctlr.py 変更記述あり
                - YO_pointConstraintByMatrix1_main.py 変更記述あり
            詳細はそれ自身のリマインダに記述...
        version = '-4.3-'

    done: 2023/11/20
        - 変換箇所7
            - YO_pointConstraintByMatrix1_Modl.py 変更記述あり
            詳細はそれ自身のリマインダに記述...
        version = '-4.2-'

    done: 2023/11/17
        - 新規2
            - YO_pointConstraintByMatrix1_Modl.py 変更記述あり
            詳細はそれ自身のリマインダに記述...

        version = '-4.1-'

    done: 2023/11/16
        - 生かさない箇所1
            - YO_pointConstraintByMatrix1_Modl.py 変更記述あり
            詳細はそれ自身のリマインダに記述...

        version = '-4.0-'

    done: 2023/11/03~2023/11/09
        - 変更箇所2
            - YO_pointConstraintByMatrix1_Modl.py 変更記述あり
            詳細はそれ自身のリマインダに記述...

        version = '-3.0-'

    done: 2023/10/26
        汎用箇所を、モジュールとして読み込みに変更
            - YO_pointConstraintByMatrix1_Modl.py 変更記述あり
            - YO_pointConstraintByMatrix1_View.py 変更記述あり
            - YO_pointConstraintByMatrix1_Ctlr.py 変更記述あり
            - YO_pointConstraintByMatrix1_main.py 変更記述あり
            詳細はそれ自身のリマインダに記述...

        version = '-2.0-'

    done: 2023/10/16
        - 変更箇所1
            - YO_pointConstraintByMatrix1_Modl.py 更記述あり
            - YO_pointConstraintByMatrix1_View.py 更記述あり
            詳細はそれ自身のリマインダに記述...

        version = '-1.1-'

    done: 2023/10/12~2023/10/16
        新規

        version = '-1.0-'
"""

TITLE = 'YO_pointConstraintByMatrix1'  # MVCモデルを意識しファイル分割した、パッケージ記述
VERSION = '-5.5- <py 3.7.7, ui:PyMel 1.2.0 + CSE2:PySide2 5.15.2>'
SPACE = ' '

CommandExample = '''
<接続編>
# UI立ち上げずに、コマンドで実行するには
# 以下 e.g.):
# import <パッケージ名>.<モジュール名>
import YO_utilityTools.pointConstraintByMatrix.YO_pointConstraintByMatrix1_Modl
reload(YO_utilityTools.pointConstraintByMatrix.YO_pointConstraintByMatrix1_Modl)
# from <パッケージ名> import <モジュール名>
from YO_utilityTools.pointConstraintByMatrix import YO_pointConstraintByMatrix1_Modl
YO_pointConstraintByMatrix1_Modl.PConByMat_Modl().command(connect = True, source = 'spineC', target = 'spineC_jtPxy')

<切断編>
# UI立ち上げずに、コマンドで実行するには
# 以下 e.g.):
# import <パッケージ名>.<モジュール名>
import YO_utilityTools.pointConstraintByMatrix.YO_pointConstraintByMatrix1_Modl
reload(YO_utilityTools.pointConstraintByMatrix.YO_pointConstraintByMatrix1_Modl)
# from <パッケージ名> import <モジュール名>
from YO_utilityTools.pointConstraintByMatrix import YO_pointConstraintByMatrix1_Modl
YO_pointConstraintByMatrix1_Modl.PConByMat_Modl().brkAndRest_command(target = 'spineC_jtPxy')
'''

if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
