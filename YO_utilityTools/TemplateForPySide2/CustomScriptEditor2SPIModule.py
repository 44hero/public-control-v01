# -*- coding: utf-8 -*-

u"""
CustomScriptEditor2SPIModule.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -1.0-
:Date: 2024/05/10

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PySide2 version: 5.15.2

概要(overview):
    カスタムスクリプトエディタ２用のシングルトンパターンを実装するためのモジュール
    Custom ScriptEditor2 SingletonPattern Implementation Module
        - 通称: CSE2SPIModule
        -
詳細(details):
    使用したいそれぞれのファイルで、
        CustomScriptEditor2 の新しいインスタンスを作成する代わりに、
            これらのインスタンスを一度だけ、ここで作成し、
                これを、他のすべてのファイルの場所で再利用することをお勧めします。
    これは一つの方法であり、
        当ファイルのように、別の Pythonファイル（例えば CustomScriptEditor2SPIModule.py ）を作成し、
            その中で、CustomScriptEditor2 のインスタンスを作成することです。
    これにより、CustomScriptEditor2 のインスタンスは一度だけ作成され、
        例えば、
            SampleA_cmdsUI.py と SampleB_pymelUI.py の両方で共有されるようになります。
    これがシングルトンパターンの一般的な実装方法です。
使用法(usage):
    ::

        # -*- coding: utf-8 -*-
        from YO_utilityTools.singleton import custom_scriptEditor2_instance

        self.scriptEditor2 = custom_scriptEditor2_instance

        # CustomScriptEditor2 ﾓｼﾞｭｰﾙ先では、あえて、show() せず、使用先で show() します。
        self.scriptEditor2.show()  # note): これは必須です。

注意(note):
    ・ 他に必須な独自モジュール
        ::

            # ローカルで作成したモジュール ######################################################
            # Class CustomScriptEditor2 のインスタンスを作成し、UI要素を作成
            from .CustomScriptEditor2 import CustomScriptEditor2

-リマインダ-
    done: 2024/05/10
        新規作成

        version = '-1.0-'
"""

# 標準ライブラリ #################################################################
from importlib import reload

# ローカルで作成したモジュール ######################################################
# Class CustomScriptEditor2 のインスタンスを作成し、UI要素を作成
from .CustomScriptEditor2 import CustomScriptEditor2


_title = 'resultOutputUI_forHeadsUpSpecialization2'
_infoDetail = ('<注意喚起特化用_結果_出力_UI>\n\n'
               '各ｺｰﾄﾞ実行中に頻繁に出力される結果表示において、\n'
               '注意喚起の結果出力だけにフォーカスした、\n'
               '注意喚起特化用UI\n'
               'です。\n\n'
               'note): \n'
               '右ボタン押下でエディタ用途として\n簡単な編集も可能です。')

custom_scriptEditor2_instance = CustomScriptEditor2(title = _title, infoDetail = _infoDetail)


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
