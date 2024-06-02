# -*- coding: utf-8 -*-

u"""
yoCustomScriptEditor2StandAlone.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -1.0-
:Date: 2024/05/13

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PySide2 version: 5.15.2

概要(overview):
    CustomScriptEditor2 シングルトン版 を スタンドアロン で起動する モジュールです
詳細(details):
    PySide2 UI である CustomScriptEditor2.py モジュール
        を実装するための、
            CustomScriptEditor2SPIModule.py を
                モジュール として読み込み、単独起動を想定した、
                    新規 モジュールです
注意(note):
    ・ 他に必須な独自モジュール
        ::

            # ローカルで作成したモジュール ######################################################
            from .TemplateForPySide2.CustomScriptEditor2SPIModule import custom_scriptEditor2_instance

-リマインダ-
    done: 2024/05/13
        新規作成

        version = '-1.0-'
"""
# 標準ライブラリ #################################################################
from importlib import import_module, reload
import pkgutil

# サードパーティライブラリ #########################################################
from PySide2.QtCore import Slot

# ローカルで作成したモジュール ######################################################
if 'custom_scriptEditor2_instance' not in globals():
    from .TemplateForPySide2.CustomScriptEditor2SPIModule import custom_scriptEditor2_instance



class CSE2StandAlonePyside2(object):
    def __init__(self):
        """Initialize data attributes. Constructor for  class."""
        # 追加7 ########################################################### start
        self.scriptEditor2_chunk1()
        self.scriptEditor2_chunk2()
        # 追加7 ########################################################### end

    # 追加7 ########################################################### start
    # ここで、CustomScriptEditor2 の closedシグナル を購読しています
    def scriptEditor2_chunk1(self):
        # note): custom_scriptEditor2_instance 本モジュール基で、
        #   CustomScriptEditor2(title, infoDetail)
        #   引数: title, 引数: infoDetail
        #   を定義しています
        self.scriptEditor2 = custom_scriptEditor2_instance

        # イレギュラー
        # ここで、CustomScriptEditor2 の closedシグナル を購読しません
        self.scriptEditor2.closed.connect(self.on_scriptEditor2_closed)
        # カスタムで、専用の スクリプトエディタ を初期化
        # self.scriptEditor2 = None
        self.statusCurrent_scriptEditor2 = 'open'

    def scriptEditor2_chunk2(self):
        # print('--------- ' + f'{self.__class__}' + ' ---------')
        print('outPut 専用 scriptEditor2 ウィジェット を 単独 で作成します')
        self.create_scriptEditor2_and_show()
        # print(self.scriptEditor2)
        # print('--------- ' + f'{self.__class__}' + ' ---------' * 3 + 'end\n')

    def create_scriptEditor2_and_show(self):
        # CustomScriptEditor2 ﾓｼﾞｭｰﾙ先では、あえて、show() せず、ここで show() しています。
        self.scriptEditor2.show()  # note): これは必須です。
        self.statusCurrent_scriptEditor2 = 'open'

    # イレギュラー
    # CustomScriptEditor2 クラスの closedシグナル が発行されると 当メソッド が呼び出されません
    # @Slot()
    def on_scriptEditor2_closed(self):
        # commonMessage = "Script editor was hided. Not closed !!"
        # message_warning(commonMessage + f'{self.__class__}')

        self.statusCurrent_scriptEditor2 = 'closed'
        # # QTextEdit の内容を保存
        # self.script_editor_content = self.scriptEditor2.text_edit.toPlainText()
        # print(self.script_editor_content)
        return self.statusCurrent_scriptEditor2
    # 追加7 ########################################################### end


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
    CSE2StandAlonePyside2()  # ui
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
