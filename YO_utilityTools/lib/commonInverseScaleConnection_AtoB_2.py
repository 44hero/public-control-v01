# -*- coding: utf-8 -*-

u"""
commonInverseScaleConnection_AtoB_2.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -2.0-
:Date: 2023/05/25

概要(overview):
    選択ノード1 の scale attr から、 選択ノード2 の inverseScale attr へ接続します
詳細(details):
    選択ノード2つに対して実行する事を前提としたツールです。

    1番目選択には、
        nodeType が、transform もしくは、 joint
    が好ましく、
    2番目選択には、
        nodeType は、joint
    です。
    接続されているかのチェックを含め、接続が発動されます。

    以上の条件以外では、ジョブはストップし、warning が発せられます。

使用法(usage):
    ::

        # -*- coding: utf-8 -*-

        from imp import reload

        # UI立ち上げるには
        # import <パッケージ名>.<モジュール名>
        import YO_utilityTools.lib.commonInverseScaleConnection_AtoB_2
        reload(YO_utilityTools.lib.commonInverseScaleConnection_AtoB_2)
        # from <パッケージ名> import <モジュール名>
        from YO_utilityTools.lib.commonInverseScaleConnection_AtoB_2 import inverseScaleConnection_exe
        # <モジュール名>.<□□:機能名>()
        inverseScaleConnection_exe()

注意(note):
    ・ 他に必須な独自モジュール
        ::

            from ..lib.message import message
            from ..lib.message_warning import message_warning
            from ..lib.commonCheckSelection import commonCheckSelection  # :return: string

-リマインダ-
    done: 2023/05/25
        - 仕組みを新しくしました

        version = '-2.0-'
    done: 
        - 整理整頓 2021/09/26
        
        version = '-1.1-'
    done: 
        - 新規作成 2020/07/30
        
        version = '-1.0-'
"""

# 標準ライブラリ #################################################################

# サードパーティライブラリ #########################################################
import maya.cmds as cmds

# ローカルで作成したモジュール ######################################################
from ..lib.message import message
from ..lib.message_warning import message_warning
from ..lib.commonCheckSelection import commonCheckSelection  # :return: string

version = '-2.0-'
print('version is {}'.format(version))


def selection():
    sels = commonCheckSelection()
    sel1 = None
    sel2 = None
    if not sels:
        pass
    elif len(sels) >= 2:
        sel1, sel2 = sels[0], sels[1]  # index 2以降を切り捨てます
    elif len(sels) == 1:
        sel1 = sels[0]
    return sel1, sel2


# 選択ノード1 の scale attr から、 選択ノード2 の inverseScale attr へ接続する関数
def inverseScaleConnection_exe(*args):
    u""" < 選択ノード1 の scale attr から、 選択ノード2 の inverseScale attr へ接続する関数 です。 >
    """
    selList = selection()
    print(selList)
    isInNone = None in selList  # 1つでもNoneがあれば、Trueを返し、実行はストップされます。
    if isInNone:
        message_warning(u'実行はキャンセルしました。'
                        u'実行したいノードを2つ選択して実行してください。'
                        )
        pass
    else:
        isConnect = cmds.isConnected(u'{}.scale'.format(selList[0]), u'{}.inverseScale'.format(selList[1]))
        if not isConnect:
            message(u'scale attr -> inverseScale attr への、未接続箇所が見つかりました。'
                    u'続行中。。。')
            cmds.connectAttr(u'{}.scale'.format(selList[0]), u'{}.inverseScale'.format(selList[1])
                             , f = True
                             )
            message(u'{}.scale attr -> {}.inverseScale attr, 接続しました。'
                    .format(selList[0], selList[1])
                    )
        else:
            message_warning(u'既に、 {}.scale attr -> {}.inverseScale attr, 接続済です。接続ジョブは、キャンセルしました。'
                            .format(selList[0], selList[1])
                            )
            pass

if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
