# -*- coding:utf-8 -*-
'''电子科大抢课模块'''
import threading
import time
import requests
import signal
from .exceptions import CatchCourseError


__all__ = ["get_open_entrance"]
__CATCH_COURSE_URL = "http://eams.uestc.edu.cn/eams/stdElectCourse!batchOperator.action?profileId="

def __get_mid_text(text, left_text, right_text, start=0):
    '''获取中间文本'''
    left = text.find(left_text, start)
    if left == -1:
        return ('', -1)
    left += len(left_text)
    right = text.find(right_text, left)
    if right == -1:
        return ('', -1)
    return (text[left:right], right)


def __get_open_url_data(login_session, todo_list, ret_list, thread_lock, display_result):
    '''读取选课网页'''
    while True:
        thread_lock.acquire()
        if todo_list:
            now_get = todo_list.pop()
            if display_result and now_get % 100 == 0:
                print(now_get)

        else:
            thread_lock.release()
            break

        thread_lock.release()
        while True:
            try:
                response = login_session.get(__CATCH_COURSE_URL + str(now_get))
            except requests.exceptions.ConnectionError:
                raise CatchCourseError('无法连接电子科大网络')

            if '学号' in response.text:
                thread_lock.acquire()
                ret_list.append(now_get)
                thread_lock.release()

            #我也忘了下面这句干嘛的了
            if '(possibly due to' not in response.text:
                break


def get_open_entrance(login_session, start_entrance=0, end_entrance=2000, max_thread=50,\
display_result=False):
    '''获取选课通道 返回开放通道的list'''
    ret_list = []
    todo_list = []
    threads = []
    thread_lock = threading.Lock()
    for i in range(end_entrance, start_entrance - 1, -1):
        todo_list.append(i)
    for i in range(0, max_thread):
        threads.append(threading.Thread(target=__get_open_url_data, args=(login_session, todo_list,\
        ret_list, thread_lock, display_result)))
        threads[-1].start()

    #阻塞
    for thread in threads:
        thread.join()

    ret_list.sort()
    return ret_list

def choose_course(login_session, entrance, class_id, choose):
    '''选课'''
    postdata = {'operator0': '%s:%s:0' % (str(class_id), str(choose).lower())}
    response = login_session.post(__CATCH_COURSE_URL + str(entrance), data=postdata)
    info, end = __get_mid_text(response.text, 'text-align:left;margin:auto;">', '</br>')
    if end == -1:
        info += '网络错误！'
    info = info.replace(' ', '').replace('\n', '').replace('\t', '')
    info += '  id:%s  entrance:%s' % (class_id, entrance)
    return info

"""
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
"""