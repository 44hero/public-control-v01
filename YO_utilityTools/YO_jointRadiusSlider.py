# -*- coding: utf-8 -*-

u"""
YO_jointRadiusSlider.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -2.0-
:Date: 2023/10/27

使用法(usage):
    YO_jointRadiusSlider.ui()

-リマインダ-
    done: 2023/10/27
        - python2系 -> python3系 変換
            - print組み込み関数 箇所

        version = '-2.0-'

    done: 2018/01/10
        - 新規
        version = '-1.0-'
"""

import maya.cmds as cmds
from functools import partial


def ui(*args):
    space = ' '
    version = '-2.0- <py 3.7.7 確認済, ui:cmds>'
    if cmds.window('jointRadiusSlider', exists = True):
        cmds.deleteUI('jointRadiusSlider')

    window = cmds.window('jointRadiusSlider'
                         , title = 'jointRadiusSlider' + space + version
                         , menuBar = True
                         , w = 250, h = 280
                         , sizeable = True
                         , minimizeButton = False
                         , maximizeButton = False
                         )
    cmds.columnLayout(adj = True)

    cmds.columnLayout(adjustableColumn = True)
    cmds.text(label = version, h = 20, annotation = version)

    cmds.paneLayout()
    selLists = cmds.textScrollList('selLists', numberOfRows = 10,
                                   allowMultiSelection = True, w = 10, dcc = 'selItems()',
                                   ann = u'選択しているjointにだけradius編集を実行します')
    cmds.setParent('..')
    cmds.columnLayout()
    cmds.button('Sets', l = 'Sets', c = partial(selectsSets),
                ann = u'選択したjointをリストとしてセットします。')
    setJSSld = cmds.floatSliderGrp('setJointSizeSlider', label = 'joint radius',
                                   field = True, minValue = 0.1, maxValue = 1.0,
                                   fieldMinValue = 0.001, fieldMaxValue = 5.0, value = 0.5,
                                   pre = 2, cc = partial(changeSlider),
                                   cw3 = [55, 40, 140])
    cmds.button('selectSetsAll', l = 'Select Sets All', c = partial(selectSetsAll),
                ann = u'登録済みのjointリストを全選択できます。')
    cmds.button('setsAllClear', l = 'Sets All Clear', c = partial(setsAllClear),
                bgc = (0.4, 0.4, 0.4), ann = u'登録済みのjointリストを解除できます。')
    cmds.button(label = 'Close', c = 'cmds.deleteUI("jointRadiusSlider")')
    cmds.showWindow(window)


def selectsSets(*args):
    sels = cmds.ls(sl = True, typ = 'joint')
    cmds.select(cl = True)
    print(u'実行できています。\n')
    try:
        cmds.select(sels, r = True)
        print(u'一つ以上のjoint が、格納されています。\n')
        print(u'リストに格納されているjointの半径をスライダーで編集できます。\n')
        cmds.textScrollList('selLists', e = True, a = sels)
        qSetJSSldValue = cmds.floatSliderGrp('setJointSizeSlider', q = True, v = True)
        for sel in sels:
            cmds.setAttr('%s.radius' % sel, qSetJSSldValue)
        cmds.button('Sets', e = True, en = False)
        cmds.button('selectSetsAll', e = True, bgc = (0.5, 0.5, 0.8))
    except:
        print(u'note: 何か選択したうえで実行してみてください。\n')
        pass


def selItems(*args):
    sels = cmds.textScrollList("selLists", q = True, si = True)
    cmds.select(sels, r = True)


def selectSetsAll(*args):
    sels = cmds.textScrollList("selLists", q = True, ai = True)
    cmds.select(sels, r = True)
    print(u'格納済みの全jointを選択しています。\n')


def setsAllClear(*args):
    cmds.textScrollList("selLists", e = True, ra = True)
    cmds.button('Sets', e = True, en = True)
    cmds.button('selectSetsAll', e = True, bgc = (0.5, 0.5, 0.5))
    print(u'格納済みの全jointを Sets から解除しました。\n')


def changeSlider(*args):
    js = setsJoints()  # print js
    para = cmds.floatSliderGrp('setJointSizeSlider', q = True, v = True)
    # print para
    for j in js:
        cmds.setAttr("%s.radius" % j, para)
    print(u'格納済みの全jointの半径を編集中です。\n')


def setsJoints(*args):
    sels = cmds.ls(sl = True)  # print sels
    qSetJSSldValue = cmds.floatSliderGrp('setJointSizeSlider', q = True,
                                         v = True)  # print qSetJSSldValue;print type(qSetJSSldValue)
    for sel in sels:
        cmds.setAttr('%s.radius' % sel, qSetJSSldValue)

    return sels

if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
    ui()
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する

print(u'モジュール名:{}'.format(__name__))  # 実行したモジュール名を表示する
