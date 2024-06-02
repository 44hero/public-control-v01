# -*- coding: utf-8 -*-

u"""
YO_shearConstraintByMatrix1_main.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -2.3-
:Date: 2024/01/04

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PyMel version: 1.2.0

-リマインダ-
    done: 2024/01/04
        - 変換箇所8
            - 概要: 絶対パス から 相対パス へ記述変更
            - 詳細:
                ::

                  -     from YO_utilityTools.shearConstraintByMatrix.[...] import ...
                  +     from .[...] import ...

                  -     from YO_utilityTools.lib.[...] import ...
                  +     from ..lib.[...] import ...

        version = '-2.3-'

    done: 2023/11/13~2023/11/15
        新規

        version = '-1.0-'
"""

# 標準ライブラリ
import os
import inspect
# from functools import partial  # partial 利用時は、最後の引数に、*args 要時あり
# import pprint
from importlib import reload

# サードパーティライブラリ

# ローカルで作成したモジュール
# # パッケージ内のモジュールの更新を都度反映するように記述 ####################### start
# import YO_utilityTools.shearConstraintByMatrix  # pointConstraintByMatrix パッケージに対して
# for key in YO_utilityTools.shearConstraintByMatrix.__dict__:
#     if not key.startswith('__'):
#         reload(YO_utilityTools.shearConstraintByMatrix.__dict__[key])
# # パッケージ内のモジュールの更新を都度反映するように記述 ####################### end
#
# # パッケージ内のモジュールの更新を都度反映するように記述 ####################### start
# import YO_utilityTools.lib  # lib パッケージに対して
# for key in YO_utilityTools.lib.__dict__:
#     if not key.startswith('__'):
#         reload(YO_utilityTools.lib.__dict__[key])
# # パッケージ内のモジュールの更新を都度反映するように記述 ####################### end

# あえてパッケージ宣言  ####################### start
current_file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
# print(f"Current file path: \n\t{current_file_path}")
directoryFullPath = os.path.dirname(current_file_path)
parentDirFullPath = os.path.abspath(os.path.join(directoryFullPath, os.pardir))
fileName = os.path.basename(current_file_path)  # 実行中のファイル名の取得
directory = directoryFullPath.split('\\', )[-1]  # \ で分割したリストの、最後のみ取得
parentDir = parentDirFullPath.split('\\', )[-1]  # \ で分割したリストの、最後のみ取得
# print(fileName)  # YO_shearConstraintByMatrix1_main.py
# print(directory)  # shearConstraintByMatrix
# print(parentDir)  # YO_utilityTools
#
# 基本的にはモジュール実行ベースの記述だが、
# PyCharm等のデバッグポート使用時のスクリプト実行も可能にするため、あえてパッケージ宣言
__package__ = f'{parentDir}.{directory}'  # "YO_utilityTools.shearConstraintByMatrix"
# あえてパッケージ宣言  ####################### end

# mvc_model_module_directly_related_to_itself(自身に直接関わるMVCモデルモジュール)
from .YO_shearConstraintByMatrix1_Modl import ShConByMat_Modl
from .YO_shearConstraintByMatrix1_View import ShConByMat_View
from .YO_shearConstraintByMatrix1_Ctlr import ShConByMat_Ctlr

# 変換箇所4 ### start-----------------
# YO_printLoadedModules モジュールの print_loaded_modules 関数の読み込み
# from ..lib.YO_printLoadedModules import print_loaded_modules
# 変換箇所4 ### end-----------------


def main():
    u""" < アプリケーションのエントリーポイントである main関数 です >

    ::

      Model、 View、 Controller を作成し、
        アプリケーションを開始するためのロジックを提供します。
      Controllerクラス のインスタンスを生成してアプリケーションを実行します。
    """
    m = ShConByMat_Modl()
    v = ShConByMat_View(m)
    ShConByMat_Ctlr(v, m)


if __name__ == '__main__':
    print('-' * 100)
    print(f'{parentDir}.{directory}.{fileName}: loaded as script file')
    print(f'{current_file_path}')  # 実行したモジュールフルパスを表示する

    # 変換箇所3 ### start-----------------
    # for key in YO_utilityTools.shearConstraintByMatrix.__dict__:
    #     if not key.startswith('__'):
    #         # print(YO_utilityTools.shearConstraintByMatrix.__dict__[key].__name__)
    #         if key.endswith('_main'):
    #             fileName = YO_utilityTools.shearConstraintByMatrix.__dict__[key].__name__
    #             # print(fileName)
    #
    #             print('-' * 100)
    #             print(u'{}.py: loaded as script file'.format(fileName))
    #             filePath = YO_utilityTools.shearConstraintByMatrix.__dict__[key].__file__
    #             # print(filePath)
    #             print('{}'.format(filePath))
    #             # print_loaded_modules(filePath)  # 開発時(development)のみコメントアウトの除外を推奨
    #             print('-' * 100)
    # # 変換箇所3 ### end-----------------

    # print_loaded_modules(current_file_path)  # 開発時(development)のみコメントアウトの除外を推奨

    print('-' * 100)
    main()
else:
    print('-' * 100)
    print(f'{__name__}.py: loaded as module file')
    print(f'{__file__}')  # 実行したモジュールフルパスを表示する

    # 変換箇所3 ### start-----------------
    filePath = __file__
    # print_loaded_modules(filePath)  # 開発時(development)のみコメントアウトの除外を推奨
    # 変換箇所3 ### end-----------------
    print('-' * 100)
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
