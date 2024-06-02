# -*- coding: utf-8 -*-

u"""
commonCheckSkinCluster.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -1.0-
:Date: 2024/04/09

概要(overview):
    selection の skinCluster を取得する 関数
詳細(details):
    リターンは string
使用法(usage):
    from commonCheckSkinCluster import commonCheckSkinCluster
    e.g.:
        ノード1:sel
    commonCheckSkinCluster()
注意(note):
    ・ 他に必須な独自モジュール
        ::

            # サードパーティライブラリ #########################################################
            import maya.cmds as cmds

            # ローカルで作成したモジュール ######################################################
            from ..lib.commonCheckSelection import commonCheckSelection
            from ..lib.commonCheckShape import commonCheckShape
            from ..lib.message import message
            from ..lib.message_warning import message_warning

-リマインダ-
    done: 2024/04/09
        新規
        version = '-1.0-'
"""


# 標準ライブラリ #################################################################
import re

# サードパーティライブラリ #########################################################
import maya.cmds as cmds

# ローカルで作成したモジュール ######################################################
from ..lib.commonCheckSelection import commonCheckSelection
from ..lib.commonCheckShape import commonCheckShape
from ..lib.message import message
from ..lib.message_warning import message_warning


# selection の skinCluster を取得する 関数
def commonCheckSkinCluster(*args):
    u"""< selection の skinCluster を取得する 関数 >

    #######################

    #.
        :return: name_SC:
        :rtype name_SC: str

    #######################
    """
    SC = []
    name_SC = ''
    sels = commonCheckSelection()

    hasShapeList = [commonCheckShape(sel) for sel in sels]
    if not all(hasShapeList):
        message_warning(u'shape を持った geometry を選択して実行してください。')
        return name_SC

    if not sels or cmds.objectType(sels[0]) != u'transform':
        message_warning(u'skinning された geometry を選択して実行してください。')
        return name_SC
    elif len(sels) >= 2:
        pass
        message_warning(u'geometry を複数選択して実行してます。\n'
                        u'一つだけ選択して実行してください。')
    else:
        geoShape = cmds.listRelatives(sels[0], shapes = True)[0]
        gpIDs = cmds.listConnections(geoShape,
                                     s = True, d = False,
                                     type = 'groupId') or []

        if not gpIDs:  # material object assign type
            set = cmds.listConnections(geoShape,
                                       s = True, d = False,
                                       type = 'skinCluster') or []
            if set:
                SC.append(set[0])
        else:  # material face assign type
            gpPartsList = [cmds.listConnections(gpID,
                                                s = False, d = True,
                                                type = 'groupParts') or []
                           for gpID in gpIDs
                           ]
            cmds.select(*gpPartsList)
            gpPartsList = commonCheckSelection()
            cmds.select(gpPartsList)
            for obj in gpPartsList:
                set = cmds.listConnections(obj, type = 'skinCluster') or []
                if set:
                    SC.append(set[0])

        if not SC:
            message_warning(u'skinning された geometry を選択して実行してください。')
        else:
            name_SC = SC[0]
            print(u'\"{}\"'
                  u'\n\thave a'
                  u'\n\t\t\"{}\"'.format(geoShape, name_SC)
                  )
            # infs = cmds.skinCluster(SC, q = True, inf = True)
            # cmds.select(infs)
            # selNodes = cmds.ls(sl = True)
            # print('influences list are   \n')
            # print(selNodes)
            # # command 用 output print
            # print('\n' + '## result: command output ' + '##' * 20)
            # print('selNodes = {}'.format(selNodes))
            # print('cmds.select(selNodes, r = True)'.format(selNodes))
            # print('##' * 30)

            # self.expFileNameTxtFld_lEdtWid.setText(name_SC)

            cmds.select(sels, r = True)
    return name_SC

if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
