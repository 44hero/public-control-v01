# -*- coding: utf-8 -*-

u"""
pyside2IniFileSetting.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -2.0-
:Date: 2024/03/15

概要(overview):
    ****のツールです。
詳細(details):
    ・ ***

    ・ ***
使用法(usage):
    ::

        ***
注意(note):
    ・ 当ツールは、****。
        #.
            ****

    ・ 他に必須なモジュール
        ::

            from *** import ***  # ***です

<UI 説明>
    ***

-UIを立ち上げずにコマンドベースで実行する方法-
    使用法(usage):
        e.g.):
            ***

-リマインダ-
    done: 2024/02/22~2024/03/15
        - 更新
            - 概要: 新しいことをインプットしたので、それを反映したひな形を更新
            - 詳細:

        version = '-2.0-'
    done: 2024/02/22
        新規作成

        version = '-1.0-'
"""

# 標準ライブラリ #################################################################
import os

# サードパーティライブラリ #########################################################
from PySide2.QtCore import QSettings

# ローカルで作成したモジュール #####################################################


class IniFileSetting(object):
    def __init__(self, title: str):
        self.prefix = 'test'
        self.commonName = 'MayaPySide2_windowPrefs_setting'
        self.win = title + '_ui'

        self.filename = None
        self.__settings = None

    # オリジナルメソッド
    # .iniファイルの設定 関数
    def iniFileSetting(self):
        u""" < .iniファイルの設定 関数 です >

        オリジナルメソッド
        """
        folderName = f'{self.prefix}_{self.commonName}'
        maya_app_dir = os.getenv('MAYA_APP_DIR')  # user document maya directory
        maya_location = os.getenv('MAYA_LOCATION')  # pc maya directory(include version)
        maya_version = maya_location.split(r'/')[-1]  # get a maya version name
        deleteStr = 'Maya'
        versionNumber = maya_version.replace(deleteStr, '')  # get a maya version number only
        user_maya_document_dir = r'{}/{}'.format(maya_app_dir, versionNumber)

        # .iniファイル名
        settingFileName = self.win + '.ini'
        # 絶対パスを含むファイル名の設定
        self.filename = os.path.join(user_maya_document_dir,
                                     folderName,
                                     settingFileName
                                     )
        # print('###' * 10)
        # print(f'Preparing...')
        # print(f'\t'
        #       f'Preparing a set of .INI file, at \n\t\t'
        #       f'{self.filename}\n'
        #       f'Note: It has not been saved yet.'
        #       )
        # QSettingsで、ファイル名 と、フォーマット を指定してインスタンスを作成
        self.__settings = QSettings(self.filename, QSettings.IniFormat)
        # 「setIniCodec」を使って文字コードを「utf-8」で指定すると、日本語にも威力発揮
        self.__settings.setIniCodec('utf-8')

        return self.filename, self.__settings

    # .iniファイルの内容をクリアする
    def clear_ini_file(self):
        # QSettingsオブジェクトを削除して再作成
        if os.path.exists(self.filename):
            os.remove(self.filename)
        self.__settings = QSettings(self.filename, QSettings.IniFormat)
        self.__settings.setIniCodec('utf-8')
