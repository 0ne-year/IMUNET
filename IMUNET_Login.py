# 内蒙古大学校园网登入
# 作者：Constantine
# 创作日期：2020年12月1日
# 版本：v2.0
# 修正时间：2020年12月10日
# 更新内容：自动获取wifi并且进行连接。

import requests
import time
# 保存包中写义的常量
import pywifi
from pywifi import const


def print_me():
    print("内蒙古大学校园网登入")
    print("作者：Constantine")
    print("创作日期：2020年12月1日")
    print("版本：v2.0")
    print("修正时间：2020年12月10日")
    print("更新内容：自动获取wifi并且进行连接。")


def web_sent(user, pwd):
    # 校园网登入链接
    url_go = "http://172.31.99.50:804/srun_portal_pc.php?ac_id=2&"  # 验证网站
    url_succeed = "http://172.31.99.50:804/srun_portal_pc_succeed.php"   #登入成功网站

    # 发送的数据
    user_data = {
        "action": "login",
        "username": user,
        "password": pwd,
        "ac_id": "2",
        # "save_me": "1",
        "ajax": "1"
    }

    # 向目标网站发送请求
    read = 0
    web_return = requests.post(url_go, data=user_data)
    while web_return.text == "Portal not response.":
        print(web_return.text, "\n网页无响应正在重新登入...")
        time.sleep(1)
        # web_return = requests.post(url_go, data=user_data)
        read += 1
        if read >= 7:
            print("服务器忙碌，请重启软件再试一次！！！")
            input("Press any key to continue . . .")
            return 11

    # 输出网页反馈结果
    if web_return.status_code == 200:
        if web_return.text[0:8] == "login_ok":
            print("登录成功！！！")
            # 获取ip和账户余额
            succeed = requests.post(url_succeed).text
            IP = succeed[succeed.rfind("IP地址：") + 76:succeed.rfind("已用流量：") - 59]
            Balance = succeed[succeed.rfind("帐户余额：") + 80:succeed.rfind("</span>")]
            while IP == '':
                succeed = requests.post(url_succeed).text
                IP = succeed[succeed.rfind("IP地址：") + 76:succeed.rfind("已用流量：") - 59]
                Balance = succeed[succeed.rfind("帐户余额：") + 80:succeed.rfind("</span>")]
            print("获取的IP为:", IP)
            print("账户余额：", Balance, "￥")
            input("Press any key to continue . . .")
        else:
            print(web_return.text[:web_return.text.rfind(".") + 1])
            input("Press any key to continue . . .")

# 以下为自动连接WiFi

def scan_wifi():

    # 扫苗附件wifi
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    iface.scan()  # 扫苗附件wifi
    time.sleep(1)
    basewifi = iface.scan_results()

    return basewifi


def connect_wifi():
    wifi = pywifi.PyWiFi()  # 创建一个wifi对象
    ifaces = wifi.interfaces()[0]  # 取第一个无限网卡
    print(ifaces.name())  # 输出无线网卡名称
    ifaces.disconnect()  # 断开网卡连接
    time.sleep(3)  # 缓冲3秒

    profile = pywifi.Profile()  # 配置文件
    profile.ssid = "IMUNET"  # wifi名称
    profile.auth = const.AUTH_ALG_OPEN  # 需要密码
    profile.akm.append(const.AKM_TYPE_NONE)  # 加密类型
    profile.cipher = const.CIPHER_TYPE_CCMP  # 加密单元
    # profile.key = '4000103000'  # wifi密码

    ifaces.remove_all_network_profiles()  # 删除其他配置文件
    tmp_profile = ifaces.add_network_profile(profile)  # 加载配置文件

    ifaces.connect(tmp_profile)  # 连接
    time.sleep(10)  # 尝试10秒能否成功连接
    isok = True
    if ifaces.status() == const.IFACE_CONNECTED:
        print("成功连接")
    else:
        print("失败")
    # ifaces.disconnect()  # 断开连接
    time.sleep(1)
    return isok


def requests_wifi():
    request_wifi = scan_wifi()
    if request_wifi != '':
        for i in request_wifi:
            if format(i.ssid) == 'IMUNET':
                print('成功连接IMUNET！！！')
                return 1
    print('没有发现IMUNET！！！')
    return 0


def main(user,pwd):
    if requests_wifi():
        print("请不要关闭程序，正在登录中...")
        time.sleep(1)
        web_sent(user, pwd)
    else:
        print("没有连接IMUNET，无法登录！！！")


# 执行指令
if __name__ == '__main__':
    print_me()
    user = "*******"    # 此处为用户名
    pwd = "****"        # 此处为密码
    main(user,pwd)
