# -*- coding: utf-8 -*-
from util.ParseExcel import *
from config.VarConfig import *
import time
from action.PageAction import *
import traceback
from util.Log import *

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#创建解析Excel对象
excelObj = ParseExcel()
#将Excel数据文件加载到内存
excelObj.loadWorkBook(dataFilePath)

#用例或用例步骤执行结束后，向excel中写入执行结果
def writeTestResult(sheetObj,rowNo,colsNo,testResult,
                    errorInfo = None,picPah= None):
    #测试通过结果信息为绿色，失败为红色
    colorDict = {"pass":"green","faild":"red"}

    colsDict = {
        "testCase":[testCase_runTime,testCase_testResult],
        "caseStep":[testStep_runTime,testStep_testResult]}
    try:
        #在测试步骤sheet中，写入测试时间
        excelObj.writeCellCurrentTime(sheetObj,
                                      rowNo=rowNo,colsNo= colsDict[colsNo][0])
        #在测试步骤sheet中，写入测试结果
        excelObj.writeCell(sheetObj,content=testResult,
                           rowNo=rowNo, colsNo=colsDict[colsNo][1],
                           style = colorDict[testResult])
        if errorInfo and picPah:
            # 在测试步骤sheet中，写入异常数据
            excelObj.writeCell(sheetObj,content=errorInfo,
                               rowNo = rowNo,colsNo=testStep_errorInfo)

            # 在测试步骤sheet中，写入异常截图路径
            excelObj.writeCell(sheetObj, content=picPah,
                               rowNo=rowNo, colsNo=testStep_errorPic)
        else:
            #在测试步骤sheet中，清空异常信息单元格
            excelObj.writeCell(sheetObj,content="",
                               rowNo = rowNo,colsNo=testStep_errorInfo)
            # 在测试步骤sheet中，清空异常截图路径
            excelObj.writeCell(sheetObj, content="",
                               rowNo=rowNo, colsNo=testStep_errorPic)
    except Exception,e:
        logging.debug(u"写excel出错，%s",traceback.print_exc())


