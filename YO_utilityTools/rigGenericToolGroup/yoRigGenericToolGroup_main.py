# -*- coding: utf-8 -*-

u"""
yoRigGenericToolGroup_main.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -2.0-
:Date: 2024/03/17

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PySide2 version: 5.15.2

-リマインダ-
    done: 2024/03/17
        新規

        version = '-2.0-'
    done: 2024/01/26~2024/03/03
        新規

        version = '-1.0-'
"""

# 標準ライブラリ #################################################################
import os
import inspect
# import pprint
from importlib import import_module, reload
import pkgutil

# サードパーティライブラリ #########################################################

# ローカルで作成したモジュール ######################################################
# # パッケージ内のモジュールの更新を都度反映するように記述 ####################### start
# import YO_utilityTools.renameTool  # renameTool パッケージに対して
# for key in YO_utilityTools.renameTool.__dict__:
#     if not key.startswith('__'):
#         reload(YO_utilityTools.renameTool.__dict__[key])
# # パッケージ内のモジュールの更新を都度反映するように記述 ####################### end
#
# # パッケージ内のモジュールの更新を都度反映するように記述 ####################### start
# import YO_utilityTools.createSpaceNode  # createSpaceNode パッケージに対して
# for key in YO_utilityTools.createSpaceNode.__dict__:
#     if not key.startswith('__'):
#         reload(YO_utilityTools.createSpaceNode.__dict__[key])
# # パッケージ内のモジュールの更新を都度反映するように記述 ####################### end
#
# # パッケージ内のモジュールの更新を都度反映するように記述 ####################### start
# import YO_utilityTools.lib  # lib パッケージに対して
# for key in YO_utilityTools.lib.__dict__:
#     if not key.startswith('__'):
#         reload(YO_utilityTools.lib.__dict__[key])
# # パッケージ内のモジュールの更新を都度反映するように記述 ####################### end
#
# # パッケージ内のモジュールの更新を都度反映するように記述 ####################### start
# import YO_utilityTools  # YO_utilityTools パッケージに対して
# for key in YO_utilityTools.__dict__:
#     if not key.startswith('__'):
#         reload(YO_utilityTools.__dict__[key])
# # パッケージ内のモジュールの更新を都度反映するように記述 ####################### end
# 
# # パッケージ内の子階層に、sabパッケージフォルダ が存在しているので、特殊なケース ################# start
# # note): sabパッケージフォルダ のモジュールも同時に読み込むので、多少動作が遅くなります
# import YO_utilityTools.TemplateForPySide2 as package
# assert(hasattr(package, "__path__"))
# for _, module_name, _ in pkgutil.walk_packages(path = package.__path__,
#                                                prefix = package.__name__ + '.',
#                                                onerror = lambda x: None
#                                                ):
#     if not module_name.endswith('__init__'):
#         try:
#             module = import_module(module_name)
#             reload(module)
#             # print(f'Reloaded module: {module_name}')
#         except ImportError as e:
#             print(f'Error reloading module {module_name}: {e}')
# # パッケージ内の子階層に、sabパッケージフォルダ が存在しているので、特殊なケース ################# end
#
# # パッケージ内のモジュールの更新を都度反映するように記述 ####################### start
# import YO_utilityTools.TemplateForPySide2.type2  # TemplateForPySide2 パッケージに対して
# for key in YO_utilityTools.TemplateForPySide2.type2.__dict__:
#     if not key.startswith('__'):
#         reload(YO_utilityTools.TemplateForPySide2.type2.__dict__[key])
# # パッケージ内のモジュールの更新を都度反映するように記述 ####################### end
#
# # パッケージ内のモジュールの更新を都度反映するように記述 ####################### start
# import YO_utilityTools.rigGenericToolGroup  # rigGenericToolGroup パッケージに対して
# for key in YO_utilityTools.rigGenericToolGroup.__dict__:
#     if not key.startswith('__'):
#         reload(YO_utilityTools.rigGenericToolGroup.__dict__[key])
# # パッケージ内のモジュールの更新を都度反映するように記述 ####################### end

# あえてパッケージ宣言  ####################### start
current_file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
# print(f"Current file path: \n\t{current_file_path}")
directoryFullPath = os.path.dirname(current_file_path)
parentDirFullPath = os.path.abspath(os.path.join(directoryFullPath, os.pardir))
fileName = os.path.basename(current_file_path)  # 実行中のファイル名の取得
directory = directoryFullPath.split('\\', )[-1]  # \ で分割したリストの、最後のみ取得
parentDir = parentDirFullPath.split('\\', )[-1]  # \ で分割したリストの、最後のみ取得
# print(fileName)  # yoRigGenericToolGroup_main.py
# print(directory)  # rigGenericToolGroup
# print(parentDir)  # YO_utilityTools
#
# 基本的にはモジュール実行ベースの記述だが、
# PyCharm等のデバッグポート使用時のスクリプト実行も可能にするため、あえてパッケージ宣言
__package__ = f'{parentDir}.{directory}'  # "YO_utilityTools.rigGenericToolGroup"
print(__package__)
# あえてパッケージ宣言  ####################### end

# mvc_model_module_directly_related_to_itself(自身に直接関わるMVCモデルモジュール)
from .yoRigGenericToolGroup_Modl import RigGenTlGp_Modl
from .yoRigGenericToolGroup_View import RigGenTlGp_View
from .yoRigGenericToolGroup_Ctlr import RigGenTlGp_Ctlr

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
    m = RigGenTlGp_Modl()
    v = RigGenTlGp_View(m)
    RigGenTlGp_Ctlr(v, m)


if __name__ == '__main__':
    print('-' * 100)
    print(f'{parentDir}.{directory}.{fileName}: loaded as script file')
    print(f'{current_file_path}')  # 実行したモジュールフルパスを表示する

    # 変換箇所3 ### start-----------------
    # for key in YO_utilityTools.rigGenericToolGroup.__dict__:
    #     if not key.startswith('__'):
    #         # print(YO_utilityTools.rigGenericToolGroup.__dict__[key].__name__)
    #         if key.endswith('_main'):
    #             fileName = YO_utilityTools.rigGenericToolGroup.__dict__[key].__name__
    #             # print(fileName)
    #
    #             print('-' * 100)
    #             print(u'{}.py: loaded as script file'.format(fileName))
    #             filePath = YO_utilityTools.rigGenericToolGroup.__dict__[key].__file__
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
