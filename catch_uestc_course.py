import requests
import threading
import uestc_login
import optparse
def get_mid_text(text, left_text, right_text, start = 0):
    left = text.find(left_text, start)
    if left == -1:
        return None
    left += len(left_text)
    right = text.find(right_text, left)
    if right == -1:
        return None
    return (text[left:right], left)
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

def catch_course(u, port, id, choose = True):
    while True:
        postdata = {'operator0': '%s:%s:0' % (str(id), str(choose).lower())}
        r = u.get(url = 'http://eams.uestc.edu.cn/eams/stdElectCourse!defaultPage.action?electionProfile.id=917') #获取jesession
        r = u.post('http://eams.uestc.edu.cn/eams/stdElectCourse!batchOperator.action?profileId=917', data = postdata)
        (info, end) = get_mid_text(r.text, 'text-align:left;margin:auto;">', '</br>')
        info = info.replace(' ','').replace('\n','').replace('\t','')
        print(info)
        if '成功' in info:
            break


parser = optparse.OptionParser()
parser.add_option('-n', '--num',
                  help="学号")
parser.add_option('-p', '--password',
                  help="密码")
parser.add_option('-P', '--port',
                  help="抢课端口（任意一个，可以用-g获得）")
parser.add_option('-g', '--getport', action = 'store_true',
                  help="获取抢课端口")
(options, args) = parser.parse_args()
print(options)
if options.num == None:
    options.num = input('请输入你的学号:')
if options.password == None:
    options.password = input('请输入你的密码:')
while True:
    try:
        options.port = int(options.port)
    except Exception:
        options.port = input('请输入正确的抢课端口:')
        continue
    break
#parser.add_option('-l', '--list',help="s1:c1,s2:c2,...")
u = uestc_login.login(options.num, options.password)
if u == None:
    print(uestc_login.uestcget_last_error())
    exit()
if options.getport:
    print('url:\nhttp://eams.uestc.edu.cn/eams/stdElectCourse!defaultPage.action?electionProfile.id=')
    print('port:\n' + str(get_open_url(u, threading_max = 50)))
    exit()
catch_course(u, options.port, 276926, True)
catch_course(u, options.port, 276926, False)
catch_course(u, options.port, 276926, True)