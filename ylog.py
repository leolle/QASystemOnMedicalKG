#!/usr/bin/env python2
# -*- coding: utf-8 -*-
""" 封装了python的logging库，分别对控制台、文件及syslog日志做了更精细化的控制，
其中文件日志整合了官方的按天和按大小切割文件。
"""
import traceback
import logging
import logging.handlers
import os
import socket
import time
import sys

# init logging
DEFAULT_LOG_FORMAT = '%(asctime)s %(levelno)s %(message)s'


class MillisecFormatter(logging.Formatter):
    import datetime as dt
    converter = dt.datetime.fromtimestamp

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%H:%M:%S")
            s = "%s.%03d" % (t, record.msecs)
        return s


time_formatter = MillisecFormatter(DEFAULT_LOG_FORMAT)
fulltime_formatter = logging.Formatter(DEFAULT_LOG_FORMAT)


def set_format(format, datefmt):
    """设定日志输出格式化字符串

    :param format: 参照官方logging模块
    :param datefmt: 参照官方logging模块

    """
    time_formatter = logging.Formatter(format, datefmt)
    fulltime_formatter = logging.Formatter(format)


logger = logging.getLogger("base")
logger.propagate = False


def set_level(lvl):
    """设定最低输出日志等级，在该等级以下的日志不会被输出

    :param lvl: logging.level 可选值CRITICAL,ERROR,WARNING,INFO,DEBUG

    """
    logger.setLevel(lvl)


set_level(logging.INFO)  # set default log level

# logger.addHandler(logging.NullHandler())


def console_on():
    """启用控制台log输出
    """
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(fulltime_formatter)
    if not logger.handlers:
        logger.addHandler(stream_handler)
        # if logger.handlers:
    #     print('repeated handler')


def filelog_on(appname="app"):
    """启用文件日志

    :param str appname: 程序名

    """
    from datetime import datetime
    if not os.path.exists('log'):
        os.makedirs('log')
    filename = "log/%s.log" % (appname)

    filelog_handler = DailySizedRotatingFileHandler(filename=filename)
    filelog_handler.setFormatter(time_formatter)
    logger.addHandler(filelog_handler)


def remote_syslog_on(address=('localhost', 514), socktype=socket.SOCK_DGRAM):
    """启用远程模式syslog日志

    :param address: 远程syslog地址
    :param socktype: socket类型，默认以UDP方式发送日志

    """
    syslog_handler = logging.handlers.SysLogHandler(
        address=address, socktype=socktype)
    syslog_handler.setFormatter(fulltime_formatter)
    logger.addHandler(syslog_handler)


def log_trace_back():
    trace_back_msg = traceback.format_exc()
    if trace_back_msg != 'None\n':  # TODO: do not compare with str
        logger.error(trace_back_msg)


def error(*args, **kwargs):
    """写error级别日志
    """
    logger.error(*args, **kwargs)
    log_trace_back()


def info(*args, **kwargs):
    """写info级别日志
    """
    logger.info(*args, **kwargs)


def warning(*args, **kwargs):
    """写warning级别日志
    """
    logger.warning(*args, **kwargs)
    log_trace_back()


def debug(*args, **kwargs):
    """写debug级别日志
    """
    logger.debug(*args, **kwargs)


def exception(*args, **kwargs):
    """输出error日志，并打印堆栈信息
    """
    logger.exception(*args, **kwargs)


def critical(*args, **kwargs):
    """写critical级别日志
    """
    logger.critical(*args, **kwargs)
    log_trace_back()


class DailySizedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):

    def __init__(self,
                 filename,
                 maxBytes=5 * 1024 * 1024,
                 backupCount=1000,
                 encoding='utf-8'):
        """构造一个按时间和文件大小rotate的logging.Handler

        :param filename: 文件名
        :param maxBytes: 日志文件最大Size，默认5M
        :param backupCount: 最大文件数，默认1000
        既作用于按天也作用于按大小转换
        支持保存1000天的日志
        支持每天保存10G的日志

        :param encoding: 日志编码

        """
        assert maxBytes >= 0
        assert backupCount >= 0

        if maxBytes > 0:
            mode = 'a'

        logging.handlers.TimedRotatingFileHandler.__init__(
            self,
            filename,
            when='MIDNIGHT',
            backupCount=backupCount,
            encoding=encoding,
            delay=False)
        self.maxBytes = maxBytes

    def shouldRollover(self, record):
        """ 该方法决定何时rotate日志文件

        :param record: 将要输出的日志记录

        """
        self.stream = self._open()

        # 以下代码摘自官方RotatingFileHandler
        if self.stream is None:  # delay was set...
            self.stream = self._open()
        if self.maxBytes > 0:  # are we rolling over?
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, 2)  #due to non-posix-compliant Windows feature
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return 1

        # 以下代码摘自官方TimedRotatingFileHandler
        t = int(time.time())
        if t >= self.rolloverAt:
            return 1
        #print "No need to rollover: %d, %d" % (t, self.rolloverAt)
        return 0

    def doRollover(self):
        """
        扩展了官方TimedRotatingFileHandler的版本，建立新文件时格式定义为
        filename.%Y-%m-%d.num
        num从1开始，每次rotate时自增
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)

        timed_filename = self.baseFilename + "." + time.strftime(
            self.suffix, timeTuple)
        if os.path.exists(timed_filename + '.1'):
            if sys.version_info.major > 2:
                for i in range(self.backupCount, 0, -1):
                    sfn = "%s.%d" % (timed_filename, i)
                    dfn = "%s.%d" % (timed_filename, i + 1)
                    if os.path.exists(sfn):
                        #print "%s -> %s" % (sfn, dfn)
                        if os.path.exists(dfn):
                            os.remove(dfn)
                        os.rename(sfn, dfn)
            else:
                for i in xrange(self.backupCount, 0, -1):
                    sfn = "%s.%d" % (timed_filename, i)
                    dfn = "%s.%d" % (timed_filename, i + 1)
                    if os.path.exists(sfn):
                        #print "%s -> %s" % (sfn, dfn)
                        if os.path.exists(dfn):
                            os.remove(dfn)
                        os.rename(sfn, dfn)

        dfn = timed_filename + '.1'
        if os.path.exists(self.baseFilename):
            os.rename(self.baseFilename, dfn)

        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        #If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or
                self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt


if __name__ == '__main__':
    set_level(logging.WARNING)
    console_on()
    filelog_on("app")
    remote_syslog_on()

    info('info')
    critical('critical')

    while True:
        time.sleep(0.1)
        error('error')
        debug('debug')
        warning('warning')
        info('info')
        critical('critical')

    # for i in xrange(1000):
    #     time.sleep(0.1)
    #     warning('warning')
