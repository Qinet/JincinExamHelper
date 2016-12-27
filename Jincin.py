#!/usr/bin/env python
# encoding: utf-8
import os
import re
import json

import sys

import requests

def getLocalAnswer(id):
    content = {}
    try:
        f = open("learn_db", 'r')
        line = f.readline().strip()
        while line:
            a = json.loads(line)
            content[a['id']] = a
            line = f.readline().strip()
    except:
        f=""
    finally:
        if f: f.close()
    if content.has_key(id):
        answer = content[id]['answer'].encode("utf-8")
        return answer
    return "?"

def getAnswerList(page):
    #print isinstance(page,unicode)
    questions = re.findall('<li class="ks_tm.*?" id="(\d*?)">(.*?)\n?</li>',page.encode("utf-8"))
    # print questions
    print "解析试卷问题成功！"
    answerList = []
    # print page
    # f=open("test.html",'w')
    # f.write(page.encode("utf-8"))
    # f.close()
    db = loadAnswerDb()
    i,j=0,0
    for id,question in questions:
        # print question
        if db.has_key(id):
            answer = db[id]['answer'].encode("utf-8")
            # print "from db"
            i+=1
        else:
            answer = getLocalAnswer(id)
            # print "from old_db"
            j+=1
        # print id+" "+question+" "+answer
        answerList.append((id,answer))
    # print answerList
    # print i,j
    return answerList

def collectAnswer(page):
    page = page.encode("utf-8")
    questions = re.findall('jsonQuestion=(.+?);\n\t\t\t \t\tshowQuestion\(jsonQuestion,(\d+?)\);', page)
    print questions
    rightAnswerList = re.findall('id="correctAnswer_(\d+?)".*?>(\w)</span>', page)
    print rightAnswerList
    temp = []
    rightTemp = {}
    for id, answer in rightAnswerList:
        rightTemp[id] = answer
    import json
    for question,id in questions:
        try:
            question = json.loads(question)
        except:
            try:
                question = "".join(question.split())
                question = json.loads(question)
            except:
                question = question.replace("title", "\"title\"")
                question = question.replace("name", "\"name\"")
                question = question.replace("text", "\"text\"")
                question = question.replace("options", "\"options\"")
                question = "".join(question.split())
                question = json.loads(question)
        print question
        question["id"] = id
        question["answer"]= rightTemp[id]
        print question
        temp.append(question)
    # for id,content in chooseList:
    #     content = content.replace("&nbsp;","")
    #     temp.append((id,content))
    for i in temp:
        content = json.dumps(i, ensure_ascii=False).encode("utf-8")
        with open('learn_db','a') as answerFile:
            answerFile.write(content+"\n")
    return 200

def loadAnswerDb():
    content = {}
    import QuestionBank
    try:
        r = requests.get(url="http://newyzu.tk/JinCinExamDb", timeout=5)
        if r.status_code!=200:
            raise Exception
        else:
            print "成功启用在线题库"

        for line in r.content.split('\n'):
            try:
                a = json.loads(line)
            except:
                print "error",a
            content[a['id']] = a
    except:
        print "启用本地题库"
        for line in QuestionBank.get().split('\n'):
            a = json.loads(line)
            content[a['id']] = a

    return content
if __name__=='__main__':
    print loadAnswerDb()['1394']['answer']
