# -*- coding: utf-8 -*-
from util.ParseExcel import *
from config.VarConfig import *
import time
from action.PageAction import *
import traceback

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#创建解析Excel对象

def TestSendMailWithAttachment():
    print u"启动浏览器"
    open_browser("firefox")
    maximize_browser()
    visit_url("http://mail.126.com")
    click("id", "lbNormal")
    ls =[1,2,3,4]
    print ls[2]
    switch_to_frame_index(ls[2])
    #switch_to_frame_index(3)
    time.sleep(3)

    wait = WaitUtil(driver)
    input_string("xpath","//input[@name='email']","nbcb666")
    print u"输入登录密码"
    input_string("xpath", "//input[@name='password']", "nbcbnbcb")
    print u"登录"
    click("id","dologin")
    time.sleep(5)
    switch_to_default_content()
    assert_title(u"网易邮箱")
    print u"登录成功"

    waitVisibilityOfElementLocated("xpath","//span[text()='写 信']")
    click("xpath","//span[text()='写 信']")
    print u"写信。。。"
    #收件人地址
    input_string("xpath","//div[contains(@id,'_mail_emailinput')]/input","110551444@qq.com")
    #主题
    input_string("xpath", "//input[contains(@id,'subjectInput')]", u"新邮件")
    print u"单击上传附件btn"
    click("xpath","//div[contains(@title,'600首')]")
    print u"上传附件"
    paste_string(u"c:\\t1.xlsx")
    press_enter_key()
    #waitVisibilityOfElementLocated("xpath","span[text()='上传完成']")

    waitFrameToBeAvailableAndSwitchToIt("xpath","//iframe[@tabindex = 1]")
    print u"输入邮件正文"
    input_string("xpath","/html/body","sdfsfsfsdfsfsdfsdf9s9fd")
    switch_to_default_content()
    print u"写信完成"

    click("xpath","//header//span[text()='发送']")
    time.sleep(3)
    assert_string_in_pagesource(u"发送成功")
    close_browser()

if __name__ == '__main__':
    TestSendMailWithAttachment()

