# -*- coding: utf-8 -*-

u"""
commonCheckJoint.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -1.0-
:Date: 2024/04/09

概要(overview):
    ノード1 が joint どうか調べる関数
詳細(details):
    リターンは bool(True or False)
使用法(usage):
    from commonCheckJoint import commonCheckJoint
    e.g.:
        ノード1:sel
    commonCheckJoint(sel)
注意(note):
    ・ 他に必須な独自モジュール
        ::

            # サードパーティライブラリ #########################################################
            import maya.cmds as cmds

-リマインダ-
    done: 2024/04/09
        修正
            概要:
            詳細: print を message_warning モジュールに変更
        version = '-2.0-'

    done: 2020/07/03
        新規
        version = '-1.0-'
"""


# 標準ライブラリ #################################################################

# サードパーティライブラリ #########################################################
import maya.cmds as cmds

# ローカルで作成したモジュール ######################################################


# selection が joint かどうか調べる関数
def commonCheckJoint(sel = None, *args):
    u"""< selection が joint かどうか調べる関数 >

    #######################

    #.
        :param str sel:

    #.
        :return: isJoint
        :rtype isJoint: bool

    #######################
    """
    # print(sel)
    isJoint = False  # type: bool
    if sel:
        isJoint = cmds.objectType(sel, isType = 'joint')
    else:
        isJoint = False
    return isJoint  # type: bool

if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
    commonCheckJoint()
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
