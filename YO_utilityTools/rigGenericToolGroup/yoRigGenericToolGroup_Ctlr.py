# -*- coding: utf-8 -*-

u"""
yoRigGenericToolGroup_Ctrl.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -5.5-
:Date: 2024/05/17

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PySide2 version: 5.15.2

-リマインダ-
    done: 2024/05/17
        - 追加6 と 変更6 と 新規6
            - 概要: ***_View モジュール の tabB の
                IHIツールの Hide, Show の呼び出し の改善
                に伴う、
                当 ***_Ctrl モジュール への関連を 追加 と 変更
            - 詳細:
                ::

                    +   # 全タブ 用
                        # 各ツールのUI起動の呼び出し 関数 をコントロールする 関数
                        def toolUIBootBtn(self, message_text: str, caseIndex_: str, *args):
                            ...
                            docstring help への追記 のみ
                            ...

                    +   # 変更6 ############################################################### start
                        # 未使用にしたので、以下は一旦キャンセルにしました。
                        # # 追加4
                        # # タブB 用 (group2)
                        # # IHIツールの Hide, Show の呼び出し 関数 をコントロールする 関数
                        # def ui_buttonRightClick_command(self,
                        #                                 message_text: str,
                        #                                 caseIndexOption_: str
                        #                                 ):
                        #     ...
                        # # 変更6 ############################################################### end
        version = '-5.5-'

    done: 2024/05/08
        追加と変更と新規5
            - 概要: ***_View モジュール へ 新規tabF の 追加に伴う、
                当 ***_Ctrl モジュール への関連を 追加
            - 詳細:
                ::

                    +   # 全タブ 用
                        # 各ツールのUI起動の呼び出し 関数 をコントロールする 関数
                        def toolUIBootBtn(self, message_text: str, caseIndex_: str, *args):
                            ...
                            docstring help への追記 のみ
                            ...
        version = '-5.1-'

    done: 2024/05/01
        追加4
            - 概要: ***_View モジュール の tabB へ
                IHIツールの Hide, Show の呼び出し 追加
                に伴う、当 ***_Ctrl モジュール への関連を 追加
            - 詳細:
                ::

                    +   # 追加4
                        # タブB 用 (group2)
                        # IHIツールの Hide, Show の呼び出し 関数 をコントロールする 関数
                        def ui_buttonRightClick_command(self,
                                                        message_text: str,
                                                        caseIndexOption_: str
                                                        ):
                            ...
        version = '-5.0-'

    done: 2024/04/11~2024/04/17
        追加3
            - 概要: ***_View モジュール の tabA,D の 各ツールの
                Help の呼び出し 追加
                コマンド実行する記述例 の呼び出し 追加
                に伴う、
                当 ***_Ctrl モジュール への関連を 追加
            - 詳細:
                ::

                    +   # 追加3
                        # タブA,D 用
                        # 各ツールの Help起動の呼び出し 関数 をコントロールする 関数
                        def ui_buttonRightClick_help(self, message_text: str, caseIndex_: str):
                            ...

                    +   # 追加3
                        # タブA,D 用
                        # 各ツールの UI起動せずにコマンド実行する記述例の呼び出し 関数 をコントロールする 関数
                        def ui_buttonRightClick_commandExample(self,
                                                               message_text: str,
                                                               caseIndex_: str
                                                               ):
                                                               ...
        version = '-4.0-'

    done: 2024/04/11
        追加2
            - 概要: ***_View モジュール の tabB へ YO_constraintToGeometry2 UI の呼び出し 追加
                に伴う、当 ***_Ctrl モジュール への関連を 追記
            - 詳細:
        version = '-3.1-'

    done: 2024/04/09
        追加1
            - 概要: tabE へ Node current view として reference の on/off 表示切り替え を追加
            - 詳細:
                ::

                    +   # Node: current view 表示 用
                        def ui_checkBox_nv(self
                                           , message_text: str
                                           , caseIndex_: str, cBxWid_: str
                                           , longName_: str , state_: int
                                           , *args
                                           ):
                                           ...

        version = '-3.0-'

    done: 2024/03/17~
        新規
        version = '-2.0-'

    done: 2024/01/26~2024/03/03
        新規
        version = '-1.0-'

"""

# 標準ライブラリ #################################################################

# サードパーティライブラリ #########################################################

