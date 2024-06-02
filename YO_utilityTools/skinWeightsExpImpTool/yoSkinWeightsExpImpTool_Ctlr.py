# -*- coding: utf-8 -*-

u"""
yoSkinWeightsExpImpTool_Ctrl.py

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

# サードパーティライブラリ #########################################################

# ローカルで作成したモジュール ######################################################
# 汎用ライブラリー の使用 #################################################### start
from ..lib.commonCheckSkinCluster import commonCheckSkinCluster
from ..lib.message import message
from ..lib.message_warning import message_warning
# 汎用ライブラリー の使用 #################################################### end
# mvc_model_module_that_become_derived_basis(派生基となるMVCモデルモジュール)
from ..TemplateForPySide2.type1.templateForPySide2_type1_Ctlr import Tpl4PySide2_Type1_Ctlr


class SkinWeightExpImp_Ctlr(Tpl4PySide2_Type1_Ctlr):
    u""" < View と Model をつなぐ Controllerクラス です >

    ::

      UIとモデルを結びつけるためのメソッドを実装します。

      Viewクラス と Modelクラス への参照を受け取り、
        View からのユーザーアクションを処理し、
            Model からのデータ変更を View に反映させるロジックを実装します。
    """
    def __init__(self, _view, _model):
        super(SkinWeightExpImp_Ctlr, self).__init__(_view, _model)

    # 他の def は、base Tpl4PySide2_Type1_Ctlr から全て再利用しています。

    # 新規
    def execute_getSkinCluster(self, message_text: str, caseIndex_: str):
        message(message_text + ': <' + caseIndex_ + '>')
        name_SC = commonCheckSkinCluster()
        self.view.exp_fileNameTxtFld_upDate(name_SC)

    # 新規
    def executeBtn_export(self, message_text: str, caseIndex_: str,
                          directory: str, scName: str
                          ):
        message(message_text + ': <' + caseIndex_ + '>')
        isFileExist_bool = self.model.isFileExist_check(caseIndex_, directory, scName)
        if isFileExist_bool:
            isContinue_bool = self.view.exp_isFileExist_popUp_ui(caseIndex_, directory, scName)
            if not isContinue_bool:
                message_warning('上書き Export は、一旦キャンセルされました。')
            else:
                message_warning('上書き Export は、そのまま継続で実行されています。続けます。ご注意ください。')
                self.model.ui_executeBtnCmd_exp(caseIndex_, directory, scName)
        else:
            self.model.ui_executeBtnCmd_exp(caseIndex_, directory, scName)

    # 新規
    def executeBtn_import(self, message_text: str, caseIndex_: str,
                          directory: str, fileName: str
                          ):
        message(message_text + ': <' + caseIndex_ + '>')
        self.model.ui_executeBtnCmd_imp(caseIndex_, directory, fileName)


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
