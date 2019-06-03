# -*- coding:utf-8 -*-
"""电子科技大学登陆模块"""
import requests
from .exceptions import LoginError
from .encrypt import encrypt_AES

def __get_mid_text(text, left_text, right_text, start=0):
    """获取中间文本"""
    left = text.find(left_text, start)
    if left == -1:
        return ('', -1)
    left += len(left_text)
    right = text.find(right_text, left)
    if right == -1:
        return ('', -1)
    return (text[left:right], right)


def login(num, password):
    """登陆并返回一个requests模块的session"""
    url = 'https://idas.uestc.edu.cn/authserver/login?service='
    # 获取lt,execution
    new_session = requests.session()
    new_session.cookies.clear()
    response = new_session.get(url)

    lt_data, end = __get_mid_text(response.text, '"lt" value="', '"')
    if end == -1:
        raise LoginError('登录信息获取失败')

    execution, end = __get_mid_text(
        response.text, '"execution" value="', '"', end)
    key, end = __get_mid_text(response.text, 'pwdDefaultEncryptSalt = "', '";')
    password = encrypt_AES(b'a'*64 + password.encode('utf-8'), key.encode('utf-8'), b'a'*16).decode('utf-8')
    # 构造表格
    postdata = {
        'username': num,
        'password': password,
        'lt': lt_data,
        'dllt': 'userNamePasswordLogin',
        'execution': execution,
        '_eventId': 'submit',
        'rmShown': '1'
    }
    response = new_session.post(url, data=postdata)
    if '密码有误' in response.text:
        raise LoginError('密码错误')

    elif '验证码' in response.text:
        raise LoginError('出现验证码，请在浏览器登陆一次信息门户')

    response = new_session.get(
        'http://eams.uestc.edu.cn/eams/courseTableForStd.action')
    if '踢出' in response.text:
        click_url = __get_mid_text(response.text, '请<a href="', '"')
        new_session.get(click_url[0])
    return new_session
