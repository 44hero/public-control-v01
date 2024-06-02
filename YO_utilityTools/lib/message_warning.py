# -*- coding: utf-8 -*-

u"""
message_warning.py -1.0- 2021/05/26
author : oki yoshihiro  okiyoshihiro.job@gmail.com
概要(overview):
    ***
詳細(details):
    ***
使用法(usage):
    from message_warning import message_warning
    message_warning()
-リマインダ-
    ***
"""


import maya.OpenMaya as om


# warning message 関数
def message_warning(message_text = '', *args):
    u""" <warning message 関数 です。>
    :param message_text: str
    """
    print(u'# Result: {}'.format(message_text))
    om.MGlobal.displayWarning(message_text)

if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
    message_warning()
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
