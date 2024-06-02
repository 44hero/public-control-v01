# -*- coding: utf-8 -*-

u"""
YO_jointDrawStyle_change.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -2.0-
:Date: 2023/10/27

使用法(usage):
    YO_jointDrawStyle_change.ui()

-リマインダ-
    done: 2023/10/27
        - python2系 -> python3系 変換

        version = '-2.0-'

    done: 新規作成 2018/01/10
        version = '-1.0-'
"""

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
from functools import partial

defaultArgs = 'rBtn1'


def ui(*args):
    space = ' '
    version = '-2.0- <py 3.7.7 確認済, ui:cmds>'
    title = 'YO_jointDrawStyle_change'
    win = title + '_ui'
    if cmds.window(win, ex = True):
        cmds.deleteUI(win)
    cmds.window(win, title = title[3:] + space + version
                , widthHeight = (145, 60)
                , menuBar = True
                , sizeable = True
                , minimizeButton = False
                , maximizeButton = False
                )

    cmds.columnLayout(adjustableColumn = True)
    cmds.text(label = version, h = 20, annotation = version)

    cmds.separator(h = 10, style = 'shelf')
    collection1 = cmds.radioCollection()
    rBtn1 = cmds.radioButton(label = 'Bone', cc = partial(changeCmd, 'rBtn1'))
    rBtn2 = cmds.radioButton(label = 'Multi-child as Box', cc = partial(changeCmd, 'rBtn2'))
    rBtn3 = cmds.radioButton(label = 'None', cc = partial(changeCmd, 'rBtn3'))
    cmds.radioCollection(collection1, e = True, select = rBtn1)
    cmds.setParent('..')
    cmds.showWindow(win)


def changeCmd(*args):
    def sels():
        sels = cmds.ls(sl = True)
        return sels

    global defaultArgs
    # print(args[0])
    sels = sels()
    # print(sels)
    for selIndex in sels:
        # print(selIndex)
        if args[0] == defaultArgs:
            cmds.setAttr('%s.drawStyle' % selIndex, 0)
        elif args[0] == 'rBtn2':
            cmds.setAttr('%s.drawStyle' % selIndex, 1)
        elif args[0] == 'rBtn3':
            cmds.setAttr('%s.drawStyle' % selIndex, 2)

    if args[0] == defaultArgs:
        message(u'全てのjoint の drawStyle を Bone に設定しました。')
    elif args[0] == 'rBtn2':
        message(u'全てのjoint の drawStyle を Multi-child as Box に設定しました。')
    elif args[0] == 'rBtn3':
        message(u'全てのjoint の drawStyle を None に設定しました。')


# print message メソッド
def message(message_text, *args):
    """
    :param message_text: str
    """
    print('# Result:%s' % message_text)
    om.MGlobal.displayInfo(message_text)


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
    ui()  # ui
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
