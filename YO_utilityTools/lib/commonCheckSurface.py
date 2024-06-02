# -*- coding: utf-8 -*-

u"""
commonCheckSurface.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -1.0-
:Date: 2024/04/09

概要(overview):
    ***
詳細(details):
    ***
使用法(usage):
    from commonCheckSurface import commonCheckSurface
    commonCheckSurface()
注意(note):
    ・ 他に必須な独自モジュール
        ::

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

    done: 2021/06/21
        新規
        version = '-1.0-'
"""


# 標準ライブラリ #################################################################

# サードパーティライブラリ #########################################################
import maya.cmds as cmds

# ローカルで作成したモジュール ######################################################
from ..lib.message import message
from ..lib.message_warning import message_warning


# selection が nurbsSurface かどうか調べる関数
def commonCheckSurface(sel = None, *args):
    u"""< selection が nurbsSurface かどうか調べる関数 >

    #######################

    #.
        :param list of str sel:

    #.
        :return: isSurface:
        :rtype isSurface: bool

    #######################
    """
    # print(sel)
    isSurface = False  # type: bool
    if sel:
        shape = cmds.listRelatives(sel, shapes = True)
        if not shape:
            message_warning(u'選択したノード {} は、本来 shape を持っていません。'.format(sel))
            pass
        else:
            isSurface = cmds.objectType(shape[0], isType = 'nurbsSurface')
    else:
        isSurface = False
    return isSurface  # type: bool

if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
