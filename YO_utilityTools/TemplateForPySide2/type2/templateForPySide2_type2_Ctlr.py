# -*- coding: utf-8 -*-

u"""
templateForPySide2_type2_Ctrl.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -1.0-
:Date: 2024/03/07

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PySide2 version: 5.15.2

-リマインダ-
    done: 2024/03/07
        新規

        version = '-1.0-'
"""

# 標準ライブラリ #################################################################
# import pprint

# サードパーティライブラリ #########################################################

# ローカルで作成したモジュール ######################################################
# 汎用ライブラリー の使用 #################################################### start
from ...lib.message import message
# 汎用ライブラリー の使用 #################################################### end


class Tpl4PySide2_Type2_Ctlr(object):
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

        self.view.createUI()
        # self.view.show()
        # print(self.view.parent())

    # # sample
    # def pushButton(self):
    #     # 複数の処理を行いたい際などに直接Modelに渡すのでなくControllerを挟むということが活きてくる
    #     self.model.sayHello()
    #     self.view.updateUI()

    def menuSave(self, message_text, *args):
        message(message_text)
        # self.model.editMenuSaveSettingsCmd(message_text)  # Save Settings を実行
        self.view.saveSettings()

    # def menuReload(self, message_text, *args):
    #     message(message_text)
    #     self.model.set_default_value_toOptionVar(message_text)  # optionVar の value を default に戻す操作
    #     # self.view.editMenuCloseCmd()
    #     self.view.editMenuReloadCmd(message_text)

    def restoreExecute(self, message_text):
        message(message_text)

    def menuReset(self, message_text):
        message(message_text)
        self.view.resetSettings()

    def menuClose(self, message_text):
        message(message_text)
        # self.model.editMenuSaveSettingsCmd(message_text)  # Save Settings を実行
        # self.view.editMenuCloseCmd(message_text)
        self.view.close()

    def menuHelp(self, message_text, *args):
        message(message_text)
        self.view.helpMenuCmd(message_text)

    def executeBtn(self, message_text, *args):
        message(message_text)
        self.model.ui_executeBtnCmd(message_text)

    def selfColorChangeExeBtn(self, index_, optBtn_pbtnWid_):
        self.view.uiOptBtn_changeColorCmd(index_, optBtn_pbtnWid_)


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
