#!/usr/bin/env python
# encoding: utf-8

import logging

from data_model import DataModel


class LogicController(object):
    def __init__(self, parent, page_source_code, **kwargs):
        self.parent = parent
        self.data_model = DataModel(page_source_code=page_source_code)
        self.enable_web_copy(enable=kwargs.get("enable_web_copy", True))

    def enable_web_copy(self, enable=True):
        if not enable:
            return
        self.parent.web_panel.run_script(self.data_model.enable_copy_script)
        self.parent.show_on_statusbar(message=u"正在分析...")
        logging.debug("Cookies:%s" % self.parent.web_panel.cookies)

    def get_parse_page_status(self):
        return self.data_model.parse_page_status

    def get_answer_choice_group_formated(self):
        return self.data_model.answer_choice_group_formated

    def get_error_message(self):
        return self.data_model.error_message

    def get_auto_select_answer_script(self):
        return self.data_model.auto_select_answer_script
