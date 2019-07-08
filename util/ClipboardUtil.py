# -*- coding: utf-8 -*-
import win32clipboard as w
import win32con

class Clipboard(object):
    """模拟windows设置剪贴板"""

    #读取剪贴板
    @staticmethod
    def getText():
        #打开剪贴板
        w.OpenClipboard()
        #获取剪贴板中的数据
        d = w.GetClipboardData(win32con.CF_TEXT)
        #关闭剪贴板
        w.CloseClipboard()
        #返回剪贴板数据给调用者
        return d

    #设置剪贴板内容
    @staticmethod
    def setText(aString):
        w.OpenClipboard()
        #清空剪贴板
        w.EmptyClipboard()
        #将数据aString写入剪贴板
        w.SetClipboardData(win32con.CF_UNICODETEXT,aString)
        w.CloseClipboard()
