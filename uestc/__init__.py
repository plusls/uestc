"""一个和电子科大有关的模块"""

from . import exceptions
from .login import login
from . import catch_course
from . import query

__version__ = "1.1.2.4"
__author__ = "plusls<plusls@qq.com>"
__all__ = ['login', 'exceptions', 'query']
