# -*- coding: utf-8 -*-

u"""
YO_nodeCreateToWorldSpace.py -2.0- 2019/08/23
YO_nodeCreateToWorldSpace.py -1.0- 2017/07/04
author : oki yoshihiro  okiyoshihiro.job@gmail.com
補足 : maya作業画面上で、ユーザーの選択した箇所に対して、
locator・null・joint の何れかをワールド座標数値で配置します。
-リマインダ-
    done: 2024/03/17
        - python2系 -> python3系 check

        version = '-3.0-'
done:nodeType locator, object mode 時に、 新規作成されたlocatorの内、最後を選択したい 14:30 2019/08/23
"""

# 標準ライブラリ #################################################################
from functools import partial

# サードパーティライブラリ #########################################################
import maya.cmds as cmds
import maya.OpenMaya as om
import maya.mel as mel

space = ' '
version = '-3.0- <py 3.7.7 確認済, ui:cmds>'
title = 'nodeCreateToWorldSpace'
win = title + '_ui'

def ui():
    global win

    if cmds.window(win, exists = True):
        cmds.deleteUI(win)
    nctwsWin = cmds.window(win, menuBar = True, title = title + space + version,
                           iconName = 'Short Name', widthHeight = (286, 170), sizeable = True,
                           minimizeButton = False)

    cmds.menu(label = 'Edit', tearOff = False)
    cmds.menuItem(divider = True)
    cmds.menuItem(label = 'Reset Settings', c = partial(ui_Reload_exe))
    cmds.menuItem(label = 'Close This UI', c = partial(ui_CloseBttn_exe))
    cmds.menu(label = 'Help', helpMenu = True)

    cmds.rowColumnLayout('A', numberOfColumns = 1)

    cmds.text(label = version, h = 20, annotation = version)

    cmds.separator(w = 225, parent = 'A')
    cmds.setParent('..')

    # cFmLyout = cmds.formLayout('cFmLyout', numberOfDivisions = 100)

    # node type #
    a1 = cmds.columnLayout('cCmnLyout_nodeType')
    cmds.optionMenu('cOpMnu_nodeType', label = 'node type', w = 150, bgc = [0.5, 0.5, 0.5],
                    enableBackground = False)
    cmds.menuItem('cMuItm_loc', l = 'locator')
    cmds.menuItem('cMuItm_nul', l = 'null')
    cmds.menuItem('cMuItm_jot', l = 'joint')
    cmds.setParent('..')

    # mode #
    cRwLyout_mode = cmds.rowLayout('cRwLyout_mode',
                                   numberOfColumns = 2)  # cRwLyout_mode..start
    cmds.text(l = 'mode  ')
    # cRwCmnLyout_mode..start
    cRwCmnLyout_mode = cmds.rowColumnLayout('cRwCmnLyout_mode', numberOfColumns = 2,
                                            columnWidth = [(1, 80), (2, 105), (3, 80),
                                                           (4, 105)])
    cmds.radioCollection('cRoCllcton', parent = cRwCmnLyout_mode)
    cmds.radioButton('cRoBtn_1_eP', label = 'each points', select = True,
                     parent = cRwCmnLyout_mode)
    cmds.radioButton('cRoBtn_2_aP', label = 'average of points', parent = cRwCmnLyout_mode)
    cmds.radioButton('cRoBtn_3_eO', label = 'each objects', parent = cRwCmnLyout_mode)
    cmds.radioButton('cRoBtn_4_aO', label = 'average of objects', parent = cRwCmnLyout_mode)
    cmds.setParent('..')  # cRwCmnLyout_mode...end
    cmds.setParent('..')  # cRwLyout_mode..end

    cRwCmnLyout_spt = cmds.rowColumnLayout('cRwCmnLyout_spt', numberOfColumns = 1)
    cmds.separator(w = 225, parent = cRwCmnLyout_spt)
    cmds.setParent('..')

    b1 = cmds.rowLayout('cRwLyout_CreClse', numberOfColumns = 2, columnWidth2 = (112, 112),
                        columnAttach = ((1, 'both', 1), (2, 'both', 1)), height = 30)
    cBtn1_create = cmds.button('cBtn1_create', label = 'Create',
                               c = partial(ui_CreateBttn_exe))
    cBtn2_close = cmds.button('cBtn2_close', label = 'Close',
                              c = partial(ui_CloseBttn_exe))
    cmds.setParent('..')

    # #サイズ自動調整コード
    # cmds.formLayout('cFmLyout', edit = True,
    #                 attachForm = [
    #                     (a1, 'top', 5), (a1, 'left', 5)
    #                     , (b1, 'top', 20), (b1, 'left', 5)
    #                     , (b1, 'right', 5), (b1, 'bottom', 5)
    #                 ],
    #                 attachControl = [
    #                     (a1, 'bottom', 5, b1)
    #                 ],
    #                 attachPosition = [
    #                     (a1, 'right', 5, 100)
    #                     , (b1, 'right', 5, 100)
    #                 ]
    #                 )

    cmds.showWindow(win)

