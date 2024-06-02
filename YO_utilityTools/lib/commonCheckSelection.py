# -*- coding: utf-8 -*-

u"""
commonCheckSelection.py

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
    from commonCheckSelection import commonCheckSelection
    commonCheckSelection()
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

    done: 2020/06/17
        新規
        version = '-1.0-'
"""


# 標準ライブラリ #################################################################

# サードパーティライブラリ #########################################################
import maya.cmds as cmds

# ローカルで作成したモジュール ######################################################
from ..lib.message import message
from ..lib.message_warning import message_warning


# selection 共通関数 v3 -flatten込み
def commonCheckSelection(*args):
    u"""< selection 共通関数 v3 -flatten込み >

    #######################

    #.
        :return: selList
        :rtype selList: list of str

    #######################
    """
    selList = cmds.ls(sl = True, flatten = True) or []
    # print(selList)
    # if not len(selList):
    #     print('\n' + '***' * 10)
    #     print(u'# result : node を選択し、してください。')
    #     print('***' * 20 + '\n')
    # else:
    #     print('\n' + '***' * 10)
    #     print(u'# result : commonCheckSelection:継続中')
    #     print('***' * 10 + '\n')
    # print(selList)
    # print(type(selList))
    # for index in selList:
    # print(index)
    # print(type(index))  # type 'unicode'
    return selList

if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
    commonCheckSelection()
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
