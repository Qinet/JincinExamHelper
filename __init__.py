#!/usr/bin/env python
# encoding: utf-8

import sys
import logging

logging.basicConfig(level=logging.DEBUG)

_ver = sys.version_info
is_py2 = (_ver[0] == 2)
is_py3 = (_ver[0] == 3)

if is_py2:
    from ConfigParser import RawConfigParser as ConfigParser
# TODO When wx library support Pthon3,use the code.
# if is_py3:
#     from configparser import ConfigParser

config = ConfigParser()
try:
    config.read("conf.cfg")
    enable_copy_script = config.get("DEFAULT", "EnableCopyScript")
    select_answer_script_template = config.get("DEFAULT", "SelectAnswerScriptTemplate")
    find_question_regex = config.get("DEFAULT", "FindQuestionRegEx")
    online_question_bank_url = config.get("DEFAULT", "OnlineQuestionBankURL")
except:
    enable_copy_script = 'document.body.onselectstart="";document.body.oncopy="";document.body.oncut="";document.body.oncontextmenu="";'
    select_answer_script_template = 'var strQuestionIds0="%s";var strQuestionAnswer0="%s";var strQuestionAnsers=strQuestionAnswer0.split(",");var questionIds=strQuestionIds0.split(",");var objRightCount=0;if(strQuestionAnsers.length>0){for(var i=0;i<questionIds.length;i++){if(strQuestionAnsers[i]!="0"){var name="radio_"+questionIds[i];var objs=document.getElementsByName(name);for(var j=0;j<objs.length;j++){if(objs[j].value==strQuestionAnsers[i]){objs[j].checked=true;var span=document.getElementById("correctAnswer_"+questionIds[i]);var span_right=document.getElementById("span_right_"+questionIds[i]);var span_wrong=document.getElementById("span_wrong_"+questionIds[i]);if(span!=null&&span_right!=null&&span_wrong!=null){if(span.innerText==strQuestionAnsers[i]){span_right.style.display="";span_wrong.style.display="none";objRightCount++;}else{span_right.style.display="none";span_wrong.style.display="";}}}}}}}doCommit(1,0);'

__author__ = u"Qinet"
__title__ = u"锦诚网助手"
__version__ = u'4.0.1'
__update__ = u"2016/11/23"

_HAS_FUND_MESSAGE = u"答案仅供参考！\n\n答题完毕后请随机抽取3-5个题目，检查与网上答案是否一致！\n"
_NOT_FIND_MESSAGE = u"未找到题目！\n"u"请确保在 考! 试! 页! 面! 点击一键答题！！！ \n\n"u"已知问题：个别Win7系统可能无法解析，请更换电脑后再次尝试！\n"u"温馨提示：Win8/Win10成功率更高哦！\n"
