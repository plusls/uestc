'''本程序可用来自动查分，自动过滤选修课并计算加权平均分
'''
import uestc
import argparse
import json


def check_args(parser, args):
    if args.username is None:
        parser.error('请输入学号')
    if args.password is None:
        parser.error('请输入密码')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username',
                        help='用户名')
    parser.add_argument('--password',
                        help='密码')

    args = parser.parse_args()
    check_args(parser, args)

    login_session = uestc.login(args.username, args.password)
    semesterid_data = uestc.query.get_semesterid_data(login_session)
    course_list = []
    import_list = []
    type_black_list = ['交叉通识', '核心通识', '选修', '体育', '学科前沿课', '创新与拓展项目']
    type_black_list += []

    name_black_list = []
    name_black_list += ['实习']

    type_white_list = ['思想政治', '学科通识', '学科基础', '学科拓展']
    name_white_list = ['军事理论', '英语m', '程序设计（C与C++）', '计算机网络', '数据库原理及应用', '软件工程及应用',
                       '计算机系统结构', '汇编语言与微机接口技术',
                       '综合素质实践Ⅰ', '综合素质实践Ⅱ', '数字逻辑综合实验', '综合课程设计',
                       '计算机组成原理综合实验', '计算机系统结构综合实验', 
                       '汇编语言与微机接口技术综合实验', '系统级软件综合课程设计', 
                       '软件开发综合实验']

    score = 0
    credit = 0
    for semester in semesterid_data:
        course_list += uestc.query.get_score(login_session, semester)
    course_list.append(uestc.query.Course('', '', '', '英语', '', '16', '', '', '90', ''))

    is_black = False

    for course in course_list:
        if is_black:
            next_course = False
            for type_name in type_black_list:
                if type_name in course.type:
                    next_course = True
                    break
            for name in name_black_list:
                #print(name)
                if name in course.name:
                    next_course = True
                    break
        else:
            next_course = True
            for type_name in type_white_list:
                if type_name in course.type:
                    next_course = False
                    break
            for name in name_white_list:
                #print(name)
                if name in course.name:
                    next_course = False
                    break

        if next_course is False:
            try:
                score += int(course.score)*float(course.credit)
                credit += float(course.credit)
            except Exception as e:
                print(type(e), e)
                print(course)
            import_list.append(course)
    score /= credit

    course_list_str = '\n'
    for course in course_list:
        course_list_str += '---------------\n'
        course_list_str += 'name:{}\n'.format(course.name)
        course_list_str += 'score:{}\n'.format(course.score)
        course_list_str += 'point:{}\n'.format(course.point)
        course_list_str += 'credit:{}\n'.format(course.credit)
        course_list_str += '---------------\n'

    print(course_list_str)
    #print(course_list_str)
    print('')
    print('')
    print('')
    import_list_str = '\n'
    for course in import_list:
        import_list_str += '---------------\n'
        import_list_str += 'name:{}\n'.format(course.name)
        import_list_str += 'score:{}\n'.format(course.score)
        import_list_str += 'point:{}\n'.format(course.point)
        import_list_str += 'credit:{}\n'.format(course.credit)
        import_list_str += '---------------\n'

    print('重要科目:{}'.format(import_list_str))
    print('加权平均分:{}'.format(score))


if __name__ == '__main__':
    main()
