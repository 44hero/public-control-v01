# -*- coding: utf-8 -*-

u"""
commonCheckShape.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -1.0-
:Date: 2024/04/09

概要(overview):
    ノード1 が shape を持っているかどうか調べる関数
詳細(details):
    リターンは bool(True or False)
使用法(usage):
    from commonCheckShape import commonCheckShape
    e.g.:
        ノード1:sel
    commonCheckShape(sel)
注意(note):
    ・ 他に必須な独自モジュール
        ::

            # 標準ライブラリ #################################################################
            import re

            # サードパーティライブラリ #########################################################
            import maya.cmds as cmds

            # ローカルで作成したモジュール ######################################################
            from ..lib.message import message
            from ..lib.message_warning import message_warning

-リマインダ-
    done: 2024/04/09
        修正
            概要:
            詳細: print を message_warning モジュールに変更
        version = '-2.0-'

    done: 2024/04/09
        新規
        version = '-1.0-'
"""


# 標準ライブラリ #################################################################
import re

# サードパーティライブラリ #########################################################
import maya.cmds as cmds

# ローカルで作成したモジュール ######################################################
from ..lib.message import message
from ..lib.message_warning import message_warning


# selection が shape を持っているかどうか調べる関数
def commonCheckShape(sel = None, *args):
    u"""< selection が curve かどうか調べる関数 >

    #######################

    #.
        :param list of str sel:

    #.
        :return hasShape:
        :rtype hasShape: bool

    #######################
    """
    # print(sel)
    hasShape = False  # type: bool
    if sel:
        shape = cmds.listRelatives(sel, shapes = True)
        if not shape:
            message_warning(u'選択したノード {} は、本来 shape を持っていません。'.format(sel))
            pass
        else:
            # print(shape)
            # ワイルドカード
            wildcard = 'Orig'
            # 正規表現パターンを作成: 末尾に wildcard の有無で判断
            pattern = re.compile(f'.*{wildcard}\d*$')
            # 条件に一致しない要素を抽出
            pureShape_list = [item for item in shape if not pattern.match(item)]
            print(pureShape_list)
            # isCurve = cmds.objectType(shape[0], isType = 'nurbsCurve')
            hasShape = True
    else:
        hasShape = False
    return hasShape  # type: bool


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
