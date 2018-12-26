# uestc
一个电子科大的模块

涉及登录，查分，抢课等功能

## 安装

```python
pip3 install uestc
```

## 文档

### uestc.exceptions

异常

### uestc.login

登录模块

提供了登陆uestc的接口

登录失败会抛出异常

成功则返回一个request模块的session

```python
>>> uestc.login('20160601*****','123456')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/mnt/c/Users/plusl/code/uestc/uestc/login.py", line 48, in login
    raise LoginError('密码错误')
uestc.exceptions.LoginError: 密码错误
>>> uestc.login('201606*********','******')
<requests.sessions.Session object at 0x7f2a8e83eb00>
```

### uestc.catch_course

抢课模块

#### catch_course

抢课

例：

```python
>>> import uestc
>>> session=uestc.login('201606*********','******')
>>> uestc.catch_course.catch_course(session, [998], [283884])
>>> uestc.catch_course.catch_course(session, [998], [283884])
^C{283884: {998: 1}}
```

#### choose_course

选课并返回结果

#### get_open_entrance

获取选课通道

#### change_class_cash

修改选中的课程的权重

#### get_choose_class_list

获取选中的课程的列表

#### get_entrance_student_count

获取当前选课的学生数量

#### get_course_data

获取课程信息，包含自己投入的权重

#### get_platform_cash

获取各个平台剩余的权重

### uestc.query

查询模块

#### get_now_semesterid

获取当前学期id

#### get_semesterid_data

获取所有学期id的数据 返回一个学期id的list

例：

```python
>>> uestc.query.get_semesterid_data(session)
{'2008-2009-1': 21, '2008-2009-2': 22, '2009-2010-1': 19, '2009-2010-2': 20, '2010-2011-1': 17, '2010-2011-2': 18, '2011-2012-1': 15, '2011-2012-2': 16, '2012-2013-1': 13, '2012-2013-2': 14, '2013-2014-1': 1, '2013-2014-2': 2, '2014-2015-1': 43, '2014-2015-2': 63, '2015-2016-1': 84, '2015-2016-2': 103, '2016-2017-1': 123, '2016-2017-2': 143, '2017-2018-1': 163}
```

#### get_score

获取指定学期的分数

会得到course list

例：

```python
In [5]: uestc.query.get_score(s, '2017-2018-2')
Out[5]:
[Course(semester=2017-20182, code=E0805130, id=E0805130.03, name=计算机网络, type=专业核心课程, credit=3, default_score=92, resit_score=--, score=92, point=4),
 Course(semester=2017-20182, code=L0801910, id=L0801910.07, name=综合课程设计, type=实践类核心课程, credit=1, default_score=87, resit_score=--, score=87, point=4),
 Course(semester=2017-20182, code=E0800740, id=E0800740.03, name=数字逻辑, type=学科基础课程, credit=4, default_score=76, resit_score=--, score=76, point=3.1),
 Course(semester=2017-20182, code=K0802210, id=K0802210.07, name=数字逻辑综合实验, type=实践类核心课程, credit=1, default_score=80, resit_score=--, score=80, point=3.5),
 Course(semester=2017-20182, code=B2018410, id=B2018410.05, name=器械健身D, type=大学体育IV, credit=1, default_score=94, resit_score=--, score=94, point=4),
 Course(semester=2017-20182, code=A7304010, id=A7304010.02, name=成电讲坛（一）, type=核心通识课程, credit=1, default_score=通过, resit_score=--, score=通过, point=4),
 Course(semester=2017-20182, code=B1701620, id=B1701620.01, name=科技英语, type=C类专门用途类, credit=2, default_score=61, resit_score=--, score=61, point=1.6),
 Course(semester=2017-20182, code=G0801530, id=G0801530.01, name=数据库原理及应用, type=专业核心课程, credit=3, default_score=88, resit_score=--, score=88, point=4),
 Course(semester=2017-20182, code=A9905220, id=A9905220.02, name=电影鉴赏, type=核心通识课程, credit=2, default_score=82, resit_score=--, score=82, point=3.7)]
```

## sample

sample目录下为样例程序

### query_score.py

可以查询分数，过滤课程并自动计算加权平均分

