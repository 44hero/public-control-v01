# -*- coding: utf-8 -*-

u"""
renameTool package

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

概要(overview):
    独自規格の命名規則に基づいた rename ツール の バージョン5(PyMel版)
        MVCモデルパッケージ
            です
詳細(details):
    ・ 独自規格の命名規則とは、
        #.
            第1単語 + 第2単語 + 第3単語 で基本的に構成

        #.
            命名には、多くても 2つの  _(アンダーバー) で必ず構成する

            e.g.): lip_jtA_GpL, lip_jtA, lip_geo, lip_rigGeo

        #.
            第1単語, 第2単語は 必ず小文字で始まる、ローワーキャメルケース記述 を基本とする

            e.g.): lip_jt, lip_geo, lip_rigGeo, lip_jtA_GpL

        #.
            第3単語は 必ず大文字で始まる、アッパーキャメルケース記述 を基本とする

            e.g.): lip_jtA_GpL, lip_jt_AL, lip_jtA_L

        #.
            識別子は、 必ず大文字で始まり、第3単語で使用する事 を基本とする

            識別子とは、
                -a. ナンバリング用識別子(@)

                -b. 文字列 Gp 識別子（グループの意）

                -c. サイド用識別子
            を想定しています

            e.g.): "A", "B", "L", "R", "Gp" ....

        #.
            -a. ナンバリング用識別子 は 第1単語 第2単語 第3単語 どこで使用しても構わないが、2個以上 存在してはいけない

            以下は NG です

            NG. ): lip_jt@_@L, lip@_jt@_L

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
        import YO_utilityTools.renameTool.YO_renameTool5_main
        reload(YO_utilityTools.renameTool.YO_renameTool5_main)
        # from <パッケージ名> import <モジュール名>
        from YO_utilityTools.renameTool import YO_renameTool5_main
        # <モジュール名>.<□□:機能名>()
        YO_renameTool5_main.main()

        # UI立ち上げずに、コマンドで実行するには
        # 以下 e.g.):
        # import <パッケージ名>.<モジュール名>
        import YO_utilityTools.renameTool.YO_renameTool5_Modl
        reload(YO_utilityTools.renameTool.YO_renameTool5_Modl)
        # from <パッケージ名> import <モジュール名>
        from YO_utilityTools.renameTool import YO_renameTool5_Modl
        # <モジュール名>.<クラス名>().<□□:機能名>()
        YO_renameTool5_Modl.RT_Modl().exe(mode = 0, n = [u'lip', u'jt@', u'', u'', u''])

注意(note):
    他に必須な独自モジュール
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
        強制的.
            mode = 0
                もともとのネーミング構成要素を基にせず、強制的にネーミングを整理整頓するモードです
        構成要素をキープ.
            mode = 1
                もともとのネーミング構成要素を基にして、ネーミングを整理整頓するモードです

        **default: 0(強制的モード)**

    ・ textField: ネーミングの決定
        大別して、第1単語, 第2単語, 第3単語 での構成を基本としています
        ::

            | textField A1 | textField B1 | textField C1  textField C2  textField C3 |
            |    第1単語    |    第2単語    | 第3単語-要素1   第3単語-要素2  第3単語-要素3  |
            |    tFld A1   |    tFld B1   |    tFld C1      tFld C2       tFld C3    |

        'tFld A1' + '_' + 'tFld B1' + '_' + 'tFld C1' + 'tFld C2' + 'tFld C3'
            での構成を基本としています

        第1単語(ローワーキャメルケース記述)
            textField A1. 第1単語
                主に一般的な命名入力領域です。
                小文字で始めます。
        第2単語(ローワーキャメルケース記述)
            textField B1. 第2単語
                主に役割等を表す入力領域です。
                小文字で始めます。
                基本的なナンバリング用識別子はここで設定します。
        第3単語(アッパーキャメルケース記述)
            textField C1. 第3単語-要素1
                ナンバリング用識別子領域です。大文字です。
                e.g.): "@" ("A", "B", "AA", "AB" ....)
            textField C2. 第3単語-要素2
                文字列 Gp 識別子領域です。大文字で始めます。
                e.g.): "Gp"
            textField C3. 第3単語-要素3
                サイド用識別子領域です。大文字です。
                e.g.): "L", "R"
        以上5つの textField で構成しています。
        ::

            e.g.): lip_jtA      e.g.): lip_jtA_L    e.g.): lip_jt_AL    e.g.): lip_jt_GpL
                tFld A1. lip        tFld A1. lip        tFld A1. lip        tFld A1. lip
                tFld B1. jt@        tFld B1. jt@        tFld B1. jt         tFld B1. jt
                tFld C1. blank      tFld C1. blank      tFld C1. @          tFld C1. blank
                tFld C2. blank      tFld C2. blank      tFld C2. blank      tFld C2. Gp
                tFld C3. blank      tFld C3. L          tFld C3. L          tFld C3. L

-UIを立ち上げずにコマンドベースで実行する方法-
    使用法(usage):
        e.g.): 強制的モードで、'lip_jtA_L' とネーミングしたい時は。。。
            :param mode: str(0/1)    rename mode(ネーミングのモード)
                0(強制的モード)
            :param n: list of string(range 5)
                tFld A1. ベースとなる文字列
                    lip
                tFld B1. 役割等を表す入力領域 + ナンバリング用識別文字列
                    jt@
                tFld C1. ナンバリング用識別子
                    blank
                tFld C2. 文字列 Gp 識別子
                    blank
                tFld C3. サイド用識別子
                    L
            mode 0 と、
                'lip' + '_' + 'jt@' + '_' + '' + '' + 'L'
            で構成します。

            <longName>:
                ::

                    YO_renameTool5_Modl.RT_Modl().exe(mode = 0, n = [u'lip', u'jt@', u'', u'', u''])
            <shortName>:
                ::

                    *****

-リマインダ-
    done: 2024/05/13~2024/05/15
        - 変更7 と 追加7
            - 概要: maya default の Script Editor へのログ出力 を、
                YO_logProcess.action('ERROR'...)
                YO_logProcess.action('WARNING'...)
                    で行っていた箇所を、
                カスタムの Script Editor2 (PySide2作成UI) で置き換え
                - YO_renameTool5_Modl.py 変更記述あり
                - YO_renameTool5_View.py 変更記述あり
            詳細はそれ自身のリマインダに記述...
        version = '-5.0-'

    done: 2023/12/21
        - 変換箇所6
            絶対パス から 相対パス へ記述変更
                - YO_renameTool5_Modl.py 変更記述あり
                - YO_renameTool5_View.py 変更記述あり
                - YO_renameTool5_Ctlr.py 変更記述あり
                - YO_renameTool5_main.py 変更記述あり
            詳細はそれ自身のリマインダに記述...
        version = '-4.2-'

    done: 2023/11/20
        - 変換箇所5
            - YO_renameTool5_Modl.py 変更記述あり
            詳細はそれ自身のリマインダに記述...

        version = '-4.1-'

    done: 2023//10/26
        汎用箇所を、モジュールとして読み込みに変更
            - YO_renameTool5_Modl.py 変更記述あり
            - YO_renameTool5_View.py 変更記述あり
            - YO_renameTool5_Ctlr.py 変更記述あり
            - YO_renameTool5_main.py 変更記述あり
            詳細はそれ自身のリマインダに記述...

        version = '-4.0-'

    done: 2023/09/25~2023/10/03
        python2系 -> python3系 変換
            - YO_renameTools5_main.py 変換記述あり
            詳細はそれ自身のリマインダに記述...

        version = '-3.5-'

    done: 2023/09/08~2023/09/20
        python2系 -> python3系 変換
            - YO_renameTools5_main.py 変換記述あり
            - YO_renameTools5_Modl.py 変換記述あり
            詳細はそれ自身のリマインダに記述...

        version = '-3.0-'

    done: 2023/03/13~2022/04/13
        派生ファイル作成を考慮してコードの見直し

        version = '-2.0-'

    done: 2023/02/22~2022/02/23
        新規

        version = '-1.0-'
"""

TITLE = 'YO_renameTool5'  # MVCモデルを意識しファイル分割した、パッケージ記述
VERSION = '-5.0- <py 3.7.7, ui:PyMel 1.2.0 + CSE2:PySide2 5.15.2>'
SPACE = ' '

CommandExample = '''
# UI立ち上げずに、コマンドで実行するには
# 以下 e.g.):
# import <パッケージ名>.<モジュール名>
import YO_utilityTools.renameTool.YO_renameTool5_Modl
reload(YO_utilityTools.renameTool.YO_renameTool5_Modl)
# from <パッケージ名> import <モジュール名>
from YO_utilityTools.renameTool import YO_renameTool5_Modl
# <モジュール名>.<クラス名>().<□□:機能名>()
YO_renameTool5_Modl.RT_Modl().exe(mode = 0, n = [u'lip', u'jt@', u'', u'', u''])
'''

if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
