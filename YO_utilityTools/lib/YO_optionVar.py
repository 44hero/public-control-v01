# -*- coding: utf-8 -*-

u"""
YO_optionVar.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -1.0-
:Date: 2023/03/01

補足:
    maya2018 PyMel 2.0.0~alpha0
        pm.optionVar に代わる
            maya cmds ベース記述 利用を目的としています

-リマインダ-
    done: 新規 2023/03/02
"""

import maya.cmds as cmds


# オプション変数を取得する関数
def getOptionVarCmd(name):
    u""" < オプション変数を取得する関数 >

    :param str name: dict の key に相当
    :return None or str or bool: dict の value に相当
    """
    # if cmds.optionVar(exists = name):
    #     return cmds.optionVar(q = name)
    # else:
    #     return None
    if cmds.optionVar(exists = name):  # 特定の name の存在の確認
        getValue = cmds.optionVar(q = name)  # 特定の name の value を get  # type: str
        # print('get value is type: \n\t' + str(type(getValue)))
        if getValue == 'False':  # type: str
            return False  # type: bool
        elif getValue == 'True':  # type: str
            return True  # type: bool
        else:
            return cmds.optionVar(q = name)  # そのまま出力  # type: str
    else:
        return None  # type: None


# オプション変数を設定する関数
def setOptionVarCmd(name, value):
    u""" < オプション変数を設定する関数 >

    :param str name: dict の key に相当
    :param str value: dict の value に相当
    """
    # cmds.optionVar(stringValue = [name, value])  # [str, str]

    # print(value)
    # print('set value is type: \n\t' + str(type(value)))
    if type(value) is float:
        # print('float exe')
        cmds.optionVar(floatValue = [name, value])  # [str, float]
    # elif type(value) is bool:
    #     print('bool exe to string')
    #     # print(value)
    #     if value is False:
    #         cmds.optionVar(stringValue = [name, 'False'])  # [str, int]
    #     elif value is True:
    #         cmds.optionVar(stringValue = [name, 'True'])  # [str, int]
    elif type(value) is bool:
        # print('int exe')
        cmds.optionVar(intValue = [name, value])  # [str, int]
    elif type(value) is int:
        # print('int exe')
        cmds.optionVar(intValue = [name, value])  # [str, int]
    else:
        # print('string exe')
        cmds.optionVar(stringValue = [name, value])  # [str, int]


# オプション変数をdict操作し、更新をかける関数
def upDateOptionVarsDictCmd():
    u""" < オプション変数をdict操作し、更新をかける関数 >

    :return dict optionVarsDict: dict(name, value) で構成された辞書の一連を作成
    """
    optionVarsList = cmds.optionVar(list = True)  # type: list
    optionVarsDict = {}
    for optionVarName in optionVarsList:
        optionVarValue = cmds.optionVar(q = optionVarName)
        optionVarsDict[optionVarName] = optionVarValue
    return optionVarsDict  # type: dict


# オプション変数に更新をかける関数
def upDateOptionVarCmd(name, value):
    cmds.optionVar(sv = [name, value])
    return


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
