'''电子科技大学登陆'''
import requests
__error__ = 0
__all__ = ['login', 'get_last_error']
def get_mid_text(text, left_text, right_text, start=0):
    '''获取中间文本'''
    left = text.find(left_text, start)
    if left == -1:
        return ('', -1)
    left += len(left_text)
    right = text.find(right_text, left)
    if right == -1:
        return ('', -1)
    return (text[left:right], right)


def login(num, password):
    '''登陆'''
    global __error__
    url = 'http://idas.uestc.edu.cn/authserver/login?service=http://portal.uestc.edu.cn/index.portal'
    # 获取lt,execution
    new_session = requests.session()
    new_session.cookies.clear()
    # r=u.get(url)
    try:
        response = new_session.get(url)
    except requests.exceptions.ConnectionError:
        __error__ = 0
        return None
    lt_data, end = get_mid_text(response.text, '"lt" value="', '"')
    if end == -1:
        __error__ = 0
        return None
    execution, end = get_mid_text(response.text, '"execution" value="', '"', end)
    # 构造表格
    postdata = {
        'username':num,
        'password':password,
        'lt':lt_data,
        'dllt':'userNamePasswordLogin',
        'execution':execution,
        '_eventId':'submit',
        'rmShown':'1'
        }
    response = new_session.post(url, data=postdata)
    if '验证码' in response.text:
        __error__ = 1
        return None
    return new_session


def get_last_error():
    '''获取最后一次登录失败的错误'''
    error_text = ['你的网炸了', '密码错误']
    return error_text[__error__]
