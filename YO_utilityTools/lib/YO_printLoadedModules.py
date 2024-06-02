# -*- coding: utf-8 -*-

u"""
YO_printLoadedModules.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -1.0-
:Date: 2023/10/03

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PyMel version: 1.2.0

概要(overview):
    過去資産ツールの python2系 -> python3系 変換 に伴い、ModuleFinder の再考察
        結果、
            ModuleFinderモジュール を活用した、独自の出力支援モジュールを作成
注意(note):
    当ツールは、
        YO_utilityTools パッケージ専用のハードコーディング記述を含んだ関数を持っています
            故に、万能なコードではございません
注意(note):
    python3系 変換に伴い、python標準ライブラリ modulefinder がエラーを吐き出す恐れがある為、
        回避策を施しています
            いつかは、必要なくなるかもしれません。。。(´；ω；`)ｳｯ…
    回避策箇所:
        ::

          import _locale
          _locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])
注意(note):
    必須なモジュール
        ::

          # python3系記述 python標準ライブラリ modulefinder エラー回避用
          import _locale

          # python標準ライブラリ modulefinder
          from modulefinder import ModuleFinder

-リマインダ-
    done: 2023/10/03
        新規
            PACKAGENAME = 'YO_utilityTools'

        version = '-1.0-'
"""

# エラーを吐き出しへの回避策 記述 ####################################### start
# #########################################
# 説明
# #########################################
# python3系記述になって、python標準ライブラリ modulefinder に対して以下のエラーを吐き出しすことがあります
# それを回避する記述です。よくあるのが、以下のようなエラーサンプルです。
# ####################
# エラーサンプル #######
# ####################
# modulefinder.py line 287: 'cp932' codec can't decode byte 0x87 in position 264: illegal multibyte sequence
import _locale
_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])
# エラーを吐き出しへの回避策 記述 ####################################### end

# python標準ライブラリ modulefinder
from modulefinder import ModuleFinder

import pprint

PACKAGENAME = 'YO_utilityTools'


# ModuleFinderモジュール を活用した、独自の出力支援関数
def print_loaded_modules(file_path):
    u""" < ModuleFinderモジュール を活用した、独自の出力支援関数 です >

    .. note::

        当ツールは、
            YO_utilityTools パッケージ専用のハードコーディング記述を施しています
                故に、万能なコードではございません

    :param file_path: ファイルの絶対パス です
    :type file_path: string
    """
    finder = ModuleFinder()
    finder.load_file(file_path)
    # finder.run_script(file_path)
    # finder.report()
    print('-' * 50)
    print('Loaded modules:')
    for name, mod in finder.modules.items():
        if name.startswith('{}.'.format(PACKAGENAME)):
            print('\t{}: '.format(name))
            # print(name)
            # pprint.pprint(', '.join(mod.globalnames.keys()))
        # print(' ' * 4 + '\n\t'.join(mod.globalnames.keys()))  # test
    print('-' * 50)
    #
    # print('-' * 50)
    # print('Modules not imported:')
    # print(' ' * 4 + '\n\t'.join(finder.badmodules.keys()))
    # print('-' * 50)
    # print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する

if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