def ui_CreateBttn_exe(*args):
    nodeType_sel = cmds.optionMenu('cOpMnu_nodeType', q = True, sl = True)
    # print(nodeType_sel)# nodeType: 1:locator, 2:null, 3:joint
    mode_sel = cmds.radioCollection('cRoCllcton', q = True, sl = True)
    # print(mode_sel)
    # mode: cRoBtn_1_eP(each points), cRoBtn_2_aP(average of points),
    # cRoBtn_3_eO(each objects), cRoBtn_4_aO(average of objects)
    if nodeType_sel == 1:
        if mode_sel == 'cRoBtn_1_eP':
            exe(1, 1)
        elif mode_sel == 'cRoBtn_2_aP':
            exe(1, 2)
        elif mode_sel == 'cRoBtn_3_eO':
            exe(1, 3)
        elif mode_sel == 'cRoBtn_4_aO':
            exe(1, 4)
    elif nodeType_sel == 2:
        if mode_sel == 'cRoBtn_1_eP':
            exe(2, 1)
        elif mode_sel == 'cRoBtn_2_aP':
            exe(2, 2)
        elif mode_sel == 'cRoBtn_3_eO':
            exe(2, 3)
        elif mode_sel == 'cRoBtn_4_aO':
            exe(2, 4)
    elif nodeType_sel == 3:
        if mode_sel == 'cRoBtn_1_eP':
            exe(3, 1)
        elif mode_sel == 'cRoBtn_2_aP':
            exe(3, 2)
        elif mode_sel == 'cRoBtn_3_eO':
            exe(3, 3)
        elif mode_sel == 'cRoBtn_4_aO':
            exe(3, 4)

def ui_CloseBttn_exe(*args):
    global win
    cmds.deleteUI(win, window = True)

def ui_Reload_exe(*args):
    cmds.evalDeferred(lambda *args: ui())
    # ui()

