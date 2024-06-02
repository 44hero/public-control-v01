# -*- coding: utf-8 -*-

u"""
YO_logger2.py

:Author:
    oki yoshihiro
    okiyoshihiro.job@gmail.com
:Version: -1.0-
:Date: 2022/09/12

概要(overview):
    組み込み関数printに代わる、汎用性のある一連のログを出力するモジュールです
詳細(details):
    ・ 以下の2パターンを実現
        #. 目的の関数のコード内部でのログ表示

        #. 目的の関数のコードの先頭末端でのログ表示
使用法(usage):
    ・ 目的先での記述例は以下
        #. 目的の関数のコード内部に、細かな情報を出力するための、組み込み関数printに代わる、
            ログ表示を行いたい時

            e.g.):
                ::

                  from YO_logger2 import LogProcess_Output  # ログプロセス出力用クラス
                  YO_logProcess = LogProcess_Output()  # インスタンスオブジェクト化
                            ...
                            ...
                            ...
                  YO_logProcess.action(levelStr, message) # action func実行で細かな情報出力、として利用
                            :param str levelStr: loggingレベル記述です。
                              default 'NOTSET'
                              以下のいずれかです。
                              いずれか.):
                                  'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'
                            :param str message: メッセージ出力の為の任意な記述です。

        #. 目的の関数のコードの先頭にデコレーターを付与し、デコレーターを利用した、
            ログ表示を行いたい時

            e.g.):
                ::

                  from YO_logger2 import Decorator  # ログデコレーター用クラス
                  instance = Decorator()  # インスタンスオブジェクト化
                            ...
                            ...
                            ...
                  @instance.declogger
                  def ****(...):
                    ...
注意(note):
    他に必須な独自モジュール
        ::

-リマインダ-
    done: 新規作成 2023/02/22~
        version = '-1.0-'
"""

# ログのライブラリ
import logging
from logging import getLogger, StreamHandler, Formatter  # 途中で誤ってloggingを汚さないように個別にimport
import inspect


