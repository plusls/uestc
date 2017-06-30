# -*- coding:utf-8 -*-
'''电子科大抢课模块'''
import threading
import time
import signal
import requests
from .exceptions import CatchCourseError


__all__ = ["get_open_entrance"]
__CATCH_COURSE_URL = "http://eams.uestc.edu.cn/eams/stdElectCourse!batchOperator.action?profileId="

__EXIT_THREAD = False
__CATCH_COURSE_RESULT = []


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

            # 我也忘了下面这句干嘛的了
            if '(possibly due to' not in response.text:
                break


def get_open_entrance(login_session, start_entrance=0, end_entrance=2000, max_thread=50,
                      display_result=False):
    '''获取选课通道 返回开放通道的list'''
    ret_list = []
    todo_list = []
    threads = []
    thread_lock = threading.Lock()
    for i in range(end_entrance, start_entrance - 1, -1):
        todo_list.append(i)
    for i in range(0, max_thread):
        threads.append(threading.Thread(target=__get_open_url_data, args=(login_session, todo_list,
                                                                          ret_list, thread_lock, display_result)))
        threads[-1].start()

    # 阻塞
    for thread in threads:
        thread.join()

    ret_list.sort()
    return ret_list


def choose_course(login_session, entrance, class_id, choose):
    '''选课'''
    postdata = {'operator0': '%s:%s:0' % (str(class_id), str(choose).lower())}
    response = login_session.post(
        __CATCH_COURSE_URL + str(entrance), data=postdata)
    info, end = __get_mid_text(
        response.text, 'text-align:left;margin:auto;">', '</br>')
    if end == -1:
        info += '网络错误！'
    info = info.replace(' ', '').replace('\n', '').replace('\t', '')
    info += '  id:%s  entrance:%s' % (class_id, entrance)
    return info


def __catch_course(login_session, entrance, class_id, thread_name,
                   thread_lock, choose=True, sleep=0):
    count = 0
    while True:
        info = choose_course(login_session, entrance, class_id, choose)
        count += 1
        print(thread_name + '正在进行第%d次尝试' % (count, ) + info)

        if __EXIT_THREAD or '成功' in info or '本批次' in info or '只开放给' in info or '学分已达上限' in info:
            thread_lock.acquire()
            __CATCH_COURSE_RESULT.append(info)
            thread_lock.release()
            break

        elif '网络错误' in info:
            print('jesession已经过期 正在获取jesession')
            while True:
                try:
                    response = login_session.get(
                        url=__CATCH_COURSE_URL + str(entrance))
                except requests.exceptions.ConnectionError:
                    print('获取获取jesession失败：网络错误！')
                    continue
                if '(possibly due to' not in response.text:
                    print('获取获取jesession成功')
                    break
                else:
                    print('获取获取jesession失败：傻逼你电抽风了！')
        time.sleep(sleep)


def catch_course(login_session, entrance_list, class_id_list, choose=True, sleep=0):
    '''抢课
    该函数执行后除非所有课程抢到，否则不会结束
    抢到所有课后会自动退出整个程序
    以及该函数会捕获中断信号
    中断后会输出选课结果'''
    global __EXIT_THREAD
    __EXIT_THREAD = False
    signal.signal(signal.SIGINT, catch_course_quit)
    signal.signal(signal.SIGTERM, catch_course_quit)
    threads = []
    thread_lock = threading.Lock()

    print('开始抢课')
    for class_id in class_id_list:
        for entrance in entrance_list:
            threads.append(
                threading.Thread(
                    target=__catch_course, args=(
                        login_session, int(entrance),
                        class_id, '[Thread-%d]' % (len(threads) + 1), thread_lock, True, 0)))
        threads[-1].start()

    for thread in threads:
        thread.join()

    catch_course_quit(None, None)


def catch_course_quit(signum, frame):
    '''键盘中断时调用'''
    global __EXIT_THREAD
    __EXIT_THREAD = True
    while threading.activeCount() > 1:
        pass
    print('正在退出程序')
    print('\n\n\n')
    print('抢课结果如下:')
    for i in range(len(__CATCH_COURSE_RESULT)):
        print(str(i) + '.' + __CATCH_COURSE_RESULT[i])

    exit()
