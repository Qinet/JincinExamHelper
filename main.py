#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: Qin
@license: Apache Licence 
@contact: caofeng4750@gmail.com
@site: 
@software: PyCharm
@file: main.py
@time: 2016/1/9/0009 14:00
"""

import logging
import wx
import wx.html2 as webview
import Jincin
from __init__ import __version__, __update__, __author__, __title__
from logic_controller import LogicController

HOMEURL = "http://sso.njcedu.com/"
ABOUT = (u"Version    : {version}\n"
         u"Update     : {update} \n"
         u"Developer  : {author}"
         .format(**dict(version=__version__, update=__update__, author=__author__)))
logging.basicConfig(level=logging.DEBUG)
autoLearn = False
CAN_CHANGE = 1
CAN_NOT_CHANGE = 0


class WebPanel(wx.Panel):
    def __init__(self, parent=None):
        super(WebPanel, self).__init__(parent=parent)
        self.current_url = HOMEURL
        sizer = wx.BoxSizer(orient=wx.VERTICAL)
        btn_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.web_view = webview.WebView.New(parent=self)
        self.Bind(event=webview.EVT_WEBVIEW_LOADED, handler=self.webview_loaded, source=self.web_view)
        self.Bind(event=webview.EVT_WEBVIEW_NEWWINDOW, handler=self.open_new_window, source=self.web_view)

        btn_home = wx.Button(parent=self, label=u"主页", style=wx.BU_EXACTFIT)
        self.Bind(event=wx.EVT_BUTTON, handler=self.click_home_button, source=btn_home)
        btn_sizer.Add(item=btn_home, proportion=CAN_NOT_CHANGE, flag=wx.EXPAND | wx.ALL, border=2)

        btn_back_page = wx.Button(parent=self, label=u"<--", style=wx.BU_EXACTFIT)
        self.Bind(event=wx.EVT_BUTTON, handler=self.click_preview_page_button, source=btn_back_page)
        self.Bind(event=wx.EVT_UPDATE_UI, handler=self.check_can_goback, source=btn_back_page)
        btn_sizer.Add(item=btn_back_page, proportion=CAN_NOT_CHANGE, flag=wx.EXPAND | wx.ALL, border=2)

        btn_next_page = wx.Button(parent=self, label=u"-->", style=wx.BU_EXACTFIT)
        self.Bind(event=wx.EVT_BUTTON, handler=self.click_next_page_button, source=btn_next_page)
        self.Bind(event=wx.EVT_UPDATE_UI, handler=self.check_can_goforward, source=btn_next_page)
        btn_sizer.Add(item=btn_next_page, proportion=CAN_NOT_CHANGE, flag=wx.EXPAND | wx.ALL, border=2)

        btn_stop = wx.Button(parent=self, label=u"停止", style=wx.BU_EXACTFIT)
        self.Bind(event=wx.EVT_BUTTON, handler=self.click_stop_button, source=btn_stop)
        btn_sizer.Add(item=btn_stop, proportion=CAN_NOT_CHANGE, flag=wx.EXPAND | wx.ALL, border=2)

        btn_refresh = wx.Button(parent=self, label=u"刷新", style=wx.BU_EXACTFIT)
        self.Bind(event=wx.EVT_BUTTON, handler=self.click_refresh_page_button, source=btn_refresh)
        btn_sizer.Add(btn_refresh, proportion=CAN_NOT_CHANGE, flag=wx.EXPAND | wx.ALL, border=2)

        url_bar_title = wx.StaticText(parent=self, label=u"地址:")
        btn_sizer.Add(url_bar_title, proportion=CAN_NOT_CHANGE, flag=wx.CENTER | wx.ALL, border=2)

        self.location = wx.ComboBox(parent=self, value=wx.EmptyString, style=wx.CB_DROPDOWN | wx.TE_PROCESS_ENTER)
        self.location.Bind(event=wx.EVT_TEXT_ENTER, handler=self.enter_location)
        self.Bind(event=wx.EVT_COMBOBOX, handler=self.select_location, source=self.location)
        btn_sizer.Add(item=self.location, proportion=CAN_CHANGE, flag=wx.EXPAND | wx.ALL, border=2)

        sizer.Add(item=btn_sizer, proportion=CAN_NOT_CHANGE, flag=wx.EXPAND)
        sizer.Add(item=self.web_view, proportion=CAN_CHANGE, flag=wx.EXPAND)
        self.SetSizer(sizer=sizer)

        self.web_view.LoadURL(url=self.current_url)

    def open_new_window(self, event):
        # print event.GetURL()
        self.current_url = event.GetURL()
        self.location.SetValue(value=self.current_url)
        self.web_view.LoadURL(url=self.current_url)

    def webview_loaded(self, event):
        # The full document has loaded
        logging.debug(u"页面加载完成:%s" % event.GetURL())
        self.current_url = event.GetURL()
        self.location.SetValue(value=self.current_url)

    def select_location(self, event=None):
        # Control bar events
        url = self.location.GetStringSelection()
        self.web_view.LoadURL(url=url)

    def enter_location(self, event=None):
        url = self.location.GetValue()
        self.location.Append(url)
        self.web_view.LoadURL(url)

    def click_home_button(self, event=None):
        self.location.SetValue(HOMEURL)
        self.web_view.LoadURL(HOMEURL)

    def click_refresh_page_button(self, event=None):
        # print self.wv.GetPageSource()
        self.web_view.Reload()

    def click_preview_page_button(self, event=None):
        self.web_view.GoBack()

    def click_next_page_button(self, event=None):
        self.web_view.GoForward()

    def click_stop_button(self, event=None):
        self.web_view.Stop()

    def check_can_goback(self, event=None):
        event.Enable(self.web_view.CanGoBack())

    def check_can_goforward(self, event=None):
        event.Enable(self.web_view.CanGoForward())

    def run_script(self, script):
        self.web_view.RunScript(script)

    def get_page_source_code(self):
        return self.web_view.GetPageSource()

    def get_webview_status(self):
        return self.web_view.IsBusy()

    @property
    def cookies(self):
        # self.wv.RunScript("document.title = document.cookie.split(\"; \")")
        prev_title = self.web_view.GetCurrentTitle()
        self.web_view.RunScript("document.title = document.cookie.split(\"; \")")
        cookies = self.web_view.GetCurrentTitle()
        self.web_view.RunScript("document.title = %s" % prev_title)
        return cookies

    def get_cookies(self):
        return self.cookies


class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        (self.display_length_, self.display_height_) = wx.GetDisplaySize()
        self.frame_width_ = self.display_length_ * 90 / 100
        self.frame_height_ = self.display_height_ * 90 / 100
        self.answer_panel_width_ = self.frame_width_ * 15 / 100
        super(MainFrame, self).__init__(parent=parent, title=title, size=(self.frame_width_, self.frame_height_))

        self.splitter = wx.SplitterWindow(parent=self, style=wx.SP_LIVE_UPDATE)
        self.splitter.SetMinimumPaneSize(min=100)

        self.web_panel = WebPanel(parent=self.splitter)
        self.answer_panel = wx.Panel(parent=self.splitter)
        self.answers_box = wx.BoxSizer(orient=wx.VERTICAL)
        self.answers_box.Add(item=self.answer_panel)

        self.splitter.SplitVertically(window1=self.answer_panel, window2=self.web_panel,
                                      sashPosition=self.answer_panel_width_)

        self.Sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.Sizer.Add(item=self.splitter, proportion=CAN_CHANGE, flag=wx.EXPAND)

        auto_answer_button = wx.Button(parent=self, label=u"一键答题")
        auto_crawl_answers_button = wx.Button(parent=self, label=u"自动学习")
        self.Bind(event=wx.EVT_BUTTON, handler=self.click_search_answer, source=auto_answer_button)
        self.Bind(event=wx.EVT_BUTTON, handler=self.learn_answers, source=auto_crawl_answers_button)

        self.buttons_box = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.buttons_box.Add(item=auto_answer_button, proportion=CAN_NOT_CHANGE, flag=wx.LEFT | wx.RIGHT, border=5)
        if autoLearn:
            self.buttons_box.Add(item=auto_crawl_answers_button, proportion=CAN_NOT_CHANGE, flag=wx.LEFT | wx.RIGHT,
                                 border=5)
        self.Sizer.Add(item=self.buttons_box, proportion=CAN_NOT_CHANGE, flag=wx.TOP | wx.BOTTOM, border=5)

        menu = wx.Menu()
        menu_about = menu.Append(id=wx.ID_ABOUT, text=u"&关于", help=u" 关于本程序")
        menu_feedback = menu.Append(id=wx.ID_OPEN, text=u"&反馈", help=u" 反馈")
        self.Bind(event=wx.EVT_MENU, handler=self.show_about, source=menu_about)
        self.Bind(event=wx.EVT_MENU, handler=self.show_feedback, source=menu_feedback)
        menu_bar = wx.MenuBar()
        menu_bar.Append(menu, u"&帮助")
        self.SetMenuBar(menu_bar)

        self.Centre()

    def show_on_answer_panel(self, content2show):
        text = wx.StaticText(parent=self.answer_panel, label=content2show)
        text.SetFont(wx.Font(pointSize=self.answer_panel_width_/10, family=wx.ROMAN, style=wx.NORMAL, weight=wx.BOLD))
        self.answers_box.Add(item=text, proportion=CAN_NOT_CHANGE, border=5)

    def show_on_statusbar(self, message):
        if not self.GetStatusBar():
            self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText(message)

    def show_dialog(self, messgage, caption, style):
        dlg = wx.MessageDialog(parent=self, message=messgage, caption=caption, style=style)
        dlg.ShowModal()
        dlg.Destroy()

    def click_search_answer(self, event=None):
        page_source_code = self.web_panel.get_page_source_code()
        _logic_controller = LogicController(parent=self, page_source_code=page_source_code)
        _logic_controller.enable_web_copy()
        get_answers_result = _logic_controller.get_answers()
        logging.debug("result:%s" % str(get_answers_result))
        if get_answers_result:
            self.show_on_statusbar(message=u"匹配完成！")
            self.show_on_answer_panel("1")
            '''
                    show_answers_on_answer_panel
                    show_success_dialog
                    '''
            _logic_controller.auto_select_answers(func=self.web_panel.run_script)
            from __init__ import _HAS_FUND_MESSAGE
            self.show_dialog(messgage=_HAS_FUND_MESSAGE, caption=u"友情提示(●'◡'●)", style=wx.OK)
        else:
            self.show_on_statusbar(message=u"分析过程发生错误！")
            from __init__ import _NOT_FIND_MESSAGE
            self.show_dialog(messgage=_NOT_FIND_MESSAGE, caption=u"Error", style=wx.ICON_ERROR)


            # string = '  01.  '
            # index = 1
            # question_ids = []
            # question_answer = []
            # for question_id, answer in answer_list:
            #     string = string + answer + "  "
            #     # print id,answer
            #     question_ids.append(question_id)
            #     question_answer.append(answer)
            #     if index % 20 == 0:
            #         string = string + "\n  "
            #     if index % 5 == 0 and index < len(answer_list) - 1:
            #         string = string + "\n  " + str(index + 1).zfill(2) + ".  "
            #     index += 1
            #     # print index
            #     str_question_ids = ",".join(question_ids)
            #     str_question_answer = ",".join(question_answer)



            # self.statusbar.Destroy()

    def learn_answers(self, evt):
        if not autoLearn:
            dlg = wx.MessageDialog(self, u"自动学习功能可以忽略", u"", wx.OK)
            dlg.ShowModal()  # Shows it
            dlg.Destroy()  # finally destroy it when finished.
        page = self.web_panel.get_page_source_code()
        Jincin.collectAnswer(page)

    def show_about(self, evt):
        self.show_dialog(messgage=ABOUT, caption=u"关于本程序", style=wx.OK)

    def show_feedback(self, evt):
        self.show_dialog(messgage=u"https://github.com/Qinet/JincinExamHelper/issues", caption=u"反馈", style=wx.OK)


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(None, u"%s" % __title__)
    frame.Show()
    app.MainLoop()
