"""uestc异常模块"""

__all__ = ["LoginError", "QueryScoreError"]

class LoginError(Exception):
    """登录异常"""

class QueryScoreError(Exception):
    """查询成绩异常"""

