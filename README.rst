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

    >>> uestc.login('2016060106001','123456')
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
~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~

获取选课通道
