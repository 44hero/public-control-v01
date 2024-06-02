# -*- coding: utf-8 -*-

u"""
templateForPySide2_type1_Modl.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -1.0-
:Date: 2024/01/26

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PySide2 version: 5.15.2

-リマインダ-
    done: 2023/11/23~2024/01/26
        新規

        version = '-1.0-'
"""

# 標準ライブラリ #################################################################
# from pprint import pprint

# サードパーティライブラリ #########################################################

# ローカルで作成したモジュール ######################################################
# basic_configuration(基本構成)
from .config import SPACE, TITLE, VERSION
# 汎用ライブラリー の使用 #################################################### start
from ...lib.message import message
# 汎用ライブラリー の使用 #################################################### end


class Tpl4PySide2_Type1_Modl(object):
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
    pass
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
