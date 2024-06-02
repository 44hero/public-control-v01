# -*- coding: utf-8 -*-

u"""
YO_uuID.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -1.0-
:Date: 2023/10/23

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PyMel version: 1.2.0

補足:
    個別ノードの持つ単独UUID番号、に対する独自操作を行います

-リマインダ-
    done: 2023/10/23
        新規

        version = '-1.0-'
"""

import maya.cmds as cmds


class UUID(object):
    def __init__(self):
        self.initSelectionNodeUUIDLists = []  # 格納用リスト宣言と初期化

    # 単独選択ノードから単独UUID番号をゲットする関数
    def get_ID_fromSel(self, sel):    # select one node :return: str
        u""" < 単独選択ノードから単独UUID番号をゲットする関数 です >

        ::

          # select one node :return: str

        #######################

        #.
            :param str sel: 単独選択ノード名

        #.
            :return : get_ID
                単独UUID番号
            :rtype: str

        #######################
        """
        get_ID = cmds.ls(sel, uuid = True)[0]  # 選択し終えたノードの 単独UUID番号 をゲット
        cmds.select(cl = True)
        return get_ID

    # 単独UUID番号から単独ノードを選択する関数
    def select_fromID(self, get_ID):  # 引数: str
        u""" < 単独UUID番号から単独ノードを選択する関数 です >

        ::

          # 引数: str

        #######################

        #.
            :param str get_ID: 単独UUID番号

        #######################
        """
        getNode = cmds.ls(get_ID)[0]  # 単独UUID番号 を参照して特定ノードの選択
        cmds.select(getNode, r = True)

    # 選択ノードの明示の為に準備する格納用
    # 独自の 選択ノードの明示に使用
    # 格納用
    def initSelectionNode_storeUUID(self, lists):  # select any nodes  :return: list[str]
        u""" < 選択ノードの明示の為に準備する格納用 関数 です >

        ::

          独自の 選択ノードの明示に使用
          格納用
          # select any nodes  :return: list[str

        #######################

        #.
            :param list[str] lists: list of select any nodes

        #.
            :return : initSelectionNodeUUIDLists: list of uuid
            :rtype: list[str]

        #######################
        """
        selectionLists = lists
        # uuidSelectionLists = []
        for index in selectionLists:
            self.initSelectionNodeUUIDLists.append(self.get_ID_fromSel(index))  # 選択ノードからIDを取得する
        cmds.select(cl = True)
        # self.initSelectionNodeUUIDLists = uuidSelectionLists
        return self.initSelectionNodeUUIDLists

    # 選択ノードの明示の為の再選択用
    # 独自の 選択ノードの明示に使用
    # 再選択用
    def initSelectionNode_reSelect(self, lists):  # set any uuid
        u""" < 選択ノードの明示の為の再選択用 関数 です >

        ::

          独自の 選択ノードの明示に使用
          再選択用
          # set any uuid

        #######################

        #.
            :param list[str] lists: set list of uuid

        #######################
        """
        uuidSelectionLists = lists
        # print(uuidSelectionLists)
        for index in uuidSelectionLists:
            getNode = cmds.ls(index)[0]  # 単独UUID番号 を参照して特定ノードの選択
            cmds.select(getNode, add = True)
            # print(getNode)


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
