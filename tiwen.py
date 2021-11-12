import requests, json, base64, hashlib
import re
import os

class signin:
    def __init__(self, usr: str, pwd: str):
        requests.packages.urllib3.disable_warnings()
        self.usr = usr  # 手机号
        self.pwd = pwd  # 密码
        # 定义一个session()的对象实体s来储存cookie
        self.s = requests.Session()
        # self.s.proxies = {'http': 'http://localhost:8888', 'https': 'http://localhost:8888'}
        # self.s.verify = False
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; EBG-AN10 Build/HUAWEIEBG-AN10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36Ant-Android-WebView',
            'Authorization': 'BASIC '
                             'NTgyYWFhZTU5N2Q1YjE2ZTU4NjhlZjVmOmRiMzU3YmRiNmYzYTBjNzJkYzJkOWM5MjkzMmFkMDYyZWRkZWE5ZjY='
        }
        self.interUrl = 'https://h5api.xiaoyuanjijiehao.com/api/staff/interface'

    # 模拟登录
    def login(self):
        usr1 = "{\"LoginModel\":1,\"Service\":\"ANT\",\"UserName\":\"%s\"}" % self.usr
        log_url = "https://auth.xiaoyuanjijiehao.com/oauth2/token"
        data = {
            'password': hashlib.md5(self.pwd.encode()).hexdigest(),
            'grant_type': 'password',
            'username': str(base64.b64encode(usr1.encode('utf-8')), 'utf-8'),
        }
        req = self.s.post(log_url, headers=self.headers, data=data, verify=False)
        log_page = req.text
        # 获取请求头
        head = req.headers
        # 获取cookie
        cook = str(re.search("SERVERID=(.*?);Path=/", head.get("Set-Cookie")).group())
        cook = re.sub(";Path=/", "", cook)
        # print(cook)
        # 获取access_token
        token = json.loads(log_page.strip())["access_token"]
        # 更新header
        self.s.headers.update({'AccessToken': 'ACKEY_' + token})
        self.s.headers.update({'Cookie': cook})
        return self


class report:
    def __init__(self, usr: str, pwd: str):
        requests.packages.urllib3.disable_warnings()
        self.url = "https://h5api.xiaoyuanjijiehao.com/api/staff/interface"
        self.headers = {
            'Host': 'h5api.xiaoyuanjijiehao.com',
            'Connection': 'keep-alive',
            # 'Content-Length': '88',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; EBG-AN10 Build/HUAWEIEBG-AN10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36Ant-Android-WebView',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://h5api.xiaoyuanjijiehao.com',
            'X-Requested-With': 'com.zjelite.antlinkercampus',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://h5api.xiaoyuanjijiehao.com/h5/www1/11906/m_infocollect_formdesign/?x_ant_org=11906',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        self.si = signin(usr, pwd)
        self.si.login()
        # 获取报体温页面TaskCode

    def get_taskcode(self):
        # 拼凑请求头
        thisHeader = self.headers
        # thisHeader.update({'Content-Length': '88'})
        thisHeader.update({'AccessToken': self.si.s.headers.get("AccessToken")})
        thisHeader.update(
            {'Cookie': str(self.si.s.headers.get("AccessToken")) + "; " + str(self.si.s.headers.get("Cookie"))})
        # 请求内容
        querystring = {
            "Router": '/api/newcommtask/getstudenttasklist',
            "Method": 'POST',
            "Body": '{"UID":""}'
        }
        rep = requests.post(self.url, headers=thisHeader, json=querystring, verify=False)
        # 正则表达式获取taskcode
        notdealtaskcode = re.search("TaskCode(.*?)\",\"T", rep.text).group()
        taskcode = re.sub("TaskCode\":\"", "", notdealtaskcode)
        TaskCode = re.sub("\",\"T", "", taskcode)
        return TaskCode


def push_request(phone: str, password: str, name: str, stuID: str, academy: str, className:str):
    repo = report(phone, password)
    # 拼凑请求头
    thisHeader = {
        'Host': 'h5api.xiaoyuanjijiehao.com',
        'Connection': 'keep-alive',
        'Content-Length': '',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json, text / plain,*/*',
        'AccessToken': 'ACKEY_HICMVZXLNYGSTZ427FVHRW',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; EBG-AN10 Build/HUAWEIEBG-AN10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36Ant-Android-WebView',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://h5api.xiaoyuanjijiehao.com',
        'X-Requested-With': 'com.zjelite.antlinkercampus',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://h5api.xiaoyuanjijiehao.com/h5/www1/11906/m_infocollect_formdesign/?x_ant_org=11906',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': 'SERVERID=cae83636b39e2fba4f9912bb73912357|1611385614|1611385584'
    }
    # thisHeader.update({'Content-Length': '974'})
    thisHeader.update({'AccessToken': repo.si.s.headers.get("AccessToken")})
    thisHeader.update({'Cookie': str(repo.si.s.headers.get("Cookie"))})
    # print(thisHeader)
    data = {"Router":"/api/newcustomerform/submit","Method":"POST","Body":"{\"Field\":[{\"FieldCode\":\"disabled\","
                                                                          "\"Content\":\"XXX\"},"
                                                                          "{\"FieldCode\":\"disabled\","
                                                                          "\"Content\":\"YYY\"},"
                                                                          "{\"FieldCode\":\"disabled\","
                                                                          "\"Content\":\"XXX\"},"
                                                                          "{\"FieldCode\":\"disabled\","
                                                                          "\"Content\":\"XXX\"},"
                                                                          "{\"FieldCode\":\"disabled\","
                                                                          "\"Content\":\"XXX\"},"
                                                                          "{\"FieldCode\":\"disabled\","
                                                                          "\"Content\":\"XXX\"},{\"FieldCode\":\"\","
                                                                          "\"Content\":\"< 37.3℃\"},"
                                                                          "{\"FieldCode\":\"\",\"Content\":\"< 37.3℃\"},"
                                                                          "{\"FieldCode\":\"\","
                                                                          "\"Content\":\"< 37.3℃\"},"
                                                                          "{\"FieldCode\":\"\",\"Content\":\"否\"},"
                                                                          "{\"FieldCode\":\"\",\"Content\":\"否\"},"
                                                                          "{\"FieldCode\":\"\",\"Content\":\"否\"},"
                                                                          "{\"FieldCode\":\"\",\"Content\":\"否\"}],"
                                                                          "\"TaskCode\":\"aa\",\"TemplateId\":\"cc\"}"}
    body = json.loads(data["Body"])
    # 替换taskcode
    body["TaskCode"] = repo.get_taskcode()
    body["Field"][4]["Content"] = stuID
    body["Field"][5]["Content"] = name
    body["Field"][0]["Content"] = academy
    body["Field"][1]["Content"] = stuID[0:4]
    body["Field"][3]["Content"] = className
    body = json.dumps(body,ensure_ascii=False)
    data["Body"] = body
    # data["Body"] = data["Body"]
    print(data)
    # 发请求
    req = requests.post("https://h5api.xiaoyuanjijiehao.com/api/staff/interface", json=data, headers=thisHeader,verify=False)
    if req.json()["FeedbackText"] == '成功':
        return True
    return False

def main():
    option = json.loads(os.getenv('QDU_INFO'))
    result = push_request(**option)
    print(result)
    if not result:
        exit(-1)

if __name__ == '__main__':
    main()