# -*- coding:utf-8 -*-
"""电子科大抢课模块"""
import threading
import time
import signal
import requests
import traceback
import json
from bs4 import BeautifulSoup

__all__ = ["DEBUG", "get_open_entrance", "choose_course",
           "catch_course", "display_catch_course_result", "change_class_cash", "get_choose_class_list", "get_entrance_student_count", "get_course_data", "get_platform_cash"]
__CATCH_COURSE_POST_URL = "http://eams.uestc.edu.cn/eams/stdElectCourse!batchOperator.action?profileId="
__CATCH_COURSE_URL = "http://eams.uestc.edu.cn/eams/stdElectCourse!defaultPage.action?electionProfile.id="
__CHANGE_CLASS_CASH_URL = "http://eams.uestc.edu.cn/eams/stdVirtualCashElect!changeVirtualCash.action"
__ENTRANCE_CLASS_LIST_URL = "http://eams.uestc.edu.cn/eams/stdElectCourse!data.action?profileId="
__ENTRANCE_STUDENT_COUNT_URL = "http://eams.uestc.edu.cn/eams/stdElectCourse!queryStdCount.action?profileId="
__CLASS_DATA_URL = "http://eams.uestc.edu.cn/eams/electionLessonInfo.action?lesson.id="
__CASH_DATA_URL = "http://eams.uestc.edu.cn/eams/stdVirtualCashElect!getLessonCost.action?lessonId="
__PLATFORM_CASH_URL = "http://eams.uestc.edu.cn/eams/stdVirtualCashElect!getCurrentCash.action?profileId="
__EXIT_THREAD = False
__CATCH_COURSE_RESULT = []
__EXIT_TEXT_LIST = ['本批次', '只开放给', '学分已达上限', '现在未到选课时间', '超过限选门数', '冲突']
DEBUG = False
#__EXIT_TEXT_LIST = ['本批次', '只开放给', '学分已达上限']


class Course:
    def __init__(self, id, code, name, now_choose, max_choose, cash):
        self.code = id
        self.id = code
        self.name = name
        self.now_choose = now_choose
        self.max_choose = max_choose
        self.cash = cash

    def __str__(self):
        return 'Course(id={}, code={}, name={}, now_choose={}, max_choose={}, cash={})'.format(self.id, self.code, self.name, self.now_choose, self.max_choose, self.cash)
    __repr__ = __str__


def __get_open_url_data(login_session, todo_list, ret_list, thread_lock, display_result):
    """读取选课网页"""
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

            response = login_session.get(__CATCH_COURSE_URL + str(now_get))
            if '学号' in response.text:
                thread_lock.acquire()
                ret_list.append(now_get)
                thread_lock.release()

            # 我也忘了下面这句干嘛的了
            if '(possibly due to' not in response.text:
                break


def get_open_entrance(login_session, start_entrance=0, end_entrance=2000, max_thread=100,
                      display_result=False):
    """获取选课通道 返回开放通道的list
    start_entrance 最小的通道
    end_entrance 最大的通道
    max_thread 最大线程数
    display_result 是否实时返回扫描状态
    """
    ret_list = []
    todo_list = []
    threads = []
    thread_lock = threading.Lock()
    for i in range(end_entrance, start_entrance - 1, -1):
        todo_list.append(i)
    for i in range(0, max_thread):
        threads.append(threading.Thread(target=__get_open_url_data,
                                        args=(login_session, todo_list,
                                              ret_list, thread_lock, display_result)))
        threads[-1].start()

    # 阻塞
    for thread in threads:
        thread.join()

    ret_list.sort()
    return ret_list


def get_choose_class_list(login_session, entrance):
    """获取已选的课程列表
    entrance 任意一个通道
    """
    try:
        # 不写会报未到选课时间
        login_session.get('{}{}'.format(__CATCH_COURSE_URL, entrance))
        req_text = login_session.get(
            '{}{}'.format(__CATCH_COURSE_URL, entrance)).text
    except Exception as e:
        if DEBUG:
            traceback.print_exc()
        return []
    delete_list = [' ', '\r', '\t', ';', '=',
                   '[', ']', '"', 'true', 'electedIds', 'l']
    req_text = req_text.split('] = "self";\r\n\t\t\t\telectedIds')[
        1].split(';\r\n\t\t\t\tauditLessonIds')[0]
    for text in delete_list:
        req_text = req_text.replace(text, '')
    return req_text.split('\n')


