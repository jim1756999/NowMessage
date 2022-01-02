import math
import socket


class ChatClient:

    def __init__(self):
        print("初始化tcp客户端")
        self.sk = socket.socket()
        self.sk.connect(('127.0.0.1', 12323))

    # 验证登录
    def check_user(self, user, key):
        # 请求类型
        self.sk.sendall(bytes("1", "utf-8"))
        # 依次发送用户名密码
        self.send_string_with_length(user)
        self.send_string_with_length(key)
        # 获取服务器的返回值，"1"代表通过，“0”代表不通过
        check_result = self.recv_string_by_length(1)
        return check_result == "1"

    # 注册
    def register_user(self, user, key):
        # 请求类型
        self.sk.sendall(bytes("2", "utf-8"))
        # 依次发送用户名密码
        self.send_string_with_length(user)
        self.send_string_with_length(key)
        # 获取服务器的返回值，"0"代表通过，“1”代表已有用户名, "2"代表其他错误
        return self.recv_string_by_length(1)

    # 发送消息
    def send_message(self, message):
        self.sk.sendall(bytes("3", "utf-8"))
        self.send_string_with_length(message)

    ########################### 封装一些发送接受数据的方法 ##############################
    # 发送带长度的字符串
    def send_string_with_length(self, content):
        # 先发送内容的长度
        self.sk.sendall(bytes(content, encoding='utf-8').__len__().to_bytes(4, byteorder='big'))
        # 再发送内容
        self.sk.sendall(bytes(content, encoding='utf-8'))

    # 获取服务器传来的定长字符串
    def recv_string_by_length(self, len):
        return str(self.sk.recv(len), "utf-8")

    # 获取服务端传来的变长字符串，这种情况下服务器会先传一个长度值
    def recv_all_string(self):
        # 获取消息长度
        length = int.from_bytes(self.sk.recv(4), byteorder='big')
        b_size = 3 * 1024  # 注意utf8编码中汉字占3字节，英文占1字节
        times = math.ceil(length / b_size)
        content = ''
        for i in range(times):
            if i == times - 1:
                seg_b = self.sk.recv(length % b_size)
            else:
                seg_b = self.sk.recv(b_size)
            content += str(seg_b, encoding='utf-8')
        return content

    def send_number(self, number):
        self.sk.sendall(int(number).to_bytes(4, byteorder='big'))

    def recv_number(self):
        return int.from_bytes(self.sk.recv(4), byteorder='big')
