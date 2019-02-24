.. _header-n0:

uestc
=====

一个电子科大的模块

涉及登录，查分，抢课等功能

.. _header-n58:

免责声明
--------

1. 本项目提供的API均为UESTC教务系统提供的，不涉及对任何 UESTC
   教务系统网络及其任何相关子站的直接网络攻击，仅通过较高频率的模拟操作达到目的。

2. 本项目需要使用使用者的信息门户账户名及密码，但是保证不进行除\ **在本机获取
   cookies
   之外**\ 的用途。同时本项目不承担任何形式由于使用者操作失误导致的信息门户账户名及密码泄露，并由此直接或间接导致的、无限的损失。

3. 若因为使用者操作频次过高直接或间接导致的对教务系统的过大压力，由使用者承担其无限责任。使用者的
   cookies
   和账号信息会被教务系统记录，本项目作者不因此直接或间接承担任何责任。本项目可以保证默认参数不会引发本条所述的相关责任，但同时此保证不对使用者提供责任豁免条件。

4. 若因为其他问题导致不良后果，参考\ `中华人民共和国网络安全法 <http://www.npc.gov.cn/npc/xinwen/2016-11/07/content_2001605.htm>`__\ 。

5. 本项目的其他副本（包括但不仅限于离线储存、fork
   项目）在保持代码完全相同情况下，享受和本免责声明相同的免责条款；反之不然。因不当储存、复制和扩散导致的、无限的风险与责任由相关操作者承担，与本项目无关。

.. _header-n53:

安装
----

.. code:: python

   pip3 install uestc

.. _header-n6:

文档
----

.. _header-n7:

uestc.exceptions
~~~~~~~~~~~~~~~~

异常

.. _header-n9:

uestc.login
~~~~~~~~~~~

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

.. _header-n15:

uestc.catch_course
~~~~~~~~~~~~~~~~~~

抢课模块

.. _header-n17:

catch_course
^^^^^^^^^^^^

抢课

例：

.. code:: python

   >>> import uestc
   >>> session=uestc.login('201606*********','******')
   >>> uestc.catch_course.catch_course(session, [998], [283884])
   >>> uestc.catch_course.catch_course(session, [998], [283884])
   ^C{283884: {998: 1}}

.. _header-n21:

choose_course
^^^^^^^^^^^^^

选课并返回结果

.. _header-n23:

get\ *open*\ entrance
^^^^^^^^^^^^^^^^^^^^^

获取选课通道

.. _header-n25:

change\ *class*\ cash
^^^^^^^^^^^^^^^^^^^^^

修改选中的课程的权重

.. _header-n27:

get\ *choose*\ class_list
^^^^^^^^^^^^^^^^^^^^^^^^^

获取选中的课程的列表

.. _header-n29:

get\ *entrance*\ student_count
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

获取当前选课的学生数量

.. _header-n31:

get\ *course*\ data
^^^^^^^^^^^^^^^^^^^

获取课程信息，包含自己投入的权重

.. _header-n33:

get\ *platform*\ cash
^^^^^^^^^^^^^^^^^^^^^

获取各个平台剩余的权重

.. _header-n35:

uestc.query
~~~~~~~~~~~

查询模块

.. _header-n37:

get\ *now*\ semesterid
^^^^^^^^^^^^^^^^^^^^^^

获取当前学期id

.. _header-n39:

get\ *semesterid*\ data
^^^^^^^^^^^^^^^^^^^^^^^

获取所有学期id的数据 返回一个学期id的list

例：

.. code:: python

   >>> uestc.query.get_semesterid_data(session)
   {'2008-2009-1': 21, '2008-2009-2': 22, '2009-2010-1': 19, '2009-2010-2': 20, '2010-2011-1': 17, '2010-2011-2': 18, '2011-2012-1': 15, '2011-2012-2': 16, '2012-2013-1': 13, '2012-2013-2': 14, '2013-2014-1': 1, '2013-2014-2': 2, '2014-2015-1': 43, '2014-2015-2': 63, '2015-2016-1': 84, '2015-2016-2': 103, '2016-2017-1': 123, '2016-2017-2': 143, '2017-2018-1': 163}

.. _header-n43:

get_score
^^^^^^^^^

获取指定学期的分数

会得到course list

例：

.. code:: python

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

.. _header-n48:

sample
------

sample目录下为样例程序

.. _header-n50:

query_score.py
~~~~~~~~~~~~~~

可以查询分数，过滤课程并自动计算加权平均分
