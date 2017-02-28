import requests
def get_mid_text(text, left_text, right_text, start = 0):
    left = text.find(left_text, start)
    if left == -1:
        return None
    left += len(left_text)
    right = text.find(right_text, left)
    if right == -1:
        return None
    return (text[left:right], right)
def uestc_login(num, password):
    url = 'http://idas.uestc.edu.cn/authserver/login?service=http://portal.uestc.edu.cn/index.portal'
    #获取lt,execution
    u=requests.Session()
    u.cookies.clear()
    r=u.get(url)
    lt, end, = get_mid_text(r.text, '"lt" value="','"')
    execution, end, = get_mid_text(r.text, '"execution" value="','"',end)
    #构造表格
    postdata = {
        'username':num,
        'password':password,
        'lt':lt,
        'dllt':'userNamePasswordLogin',
        'execution':execution,
        '_eventId':'submit',
        'rmShown':'1'
        }
    r=u.post(url,data=postdata)
    #print(r.text)
    try:
        u.cookies.get_dict()['JSESSIONID']
    except Exception:
        return '请检查账号密码'
    return u
