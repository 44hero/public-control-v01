# -*- coding: utf-8 -*-

u"""
MyTabWidget.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -1.0-
:Date: 2024/03/08

.. note:: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PySide2 version: 5.15.2

概要(overview):
    - 通称: マイタブウィジェット(MyTabWidget)
    - 型: Union[QTabWidget, TypeOfSubclass]
        QTabWidgetクラス または、 その派生クラス(サブクラス) という意味です
詳細(details):
    PySide2.QtWidgets.QTabWidget の、独自規格クラス です。
使用法(usage):
    :param int tabCount: 1 以上のtab数を指定
        は、必須です。
    ::

        # ローカルで作成したモジュール
        import MyTabWidget
        reload(MyTabWidget)
        from MyTabWidget import MyTabWidget

        # 以下 e.g.):
        ############################################################
        tab_wid = MyTabWidget(tabCount = 3)  # tabウィジェット note): 数は、tab名 のリスト と等数がベスト
        main_layout.addWidget(tab_wid)  # メインレイアウト に タブウィジェット を追加
        ##############################

-リマインダ-
    done: 2024/03/08
        新規作成

        version = '-1.0-'
"""

# 標準ライブラリ
from typing import Tuple, List

# サードパーティライブラリ
from PySide2.QtWidgets import (QFrame, QTabWidget, QWidget, QVBoxLayout,
                               QGridLayout
                               )


