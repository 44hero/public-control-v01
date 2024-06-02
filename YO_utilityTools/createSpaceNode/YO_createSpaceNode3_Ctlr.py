# -*- coding: utf-8 -*-

u"""
YO_createSpaceNode3_Ctlr.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -3.1-
:Date: 2023/12/21

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PyMel version: 1.2.0

-リマインダ-
    done: 2023/12/21
        - 変換箇所5
            - 概要: 絶対パス から 相対パス へ記述変更
            - 詳細:
                ::

                  -     from YO_utilityTools.renameTool.YO_renameTool5_Ctlr import RT_Ctlr
                  +     from ..renameTool.YO_renameTool5_Ctlr import RT_Ctlr

        version = '-3.1-'

    done: 2023/04/17~2023/05/08
        新規

        version = '-1.0-'
"""

# 標準ライブラリ
# import pprint

# サードパーティライブラリ

# ローカルで作成したモジュール
# mvc_model_module_that_become_derived_basis(派生基となるMVCモデルモジュール)
from ..renameTool.YO_renameTool5_Ctlr import RT_Ctlr


class CSpaceNode_Ctlr(RT_Ctlr):
    u""" < View と Model をつなぐ Controllerクラス です >

    ::

      UIとモデルを結びつけるためのメソッドを実装します。

      Viewクラス と Modelクラス への参照を受け取り、
        View からのユーザーアクションを処理し、
            Model からのデータ変更を View に反映させるロジックを実装します。
    """
    def __init__(self, _view, _model):
        super(CSpaceNode_Ctlr, self).__init__(_view, _model)

    # 他の def は、base RT_Ctlr から全て再利用しています。

if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
