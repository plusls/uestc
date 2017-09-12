uestc
=====

一个电子科大的模块

涉及登录，查分，抢课等功能

uestc.exceptions
----------------

异常

uestc.login
-----------

登录模块

提供了登陆uestc的接口

登录失败会抛出异常

成功则返回一个request模块的session

.. code:: python

    >>> uestc.login('20160601*****','123456')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/mnt/c/Users/plusl/code/uestc/uestc/login.py", line 48, in login
        raise LoginError('密码错误')
    uestc.exceptions.LoginError: 密码错误
    >>> uestc.login('201606*********','******')
    <requests.sessions.Session object at 0x7f2a8e83eb00>

uestc.catch\_course
-------------------

抢课模块

catch\_course
~~~~~~~~~~~~~

抢课

例：

.. code:: python

    >>> import uestc
    >>> session=uestc.login('201606*********','******')
    >>> uestc.catch_course.catch_course(session, [998], [283884])
    >>> uestc.catch_course.catch_course(session, [998], [283884])
    ^C{283884: {998: 1}}

choose\_course
~~~~~~~~~~~~~~

选课并返回结果

get\_open\_entrance
^^^^^^^^^^^^^^^^^^^

获取选课通道

uestc.query
-----------

查询模块

get\_now\_semesterid
~~~~~~~~~~~~~~~~~~~~

获取当前学期id

get\_semesterid\_data
~~~~~~~~~~~~~~~~~~~~~

获取所有学期id的数据 返回一个学期id的list

例：

.. code:: python

    >>> uestc.query.get_semesterid_data(session)
    {'2008-2009-1': 21, '2008-2009-2': 22, '2009-2010-1': 19, '2009-2010-2': 20, '2010-2011-1': 17, '2010-2011-2': 18, '2011-2012-1': 15, '2011-2012-2': 16, '2012-2013-1': 13, '2012-2013-2': 14, '2013-2014-1': 1, '2013-2014-2': 2, '2014-2015-1': 43, '2014-2015-2': 63, '2015-2016-1': 84, '2015-2016-2': 103, '2016-2017-1': 123, '2016-2017-2': 143, '2017-2018-1': 163}

get\_score
~~~~~~~~~~

获取指定学期的分数

将会得到list与list的嵌套

返回值的最后一个元素为加权平均值

例：

.. code:: python

    >>> uestc.query.get_score(session, '2016-2017-2')
    [['2016-20172', 'B1400210', 'B1400210.D4', '大学体育II', '军事理论、体育', '1', '88', '--', '88', '4'], ['2016-20172', 'I9900520', 'I9900520.02', '钢琴演奏基础', '素质教育选修课（艺体类）', '2', '89', '--', '89'
    , '4'], ['2016-20172', 'I9900320', 'I9900320.01', '电影音乐赏析', '素质教育选修课（艺体类）', '2', '0', '--', '0', '0'], ['2016-20172', 'G0601240', 'G0601240.02', '程序设计（C与C++）', '专业核心课程', '4', '95',
     '--', '95', '4']]
