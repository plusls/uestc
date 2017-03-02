#!/usr/bin/env python3
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
    while now[0] < 1000:
        __lock__.acquire()
        num = now[0]
        now[0] += 1
        __lock__.release()
        response = session.get(URL[0] + str(num))
        if '学号' in response.text:
            __lock__.acquire()
            now.append(num)
            __lock__.release()

def get_open_url(session, threading_max=50):
    '''获取抢课端口'''
    now = [0]
    while now[0] < 1000:
        if len(__threads__) <= min(threading_max, 1000 - now[0]):
            __threads__.append(threading.Thread(target=get_open_url_data, args=(session, now)))
            __threads__[len(__threads__) - 1].start()
    for i in __threads__:
        i.join()
    ret = now[1:]
    ret.sort()
    return ret

def catch_course(session, port, class_info, choose=True, sleep=0):
    '''抢课'''
    count = 0
    while True:
        postdata = {'operator0': '%s:%s:0' % (str(class_info), str(choose).lower())}
        response = session.post(URL[1] + str(port), data=postdata)
        info, end = get_mid_text(response.text, 'text-align:left;margin:auto;">', '</br>')
        if end == -1:
            info = '网络错误！'
        info = info.replace(' ', '').replace('\n', '').replace('\t', '')
        count += 1
        print('正在进行第%d次尝试    ' % (count, ))
        print(info)
        if __quit_thread__[0] or '成功' in info:
            __lock__.acquire()
            __result__.append(info)
            __lock__.release()
            break
        elif '网络错误' in info:
            print('jesession已经过期 正在获取jesession')
            while True:
                try:
                    session.get(url=URL[0] + str(port)) 
                except Exception:
                    print('获取获取jesession失败：网络错误！')
                    continue
                print('获取获取jesession成功')
                break
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
    exit()


# 参数设T
parser = optparse.OptionParser()
parser.add_option('-n', '--num',
                  help="学号")
parser.add_option('-p', '--password',
                  help="密码")
parser.add_option('-P', '--port',
                  help="抢课端口（任意一个，可以用-g获得）")
#parser.add_option('-t', '--time',
#                  help="每次抢课的延时 单位为秒")
parser.add_option('-g', '--getport', action='store_true',
                  help="获取抢课端口")
parser.add_option('-l', '--list',
                  help="课程编号 即?lesson.id=276731后的数字 格式：c1,c2,c3...")
(__options__, __args__) = parser.parse_args()
print(__options__)
if __options__.num is None:
    __options__.num = input('请输入你的学号:')
if __options__.password is None:
    __options__.password = getpass.getpass('请输入你的密码:')
while True:
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
    print('接下来输入课程编号')
    print('课程编号 即?lesson.id=276731后的数字 格式：c1,c2,c3...')
    __options__.list = input('请输入你的课程编号：')
print(__options__.list)
while True:
    try:
        __options__.port = int(__options__.port)
    except ValueError:
        __options__.port = input('请输入正确的抢课端口:')
        continue
    break


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

if __options__.getport:
    print('url:\n' + URL[0])
    print('port:\n' + str(get_open_url(__session__, threading_max=50)))
    exit()

print('开始抢课')
signal.signal(signal.SIGINT, program_quit)
signal.signal(signal.SIGTERM, program_quit)
for each in __options__.list:
    __threads__.append(
        threading.Thread(target=catch_course, args=(__session__, __options__.port, each, True, 0))
        )
    __threads__[len(__threads__) - 1].start()
for each in __threads__:
    each.join()