# -*- coding: utf-8 -*-

u"""
YO_validate.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -1.0-
:Date: 2023/10/26

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PyMel version: 1.2.0

概要(overview):
    - validate_func
        Pythonで作った自作関数を使用する時に、
            意図しない利用や挙動を検出するために、引数と返り値の型をチェックするデコレータとして機能。
        型アノテーションを利用するため、Python3が前提。
        内容をログに出すことで、デバッグする際にも役立ちます。
    - type_checked
        実行時の、任意の関数の引数の型チェック、が行えます
使用法(usage):
    - validate_func
        モジュールとして import した後、
            以下のように、アノテーションを必要な関数の先頭に記述します

        ::

          from YO_utilityTools.lib.YO_validate import validate_func
          # ...
          @validate_func
          def ***(self, ****):
            ...

    - type_checked
        モジュールとして import した後、
            例えば以下のように記述します

        ::

          from YO_utilityTools.lib.YO_validate import type_checked
          # ...
          ####################### sample type_checked ###############
          x = type_checked(strsCompLists, str)
          print(x)
          ####################### sample type_checked ###############

        .. note::
            - e.g.):
                上記のコードの内、以下の記述
                    type_checked(strsCompLists, str)
                の時は、
                    :param str strsCompLists: 第一引数
                        調べたい引数を文字列
                    :param type str: 第二引数
                        この箇所は、期待する型
                        e.g.): str, int, list, bool, float...
                を記述
            - 重要:
                str: この箇所を期待する型で記述しなければ、
                    プログラムはそこで停止します

-リマインダ-
done: 2023/10/26
    新規

    version = '-1.0-'
"""

import inspect


# 意図しない利用や挙動を検出するために、引数と返り値の型をチェックします
def validate_func(func):
    u""" < 意図しない利用や挙動を検出するために、引数と返り値の型をチェックする 関数 です >

    ::

      型アノテーションを利用するため、Python3が前提。
        内容をログに出すことで、デバッグする際にも役立ちます。

    #######################

    #.
        :return: validate_func_wrapper
        :rtype:

    #######################
    """
    def validate_func_wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        args_value = sig.bind(*args, **kwargs)  # 引数名と値のdict

        # 引数の検証
        for args_name, args_value in args_value.arguments.items():
            print(args_name, args_value)
            args_type = sig.parameters[args_name].annotation
            # 型が指定されている(not empty)、かつ 型が一致していない場合エラー
            if args_type is not inspect._empty and type(args_value) != args_type:
                raise Exception('引数の型が異なります')
            print(u'引数 {} は正常です\n'.format(args_name))

        results = func(*args, **kwargs)

        # 返り値の検証
        return_type = sig.return_annotation
        # 型が指定されている(not empty)、かつ型が一致していない場合エラー
        if return_type is not inspect._empty and type(results) != return_type:
            raise Exception('返り値の型が異なります')
        print(u'返り値の型は正常です\n\n')

        return results
    return validate_func_wrapper


# 実行時の、任意の関数の引数の型チェック、が行えます
def type_checked(x: str, type_: type) -> tuple:
    u""" < 実行時の、任意の関数の引数の型チェック 関数 です >

    ::

      :param type type_: 第二引数
       この箇所を期待する型で記述しなければ、
        プログラムはそこで停止します

    #######################

    #.
        :param str x: 第一引数
            調べたい引数

        :param type type_: 第二引数
            望んだ型
            e.g.): int, list, bool, float...

    #.
        :return: x, type_
        :rtype: tuple[str. str]

    #######################
    """
    if not isinstance(x, type_):
        raise TypeError(f"x must be instance of {type_} but actual type {type(x)}.")
    return x, type_


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
