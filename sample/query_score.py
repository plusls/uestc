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
    name_black_list += []

    score = 0
    credit = 0
    for semester in semesterid_data:
        course_list += uestc.query.get_score(login_session, semester)
    #course_list.append(uestc.query.Course('', '', '', 'test', '', '16', '', '', '90', ''))
    for course in course_list:
        next_course = False
        for type_name in type_black_list:
            if type_name in course.type:
                next_course = True
                break
        for name in name_black_list:
            if name in course.name:
                next_course = True
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
    print(course_list)
    print('')
    print('')
    print('')
    print('重要科目:{}'.format(import_list))
    print('加权平均分:{}'.format(score))


if __name__ == '__main__':
    main()