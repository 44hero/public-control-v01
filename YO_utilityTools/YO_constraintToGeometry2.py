# -*- coding: utf-8 -*-

u"""
YO_constraintToGeometry2.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -5.0-
:Date: 2024/04/10

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PySide2 version: 5.15.2

概要(overview):
    1.ジオメトリ へ、2.別ノード(複数可) のコンストレインを実現するツールです。
詳細(details):
    便宜上 rivet と呼称しています。
    コンストレインのタイプには、
    ①surf rivet type
    ②mesh rivet type　
    ③follicle type
    と大別しています。
    <note> ③follicle type のみ、
        2.別ノード(複数)の初期の階層の親に、それぞれ 一つ space を作成し、
        follicle の子供にしている方法を取っています。
        その都合上、ユーザーの手動による、space の軸の変更を余儀なくしております。
        もっと言うと、事前にベクトルを決定しておくのが、他の type に比べ難儀だったためです。。
        具体的な、それぞれの space の、ユーザーによる軸の手動変更方法は以下です。
        最後に必ず作成される、仮のダミー dummySphereA を回転させる事で実現できるようにしています。
        仮のダミー dummySphereA の回転により、一遍に space の軸を決定できる手段をとっています。
        決定後は、その仮のダミー dummySphereA は必ず削除してください。
    <note>
        独自外部モジュール使用：YO_renameTool
            YO独自の命名規則の実行時
        独自外部モジュール使用：YO_createSpaceNode
            space ノード作成時
使用法(usage):
    ::

        import YO_constraintToGeometry2
        YO_constraintToGeometry2.UI.showUI()

-UIを立ち上げずにコマンドで実行する方法-
補足 : コンストレインのタイプ、実行したい対象、及び upベクトル、aimベクトル さえ明確ならば、
       UIを立ち上げずにコマンドで実行も出来ます。
       geo：ジオメトリ名(ex:'nurbsPlane1')
       nodes：実行したい対象オブジェクト名(ex:[u'planeA_jtA', u'planeA_jtB'])
       up：upベクトル(ex:[0.0, 0.0, 1.0])
       aim：aimベクトル(ex:[0.0, 1.0, 0.0])
       type：コンストレインのタイプ(ex:1)
usage: ex:
       longName:
       YO_constraintToGeometry2.UI().command(geo = u'nurbsPlane1', nodes = [u'planeA_jtA'], up = [0.0, 0.0, 1.0], aim = [0.0, 1.0, 0.0], type = 1)
       shortName:
       YO_constraintToGeometry2.UI().command(g = u'nurbsPlane1', ns = [u'planeA_jtA'], up = [0.0, 0.0, 1.0], am = [0.0, 1.0, 0.0], ty = 1)

-リマインダ-
    done: 2024/05/03
        - 追加と修正2
            - 概要: エラー回避を目的としています
            - 詳細: UI実行 か コマンド実行 かを明示し、scriptJob エラーを排除します。
                ::

                    +   # 追加と修正2
                        self.runInUiOrCommand = ''  # 'fromUI' or 'fromCmd'

                    +   def command(self, *args, **kwargs):
                            ...
                            # 追加と修正2
                            # print(self.runInUiOrCommand)
                            if self.runInUiOrCommand == 'fromUI':
                                self.runInUiOrCommand ='fromUI'
                            elif self.runInUiOrCommand == '':
                                self.runInUiOrCommand ='fromCmd'
                            print(f'check, Run in UI or Command: {self.runInUiOrCommand}')
                            ...

                    +   def commonResultPrintOut(self, geoNode, leftNodes, upV, amV, cnstTyp):
                            ...
                            # 追加と修正2
                            # print(f'check, Run in UI or Command: {self.runInUiOrCommand}')
                            if self.runInUiOrCommand == 'fromCmd':
                                pass
                            elif self.runInUiOrCommand == 'fromUI':
                                # 追加1
                                # エラー回避を終了し、script job を新規に復活させます
                                self.jobNum = cmds.scriptJob(event = ["SelectionChanged", self.ui_select_act_exe]
                                                             , parent = self.win
                                                             )
                                print(u'\n再び '
                                      'scriptJob : %s' % self.jobNum)
                            ...
        version = '-5.0-'

    done: 2024/04/10
        - 追加1
            - 概要: エラー回避を目的としています
            - 詳細: エラー出現の放置を、クリアーさせます。scriptJob が悪さをしている箇所あり
                ::

                    +   # 追加1
                        # 全て上手くいっているので、一旦 script job を切断し、エラー回避します
                        cmds.scriptJob(kill = self.jobNum, force = True)
                        print('kill scriptJob : %s' % self.jobNum)

                    +   # 追加1
                        # 実行終了後、即座に、leftNodes のみを選択
                        cmds.select(leftNodes, r = True)

                    +   # 追加1
                        # エラー回避を終了し、script job を新規に復活させます
                        self.jobNum = cmds.scriptJob(event = ["SelectionChanged", self.ui_select_act_exe], parent = self.win
                                                     )
                        print('scriptJob : %s' % self.jobNum)

        - 修正1
            - 概要: old style モジュール 使用を最新へ入れ替え
            - 詳細:
                ::

                    +   # ローカルで作成したモジュール ######################################################
                        # 修正1
                        # UI立ち上げずに、コマンドで実行用
                        from .renameTool.YO_renameTool5_Modl import RT_Modl
                        # UI立ち上げずに、コマンドで実行用
                        from .createSpaceNode.YO_createSpaceNode3_Modl import CSpaceNode_Modl

                    -   YO_renameTool
                    +   YO_renameTool5(renameTool package) へ変更

                    -   YO_createSpaceNode
                    +   YO_createSpaceNode3(createSpaceNode package) へ変更
        version = '-4.0-'

    done: 2024/03/17
        - python2系 -> python3系 check
            - py3へ変更
                - 概要: dict 関連
                - 詳細:
                    ::

                        -   ptnB_dict.items()
                        +   list(ptnB_dict.items())

                        -   ptnC_dict.items()
                        +   list(ptnC_dict.items())

                        -   kwargs.keys()
                        +   list(kwargs.keys())
        version = '-3.0-'

    done: 前回からの記述の継続着手 2019/10/25 - 2019/11/07
        version = '-1.0-'
"""

# 標準ライブラリ #################################################################
import re
import sys
from functools import partial
from importlib import reload

# サードパーティライブラリ #########################################################
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om

# ローカルで作成したモジュール ######################################################
# # パッケージ内のモジュールの更新を都度反映するように記述 ####################### start
# import YO_utilityTools.renameTool  # renameTool パッケージに対して
# for key in YO_utilityTools.renameTool.__dict__:
#     if not key.startswith('__'):
#         reload(YO_utilityTools.renameTool.__dict__[key])
# # パッケージ内のモジュールの更新を都度反映するように記述 ####################### end
from .renameTool.YO_renameTool5_Modl import RT_Modl
# UI立ち上げずに、コマンドで実行用
from .createSpaceNode.YO_createSpaceNode3_Modl import CSpaceNode_Modl