# ######################################################################################
# 関数コード内にlog processを出力目的 ###################################### start
# 目的の関数コード内にlog processを出力するクラス
class LogProcess_Output(object):
    u"""< 目的の関数コード内にlog processを出力するクラス です >

    ::

      -使い方-
        目的の関数のコード内部に、細かな情報を出力するための、組み込み関数printに代わる、ログ表示を行います
        e.g.):
          目的の関数のコード内部に、
              YO_logProcess.action(....) :
          のように、埋め込み記述します。細かな情報出力、として利用しています。
          組み込み関数printに代わるものと考えてください。
          そのためには、予め、
              from YO_logger2 import LogProcess_Output
              YO_logProcess = LogProcess_Output()
          という風に、インスタンス化が必要です。

      -開発用と本番用の切り替え方法-
        LogProcess_Output.action コード内の、
          以下の 1. 2.何れかを示すコード行記述の、コメントアウトが肝となっています
              開発用(development)と、本番用(product) を共存させないようにします
            1. logger = self.myDeveLogger()  # 開発用(development)
            2. logger = self.myPdctLogger()  # 本番用(product)
          通常は、1行目をコメントアウトしています。
            b/c): 本番用(product)で使用が常な為

      -loggingの基本-
        1. ログを管理するloggerを作成
        2. ログ出力を管理するhandlerを作成
        3. 任意のhandlerをloggerにセット。
        という風に使っていきます。

      -ロギングレベルとは-
        +-----------+------+--------------------------------+
        | レベル     | 数値 | 利用するタイミング(任意)                  |
        +===========+======+================================+
        | CRITICAL  | 50   | プログラムが実行不可となるような重大なエラーが発生した場合  |
        | ERROR     | 40   | 重大な問題により、機能を実行出来ない場合           |
        | WARNING   | 30   | 想定外の処理やそれが起こりそうな場合             |
        | INFO      | 20   | 想定内の処理が行われた場合                  |
        | DEBUG     | 10   | 問題探求に必要な詳細な情報を出力したい場合          |
        | NOTSET    | 0    |                                |
        +-----------+------+--------------------------------+
    """
    def __init__(self):
        pass

    # logを出力する関数
    def action(self, levelStr = 'NOTSET', message = 'test'):
        u""" < logを出力する関数 です >

        ::

          -開発用と本番用の切り替え方法-
            以下の 1. 2.何れかを示すコード行を、コメントアウトして、
              開発用(development)と、本番用(product) を共存させないようにします
                1. logger = self.myDeveLogger()  # 開発用(development)
                2. logger = self.myPdctLogger()  # 本番用(product)
            通常は、1行目をコメントアウトしています。
                b/c): 本番用(product)で使用が常な為

        #######################

        #.
            :param str levelStr: loggingレベル記述です。
                default 'NOTSET'

            以下のいずれかです。
                いずれか.):
                    'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'
            レベルについて.):
                'CRITICAL' > 'ERROR' > 'WARNING' > 'INFO' > 'DEBUG' > 'NOTSET'

        #.
            :param str message: メッセージ出力の為の任意な記述です。

        #######################
        """
        # #################################################
        # 以下の2行のコードを何れか、
        #   logger = self.myDeveLogger()  # 開発用(development)
        #   logger = self.myPdctLogger()  # 本番用(product)
        # の行をコメントアウトして、
        # 開発用(development)と、本番用(product)を区別してください
        # 通常は、1行目をコメントアウトしています。
        #   b/c): 本番用(product)で使用が常な為
        # #################################################
        # logger = self.myDeveLogger()  # 開発用(development)
        logger = self.myPdctLogger()  # 本番用(product)

        # --------------------------------
        # ログ出力
        # --------------------------------
        if levelStr is 'NOTSET':
            # logger.log(0, 'NOTSET' + ' ' + 'Hello World!')  # NOTSET
            logger.log(0, message)
        elif levelStr is 'DEBUG':
            # logger.log(10, 'DEBUG' + ' ' + 'Hello World!')  # DEBUG
            logger.debug('-----' * 5 + '\n\t' + 'DEBUG' + '\n\t\t' + message)  # DEBUGと同等
        elif levelStr is 'INFO':
            # logger.log(20, 'INFO' + ' ' + 'Hello World!')  # INFO
            logger.info('-----' * 5 + '\n\t' + 'INFO' + '\n\t\t' + message)  # INFOと同等
        elif levelStr is 'WARNING':
            # logger.log(30, 'WARNING' + ' ' + 'Hello World!')  # WARNING
            logger.warning(message)  # WARNINGと同等
        elif levelStr is 'ERROR':
            # logger.log(40, 'ERROR' + ' ' + 'Hello World!')  # ERROR
            logger.error(message)  # ERRORと同等
        elif levelStr is 'CRITICAL':
            # logger.log(50, 'CRITICAL' + ' ' + 'Hello World!')  # CRITICAL
            logger.critical(message)  # CRITICALと同等

    # 開発用独自loggerを準備   # 'development_log'
    def myDeveLogger(self):
        u""" < 開発用独自loggerを準備 します >

        ::

          'development_log' としてdebugより上レベル出力を想定しています
          loggerのログレベルがDEBUGの場合、それより低いhandlerのDEBUGまでは表示されます
          基本的には、
              1. ログを管理するloggerを作成
              2. ログ出力を管理するhandlerを作成
              3. 任意のhandlerをloggerにセット。
          という風に使っていきます。

        #######################

        #.
            :return: my_Deve_logger
                ログを管理する開発用独自logger
            :rtype my_Deve_logger: Logger object

        #######################
        """
        # loggerのログレベルがDEBUGの場合、それより低いhandlerのDEBUGまでは表示される。
        # --------------------------------
        # 1.loggerの設定
        # --------------------------------
        # loggerオブジェクトの宣言
        my_Deve_logger = getLogger('development_log')
        # loggerのログレベル設定(ハンドラに渡すエラーメッセージのレベル)
        my_Deve_logger.setLevel(logging.DEBUG)
        # 一旦handlerが無いか調べて有ったら消す
        for h in my_Deve_logger.handlers[:]:
            # print(h)
            my_Deve_logger.removeHandler(h)
            h.close()
        # --------------------------------
        # 2.handlerの設定
        # --------------------------------
        # 独自formatを定義するためには、独自handlerと独自formatterが必要なので。。
        # handlerの生成
        my_Deve_handler = StreamHandler()
        # handlerのログレベル設定(ハンドラが出力するエラーメッセージのレベル)
        my_Deve_handler.setLevel(logging.DEBUG)
        # ログ出力フォーマット設定
        my_Deve_formatter = Formatter(''
                                      '-----' * 20 + '\n\t'
                                      +
                                      '%(asctime)s'
                                      ' - '
                                      '%(name)s'
                                      ' - '
                                      '%(funcName)s'
                                      ' - '
                                      '%(levelname)s'
                                      # ' - '
                                      # '%(pathname)s'
                                      )
        my_Deve_handler.setFormatter(my_Deve_formatter)
        # --------------------------------
        # 3.loggerにhandlerをセット
        # --------------------------------
        my_Deve_logger.addHandler(my_Deve_handler)
        my_Deve_logger.propagate = True

        return my_Deve_logger

    # 本番用独自loggerを準備   # 'product_log'
    def myPdctLogger(self):
        u""" < 本番用独自loggerを準備 します >

        ::

          'product_log' としてinfoより上レベル出力を想定しています
          loggerのログレベルがINFOの場合、それより低いhandlerのINFOまでは表示されます
          基本的には、
              1. ログを管理するloggerを作成
              2. ログ出力を管理するhandlerを作成
              3. 任意のhandlerをloggerにセット。
          という風に使っていきます。

        #######################

        #.
            :return: my_Pdct_logger
                ログを管理する本番用独自logger
            :rtype my_Pdct_logger: Logger object

        #######################
        """
        # loggerのログレベルがINFOの場合、それより低いhandlerのINFOまでは表示される。
        # --------------------------------
        # 1.loggerの設定
        # --------------------------------
        # loggerオブジェクトの宣言
        my_Pdct_logger = getLogger('product_log')
        # loggerのログレベル設定(ハンドラに渡すエラーメッセージのレベル)
        my_Pdct_logger.setLevel(logging.INFO)
        # 一旦handlerが無いか調べて有ったら消す
        for h in my_Pdct_logger.handlers[:]:
            # print(h)
            my_Pdct_logger.removeHandler(h)
            h.close()
        # --------------------------------
        # 2.handlerの設定
        # --------------------------------
        # 独自formatを定義するためには、独自handlerと独自formatterが必要なので。。
        # handlerの生成
        my_Pdct_handler = StreamHandler()
        # handlerのログレベル設定(ハンドラが出力するエラーメッセージのレベル)
        my_Pdct_handler.setLevel(logging.INFO)
        # ログ出力フォーマット設定
        my_Pdct_formatter = Formatter(''
                                      +
                                      '-----' * 20 + '\n\t'
                                      +
                                      # '%(asctime)s'
                                      # ' - '
                                      # '%(pathname)s'
                                      # ' - '
                                      '%(module)s'
                                      ' - '
                                      # '%(filename)s'
                                      # ' - '
                                      '%(funcName)s'
                                      ' - '
                                      '%(levelname)s'
                                      # ' - '
                                      # '%(lineno)d'
                                      # ' - '
                                      # '%(message)s'
                                      )
        my_Pdct_handler.setFormatter(my_Pdct_formatter)
        # --------------------------------
        # 3.loggerにhandlerをセット
        # --------------------------------
        my_Pdct_logger.addHandler(my_Pdct_handler)
        my_Pdct_logger.propagate = True

        return my_Pdct_logger


