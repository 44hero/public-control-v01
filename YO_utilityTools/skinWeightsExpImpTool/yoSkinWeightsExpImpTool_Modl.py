# -*- coding: utf-8 -*-

u"""
yoSkinWeightsExpImpTool_Modl.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -1.0-
:Date: 2024/04/25

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PySide2 version: 5.15.2

-リマインダ-
    done: 2024/04/21~2024/04/25
        新規
        version = '-1.0-'
"""

# 標準ライブラリ #################################################################
import os
from xml.etree import ElementTree

# サードパーティライブラリ #########################################################
import maya.cmds as cmds
import maya.OpenMaya as om
from maya import mel

# ローカルで作成したモジュール ######################################################
# 汎用ライブラリー の使用 ################################################################ start
from ..lib.message import message
from ..lib.message_warning import message_warning
# 汎用ライブラリー の使用 ################################################################## end


class SkinWeightExpImp_Modl(object):
    u""" < アプリケーションのデータモデルを表す Modelクラス です >

    ::

      データの取得や処理を行うためのメソッドを実装します。

      Modelクラスはアプリケーションの状態を表すデータフィールドを持ち、
        アプリケーションのロジックを実装するメソッドを提供します。

    ######

        構成要素は以下の9群
            - common コマンド群

            - コンストラクタのまとまり群

            - 1. UI-1. メニュー コマンド群
                一部ここ Model へ移動

            - 4. UI-4. OptionVar を利用したパラメータ管理 コマンド群

            - 2. UI-2. 追加オプション コマンド群

            - その他 アルゴリズムとなる コマンド群

            - 3. UI-3. common ボタン コマンド群

            - 5. スクリプトベースコマンド入力への対応

            - 「rename の核となる コマンド群」

                - 共通な一連の関数のまとまり

                - イレギュラー対応用

                - rename操作

    ######
    """
    def __init__(self):
        self.__constructor_chunk2()

    # コンストラクタのまとまり2 # タイトル等の定義
    def __constructor_chunk2(self):
        u""" < コンストラクタのまとまり2 # タイトル等の定義 です > """
        # self.title = TITLE
        # self.win = TITLE + '_ui'
        # self.space = SPACE
        # self.version = VERSION
        # self.underScore = '_'
        pass

    # その他 アルゴリズムとなる コマンド群 ################################################ start
    def getSkinClusterNode(self, target):
        history = cmds.listHistory(target, pruneDagObjects = True)
        skinNode = cmds.ls(history, type = "skinCluster") or None

        if skinNode != None:
            return skinNode[0]

        return None

    def getBindInfo(self, filePath):
        tree = ElementTree.parse(filePath)
        root = tree.getroot()
        skinBindDict = {}

        ##weights を見つける
        for e in root.findall('weights'):
            # それぞれのパラメーターを取得
            inf = e.get("source")
            shape = e.get("shape")
            deformer = e.get("deformer")

            if deformer in list(skinBindDict.keys()):
                if inf not in skinBindDict[deformer]["inf"]:
                    skinBindDict[deformer]["inf"].append(inf)
            else:
                skinBindDict[deformer] = {"inf": [inf], "shape": shape}
        return skinBindDict

    def importSkinWeight(self, filePath, fileName):
        skinBindDict = self.getBindInfo(filePath + '/'+ fileName)
        # print(skinBindDict)

        for deformerNode in list(skinBindDict.keys()):
            target = skinBindDict[deformerNode]["shape"]
            infs = skinBindDict[deformerNode]["inf"]

            # skinClusterの有無確認
            targetSkinNode = self.getSkinClusterNode(target)

            # print(f'targetSkinNode: {targetSkinNode}')
            # print(f'infs: {infs}')
            # print(f'target: {target}')

            isExistsLists = [cmds.objExists(inf) for inf in infs]
            not_exists = [inf for inf, exists in zip(infs, isExistsLists) if not exists]
            if not_exists:
                message_warning(f'{not_exists} が、当シーン内に 存在しません。'
                                'ご確認願います。'
                                'Import weight 作業はストップ致しました。')
            if all(isExistsLists):
                if targetSkinNode == None:
                    targetSkinNode = cmds.skinCluster(infs, target,
                                                      normalizeWeights = 1,
                                                      toSelectedBones = True,
                                                      name = deformerNode
                                                      )[0]
                    message_warning('skinning は、未だされていない事を確認しました。'
                                    'まず、skinning しました。')
                else:
                    # 現在のインフルエンスを取得して、addInfするための差分を取る
                    curInfs = cmds.skinCluster(targetSkinNode, q = True, inf = True)
                    addInfs = list(set(infs) - set(curInfs))

                    for inf in addInfs:
                        cmds.skinCluster(targetSkinNode, e = True, ai = inf,
                                         weight = 0
                                         )
                    message_warning('既に skinning されている事を確認しました。'
                                    'skinning は上書きされます。')
                cmds.deformerWeights(fileName, path = filePath,
                                     deformer = targetSkinNode, method = "index",
                                     im = True
                                     )
                cmds.skinCluster(targetSkinNode,e = True, forceNormalizeWeights = True)
                message(f'Import a skinCluster weight file ({fileName}) was successful !!')
    # その他 アルゴリズムとなる コマンド群 ################################################### end

    # 3. UI-3. common ボタン コマンド群 ################################################# start
    def isFileExist_check(self, caseIndex, directory, scName):
        file_name = f'{scName}.xml'
        file_path = os.path.join(directory, file_name)
        isFileExist_bool: bool = False
        if os.path.exists(file_path):
            message_warning(f'{file_name} は、所定の directory {directory} 既に存在します。')
            isFileExist_bool = True
        else:
            message(f'{file_name} は、所定の directory {directory} には存在しません。続けます。')
            isFileExist_bool = False
        return isFileExist_bool

    @staticmethod
    def default_case():
        print("Default case")

    # Export ツール による 書き出し 関数
    def ui_executeBtnCmd_exp(self, caseIndex, directory, scName):
        file_name = f'{scName}.xml'
        switch_dict = {'caseA1': lambda: cmds.deformerWeights(file_name,
                                                              export = True,
                                                              path = directory,
                                                              deformer = scName
                                                              ),
                       }
        func = switch_dict.get(caseIndex)
        if func is not None:
            func()
            message(f'Export a skinCluster weight file ({scName}.xml) was successful !!')
        else:
            self.default_case()


    # Import ツール による 呼び出し 関数
    def ui_executeBtnCmd_imp(self, caseIndex, directory, fileName):
        print(caseIndex)
        print(directory, fileName)
        switch_dict = {'caseA2': lambda: self.importSkinWeight(directory, fileName),
                       }
        func = switch_dict.get(caseIndex)
        if func is not None:
            func()
        else:
            self.default_case()
    # 3. UI-3. common ボタン コマンド群 ################################################### end


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
