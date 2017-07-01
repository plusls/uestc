'''一个和电子科大有关的模块'''

from . import exceptions
from .login import login
from . import catch_course

__version__ = "1.0"
__author__ = "plusls<plusls@qq.com>"
__all__ = ['login', 'exceptions', 'catch_course']
