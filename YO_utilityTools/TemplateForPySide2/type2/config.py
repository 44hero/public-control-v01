# -*- coding: utf-8 -*-

u"""
TemplateForPySide2_type2 package

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -1.0-
:Date: 2024/03/07

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PySide2 version: 5.15.2

概要(overview):
    PySide2 UI の、タブ有りの ひな形 です。
    - 通称: type2
詳細(details):
    タブを必要とするUIの、ひな形となります。

    当、モジュールをクラス継承して、
        当方の PySide2 タブ有りのUI は作成されています。

-リマインダ-
    done: 2024/03/07
        新規

        version = '-1.0-'
"""

TITLE = 'TemplateForPySide2_type2'  # MVCモデルを意識しファイル分割した、パッケージ記述
VERSION = '-1.0- <py 3.7.7, ui:PySide2 5.15.2>'
SPACE = ' '

if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