def get_course_data(login_session, class_id):
    """获取课程信息
    失败则id为负 name为空
    """
    course = Course(-1, "", "", -1, -1, -1)

    try:
        # 处理重复登录
        while True:
            req_text = login_session.get(
                '{}{}'.format(__CASH_DATA_URL, class_id)).text
            if '当前用户存在重复登录的情况' not in req_text:
                break
    except Exception as e:
        if DEBUG:
            traceback.print_exc()
        return course
    course.cash = int(req_text)
    try:
        # 处理重复登录
        while True:
            req_text = login_session.get(
                '{}{}'.format(__CLASS_DATA_URL, class_id)).text
            if '当前用户存在重复登录的情况' not in req_text:
                break
    except Exception as e:
        if DEBUG:
            traceback.print_exc()
        return course
    course.id = class_id
    soup = BeautifulSoup(req_text, 'html.parser')
    td_list = soup.find_all('td')
    i = 0
    while i < len(td_list):
        text = td_list[i].string
        if text == '课程序号:':
            course.code = td_list[i + 1].string
            i += 1
        elif text == '课程名称:':
            course.name = td_list[i + 1].string
            i += 1
        elif text == '人数上限:':
            course.max_choose = int(td_list[i + 1].string)
            i += 1
        elif text == '实际人数:':
            course.now_choose = int(td_list[i + 1].string)
            i += 1
        i += 1

    # if DEBUG:
    #     print('course data:')
    #     for td in td_list:
    #         print(repr(td.string))
    #     print('------------')
    return course


def get_entrance_student_count(login_session, entrance):
    """获取当前通道所有课程选课学生人数
    entrance 当前通道
    """
    try:
        # 不写会报未到选课时间
        login_session.get('{}{}'.format(__CATCH_COURSE_URL, entrance))
        response = login_session.get('{}{}'.format(
            __ENTRANCE_STUDENT_COUNT_URL, entrance))
        student_count_text = response.text
    except Exception as e:
        if DEBUG:
            traceback.print_exc()
        return []
    # 返回结果
    # /*sc 当前人数, lc 人数上限,coc跨院系人数上限,ac/bc/cc是a/b/c平台课的人数*/
    # window.lessonId2Counts={'355454':{sc:152,lc:110,coc:0,ac:150,bc:4,cc:0}}
    student_count_text = student_count_text.split('window.lessonId2Counts=')[1]

    replace_list = ['sc', 'lc', 'coc', 'ac', 'bc', 'cc']

    for replace_text in replace_list:
        student_count_text = student_count_text.replace(
            '{}:'.format(replace_text), '"{}":'.format(replace_text))

    student_count_text = student_count_text.replace("'", '"')

    student_count_list = json.loads(student_count_text)
    return student_count_list

def get_platform_cash(login_session, entrance):
    """获取平台剩余权重
    entrance 任意一个通道
    """
    try:
        # 处理重复登录
        while True:
            req_text = login_session.get(
                '{}{}'.format(__CATCH_COURSE_URL, entrance)).text
            if '当前用户存在重复登录的情况' not in req_text:
                break
        req_text = login_session.get('{}{}'.format(__PLATFORM_CASH_URL, entrance)).text
        platform_cash_text = req_text
    except Exception as e:
        if DEBUG:
            traceback.print_exc()
        return []
    # 返回结果
    # { cashes : [{id : '615138', coins : '0', type : 'PLATFORMA'},{id : '615139', coins : '30', type : 'PLATFORMB'},{id : '615140', coins : '100', type : 'PLATFORMC'}] }
    replace_list = ['cashes', 'id', 'coins', 'type']
    for replace_text in replace_list:
        platform_cash_text = platform_cash_text.replace(
            '{} :'.format(replace_text), '"{}":'.format(replace_text))

    platform_cash_text = platform_cash_text.replace("'", '"')
    platform_cash_list = json.loads(platform_cash_text)['cashes']
    ret = {}
    for platform_cash in platform_cash_list:
        ret[platform_cash['type'].split('PLATFORM')[1]] = int(platform_cash['coins'])
    return ret

def get_entrance_class(login_session, entrance):
    """获取当前通道的选课
    可以获取当前通道的课程列表
    entrance 当前通道
    """
    try:
        # 不写会报未到选课时间
        login_session.get('{}{}'.format(__CATCH_COURSE_URL, entrance))
        response = login_session.get('{}{}'.format(
            __ENTRANCE_CLASS_LIST_URL, entrance))
        class_data_text = response.text
    except Exception as e:
        if DEBUG:
            traceback.print_exc()
        return []
    class_data_text = class_data_text[18:-1]
    replace_list = ['id', 'no', 'name', 'code', 'credits', 'courseId', 'startWeek', 'endWeek', 'courseTypeId', 'courseTypeName', 'courseTypeCode', 'scheduled', 'hasTextBook', 'period',  'weekHour', 'revertCount',
                    'withdrawable', 'textbooks', 'teachers', 'crossCollege', 'campusCode', 'campusName', 'remark', 'electCourseRemark', 'arrangeInfo', 'weekDay', 'weekStateText', 'weekState', 'startUnit', 'endUnit', 'rooms', 'examArrange', 'isRestudy']

    for replace_text in replace_list:
        class_data_text = class_data_text.replace(
            '{}:'.format(replace_text), '"{}":'.format(replace_text))

    class_data_text = class_data_text.replace("\\'", "\\\\'")

    class_data_text = class_data_text.replace(":'", ':"')
    class_data_text = class_data_text.replace("',", '",')
    class_data_text = class_data_text.replace("'}", '"}')

    class_data_list = json.loads(class_data_text)
    return class_data_list


