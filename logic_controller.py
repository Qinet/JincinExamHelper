# -*- coding: utf-8 -*-

"""
@author: Qinet
@contact: qinet.code@gmail.com
@site: https://github.com/Qinet
@license: Apache v2 License
@file: controller.py
@time: 2017/3/20 23:16
"""

import logging
from data_controller import DataController
from __init__ import enable_copy_script, select_answer_script_template


class LogicController(object):
    def __init__(self, parent, page_source_code):
        self.parent = parent
        self.page_source_code = page_source_code
        self.enable_copy_script = enable_copy_script
        self.select_answer_script_template = select_answer_script_template
        self.data_controller = DataController(page_source_code=self.page_source_code)

    def enable_web_copy(self):
        self.parent.web_panel.run_script(self.enable_copy_script)
        self.parent.show_on_statusbar(message=u"正在分析...")
        logging.debug("Cookies:%s" % self.parent.web_panel.cookies)

    def get_answers(self):
        answer_list =self.data_controller.question_answer_group
        logging.debug("answer_list:%s" % answer_list)
        if not answer_list:
            return None
        string = '  01.  '
        index = 1
        question_ids = []
        question_answer = []
        for question_id, answer in answer_list:
            string = string + answer + "  "
            # print id,answer
            question_ids.append(question_id)
            question_answer.append(answer)
            if index % 20 == 0:
                string = string + "\n  "
            if index % 5 == 0 and index < len(answer_list) - 1:
                string = string + "\n  " + str(index + 1).zfill(2) + ".  "
            index += 1
            # print index
            str_question_ids = ",".join(question_ids)
            str_question_answer = ",".join(question_answer)
        print zip(str_question_ids,str_question_answer)
        return (str_question_ids,str_question_answer)
    def auto_select_answers(self, func):
        # (question_ids, question_answer) =
        # func(self.select_answer_script_template%(question_ids, question_answer))
        return