def exe(nodeType = 1, mode = 1):
    # points mode
    def common_eachPoints_exe(nodeName, modeName):
        def eachPoints_nodeCreate(nodeName, pointPosList, pIndexRepl):
            nodes = []
            if nodeName == 'locator':
                node = cmds.createNode('transform',
                                       n = u'%s' % pIndexRepl + '_' + '%s' % nodeName)
                for i, p in enumerate(pointPosList):
                    cmds.setAttr('%s.t' % node + 'xyz'[i], p)
                    nodes.append(node)
                locShape = cmds.createNode('locator')
                locShapeParnt = cmds.listRelatives(p = True)
                cmds.parent(locShape, node, s = True, r = True)
                cmds.delete(locShapeParnt)
                for nIndex in nodes:
                    # print(nIndex)
                    getChild = cmds.listRelatives(nIndex, c = True)
                    # print(getChild[0])
                    cmds.rename(getChild[0], nIndex + u'Shape')
            elif nodeName == 'null':
                node = cmds.createNode('transform',
                                       n = u'%s' % pIndexRepl + '_' + '%s' % nodeName)
                for i, p in enumerate(pointPosList):
                    cmds.setAttr('%s.t' % node + 'xyz'[i], p)
            elif nodeName == 'joint':
                node = cmds.createNode('joint',
                                       n = u'%s' % pIndexRepl + '_' + '%s' % nodeName)
                for i, p in enumerate(pointPosList):
                    cmds.setAttr('%s.t' % node + 'xyz'[i], p)

        getPoints = cmds.ls(sl = True, fl = True)
        for pIndex in getPoints:
            pointPosList = cmds.pointPosition(pIndex)
            print(pIndex, pointPosList)
            index = pIndex.rfind('.')
            if not index == -1:
                pIndexRepl = pIndex.replace('.', '_')
                index = pIndexRepl.rfind('[')
                if not index == -1:
                    pIndexRepl = pIndexRepl.replace('[', '_')
                    index = pIndexRepl.rfind(']')
                    if not index == -1:
                        pIndexRepl = pIndexRepl.replace(']', '')
                        eachPoints_nodeCreate(nodeName, pointPosList, pIndexRepl)

    def common_averagePoints_exe(nodeName, modeName):
        def averagePoints_eachAxis(nodeName, modeName, axis):
            getPoints = cmds.ls(sl = True, fl = True)
            sum = 0.0
            axisPosition = []
            for pIndex in getPoints:
                pointPosList = cmds.pointPosition(pIndex)
                # print(pointPosList[axis])
                axisPosition.append(pointPosList[axis])  # print(pIndex, pointPos
            count = len(getPoints)
            # print(count)
            # print(axisPosition)
            for ap in axisPosition:
                sum += ap  # print(sum)
            # print('sum is %s' % sum)
            average = sum / count
            # print('average is %s' % average)
            # print(axis)
            # print('xyz'[axis])
            return average

        averageXYZ = []
        for i in range(3):
            average = averagePoints_eachAxis(nodeName, modeName, axis = i)
            averageXYZ.append(average)
        return averageXYZ

    def averagePoints_nodeCreate_and_pos(nodeName, averageXYZ):
        if nodeName == 'locator':
            node = cmds.spaceLocator(p = [0, 0, 0], n = u'%s' % nodeName)[0]
        elif nodeName == 'null':
            node = cmds.createNode('transform', n = u'%s' % nodeName)
        elif nodeName == 'joint':
            node = cmds.createNode('joint', n = u'%s' % nodeName)
        for e, average_axisValue in enumerate(averageXYZ):
            # print(e, average_axisValue)
            cmds.setAttr('%s.t' % node + 'xyz'[e], average_axisValue)
        return node

    def averagePoints_node_rename(getPoints, node, nodeName):
        pIndexReplLists = []
        for pIndex in getPoints:
            index = pIndex.rfind('.')
            if not index == -1:
                pIndexRepl = pIndex.replace('.', '_')
                index = pIndexRepl.rfind('[')
                if not index == -1:
                    pIndexRepl = pIndexRepl.replace('[', '_')
                    index = pIndexRepl.rfind(']')
                    if not index == -1:
                        pIndexRepl = pIndexRepl.replace(']', '')
                        pIndexReplLists.append(pIndexRepl)
        objNameSample = pIndexReplLists[0]  # 0番目から文字列抽出
        objNameSampleLists = objNameSample.split('_', 2)  # 2ケ目で文字列分割
        objName = objNameSampleLists[0] + '_' + objNameSampleLists[
            1] + '_average_' + nodeName
        cmds.rename(node, objName)

    # objects mode
    def common_eachObjects_exe(nodeName, modeName):
        def eachObjects_nodeCreate(nodeName, objPosList, objIndex):
            nodes = []
            if nodeName == 'locator':
                node = cmds.createNode('transform',
                                       n = u'%s' % objIndex + '_' + '%s' % nodeName)
                for i, p in enumerate(objPosList):
                    cmds.setAttr('%s.t' % node + 'xyz'[i], p)
                    nodes.append(node)
                # print(nodes)
                locShape = cmds.createNode('locator')
                locShapeParnt = cmds.listRelatives(p = True)
                cmds.parent(locShape, node, s = True, r = True)
                cmds.delete(locShapeParnt)
                for nIndex in nodes:
                    getChild = cmds.listRelatives(nIndex, c = True)
                    cmds.rename(getChild[0], nIndex + u'Shape')
                    newParentNode = cmds.listRelatives(nIndex + u'Shape', allParents = True)
                    return newParentNode[0]
            elif nodeName == 'null':
                node = cmds.createNode('transform',
                                       n = u'%s' % objIndex + '_' + '%s' % nodeName)
                for i, p in enumerate(objPosList):
                    cmds.setAttr('%s.t' % node + 'xyz'[i], p)
                return node
            elif nodeName == 'joint':
                node = cmds.createNode('joint',
                                       n = u'%s' % objIndex + '_' + '%s' % nodeName)
                for i, p in enumerate(objPosList):
                    cmds.setAttr('%s.t' % node + 'xyz'[i], p)
                return node
        getObjects = cmds.ls(sl = True)
        for objIndex in getObjects:
            objPosList = cmds.xform(objIndex, q = True, ws = True, t = True)
            # print(objIndex, objPosList)
            parentNode = eachObjects_nodeCreate(nodeName, objPosList, objIndex)
            cmds.select(parentNode, r = True)  # 最後を選択
        # print(getObjects)

    def common_averageObjects_exe(nodeName, modeName):
        def averageObjects_eachAxis(nodeName, modeName, axis):
            getObjects = cmds.ls(sl = True, fl = True)
            sum = 0.0
            axisPosition = []
            for objIndex in getObjects:
                objPosList = cmds.xform(objIndex, q = True, ws = True, t = True)
                # print(pointPosList[axis])
                axisPosition.append(objPosList[axis])  # print(pIndex, pointPosList)
            count = len(getObjects)
            # print(count)
            # print(axisPosition)
            for ap in axisPosition:
                sum += ap  # print(sum)
            # print('sum is %s' % sum)
            average = sum / count
            # print('average is %s' % average)
            # print(axis)
            # print('xyz'[axis])
            return average

        averageXYZ = []
        for i in range(3):
            average = averageObjects_eachAxis(nodeName, modeName, axis = i)
            averageXYZ.append(average)
        return averageXYZ

    def averageObjects_nodeCreate_and_pos(nodeName, averageXYZ):
        node = None
        if nodeName == 'locator':
            node = cmds.spaceLocator(p = [0, 0, 0], n = u'%s' % nodeName)[0]
        elif nodeName == 'null':
            node = cmds.createNode('transform', n = u'%s' % nodeName)
        elif nodeName == 'joint':
            node = cmds.createNode('joint', n = u'%s' % nodeName)
        for e, average_axisValue in enumerate(averageXYZ):
            # print(e, average_axisValue)
            cmds.setAttr('%s.t' % node + 'xyz'[e], average_axisValue)
        return node

    def averageObjects_node_rename(getObjects, node, nodeName):
        # print(getObjects, node, nodeName)
        objName = getObjects[0] + '_' + getObjects[-1] + '_average_' + nodeName
        cmds.rename(node, objName)

    ### main code
    if nodeType == 1:
        nodeName = 'locator'
        if mode == 1:
            modeName = 'each points'
            print(u'[nodeType]:{}, [mode]:{}'.format(nodeName, modeName))
            common_eachPoints_exe(nodeName, modeName)
        elif mode == 2:
            modeName = 'average of points'
            getPoints = cmds.ls(sl = True, fl = True)
            print(u'[nodeType]:{}, [mode]:{}'.format(nodeName, modeName))
            averageXYZ = common_averagePoints_exe(nodeName, modeName)
            node = averagePoints_nodeCreate_and_pos(nodeName, averageXYZ)
            averagePoints_node_rename(getPoints, node, nodeName)
        elif mode == 3:
            modeName = 'each objects'
            print(u'[nodeType]:{}, [mode]:{}'.format(nodeName, modeName))
            common_eachObjects_exe(nodeName, modeName)
        elif mode == 4:
            modeName = 'average of objects'
            getObjects = cmds.ls(sl = True)
            print(u'[nodeType]:{}, [mode]:{}'.format(nodeName, modeName))
            averageXYZ = common_averageObjects_exe(nodeName, modeName)
            node = averageObjects_nodeCreate_and_pos(nodeName, averageXYZ)
            averageObjects_node_rename(getObjects, node, nodeName)
    elif nodeType == 2:
        nodeName = 'null'
        if mode == 1:
            modeName = 'each points'
            print(u'[nodeType]:{}, [mode]:{}'.format(nodeName, modeName))
            common_eachPoints_exe(nodeName, modeName)
        elif mode == 2:
            modeName = 'average of points'
            getPoints = cmds.ls(sl = True, fl = True)
            print(u'[nodeType]:{}, [mode]:{}'.format(nodeName, modeName))
            averageXYZ = common_averagePoints_exe(nodeName, modeName)
            node = averagePoints_nodeCreate_and_pos(nodeName, averageXYZ)
            averagePoints_node_rename(getPoints, node, nodeName)
        elif mode == 3:
            modeName = 'each objects'
            print(u'[nodeType]:{}, [mode]:{}'.format(nodeName, modeName))
            common_eachObjects_exe(nodeName, modeName)
        elif mode == 4:
            modeName = 'average of objects'
            getObjects = cmds.ls(sl = True)
            print(u'[nodeType]:{}, [mode]:{}'.format(nodeName, modeName))
            averageXYZ = common_averageObjects_exe(nodeName, modeName)
            node = averageObjects_nodeCreate_and_pos(nodeName, averageXYZ)
            averageObjects_node_rename(getObjects, node, nodeName)
    elif nodeType == 3:
        nodeName = 'joint'
        if mode == 1:
            modeName = 'each points'
            print(u'[nodeType]:{}, [mode]:{}'.format(nodeName, modeName))
            common_eachPoints_exe(nodeName, modeName)
        elif mode == 2:
            modeName = 'average of points'
            getPoints = cmds.ls(sl = True, fl = True)
            print(u'[nodeType]:{}, [mode]:{}'.format(nodeName, modeName))
            averageXYZ = common_averagePoints_exe(nodeName, modeName)
            node = averagePoints_nodeCreate_and_pos(nodeName, averageXYZ)
            averagePoints_node_rename(getPoints, node, nodeName)
        elif mode == 3:
            modeName = 'each objects'
            print(u'[nodeType]:{}, [mode]:{}'.format(nodeName, modeName))
            common_eachObjects_exe(nodeName, modeName)
        elif mode == 4:
            modeName = 'average of objects'
            getObjects = cmds.ls(sl = True)
            print(u'[nodeType]:{}, [mode]:{}'.format(nodeName, modeName))
            averageXYZ = common_averageObjects_exe(nodeName, modeName)
            node = averageObjects_nodeCreate_and_pos(nodeName, averageXYZ)
            averageObjects_node_rename(getObjects, node, nodeName)


if __name__ == '__main__':
    print(u'YO_nodeCreateToWorldSpace.py: loaded as script file')
    ui()
else:
    print(u'YO_nodeCreateToWorldSpace.py: loaded as module file')

print(u'モジュール名：{}'.format(__name__))  # 実行したモジュール名を表示する
