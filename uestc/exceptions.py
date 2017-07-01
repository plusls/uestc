"""uestc异常模块"""

__all__ = ["LoginError", "CatchCourseError"]

class LoginError(Exception):
    """登录异常"""


class CatchCourseError(Exception):
    """抢课异常"""

