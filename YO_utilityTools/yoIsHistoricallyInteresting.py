# -*- coding: utf-8 -*-

u"""
yoIsHistoricallyInteresting.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -1.0-
:Date: 2024/05/01

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PySide2 version: 5.15.2

概要(overview):
    - 通称: IsHistoricallyInteresting
    - 型:
詳細(details):
    オープンしているシーン全体のノードに対して、
        isHistoricallyInteresting 属性を設定することを
            主な目的としています。
    - 基本情報
        setIsHistoricallyInteresting(value = 0): Interesting to no one
            off、チャンネルボックス から 履歴を非表示にする
        setIsHistoricallyInteresting(value = 1): Interesting to Channel Box only
            on、チャンネルボックス のみに 履歴を表示する
        setIsHistoricallyInteresting(value = 2): Interesting to Channel Box and Attribute Editor
            on、チャンネルボックス と アトリビュートエディタ 両方に 履歴を表示する
        プログラマ・TD が関心のあるのは 0 です。
            2 はユーザー用です。
    参考サイト:
        https://kleinhei.nz/2022/08/hide-history-from-channel-box/
        https://groups.google.com/g/python_inside_maya/c/1Ps3uzwqSUQ
使用法(usage):
    ::

        # ローカルで作成したモジュール
        import yoIsHistoricallyInteresting as isHistInter
        reload(isHistInter)

        # 以下 e.g.):
        ############################################################
        # チャンネルボックス から 履歴を非表示にする
        isHistInter.hide()

        # チャンネルボックス のみに 履歴を表示する
        # ここでは使いません
        # setIsHistoricallyInteresting(value = 1)

        # チャンネルボックス と アトリビュートエディタ 両方に 履歴を表示する
        isHistInter.show()
        ##############################

注意(note):
    チャンネルボックス から 履歴を非表示にする 時に、
        ノードの チャンネルボックス SHAPES アトリビュート へも影響されてしまう事を考慮しています。
            そこで、
                チャンネルボックス SHAPES アトリビュート だけは表示して欲しいので、
                    setShowShapesOnly() 関数 を必要としていることは
                        重要です。
    ・ 他に必須なモジュール
        ::

            # サードパーティライブラリ #########################################################
            from maya import cmds

            # ローカルで作成したモジュール ######################################################
            from .lib.message import message

-リマインダ-
    done: 2024/05/01
        新規作成
        version = '-1.0-'
"""

# 標準ライブラリ #################################################################
# from typing import Tuple, List

# サードパーティライブラリ #########################################################
from maya import cmds

# ローカルで作成したモジュール ######################################################
from .lib.message import message
from .lib.commonCheckSelection import commonCheckSelection

# シーン内のすべてのノードに isHistoricallyInteresting 属性を設定する 関数
def setIsHistoricallyInteresting(value = 0):
    u""" < シーン内のすべてのノードに isHistoricallyInteresting 属性を設定する 関数 です >

    ::

        setIsHistoricallyInteresting(value = 0) # チャンネルボックス から 履歴を非表示にする
        setIsHistoricallyInteresting(value = 2) # チャンネルボックス と アトリビュートエディタ 両方に 履歴を表示する

    #######################

    :param int value:
        0: Interesting to no one
            off、チャンネルボックス から 履歴を非表示にする
        1: Interesting to Channel Box only
            on、チャンネルボックス のみに 履歴を表示する
        2: Interesting to Channel Box and Attribute Editor
            on、チャンネルボックス と アトリビュートエディタ 両方に 履歴を表示する
        プログラマ・TD が関心のあるのは 0 です。
            2 はユーザー用です。

    #######################
    """
    # get all dependency nodes
    cmds.select(r = True, allDependencyNodes = True)
    allNodes = cmds.ls(sl = True)
    # get all shapes
    allNodes.extend(cmds.ls(shapes = True))

    failed = []
    for node in allNodes:
        plug = f'{node}.ihi'
        if cmds.objExists(plug):
            try:
                cmds.setAttr(plug, value)
            except:
                failed.append(node)
    if failed:
        print(f'Skipped the following nodes {failed}')

# シーン内のすべてのノードの SHAPES アトリビュートを表示する 関数
def setShowShapesOnly():
    u""" < シーン内のすべてのノードの SHAPES アトリビュートを表示する 関数 です >
    """
    # Get all shape nodes
    shape_nodes = cmds.ls(shapes = True)

    for node in shape_nodes:
        plug = f'{node}.ihi'
        if cmds.objExists(plug):
            try:
                cmds.setAttr(plug, 2)  # Show SHAPES
            except:
                print(f'Failed to set attribute for node: {node}')

# 完全に隠したいとき
def hide():
    keepSels = commonCheckSelection()
    # チャンネルボックス から 履歴を非表示にする
    setIsHistoricallyInteresting(value = 0)
    # チャンネルボックス SHAPES アトリビュート だけは表示して欲しいので以下の関数も必要
    setShowShapesOnly()
    cmds.select(cl = True)
    print('\n' + '###' * 20)
    message('シーン全体のノードに対して、'
            'チャンネルボックスから履歴を非表示にしました。')
    print('###' * 20 + '\n')
    if keepSels:
        cmds.select(keepSels, r = True)
    
# 完全に基に戻し、表示させたいとき
def show():
    keepSels = commonCheckSelection()
    # チャンネルボックス と アトリビュートエディタ 両方に 履歴を表示する
    setIsHistoricallyInteresting(value = 2)
    cmds.select(cl = True)
    print('\n' + '###' * 20)
    message('シーン全体のノードに対して、'
            'チャンネルボックス と アトリビュートエディタ 両方に 履歴を表示する設定にしました。')
    print('###' * 20 + '\n')
    if keepSels:
        cmds.select(keepSels, r = True)



if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