def TestSendMailWithAttachment():
    try:
        #根据Excel文件中的sheet名获取sheet对象
        caseSheet = excelObj.getSheetByName(u"测试用例")
        #获取测试用例sheet是否执行列对象
        isExecuteColumn = excelObj.getColumn(caseSheet,testCase_isExecute)
        #记录执行成功用例数量个数
        successfulCase = 0
        #记录需要执行的用例个数
        requiredCase = 0
        for idx,i in enumerate(isExecuteColumn[1:]):
            #因为用例sheet中第一行为标题行，无须执行
            #print i.value
            #循环遍历“测试用例”表中的测试用例，执行被设置为执行的用例
            if i== "y":
                requiredCase +=1
                #获取“测试用例”表中第idx+2行数据
                caseRow = excelObj.getRow(caseSheet,idx+2)
                #获取第idx+2行的“步骤sheet”单元格内容
                caseStepSheetName = caseRow[testCase_testStepSheetName - 1]
                #print caseStepSheetName
                #根据用例步骤名获取步骤Sheet对象
                stepSheet = excelObj.getSheetByName(caseStepSheetName)
                #获取步骤sheet中步骤数量
                stepNum = excelObj.getRowsNumber(stepSheet)
                #print stepNum
                #记录测试用例i 的步骤成功数
                successfulSteps = 0
                logging.info(u"开始执行测试用例" "%s"%caseRow[testCase_testCaseName-1])

                for step in xrange(2,stepNum+1):
                    #因为步骤sheet中的第一行为标题行，无需执行
                    #获取步骤sheet中第Step行对象
                    stepRow = excelObj.getRow(stepSheet,step)
                    #获取关键字作为调用函数的名
                    keyWord = stepRow[testStep_keyWords-1]
                    #获取元素定位方式
                    locationType = stepRow[testStep_locationType-1]
                    #获取定位表达式
                    locatorExpression = stepRow[testStep_locatorExpression-1]
                    #获取操作值作为调用函数的参数
                    operateValue = stepRow[testStep_operateValue-1]
                    #获取frame index
                    frameIndex = stepRow[testStep_frameIndex-1]

                    #将操作值为数字类型的数据转成字符串类型，方便字符串拼接
                    if isinstance(operateValue,long):
                        operateValue = str(operateValue)
                        print keyWord,locationType,locatorExpression,operateValue

                    exprssionStr=""
                    #构造需要执行的python语句，
                    #对应的是PageAction.py文件中的页面动作函数调用的字符串表示
                    if keyWord and operateValue and \
                        locationType is None and locatorExpression is None and frameIndex is None :
                        exprssionStr = keyWord.strip() + "(u'"+operateValue+"')"
                    elif keyWord and operateValue is None and \
                        locationType is None and locatorExpression is None and frameIndex is None:
                        exprssionStr = keyWord.strip()+"()"
                    elif keyWord and operateValue and locationType and\
                            locatorExpression is None and frameIndex is None:
                        exprssionStr = keyWord.strip() + \
                        "('"+locationType.strip()+"',u'"+operateValue+"')"
                    elif keyWord and operateValue and \
                        locationType and locatorExpression and frameIndex is None:
                        exprssionStr = keyWord.strip()+\
                        "('"+locationType.strip()+"','"+\
                                str(locatorExpression).replace("'",'"').strip()+\
                                       "',u'"+operateValue+"')"
                    elif keyWord and locatorExpression and locationType \
                            and operateValue is None and frameIndex is None:
                        exprssionStr = keyWord.strip() + \
                                       "('" + locationType.strip() + "','"+\
                                       str(locatorExpression).replace("'", '"').strip() + "')"
                    elif keyWord and locatorExpression and\
                        locationType is None and operateValue is None and frameIndex is None:
                        exprssionStr = keyWord.strip() + "(u'" + locatorExpression + "')"
                    elif keyWord and frameIndex and \
                        locationType is None and operateValue is None and\
                            locatorExpression is None:
                        frameIndex1 = str(frameIndex)
                        exprssionStr = keyWord.strip() + "("+frameIndex1+")"
                        print exprssionStr

                    #print exprssionStr
                    try:
                        #通过eval函数，将拼接的页面动作函数调用的字符串表示
                        #当成有效的python表达式执行，从而执行测试步骤的sheet中
                        #关键字PageAction.py文件中对应的映射方法
                        #来完成页面操作
                        eval(exprssionStr)
                        excelObj.writeCellCurrentTime(
                            stepSheet,rowNo=step,
                            colsNo=testStep_runTime)
                    except Exception,e:
                        #截取异常屏幕图片
                        capturePic=capture_screen()
                        #获取详细的异常堆栈信息
                        errorInfo = traceback.format_exc()
                        #在测试步骤sheet中写入失败信息
                        writeTestResult(
                            stepSheet,step,"caseStep",
                            "faild",errorInfo,capturePic)
                        logging.info(u"步骤",u"执行失败，错误信息:" ,(stepRow[testStep_testStepDescribe-1],errorInfo))

                    else:
                        #在测试步骤sheet中写入成功信息
                        writeTestResult(stepSheet,step,"caseStep","pass")
                        #每成功一步，successfulSteps变量自增+1
                        successfulSteps +=1

                        logging.info(u"步骤",u"执行通过",stepRow[testStep_testStepDescribe - 1])
                if successfulSteps == stepNum-1:
                    #当测试用例步骤sheet中所有步骤执行成功，将成功信息写入 测试用例sheet
                    #否则写入失败
                    writeTestResult(caseSheet,idx+2,"testCase","pass")
                    successfulCase +=1
                else:
                    writeTestResult(caseSheet,idx+2,"testCase","faild")
        logging.info(u"共%d条用例，%d条需要执行，本次执行通过%d条"\
            %(len(isExecuteColumn)-1,requiredCase,successfulCase))
    except Exception,e:
        #打印详细的异常堆栈信息
        print traceback.print_exc()
if __name__ == '__main__':
    TestSendMailWithAttachment()

