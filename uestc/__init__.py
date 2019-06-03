"""一个和电子科大有关的模块"""
import __main__
if __main__.__doc__ != 'setup.py':
    from . import exceptions
    from .login import login
    from . import catch_course
    from . import query

__version__ = "1.2.2"
__author__ = "plusls<plusls@qq.com>"
__name__ = "uestc"
__doc__ = "一个和电子科大有关的模块"
__all__ = ['login', 'exceptions', 'query']