def change_class_cash(login_session, entrance, class_id, cash):
    """该变课程权重
    class_id 课程id 可用 get_entrance_class获取详细信息
    cash 要修改成的选课权重
    """
    postdata = {'profileId': entrance,
                'lessonId': class_id, 'changeCost': cash}
    try:
        # 不写会报未到选课时间
        login_session.get(__CATCH_COURSE_URL + str(entrance))
        response = login_session.post(__CHANGE_CLASS_CASH_URL, data=postdata)
        info = response.text
    except Exception as e:
        if DEBUG:
            traceback.print_exc()
        info = ''

    if info == '':
        info = '网络错误！'
    info = info.replace(' ', '').replace('\n', '').replace('\t', '')
    info += '  id:%s  entrance:%s' % (class_id, entrance)
    return info


def choose_course(login_session, entrance, class_id, choose, cash=None):
    """选课 class_id为int
    class_id int 课程id
    choose bool 选课或退课
    score int 投分
    """
    postdata = {'operator0': '%s:%s:0' % (str(class_id), str(choose).lower())}
    if cash != None:
        postdata['virtualCashCost' + str(class_id)] = cash

    try:
        # 新版系统不允许提前选课 必须先访问这个页面
        # 否则会 非规定时间进行的选课，系统均视为测试数据，并将于正式选课前全部清除。
        login_session.get("http://eams.uestc.edu.cn/eams/stdElectCourse.action")
        # 不写会报未到选课时间
        login_session.get((__CATCH_COURSE_URL) + str(entrance))
        # 选课
        response = login_session.post(
            __CATCH_COURSE_POST_URL + str(entrance), data=postdata)
        info = response.text.partition(
            'text-align:left;margin:auto;">')[2].partition('</br>')[0]
    except Exception as e:
        if DEBUG:
            traceback.print_exc()
        info = ''

    # 现在未到选课时间格式不同 单独处理
    if '现在未到选课时间' in response.text:
        info = '现在未到选课时间，无法选课！'
    elif info == '':
        info = '网络错误！'
    info = info.replace(' ', '').replace('\n', '').replace('\t', '')
    info += '  id:%s  entrance:%s' % (class_id, entrance)
    return info


def __catch_course(login_session, entrance, class_id, thread_name,
                   thread_lock, ret_dict, choose, sleep, display_text, force):
    count = 0
    exit_thread = False
    while True:
        exit_thread = __EXIT_THREAD
        info = choose_course(login_session, entrance, class_id, choose)
        count += 1
        if display_text:
            thread_lock.acquire()
            print('%s正在进行第%d次尝试\n%s' % (thread_name, count, info))
            thread_lock.release()

        for exit_text in __EXIT_TEXT_LIST:
            if exit_text in info:
                if force == True and exit_text == '现在未到选课时间':
                    continue
                else:
                    ret_dict[class_id][entrance] = 1
                break
        if '成功' in info:
            ret_dict[class_id][entrance] = 0
        if ret_dict[class_id][entrance] != None:
            exit_thread = True

        thread_lock.acquire()
        if exit_thread:
            __CATCH_COURSE_RESULT.append(info)
            thread_lock.release()
            break

        thread_lock.release()
        time.sleep(sleep)


def catch_course(login_session, entrance_list, class_id_list, choose=True, sleep=0, max_thread=5,
                 display_text=False, force=False):
    """抢课
    该函数执行后除非所有课程抢到，否则不会结束
    以及该函数会捕获中断信号
    中断后会输出选课结果
    将会返回一个dict 表示选课结果
    entrance与class_id均为int
    若dict为0表示选课成功，为其他值则为失败"""
    global __EXIT_THREAD
    __EXIT_THREAD = False
    __CATCH_COURSE_RESULT.clear()
    signal.signal(signal.SIGINT, catch_course_quit)
    signal.signal(signal.SIGTERM, catch_course_quit)
    threads = []
    ret_dict = {}
    thread_lock = threading.Lock()

    for class_id in class_id_list:
        ret_dict[class_id] = {}
        for entrance in entrance_list:
            ret_dict[class_id][entrance] = None
            for i in range(max_thread):
                threads.append(
                    threading.Thread(
                        target=__catch_course, args=(
                            login_session, entrance,
                            class_id, '[%d-%d-Thread-%d]' % (
                                class_id, entrance, (i + 1)),
                            thread_lock, ret_dict, choose, sleep, display_text, force)))
                threads[-1].start()

    for thread in threads:
        thread.join()

    # 输出抢课结果
    if display_text:
        display_catch_course_result()

    for class_id in ret_dict:
        for entrance in ret_dict[class_id]:
            if ret_dict[class_id][entrance] is None:
                ret_dict[class_id][entrance] = 1

    return ret_dict


def catch_course_quit(signum, frame):
    """键盘中断时调用"""
    global __EXIT_THREAD
    __EXIT_THREAD = True
    while threading.activeCount() > 1:
        pass


def display_catch_course_result():
    """输出抢课结果"""
    print('正在停止抢课')
    print('\n\n\n')
    print('抢课结果如下:')
    for i in range(len(__CATCH_COURSE_RESULT)):
        print(str(i + 1) + '.' + __CATCH_COURSE_RESULT[i])
