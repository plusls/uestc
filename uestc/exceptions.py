"""uestc异常模块"""

__all__ = ["LoginError", "QueryError"]

class LoginError(Exception):
    """登录异常"""

class QueryError(Exception):
    """查询成绩异常"""

