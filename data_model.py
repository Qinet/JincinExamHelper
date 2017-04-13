#!/usr/bin/env python
# encoding: utf-8
import functools
import re
import json
import requests

import local_question_bank
from __init__ import logging
from __init__ import find_question_regex
from __init__ import online_question_bank_url


class ConnectionError(BaseException):
    pass

class ParsePageError(BaseException):
    pass
class DataController(object):
    def __init__(self, page_source_code):
        """
        :rtype:DataController
        """
        self.page_source_code = self.decode2unicode(page_source_code)
        self.question_bank = self.__load_question_bank_unicode()
        self.question_id_group = self.__question_id_group
        self.answer_choice_group = self.__answer_choice_group

    @staticmethod
    def decode2unicode(text2deecode):
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

    @property
    def __question_id_group(self):
        '''
        :return: tuple(question1_id, question2_id, ...)
        '''
        question_id_group = re.findall(find_question_regex, self.page_source_code)
        if question_id_group:
            logging.debug("Parse Question Success！")
            return tuple(zip(*question_id_group)[0])
        else:
            logging.debug("find_question_regex:%s" % find_question_regex)
            logging.error("Can not find question on page source code.")
            return ParsePageError

    @__question_id_group.setter
    def __question_id_group(self,object):
        self.__question_id_group = object

    def parse_page_checker(self):
        def decorater(func):
            def wrappedfunc(self, *args, **kwargs):
                if not self.question_id_group:
                    print "sdsds"
                return func(self, *args, **kwargs)

            return wrappedfunc

        return decorater

    def find_answer(self, question_id=""):
        for item in self.question_bank:
            if item.get("id", "") == unicode(question_id):
                return item

    @property
    def __answer_choice_group(self):
        if isinstance(self.question_id_group,ParsePageError):
            return None
        __answer_item_group = map(self.find_answer, self.question_id_group)
        __answer_choice_group = map(lambda x: x["answer"], __answer_item_group)
        return __answer_choice_group

    @property
    def question_answer_group(self):
        '''
        :return:  [(question1,answer_choice1), (question2,answer_choice2), (...)]
        '''
        return zip(self.question_id_group, self.answer_choice_group)

    @staticmethod
    def __load_question_bank_unicode():
        '''
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
        '''
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


if __name__ == '__main__':
    with open(r"source_code", "r") as page_source_code_file:
        page_source_code = page_source_code_file.read()
        get_answer = DataController(page_source_code=page_source_code)
        print get_answer.question_answer_group
        # print loadAnswerDb()['1394']['answer']
