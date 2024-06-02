# -*- coding: utf-8 -*-

u"""
yoGetAttributeFromModule.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -1.0-
:Date: 2024/03/16

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PySide2 version: 5.15.2

概要(overview):
    - 通称:
    - 型:
詳細(details):
    任意のモジュールに対し、
        内包されている、関数(メソッド)、プロパティ を
            明示します
    関数 プロパティ の順に、アルファベット順にソートして出力します。
使用法(usage):
    :param str moduleName: 任意のモジュール名
        は、必須です。
    ::

        # ローカルで作成したモジュール
        import yoGetAttributeFromModule
        reload(yoGetAttributeFromModule)
        from yoGetAttributeFromModule import GetAttrFrmMod

        # 以下 e.g.):
        ############################################################
        GetAttrFrmMod(moduleName = 'Container')
        ##############################

-リマインダ-
    done: 2024/03/16
        新規作成

        version = '-1.0-'
"""
# 標準ライブラリ #################################################################
import inspect
# from typing import Tuple, List

# サードパーティライブラリ #########################################################

# ローカルで作成したモジュール ######################################################


class GetAttrFrmMod(object):
    def __init__(self, moduleName: str) -> None:
        u"""

        :rtype: None
        :param moduleName: 任意のモジュール名
        :type moduleName: str
        """
        # print(type(moduleName))
        # print('')
        # モジュールのアトリビュートを取得
        attributes_dict = moduleName.__dict__

        # 関数とプロパティを分けてリストに追加
        functions = []
        properties = []
        for attribute_name, attribute_value in attributes_dict.items():
            if attribute_name != "__init__":
                if inspect.isfunction(attribute_value):
                    functions.append((attribute_name, attribute_value))
                elif isinstance(attribute_value, property):
                    properties.append((attribute_name, attribute_value))

        # 関数とプロパティをアルファベット順にソート
        functions.sort(key = lambda x: x[0])
        properties.sort(key = lambda x: x[0])

        print(f'\n'
              f'指定したモジュール:\n'
              f'\t{moduleName}\n'
              f'は、以下の 関数 と プロパティ をアトリビュートとして保持しています。')
        print('###' * 10)
        # ソートされたリストを表示
        for index, (attribute_name, attribute_value) in enumerate(functions + properties):
            print(f'{index}. {attribute_name}: '
                  f'\n\t'
                  f'{attribute_value}'
                  , end = '\n'
                  )
        print('###' * 10)


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
