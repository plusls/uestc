import requests

global error_text, error
error_text = ['你的网炸了','密码错误']
error = 0


def get_mid_text(text, left_text, right_text, start = 0): #  获取中间文本
    left = text.find(left_text, start)
    if left == -1:
        return None
    left += len(left_text)
    right = text.find(right_text, left)
    if right == -1:
        return None
    return (text[left:right], right)


def login(num, password):
    url = 'http://idas.uestc.edu.cn/authserver/login?service=http://portal.uestc.edu.cn/index.portal'
    # 获取lt,execution
    u = requests.session()
    u.cookies.clear()
    # r=u.get(url)
    try:
        r = u.get(url)
    except requests.exceptions.ConnectionError:
        return None
    lt, end = get_mid_text(r.text, '"lt" value="', '"')
    execution, end = get_mid_text(r.text, '"execution" value="', '"', end)
    # 构造表格
    postdata = {
        'username':num,
        'password':password,
        'lt':lt,
        'dllt':'userNamePasswordLogin',
        'execution':execution,
        '_eventId':'submit',
        'rmShown':'1'
        }
    r = u.post(url, data = postdata)
    if '验证码' in r.text:
        return None
    return u


def get_last_error():
    return error_text[error]