class UI(object):
    @classmethod
    def showUI(cls):
        u"""A function to instantiate the YO constraint To Geometry2 UI window
        :return win:
        :rtype win: string
        """
        win = cls()
        win.createUI()
        # print('koko')
        # print(win)
        return win

    # class Name を Output します
    def classNameOutput(self):
        u""" <class Name を Output します>
        :return self.__class__.__name__:
        :rtype self.__class__.__name__: string
        """
        return self.__class__.__name__

    def __init__(self):
        u"""Initialize data attributes"""
        self.space = ' '
        self.version = '-4.0- <py 3.7.7 確認済, ui:cmds>'
        self.title = 'YO_constraintToGeometry2'  # Long Name 1.0.0
        self.win = self.title + '_ui'
        self.iconName = 'Short Name 1.0.0'  # Short Name 1.0.0

        self.widthHeight = (200, 55)
        self.bgc = [0.4, 0.4, 0.4]
        self.bgcRed = [0.7, 0.5, 0.5]
        self.bgcBlue = [0.5, 0.5, 0.9]
        self.bgcBlue2 = [0.0, 0.7, 1.0]  # list of float
        self.bgcDarkBlue = [0.2, 0.2, 0.4]
        self.bgcWhite = [0.9, 0.9, 0.9]
        self.bgcPureWhite = [1.0, 1.0, 1.0]
        self.bgcDarkGray = [0.2, 0.2, 0.2]
        self.bgcBlack = [0.0, 0.0, 0.0]
        self.geoNode = ''
        self.geoNodeType = 'nurbsSurface'
        self.geoNodeShape = ''
        self.leftNodes = []
        self.leftNodesSpace = []
        self.outputRotAngle = []
        self.nodeAll = []
        self.upV = [0, 0, 1]
        self.amV = [0, 1, 0]
        self.cnstTyp = 1
        self.selectedToF = False  # scriptJob に利用。あくまでもUIありきの時に利用します。
        self.selList = []  # scriptJob に利用。あくまでもUIありきの時に利用します。
        self.jobNum = 0  # scriptJob に利用。
        self.currentActionText = u'初めにジオメトリを選択後、拘束したいノードを選択し、実行。(複数選択可)'  # scriptJob に利用。

        # 追加と修正2
        self.runInUiOrCommand = ''  # 'fromUI' or 'fromCmd'

    def createUI(self):
        if cmds.window(self.win, exists = True):
            cmds.deleteUI(self.win)
        cmds.window(self.win, menuBar = True
                    , title = self.title[3:] + self.space + self.version
                    , iconName = self.iconName,
                    widthHeight = self.widthHeight)
        cmds.menu(label = 'Edit', tearOff = False)
        cmds.menuItem(label = 'Reset Settings', c = self.ui_Reload)
        cmds.menuItem(label = 'Close This UI', c = self.ui_Close)
        cmds.menu(label = 'Help', helpMenu = True)

        cmds.columnLayout(adjustableColumn = True)
        cmds.separator()
        cmds.setParent('..')

        cmds.columnLayout(adj = True)
        cmds.text(l = u'constraint To Geometry ツール')
        cmds.text(l = self.version)
        cmds.text(l = u'note:', bgc = self.bgcBlue
                  , annotation = u'1.ジオメトリ へ、2.別ノード(複数可) のコンストレインを実現するツールです。\n'
                                 u'便宜上 rivet と呼称しています。\n'
                                 u'コンストレインのタイプには、①surf rivet type ②mesh rivet type '
                                 u'③follicle typeと\n'
                                 u'大別しています。\n'
                                 u'note:  \n'
                                 u'\t③follicle type のみ、2.別ノード(複数)の初期の階層の親に、'
                                 u'それぞれ一つ space を作成し、\n'
                                 u'\tfollicle の子供にしている方法を取っています。'
                                 u'その都合上、ユーザーの手動による、space の軸の変更\n'
                                 u'\tを余儀なくしております。もっと言うと、事前にベクトルを決定し'
                                 u'ておくのが、他の type に比べ\n'
                                 u'\t難儀だったためです。。\n'
                                 u'\t具体的な、それぞれの space の、'
                                 u'ユーザーによる軸の手動変更方法は以下です。\n'
                                 u'\t最後に必ず作成される、仮のダミー dummySphereA を回転させる事'
                                 u'で実現できるようにしています。\n'
                                 u'\t仮のダミー dummySphereA の回転により、'
                                 u'一遍に space の軸を決定できる手段をとっています。\n'
                                 u'\t決定後は、その仮のダミー dummySphereA は必ず削除してください。'
                  )
        cmds.separator()
        # action message
        cmds.text('cmdTxt_currentAction', label = self.currentActionText, height = 20,
                  fn = 'obliqueLabelFont', bgc = self.bgc)
        cmds.setParent('..')

        cForm = cmds.formLayout('cForm', numberOfDivisions = 100)

        # main ###########################################################################
        main_cLayout = cmds.columnLayout('main_cLayout', adj = False)

        ################################################
        # type 選択ボタン フィールド まとまり # typ_cRwCmnLyut
        ################################################
        # typ_cRwCmnLyut..start
        typ_cRwCmnLyut = cmds.rowColumnLayout('typ_cRwCmnLyut', numberOfColumns = 4)
        cmds.text(l = 'constraint type ')
        typ_cRdioCollectA = cmds.radioCollection('typ_cRdioCollectA',
                                                 parent = typ_cRwCmnLyut)
        typ_cRdioBtnA = cmds.radioButton('typ_cRdioBtnA', label = u'Surface type<classic>',
                                         select = True, bgc = self.bgcBlue,
                                         cc = partial(self.ui_typeChangeBttn_exe, u'typ1_surf')
                                         )
        typ_cRdioBtnB = cmds.radioButton('typ_cRdioBtnB', label = u'Mesh type<classic>',
                                         bgc = self.bgcDarkBlue,
                                         cc = partial(self.ui_typeChangeBttn_exe, u'typ2_mesh')
                                         )
        typ_cRdioBtnC = cmds.radioButton('typ_cRdioBtnC', label = u'follicle type',
                                         bgc = self.bgcDarkBlue,
                                         cc = partial(self.ui_typeChangeBttn_exe, u'typ3_folc')
                                         )
        cmds.setParent('..')  # typ_cRwCmnLyut...end
        # type 選択ボタン フィールド まとまり　終わり ####

        cmds.separator(height = 3)

        ################################################
        # up vector, aim vector フィールド まとまり
        ################################################
        upVamV_cRwCmnLyut = cmds.rowColumnLayout('upVamV_cRwCmnLyut', numberOfColumns = 5
                                                 , columnOffset = ([1, 'left', 22], [2, 'right', 5]
                                                                   , [3, 'right', 5], [4, 'right', 5]
                                                                   )
                                                 )
        cmds.text(l = 'Up vector')
        cmds.intSliderGrp('upVx', field = True, label = 'x', minValue = -1, maxValue = 1,
                          fieldMinValue = -1, fieldMaxValue = 1, value = 1,
                          columnWidth = ([1, 10], [2, 20], [3, 50])
                          , bgc = self.bgcWhite,
                          changeCommand = partial(self.ui_changeUpV_intSlide, 'currentValue_upVx')
                          )
        cmds.intSliderGrp('upVy', field = True, label = 'y', minValue = -1, maxValue = 1,
                          fieldMinValue = -1, fieldMaxValue = 1, value = 0,
                          columnWidth = ([1, 10], [2, 20], [3, 50])
                          , bgc = self.bgc,
                          changeCommand = partial(self.ui_changeUpV_intSlide, 'currentValue_upVy')
                          )
        cmds.intSliderGrp('upVz', field = True, label = 'z', minValue = -1, maxValue = 1,
                          fieldMinValue = -1, fieldMaxValue = 1, value = 0,
                          columnWidth = ([1, 10], [2, 20], [3, 50])
                          , bgc = self.bgc
                          , changeCommand = partial(self.ui_changeUpV_intSlide, 'currentValue_upVz')
                          )
        cmds.button('upResetBttn', l = 'reset', w = 26
                    , bgc = self.bgcPureWhite
                    , c = self.ui_upV_values_reset
                    )
        # cmds.intSliderGrp('upVx', e = True, value = 0, bgc = self.bgc)
        # cmds.intSliderGrp('upVy', e = True, value = 0, bgc = self.bgc)
        # cmds.intSliderGrp('upVz', e = True, value = 1, bgc = self.bgcWhite)

        cmds.text(l = 'Aim vector ')
        cmds.intSliderGrp('amVx', field = True, label = 'x', minValue = -1, maxValue = 1,
                          fieldMinValue = -1, fieldMaxValue = 1, value = 0,
                          columnWidth = ([1, 10], [2, 20], [3, 50])
                          , bgc = self.bgc
                          , changeCommand = partial(self.ui_changeAmV_intSlide,
                                                  'currentValue_amVx'))
        cmds.intSliderGrp('amVy', field = True, label = 'y', minValue = -1, maxValue = 1,
                          fieldMinValue = -1, fieldMaxValue = 1, value = 1,
                          columnWidth = ([1, 10], [2, 20], [3, 50])
                          , bgc = self.bgcWhite
                          , changeCommand = partial(self.ui_changeAmV_intSlide,
                                                  'currentValue_amVy'))
        cmds.intSliderGrp('amVz', field = True, label = 'z', minValue = -1, maxValue = 1,
                          fieldMinValue = -1, fieldMaxValue = 1, value = 0,
                          columnWidth = ([1, 10], [2, 20], [3, 50])
                          , bgc = self.bgc
                          , changeCommand = partial(self.ui_changeAmV_intSlide,
                                                  'currentValue_amVz'))
        cmds.button('amResetBttn', l = 'reset', w = 26
                    , bgc = self.bgcPureWhite
                    , c = self.ui_amV_values_reset
                    )
        cmds.setParent('..')  # upVamV_cRwCmnLyut...end
        # up vector, aim vector フィールド まとまり　終わり ####

        cmds.setParent('..')  # main_cLayout
        # main　終わり ######################################################################

        # option ##############################################
        op_rCLayout = cmds.rowColumnLayout('op_rCLayout', numberOfColumns = 2,
                                           columnAlign = ([1, 'center'], [2, 'center']),
                                           columnSpacing = ([1, 120], [2, 20]))

        cmds.text(l = 'yedsvdsfvdfsrvdfsrvfdrvbdrfvbedsvs')
        cmds.text(label = 'Default')
        cmds.separator()
        cmds.text(label = 'None')
        cmds.separator()
        cmds.text(label = 'None')
        cmds.setParent('..')  # op_rCLayout
        # option　終わり ####################################################################

        cBtn1 = cmds.button('cBtn1', label = 'Execute'
                            , bgc = self.bgcBlue2
                            , c = self.execute
                            )
        cBtn2 = cmds.button('cBtn2', label = 'Close', c = self.ui_Close)
        cBtn3 = cmds.button('cBt3', label = 'Break Connection and Bake', enable = True
                            , annotation = 'Break Connections and Bake From selects nodes'
                            , bgc = self.bgcRed
                            , c = self.brkCommand
                            )
        cmds.formLayout(cForm, e = True
                        , attachForm = ([main_cLayout, 'left', 5], [main_cLayout, 'right', 5]
                                        , [main_cLayout, 'top', 5]
                                        , [op_rCLayout, 'left', 5], [op_rCLayout, 'right', 5]
                                        , [op_rCLayout, 'top', 75]
                                        , [cBtn1, 'left', 5], [cBtn1, 'bottom', 5]
                                        , [cBtn2, 'bottom', 5], [cBtn3, 'right', 5]
                                        , [cBtn3, 'bottom', 5]
                                        )
                        , attachPosition = ([cBtn1, 'right', 0, 33], [cBtn3, 'left', 0, 67])
                        , attachControl = ([cBtn2, 'left', 4, cBtn1], [cBtn2, 'right', 4, cBtn3])
                        , attachNone = ([main_cLayout, 'top'], [cBtn1, 'top']
                                        , [cBtn2, 'top'], [cBtn3, 'top']
                                        )
                        )

        cmds.showWindow()

        self.jobNum = cmds.scriptJob(event = ["SelectionChanged", self.ui_select_act_exe]
                                     , parent = self.win
                                     )
        print('scriptJob : %s' % self.jobNum)
        return self.jobNum  # UI reload

    def ui_Reload(self, *args):
        cmds.evalDeferred(lambda *args: self.showUI())
        # self.showUI()

    def ui_Close(self, *args):
        u""" <UI close - 同時に scriptJob の kill も実行->
        """
        cmds.deleteUI(self.win, window = True)
        print('delete UI')
        cmds.scriptJob(kill = self.jobNum, force = True)
        print('kill scriptJob : %s' % self.jobNum)

    def ui_select_act_exe(self, *args):
        u""" <selection script job - action message 用の簡易文、作成関数 ->
        """
        selectedToF = cmds.isTrue('SomethingSelected')
        self.selectedToF = selectedToF
        # print('SomethingSelected : %s' % selectedToF)
        selList = self.commonCheckSelection()
        self.selList = selList
        print('Selected : %s' % selList)
        if selectedToF == 0:
            cmds.text('cmdTxt_currentAction', e = True, label = self.currentActionText,
                      bgc = self.bgc)
        else:
            self.geoNode = selList[0]
            self.leftNodes = selList[1:]
            print('koko')
            print(self.geoNode, self.leftNodes)
            # cmds.text('cmdTxt_currentAction', e = True, label = u'aho************')
            shape = cmds.listRelatives(selList[0], s = True)[0]
            print('shape is: {}'.format(shape))
            # print(cmds.objectType(shape))
            if not cmds.objectType(shape) == 'mesh':
                if not cmds.objectType(shape) == 'nurbsSurface':
                    cmds.text('cmdTxt_currentAction', e = True,
                              label = u'初めにジオメトリを選択してください。', bgc = self.bgcRed)
                    pass
            if cmds.objectType(shape) == 'mesh' or cmds.objectType(shape) == 'nurbsSurface':
                if cmds.objectType(shape) == 'mesh':
                    self.geoNodeType = 'mesh'
                elif cmds.objectType(shape) == 'nurbsSurface':
                    self.geoNodeType = 'nurbsSurface'
                cmds.text('cmdTxt_currentAction', e = True, label = u'二番目以降は拘束したいノードを'
                                                                    u'選択し、実行。(複数選択可)',
                          bgc = self.bgcBlue)
                if len(selList) > 1:
                    cmds.text('cmdTxt_currentAction', e = True, label = u'Ready...')

    def ui_typeChangeBttn_exe(self, *args):
        # print(args[0])
        if args[0] == u'typ1_surf':
            cmds.radioButton('typ_cRdioBtnA', e = True, bgc = self.bgcBlue)
            cmds.radioButton('typ_cRdioBtnB', e = True, bgc = self.bgcDarkBlue)
            cmds.radioButton('typ_cRdioBtnC', e = True, bgc = self.bgcDarkBlue)
        elif args[0] == u'typ2_mesh':
            cmds.radioButton('typ_cRdioBtnA', e = True, bgc = self.bgcDarkBlue)
            cmds.radioButton('typ_cRdioBtnB', e = True, bgc = self.bgcBlue)
            cmds.radioButton('typ_cRdioBtnC', e = True, bgc = self.bgcDarkBlue)
        elif args[0] == u'typ3_folc':
            cmds.radioButton('typ_cRdioBtnA', e = True, bgc = self.bgcDarkBlue)
            cmds.radioButton('typ_cRdioBtnB', e = True, bgc = self.bgcDarkBlue)
            cmds.radioButton('typ_cRdioBtnC', e = True, bgc = self.bgcBlue)

    def ui_changeUpV_intSlide(self, *args):
        # print(args)
        currentValue_upVx = cmds.intSliderGrp('upVx', q = True, value = True)
        currentValue_upVy = cmds.intSliderGrp('upVy', q = True, value = True)
        currentValue_upVz = cmds.intSliderGrp('upVz', q = True, value = True)
        if currentValue_upVx == 0:
            cmds.intSliderGrp('upVx', e = True, bgc = self.bgc)
        elif currentValue_upVx == -1:
            cmds.intSliderGrp('upVx', e = True, bgc = self.bgcDarkGray)
        else:
            cmds.intSliderGrp('upVx', e = True, bgc = self.bgcWhite)

        if currentValue_upVy == 0:
            cmds.intSliderGrp('upVy', e = True, bgc = self.bgc)
        elif currentValue_upVy == -1:
            cmds.intSliderGrp('upVy', e = True, bgc = self.bgcDarkGray)
        else:
            cmds.intSliderGrp('upVy', e = True, bgc = self.bgcWhite)

        if currentValue_upVz == 0:
            cmds.intSliderGrp('upVz', e = True, bgc = self.bgc)
        elif currentValue_upVz == -1:
            cmds.intSliderGrp('upVz', e = True, bgc = self.bgcDarkGray)
        else:
            cmds.intSliderGrp('upVz', e = True, bgc = self.bgcWhite)

    def ui_changeAmV_intSlide(self, *args):
        # print(args)
        currentValue_amVx = cmds.intSliderGrp('amVx', q = True, value = True)
        currentValue_amVy = cmds.intSliderGrp('amVy', q = True, value = True)
        currentValue_amVz = cmds.intSliderGrp('amVz', q = True, value = True)
        if currentValue_amVx == 0:
            cmds.intSliderGrp('amVx', e = True, bgc = self.bgc)
        elif currentValue_amVx == -1:
            cmds.intSliderGrp('amVx', e = True, bgc = self.bgcDarkGray)
        else:
            cmds.intSliderGrp('amVx', e = True, bgc = self.bgcWhite)

        if currentValue_amVy == 0:
            cmds.intSliderGrp('amVy', e = True, bgc = self.bgc)
        elif currentValue_amVy == -1:
            cmds.intSliderGrp('amVy', e = True, bgc = self.bgcDarkGray)
        else:
            cmds.intSliderGrp('amVy', e = True, bgc = self.bgcWhite)

        if currentValue_amVz == 0:
            cmds.intSliderGrp('amVz', e = True, bgc = self.bgc)
        elif currentValue_amVz == -1:
            cmds.intSliderGrp('amVz', e = True, bgc = self.bgcDarkGray)
        else:
            cmds.intSliderGrp('amVz', e = True, bgc = self.bgcWhite)

    def ui_upV_values_get(self, *args):
        currentValue_upVx = cmds.intSliderGrp('upVx', q = True, value = True)
        currentValue_upVy = cmds.intSliderGrp('upVy', q = True, value = True)
        currentValue_upVz = cmds.intSliderGrp('upVz', q = True, value = True)
        upV = [float(currentValue_upVx), float(currentValue_upVy), float(currentValue_upVz)]
        # print(upV)
        return 1, upV

    def ui_amV_values_get(self, *args):
        currentValue_amVx = cmds.intSliderGrp('amVx', q = True, value = True)
        currentValue_amVy = cmds.intSliderGrp('amVy', q = True, value = True)
        currentValue_amVz = cmds.intSliderGrp('amVz', q = True, value = True)
        amV = [float(currentValue_amVx), float(currentValue_amVy), float(currentValue_amVz)]
        # print(amV)
        return 1, amV

    def ui_upV_values_reset(self, *args):
        cmds.intSliderGrp('upVx', e = True, value = 1.0, bgc = self.bgcWhite)
        cmds.intSliderGrp('upVy', e = True, value = 0.0, bgc = self.bgc)
        cmds.intSliderGrp('upVz', e = True, value = 0.0, bgc = self.bgc)

    def ui_amV_values_reset(self, *args):
        cmds.intSliderGrp('amVx', e = True, value = 0.0, bgc = self.bgc)
        cmds.intSliderGrp('amVy', e = True, value = 1.0, bgc = self.bgcWhite)
        cmds.intSliderGrp('amVz', e = True, value = 0.0, bgc = self.bgc)

    ########################################################################################
    # name string determine exe ################### 命名規則のコントロール ##############start
    # under bar 3 or 2 version
    def nodeName_decomp_exeB(self, nodes):
        u""" <under bar 3 or 2 version>
        :param nodes:
        :type nodes: string
        :return strsCompLists:
        :rtype strsCompLists: list of string
        """
        patternB = re.compile(
            r'(?P<match1>.*)_(?P<match2>.*)_(?P<match3>.*)|(?P<match4>.*)_(?P<match5>.*)')
        iterator = patternB.finditer(nodes)
        for itr in iterator:
            # パターンヒットを辞書として出力
            ptnB_dict = itr.groupdict()
            # print(ptnB_dict)
            # py3へ変更
            for ptnBNumber_keys, ptnBFindStrs_values in list(ptnB_dict.items()):
                # print(ptnBNumber_keys, ptnBFindStrs_values)
                if ptnBFindStrs_values is None:
                    # value が None の keys のみを辞書から削除
                    ptnB_dict.pop(ptnBNumber_keys)
            # print(ptnB_dict)
            # 余計なものを省いた最終辞書を, ちゃんと綺麗にソートしたいが,
            # 辞書はソートできないので keys でソートする。するとタプルになってしまう。
            ptnB_tuple = sorted(ptnB_dict.items())
            # print(ptnB_tuple)
            strsCompLists = []
            for ptnB in ptnB_tuple:
                # タプルの各要素の内,欲しいのは index[1] なので,
                # 新規リストへ index[1] のみを順次格納する。
                # print(ptn[1])
                strsCompLists.append(ptnB[1])
            return strsCompLists

    # no under bar version
    def nodeName_decomp_exeC(self, nodes):
        u""" <no under bar version>
        :param nodes:
        :type nodes: string
        :return strsCompLists:
        :rtype strsCompLists: list of string
        """
        patternC = re.compile(r'(?P<match6>.*)')
        iterator = patternC.finditer(nodes)
        for itr in iterator:
            # パターンヒットを辞書として出力
            ptnC_dict = itr.groupdict()
            # print(ptnC_dict)
            # py3へ変更
            for ptnCNumber_keys, ptnCFindStrs_values in list(ptnC_dict.items()):
                # print(ptnCNumber_keys, ptnCFindStrs_values)
                if ptnCFindStrs_values is None:
                    # value が None の keys のみを辞書から削除
                    ptnC_dict.pop(ptnCNumber_keys)
            # print(ptnC_dict)
            # 余計なものを省いた最終辞書を, ちゃんと綺麗にソートしたいが,
            # 辞書はソートできないので keys でソートする。するとタプルになってしまう。
            ptnC_tuple = sorted(ptnC_dict.items())
            # print(ptnC_tuple)
            strsCompLists = []
            for ptnC in ptnC_tuple:
                # タプルの各要素の内,欲しいのは index[1] なので,
                # 新規リストへ index[1] のみを順次格納する。
                # print(ptn[1])
                strsCompLists.append(ptnC[1])
            return strsCompLists

    # strCompLists のカウント数に応じたネーミングの振り分け
    def strCompLists_count_caseDividing_exe(self, strsCompLists = None,
                                            utilNodeShortNameSet = '***'):
        u""" <strCompLists のカウント数に応じたネーミングの振り分け>
        :param strsCompLists:
        :type strsCompLists: list of string ['', '', '']
        :param utilNodeShortNameSet:
        :type utilNodeShortNameSet: list of string
        """
        if strsCompLists is None:
            strsCompLists = ['', '', '']
        print(f'strsCompLists: {strsCompLists}')
        print(f'utilNodeShortNameSet(start): {utilNodeShortNameSet}')
        if len(strsCompLists) == 3:
            utilNodeShortNameSet = utilNodeShortNameSet.title()  # 大文字整形
            print(f'utilNodeShortNameSet(change): {utilNodeShortNameSet}')
            utilNodeShortName = utilNodeShortNameSet.replace(' ', '')  # space削除
            print('3')
            # 修正1
            RT_Modl().exe(mode = 0
                          , n = [u'%s' % strsCompLists[0],
                                 u'%s%s@' % (
                                     strsCompLists[1], utilNodeShortName
                                     ),
                                 u'~', u'', u'%s' % strsCompLists[2]]
                          )
            # YO_renameTool.exe(typ = 0
            #                   , n = [u'%s' % strsCompLists[0],
            #                          u'%s%s@' % (
            #                              strsCompLists[1], utilNodeShortName
            #                              ),
            #                          u'~', u'', u'%s' % strsCompLists[2]]
            #                   )
        elif len(strsCompLists) == 2:
            # utilNodeShortNameSet = utilNodeShortNameSet.title()  # old: 大文字整形
            utilNodeShortName = utilNodeShortNameSet.replace(' ', '')  # space削除
            print(f'utilNodeShortName: {utilNodeShortName}')
            print('2')
            # 修正1
            RT_Modl().exe(mode = 0
                          # this is Python2系 old 記述Style
                          # , n = [u'%s' % strsCompLists[0],
                          #        u'%s%s@' % (
                          #            strsCompLists[1], utilNodeShortName
                          #            ),
                          #        u'~', u'', u''
                          #        ]
                          # this is Python3系 new 記述Style
                          , n = [f'{strsCompLists[0]}',
                                 f'{strsCompLists[1]}{utilNodeShortName}@',
                                 u'', u'', u''  # 修正2: old - > u'~', u'', u''
                                 ]
                          )
            # YO_renameTool.exe(typ = 0
            #                   , n = [u'%s' % strsCompLists[0],
            #                          u'%s%s@' % (
            #                              strsCompLists[1], utilNodeShortName
            #                              ),
            #                          u'~', u'', u''
            #                          ]
            #                   )
        elif len(strsCompLists) == 1:
            # 小文字整形(そのまま) + space削除のみ
            utilNodeShortName = utilNodeShortNameSet.replace(' ', '')
            print(f'utilNodeShortName: {utilNodeShortName}')
            print('1')
            # 修正1
            RT_Modl().exe(mode = 0
                          , n = [u'%s' % strsCompLists[0],
                                 u'%s@' % utilNodeShortName,
                                 u'~', u'', u''
                                 ]
                          )
            # YO_renameTool.exe(typ = 0
            #                   , n = [u'%s' % strsCompLists[0],
            #                          u'%s@' % utilNodeShortName,
            #                          u'~', u'', u''
            #                          ]
            #                   )
    # name string determine exe ################### 命名規則のコントロール ############### end
    ########################################################################################

    ########################################################################################
    # surfaceConstraintByRivet(sCnstByRvt) ######### surfaceConstraintByRivet ######## start
    # surfType rivet control
    def surfaceConstraintByRivet(self, *args):
        u""" <sCnstByRvt :control>
        """
        srf = self.geoNode
        leftNodes = self.leftNodes
        for leftIndex in leftNodes:
            cmds.select(srf, r = True)
            cmds.select(leftIndex, add = True)
            cmds.geometryConstraint(weight = True)
            cmds.select(leftIndex, r = True)
            geoCnst = cmds.listConnections(d = True, type = 'geometryConstraint')[0]
            cmds.delete(geoCnst)
        ########################
        # ① closestPointOnSurface を作成し、近接のuv point を取得する
        ########################
        srfSh = cmds.listRelatives(srf, s = True)[0]  # print(srfSh)
        uvLists = []  # uvListsの数と第二選択(leftNodes)：コンストレインしたいノード（複数可）の数は同じ！！
        for leftIndex in leftNodes:
            cPOS = cmds.createNode("closestPointOnSurface", n = '%s_cPOS' % leftIndex)
            cmds.connectAttr('%s.translate' % leftIndex, '%s.inPosition' % cPOS, f = True)
            cmds.connectAttr('%s.worldSpace' % srfSh, '%s.inputSurface' % cPOS, f = True)
            cPOSParaU = cmds.getAttr('%s.parameterU' % cPOS)
            cPOSParaV = cmds.getAttr('%s.parameterV' % cPOS)
            # print(cPOSParaU, cPOSParaV)
            uvIndex = "%s.uv[%f][%f]" % (srfSh, cPOSParaU, cPOSParaV)
            uvLists.append(uvIndex)
            cmds.delete(cPOS)  # uvIndex　を取得出来たので、closestPointOnSurface は削除！！
        # print(uvLists)
        ########################
        # ② 最終リベットの実行
        ########################
        for uvIndex, leftIndex in zip(uvLists, leftNodes):
            # print(uvIndex, leftIndex)
            self.surfType_rivet_toOneUVpoint(uvIndex, leftIndex)  # ② 最終リベットの実行

    # surfType rivet main アルゴリズム
    def surfType_rivet_toOneUVpoint(self, nameList = None, leftIndex = None):
        u""" <sCnstByRvt :main アルゴリズム>
        :param nameList:
        :type nameList: string
        :param leftIndex:
        :type leftIndex: string
        """
        # print(nameList, leftIndex)
        nameObject = nameList.split('.')[0]  # print(nameObject)
        uv = nameList.split('.uv')[1]  # print(uv)
        u = uv.split('[')[1]  # print(u)
        u = u.split(']')[0]  # print(u)
        v = uv.split('[')[2]  # print(v)
        v = v.split(']')[0]  # print(v)
        # print(u, v)

        # naming 解析
        strsCompLists = self.nodeName_decomp_exeB(leftIndex)  # under bar 3 or 2 version
        if strsCompLists is None:
            strsCompLists = self.nodeName_decomp_exeC(leftIndex)  # no under bar version
        print(u'%s naming 解析 ...' % leftIndex)
        print('\t%s' % strsCompLists)

        # pointOnSurfaceInfo1
        cmds.createNode('pointOnSurfaceInfo')  # rivetPointOnSurfaceInfo1
        utilNodeShortNameSet = 'pOn SfInfo' + 'Rvt'  # old): 'rvt POSInfo'
        self.strCompLists_count_caseDividing_exe(strsCompLists,
                                                 utilNodeShortNameSet)  # naming
        namePOSI = cmds.ls(sl = True)[0]
        cmds.setAttr('%s.turnOnPercentage' % namePOSI, 0)
        cmds.setAttr('%s.parameterU' % namePOSI, float(u))
        cmds.setAttr('%s.parameterV' % namePOSI, float(v))
        cmds.connectAttr('%s.worldSpace' % nameObject, '%s.inputSurface' % namePOSI)

        nameLocator = leftIndex
        # print(nameLocator)
        # nameLocator = cmds.createNode('transform', n = "rivet1")
        # cmds.createNode('locator', n = ("%sShape" % nameLocator), p = nameLocator)

        # aimConstraint1
        nameAC = cmds.createNode('aimConstraint', p = nameLocator)  # rivetAimConstraint1
        utilNodeShortNameSet = 'aim Const' + 'Rvt'  # old): 'rvt ACnst'
        self.strCompLists_count_caseDividing_exe(strsCompLists,
                                                 utilNodeShortNameSet)  # naming
        nameAC = cmds.ls(sl = True)[0]
        cmds.setAttr('%s.target[0].tw' % nameAC, 1)
        # print(self.upV, self.amV)
        upV = self.upV
        amV = self.amV
        cmds.setAttr('%s.upVector' % nameAC, upV[0], upV[1], upV[2], type = 'double3')
        cmds.setAttr('%s.aimVector' % nameAC, amV[0], amV[1], amV[2], type = 'double3')
        cmds.setAttr('%s.v' % nameAC, k = False)

        cmds.setAttr('%s.tx' % nameAC, k = False)
        cmds.setAttr('%s.ty' % nameAC, k = False)
        cmds.setAttr('%s.tz' % nameAC, k = False)
        cmds.setAttr('%s.rx' % nameAC, k = False)
        cmds.setAttr('%s.ry' % nameAC, k = False)
        cmds.setAttr('%s.rz' % nameAC, k = False)
        cmds.setAttr('%s.sx' % nameAC, k = False)
        cmds.setAttr('%s.sy' % nameAC, k = False)
        cmds.setAttr('%s.sz' % nameAC, k = False)

        cmds.connectAttr("%s.position" % namePOSI, "%s.translate" % nameLocator)
        cmds.connectAttr("%s.normal" % namePOSI, "%s.target[0].targetTranslate" % nameAC)
        cmds.connectAttr("%s.tangentV" % namePOSI, "%s.worldUpVector" % nameAC)
        cmds.connectAttr("%s.constraintRotateX" % nameAC, "%s.rx" % nameLocator)
        cmds.connectAttr("%s.constraintRotateY" % nameAC, "%s.ry" % nameLocator)
        cmds.connectAttr("%s.constraintRotateZ" % nameAC, "%s.rz" % nameLocator)

        # cmds.select(nameLocator, r = True)  # return nameLocator
    # surfaceConstraintByRivet(sCnstByRvt) ######### surfaceConstraintByRivet ########## end
    ########################################################################################

    ########################################################################################
    # meshConstraintByRivet(mCnstByRvt) ############### meshConstraintByRivet ######## start
    # meshType rivet control
    def meshConstraintByRivet(self, *args):
        u""" <mCnstByRvt :control>
        """
        msh = self.geoNode
        leftNodes = self.leftNodes
        for leftIndex in leftNodes:
            cmds.select(msh, r = True)
            cmds.select(leftIndex, add = True)
            cmds.geometryConstraint(weight = True)
            cmds.select(leftIndex, r = True)
            geoCnst = cmds.listConnections(d = True, type = 'geometryConstraint')[0]
            cmds.delete(geoCnst)
        ########################
        # ① closestPointOnMesh を作成し、近接のfaceIndexを取得する
        ########################
        mshSh = cmds.listRelatives(msh, s = True)[0]  # print(mshSh)
        faceLists = []  # faceListsの数と第二選択(leftNodes)：コンストレインしたいノード（複数可）の数は同じ！！

        for leftIndex in leftNodes:
            cPOM = cmds.createNode("closestPointOnMesh", n = '%s_cPOM' % leftIndex)
            cmds.connectAttr('%s.translate' % leftIndex, '%s.inPosition' % cPOM, f = True)
            cmds.connectAttr('%s.worldMesh' % mshSh, '%s.inMesh' % cPOM, f = True)
            cmds.connectAttr('%s.worldMatrix' % mshSh, '%s.inputMatrix' % cPOM, f = True)
            faceIndex = cmds.getAttr('%s.closestFaceIndex' % cPOM)
            # print(faceIndex)
            faceIndex = "%s.f[%i]" % (mshSh, faceIndex)
            faceLists.append(faceIndex)
            cmds.delete(cPOM)  # faceIndex　を取得出来たので、closestPointOnMesh は削除！！
        # print(faceLists)
        ########################
        # ② 1.face 選択から、2.エッジ 選択への変換
        #########################
        # と
        #########################
        # ③ 最終リベットの実行
        #########################
        for faceIndex, leftIndex in zip(faceLists, leftNodes):
            edgeLists = []
            cmds.select(faceIndex, r = True)
            components = cmds.ls(sl = True)
            # print(components)
            components = self.toVertex(components)
            # print(components)
            vGroup1 = components[0:2]
            # print(vGroup1)
            vGroup2 = components[2:]
            # print(vGroup2)
            components = self.toFlatten(components)
            # print(components)

            cmds.select(vGroup1, r = True)
            mel.eval('ConvertSelectionToContainedEdges')
            edge1 = cmds.ls(sl = True)[0]  # print(edge1)
            edgeLists.append(edge1)

            cmds.select(vGroup2, r = True)
            mel.eval('ConvertSelectionToContainedEdges')
            edge2 = cmds.ls(sl = True)[0]  # print(edge2)
            edgeLists.append(edge2)

            # print(faceIndex)
            # print('\t%s' % edgeLists)  # ② 1.face 選択から、2.エッジ 選択への変換
            self.meshType_rivet_toBetweenTwoEdges(edgeLists, leftIndex)  # ③ 最終リベットの実行

    # mesh コンポーネント変換関数 ################################ start
    # コンポーネントのIDが連続していてもまとめられないようにする関数
    def toFlatten(self, components):
        u""" <mCnstByRvt :コンポーネントのIDが連続していてもまとめられないようにする関数>
        :param components:
        :type components: string
        :return cmds.ls(components, fl = True, l = True):
        :rtype cmds.ls(components, fl = True, l = True): list of string
        """
        return cmds.ls(components, fl = True, l = True)

    # 頂点のリストに変換する関数
    def toVertex(self, components):
        u""" <mCnstByRvt :頂点のリストに変換する関数>
        :param components:
        :type components: string
        :return self.toFlatten(components):
        :rtype self.toFlatten(components): list of string
        """
        components = cmds.polyListComponentConversion(components, fv = 1, ff = 1, fe = 1,
                                                      fuv = 1, fvf = 1, tv = 1)
        return self.toFlatten(components)

    # エッジのリストに変換する関数
    def toEdge(self, components):
        u""" <mCnstByRvt :エッジのリストに変換する関数>
        :param components:
        :type components: string
        :return self.toFlatten(components):
        :rtype self.toFlatten(components): list of string
        """
        # components = cm
        components = cmds.polyListComponentConversion(components, fv = 1, ff = 1, fuv = 1,
                                                      fvf = 1, te = 1)
        return self.toFlatten(components)

    # すべてのコンポーネントが含まれたエッジに変換する関数
    def toContainedEdge(self, components):
        u""" <mCnstByRvt :すべてのコンポーネントが含まれたエッジに変換する関数>
        :param components:
        :type components: string
        :return self.toFlatten(components):
        :rtype self.toFlatten(components): list of string
        """
        components = cmds.polyListComponentConversion(components, fv = 1, ff = 1, fuv = 1,
                                                      fvf = 1, te = 1, internal = 1)
        return self.toFlatten(components)

    # フェイスに変換する関数
    def toFace(self, components):
        u""" <mCnstByRvt :フェイスに変換する関数>
        :param components:
        :type components: string
        :return self.toFlatten(components):
        :rtype self.toFlatten(components): list of string
        """
        components = cmds.polyListComponentConversion(components, fv = 1, fe = 1, fuv = 1,
                                                      fvf = 1, tf = 1)
        return self.toFlatten(components)
    # mesh コンポーネント変換関数 ################################ end

    # meshType main rivet アルゴリズム
    def meshType_rivet_toBetweenTwoEdges(self, nameList = None, leftIndex = None):
        u""" <mCnstByRvt :main アルゴリズム>
        :param nameList:
        :type nameList: string
        :param leftIndex:
        :type leftIndex: string
        """
        # print(nameList, leftIndex)
        nameObject = nameList[0].split('.')[0]  # print(nameObject)
        parts1 = nameList[0].split('.')[1]  # print(parts1)
        e1 = parts1.split('[')[1]  # print(e1)
        e1 = e1.split(']')[0]  # print(e1)
        parts2 = nameList[1].split('.')[1]  # print(parts2)
        e2 = parts2.split('[')[1]  # print(e2)
        e2 = e2.split(']')[0]  # print(e2)
        # print(e1, e2)

        # naming 解析
        strsCompLists = self.nodeName_decomp_exeB(leftIndex)  # under bar 3 or 2 version
        if strsCompLists is None:
            strsCompLists = self.nodeName_decomp_exeC(leftIndex)  # no under bar version
        print(u'%s naming 解析 ...' % leftIndex)
        print('\t%s' % strsCompLists)

        # curveFromMeshEdge 1
        cmds.createNode('curveFromMeshEdge')  # rivetCurveFromMeshEdge1
        utilNodeShortNameSet = 'rvt CFMEdge A'
        self.strCompLists_count_caseDividing_exe(strsCompLists,
                                                 utilNodeShortNameSet)  # naming
        nameCFME1 = cmds.ls(sl = True)[0]
        cmds.setAttr('%s.isHistoricallyInteresting' % nameCFME1, 1)
        cmds.setAttr('%s.edgeIndex[0]' % nameCFME1, int(e1))

        # curveFromMeshEdge 2
        cmds.createNode('curveFromMeshEdge')  # rivetCurveFromMeshEdge2
        utilNodeShortNameSet = 'rvt CFMEdge B'
        self.strCompLists_count_caseDividing_exe(strsCompLists,
                                                 utilNodeShortNameSet)  # naming
        nameCFME2 = cmds.ls(sl = True)[0]
        cmds.setAttr('%s.isHistoricallyInteresting' % nameCFME2, 1)
        cmds.setAttr('%s.edgeIndex[0]' % nameCFME2, int(e2))

        # rivetLoft1
        cmds.createNode('loft')  # rivetLoft1
        utilNodeShortNameSet = 'rvt Loft'
        self.strCompLists_count_caseDividing_exe(strsCompLists,
                                                 utilNodeShortNameSet)  # naming
        nameLoft = cmds.ls(sl = True)[0]
        cmds.setAttr('%s.inputCurve' % nameLoft, s = 2)
        cmds.setAttr('%s.uniform' % nameLoft, True)
        cmds.setAttr('%s.reverseSurfaceNormals' % nameLoft, True)

        # pointOnSurfaceInfo1
        cmds.createNode('pointOnSurfaceInfo')  # rivetPointOnSurfaceInfo1
        utilNodeShortNameSet = 'rvt POSInfo'
        self.strCompLists_count_caseDividing_exe(strsCompLists,
                                                 utilNodeShortNameSet)  # naming
        namePOSI = cmds.ls(sl = True)[0]
        cmds.setAttr('%s.turnOnPercentage' % namePOSI, 1)
        cmds.setAttr('%s.parameterU' % namePOSI, 0.5)
        cmds.setAttr('%s.parameterV' % namePOSI, 0.5)

        cmds.connectAttr("%s.outputSurface" % nameLoft, "%s.inputSurface" % namePOSI,
                         f = True)
        cmds.connectAttr("%s.outputCurve" % nameCFME1, "%s.inputCurve[0]" % nameLoft)
        cmds.connectAttr("%s.outputCurve" % nameCFME2, "%s.inputCurve[1]" % nameLoft)
        cmds.connectAttr("%s.worldMesh" % nameObject, "%s.inputMesh" % nameCFME1)
        cmds.connectAttr("%s.worldMesh" % nameObject, "%s.inputMesh" % nameCFME2)

        nameLocator = leftIndex
        # print(nameLocator)
        # nameLocator = cmds.createNode('transform', n = "rivet1")
        # cmds.createNode('locator', n = ("%sShape" % nameLocator), p = nameLocator)

        # aimConstraint1
        cmds.createNode('aimConstraint', p = nameLocator)
        utilNodeShortNameSet = 'rvt ACnst'  # rivetAimConstraint1
        self.strCompLists_count_caseDividing_exe(strsCompLists,
                                                 utilNodeShortNameSet)  # naming
        nameAC = cmds.ls(sl = True)[0]
        cmds.setAttr('%s.target[0].tw' % nameAC, 1)
        # print(self.upV, self.amV)
        upV = self.upV
        amV = self.amV
        cmds.setAttr('%s.aimVector' % nameAC, upV[0], upV[1], upV[2], type = 'double3')
        cmds.setAttr('%s.upVector' % nameAC, amV[0], amV[1], amV[2], type = 'double3')
        cmds.setAttr('%s.v' % nameAC, k = False)

        cmds.setAttr('%s.tx' % nameAC, k = False)
        cmds.setAttr('%s.ty' % nameAC, k = False)
        cmds.setAttr('%s.tz' % nameAC, k = False)
        cmds.setAttr('%s.rx' % nameAC, k = False)
        cmds.setAttr('%s.ry' % nameAC, k = False)
        cmds.setAttr('%s.rz' % nameAC, k = False)
        cmds.setAttr('%s.sx' % nameAC, k = False)
        cmds.setAttr('%s.sy' % nameAC, k = False)
        cmds.setAttr('%s.sz' % nameAC, k = False)

        cmds.connectAttr("%s.position" % namePOSI, "%s.translate" % nameLocator)
        cmds.connectAttr("%s.normal" % namePOSI, "%s.target[0].targetTranslate" % nameAC)
        cmds.connectAttr("%s.tangentV" % namePOSI, "%s.worldUpVector" % nameAC)
        cmds.connectAttr("%s.constraintRotateX" % nameAC, "%s.rx" % nameLocator)
        cmds.connectAttr("%s.constraintRotateY" % nameAC, "%s.ry" % nameLocator)
        cmds.connectAttr("%s.constraintRotateZ" % nameAC, "%s.rz" % nameLocator)

        # print('debug koko')
        # print (nameCFME1, nameCFME2, nameLoft, namePOSI, nameAC)
        # print (nameLocator)
        # cmds.select(nameLocator, r = True)  # return nameLocator
    # meshConstraintByRivet(mCnstByRvt) ############### meshConstraintByRivet ########## end
    ########################################################################################

    ########################################################################################
    # geoConstraintByFollicle(gCnstByFlcl) ############ geoConstraintByFollicle ###### start
    # follicle control
    def geoConstraintByFollicle(self, *args):
        u""" <gCnstByFlcl :control>
         """
        geo = self.geoNode
        leftNodes = self.leftNodes
        # print(geo, leftNodes)
        self.parentToSurface()
        cmds.select(leftNodes, r = True)  # leftNodes 其々の親に space を作成する
        # 修正1
        CSpaceNode_Modl().exe(mode = 1
                              , n = [u'~', u'~[Space]', u'~', u'', u'']
                              , nodeType = u'null'
                              )
        # YO_createSpaceNode.exe(typ = 1, nt = 'null',
        #                        n = [u'~', u'~[Space]', u'~', u'', u'']
        #                        )
        self.leftNodesSpace = cmds.ls(sl = True)
        leftNodesSpace = self.leftNodesSpace
        upV = self.upV
        amV = self.amV
        # print(upV, amV)
        dmyAglBtw = cmds.createNode('angleBetween', n = 'dummyAngleBetweenA')
        dmySphere = cmds.sphere(ch = False, n = 'dummySphereA')[0]

        mel.eval('ToggleLocalRotationAxes')

        cmds.connectAttr('%s.euler' % dmyAglBtw, '%s.rotate' % dmySphere, f = True)

        # upV
        cmds.setAttr('%s.vector1X' % dmyAglBtw, upV[0])
        cmds.setAttr('%s.vector1Y' % dmyAglBtw, upV[1])
        cmds.setAttr('%s.vector1Z' % dmyAglBtw, upV[2])

        # aimV
        cmds.setAttr('%s.vector2X' % dmyAglBtw, amV[0])
        cmds.setAttr('%s.vector2Y' % dmyAglBtw, amV[1])
        cmds.setAttr('%s.vector2Z' % dmyAglBtw, amV[2])

        outputRotAngle = cmds.getAttr('%s.rotate' % dmySphere)
        # print(outputRotAngle)
        self.outputRotAngle = outputRotAngle

        # cmds.delete(dmySphere, dmyAglBtw)
        for index in leftNodesSpace:
            cmds.connectAttr('%s.rotate' % dmySphere, '%s.rotate' % index, f = True)
        # cmds.delete(dmySphere, dmyAglBtw)
        cmds.delete(dmyAglBtw)
        cmds.select(cl = True)
        cmds.select(leftNodesSpace, r = True)

    # follicle unit
    def convertToCmFactor(self, *args):
        u""" <gCnstByFlcl :control>
         """
        unit = cmds.currentUnit(q = True, linear = True)
        if unit == 'mm':
            return 0.1
        elif unit == 'cm':
            return 1.0
        elif unit == 'm':
            return 100.0
        elif unit == 'in':
            return 2.54
        elif unit == 'ft':
            return 30.48
        elif unit == 'yd':
            return 91.44
        else:
            return 1.0

    # follicle main アルゴリズム 2
    def attachObjectToSurface(self, obj = '', surface = '', u = 0.0, v = 0.0):
        u""" <gCnstByFlcl :follicle main アルゴリズム 2>
        :param obj:
        :type obj: string  note: 拘束される transform ノードです。
        :param surface:
        :type surface: string  note: shapeです。
        :param u:
        :type u: float
        :param v:
        :type v: float
        """
        # print(obj, surface, u, v)

        # naming 解析
        strsCompLists = self.nodeName_decomp_exeB(obj)  # under bar 3 or 2 version
        if strsCompLists is None:
            strsCompLists = self.nodeName_decomp_exeC(obj)  # no under bar version
        print(u'%s naming 解析 ...' % obj)
        print('\t%s' % strsCompLists)

        # follicle1
        follicleTemp = cmds.createNode('follicle')  # follicle1 shape
        tforms = mel.eval('listTransforms %s' % follicleTemp)
        # print(tforms)
        follicleDagTemp = tforms[0]  # follicle1 transform
        # print(follicleDagTemp)
        cmds.select(follicleDagTemp, r = True)
        utilNodeShortNameSet = 'rvt Flcl'
        self.strCompLists_count_caseDividing_exe(strsCompLists,
                                                 utilNodeShortNameSet)  # naming
        follicleDag = cmds.ls(sl = True)[0]  # note: ここでは 親transform
        # print(follicleDag)
        follicle = cmds.listRelatives(follicleDag, shapes = True)[0]  # note: ここでは 子shape
        # # follicle = cmds.ls(sl = True)[0]
        # print(follicle)

        cmds.connectAttr('%s.worldMatrix[0]' % surface, '%s.inputWorldMatrix' % follicle,
                         f = True)
        nType = cmds.nodeType(surface)  # print(nType)
        if nType == 'nurbsSurface':
            cmds.connectAttr('%s.local' % surface, '%s.inputSurface' % follicle, f = True)
        else:
            cmds.connectAttr('%s.outMesh' % surface, '%s.inputMesh' % follicle, f = True)

        cmds.connectAttr('%s.outTranslate' % follicle, '%s.translate' % follicleDag,
                         f = True)
        # print(cmds.getAttr('%s.outRotate' % follicle))
        cmds.connectAttr('%s.outRotate' % follicle, '%s.rotate' % follicleDag,
                         f = True)  # 軸(オリエントnormal)がここで決定している
        cmds.setAttr('%s.translate' % follicleDag, l = True)
        cmds.setAttr('%s.rotate' % follicleDag, l = True)
        cmds.setAttr('%s.parameterU' % follicle, u)  # ポジションがここで決定している
        cmds.setAttr('%s.parameterV' % follicle, v)  # ポジションがここで決定している

        cmds.parent(obj, follicleDag)
        for xyz in list('xyz'):
            cmds.setAttr('%s.t%s' % (obj, xyz), 0)
            cmds.setAttr('%s.r%s' % (obj, xyz), 0)

    # follicle main アルゴリズム 1
    def parentToSurface(self, *args):
        u""" <gCnstByFlcl :follicle main アルゴリズム 1>
         """
        # sl = cmds.ls(sl = True)
        # numSel = len(sl)
        sl = self.nodeAll
        numSel = len(sl)
        # if numSel < 2:
        #     cmds.warning(
        #         "ParentToSurface: select object(s) to parent followed by a mesh or "
        #         "nurbsSurface to attach to.")
        #     return
        # surface = sl[-1]
        surface = self.geoNode  # note: ここでは transform
        # print(surface)
        if cmds.nodeType(surface) == 'transform':
            shapes = cmds.ls(surface, dagObjects = True, shapes = True,
                             noIntermediate = True, visible = True)
            # print(shapes)
            if len(shapes) > 0:
                surface = shapes[0]
        # print(surface)
        self.geoNodeShape = surface
        surface = self.geoNodeShape  # note: ここでは 親transform の 子shape
        # nType = cmds.nodeType(surface)
        nType = self.geoNodeType
        # print(nType)
        if nType != 'mesh' and nType != 'nurbsSurface':
            cmds.warning('ParentToSurface: Last selected item '
                         'must be a mesh or nurbsSurface.')
            return
        clPos = ''
        convertFac = 1.0

        # print(surface)

        # naming 解析
        strsCompLists = self.nodeName_decomp_exeB(surface)  # under bar 3 or 2 version
        if strsCompLists is None:
            strsCompLists = self.nodeName_decomp_exeC(surface)  # no under bar version
        print(u'%s naming 解析 ...' % surface)
        print('\t%s' % strsCompLists)

        if nType == 'nurbsSurface':  # nurbsSurface バージョン
            # closestPointOnSurface1
            # naming
            cmds.createNode('closestPointOnSurface')  # closestPointOnSurface1
            utilNodeShortNameSet = 'rvt CPOSurf'
            self.strCompLists_count_caseDividing_exe(strsCompLists,
                                                     utilNodeShortNameSet)  # naming
            clPos = cmds.ls(sl = True)[0]  # 新規のノード変数名を clPos と 'わざと' 統一

            cmds.connectAttr('%s.worldSpace[0]' % surface, '%s.inputSurface' % clPos,
                             f = True)
            minU = cmds.getAttr('%s.minValueU' % surface)
            maxU = cmds.getAttr('%s.maxValueU' % surface)
            sizeU = maxU - minU  # print(sizeU)
            minV = cmds.getAttr('%s.minValueV' % surface)
            maxV = cmds.getAttr('%s.maxValueV' % surface)
            sizeV = maxV - minV  # print(sizeV)
        else:  # mesh バージョン
            convertFac = self.convertToCmFactor()
            # closestPointOnMesh1
            # naming
            cmds.createNode('closestPointOnMesh')  # closestPointOnMesh1
            utilNodeShortNameSet = 'rvt CPOMesh'
            self.strCompLists_count_caseDividing_exe(strsCompLists,
                                                     utilNodeShortNameSet)  # naming
            clPos = cmds.ls(sl = True)[0]  # 新規のノード変数名を clPos と 'わざと' 統一

            cmds.connectAttr('%s.worldMesh[0]' % surface, '%s.inMesh' % clPos, f = True)
            cmds.connectAttr('%s.worldMatrix[0]' % surface, '%s.inputMatrix' % clPos,
                             f = True)  # もしnearestPointOnMeshを利用の時は、ここは不要！

        leftNodes = self.leftNodes
        for numIndex in range(numSel - 1):
            obj = leftNodes[numIndex]
            # print('koko')
            # print(obj)
            if cmds.nodeType(obj) != 'transform':
                cmds.warning('ParentToSurface: select the transform of the node(s) '
                             'to constrain\n')
                continue
            bbox = []
            bbox = cmds.xform(obj, q = True, ws = True, bb = True)
            # print(bbox)
            pos = []
            pos.append((bbox[0] + bbox[3]) * 0.5)
            pos.append((bbox[1] + bbox[4]) * 0.5)
            pos.append((bbox[2] + bbox[5]) * 0.5)
            # print(pos)
            cmds.setAttr('%s.inPosition' % clPos,
                         pos[0] * convertFac,
                         pos[1] * convertFac,
                         pos[2] * convertFac,
                         type = 'double3'
                         )
            closestU = cmds.getAttr('%s.parameterU' % clPos)
            closestV = cmds.getAttr('%s.parameterV' % clPos)
            if nType == 'nurbsSurface':
                closestU = (closestU + minU) / sizeU
                closestV = (closestV + minV) / sizeV

            # print('exe')
            # print(obj, surface)
            self.attachObjectToSurface(obj, surface, closestU, closestV)
        cmds.delete(
            clPos)  # 最後に 不要となった clPos が残ったままなので削除  # if clPos != '':  #     cmds.delete(clPos)
    # geoConstraintByFollicle(gCnstByFlcl) ############ geoConstraintByFollicle ######## end
    ########################################################################################

    # selection 共通関数 v2
    def commonCheckSelection(self, *args):
        u""" <selection 共通関数 v2>
        :return selList:
        :rtype selList: list of string
        """
        selList = cmds.ls(sl = True) or []
        # print(selList)
        # if not len(selList):
        #     print('\n' + '***' * 10)
        #     print(u'# result : node を選択し、してください。')
        #     print('***' * 20 + '\n')
        # else:
        #     print('\n' + '***' * 10)
        #     print(u'# result : commonCheckSelection:継続中')
        #     print('***' * 10 + '\n')
        return selList

    # 1番目選択の geoNodeType を数字で返します
    def geoNodeTypeCheck(self, *args):
        u""" <1番目選択の geoNodeType を数字で返します>
        :return geoNodeTypNum: int 0 or 1 or 2
        :rtype geoNodeTypNum: int
        """
        geoNodeTypNum = 0
        if len(self.geoNode) == 0 or len(self.leftNodes) == 0:
            print('***' * 10)
            print(u'1番目2番目の入力登録に誤りがあります。'
                  u'シーン内に存在しないオブジェクトの可能性があるか、'
                  u'もしくは、何も登録がされていません。')
            print('***' * 10)
            geoNodeTypNum = 0
            return geoNodeTypNum
        else:
            geo = self.geoNode
            # print(geo)
            geoType = cmds.objectType(cmds.listRelatives(geo, s = True)[0])
            if geoType == 'nurbsSurface':
                geoNodeTypNum = 1
                self.geoNodeType = 'nurbsSurface'
            elif geoType == 'mesh':
                geoNodeTypNum = 2
                self.geoNodeType = 'mesh'
            else:
                geoNodeTypNum = 0
                self.geoNodeType = 'other'
            return geoNodeTypNum

    # あくまでもUIありきの時に利用します。
    def execute(self, *args):
        u""" <あくまでもUIありきの時に利用します>
        """
        self.runInUiOrCommand = 'fromUI'
        print(self.runInUiOrCommand)

        # print(args)
        selList = self.selList
        print(selList)
        if not selList:
            print(u'中止します。')
            pass
        elif len(selList) == 1:
            print(u'選択しているものが一つだけなので、中止します。\n')
            pass
        elif len(selList) >= 2:
            print(u'選択しているものが2ケ以上なので、継続中。。。\n')
            geoNode = self.geoNode
            leftNodes = self.leftNodes
            print(geoNode, leftNodes)
            cnstTyp = cmds.radioCollection('typ_cRdioCollectA', q = True, select = True)
            if cnstTyp == 'typ_cRdioBtnA':
                cnstTyp = 1
            elif cnstTyp == 'typ_cRdioBtnB':
                cnstTyp = 2
            elif cnstTyp == 'typ_cRdioBtnC':
                cnstTyp = 3
            self.cnstTyp = cnstTyp
            # print('constraint type : %s' % cnstTyp)
            upV = self.ui_upV_values_get()[1]  # get upV value
            self.upV = upV
            amV = self.ui_amV_values_get()[1]  # get amV value
            self.amV = amV
            print(self.geoNode, self.leftNodes, self.upV, self.amV, self.cnstTyp)

            # 追加1
            # 全て上手くいっているので、一旦 script job を切断し、エラー回避します
            cmds.scriptJob(kill = self.jobNum, force = True)
            print(u'\n一旦 '
                  'kill scriptJob : %s' % self.jobNum)

            self.command(geo = geoNode, nodes = leftNodes, up = upV, aim = amV,
                         type = cnstTyp)  # main command 関数へ渡ります

    # node TRの connection を break し、接続された余計なノードも同時に除去する関数
    def brkCommand(self, *args):
        u""" <node TRの connection を break し、接続された余計なノードも同時に除去する関数 です。>
        """
        # print('hello')
        sels = self.commonCheckSelection()
        # print (sels)
        hasPOSINodes = []  # POSI : pointOnSurfaceInfo の略
        for sel in sels:
            ptOnSrfInfo = cmds.listConnections(sel, p = False
                                               , type = 'pointOnSurfaceInfo'
                                               ) or []
            if not ptOnSrfInfo:
                pass
            else:
                hasPOSINodes.append(sel)
        # print (hasPOSINodes)
        for node in hasPOSINodes:
            ptOnSrfInfo = cmds.listConnections(node, p = False
                                               , type = 'pointOnSurfaceInfo')[0]
            print (ptOnSrfInfo)
            cmds.delete(ptOnSrfInfo)

    # main
    # 辞書型引数を持つ、当関数 command を必ず経由します
    def command(self, *args, **kwargs):
        u""" <main : 辞書型引数を持つ、当関数 command を必ず経由します>

        :param kwargs: geo = string
            , nodes = list of string [string, string, ..]
            , up = list of int [int, int, int]
            , aim = list of int [int, int, int]
            , type = int            # longName
        :param kwargs: g = string
            , ns = list of string [string, string, ..]
            , up = list of int [int, int, int], am = list of int [int, int, int]
            , ty = int
            # shortName
        :type kwargs: dict
        """
        # 追加と修正2
        # print(self.runInUiOrCommand)
        if self.runInUiOrCommand == 'fromUI':
            self.runInUiOrCommand ='fromUI'
        elif self.runInUiOrCommand == '':
            self.runInUiOrCommand ='fromCmd'
        print(f'check, Run in UI or Command: {self.runInUiOrCommand}')

        print('\n' + '***' * 20)
        print('kwargs : %s' % kwargs)
        # py3へ変更
        key0 = list(kwargs.keys())[0]  # kwargs.keys() - > list(kwargs.keys())
        val0 = kwargs.get(key0)
        key1 = list(kwargs.keys())[1]  # kwargs.keys() - > list(kwargs.keys())
        val1 = kwargs.get(key1)
        key2 = list(kwargs.keys())[2]  # kwargs.keys() - > list(kwargs.keys())
        val2 = kwargs.get(key2)
        key3 = list(kwargs.keys())[3]  # kwargs.keys() - > list(kwargs.keys())
        val3 = kwargs.get(key3)
        key4 = list(kwargs.keys())[4]  # kwargs.keys() - > list(kwargs.keys())
        val4 = kwargs.get(key4)
        geoNode = kwargs.get('geo', kwargs.get('g', val0))  # longName shortName を考慮
        print('geo : %s' % geoNode)
        leftNodes = kwargs.get('nodes', kwargs.get('ns', val1))  # longName shortName を考慮
        print('nodes : %s' % leftNodes)
        upV = kwargs.get('up', kwargs.get('up', val2))  # longName shortName を考慮
        print('upV : %s' % upV)
        amV = kwargs.get('aim', kwargs.get('am', val3))  # longName shortName を考慮
        print('aimV : %s' % amV)
        cnstTyp = kwargs.get('type', kwargs.get('ty', val4))  # longName shortName を考慮
        print('type : %s' % cnstTyp)
        print('***' * 20 + '\n')
        self.geoNode = geoNode
        self.leftNodes = leftNodes
        # print(geoNode, leftNodes)
        nodeAll = [geoNode]  # geoNode だけあらかじめ入れておく
        for index in leftNodes:
            nodeAll.append(index)
        # print(nodeAll)
        self.nodeAll = nodeAll
        print(self.nodeAll)
        self.upV = upV
        self.amV = amV
        geoNodeTypNum = self.geoNodeTypeCheck()
        print(geoNodeTypNum)
        self.cnstTyp = cnstTyp
        print(cnstTyp)
        # print('\n')
        print('\n' + '***' * 20)
        if geoNodeTypNum == 0:
            print('***' * 10)
            print(u'1番目に入力登録されたオブジェクトが、'
                  u'\'nurbsSurface\' \'mesh\' 以外の可能性があります。\n'
                  u'もしくは、2番目に入力登録されたオブジェクトに誤りがあります。'
                  u'確認願います。\n操作を中止します。end...')
            print('***' * 10)
            pass
        elif geoNodeTypNum == 1 and cnstTyp == 1:  # 1:nurbsByRivet タイプ 実行の決定
            print('***' * 10)
            print(u'########## nurbsByRivet タイプ start... ##########')
            self.surfaceConstraintByRivet()
            print('***' * 10)
        elif geoNodeTypNum == 2 and cnstTyp == 2:  # 2:meshByRivet バージョン 実行の決定
            print('***' * 10)
            print(u'########## meshByRivet タイプ start... ##########')
            self.meshConstraintByRivet()
            print('***' * 10)
        elif cnstTyp == 3:  # 3:geoByFollicle バージョン 実行の決定
            print('***' * 10)
            print(u'########## geoByFollicle タイプ start... ##########')
            # print(self.geoNodeType)
            self.geoConstraintByFollicle()
            print('***' * 10)
        else:
            print('***' * 10)
            print(u'1番目に入力登録されたオブジェクトの nodeType と、\n'
                  u'ユーザーの指定した、constraint type が異なっている可能性があります。\n'
                  u'確認願います。\n操作を中止します。end...')
            print('***' * 10)
            pass
        print('***' * 20 + '\n')
        self.commonResultPrintOut(geoNode, leftNodes, upV, amV, cnstTyp)

    # コマンドベースの実行文を生成する関数
    def commonResultPrintOut(self, geoNode, leftNodes, upV, amV, cnstTyp):
        u""" <コマンドベースの実行文を生成する関数>
        :param geoNode:
        :type geoNode: string
        :param leftNodes:
        :type leftNodes: list of string
        :param upV:
        :type upV: list of int    [int, int, int]    int:-1 or 0 or 1
        :param amV:
        :type amV: list of int    [int, int, int]    int:-1 or 0 or 1
        :param cnstTyp:
        :type cnstTyp: int:1 or 2 or 3
        """
        moduleName = __name__
        # print(moduleName)
        className = self.classNameOutput()
        # print(className)
        print(geoNode, leftNodes, upV, amV, cnstTyp)
        print('execute done')

        # 追加1
        # 実行終了後、即座に、leftNodes のみを選択
        cmds.select(leftNodes, r = True)

        # 追加と修正2
        # print(f'check, Run in UI or Command: {self.runInUiOrCommand}')
        if self.runInUiOrCommand == 'fromCmd':
            pass
        elif self.runInUiOrCommand == 'fromUI':
            # 追加1
            # エラー回避を終了し、script job を新規に復活させます
            self.jobNum = cmds.scriptJob(event = ["SelectionChanged", self.ui_select_act_exe]
                                         , parent = self.win
                                         )
            print(u'\n再び '
                  'scriptJob : %s' % self.jobNum)

        print('...........')
        print('# result : {A}.{AA}().{AAA}'
              '(geo = u\'{B}\', nodes = {C}, up = {D}, aim = {E}, type = {F})'
              .format(A = moduleName, AA = className, AAA = 'command',
                      B = geoNode, C = leftNodes, D = upV, E = amV, F = cnstTyp)
              )
        print('# result : {A}.{AA}().{AAA}'
              '(g = u\'{B}\', ns = {C}, up = {D}, am = {E}, ty = {F})'
              .format(A = moduleName, AA = className, AAA = 'command',
                      B = geoNode, C = leftNodes, D = upV, E = amV, F = cnstTyp)
              )
        return self.jobNum  # UI restart


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
    UI.showUI()  # open UI
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する

print(u'モジュール名：{}\n'.format(__name__))  # 実行したモジュール名を表示する
