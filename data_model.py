#!/usr/bin/env python
# encoding: utf-8

import re
import json

import requests

import local_question_bank
from __init__ import logging
from __init__ import find_question_regex
from __init__ import online_question_bank_url
from __init__ import enable_copy_script, select_answer_script_template


def _decode2unicode(text2deecode):
    if isinstance(text2deecode, unicode):
        return text2deecode

    # TODO Add more frequently used charsets in charset_group when you need them.
    charset_group = ["utf-8", "gbk", "gb2312", "cp936"]
    for charset in charset_group:
        try:
            return text2deecode.decode(charset)
        except UnicodeDecodeError:
            pass
        except:
            raise
    else:
        logging.error("other charset error")
        raise UnicodeDecodeError


def _load_question_bank_unicode(online_question_bank_url=online_question_bank_url):
    """
    :return: List [item1, item2, ...]
    item = {
        "id": "1010",
        "answer": "A",
        "options": [
            {   "text": "OptionsA",
                "name": "A"
            },
            {   "text": ""OptionsB,
                "name": "B"
            },
            {   "text": "OptionsC",
                "name": "C"
            },
            {   "text": "OptionsD",
                "name": "D"
            }
        ],
        "title": "qustion_text"
    }
    """
    try:
        r = requests.get(url=online_question_bank_url, timeout=10)
        if r.status_code != 200:
            logging.debug("online_bank_status_code：%s" % r.status_code)
            raise ConnectionError
        else:
            logging.debug("Load online bank success!")
        question_bank_temp = r.content
    except Exception, e:
        logging.error("Load online bank fail;Error:%s" % e.message)
        logging.debug("Load local bank...")
        question_bank_temp = local_question_bank.get()

    index, item = (-1, None)
    __question_bank_unicode = ""
    try:
        __question_bank_unicode = [json.loads(item) for index, item in enumerate(question_bank_temp.split('\n')) if
                                   item.strip()]
    except Exception, e:
        logging.error("Load_online_bank;{0}:{1}".format(index, item))
        logging.error("Load_online_bank error reason:{0}".format(e.message))

    return __question_bank_unicode


class ConnectionError(BaseException):
    pass


class ParsePageError(BaseException):
    pass


class DataModel(object):
    question_bank = _load_question_bank_unicode(online_question_bank_url)
    logging.debug(question_bank[:100])

    def __init__(self, page_source_code=""):
        """
        :rtype:DataModel
        """
        self.parse_page_status = False
        self.error_message = u"Unknow Error"
        self.enable_copy_script = enable_copy_script
        self.select_answer_script_template = select_answer_script_template
        self.page_source_code = _decode2unicode(page_source_code)
        self.question_id_group = self.__get_question_id_group()
        self.answer_choice_group = self.__get_answer_choice_group()
        self.answer_choice_group_formated = self.get_answer_choice_group_formated()
        self.auto_select_answer_script = self.get_auto_select_answer_script()

    def __find_answer(self, question_id=""):
        for item in self.question_bank:
            if item.get("id", "X") == unicode(question_id):
                return item
        return None

    def __get_question_id_group(self):
        """
        :return: tuple(question1_id, question2_id, ...)
        """
        question_id_group = re.findall(find_question_regex, self.page_source_code)
        if question_id_group:
            logging.debug("Parse Question Success！")
            return tuple(zip(*question_id_group)[0])
        else:
            logging.debug("find_question_regex:%s" % find_question_regex)
            logging.error("Can not find question on page source code.")
            self.error_message = u"无法解析问题"
            return ()

    def __get_answer_choice_group(self):
        """
        :return: list [answer1, answer2, ...]
        """
        if not self.question_id_group:
            return []
        logging.debug(self.question_id_group)
        __answer_item_group = map(self.__find_answer, self.question_id_group)
        logging.debug("answer_item_group:{}".format(__answer_item_group))
        __answer_choice_group = map(lambda x: x["answer"] if x else "X", __answer_item_group)
        logging.debug("answer_choice_group:{}".format(__answer_choice_group))
        return __answer_choice_group

    def get_auto_select_answer_script(self):
        if not self.parse_page_status:
            return ""
        logging.debug(
            select_answer_script_template % (",".join(self.question_id_group), ",".join(self.answer_choice_group)))
        return select_answer_script_template % (",".join(self.question_id_group), ",".join(self.answer_choice_group))

    def get_answer_choice_group_formated(self):
        if not (self.question_id_group and self.answer_choice_group):
            return ""
        choice_group = self.answer_choice_group

        # TODO:这里无法直接用join；"+" 效率低,要实现动态连接
        choice_group_length = len(choice_group)
        pieces = 20
        group_length = choice_group_length / pieces  # 5
        choice_group_temp = []
        for index, choice in enumerate(choice_group):
            if index % group_length == 0:
                choice_group_temp.append("\n{index:0>2}.".format(index=index + 1))
            choice_group_temp.append("  ")
            choice_group_temp.append(choice)
        choice_group_formated = "".join(choice_group_temp)

        self.parse_page_status = True
        return choice_group_formated


if __name__ == '__main__':
    pass