# ローカルで作成したモジュール ######################################################
# 汎用ライブラリー の使用 #################################################### start
from ..lib.message import message
from ..lib.message_warning import message_warning
# 汎用ライブラリー の使用 #################################################### end
# mvc_model_module_that_become_derived_basis(派生基となるMVCモデルモジュール)
from ..TemplateForPySide2.type2.templateForPySide2_type2_Ctlr import Tpl4PySide2_Type2_Ctlr


class RigGenTlGp_Ctlr(Tpl4PySide2_Type2_Ctlr):
    u""" < View と Model をつなぐ Controllerクラス です >

    ::

      UIとモデルを結びつけるためのメソッドを実装します。

      Viewクラス と Modelクラス への参照を受け取り、
        View からのユーザーアクションを処理し、
            Model からのデータ変更を View に反映させるロジックを実装します。
    """
    def __init__(self, _view, _model):
        super(RigGenTlGp_Ctlr, self).__init__(_view, _model)

    # 他の def は、base Tpl4PySide2_Ctlr から全て再利用しています。

    # 全タブ 用
    # 各ツールのUI起動の呼び出し 関数 をコントロールする 関数
    def toolUIBootBtn(self, message_text: str, caseIndex_: str, *args):
        u""" < 全タブ 用 各ツールのUI起動の呼び出し 関数 をコントロールする 関数 >

        .. note:: 以下、対応の一覧
            ::

                switch_dict = {'caseA1': lambda: YO_renameTool5_main.main(),
                               'caseA2': lambda: YO_createSpaceNode3_main.main(),
                               'caseB1': lambda: YO_nodeCreateToWorldSpace.ui(),

                               # 追加2
                               'caseB2': lambda: YO_constraintToGeometry2.UI.showUI(),

                               # 追加6
                               'caseB3hide': lambda: isHistInter.hide(),
                               'caseB3show': lambda: isHistInter.show(),

                               'caseC1': lambda: YO_createClusterAndRename6_main.main(),
                               'caseC2': lambda: YO_createSpIkAndRename3_main.main(),
                               'caseD1': lambda: YO_pointConstraintByMatrix1_main.main(),
                               'caseD2': lambda: YO_orientConstraintByMatrix1_main.main(),
                               'caseD3': lambda: YO_scaleConstraintByMatrix1_main.main(),
                               'caseD4': lambda: YO_shearConstraintByMatrix1_main.main(),
                               'caseD5': lambda: YO_parentConstraintByMatrix5.UI.showUI(),
                               'caseD6': lambda: YO_parentConstraintByMatrix62.UI.showUI(),

                               # 追加と変更と新規5
                               'caseF1': lambda: yoSkinWeightsExpImpTool_main.main(),
                               }

        ######################

        :param str message_text: メッセージです
        :param str caseIndex_: RigGenTlGp_View で定義されている 各 caseIndex に相当します
        """
        message(message_text + ': <' + caseIndex_ + '>')
        self.model.call_eachToolUIBoot(caseIndex = caseIndex_)

    # 変更6 ############################################################### start
    # 未使用にしたので、以下は一旦キャンセルにしました。
    # # 追加4
    # # タブB 用 (group2)
    # # IHIツールの Hide, Show の呼び出し 関数 をコントロールする 関数
    # def ui_buttonRightClick_command(self,
    #                                 message_text: str,
    #                                 caseIndexOption_: str
    #                                 ):
    #     u""" < タブB 用 (group2) IHIツールの Hide, Show の呼び出し 関数 をコントロールする 関数 です >
    #
    #     .. note:: 以下、対応の一覧
    #         ::
    #
    #             switch_dict = {
    #                 'caseB3hide': lambda: isHistInter.hide(),
    #                 'caseB3show': lambda: isHistInter.show(),
    #                 }
    #
    #     ######################
    #
    #     :param str message_text:
    #     :param str caseIndexOption_:
    #     :rtype: None
    #     """
    #     message(message_text + ': <' + caseIndexOption_ + '>')
    #     # 各ツールの UI起動せずにコマンド実行する記述例の呼び出し 関数
    #     self.model.call_eachToolCommandBoot(caseIndexOption = caseIndexOption_)
    # 変更6 ############################################################### end

    # 追加3
    # タブA,D 用
    # 各ツールの Help起動の呼び出し 関数 をコントロールする 関数
    def ui_buttonRightClick_help(self, message_text: str, caseIndex_: str):
        u""" < タブA,D 用 各ツールの Help起動の呼び出し 関数 をコントロールする 関数 です >

        .. note:: 以下、対応の一覧
            ::

                switch_dict = {
                    # 追加3
                    'caseA1': lambda: help(renameToolConfig),
                    'caseA2': lambda: help(createSpaceNodeConfig),

                    # 'caseB1': lambda: YO_nodeCreateToWorldSpace.ui(),
                    #
                    # # 追加2
                    # 'caseB2': lambda: YO_constraintToGeometry2.UI.showUI(),
                    #
                    # 'caseC1': lambda: YO_createClusterAndRename6_main.main(),
                    # 'caseC2': lambda: YO_createSpIkAndRename3_main.main(),

                    # 追加3
                    'caseD1': lambda: help(pConByMatConfig),
                    'caseD2': lambda: help(oConByMatConfig),
                    'caseD3': lambda: help(scConByMatConfig),
                    'caseD4': lambda: help(shConByMatConfig),

                    # 'caseD5': lambda: YO_parentConstraintByMatrix5.UI.showUI(),
                    # 'caseD6': lambda: YO_parentConstraintByMatrix62.UI.showUI(),
                    # 'caseE1_3j': lambda: YO_jointDrawStyle_change.ui(),
                    # 'caseE1_4j': lambda: YO_jointRadiusSlider.ui(),
                    }

        ######################

        :param str message_text:
        :param str caseIndex_:
        :rtype: None
        """
        message(message_text + ': <' + caseIndex_ + '>')
        # 各ツールの Help起動の呼び出し 関数
        self.model.call_eachToolHelpBoot(caseIndex = caseIndex_)

    # 追加3
    # タブA,D 用
    # 各ツールの UI起動せずにコマンド実行する記述例 の呼び出し 関数 をコントロールする 関数
    def ui_buttonRightClick_commandExample(self,
                                           message_text: str,
                                           caseIndex_: str
                                           ):
        u""" < タブA,D 用 各ツールの UI起動せずにコマンド実行する記述例 の呼び出し 関数 をコントロールする 関数 です >

        .. note:: 以下、対応の一覧
            ::

                switch_dict = {
                    # 追加3
                    'caseA1': lambda: print(renameToolCommandExample),
                    'caseA2': lambda: print(createSpaceNodeCommandExample),

                    # 'caseB1': lambda: YO_nodeCreateToWorldSpace.ui(),
                    #
                    # # 追加2
                    # 'caseB2': lambda: YO_constraintToGeometry2.UI.showUI(),
                    #
                    # 'caseC1': lambda: YO_createClusterAndRename6_main.main(),
                    # 'caseC2': lambda: YO_createSpIkAndRename3_main.main(),

                    # 追加3
                    'caseD1': lambda: print(pConByMatCommandExample),
                    'caseD2': lambda: print(oConByMatCommandExample),
                    'caseD3': lambda: print(scConByMatCommandExample),
                    'caseD4': lambda: print(shConByMatCommandExample),

                    # 'caseD5': lambda: YO_parentConstraintByMatrix5.UI.showUI(),
                    # 'caseD6': lambda: YO_parentConstraintByMatrix62.UI.showUI(),
                    # 'caseE1_3j': lambda: YO_jointDrawStyle_change.ui(),
                    # 'caseE1_4j': lambda: YO_jointRadiusSlider.ui(),
                    }

        ######################

        :param str message_text:
        :param str caseIndex_:
        :rtype: None
        """
        message(message_text + ': <' + caseIndex_ + '>')
        # 各ツールの UI起動せずにコマンド実行する記述例の呼び出し 関数
        self.model.call_eachToolCommandExampleBoot(caseIndex = caseIndex_)

    # タブE 用
    # Joint: channel box 表示 用
    def ui_checkBox_j(self
                      , message_text: str
                      , caseIndex_: str, cBxWid_: str
                      , longName_: str , state_: int
                      , *args
                      ):
        u""" < Joint: channel box 表示 用 >

        currentState_: 'show' | 'hide' | None です

        ###############
        :param message_text:
        :param caseIndex_:
        :param cBxWid_:
        :param longName_:
        :param state_:
        :param args:
        """
        message(message_text + ': <' + caseIndex_ + '>')
        currentState_: str = self.model.call_checkBoxAction_j(caseIndex = caseIndex_
                                                              , cBxWid_name = cBxWid_
                                                              , longName = longName_
                                                              , state = state_
                                                              )
        if not currentState_:
            pass
        self.view.currentState_checkBox_j(currentState_, cBxWid_)

    # タブE 用
    # Node: channel box 表示 用
    def ui_checkBox_n(self
                      , message_text: str
                      , caseIndex_: str, cBxWid_: str
                      , longName_: str , state_: int
                      , *args
                      ):
        u""" < Node: channel box 表示 用 >

        currentState_: 'show' | 'hide' | None です

        ###############
        :param message_text:
        :param caseIndex_:
        :param cBxWid_:
        :param longName_:
        :param state_:
        :param args:
        """
        message(message_text + ': <' + caseIndex_ + '>')
        currentState_ = self.model.call_checkBoxAction_n(caseIndex = caseIndex_
                                                         , cBxWid_name = cBxWid_
                                                         , longName = longName_
                                                         , state = state_
                                                         )
        if not currentState_:
            pass
        self.view.currentState_checkBox_n(currentState_, cBxWid_)

    # タブE 用
    # Joint: current view 表示 用
    def ui_checkBox_jv(self
                       , message_text: str
                       , caseIndex_: str, cBxWid_: str
                       , longName_: str , state_: int
                       , *args
                       ):
        u""" < Joint: current view 表示 用 >

        currentState_: 'show' | 'hide' | None です

        ###############
        :param message_text:
        :param caseIndex_:
        :param cBxWid_:
        :param longName_:
        :param state_:
        :param args:
        """
        message(message_text + ': <' + caseIndex_ + '>')
        currentState_: str = self.model.call_checkBoxAction_jv(caseIndex = caseIndex_
                                                               , cBxWid_name = cBxWid_
                                                               , longName = longName_
                                                               , state = state_
                                                               )
        if not currentState_:
            pass
        self.view.currentState_checkBox_jv(currentState_, cBxWid_)

    # タブE 用
    # Node: current view 表示 用
    def ui_checkBox_nv(self
                       , message_text: str
                       , caseIndex_: str, cBxWid_: str
                       , longName_: str , state_: int
                       , *args
                       ):
        u""" < Node: current view 表示 用 >

        currentState_: 'normal' | 'reference' | None です

        ###############
        :param message_text:
        :param caseIndex_:
        :param cBxWid_:
        :param longName_:
        :param state_:
        :param args:
        """
        message(message_text + ': <' + caseIndex_ + '>')
        currentState_: str = self.model.call_checkBoxAction_nv(caseIndex = caseIndex_
                                                               , cBxWid_name = cBxWid_
                                                               , longName = longName_
                                                               , state = state_
                                                               )
        if not currentState_:
            pass
        self.view.currentState_checkBox_nv(currentState_, cBxWid_)

    # タブE 用
    # Mesh: current view 表示 用
    def ui_checkBox_mv(self
                       , message_text: str
                       , caseIndex_: str, cBxWid_: str
                       , longName_: str , state_: int
                       , *args
                       ):
        u""" < Mesh: current view 表示 用 >

        currentState_: 'on' | 'off' | None です

        ###############
        :param message_text:
        :param caseIndex_:
        :param cBxWid_:
        :param longName_:
        :param state_:
        :param args:
        """
        message(message_text + ': <' + caseIndex_ + '>')
        currentState_: str = self.model.call_checkBoxAction_mv(caseIndex = caseIndex_
                                                               , cBxWid_name = cBxWid_
                                                               , longName = longName_
                                                               , state = state_
                                                               )
        if not currentState_:
            pass
        self.view.currentState_checkBox_mv(currentState_, cBxWid_)

    # タブE 用
    # Curve: channel box 表示
    def ui_checkBox_c(self
                      , message_text: str
                      , caseIndex_: str, cBxWid_: str
                      , longName_: str , state_: int
                      , *args
                      ):
        u""" < Curve: channel box 表示 用 >

        currentState_: 'show' | 'hide' | None です

        ###############
        :param message_text:
        :param caseIndex_:
        :param cBxWid_:
        :param longName_:
        :param state_:
        :param args:
        """
        message(message_text + ': <' + caseIndex_ + '>')
        currentState_: str = self.model.call_checkBoxAction_c(caseIndex = caseIndex_
                                                              , cBxWid_name = cBxWid_
                                                              , longName = longName_
                                                              , state = state_
                                                              )
        if not currentState_:
            pass
        self.view.currentState_checkBox_c(currentState_, cBxWid_)


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
