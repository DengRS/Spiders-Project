import itchat
from itchat.content import *
import time
import re
import os

INFO = {
    'user': None,
    'msg': None,
    'file': None,
}


@itchat.msg_register([FRIENDS])
def add_friend(msg):
    # 添加好友
    msg.user.verify()


@itchat.msg_register(TEXT, isGroupChat=True)
def at_msg(msg):
    if msg.isAt:
        itchat.send_msg(msg=msg.text, toUserName='filehelper')


@itchat.msg_register([TEXT, RECORDING, PICTURE])
def wechat_message(msg):
    # 接收到的消息
    if msg['Type'] == 'Text':
        INFO['msg'] = msg.text
    else:
        INFO['msg'] = msg['Type']
        msg.download(msg.fileName)
        INFO['file'] = msg.fileName
    if int(time.strftime('%H', time.localtime())) in [i for i in range(0, 9)]:
        user_name = itchat.search_friends(userName=msg['FromUserName'])
        name = user_name['Remarkname']
        if not name:
            name = user_name['NickName']
        itchat.send_msg(msg=f'☛微信自动回复☚: 休息时间，暂时无法回复', toUserName=name)


@itchat.msg_register([NOTE])
def monitor_message(msg):
    # 监听好友是否撤回消息
    content = msg['Content']
    pattern = re.compile(r"\<\!\[CDATA\[\"(.*)\" 撤回了一条消息\]\]\>")
    result = re.findall(pattern, content)
    if result:
        message = f"☛{result[0]}☚于{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}撤回一条信息: {INFO.get('msg')}"
        itchat.send_msg(msg=message, toUserName='filehelper')
        if INFO.get('file'):
            filePath = os.getcwd() + '\\' + INFO.get('file')
            if INFO.get('msg') == 'Recording':
                itchat.send_file(filePath, toUserName='filehelper')
            elif INFO.get('msg') == 'Picture':
                itchat.send_image(filePath, toUserName='filehelper')
            else:
                pass
            os.remove(filePath)
            INFO['file'] = None


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()