class MyTabWidget(QTabWidget):
    def __init__(self, tabCount: int = 1):
        u"""

        :type int tabCount: tabの数を指定します
        """
        super().__init__()

        # 子tab widget リスト 定義
        self._tabs: List[QTabWidget] = []  # BTW): tab widget の数と tabCount は必ず一致します
        # 子tab widget の 子frame widget リスト 定義
        self._frames: List[QFrame] = []
        # 子tab widget の 子frame widget の 子grid layout リスト 定義
        self._frame_gdLays_list: List[QGridLayout] = []  # BTW): frame grid layout の数と tabCount は必ず一致します
        # 子tabラベル名 のリスト 定義
        self._tabLabelName_list: List[str] = []
        # クリックされたタブのインデックスを保存するための属性を追加します。
        self._clicked_tab_index = None

        # # タブウィジェットの作成
        # tab_widget = QTabWidget(self)
        # メインウィンドウ全体のレイアウトにタブウィジェットを追加
        # main_layout = QVBoxLayout(self)
        # main_layout.addWidget(self)
        self.setTabShape(QTabWidget.Rounded)  # タブの見た目 note): other type: Triangular

        i = 0
        while i < tabCount:
            # ラベル名 の定義
            tabLabelName = 'tab' + str(i)  # 各タブの 暫定ラベル名

            # タブウィジェット 定義
            tab_wid = QWidget()
            self.addTab(tab_wid, tabLabelName)  # tabLabelName: 各タブの ラベル名

            # # 組み込み関数 tabBarClicked シグナル に スロット を接続します。
            # self.tabBarClicked.connect(self.on_tab_clicked)

            self._tabs.append(tab_wid)
            self._tabLabelName_list.append(tabLabelName)

            # タブの大枠レイアウト 定義
            tab_lay = QVBoxLayout(tab_wid)
            # タブ内に QFrame を配置
            frame_tab_frWid = QFrame(tab_wid)
            # 子tab widget の 子frame widget は grid layout を一つ持ちます
            frame_tab_gdLay = QGridLayout(frame_tab_frWid)
            frame_tab_frWid.setFrameShape(QFrame.StyledPanel)  # 枠のスタイルを設定
            # タブの大枠レイアウト に QFrame を追加
            tab_lay.addWidget(frame_tab_frWid)

            self._frame_gdLays_list.append(frame_tab_gdLay)

            i += 1
        # # タブ1
        # tab1_wid = QWidget()
        # self.addTab(tab1_wid, "tab1")
        # self._tabs.append(tab1_wid)
        #
        # # タブ2
        # tab2_wid = QWidget()
        # self.addTab(tab2_wid, "tab2")
        # self._tabs.append(tab2_wid)
        #
        # # タブ1の大枠レイアウト 定義
        # tab1_lay = QVBoxLayout(tab1_wid)
        # # タブ1内に QFrame を配置する
        # frame_tab1_frWid = QFrame(tab1_wid)
        # frame_tab1_gdLay = QGridLayout(frame_tab1_frWid)
        # frame_tab1_frWid.setFrameShape(QFrame.StyledPanel)  # 枠のスタイルを設定
        # # ここにQFrame内に配置したいウィジェットを追加
        # # frame_tab1_gdLay.addWidget(QPushButton('test'))
        # # タブ1の大枠レイアウト にQFrameを追加
        # tab1_lay.addWidget(frame_tab1_frWid)
        # self._frame_gdLays_list.append(frame_tab1_gdLay)
        #
        # # タブ2の大枠レイアウト 定義
        # tab2_lay = QVBoxLayout(tab2_wid)
        # # タブ1内に QFrame を配置する
        # frame_tab2_frWid = QFrame(tab2_wid)
        # frame_tab2_gdLay = QGridLayout(frame_tab2_frWid)
        # frame_tab2_frWid.setFrameShape(QFrame.StyledPanel)  # 枠のスタイルを設定
        # # ここにQFrame内に配置したいウィジェットを追加
        # # frame_tab2_gdLay.addWidget(QPushButton('test'))
        # # タブ1の大枠レイアウト にQFrameを追加
        # tab2_lay.addWidget(frame_tab2_frWid)
        # self._frame_gdLays_list.append(frame_tab2_gdLay)

    # def on_tab_clicked(self, index):
    #     # クリックされたタブのインデックスを保存します。
    #     self._clicked_tab_index = index

    # メインとなる tab widget から、子tab widget を全て返す 関数
    def getAllChildrenTabWidget_fromMainTabWidget(self) -> List[QTabWidget]:
        u""" < メインとなる tab widget から、子tab widget を全て返す 関数 です>

        メインとなる tab widget から、全ての 子tab widget をゲットします

        :return: self._tabs: 全ての 子tab widget のリスト
        :rtype:  List[QTabWidget]
        """
        return self._tabs

    # メインとなる tab widget から、子tabラベル名 を全て返す 関数
    def getAllChildrenTabLabelName_fromMainTabWidget(self) -> List[str]:
        u""" < メインとなる tab widget から、子tabラベル名 を全て返す 関数 です>

        メインとなる tab widget から、全ての 子tabラベル名 をゲットします

        :return: self._tabLabelName_list: 全ての 子tabラベル名 のリスト
        :rtype:  List[str]
        """
        return self._tabLabelName_list

    # メインとなる tab widget から、子tab widget の 子frame widget の 子grid layout を返す 関数
    def getAllChildrenGridLayout_fromMainTabWidget(self) -> List[QGridLayout]:
        u""" < メインとなる tab widget から、子tab widget の 子frame widget の 子grid layout を返す 関数 です>

        メインとなる tab widget から、全ての 子grid layout をゲットします

        :return: self._frame_gdLays_list: 全ての 子grid layout のリスト
        :rtype: List[QGridLayout]
        """
        return self._frame_gdLays_list

    # 全ての frame widget を返す プロパティ
    @property
    def allFramesCall(self) -> List[QFrame]:
        u""" < 全ての frame widget を返す 関数 です>

        allFramesCall プロパティを準備し、全ての frame widget への容易なアクセスを可にする

        :return: self._frames: 全ての frame widget の name
        :rtype: List[QFrame]
        """
        return self._frames


if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する
# pprint.pprint(RT4_UI_PyMel.mro())  # メソッドを呼び出す順番が解ります

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
