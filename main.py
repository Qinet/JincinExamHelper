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
import time
import wx
import wx.html2 as webview

import Jincin

autoLearn = False
version = "4.0.1"
aboutContent = u"Version: "+unicode(version)+u"\nUpdate - 2016/11/23\nDeveloper：Qin"

class Panel(wx.Panel):
    def __init__(self, parent=None, frame=None):
        wx.Panel.__init__(self, parent, -1)

        self.current = "http://www.jincin.com"
        self.frame = frame
        if frame:
            self.titleBase = frame.GetTitle()

        sizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.wv = webview.WebView.New(self)
        # self.Bind(webview.EVT_WEBVIEW_NAVIGATING, self.OnWebViewNavigating, self.wv)
        self.Bind(webview.EVT_WEBVIEW_LOADED, self.OnWebViewLoaded, self.wv)
        self.Bind(webview.EVT_WEBVIEW_NEWWINDOW,self.openNewWindow,self.wv)


        btn = wx.Button(self, -1, u"主页", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnOpenButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        btn = wx.Button(self, -1, u"<--", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnPrevPageButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)
        self.Bind(wx.EVT_UPDATE_UI, self.OnCheckCanGoBack, btn)

        btn = wx.Button(self, -1, u"-->", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnNextPageButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)
        self.Bind(wx.EVT_UPDATE_UI, self.OnCheckCanGoForward, btn)

        btn = wx.Button(self, -1, u"停止", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnStopButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        btn = wx.Button(self, -1, u"刷新", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnRefreshPageButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        txt = wx.StaticText(self, -1, u"地址:")
        btnSizer.Add(txt, 0, wx.CENTER|wx.ALL, 2)

        self.location = wx.ComboBox(
            self, -1, "", style=wx.CB_DROPDOWN|wx.TE_PROCESS_ENTER)
        # self.location.AppendItems(['http://www.baidu.com',
        #                            'http://www',
        #                            'http://google.com'])
        self.Bind(wx.EVT_COMBOBOX, self.OnLocationSelect, self.location)
        self.location.Bind(wx.EVT_TEXT_ENTER, self.OnLocationEnter)
        btnSizer.Add(self.location, 1, wx.EXPAND|wx.ALL, 2)


        sizer.Add(btnSizer, 0, wx.EXPAND)
        sizer.Add(self.wv, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.wv.LoadURL(self.current)

    def openNewWindow(self,evt):
        # print evt.GetURL()
        self.current=evt.GetURL()
        self.location.SetValue(self.current)
        self.wv.LoadURL(self.current)

    def ShutdownDemo(self):
        # put the frame title back
        if self.frame:
            self.frame.SetTitle(self.titleBase)


    # WebView events
    def OnWebViewNavigating(self, evt):
        # this event happens prior to trying to get a resource
        if evt.GetURL() == 'http://www.microsoft.com/':
            if wx.MessageBox("Are you sure you want to visit Microsoft?",
                             style=wx.YES_NO|wx.ICON_QUESTION) == wx.NO:
                # This is how you can cancel loading a page.
                evt.Veto()

    def OnWebViewLoaded(self, evt):
        # The full document has loaded
        self.current = evt.GetURL()
        # print evt.GetTarget()
        self.location.SetValue(self.current)


    # Control bar events
    def OnLocationSelect(self, evt):
        url = self.location.GetStringSelection()
        self.wv.LoadURL(url)

    def OnLocationEnter(self, evt):

        url = self.location.GetValue()
        self.location.Append(url)
        self.wv.LoadURL(url)


    def OnOpenButton(self, event):
        self.location.SetValue("http://www.jincin.com")
        self.wv.LoadURL("http://www.jincin.com")

    def OnPrevPageButton(self, event):
        self.wv.GoBack()

    def OnNextPageButton(self, event):
        self.wv.GoForward()

    def OnCheckCanGoBack(self, event):
        event.Enable(self.wv.CanGoBack())

    def OnCheckCanGoForward(self, event):
        event.Enable(self.wv.CanGoForward())

    def OnStopButton(self, evt):
        self.wv.Stop()

    def OnRefreshPageButton(self, evt):
        # print self.wv.GetPageSource()
        self.wv.Reload()
    def getCookie(self):
        # self.wv.RunScript("document.title = document.cookie.split(\"; \")")
        prev_title = self.wv.GetCurrentTitle()
        self.wv.RunScript("document.title = document.cookie.split(\"; \")")
        cookies = self.wv.GetCurrentTitle()
        self.wv.RunScript("document.title = %s" % prev_title)
        return cookies

    def runScript(self,script):
        self.wv.RunScript(script)

    def getPageSource2(self):
        prev_title = self.wv.GetCurrentTitle()
        self.wv.RunScript("document.title = document.documentElement.outerHTML")
        pagesource = self.wv.GetCurrentTitle()
        self.wv.RunScript("document.title = %s" % prev_title)
        return  pagesource

    def getPageSource(self):
        return self.wv.GetPageSource()

    def getStatus(self):
        return self.wv.IsBusy()

    def getUrl(self,evt):
        return evt.GetURL()

class MySplitter(wx.SplitterWindow):
    def __init__(self, parent):
        wx.SplitterWindow.__init__(self, parent, style = wx.SP_LIVE_UPDATE,)
class MyFrame(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self, parent = parent, title = title, size=(1200,650))
        self.Centre()
        self.Sizer = wx.BoxSizer(wx.VERTICAL)

        self.splitter = MySplitter(self)
        self.splitter.SetMinimumPaneSize(100)
        self.leftPanel=wx.Panel(self.splitter)
        self.leftBox = wx.BoxSizer(wx.VERTICAL)
        self.leftBox.Add(self.leftPanel)
        self.rightPanel = Panel(self.splitter)
        self.splitter.SplitVertically(self.leftPanel, self.rightPanel, 150)
        self.Sizer.Add(self.splitter, 1, wx.EXPAND)
        b1 = wx.Button(self, label=u"一键答题")
        self.Bind(wx.EVT_BUTTON, self.OnSearchAnswer, b1)
        b2 = wx.Button(self, label=u"自动学习")
        self.Bind(wx.EVT_BUTTON, self.learnAnswers, b2)
        # self.editCookie = wx.TextCtrl(self, value="", size=(300, 30))
        # self.b3=wx.Button(self,label=u'一键看视频')
        # self.Bind(wx.EVT_BUTTON,self.viewVideo,self.b3)

        self.btnbox = wx.BoxSizer(wx.HORIZONTAL)
        self.btnbox.Add(b1, 0, wx.LEFT|wx.RIGHT, 5)
        if autoLearn:
            self.btnbox.Add(b2, 0, wx.LEFT|wx.RIGHT, 5)
        # self.btnbox.Add(self.editCookie, 0, wx.LEFT | wx.RIGHT, 5)
        # self.btnbox.Add(self.b3, 0, wx.LEFT|wx.RIGHT, 5)
        # self.btnbox.Add(self.b4, 0, wx.LEFT|wx.RIGHT, 5)
        self.Sizer.Add(self.btnbox, 0, wx.TOP|wx.BOTTOM, 5)
        # self.statusbar = self.CreateStatusBar()
        # self.statusbar.Destroy()
        filemenu= wx.Menu()
        menuAbout= filemenu.Append(wx.ID_ABOUT, u"&关于",u" 关于本程序")
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        menuFB = filemenu.Append(wx.ID_OPEN, u"&反馈",u" 反馈")
        self.Bind(wx.EVT_MENU, self.feedBack, menuFB)
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,u"&帮助")
        self.SetMenuBar(menuBar)

    # def viewVideo(self,evt):
    #     self.rightPanel.runScript("")
    def OnSearchAnswer(self,evt):
        self.rightPanel.runScript('document.body.onselectstart="";document.body.oncopy="";document.body.oncut="";document.body.oncontextmenu="";')
        if not self.GetStatusBar():
            self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText(u"正在分析.")
        wx.Sleep(1)
        self.statusbar.SetStatusText(u"正在分析..")
        wx.Sleep(1)
        self.statusbar.SetStatusText(u"正在分析...")
        print self.rightPanel.getCookie()
        page =  self.rightPanel.getPageSource()
        answerList = Jincin.getAnswerList(page)
        if not answerList:
            self.statusbar.SetStatusText(u"分析过程发生错误！")
            dlg = wx.MessageDialog(self, u"未找到题目！\n请确保在 考! 试! 页! 面! 点击一键答题！！！ \n\n已知问题：个别Win7系统可能无法解析，请更换电脑后再次尝试！\n温馨提示：Win8/Win10成功率更高哦！\n", "Error", wx.ICON_ERROR)
            dlg.ShowModal()  # Show it
            dlg.Destroy()  # finally destroy it when finished.
            return
        # print answerList
        # print 1
        self.statusbar.SetStatusText(u"正在匹配.")
        self.statusbar.SetStatusText(u"正在匹配..")
        time.sleep(1)
        self.statusbar.SetStatusText(u"正在匹配...")
        time.sleep(1)
        self.statusbar.SetStatusText(u"匹配完成！")

        string='  01.  '
        index=1
        QuestionIds=[]
        QuestionAnswer=[]
        for id,answer in answerList:
            string=string+answer+"  "
            # print id,answer
            QuestionIds.append(id)
            QuestionAnswer.append(answer)
            if index % 20 == 0:
                string = string + "\n  "
            if index%5==0 and index<len(answerList)-1:
                string = string+"\n  "+str(index+1).zfill(2)+".  "
            index = index+1
            # print index
            strQuestionIds=",".join(QuestionIds)
            strQuestionAnswer=",".join(QuestionAnswer)
        script = 'var strQuestionIds0="%s";var strQuestionAnswer0="%s";var strQuestionAnsers=strQuestionAnswer0.split(",");var questionIds=strQuestionIds0.split(",");var objRightCount=0;if(strQuestionAnsers.length>0){for(var i=0;i<questionIds.length;i++){if(strQuestionAnsers[i]!="0"){var name="radio_"+questionIds[i];var objs=document.getElementsByName(name);for(var j=0;j<objs.length;j++){if(objs[j].value==strQuestionAnsers[i]){objs[j].checked=true;var span=document.getElementById("correctAnswer_"+questionIds[i]);var span_right=document.getElementById("span_right_"+questionIds[i]);var span_wrong=document.getElementById("span_wrong_"+questionIds[i]);if(span!=null&&span_right!=null&&span_wrong!=null){if(span.innerText==strQuestionAnsers[i]){span_right.style.display="";span_wrong.style.display="none";objRightCount++;}else{span_right.style.display="none";span_wrong.style.display="";}}}}}}}doCommit(1,0);'%(strQuestionIds,strQuestionAnswer)
        print script
        self.rightPanel.runScript(script)
        text = wx.StaticText(self.leftPanel,-1,string)
        text.SetFont(wx.Font(pointSize=14, family=wx.ROMAN, style=wx.NORMAL, weight=wx.BOLD, underline=False,faceName="", encoding=wx.FONTENCODING_DEFAULT))
        self.leftBox.Add(text, 0, wx.LEFT|wx.RIGHT, 5)
        self.statusbar.Destroy()
        dlg = wx.MessageDialog(self, u"答案仅供参考！\n\n答题完毕后请随机抽取3-5个题目，检查与网上答案是否一致！\n", u"友情提示(●'◡'●)", wx.OK)
        dlg.ShowModal()  # Shows it
        dlg.Destroy()  # finally destroy it when finished.
    def learnAnswers(self,evt):
        if not autoLearn:
            dlg = wx.MessageDialog(self, u"自动学习功能可以忽略",u"", wx.OK)
            dlg.ShowModal()  # Shows it
            dlg.Destroy()  # finally destroy it when finished.
        page = self.rightPanel.getPageSource()
        Jincin.collectAnswer(page)
    def scrapeAnswers(self,evt):
        page = self.rightPanel.getPageSource()

    def OnAbout(self,e):
        # Create a message dialog box
        dlg = wx.MessageDialog(self, aboutContent, u"关于本程序", wx.OK)
        dlg.ShowModal() # Shows it
        dlg.Destroy() # finally destroy it when finished.
    def feedBack(self,e):
        dlg = wx.MessageDialog(self, u" https://github.com/Qinet/JincinExamHelper/issues", u"反馈", wx.OK)
        dlg.ShowModal() # Shows it
        dlg.Destroy() # finally destroy it when finished.

if __name__ == '__main__':
    app=wx.App()
    frame = MyFrame(None,u"锦诚网助手")
    frame.Show()
    app.MainLoop()
