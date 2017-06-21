#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''电子科大抢课脚本'''
import getpass
import json
import optparse
import os
import smtplib
import time
from email.header import Header
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


import lxml.etree

import uestc_login
import xlsxwriter


def get_mid_text(text, left_text, right_text, start=0):
    '''获取中间文本'''
    left = text.find(left_text, start)
    if left == -1:
        return ('', -1)
    left += len(left_text)
    right = text.find(right_text, left)
    if right == -1:
        return ('', -1)
    return (text[left:right], right)


def start_query_score(session, semester, sleep_time=5, receivers=['plusls@qq.com'], filename='out.xlsx'):
    '''开始查询成绩'''
    old_score_data = query_score(session, semester)
    new_score_data = []
    while True:
        new_score_data = query_score(session, semester)
        if old_score_data != new_score_data:
            send_message(filename, new_score_data, receivers)
            old_score_data = new_score_data
            print('成绩已更新，已发送邮件通知')
        else:
            print(time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()) + '成绩并没有更新')
        time.sleep(sleep_time)


def send_message(filename, score_data, receivers):
    '''发送邮件'''
    sender = "plusls@qq.com"
    message = MIMEMultipart()
    message['From'] = Header('来自plusls', 'utf-8')
    message['To'] = Header('测试标题', 'utf-8')
    message['Subject'] = Header('你的成绩已经更新', 'utf-8')
    xlsxpart = MIMEApplication(open(filename, 'rb').read())
    xlsxpart.add_header('Content-Disposition', 'attachment', filename='成绩.xlsx')
    message.attach(xlsxpart)
    message.attach(MIMEText('你的成绩已经更新', 'plain', 'utf-8'))
    try:
        smtpObj = smtplib.SMTP_SSL()
        smtpObj.connect('smtp.qq.com', 465)
        smtpObj.login(sender, '15607516755a')
        smtpObj.sendmail(sender, receivers,message.as_string())
        smtpObj.quit()
        print('邮件已成功发送了')
    except smtplib.SMTPException as e:
        print(e)


def query_score(session, semester):
    '''查询成绩'''
    while True:
        try:
            response = session.get(URL[3] % __semesterid_data__[semester])
        except:
            continue
        if '学年' in response.text:
            break
    selector = lxml.etree.HTML(response.text)
    content = selector.xpath('/html/body/div/table/tbody/tr/td/text()')
    ret = []
    average_gpa = 0
    average_score = 0
    sum_credit = 0
    for i in range(len(content))[::10]:
        tmp = [content[i].replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '-')]
        for j in range(1,10):
            tmp.append(content[i + j].replace('\n', '').replace('\t', '').replace('\r', ''))
        sum_credit += int(tmp[5])
        average_score += int(tmp[8]) * int(tmp[5])
        average_gpa += float(tmp[9]) * int(tmp[5])
        ret.append(tmp)
    if len(content) > 0:
        average_score /= sum_credit
        average_gpa /= sum_credit
        tmp = [tmp[0]]
        tmp[1:] = ['NULL', 'NULL', '平均', 'NULL', 'NULL', 'NULL', 'NULL',
            '%.3f' % average_score,
            '%.3f' % average_gpa
        ]
        ret.append(tmp)
    return ret


def get_now_semesterid(session):
    '''获取当前semesterid'''
    while True:
        response = session.get(URL[0])
        try:
            data = get_mid_text(response.text, 'semesterId=', '&')
            ret = int(data[0])
        except Exception:
            print('获取当前semesterid失败，正在重试')
            continue
        return ret


def get_semesterid(session, now_semesterid):
    '''获取semesterid'''
    post_data = {
        'tagId':'semesterBar13572391471Semester',
        'dataType':'semesterCalendar',
        'value':str(now_semesterid),
        'empty':'false'
    }
    response = session.post(URL[2], post_data)
    response_text = response.text
    response_text = response.text.replace('yearDom', '"yearDom"')
    response_text = response_text.replace('termDom', '"termDom"')
    response_text = response_text.replace('semesters', '"semesters"')
    response_text = response_text.replace('schoolYear', '"schoolYear"')
    response_text = response_text.replace('id', '"id"')
    response_text = response_text.replace('name', '"name"')
    response_text = response_text.replace('yearIndex', '"yearIndex"')
    response_text = response_text.replace('termIndex', '"termIndex"')
    response_text = response_text.replace('semesterId', '"semesterId"')
    i = 0
    while True:
        if response_text.find('y' + str(i)) != -1:
            response_text = response_text.replace('y%d' % i, '"y%d"' % i)
            i += 1
        else:
            break
    semesterid_data = json.loads(response_text)['semesters']
    ret = {}
    for i in semesterid_data:
        for j in semesterid_data[i]:
            ret.update({'%s-%s' % (j['schoolYear'], j['name']):j['id']})
    return ret


def save_score(file_name, score_data):
    '''保存成绩'''
    try:
        os.remove(file_name)
    except Exception:
        pass
    workbook = xlsxwriter.Workbook(file_name)  #创建一个excel文件
    worksheet = workbook.add_worksheet()
    text = ['学年学期', '课程代码', '课程序号', '课程名称', '课程类别', '学分', '总评成绩', '补考总评', '最终', '绩点']
    for i in range(len(text)):
        worksheet.write(0, i, text[i])
    for i in range(len(score_data)):
        for j in range(len(score_data[i])):
            worksheet.write(i + 1, j, score_data[i][j])
    worksheet.set_column(0, len(score_data[i]), 15)
    workbook.close()


# 参数设置
parser = optparse.OptionParser()
parser.add_option('-n', '--num',
                  help='学号')
parser.add_option('-p', '--password',
                  help='密码')
parser.add_option('-t', '--time',
                  help='每次查询的延时 单位为秒')
parser.add_option('-s', '--semester',
                  help='学期 如 2016-2017-1')
parser.add_option('-a', '--all', action="store_true",
                  help="查询所有")
parser.add_option('-A', '--always', action="store_true",
                  help="一直查询")
(__options__, __args__) = parser.parse_args()
print(__options__)
if __options__.num is None:
    __options__.num = input('请输入你的学号:')
if __options__.password is None:
    __options__.password = getpass.getpass('请输入你的密码:')
while True:
    if __options__.semester is not None:
        if len(__options__.semester.split('-')) == 3:
            break
    __options__.semester = input('请输入你的学期:')
# 全局常量
URL = (
    'http://eams.uestc.edu.cn/eams/teach/grade/course/person.action',
    'http://eams.uestc.edu.cn/eams/teach/grade/course/person!search.action?semesterId=%d&projectType=',
    'http://eams.uestc.edu.cn/eams/dataQuery.action',
    'http://eams.uestc.edu.cn/eams/teach/grade/course/person!search.action?semesterId=%d'
)


#登陆
__session__ = uestc_login.login(__options__.num, __options__.password)
if __session__ is None:
    print('登陆失败')
    print(uestc_login.get_last_error())
    exit()
print('登陆成功')


#初始化查询
print('初始化查询...', end='')
__now_semesterid__ = get_now_semesterid(__session__)
__semesterid_data__ = get_semesterid(__session__, __now_semesterid__)
print('[OK]')

#查询
if __options__.always:
    start_query_score(__session__, __options__.semester)
else:
    print('查询.........', end='')
    __score_data__ = query_score(__session__, __options__.semester)
    save_score('out.xlsx', __score_data__)
    print('[OK]')
    print('数据已写入out.xlsx')
    #send_message(__score_data__, ['plusls@qq.com'])
