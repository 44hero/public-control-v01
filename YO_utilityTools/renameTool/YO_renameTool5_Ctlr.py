# -*- coding: utf-8 -*-

u"""
YO_renameTool5_Ctlr.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -4.2-
:Date: 2023/12/21

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PyMel version: 1.2.0

-リマインダ-
    done: 2023/12/21
        - 変換箇所6
            - 概要: 絶対パス から 相対パス へ記述変更
            - 詳細:
                ::

                  -     from YO_utilityTools.lib.[...] import ...
                  +     from ..lib.[...] import ...

        version = '-4.2-'

    done: 2023//10/25
        汎用箇所を、モジュールとして読み込みに変更

        version = '-4.0-'

    done: 2023/09/08~2023/09/20
        python2系 -> python3系 変換
            - YO_renameTools5_main.py 変換記述あり
            - YO_renameTools5_Modl.py 変換記述あり
            詳細はそれ自身のリマインダに記述...

        version = '-3.0-'

    done: 2023/03/13~2022/04/10
        派生ファイル作成を考慮してコードの見直し

        version = '-2.0-'

    done: 2023/02/22~2022/02/23
        新規

        version = '-1.0-'
"""

# 標準ライブラリ
# import pprint

# サードパーティライブラリ

# ローカルで作成したモジュール
# 汎用ライブラリー の使用 ################################################################ start
from ..lib.message import message
# from ..lib.message_warning import message_warning
# 汎用ライブラリー の使用 ################################################################## end


class RT_Ctlr(object):
    u""" < View と Model をつなぐ Controllerクラス です >

    ::

      UIとモデルを結びつけるためのメソッドを実装します。

      Viewクラス と Modelクラス への参照を受け取り、
        View からのユーザーアクションを処理し、
            Model からのデータ変更を View に反映させるロジックを実装します。
    """
    def __init__(self, _view, _model):
        self.view = _view
        self.model = _model

        self.view.controller = self
        self.model.controller = self

        self.view.create()

    # # sample
    # def pushButton(self):
    #     # 複数の処理を行いたい際などに直接Modelに渡すのでなくControllerを挟むということが活きてくる
    #     self.model.sayHello()
    #     self.view.updateUI()

    def menuSave(self, message_text, *args):
        message(message_text)
        self.model.editMenuSaveSettingsCmd('Save Settings')  # Save Settings を実行

    def menuReload(self, message_text, *args):
        message(message_text)
        self.model.set_default_value_toOptionVar()  # optionVar の value を default に戻す操作
        self.view.editMenuReloadCmd()

    def menuClose(self, message_text, *args):  # Save Settingsと、UI close を両方実行
        message(message_text)
        self.model.editMenuSaveSettingsCmd('Close and Save Settings')  # Save Settings を実行
        self.view.editMenuCloseCmd()  # UI で閉じる

    def menuHelp(self, message_text, *args):
        message(message_text)
        self.view.helpMenuCmd(message_text)

    def executeBtn(self, message_text, *args):
        message(message_text)
        self.model.ui_executeBtnCmd()

    def restoreOptionVar(self, message_text, *args):
        # message(message_text)
        self.model.restoreOptionVarCmd(message_text)

    def currentMode(self, mode, *args):
        # message(mode)
        self.model.currentModeCmd(mode)

    def limitedTypingInput(self, cmnTxtFld, *args):
        # message(cmnTxtFld)
        self.model.limitedTypingInputCmd(cmnTxtFld)

    def textFieldPupMnu(self, cmnPUpMnu, textStr, *args):
        # message(cmnPUpMnu, textStr)
        self.model.textFieldPupMnuCmd(cmnPUpMnu, textStr)


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
