import requests
import threading
from uestc_login import uestc_login
def get_mid_text(text, left_text, right_text, start = 0):
    left = text.find(left_text, start)
    if left == -1:
        return None
    left += len(left_text)
    right = text.find(right_text, left)
    if right == -1:
        return None
    return (text[left:right], right)
def get_open_url_data(data):
    url = 'http://eams.uestc.edu.cn/eams/stdElectCourse!defaultPage.action?electionProfile.id='
    while data[0] < 1000:
        data[1].acquire()
        num = data[0]
        data[0] += 1
        data[1].release()
        r = data[2].get(url + str(num))
        if '学号' in r.text:
            data[1].acquire()
            data.append(num)
            data[1].release()

def get_open_url(u, threading_max = 50):
    data = [0,threading.Lock(),u]
    threads = []
    while data[0] < 1000:
        if len(threads) <= min(threading_max, 1000 - data[0]):
            threads.append(threading.Thread(target=get_open_url_data, args = (data, )))
            threads[len(threads) - 1].start()
    for i in threads:
        i.join()
    ret = data[3:]
    ret.sort()
    return ret

u = uestc_login('2016060106001', '')
if u != '请检查账号密码':
    a = get_open_url(u, threading_max = 50)
    print(a)
