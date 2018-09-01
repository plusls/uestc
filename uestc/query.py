# -*- coding:utf-8 -*-
"""查询信息"""
import json
from .exceptions import QueryError
from bs4 import BeautifulSoup, NavigableString
__all__ = ['get_now_semesterid', 'get_semesterid_data', 'get_score', 'Class']


class Course:
    def __init__(self, semester, code, id, name, type, credit, default_score, resit_score, score, point):
        self.semester = semester
        self.code = code
        self.id = id
        self.name = name
        self.type = type
        self.credit = credit
        self.default_score = default_score
        self.resit_score = resit_score
        self.score = score
        self.point = point

    def __str__(self):
        return 'Course(semester={}, code={}, id={}, name={}, type={}, credit={}, default_score={}, resit_score={}, score={}, point={})'.format(self.semester, self.code, self.id, self.name, self.type, self.credit, self.default_score, self.resit_score, self.score, self.point)
    __repr__ = __str__


def __get_mid_text(text, left_text, right_text, start=0):
    """获取中间文本"""
    left = text.find(left_text, start)
    if left == -1:
        return ('', -1)
    left += len(left_text)
    right = text.find(right_text, left)
    if right == -1:
        return ('', -1)
    return (text[left:right], right)


def get_score(login_session, semester):
    """查询成绩
    semester样例：2015-2016-2
    返回一个course list的嵌套"""
    semesterid_data = get_semesterid_data(login_session)
    response = login_session.get(
        'http://eams.uestc.edu.cn/eams/teach/grade/course/person!search.action?semesterId=%d' % semesterid_data[semester])
    soup = BeautifulSoup(response.text, 'html.parser')
    result = soup.find_all('td')
    ret = []

    for i in range(len(result)):
        result[i].string = "".join(
            list(filter(lambda x: isinstance(x, NavigableString), result[i].descendants)))
        # 特殊情况下,名为'td'的标签内部可能嵌套有其他标签
        # 如: "<td>微积分I<span style="color:red;">(重修)</span></td>"
        # 此时result[i].string值为None，在下一步中调用时会出现错误:"AttributeError: 'NoneType' object has no attribute 'replace'"
        # 通过上面的均一化处理，保证result[i].string不为None
        result[i].string = result[i].string.replace('\n', '').replace(
            '\r', '').replace('\t', '').replace(' ', '')
    for i in range(len(result) // 10):
        course_data = result[i * 10: i * 10 + 10]
        for j in range(len(course_data)):
            course_data[j] = course_data[j].string
        course = Course(*course_data)
        ret.append(course)

    return ret


def get_now_semesterid(login_session):
    """获取当前semesterid并返回int 失败则抛出异常"""
    response = login_session.get(
        'http://eams.uestc.edu.cn/eams/teach/grade/course/person.action')
    data = __get_mid_text(response.text, 'semesterId=', '&')
    if data[1] == -1:
        raise QueryError('当前semesterid获取失败')
    ret = int(data[0])
    return ret


def get_semesterid_data(login_session):
    """获取学期对应的semesterid信息 成功则返回dict"""
    post_data = {
        'dataType': 'semesterCalendar',
    }
    # 将得到的数据转换为json
    response = login_session.post(
        'http://eams.uestc.edu.cn/eams/dataQuery.action', post_data)
    response_text = response.text

    response_text = response_text.replace(':[{id', '":[{id')
    response_text = response_text.replace('}],y', '}],"y')
    response_text = response_text.replace('{y0', '{"y0')
    response_text = response_text.replace('yearDom', '"yearDom"')
    response_text = response_text.replace('termDom', '"termDom"')
    response_text = response_text.replace('semesters', '"semesters"')
    response_text = response_text.replace('schoolYear', '"schoolYear"')
    response_text = response_text.replace('id', '"id"')
    response_text = response_text.replace('name', '"name"')
    response_text = response_text.replace('yearIndex', '"yearIndex"')
    response_text = response_text.replace('termIndex', '"termIndex"')
    response_text = response_text.replace('semesterId', '"semesterId"')

    # json转为dict并提取为有用的数据
    try:
        semesterid_data = json.loads(response_text)['semesters']
    except json.decoder.JSONDecodeError:
        print(response_text)
        raise QueryError('当前账户登录已过期，请重新登录')
    ret = {}
    for i in semesterid_data:
        for j in semesterid_data[i]:
            ret.update({'%s-%s' % (j['schoolYear'], j['name']): j['id']})
    return ret


'''
def save_score(file_name, score_data):
    """保存成绩"""
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
'''
