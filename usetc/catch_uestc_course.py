#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''电子科大抢课脚本'''
import getpass
import optparse
import threading
import time
import signal

import uestc_login


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


def get_open_url_data(session, now):
    '''读取选课网页'''
    while now[0] < 2000:
        __lock__.acquire()
        num = now[0]
        now[0] += 1
        __lock__.release()
        if num % 100 == 0:
            print(num);
        while True:
            response = session.get(URL[0] + str(num))
            if '学号' in response.text:
                __lock__.acquire()
                now.append(num)
                __lock__.release()
            if '(possibly due to' not in response.text:
                break



def get_open_url(session, threading_max=50):
    '''获取抢课端口'''
    now = [0]
    while now[0] < 2000:
        if len(__threads__) <= min(threading_max, 2000 - now[0]):
            __threads__.append(threading.Thread(target=get_open_url_data, args=(session, now)))
            __threads__[len(__threads__) - 1].start()
    for i in __threads__:
        i.join()
    ret = now[1:]
    ret.sort()
    return ret


def catch_course(session, port, class_info, name, choose=True, sleep=0):
    '''抢课'''
    count = 0
    while True:
        postdata = {'operator0': '%s:%s:0' % (str(class_info), str(choose).lower())}
        response = session.post(URL[1] + str(port), data=postdata)
        info, end = get_mid_text(response.text, 'text-align:left;margin:auto;">', '</br>')
        if end == -1:
            info += '网络错误！'
        info = info.replace(' ', '').replace('\n', '').replace('\t', '')
        info += '  id:%s  port:%s' % (class_info, port)
        count += 1
        print(name + '正在进行第%d次尝试' % (count, ))
        print(info)
        if __quit_thread__[0] or '成功' in info or '本批次' in info or '只开放给' in info or '学分已达上限' in info:
            __lock__.acquire()
            __result__.append(info)
            __lock__.release()
            break
        elif '网络错误' in info:
            print('jesession已经过期 正在获取jesession')
            while True:
                try:
                    response = session.get(url=URL[0] + str(port)) 
                except Exception:
                    print('获取获取jesession失败：网络错误！')
                    continue
                if '(possibly due to' not in response.text:
                    print('获取获取jesession成功')
                    break
                else:
                    print('获取获取jesession失败：傻逼你电抽风了！')
        time.sleep(sleep)


def program_quit(signum, frame):
    '''键盘中断时调用'''
    __quit_thread__[0] = True
    while threading.activeCount() > 1:
        pass
    print('正在退出程序')
    print('\n\n\n')
    print('抢课结果如下:')
    for i in range(len(__result__)):
        print(str(i) + '.' + __result__[i])
    print('url:\n' + URL[0])
    print('port:\n' + str(__port__))
    exit()


def send_message(filename, score_data, receivers):
    '''发送邮件'''
    sender = "plusls@qq.com"
    message = MIMEMultipart()
    message['From'] = Header(' ', 'utf-8')
    message['To'] = Header('测试标题', 'utf-8')
    message['Subject'] = Header('你的成绩已经更新', 'utf-8')
    xlsxpart = MIMEApplication(open(filename, 'rb').read())
    xlsxpart.add_header('Content-Disposition', 'attachment', filename='成绩.xlsx')
    message.attach(xlsxpart)
    message.attach(MIMEText('你的课程已抢到', 'plain', 'utf-8'))
    try:
        smtpObj = smtplib.SMTP_SSL()
        smtpObj.connect('smtp.qq.com', 465)
        smtpObj.login(sender, '15607516755a')
        smtpObj.sendmail(sender, receivers,mesage.as_string())
        smtpObj.quit()
        print('邮件已成功发送了')
    except smtplib.SMTPException as e:
        print(e)



# 参数设置
parser = optparse.OptionParser()
parser.add_option('-n', '--num',
                  help="学号")
parser.add_option('-p', '--password',
                  help="密码")
parser.add_option('-P', '--port',
                  help="抢课端口(可选)，格式p1,p2,p3,")
parser.add_option('-t', '--time',
                  help="每次抢课的延时 单位为秒")
parser.add_option('-l', '--list',
                  help="课程编号 即?lesson.id=276731后的数字 格式：c1,c2,c3...")
parser.add_option('-g', '--getport', action="store_true",
                  help="只是输出端口号")
(__options__, __args__) = parser.parse_args()
print(__options__)
if __options__.num is None:
    __options__.num = input('请输入你的学号:')
if __options__.password is None:
    __options__.password = getpass.getpass('请输入你的密码:')
while __options__.getport is None:
    if __options__.list != None:
        __options__.list = __options__.list.split(',')
        for each in range(len(__options__.list)):
            try:
                __options__.list[each] = int(__options__.list[each])
            except ValueError:
                print('课程编号输入有误')
                break
        else:
            break
    print('课程编号 即?lesson.id=276731后的数字 格式：c1,c2,c3...')
    __options__.list = input('请输入课程编号:')

print(__options__.list)


# 全局变量
URL = (
    'http://eams.uestc.edu.cn/eams/stdElectCourse!defaultPage.action?electionProfile.id=',
    'http://eams.uestc.edu.cn/eams/stdElectCourse!batchOperator.action?profileId='
)
__threads__ = []
__lock__ = threading.Lock()
__session__ = uestc_login.login(__options__.num, __options__.password)
__result__ = []
__quit_thread__ = [False]
if __session__ is None:
    print(uestc_login.get_last_error())
    exit()
print('登陆成功')


#获取端口
if __options__.port != None:
    __port__ = __options__.port.replace(' ', '').split(',')

else:
    print('开始获取端口')
    __port__ = get_open_url(__session__, threading_max=100)
    __threads__ = []
    print('端口获取完毕')
if __options__.getport is True:
    print('url:\n' + URL[0])
    print('port:\n' + str(__port__))
    exit()


print('开始抢课')
signal.signal(signal.SIGINT, program_quit)
signal.signal(signal.SIGTERM, program_quit)
for __i__ in __options__.list:
    for __j__ in __port__:
        __threads__.append(
            threading.Thread(
                target=catch_course, args=(
                    __session__, int(__j__),
                    __i__, '[Thread-%d]' % (len(__threads__) + 1), True, 0
                    )
                )
            )
        __threads__[len(__threads__) - 1].start()


for each in __threads__:
    each.join()