# 任意の行を出力
def getLineNo():
    u""" < 任意の行を出力 します >

    #######################

    #.
        :return: lineno
            行
        :rtype lineno: str

    #######################
    """
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    lineno = calframe[1][2]
    # print('\n'
    #       + '---' * 5 + '\n'
    #       + 'line number: '
    #       + str(lineno)
    #       + '\n'
    #       + '---' * 5
    #       )
    return str(lineno)


# 未使用
def _getFileName():
    u""" <>

    :return: filename
    :rtype: str
    """
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    fn = calframe[1][1].split('/')
    filename = fn[len(fn) - 1]
    return filename
# 関数コード内にlog processを出力目的 ######################################## end
# ######################################################################################

# その他のライブラリ
import logging.config
import datetime
import time
import inspect


# ######################################################################################
# デコレーター使用目的 ##################################################### start
# デコレーター使用を目的としたlog processを出力するクラス   # 'development_log'
class Decorator(object):
    u"""< デコレーター使用を目的としたlog processを出力するクラス です >

    ::

      -使い方-
        'development_log' としてdebugログより上レベル出力を想定しています
        目的の関数のコードの先頭にデコレーターを付与し、デコレーターを利用した、ログ表示を行います
        e.g.):
          目的の関数のコードの先頭に、
              @instance.declogger
          のように、付加し使用します。
          そのためには、予め、
              from YO_logger2 import Decorator
              instance = Decorator()
          という風に、インスタンス化が必要です。

      -補足-
        Decorator.declogger.wrapper コード内の、
          _logger.setLevel(logging.DEBUG) が肝となっています
        記述を、
          _logger.setLevel(logging.INFO) 等、レベルを上げることで、DEBUGログは出力されません
    """
    def my_getlogger(self):
        # logging.basicConfig(level = logging.CRITICAL)
        return getLogger(
            # '' + __name__ + '.' + self.__class__.__name__ + '.' +
            'development_log'
        )

    # 未使用
    def setfileConfig(self, _path):
        logging.config.fileConfig(fname = _path)

    def declogger(self, func):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        fn = calframe[1][1].split('/')
        filename = fn[len(fn) - 1]
        modulename = fn[len(fn) - 2]
        lineno = calframe[1][2]
        code_context = calframe[1][4]
        funcname = code_context[len(code_context) - 1]
        defaultmessage = '[' + modulename + '.' + filename + ':' \
                         + str(lineno) + '][' \
                         + funcname.strip() \
                         + ']:'

        def wrapper(*args, **kwargs):
            sw = StopWatch()
            sw.sw_start()
            _logger = self.my_getlogger()
            _logger.setLevel(logging.DEBUG)
            _logger.debug('\n\t\t' + defaultmessage + '\n\t\t\t' + '---' * 20 + ':------start-' )
            result = func(*args, **kwargs)
            processTime = u'***** 処理時間:{} ***'.format(sw.sw_stop())
            _logger.debug('\n\t\t' + defaultmessage + '\n\t\t\t' + '---' * 20 + ':------end-'
                          + '\n'
                          + processTime
                          + '\n'
                          )
            return result
        wrapper.__name__ = func.__name__
        return wrapper

    # 未使用
    def edtmessage(self, message):
        calframe = inspect.getouterframes(inspect.currentframe(), 2)
        fn = calframe[2][1].split('/')
        filename = fn[len(fn) - 1]
        modulename = fn[len(fn) - 2]
        lineno = calframe[1][2]
        return '[' + modulename + '.' + filename + ':' \
               + str(lineno) + '][' \
               + calframe[1][3] \
               + "]:" \
               + str(message)

    # 未使用
    def writedebuglog(self, message):
        self.getlogger().debug(self.edtmessage(message))
        return

    # 未使用
    def writeinfolog(self, message):
        self.getlogger().info(self.edtmessage(message))
        return

    # 未使用
    def writeerrorlog(self, message):
        self.getlogger().error(self.edtmessage(message))
        return


# 時間を計測するクラス
class StopWatch(object):
    u""" < 時間を計測するクラス です>

    ::

      Decorator.declogger.wrapper
      に使用しています
    """
    def sw_start(self):
        self.__starttime = time.time()
        return

    def sw_stop(self):
        return time.time() - self.__starttime
# デコレーター使用目的 ####################################################### end
# ######################################################################################

if __name__ == '__main__':
    print(u'{}.py: loaded as script file'.format(__name__))
else:
    print(u'{}.py: loaded as module file'.format(__name__))
    print('{}'.format(__file__))  # 実行したモジュールフルパスを表示する

print(u'モジュール名:{}\n'.format(__name__))  # 実行したモジュール名を表示する
